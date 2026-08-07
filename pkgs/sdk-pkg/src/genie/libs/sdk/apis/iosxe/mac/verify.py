"""Common verification functions for mac"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# utils
from genie.libs.sdk.apis.utils import time_to_int, has_configuration

log = logging.getLogger(__name__)


def verify_mac_from_address_family(device, address_family, expected_mac,
    evi=None, max_time=30, check_interval=10
):
    """ Verify mac from particular address family in "show l2vpn evpn mac"
        also for the particular evi (if given)

        Args:
            device ('obj'): device to use
            address_family ('str'): address family
            expected_mac ('str'): Expected mac
            evi ('str'):evi instance
            max_time ('int', optional): maximum time to wait in seconds,
                default is 30
            check_interval ('int', optional): how often to check in seconds,
                default is 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        mac_table = device.api.get_mac_table_from_address_family(address_family)

        if mac_table and evi:
            if (evi in mac_table.keys()) and (expected_mac in mac_table[evi]):
                return True

        elif mac_table:
            # Getting mac addr from dictionary to list for better verification
            mac_list = []
            for mac in mac_table.values():
                mac_list.extend(mac)
            # Checking whether the expected mac address is present in mactable
            if expected_mac in mac_list:
                return True
        else:
            timeout.sleep()

    if not mac_table:
        log.error("Could not get mac details along with evi, output is empty")
    else:
        log.error('Expected mac address is "{expected_mac}" '
            'actual mac address is "{mac_table}"'.format(expected_mac=
                expected_mac, mac_table=mac_table)
        )

    return False


def verify_mac_address_table_aging_time(device, aging_time):
    '''
    Verify mac address table aging time
    Args:
        device ('obj'): Device object
        aging_time('int'): Expect mac address table aging time
    Returns:
        True/False
    '''

    res = device.api.get_mac_address_table_aging_time()
    if res is None:
        return False
    actual_aging_time = res.get('mac_aging_time')
    if actual_aging_time != aging_time:
        log.debug(f'Expect mac address table aging time {aging_time}, '
                  f'got {actual_aging_time}')
        return False
    return True


def verify_mac_address_table_entry(
        device, mac_address, vlan, interface=None, drop=None,
        entry_type=None):
    '''
    Verify mac address table entry
    Args:
        device ('obj'): Device object
        mac_address('str'): Expect mac address, format is HHHH.HHHH.HHHH
        vlan ('int'): Vlan id
        interface ('str'): Interface name
        drop ('bool'): Drop flag, True or False
        entry_type ('str') : Mac address entry type, 'static' or 'dynamic'
    Returns:
        True/False
    '''

    res = device.api.get_mac_address_table(interface=interface, vlan=vlan)
    if res is None:
        return False
    mac_entry = res.get('mac_table', {}).get('vlans', {}).\
        get(str(vlan), {}).get('mac_addresses', {}).\
        get(mac_address.lower(), {})
    if not mac_entry:
        log.debug(f'Mac address {mac_address} entry is not found in vlan '
                  f'{vlan}')
        return False
    if interface is not None:
        # TwoGigabitEthernet and TwentyFiveGigE short name share
        # the same prefix(Twx/x/x).
        interfaces = mac_entry.get('interfaces', {})
        candidates = [interface]
        if interface.startswith('TwentyFiveGigE'):
            candidates.append(interface.replace(
                'TwentyFiveGigE', 'TwoGigabitEthernet'))
        mac_entry_intf = next(
            (interfaces[name] for name in candidates
             if name in interfaces), {})
        if not mac_entry_intf:
            log.debug(f'Mac address {mac_address} entry associate to '
                      f'{interface} not exist.')
            return False
        if entry_type is not None:
            actual_entry_type = mac_entry_intf.get('entry_type')
            if actual_entry_type != entry_type.lower():
                log.debug(f'Mac address {mac_address} entry type expected '
                          f'{entry_type}, got {actual_entry_type}')
                return False
    if drop is not None:
        mac_entry_drop = mac_entry.get('drop', {})
        actual_drop = mac_entry_drop.get('drop')
        if actual_drop != drop:
            log.debug(f'Mac address {mac_address} entry drop flag '
                      f'expected {drop}, got {actual_drop}')
            return False
        if entry_type is not None:
            actual_entry_type = mac_entry_drop.get('entry_type')
            if actual_entry_type != entry_type.lower():
                log.debug(f'Mac address {mac_address} entry type expected '
                          f'{entry_type}, got {actual_entry_type}')
                return False
    return True


def verify_mac_address_table_entry_flush(
        device, mac_address, vlan, interface=None,
        max_time=300, check_interval=5):
    '''
    Verify mac address table entry flush
    Args:
        device ('obj'): Device object
        mac_address('str'): Expect mac address, format is HHHH.HHHH.HHHH
        vlan ('int'): Vlan id
        interface ('str'): Interface name
        max_time ('int'): Max time of mac address entry check
        check_interval ('int'): The interval of mac address entry check
    Returns:
        True/False
    '''

    timeout = Timeout(max_time=max_time, interval=check_interval)
    while timeout.iterate():
        res = device.api.verify_mac_address_table_entry(
                mac_address=mac_address, vlan=vlan, interface=interface)
        if res:
            timeout.sleep()
        else:
            return True
    log.debug(f'Mac address entry mac={mac_address}, vlan={vlan}, '
              f'interface={interface} still exist after '
              f'{max_time} seconds wait')
    return False


def verify_mac_address_table_entry_learned(
        device, mac_address, vlan, interface=None, drop=None,
        entry_type=None, max_time=30, check_interval=5):
    '''
    Verify mac address table entry is learned by checking entry type is
    dynamic and entry exist in mac address table
    Args:
        device ('obj'): Device object
        mac_address('str'): Expect mac address, format is HHHH.HHHH.HHHH
        vlan ('int'): Vlan id
        interface ('str'): Interface name
        drop ('bool'): Drop flag, True or False
        entry_type ('str') : Mac address entry type, 'static' or 'dynamic'
        max_time ('int'): Max time of mac address entry check
        check_interval ('int'): The interval of mac address entry check
    Returns:
        True/False
    '''

    timeout = Timeout(max_time=max_time, interval=check_interval)
    while timeout.iterate():
        res = device.api.verify_mac_address_table_entry(
            mac_address=mac_address, vlan=vlan, interface=interface,
            drop=drop, entry_type=entry_type)
        if res:
            return True
        timeout.sleep()
    log.debug(f'Mac address entry mac={mac_address}, vlan={vlan}, '
              f'interface={interface} drop={drop} '
              f'entry_type={entry_type} does not exist after '
              f'{max_time} seconds.')
    return False


def verify_mac_address_table_count(
        device, vlan=None,
        max_dynamic_address_count=None, min_dynamic_address_count=None,
        max_static_address_count=None, min_static_address_count=None,
        max_total_mac_address_count=None, min_total_mac_address_count=None,
        max_time=30, check_interval=5):
    '''
    Verify mac address table count
    Args:
        device ('obj'): Device object
        vlan ('int'): Vlan id
        max_dynamic_address_count ('int'): Max dynamic mac address count
        min_dynamic_address_count ('int'): Min dynamic mac address count
        max_static_address_count ('int'): Max static mac address count
        min_static_address_count ('int'): Min static mac address count
        max_total_mac_address_count ('int'): Max total mac address count
        min_total_mac_address_count ('int'): Min total mac address count
        max_time ('int'): Max time of mac address count check
        check_interval ('int'): The interval of mac address count check
    Returns:
        True/False
    '''

    expectations = {
        'max_Total_dynamic_address_count': max_dynamic_address_count,
        'min_Total_dynamic_address_count': min_dynamic_address_count,
        'max_Total_static_address_count': max_static_address_count,
        'min_Total_static_address_count': min_static_address_count,
        'max_Total_mac_address_in_use': max_total_mac_address_count,
        'min_Total_mac_address_in_use': min_total_mac_address_count
    }
    timeout = Timeout(max_time=max_time, interval=check_interval)
    while timeout.iterate():
        res = device.api.get_mac_address_table_count(vlan=vlan)
        if res is None:
            timeout.sleep()
            continue
        verified = True
        for key, exp_val in expectations.items():
            if exp_val is None:
                continue
            actual_key = key.removeprefix('max_').removeprefix('min_')
            if vlan is None:
                actual_key = actual_key.lower()
            actual_val = res.get(actual_key)
            if actual_val is None:
                verified = False
                break
            if 'min' in key and actual_val < exp_val:
                log.debug(f'got mac address count {actual_key} '
                          f'{actual_val}, less than min expected '
                          f'{exp_val}')
                verified = False
                break
            if 'max' in key and actual_val > exp_val:
                log.debug(f'got mac address count {actual_key} '
                          f'{actual_val}, greater than max expected '
                          f'{exp_val}')
                verified = False
                break
        if verified:
            return True
        timeout.sleep()
    return False
