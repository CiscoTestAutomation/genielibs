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


def verify_cef_internal_label_stack(device, vrf, prefix, stack, max_time=60, check_interval=15):
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
            out = device.parse('show ip cef vrf {vrf} {prefix} internal'.format(vrf=vrf, prefix=prefix))
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
                    log.info('The following labels are not in the output: {labels}'
                             .format(labels=stack_copy))

        timeout.sleep()
    return False
