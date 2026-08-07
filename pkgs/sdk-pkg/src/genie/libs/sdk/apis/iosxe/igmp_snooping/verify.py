"""Common verify functions for IGMP snooping"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.libs.parser.utils.common import Common

log = logging.getLogger(__name__)


def __gen_local_port_set(port_list):
    """Generate a set of canonical port names from the given list of ports.
        Args:
            port_list (list): List of ports
        Returns:
            set: Set of full interface names (order-independent)
    """
    ports = set()
    for port in port_list:
        if port:
            ports.add(Common.convert_intf_name(port.strip()))
    return ports


def verify_igmp_snooping_group(
        device, vlan, group, entry_type, version, port_list,
        max_time=4, check_interval=2):
    """Verify the ip igmp snooping group entry
        Args:
            device('obj'): device object
            vlan('str'): vlan id
            group ('str'): group ip address
            entry_type('str'): type of the group entry I/S/P/A
                                I: IGMP Snooping S: Static
                                P: PIM Snooping  A:ASM mode
            version('str'): igmp version
            port_list('list'): port list of the group entry
            max_time('int'): Maximum time to wait for the verification to pass
            check_interval('int'): Time interval between checks
        Returns:
            True/False
        Raises:
            None
    """
    exp_ports = __gen_local_port_set(port_list)
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        entry = device.api.get_igmp_snooping_group(vlan, group)
        if entry:
            act_port_list = entry['port_list'].split(" ")
            act_ports = __gen_local_port_set(act_port_list)
            if entry_type == entry['type'] and \
                    version == entry['version'] and \
                    exp_ports == act_ports:
                return True
        timeout.sleep()
    return False


def verify_igmp_snooping_group_notexist(
        device, vlan, group, max_time=4, check_interval=2):
    """Verify the ip igmp snooping group entry not exist
        Args:
            device('obj'): device object
            vlan('str'): vlan id
            group ('str'): group ip address
            max_time('int'): Maximum time to wait for the verification to pass
            check_interval('int'): Time interval between checks
        Returns:
            True/False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        entry = device.api.get_igmp_snooping_group(vlan, group)
        if not entry:
            log.debug(f'Entry not found: vlan {vlan}, group {group}')
            return True
        timeout.sleep()
    return False


def verify_igmp_snooping(
        device, vlan=None, igmp_snooping=None, igmpv3_snooping=None,
        igmp_snooping_admin_state=None, igmp_snooping_oper_state=None,
        check_ttl=None, check_router_alert_option=None,
        igmpv2_immediate_leave=None, report_supression=None,
        robustness_variable=None, last_member_query_count=None,
        last_member_query_interval=None, **kwargs):
    """
    Verifies if all the given parameters are correct for igmp snooping
    Args:
        device('obj'): Device object
        vlan('str'): vlan
        igmp_snooping('str'): IGMP snooping global status,
                              Enabled/Disabled
        igmpv3_snooping('str'): IGMPv3 snooping global status,
                                Enabled/Disabled
        igmp_snooping_admin_state('str'): IGMP snooping admin state,
                                          Disabled/Enabled
        igmp_snooping_oper_state('str'): IGMP snooping oper state,
                                         Disabled/Enabled
        check_ttl('str'): check ttl, Yes/No
        check_router_alert_option('str'): check router alert option,
                                          Yes/No
        igmpv2_immediate_leave('str'): igmpv2 immediate leave,
                                       Enabled/Disabled
        report_supression('str'): report supression, Enabled/Disabled
        robustness_variable('int'): robustness variable
        last_member_query_count('int'): last member query count
        last_member_query_interval('int'): last member query interval
        kwargs: Additional key-value pairs to verify
    Returns:
        True/False
    Raises:
        None
    """

    def __dict_compare(expect, actual):
        for k in expect:
            if k in actual:
                if isinstance(expect[k], dict) and isinstance(actual[k], dict):
                    if not __dict_compare(expect[k], actual[k]):
                        return False
                elif isinstance(expect[k], list) and \
                        isinstance(actual[k], list):
                    for element in expect[k]:
                        if element not in actual[k]:
                            return False
                elif expect[k] != actual[k]:
                    log.debug(f"{k} mismatch: expected {expect[k]}, "
                              f"actual {actual[k]}")
                    return False
            else:
                log.debug(
                    f"{k} does not exist, expect {expect[k]}")
                return False
        return True

    kwargs.update({
        k: v for k, v in {
            'igmp_snooping': igmp_snooping,
            'igmpv3_snooping': igmpv3_snooping,
            'igmp_snooping_admin_state': igmp_snooping_admin_state,
            'igmp_snooping_oper_state': igmp_snooping_oper_state,
            'check_ttl': check_ttl,
            'check_router_alert_option': check_router_alert_option,
            'igmpv2_immediate_leave': igmpv2_immediate_leave,
            'report_supression': report_supression,
            'robustness_variable': robustness_variable,
            'last_member_query_count': last_member_query_count,
            'last_member_query_interval': last_member_query_interval,
        }.items()
        if v is not None
    })
    entry = device.api.get_igmp_snooping()
    if vlan:
        entry = entry.get('vlan', {}).get(str(vlan), {})
    log.debug('Verify the igmp snooping configuration.\n'
              f'Expected values: {kwargs}\n'
              f'Actual values: {entry}')
    if entry:
        return __dict_compare(kwargs, entry)
    return False


def verify_igmp_vrf_snooping_group(
        device, vrf, vlan, group, entry_type, version, port_list,
        max_time=4, check_interval=2):
    """
    Verify the ip igmp vrf snooping group entry
    Args:
        device('obj'): device object
        vrf('str'): vrf name
        vlan('str'): vlan id
        group ('str'): group ip address
        entry_type('str'): type of the group entry I/S/P/A
                            I: IGMP Snooping S: Static
                            P: PIM Snooping  A:ASM mode
        version('str'): igmp version
        port_list('list'): port list of the group entry
        max_time('int'): Maximum time to wait for the verification to pass
        check_interval('int'): Time interval between checks
    Returns:
        True/False
    Raises:
        None
    """
    exp_ports = __gen_local_port_set(port_list)

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = device.api.get_igmp_vrf_snooping_groups(vrf)
        for entry in out.values():
            if str(vlan) == str(entry.get('vlan')) and \
                    group == entry.get('group'):
                act_port_list = entry['port_list']
                act_ports = __gen_local_port_set(act_port_list)
                if entry_type == entry['type'] and \
                        version == entry['version'] and \
                        exp_ports == act_ports:
                    return True
        timeout.sleep()
    return False


def verify_igmp_vrf_snooping_group_notexist(
        device, vrf, vlan, group, max_time=4, check_interval=2):
    """
    Verify the ip igmp vrf snooping group entry not exist
    Args:
        device('obj'): device object
        vrf('str'): vrf name
        vlan('str'): vlan id
        group ('str'): group ip address
        max_time('int'): Maximum time to wait for the verification to pass
        check_interval('int'): Time interval between checks
    Returns:
        True/False
    Raises:
        None
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = device.api.get_igmp_vrf_snooping_groups(vrf)
        entry_found = False
        for entry in out.values():
            if str(vlan) == str(entry.get('vlan')) and \
                    group == entry.get('group'):
                entry_found = True
                break
        if not entry_found:
            log.debug(f'Entry not found: vrf {vrf}, vlan {vlan}, '
                      f'group {group}')
            return True
        timeout.sleep()
    return False


def verify_igmp_group(
        device, group, interface, last_reporter=None,
        max_time=4, check_interval=2):
    """
    Verify the ip igmp group entry
    Args:
        device('obj'): device object
        interface('str'): interface name
        group ('str'): group ip address
        last_reporter ('str'): last reporter ip address
        max_time('int'): Maximum time to wait for the verification to pass
        check_interval('int'): Time interval between checks
    Returns:
        True/False
    Raises:
        None
    """

    exp_intf = Common.convert_intf_name(interface) if interface else None
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = device.api.get_igmp_groups(interface)
        for grp, entry in out.get('igmp_groups', {}).items():
            if grp == group:
                act_intf = Common.convert_intf_name(entry.get('intf')) \
                    if entry.get('intf') else None
                act_reporter = entry.get('last_reporter')
                if (exp_intf is None or act_intf == exp_intf) and \
                        (last_reporter is None or
                         act_reporter == last_reporter):
                    return True
        timeout.sleep()
    return False


def verify_igmp_group_notexist(
        device, group, interface, max_time=4, check_interval=2):
    """
    Verify the ip igmp group entry not exist
    Args:
        device('obj'): device object
        interface('str'): interface name
        group ('str'): group ip address
        max_time('int'): Maximum time to wait for the verification to pass
        check_interval('int'): Time interval between checks
    Returns:
        True/False
    Raises:
        None
    """

    exp_intf = Common.convert_intf_name(interface) if interface else None
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = device.api.get_igmp_groups(interface)
        entry_found = False
        for grp, entry in out.get('igmp_groups', {}).items():
            act_intf = Common.convert_intf_name(entry.get('intf')) \
                if entry.get('intf') else None
            if grp == group and \
                    (exp_intf is None or act_intf == exp_intf):
                entry_found = True
                break
        if not entry_found:
            log.debug(
                f'Entry not found: group {group}, interface {interface}')
            return True
        timeout.sleep()
    return False


def verify_igmp_vrf_group(
        device, vrf, group, interface, last_reporter=None,
        max_time=4, check_interval=2):
    """
    Verify the ip igmp vrf group entry
    Args:
        device('obj'): device object
        vrf('str'): vrf name
        interface('str'): interface name
        group ('str'): group ip address
        last_reporter ('str'): last reporter ip address
        max_time('int'): Maximum time to wait for the verification to pass
        check_interval('int'): Time interval between checks
    Returns:
        True/False
    Raises:
        None
    """

    exp_intf = Common.convert_intf_name(interface) if interface else None
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = device.api.get_igmp_vrf_groups(vrf)
        for grp, entry in out.get('igmp_group_address', {}).items():
            if grp == group:
                act_intf = Common.convert_intf_name(entry.get('interface')) \
                    if entry.get('interface') else None
                act_reporter = entry.get('last_reporter')
                if (exp_intf is None or act_intf == exp_intf) and \
                        (last_reporter is None or
                         act_reporter == last_reporter):
                    return True
        timeout.sleep()
    return False


def verify_igmp_vrf_group_notexist(
        device, vrf, group, interface, max_time=4, check_interval=2):
    """
    Verify the ip igmp vrf group entry not exist
    Args:
        device('obj'): device object
        vrf('str'): vrf name
        interface('str'): interface name
        group ('str'): group ip address
        max_time('int'): Maximum time to wait for the verification to pass
        check_interval('int'): Time interval between checks
    Returns:
        True/False
    Raises:
        None
    """

    exp_intf = Common.convert_intf_name(interface) if interface else None
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = device.api.get_igmp_vrf_groups(vrf)
        entry_found = False
        for grp, entry in out.get('igmp_group_address', {}).items():
            act_intf = Common.convert_intf_name(entry.get('interface')) \
                if entry.get('interface') else None
            if (grp == group) and \
                    (exp_intf is None or act_intf == exp_intf):
                entry_found = True
                break
        if not entry_found:
            log.debug(
                f'Entry not found: group {group}, interface {interface}')
            return True
        timeout.sleep()
    return False


def verify_igmp_snooping_group_count(
        device, vlan, min_count, max_count=None, max_time=4, check_interval=2):
    """
    Verify the ip igmp snooping group count
    Args:
        device('obj'): device objecte
        vlan('str'): vlan id
        max_count('int'): expected maximum group count
        min_count('int'): expected minimum group count
        max_time('int'): Maximum time to wait for the verification to pass
        check_interval('int'): Time interval between checks
    Returns:
        True/False
    Raises:
        None
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = device.api.get_igmp_snooping_groups_count(vlan=vlan)
        if vlan:
            act_group_count = out.get('vlan', {}).get(
                str(vlan), {}).get('count', 0)
        else:
            act_group_count = out.get(
                'total_number_of_groups', {}).get('igmp_groups_count', 0)
        check_result = True
        if min_count is not None and act_group_count < min_count:
            check_result = False
        elif max_count is not None and act_group_count > max_count:
            check_result = False
        if check_result:
            log.debug(
                f'Group count {act_group_count} is within the '
                f'expected range [{min_count}, {max_count}]')
            return True
        timeout.sleep()
    return False
