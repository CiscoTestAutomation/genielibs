"""Common verify functions for MPLS"""

# Python
import logging

# pyats
from pyats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def verify_segment_routing_gb_range(
        device, expected_label_min, expected_label_max, max_time=30, check_interval=10):
    """ Verify segment routing global block range

        Args:
            device (`obj`): Device object
            expected_label_min (`int`): Segment routing global block start
            expected_label_max (`int`): Segment routing global block end
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
        Returns:
            result (`bool`): Verified result
    """

    try:
        out = device.parse('show mpls label table detail')
    except SchemaEmptyParserError:
        log.info("Device output is empty.")
        return False

    reqs = R(['table', '(.*)',
               'label', '(?P<label>.*)',
               'label_type', '(?P<label_type>[Lbl\-blk.*])',
               '(?P<start_label>.*)'])

    found = find([out], reqs, filter_=False, all_keys=True)

    if found:
        for item in found:
            if 'Lbl-blk SRGB' in item[1]:
                # Those are the reachability checks
                if expected_label_min == item[0]['start_label'] and \
                    item[0]['start_label'] + item[0]['size'] > expected_label_max:
                    return True
    return False


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


def verify_mpls_binding_label(device, prefix, vrf=None):
    """ Verify local and remote binding labels for prefix

        Args:
            device (`obj`): Device object
            vrf (`str`): Vrf name
            prefix (`str`): ipv4/ipv6
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

    if lib_dict and prefix in lib_dict:
        local = lib_dict[prefix].get("label_binding").get("label")
        remote = lib_dict[prefix].get("remote_binding").get("label")
        if local and remote:
            result.append(
                "Local label for {prefix} is {local}".format(
                    prefix=prefix, local=list(local)
                )
            )
            result.append(
                "Remote label for {prefix} is {remote}".format(
                    prefix=prefix, remote=list(remote)
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
        current_state = device.apis.get_mpls_ldp_peer_state(interface)
        if current_state and state in current_state:
            return True

        timeout.sleep()

    return False
