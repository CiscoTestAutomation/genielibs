"""Common verify functions for mpls"""

# Python
import logging
from netaddr import IPNetwork

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
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        result = True

        try:
            out = device.parse('show mpls forwarding-table {}'.format(ip))
        except SchemaEmptyParserError:
            log.info("Device output is empty.")
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



def verify_mpls_forwarding_table_has_prefix_in_subnet_range(device, subnet, max_time=120, check_interval=30):

    """ Verifies local label for entries with a prefix inside subnet

        Args:
            device ('obj'): Device to use
            subnet ('str'): Subnet to verify inside
            max_time ('int'): Max time to check
            check_interval ('int'): How often to check

        returns:
            True/False

        raises:
            N/A
    """
    log.info('Checking atleast one entry has a prefix in subnet {subnet} range'
             .format(subnet=subnet))

    try:
        subnet = IPNetwork(subnet)
    except Exception:
        log.info('Bad subnet provided')
        return False

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show mpls forwarding-table')
        except SchemaEmptyParserError:
            log.info('Parser output is empty')
            timeout.sleep()
            continue


        for vrf in out.get('vrf'):
            for local_label in out['vrf'][vrf].get('local_label'):
                for out_label in out['vrf'][vrf]['local_label'][local_label].get('outgoing_label_or_vc'):
                    for prefix in out['vrf'][vrf]['local_label'][local_label]['outgoing_label_or_vc'][out_label].get('prefix_or_tunnel_id'):
                        try:
                            pfx = IPNetwork(prefix)
                        except Exception:
                            continue

                        if pfx in subnet:
                            return True

        timeout.sleep()


    return False



def verify_mpls_forwarding_table_local_label_for_subnet(device, subnet, min_range, max_range, in_range=True, max_time=120, check_interval=30):

    """ Verifies local label for entries with a prefix inside subnet

        Args:
            device ('obj'): Device to use
            subnet ('str'): Subnet to verify inside
            min_range ('int'): Minimum label
            max_range ('int'): Maximum label
            in_range ('bool'): True to verify between min_range/max_range, False to verify outside
            max_time ('int'): Max time to check
            check_interval ('int'): How often to check

        returns:
            True/False

        raises:
            N/A
    """

    log.info('Checking all entries where the prefix falls inside subnet {subnet} range'
             .format(subnet=subnet))

    try:
        subnet = IPNetwork(subnet)
    except Exception:
        log.info('Bad subnet provided')
        return False

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        result = True

        try:
            out = device.parse('show mpls forwarding-table')
        except SchemaEmptyParserError:
            log.info('Parser output is empty')
            timeout.sleep()
            continue

        for vrf in out.get('vrf'):
            for local_label in out['vrf'][vrf].get('local_label'):
                for out_label in out['vrf'][vrf]['local_label'][local_label].get('outgoing_label_or_vc'):
                    for prefix in out['vrf'][vrf]['local_label'][local_label]['outgoing_label_or_vc'][out_label].get('prefix_or_tunnel_id'):
                        try:
                            pfx = IPNetwork(prefix)
                        except Exception:
                            continue

                        if pfx in subnet:
                            if in_range and min_range <= local_label <= max_range:
                                continue
                            elif in_range and not min_range <= local_label <= max_range:
                                log.info('Entry with prefix {prefix} has label {label} which is outside '
                                        'given range {range}. Expected to be inside.'
                                        .format(prefix=prefix,
                                                label=local_label,
                                                range='{}-{}'.format(min_range, max_range)))
                                result = False
                            elif not in_range and min_range <= local_label <= max_range:
                                log.info('Entry with prefix {prefix] has label {label} which is inside '
                                        'given range {range}. Expected to be outside.'
                                        .format(prefix=prefix,
                                                label=local_label,
                                                range='{}-{}'.format(min_range, max_range)))
                                result = False
                            elif not in_range and not min_range <= local_label <= max_range:
                                continue

        if result:
            return True

        timeout.sleep()

    return False

