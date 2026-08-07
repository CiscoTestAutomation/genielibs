"""Common verify functions for span"""

import logging

from genie.utils.timeout import Timeout
from genie.libs.parser.utils.common import Common

log = logging.getLogger(__name__)


def verify_span_session(device, session_id, session_type=None, src_direct=None,
                        src_port=None, dst_port=None, expect_exist=True):
    """ Verify span session in 'show monitor session <session_id>'

        Args:
            device ('obj'): Device object
            session_id ('str'): ID of the span session
            session_type ('str' or None): Expect type of span session
            src_direct ('str' or None): Expect source direction of span session
            src_port ('str' or None): Expect source port of span session
            dst_port ('str' or None): Expect destination port of span session
            expect_exist ('bool'): If True, expect the session to exist,
                                   else expect it to not exist
        Returns:
            True/False
    """

    def _check_span_session(device, session_id, session_type=None,
                            src_direct=None, src_port=None, dst_port=None):

        res = device.api.get_span_session_info(session_id)
        if res is None:
            log.debug(
                f'got "show monitor session {session_id}" result is None')
            return False
        expect = {
            'type': session_type,
            'destination_ports': dst_port,
        }
        sess_info = res.get('session', {}).get(session_id, {})
        for key, exp_val in expect.items():
            if exp_val is None:
                continue
            actual_val = sess_info.get(key)
            if actual_val != exp_val:
                log.debug(
                    f'span session {key} expected {exp_val}, '
                    f'got {actual_val}')
                return False

        source_ports = sess_info.get('source_ports') or {}
        # Verify source direction/port by exact key lookup.
        if src_direct is not None:
            if src_direct not in source_ports:
                log.debug(
                    f'span session source direction {src_direct} '
                    f'not found in {source_ports}')
                return False
            if src_port is not None and source_ports[src_direct] != src_port:
                log.debug(
                    f'span session source port for {src_direct} '
                    f'expected {src_port}, got {source_ports[src_direct]}')
                return False
        elif src_port is not None:
            if src_port not in source_ports.values():
                log.debug(
                    f'span session source port expected {src_port}, '
                    f'got {list(source_ports.values())}')
                return False
        return True

    res = _check_span_session(
        device=device,
        session_id=session_id,
        session_type=session_type,
        src_direct=src_direct,
        src_port=src_port,
        dst_port=dst_port)
    if (expect_exist is True and res is False) or \
            (expect_exist is False and res is True):
        return False
    return True


def verify_span_session_running_config(
        device, session_id, role, interface, direction=None,
        expect_exist=True):
    """ Verify span session running config

        Args:
            device ('obj'): Device object
            session_id ('str'): ID of the span session
            role ('str'): Role of the span session,
                          'source' or 'destination'
            interface ('str'): Interface of the span session
            direction ('str' or None): Direction of the span session,
                                       None, 'rx', 'tx' or 'both'
            expect_exist ('bool'): If True, expect the cfg to exist,
                                   else expect it to not exist
        Returns:
            True/False
    """

    def _check_span_session_running_config(
            device, session_id, role, interface, direction=None):

        res = device.api.get_span_session_running_config()
        if not res:
            log.debug('No span session running config found')
            return False
        intf_full_name = Common.convert_intf_name(interface)
        expect = {
            'id': session_id,
            'role': role,
            'direction': direction,
        }
        for cfg in res:
            this_match = True
            for key, exp_val in expect.items():
                if cfg.get(key) != exp_val:
                    this_match = False
                    break
            if (this_match
                    and Common.convert_intf_name(
                        cfg.get('intf', '')) == intf_full_name):
                return True
        log.debug('Span session running config not found')
        return False

    res = _check_span_session_running_config(
        device=device,
        session_id=session_id,
        role=role,
        interface=interface,
        direction=direction)
    if (expect_exist is True and res is False) or \
            (expect_exist is False and res is True):
        return False
    return True


def verify_span_port_counters(
        device, src_port, dst_port, direction,
        src_out_pkts_before=0, src_in_pkts_before=0,
        dst_out_pkts_before=0,
        counter_tolerance=0.1, max_time=30, check_interval=5):
    """ Verify span interface counters via 'show interface' output

        Args:
            device ('obj'): Device object
            src_port ('str'): Span source interface name
            dst_port ('str'): Span destination interface name
            direction ('str'): Direction of the span session,
                               'rx', 'tx' or 'both'
            src_out_pkts_before ('int'): Span source interface out_pkts
                                         counter before test traffic
            src_in_pkts_before ('int'): Span source interface in_pkts
                                        counter before test traffic
            dst_out_pkts_before ('int'): Span destination interface
                                         out_pkts counter before test
                                         traffic
            counter_tolerance ('float'): Tolerance for counter
                                         verification, default 0.1 (10%)
            max_time ('int'): Maximum wait time, default 30 seconds
            check_interval ('int'): Interval between checks,
                                    default 5 seconds
        Returns:
            True/False
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        timeout.sleep()
        src_intf_output = device.api.get_show_interface_output(
            interface=src_port)
        dst_intf_output = device.api.get_show_interface_output(
            interface=dst_port)
        if not (src_intf_output and dst_intf_output):
            log.debug(
                'Failed to get interface output for counter '
                'verification, retrying...')
            continue

        src_intf_out_pkts = device.api.get_interface_packet_counter(
            interface=src_port, counter_field='out_pkts',
            output=src_intf_output)
        src_intf_in_pkts = device.api.get_interface_packet_counter(
            interface=src_port, counter_field='in_pkts',
            output=src_intf_output)
        dst_intf_out_pkts = device.api.get_interface_packet_counter(
            interface=dst_port, counter_field='out_pkts',
            output=dst_intf_output)
        log.debug(
            f'Get interface {src_port} counters after test traffic: '
            f'in_pkts={src_intf_in_pkts}, '
            f'out_pkts={src_intf_out_pkts}, '
            f'in_pkts_increment='
            f'{src_intf_in_pkts - src_in_pkts_before}, '
            f'out_pkts_increment='
            f'{src_intf_out_pkts - src_out_pkts_before}')
        log.debug(
            f'Get interface {dst_port} counters after test traffic: '
            f'out_pkts={dst_intf_out_pkts}, '
            f'out_pkts_increment='
            f'{dst_intf_out_pkts - dst_out_pkts_before}')

        if direction == 'tx' and src_intf_out_pkts is not None:
            exp_tx_packets = src_intf_out_pkts - src_out_pkts_before
        elif direction == 'rx' and src_intf_in_pkts is not None:
            exp_tx_packets = src_intf_in_pkts - src_in_pkts_before
        elif (direction == 'both'
              and src_intf_in_pkts is not None
              and src_intf_out_pkts is not None):
            exp_tx_packets = (
                (src_intf_in_pkts - src_in_pkts_before)
                + (src_intf_out_pkts - src_out_pkts_before))
        else:
            exp_tx_packets = None

        actual_tx_packets = (
            None if dst_intf_out_pkts is None
            else dst_intf_out_pkts - dst_out_pkts_before)

        if (exp_tx_packets is not None
                and actual_tx_packets is not None
                and (exp_tx_packets * (1 - counter_tolerance)
                     <= actual_tx_packets
                     <= exp_tx_packets * (1 + counter_tolerance))):
            log.debug(
                'Verify span interface counters passed. Expected '
                f'transmitted packets is around {exp_tx_packets} '
                f'with tolerance {counter_tolerance * 100}%, '
                f'got {actual_tx_packets}')
            return True
        log.debug(
            'Verify span interface counters not passed yet. Expected '
            f'transmitted packets is around {exp_tx_packets} with '
            f'tolerance {counter_tolerance * 100}%, '
            f'got {actual_tx_packets}, retrying...')
    log.debug(
        f'Verify span interface counters failed within {max_time} seconds')
    return False
