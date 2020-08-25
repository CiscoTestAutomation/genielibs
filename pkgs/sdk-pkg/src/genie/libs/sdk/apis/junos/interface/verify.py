"""Common verify functions for interface"""

# Python
import re
import logging
import operator

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

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

def verify_interfaces_input_output_policer_found(device, interface, logical_interface, 
    max_time=90, check_interval=10):
    """ Verify input and output policer value for interface

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            logical_interface ('str'): Logical interface name
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check
        Returns:
            Boolean

        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    # Dictionary:
    # "interface-policer-information": {
    #     "physical-interface": [
    #         {
    #             "admin-status": "up",
    #             "logical-interface": [
    #                 {
    #                     "admin-status": "up",
    #                     "name": "ge-0/0/2.0",
    #                     "oper-status": "up",
    #                     "policer-information": [
    #                         {
    #                             "policer-family": "inet",
    #                             "policer-input": "GE_1M-ge-0/0/2.0-log_int-i",
    #                             "policer-output": "GE_1M-ge-0/0/2.0-log_int-o"
    while timeout.iterate():
        try:
            out = device.parse('show interfaces policers {interface}'.format(
                interface=interface.split('.')[0]
            ))
        except SchemaEmptyParserError as e:
            return None
        
        logical_interface_list = out.q.contains('policer-information|{logical_interface}'.format(logical_interface=logical_interface),
            regex=True).get_values('logical-interface')

        for logical_intf_dict in logical_interface_list:
            name = logical_intf_dict.get('name', None)
            if name != logical_interface:
                continue
            policer_information_list = logical_intf_dict.get('policer-information', [])
            if not policer_information_list:
                continue
            
            policer_input = Dq(policer_information_list[0]).get_values('policer-input')
            policer_output = Dq(policer_information_list[0]).get_values('policer-output')

            if not policer_input or not policer_output:
                continue

            return True

        timeout.sleep()
    return False

def verify_interfaces_queue_packets(device, interface, queue, expected_packets,
    packet_type='trans', invert=False, max_time=60, check_interval=10):
    """ Verifies number of packets in an interface queue

    Args:
        device (obj): Device object
        interface (str): Interface name
        queue (int): Queue number
        expected_packets (int): Expected number of packets
        packet_type (str, optional): Packet type to check for. Defaults to queued.
        invert (bool, optional): Inverts from equals to not equals. Defaults to False.
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:
        bool: True/False
    """

    op = operator.eq
    if invert:
        op = operator.ne

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show interfaces queue {interface}'.format(
                interface=interface
            ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        queue_ = out.q.get_values('queue', queue)
        if not queue_:
            timeout.sleep()
            continue

        # Example Dict
        # "queue": [
        #                 {
        #                     "queue-counters-queued-packets": "1470816406",
        #                     "queue-counters-red-packets": "0",
        #                     "queue-counters-tail-drop-packets": "0",
        #                     "queue-counters-rl-drop-packets": "0",
        #                 },]

        available_packet_types_ = ["queued", "red", "rl-drop", "tail-drop", "trans"]

        if packet_type.lower() in available_packet_types_:
            packets_ = queue_.get("queue-counters-{}-packets".format(packet_type.lower()))
            if not packets_:
                timeout.sleep()
                continue
            if op(int(expected_packets), int(packets_)):
                return True
        else:
            log.info("{packet_type} not among available types {type_list}".format(
                packet_type=packet_type,
                type_list=available_packet_types_
            ))
            return False
        
        timeout.sleep()
    return False