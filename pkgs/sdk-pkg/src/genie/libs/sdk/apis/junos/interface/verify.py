"""Common verify functions for interface"""

# Python
import re
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def verify_interfaces_terse_state(device,
                                  interface,
                                  expected_admin_state=None,
                                  expected_link_state=None,
                                  expected_oper_status=None,
                                  max_time=30,
                                  check_interval=10,
                                  expected_result=True):
    """ Verify interfaces terse

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            expected_admin_state (`str`): Expected admin state for interface
                ex.) expected_admin_state = 'up'
            expected_link_state (`str`): Expected link state for interface
                ex.) expected_link_state = 'down'
            expected_oper_status (`str`): Expected oper state for interface
                ex.) expected_oper_status = 'up'
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    interface_terse_out = None
    result = True
    while timeout.iterate():
        try:
            if interface:
                interface_terse_out = device.parse(
                    'show interfaces {interface} terse'.format(
                        interface=interface))
            else:
                interface_terse_out = device.parse('show interfaces terse')
            result = True
        except SchemaEmptyParserError:
            log.info('Failed to parse. Device output might contain nothing.')
            if not expected_result:
                return False
            result = False
            timeout.sleep()
            continue

        for intf, intf_dict in interface_terse_out.items():
            admin_state = intf_dict.get('admin_state', None)
            link_state = intf_dict.get('link_state', None)
            oper_status = intf_dict.get('oper_status', None)
            enabled = intf_dict.get('enabled', None)
            if expected_admin_state and admin_state != expected_admin_state:
                result = False
            if expected_link_state and link_state != expected_link_state:
                result = False
            if expected_oper_status and oper_status != expected_oper_status:
                result = False

            if result == expected_result:
                return expected_result

        timeout.sleep()
    return False

def verify_interface_load_balance(device, 
    load_balance_interfaces,
    interface=None,
    zero_bps_interfaces=None,
    expected_tolerance=10,
    max_time=30, check_interval=10,
    extensive=False):
    """ Verify logical interface load balance

        Args:
            device (`obj`): Device object
            load_balance_interfaces (`list`): List of interfaces to check load balance
            interface (`str`): Pass interface in show command
            zero_bps_interfaces (`list`): List of interfaces to check zero as bps value
            expected_tolerance (`int`): Expected tolerance in load balance of interfaces
            max_time (`int`): Max time, default: 60
            check_interval (`int`): Check interval, default: 10
            extensive (`bool`): Execute show command with extensive

        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        result = True
        try: 
            if interface:
                cmd = 'show interfaces {interface}'.format(interface=interface)
            else:
                cmd = 'show interfaces'
            if extensive:
                cmd = '{cmd} extensive'.format(cmd=cmd)
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        intf_output_bps = device.api.get_interface_logical_output_bps(
            interface=interface,
            logical_interface=load_balance_interfaces[0],
            extensive=True,
            output_dict=out,
        )
        if not intf_output_bps or int(intf_output_bps) == 0:
            timeout.sleep()
            continue
        intf_output_bps = int(intf_output_bps)
        min_value, max_value = device.api.get_tolerance_min_max(
            value=intf_output_bps,
            expected_tolerance=expected_tolerance)

        log.info('Load balance of interfaces {load_balance_interfaces}'
            ' should be between {min_value}<>{max_value} '
            'with tolerance of {expected_tolerance}%'.format(
                load_balance_interfaces=load_balance_interfaces,
                min_value=min_value,
                max_value=max_value,
                expected_tolerance=expected_tolerance,
            ))

        for logical_intf in load_balance_interfaces[1:]:
            intf_output_bps = device.api.get_interface_logical_output_bps(
                interface=interface, logical_interface=logical_intf,
                extensive=True, output_dict=out)

            # Check load balance is within tolerance
            if not intf_output_bps or int(intf_output_bps) < min_value or int(intf_output_bps) > max_value:
                result = False
                log.info('Interface {logical_intf} output-bps: {intf_output_bps} '
                    'is not between {min_value}<>{max_value}'.format(
                        logical_intf=logical_intf,
                        intf_output_bps=intf_output_bps,
                        min_value=min_value,
                        max_value=max_value,
                    ))
                break

        # Check if need to changed "0" bps interfaces
        if zero_bps_interfaces:
            log.info('Load balance of interfaces {zero_bps_interfaces}'
                ' should be "0" bps'.format(
                    zero_bps_interfaces=zero_bps_interfaces
                ))

            for logical_intf in zero_bps_interfaces:
                intf_output_bps = device.api.get_interface_logical_output_bps(
                    interface=interface,
                    logical_interface=logical_intf,
                    extensive=True,
                    output_dict=out)

                if not intf_output_bps or int(intf_output_bps) != 0:
                    log.info('Interface {logical_intf} is not "0" bps'.format(
                        logical_intf=logical_intf
                    ))
                    result = False
                    break

        if result:
            return True
        
        timeout.sleep()
        continue
    
    return False