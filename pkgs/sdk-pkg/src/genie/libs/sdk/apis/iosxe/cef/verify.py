import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.normalize import GroupKeys

# pyATS
from pyats.utils.objects import find, R


# CEF
from genie.libs.sdk.apis.iosxe.cef.get import get_cef_repair_path_of_route

log = logging.getLogger(__name__)

def is_routing_repair_path_in_cef(
    device,
    prefix,
    max_time=60,
    check_interval=10,
    vrf='default',
    address_family='ipv4',
):
    """ Verify 'repair path' is presente in express forwarding

        Args:
            device ('obj'): Device object
            route ('str'): Route address
            max_time ('int'): Max time in seconds retrieving and checking output
            check_interval ('int')
            vrf ('str'): VRF name
            address_family ('str'): Address family
        Raises:
            None
        Returns:
            True
            False
    """

    timeout = Timeout(max_time=max_time, interval=check_interval)

    while timeout.iterate():
        is_present = get_cef_repair_path_of_route(
            device=device,
            prefix=prefix,
            vrf=vrf,
            address_family=address_family,
        )
        if is_present:
            return True

        timeout.sleep()

    return False


def verify_cef_internal_label_stack(device, vrf, prefix, stack, max_time=60, 
                                    check_interval=15):
    """ Verify stack is programmed for prefix

        Args:
            device (`obj`): Device object
            vrf (`str`): VRF to check
            prefix (`str`): Prefix to check
            stack (`list`): Stack list to verify exists
            max_time (`int`): Maximum time to keep checking
            check_interval (`int`): How long to wait between checks

        Raises:
            N/A

        Returns:
            True/False
    """
    reqs = R(
        [
            "vrf",
            "(?P<vrf>{vrf})".format(vrf=vrf),
            "address_family",
            "(?P<address_family>.*)",
            "prefix",
            "(?P<prefix>.*)",
            "output_chain",
            "tag_midchain",
            "(?P<tag_midchain>.*)",
            "label",
            "(?P<label>.*)"
        ]
    )

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show ip cef vrf {vrf} {prefix} internal'\
                        .format(vrf=vrf, prefix=prefix))
        except SchemaEmptyParserError:
            log.info("Parser output is empty")
            timeout.sleep()
            continue

        stack_copy = list(stack)
        found = find([out], reqs, filter_=False, all_keys=True)
        if found:
            for label in found[0][0]:
                for stack_item in stack_copy:
                    if str(stack_item) in label:
                        # If item found, break to prevent else block from running
                        stack_copy.remove(stack_item)
                        break
                else:
                    # If the label is not any of the stack_items break
                    # to prevent running next else block
                    break
            else:
                # If items exist in stack copy that means the stack
                # from output had less items than expected
                if not stack_copy:
                    return True
                else:
                    log.info(
                        'The following labels are not in the output: {labels}'
                            .format(labels=stack_copy))

        timeout.sleep()
    return False

def verify_cef_outgoing_interface(device, vrf, dst_pfx, out_intf,
                                   max_time=15, check_interval=5):
    """Verify outgoing interfaces for a particular prefix in cef

        Args:
            device (`obj`): Device object
            vrf (`str`): Vrf
            dst_pfx (`str`): destination prefix
            out_intf(`list`): List of outgoing interface to be checked,
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
            
        Returns:
            True
            False
        True if outgoing interfaces is as expected, false in all other cases
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        res=1
        try:
            out = device.parse("show ip cef vrf {vrf} {dst_pfx}"\
                        .format(vrf=vrf, dst_pfx=dst_pfx))
        except SchemaEmptyParserError:
            pass
        if out:
            try:
                intfs=out.q.get_values('outgoing_interface')
                for intf in out_intf:
                    if intf in intfs:
                        log.info(
                            "Got the expected outgoing interface {intf}"\
                                .format(intf=intf))
                    else:
                        log.info("Outgoing interface {intf} not found"\
                            .format(intf=intf))
                        continue
                return True
            except KeyError:
                pass
        timeout.sleep()
    return False

def verify_cef_uid_on_active_standby(device):
    
    """ Verify cef id on both active and standby device
        Args:
            device('obj'): device 
        returns:
            True if cef uid is same on both active and standby, false in all other cases
    """

    try:
        active_uid=device.parse("show cef uid")
        output=device.execute('show cef uid', target="standby")
        stanby_uid=device.parse("show cef uid", output=output)
    except SchemaEmptyParserError:
        raise SchemaEmptyParserError(
            "Failed to parse commands"
        )
    active_client_key_node=active_uid.q.get_values('client_key_nodes')[0]
    standby_client_key_node=stanby_uid.q.get_values('client_key_nodes')[0]
    active_uid_table_entry = active_uid.q.get_values('uid_table_entries')[0]
    standby_uid_table_entry = stanby_uid.q.get_values('uid_table_entries')[0]
    return ((active_client_key_node == standby_client_key_node) and \
           (active_uid_table_entry == standby_uid_table_entry))
           
def verify_cef_path_sets_summary(device):
    """ Verify cef path sets summary on active and standby device
        Args:
            device('obj'): device
        returns:
            True if cef path set uid is same on both active and standby, false in all other cases
    """
    try:    
        output = device.parse("show cef path sets summary")
    except SchemaEmptyParserError:
        raise SchemaEmptyParserError(
            "Failed to parse commands"
        )

    uids=output.q.get_values('path_set_id')    
    # verify uid to be same on active and standby devices
    for uid in uids:
    
        # Path Set Id 0x00000001 - gets 00000001
        u_id=uid.split("x")[1]
        try:
            active_uid=device.parse(f"show cef path set id {u_id} detail | in Replicate oce:")
            out=device.execute(f"show cef path set id {u_id} detail | in Replicate oce:", target="standby")
            standby_uid=device.parse(f"show cef path set id {u_id} detail | in Replicate oce:", output=out)
        except SchemaEmptyParserError:
            raise SchemaEmptyParserError(
                "Failed to parse commands"
            )
        active_u_id=active_uid.q.get_values('uid')
        standby_u_id=active_uid.q.get_values('uid')
        if not ((set(active_u_id) == set(standby_u_id))):
            return False
    return True