"""Common verify functions for mpls"""

# Python
import logging

# pyats
from pyats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Mpls
from genie.libs.sdk.apis.iosxe.mpls.get import get_mpls_ldp_peer_state

log = logging.getLogger(__name__)


def verify_mpls_forwarding_table_outgoing_label(
    device, ip, expected_label="", same_as_local=False, 
    max_time=30, check_interval=10):
    """ Verify local and remote binding labels for ipv4

        Args:
            device (`obj`): Device object
            ip (`str`): IP address
            expected_label (`str`): Expected label
            same_as_local (`bool`): 
                True if verify outgoing labels with local label
                False if verify outgoing labels with expected label
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
        Returns:
            result (`bool`): Verified result
    """
    cmd = 'show mpls forwarding-table {}'.format(ip)
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        result = True
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{}':\n{}".format(cmd, e))
            result = False
            timeout.sleep()
            continue

        reqs = R(['vrf', '(.*)', 
                'local_label', '(?P<local_label>.*)', 
                'outgoing_label_or_vc', '(?P<outgoing_label>.*)', 
                'prefix_or_tunnel_id', '(?P<prefix>.*)',
                'outgoing_interface', '(?P<interface>.*)',
                'next_hop', '(?P<next_hop>.*)'])
        found = find([out], reqs, filter_=False, all_keys=True)

        if found:
            keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={}, 
                                        source=found, all_keys=True)
            for route in keys:
                if same_as_local:
                    log.info("Interface {route[interface]} has local label "
                            "'{route[local_label]}' and outgoing label "
                            "'{route[outgoing_label]}'".format(route=route))
                    if str(route['outgoing_label']) != str(route['local_label']):
                        result = False
                else:
                    log.info("Interface {route[interface]} outgoing label is "
                            "'{route[outgoing_label]}', exepected to have label "
                            "'{expected}'".format(route=route, expected=expected_label))
                    if str(route['outgoing_label']) != str(expected_label):
                        result = False
        else:
            log.error("Could not find any mpls route for {}".format(ip))
            result = False

        if result is True:
            return result

        timeout.sleep()
 
    return result


def is_interface_igp_sync_mpls_enabled(
    interface, device, vrf="", parsed_output=""
):
    """ Verifies if interface has LDP IGP sync enabled 
        from command 'show mpls ldp igp sync'
        
        Args:
            parsed_output ('dict')  : Output from parser
            interface ('str')       : Interface being checked
            vrf  ('str')            : vrf name
            device ('str')          : Device to be executed commands
        Raises:
            None

        Returns
            True
            False

    """

    if not parsed_output:
        try:
            parsed_output = device.parse(
                "show mpls ldp igp sync interface {intf}".format(
                    intf=interface
                )
            )
        except SchemaEmptyParserError:
            raise SchemaEmptyParserError(
                "Fail to parse 'show mpls ldp igp sync "
                "interface {intf}' command".format(intf=interface)
            )

    vrf = vrf if vrf else "default"

    try:
        igp_synchronization_enabled = (
            parsed_output["vrf"]
            .get(vrf, {})
            .get("interface", {})
            .get(interface, {})
            .get("ldp", {})
            .get("igp_synchronization_enabled", False)
        )

        sync_achieved = (
            parsed_output["vrf"]
            .get(vrf, {})
            .get("interface", {})
            .get(interface, {})
            .get("sync", {})
            .get("status", {})
            .get("sync_achieved", False)
        )
    except KeyError:
        return False

    return igp_synchronization_enabled and sync_achieved


def verify_mpls_binding_label(device, ipv4, vrf=None):
    """ Verify local and remote binding labels for ipv4

        Args:
            device (`obj`): Device object
            vrf (`str`): Vrf name
            ipv4 (`str`): ipv4 with prefix
        Returns:
            verified result
        Raises:
            None
    """
    result = []
    try:
        out = device.parse("show mpls ldp bindings")
    except SchemaEmptyParserError:
        return result
    vrf = vrf if vrf else "default"
    lib_dict = None
    try:
        lib_dict = out["vrf"][vrf]["lib_entry"]
    except KeyError as ke:
        log.error("Could not find key, error: {}".format(str(ke)))
        return False

    if lib_dict and ipv4 in lib_dict:
        local = lib_dict[ipv4].get("label_binding").get("label")
        remote = lib_dict[ipv4].get("remote_binding").get("label")
        if local and remote:
            result.append(
                "Local label for {ipv4} is {local}".format(
                    ipv4=ipv4, local=list(local)
                )
            )
            result.append(
                "Remote label for {ipv4} is {remote}".format(
                    ipv4=ipv4, remote=list(remote)
                )
            )
    else:
        return result

    return "\n".join(result)


def is_mpls_ldp_neighbor_in_state(
    device, interface, state, max_time=60, check_interval=10
):
    """ Checks if ldp neighbor is in state

        Args:
            device ('obj'): device to use
            interface ('str'): interface to search under
            state ('str'): state

        return:
            True
            False
        Raises:
            None
    """
    log.info("Checking if ldp neighbor is in state: {}".format(state))
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        current_state = get_mpls_ldp_peer_state(device, interface)
        if current_state and state in current_state:
            return True

        timeout.sleep()

    return False
