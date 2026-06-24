"""Common verify functions for lldp"""

# Python
import logging
import re
from genie.utils import Dq
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


def verify_lldp_in_state(device, max_time=60, check_interval=10):
    """ Verify that lldp is enabled on the device
        Args:
            device = device to check status on
        returns:
            True if lldp is enabled, false in all other cases
    """
    timeout = Timeout(max_time, check_interval, True)
    while timeout.iterate():
        try:
            device.parse('show lldp neighbors')
            return True
        except Exception:
            timeout.sleep()
    return False


def verify_show_lldp(device, hello_timer=None, hold_timer=None,
                     reinit_timer=None, status=None):
    """
    Verify hello_timer, hold_timer, reinit_timer, enabled in "show lldp"
    Args:
        device ('obj'): Device object
        hello_timer ('int' or None): Expect seconds of sending LLDP packets
                                     interval
        hold_timer ('int' or None): Expect seconds of LLDP hold time
        reinit_timer ('int' or None): Expect seconds of LLDP interface init
                                      delay
        status ('str' or None): Expect config status of LLDP
                                ['active', 'inactive']
    Returns:
        True/False
    """

    res = device.api.get_lldp_info()
    if (hello_timer is not None or hold_timer is not None or reinit_timer is
            not None or status == 'active') and res is None:
        log.debug('got "show lldp" result is None')
        return False
    if status == 'inactive' and res is not None:
        log.debug(f'"show lldp" result expected None, got {res}')
        return False
    expectations = {
        'hello_timer': hello_timer,
        'hold_timer': hold_timer,
        'reinit_timer': reinit_timer,
        'status': status
    }
    for key, expected_val in expectations.items():
        if expected_val is None or \
                (key == 'status' and expected_val != 'active'):
            continue
        actual_val = res.get(key)
        if actual_val != expected_val:
            log.debug(f'lldp {key} expected {expected_val}, got {actual_val}')
            return False
    return True


def verify_show_lldp_interface(device, intf, tx=None, rx=None,
                               tx_state=None, rx_state=None):
    """
    Verify tx, rx, tx_state, rx_state in "show lldp interface"
    Args:
        device ('obj'): Device object
        intf (str): Interface name
        tx ('str' or None): Expect tx config of interface
                            ['enabled', 'disabled']
        rx ('str' or None): Expect rx config of interface
                            ['enabled', 'disabled']
        tx_state ('str' or None): Expect tx state of interface
                                  ['init', 'idle', ...]
        rx_state ('str' or None): Expect rx state of interface
                                  ['wait_port_oper',
                                   'wait_for_frame', ...]
    Returns:
        True/False
    """
    res = device.api.get_lldp_interface_info(intf)
    if tx is not None or rx is not None or tx_state is not None or \
            rx_state is not None:
        if res is None:
            log.debug(f'got "show lldp interface {intf}" result is None')
            return False
    expectations = {
        'tx': tx,
        'rx': rx,
        'tx_state': tx_state,
        'rx_state': rx_state
    }
    for key, expected_val in expectations.items():
        if expected_val is None:
            continue
        actual_val = res.get('interfaces').get(intf).get(key)
        if actual_val != expected_val:
            log.debug(f'lldp interface {intf} {key} expected {expected_val}, '
                      f'got {actual_val}')
            return False
    return True


def verify_show_lldp_traffic(device, max_frame_out=None, min_frame_out=None,
                             max_entries_aged_out=None,
                             min_entries_aged_out=None,
                             max_frame_in=None, min_frame_in=None,
                             max_frame_error_in=None, min_frame_error_in=None,
                             max_frame_discard=None, min_frame_discard=None,
                             max_tlv_discard=None, min_tlv_discard=None,
                             max_tlv_unknown=None, min_tlv_unknown=None):
    """
    Verify lldp traffic statistics in "show lldp traffic"
    Args:
        device ('obj'): Device object
        max_frame_out ('int' or None): Expect max frame_out count of lldp
                                       traffic
        min_frame_out ('int' or None): Expect min frame_out count of lldp
                                       traffic
        max_entries_aged_out ('int' or None): Expect max entries_aged_out
                                              count of lldp traffic
        min_entries_aged_out ('int' or None): Expect min entries_aged_out
                                              count of lldp traffic
        max_frame_in ('int' or None): Expect max frame_in count of lldp traffic
        min_frame_in ('int' or None): Expect min frame_in count of lldp traffic
        max_frame_error_in ('int' or None): Expect max frame_error_in count of
                                            lldp traffic
        min_frame_error_in ('int' or None): Expect min frame_error_in count of
                                            lldp traffic
        max_frame_discard ('int' or None): Expect max frame_discard count of
                                           lldp traffic
        min_frame_discard ('int' or None): Expect min frame_discard count of
                                           lldp traffic
        max_tlv_discard ('int' or None): Expect max tlv_discard count of lldp
                                         traffic
        min_tlv_discard ('int' or None): Expect min tlv_discard count of lldp
                                         traffic
        max_tlv_unknown ('int' or None): Expect max tlv_unknown count of lldp
                                          traffic
        min_tlv_unknown ('int' or None): Expect min tlv_unknown count of lldp
                                          traffic
    Returns:
        True/False
    """
    res = device.api.get_lldp_traffic_info()
    if res is None:
        log.debug('got "show lldp traffic" result is None')
        return False
    expectations = {
        'max_frame_out': max_frame_out,
        'min_frame_out': min_frame_out,
        'max_entries_aged_out': max_entries_aged_out,
        'min_entries_aged_out': min_entries_aged_out,
        'max_frame_in': max_frame_in,
        'min_frame_in': min_frame_in,
        'max_frame_error_in': max_frame_error_in,
        'min_frame_error_in': min_frame_error_in,
        'max_frame_discard': max_frame_discard,
        'min_frame_discard': min_frame_discard,
        'max_tlv_discard': max_tlv_discard,
        'min_tlv_discard': min_tlv_discard,
        'max_tlv_unknown': max_tlv_unknown,
        'min_tlv_unknown': min_tlv_unknown
    }
    for key, expected_val in expectations.items():
        if expected_val is None:
            continue
        actual_key = key.removeprefix('max_').removeprefix('min_')
        actual_val = res.get(actual_key)
        if 'min' in key and actual_val < expected_val:
            log.debug(f'got lldp traffic count {actual_key} {actual_val}, '
                      f'less than min expected {expected_val}')
            return False
        if 'max' in key and actual_val > expected_val:
            log.debug(f'got lldp traffic count {actual_key} {actual_val}, '
                      f'great than max expected {expected_val}')
            return False
    return True


def verify_show_lldp_error(device, max_memory=None, min_memory=None,
                           max_encapsulation=None, min_encapsulation=None,
                           max_input_queue=None, min_input_queue=None,
                           max_table=None, min_table=None):
    """
    Verify lldp error statistics in "show lldp error"
    Args:
        device ('obj'): Device object
        max_memory ('int' or None): Expect max memory allocation failures count
                                    of lldp error
        min_memory ('int' or None): Expect min memory allocation failures count
                                    of lldp error
        max_encapsulation ('int' or None): Expect max encapsulation failures
                                           count of lldp error
        min_encapsulation ('int' or None): Expect min encapsulation failures
                                           count of lldp error
        max_input_queue ('int' or None): Expect max input queue overflows count
                                         of lldp error
        min_input_queue ('int' or None): Expect min input queue overflows count
                                         of lldp error
        max_table ('int' or None): Expect max table overflows count of lldp
                                   error
        min_table ('int' or None): Expect min table overflows count of lldp
                                   error
    Returns:
        True/False
    """
    res = device.api.get_lldp_error_info()
    if res is None:
        log.debug('got "show lldp error" result is None')
        return False
    expectations = {
        'max_memory': max_memory,
        'min_memory': min_memory,
        'max_encapsulation': max_encapsulation,
        'min_encapsulation': min_encapsulation,
        'max_input_queue': max_input_queue,
        'min_input_queue': min_input_queue,
        'max_table': max_table,
        'min_table': min_table
    }
    for key, expected_val in expectations.items():
        if expected_val is None:
            continue
        actual_key = key.removeprefix('max_').removeprefix('min_')
        actual_val = res.get(actual_key)
        if 'min' in key and actual_val < expected_val:
            log.debug(f'got lldp error count {actual_key} {actual_val}, '
                      f'less than min expected {expected_val}')
            return False
        if 'max' in key and actual_val > expected_val:
            log.debug(f'got lldp error count {actual_key} {actual_val}, '
                      f'great than max expected {expected_val}')
            return False
    return True


def verify_lldp_entry(output, interface, **kwargs):
    """
    Verify lldp entry.
    Args:
        output ('dict'): Parse output of 'show lldp entry' or 'show lldp
                         neighbors detail'
        interface ('str'): Interface name of device
        supported kwargs:
            port_id, sys_name, neigh_id, chassis_id, port_desc,
            sys_desc, max_ttl, min_ttl, cap_system, cap_enabled,
            mgmt_addr, vlan_id
    Returns:
        True/False
    """

    if output is None:
        log.debug('got "show lldp entry" or "show lldp neighbors detail" '
                  'result is None')
        return False

    exp = {
        'port_id': kwargs.get('port_id'),
        'system_name': kwargs.get('sys_name'),
        'neighbor_id': kwargs.get('neigh_id'),
        'management_address': kwargs.get('mgmt_addr'),
        'vlan_id': kwargs.get('vlan_id'),
        'system_description': kwargs.get('sys_desc'),
        'port_description': kwargs.get('port_desc'),
        'chassis_id': kwargs.get('chassis_id')
    }
    normal_expect = {k: v for k, v in exp.items() if v is not None}

    exp = {
        'max_time_remaining': kwargs.get('max_ttl'),
        'min_time_remaining': kwargs.get('min_ttl')
    }
    threshold_expect = {k: v for k, v in exp.items() if v is not None}

    exp = {
        'system': kwargs.get('cap_system'),
        'enabled': kwargs.get('cap_enabled')
    }
    capabilities_expect = {k: v for k, v in exp.items() if v is not None}

    output = output.get('interfaces', {})
    if Dq(output).contains(interface).reconstruct():
        lldp_entries = output.get(interface)
    else:
        interface = interface.replace(
            'TwentyFiveGigE', 'TwoGigabitEthernet')
        if Dq(output).contains(interface).reconstruct():
            lldp_entries = output.get(interface)
        else:
            log.debug(f'got lldp entry of interface {interface} is None')
            return False

    for key, val in normal_expect.items():
        actual_vals = Dq(lldp_entries).get_values(key)
        if val == '*':
            hit = any(actual_val is not None for actual_val in actual_vals)
        else:
            hit = any(re.search(re.escape(str(val)), str(actual_val))
                      for actual_val in actual_vals
                      if actual_val is not None)
        if not hit:
            log.debug(f'lldp entry of interface {interface} {key} expected '
                      f'{val}, got {actual_vals}')
            return False

    for key, val in threshold_expect.items():
        actual_key = key.removeprefix('max_').removeprefix('min_')
        actual_vals = Dq(lldp_entries).get_values(actual_key)
        if 'max' in key:
            intf_datas_filter = Dq(lldp_entries).value_operator(
                actual_key, '<=', val).reconstruct()
        elif 'min' in key:
            intf_datas_filter = Dq(lldp_entries).value_operator(
                actual_key, '>=', val).reconstruct()
        if not intf_datas_filter:
            log.debug(f'lldp entry of interface {interface} {key} expected '
                      f'{val}, got {actual_vals}')
            return False

    for key, vals in capabilities_expect.items():
        # capability names: ['router', 'mac_bridge', 'telephone',
        # 'docsis_cable_device', 'wlan_access_point', 'repeater',
        # 'station_only', 'other']
        actual_key = 'capabilities'
        for val in vals:
            if val == '*':
                cap_filter = Dq(lldp_entries).contains(
                    actual_key).reconstruct()
                if not cap_filter:
                    log.debug(f'lldp entry interface {interface} capabilities '
                              f'{key} expected any value, got None')
                    return False
                continue
            cap_filter = Dq(lldp_entries).contains_key_value(
                actual_key, val).reconstruct()
            actual_vals = Dq(cap_filter).get_values(key)
            if True not in actual_vals:
                log.debug(f'lldp entry interface {interface} capabilities '
                          f'{key} expected {val}, got {actual_vals}')
                return False
    return True


def verify_show_lldp_neighbors_detail(
        device, intf, max_time=40, check_interval=5, **kwargs):
    """
    Verify show lldp neighbors detail
    Args:
        device ('obj'): Device object
        intf ('str'): Interface name of device
        max_time ('int'): Max time of neighbor check
        check_interval ('int'): The interval of neighbor check
        supported kwargs:
            port_id, sys_name, neigh_id, chassis_id, port_desc,
            sys_desc, max_ttl, min_ttl, cap_system, cap_enabled,
            mgmt_addr, vlan_id
    Returns:
        True/False
    """

    timeout = Timeout(max_time=max_time, interval=check_interval)
    while timeout.iterate():
        output = device.api.get_lldp_neighbors_info()
        res = verify_lldp_entry(output, interface=intf, **kwargs)
        if res is True:
            return True
        else:
            timeout.sleep()
    else:
        return False


def verify_show_lldp_entry(
        device, intf, max_time=40, check_interval=5, **kwargs):
    """
    Verify show lldp entry
    Args:
        device ('obj'): Device object
        intf ('str'): Interface name of device
        max_time ('int'): Max time of neighbor check
        check_interval ('int'): The interval of neighbor check
        supported kwargs:
            port_id, sys_name, neigh_id, chassis_id, port_desc,
            sys_desc, max_ttl, min_ttl, cap_system, cap_enabled,
            mgmt_addr, vlan_id
    Returns:
        True/False
    """

    neighbor_id = kwargs.get('neigh_id') if kwargs.get('neigh_id') else '*'
    timeout = Timeout(max_time=max_time, interval=check_interval)
    while timeout.iterate():
        output = device.api.get_lldp_entry_info(neighbor_id=neighbor_id)
        res = verify_lldp_entry(output, interface=intf, **kwargs)
        if res is True:
            return True
        else:
            timeout.sleep()
    else:
        return False
