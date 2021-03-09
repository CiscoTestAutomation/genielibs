"""Common verify functions for interface"""

# Python
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


def verify_interfaces_extensive_state(device,
                                      interface=None,
                                      expected_oper_status='Up',
                                      max_time=30,
                                      check_interval=10):
    """ Verify interfaces extensive

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name. Default to None
            expected_oper_status (`str`): Expected oper state for interface
                Default to 'Up'
                ex.) expected_oper_status = 'Up'
            max_time ('int'): Maximum time to keep checking. Default to 30 secs
            check_interval ('int'): How often to check. Default to 10 secs
        Returns:
            result (`bool`): Verified result
        Raises:
            None
    """

    timeout = Timeout(max_time, check_interval)
    parsed_output = None
    while timeout.iterate():
        try:
            if interface:
                parsed_output = device.parse(
                    'show interfaces {interface} extensive'.format(
                        interface=interface))
            else:
                parsed_output = device.parse('show interfaces extensive')
        except SchemaEmptyParserError:
            log.info('Failed to parse. Device output might contain nothing.')
            timeout.sleep()
            continue

        # example of parsed_output
        #{
        #  "interface-information": {
        #    "physical-interface": [
        #      {
        #        "name": "ae0",
        #        "oper-status": "Up", # <---
        #        "admin-status": {
        #          "@junos:format": "Enabled"

        result = False

        for phy_list in parsed_output.q.get_values('physical-interface'):
            
            if interface and phy_list['name'] == interface:
                if phy_list['oper-status'] == expected_oper_status:
                    return True
            
            if phy_list['oper-status'] == expected_oper_status:
                result = True
            else:
                result = False
                timeout.sleep()
                continue
        
        if result:
            return True
        else:
            timeout.sleep()
            
    return False


def verify_lag_links(device,
                     interface,
                     expected_links,
                     max_time=30,
                     check_interval=10):
    """ Verify links of lag interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name (lag interface)
            expected_links (`list`): list of links to verify
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check
        Returns:
            result (`bool` or None): Verified result
        Raises:
            None
    """

    if not isinstance(expected_links, list):
        log.warn("Given 'expected_links' is not list.")
        return None

    timeout = Timeout(max_time, check_interval)
    parsed_output = None
    while timeout.iterate():
        try:
            if interface:
                parsed_output = device.parse(
                    'show interfaces {interface} extensive'.format(
                        interface=interface))
            else:
                parsed_output = device.parse('show interfaces extensive')
        except SchemaEmptyParserError:
            log.info('Failed to parse. Device output might contain nothing.')
            timeout.sleep()
            continue

        # example of parsed_output
        # {
        #   "interface-information": {
        #     "physical-interface": [
        #       {
        #         (snip)
        #         "logical-interface": [
        #           {
        #               (snip)
        #               "lag-link": [ # <-----
        #                 {
        #                   "input-packets": "104",
        #                   "input-pps": "0",
        #                   "input-bytes": "12628",
        #                   "input-bps": "0",
        #                   "output-packets": "86",
        #                   "output-pps": "0",
        #                   "output-bytes": "7216",
        #                   "output-bps": "0",
        #                   "name": "ge-0/0/0.0"
        #                 },
        #                 (snip)
        #               ],

        lag_link = parsed_output.q.get_values('lag-link')
        link_count = sum(phy_list['name'] in expected_links
                         for phy_list in lag_link)
        if link_count == len(expected_links):
            return True

        timeout.sleep()
    return False


def verify_interface_load_balance(device,
                                  load_balance_interfaces,
                                  interface=None,
                                  zero_bps_interfaces=None,
                                  traffic_upper_limit_interfaces=None,
                                  traffic_upper_limit=None,
                                  expected_tolerance=10,
                                  max_time=30,
                                  check_interval=10,
                                  extensive=False):
    """ Verify logical interface load balance

        Args:
            device (`obj`): Device object
            load_balance_interfaces (`list`): List of interfaces to check load balance
            interface (`str`): Pass interface in show command
            zero_bps_interfaces (`list`): List of interfaces to check zero as bps value
            traffic_upper_limit_interfaces (`list`): List of interfaces to check upper limit value
            traffic_upper_limit (`int`): Upper limit bps value
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
            value=intf_output_bps, expected_tolerance=expected_tolerance)

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
                interface=interface,
                logical_interface=logical_intf,
                extensive=True,
                output_dict=out)

            # Check load balance is within tolerance
            if not intf_output_bps or int(intf_output_bps) < min_value or int(
                    intf_output_bps) > max_value:
                result = False
                log.info(
                    'Interface {logical_intf} output-bps: {intf_output_bps} '
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
                         zero_bps_interfaces=zero_bps_interfaces))

            for logical_intf in zero_bps_interfaces:
                intf_output_bps = device.api.get_interface_logical_output_bps(
                    interface=interface,
                    logical_interface=logical_intf,
                    extensive=True,
                    output_dict=out)

                if not intf_output_bps or int(intf_output_bps) != 0:
                    log.info('Interface {logical_intf} is not "0" bps'.format(
                        logical_intf=logical_intf))
                    result = False
                    break

        if traffic_upper_limit_interfaces and traffic_upper_limit:
            log.info(
                'Load balance of interfaces {traffic_upper_limit_interfaces}'
                ' should be less than or equal to "{traffic_upper_limit}" bps'.
                format(traffic_upper_limit_interfaces=
                       traffic_upper_limit_interfaces,
                       traffic_upper_limit=traffic_upper_limit))

            for logical_intf in traffic_upper_limit_interfaces:
                intf_output_bps = device.api.get_interface_logical_output_bps(
                    interface=interface,
                    logical_interface=logical_intf,
                    extensive=True,
                    output_dict=out)

                if not intf_output_bps or int(intf_output_bps) > int(
                        traffic_upper_limit):
                    log.info(
                        'Interface {logical_intf} is not "{traffic_upper_limit}" bps'
                        .format(logical_intf=logical_intf,
                                traffic_upper_limit=traffic_upper_limit))
                    result = False
                    break

        if result:
            return True

        timeout.sleep()
        continue

    return False


def verify_interfaces_input_output_policer_found(device,
                                                 interface,
                                                 logical_interface,
                                                 max_time=90,
                                                 check_interval=10):
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
                interface=interface.split('.')[0]))
        except SchemaEmptyParserError as e:
            return None

        logical_interface_list = out.q.contains(
            'policer-information|{logical_interface}'.format(
                logical_interface=logical_interface),
            regex=True).get_values('logical-interface')

        for logical_intf_dict in logical_interface_list:
            name = logical_intf_dict.get('name', None)
            if name != logical_interface:
                continue
            policer_information_list = logical_intf_dict.get(
                'policer-information', [])
            if not policer_information_list:
                continue

            policer_input = Dq(
                policer_information_list[0]).get_values('policer-input')
            policer_output = Dq(
                policer_information_list[0]).get_values('policer-output')

            if not policer_input or not policer_output:
                continue

            return True

        timeout.sleep()
    return False


def verify_interfaces_queue_packets(device,
                                    interface,
                                    queue,
                                    expected_packets,
                                    packet_type='trans',
                                    invert=False,
                                    max_time=60,
                                    check_interval=10):
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
                interface=interface))
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

        available_packet_types_ = [
            "queued", "red", "rl-drop", "tail-drop", "trans"
        ]

        if packet_type.lower() in available_packet_types_:
            packets_ = queue_.get("queue-counters-{}-packets".format(
                packet_type.lower()))
            if not packets_:
                timeout.sleep()
                continue
            if op(int(expected_packets), int(packets_)):
                return True
        else:
            log.info(
                "{packet_type} not among available types {type_list}".format(
                    packet_type=packet_type,
                    type_list=available_packet_types_))
            return False

        timeout.sleep()
    return False


def verify_interface_errors(device,
                            interface,
                            expected_error_dict=None,
                            expected_value=None,
                            input=False,
                            output=False,
                            all=True,
                            max_time=30,
                            check_interval=10):
    """ Verify interface input and output errors

        Args:
            device (`obj`): Device object
            interface (`str`): Pass interface in show command
            expected_error_dict (`dict`, Optional): Expected errors dict. Defaults to None
            expected_value (`int`, Optional): Expected errors values. Defaults to None
            input (`bool`, Optional): True if input errors to verify. Default to False.
            output (`bool`, Optional): True if output errors to verify. Default to False.
            all (`bool`, Optional): False if single output error to verify. Default to True.
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds

        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            cmd = 'show interfaces extensive {interface}'.format(
                interface=interface)
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Sample output
        # {"interface-information": {
        #     "physical-interface": [
        #         {
        #             "input-error-list": {
        #                 "framing-errors": "0",
        #                 "input-discards": "0",
        #                 "input-drops": "0",
        #                 "input-errors": "0",
        #                 "input-fifo-errors": "0",
        #                 "input-l2-channel-errors": "0",
        #                 "input-l2-mismatch-timeouts": "0",
        #                 "input-l3-incompletes": "0",
        #                 "input-resource-errors": "0",
        #                 "input-runts": "0"
        #             },
        #             "output-error-list": {
        #                 "aged-packets": "0",
        #                 "carrier-transitions": "0",
        #                 "hs-link-crc-errors": "0",
        #                 "mtu-errors": "0",
        #                 "output-collisions": "0",
        #                 "output-drops": "0",
        #                 "output-errors": "0",
        #                 "output-fifo-errors": "0",
        #                 "output-resource-errors": "0"
        #             },
        #             ...

        physical_interface_list = out.q.get_values("physical-interface")
        for physical_interface in physical_interface_list:
            if input:
                input_errors = physical_interface.get("input-error-list", {})
                if all and input_errors == expected_error_dict:
                    return True
                else:
                    for k, v in input_errors.items():
                        if int(v) != expected_value:
                            return False
                    return True
            if output:
                output_errors = physical_interface.get("output-error-list", {})
                if all and output_errors == expected_error_dict:
                    return True
                else:
                    for k, v in output_errors.items():
                        if int(v) != expected_value:
                            return False
                    return True

        timeout.sleep()
        continue

    return False


def verify_interface_total_queue_counters_dropped_packets(
        device,
        interface,
        expected_queue_packet_count,
        extensive=False,
        max_time=60,
        check_interval=10):
    """ Veirfy queue counters dropped based on interfaces queue

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            expected_queue_packet_count ('dict'): Queue number as key and expected count as value
            extensive ('str'): Flag to check extensive in command
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds
        Returns:
            Boolean

        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            if extensive:
                out = device.parse(
                    'show interfaces extensive {interface}'.format(
                        interface=interface.split('.')[0]))
            else:
                out = device.parse('show interfaces {interface}'.format(
                    interface=interface.split('.')[0]))
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue
        result = True
        for expected_queue_number in expected_queue_packet_count:
            expected_count = str(
                expected_queue_packet_count[expected_queue_number])
            current_count = out.q.get_values(
                'queue-counters-total-drop-packets',
                int(expected_queue_number))
            if expected_count != current_count:
                log.info(
                    'Expected count is {expected_count} for queue {expected_queue_number} '
                    'but found {current_count}'.format(
                        expected_count=expected_count,
                        expected_queue_number=expected_queue_number,
                        current_count=current_count))
                result = False
                break
        if result:
            return True
        timeout.sleep()
    return False


def verify_traffic_statistics_data(device,
                                   interface,
                                   expected_input_packet=None,
                                   expected_output_packet=None,
                                   invert=False,
                                   max_time=60,
                                   check_interval=10):
    """ Verify queue counters dropped based on interfaces queue

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            expected_input_packet ('str'): input packet
            expected_output_packet ('str'): output packet
            invert ('bool'): Check the invert way, default: False
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds
        Returns:
            Boolean

        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show interfaces extensive {interface}'.format(
                interface=interface))
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue

        #"traffic-statistics": {
        #                        "input-bytes": "19732539397",
        #                        "input-packets": "133726363",
        #                       }
        actual_input_packet_list = Dq(out).contains(
            'traffic-statistics').get_values('input-packets')
        actual_output_packet_list = Dq(out).contains(
            'traffic-statistics').get_values('output-packets')

        # check both expected_input_packet and expected_output_packet
        if expected_input_packet and expected_output_packet:
            if invert:
                if str(expected_input_packet)!=actual_input_packet_list[0] and \
                    str(expected_output_packet)!=actual_output_packet_list[0]:
                    return True
            else:
                if str(expected_input_packet)==actual_input_packet_list[0] and \
                    str(expected_output_packet)==actual_output_packet_list[0]:
                    return True

        # only check expected_input_packet 
        elif expected_input_packet:
            if invert:
                if str(expected_input_packet)!=actual_input_packet_list[0]:
                    return True
            else:
                if str(expected_input_packet)==actual_input_packet_list[0]:
                    return True

        # only check expected_output_packet 
        elif expected_output_packet:
            if invert:
                if str(expected_output_packet)!=actual_output_packet_list[0]:
                    return True
            else:
                if str(expected_output_packet)==actual_output_packet_list[0]:
                    return True

        timeout.sleep()

    return False


def verify_no_interface_errors(device,
                               interface,
                               type=None,
                               max_time=30,
                               check_interval=10):
    """ Verify interface input and output errors

        Args:
            device (`obj`): Device object
            interface (`str`): Pass interface in show command
            type (`str`, Optional): Error type to check. Options are 'input', 'output', and None
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds

        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show interfaces extensive {interface}'.format(
                interface=interface))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Sample output
        # {"interface-information": {
        #     "physical-interface": [
        #         {
        #             "input-error-list": {
        #                 "framing-errors": "0",
        #                 "input-discards": "0",
        #                 "input-drops": "0",
        #                 "input-errors": "0",
        #                 "input-fifo-errors": "0",
        #                 "input-l2-channel-errors": "0",
        #                 "input-l2-mismatch-timeouts": "0",
        #                 "input-l3-incompletes": "0",
        #                 "input-resource-errors": "0",
        #                 "input-runts": "0"
        #             },
        #             "output-error-list": {
        #                 "aged-packets": "0",
        #                 "carrier-transitions": "0",
        #                 "hs-link-crc-errors": "0",
        #                 "mtu-errors": "0",
        #                 "output-collisions": "0",
        #                 "output-drops": "0",
        #                 "output-errors": "0",
        #                 "output-fifo-errors": "0",
        #                 "output-resource-errors": "0"
        #             },
        #             ...

        if type and type.lower() == 'input':
            errors = ['input']
        elif type and type.lower() == 'output':
            errors = ['output']
        elif type == None:
            errors = ['input', 'output']
        else:
            raise ValueError('Valid types are "input", "output" and None')

        con = False
        for error in errors:
            err_data = out.q.contains("{}-error-list".format(error))
            if any([int(e.value) for e in err_data]):
                con = True

        if con:
            timeout.sleep()
            continue

        return True

    return False


def verify_interface_hold_time(device,
                               interface,
                               expected_hold_time='0',
                               position='up',
                               max_time=60,
                               check_interval=10):
    """ Verify the hold time of an interface

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            expected_hold_time ('str'): Hold time to check for
            position ('str'): Position to check for. Options are 'up' or 'down'
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds
        Returns:
            Boolean

        Raises:
            None
    """
    expected_hold_time = str(expected_hold_time)
    position = str(position).lower()

    if position not in ['up', 'down']:
        raise ValueError('Acceptable positions are either "up" or "down"')

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show interfaces extensive {interface}'.format(
                interface=interface.split('.')[0]))
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue
        # {'interface-information': {
        #     'physical-interface': [{
        #         'down-hold-time': '0',
        #         'up-hold-time': '0'}]}}

        if out.q.get_values('{}-hold-time'.format(position),
                            0) == expected_hold_time:
            return True

        timeout.sleep()
    return False


def verify_interface_data(device,
                          interface,
                          expected_physical_description=None,
                          expected_logical_description=None,
                          expected_crc_errors=None,
                          extensive=False,
                          max_time=60,
                          check_interval=10):
    """ Verifies interface data based on different criterias

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            expected_physical_description ('str'): expected physical description
            expected_logical_description ('str'): expected logical description
            expected_crc_errors ('str'): expected crc errors
            extensive ('str'): Flag to check extensive in command
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds
        Returns:
            Boolean

        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            if extensive:
                out = device.parse(
                    'show interfaces extensive {interface}'.format(
                        interface=interface.split('.')[0]))
            else:
                out = device.parse('show interfaces {interface}'.format(
                    interface=interface.split('.')[0]))
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue

        #"physical-interface": [
        #    {
        #
        #        "current-physical-address": "00:50:56:ff:56:b6",
        #        "description": "none/100G/in/hktGCS002_ge-0/0/0",
        #        "eth-switch-error": "None",
        #        "ethernet-fec-statistics": {
        #            "fec_ccw_count": "0",
        #            "fec_ccw_error_rate": "0",
        #            "fec_nccw_count": "0",
        #            "fec_nccw_error_rate": "0",
        #        },
        #        "logical-interface": [
        #            {
        #                "address-family": [
        #                    {
        #                        "address-family-flags": {
        #                            "ifff-no-redirects": True,
        #                            "ifff-sendbcast-pkt-to-re": True,
        #                        },
        #                        "address-family-name": "inet",
        #                        "interface-address": {
        #                           "ifa-broadcast": "10.189.5.95",
        #                            "ifa-destination": "10.189.5.92/30",
        #                            "ifa-flags": {
        #                                "ifaf-is-preferred": True,
        #                                "ifaf-is-primary": True,
        #                            },
        #                            "ifa-local": "10.189.5.93",
        #                        },
        #                        "intf-curr-cnt": "1",
        #                        "description": "none/100G/in/hktGCS002_ge-0/0/0",

        if expected_logical_description:
            logical_description = out.q.contains(
                'logical-interface').get_values('description', 0)

        if expected_physical_description:
            physical_description = out.q.contains(
                'physical-interface').not_contains(
                    'logical-interface').get_values('description', 0)

        if expected_crc_errors != None:
            crc_error = out.q.get_values('input-crc-errors', 0)

        if expected_logical_description and logical_description != expected_logical_description:
            timeout.sleep()
            continue

        if expected_physical_description and physical_description != expected_physical_description:
            timeout.sleep()
            continue

        if expected_crc_errors != None and str(crc_error) == str(
                expected_crc_errors):
            timeout.sleep()
            continue
        return True

    return False


def verify_interfaces_terse_no_ipv6(device,
                                    interface,
                                    expected_interface=None,
                                    invert=False,
                                    max_time=60,
                                    check_interval=10):
    """ Verify the hold time of an interface

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            expected_interface('str'): Expected interface, default: None
            invert('bool'): Invert flag, default: False
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds
        Returns:
            Boolean

        Raises:
            None
    """
       
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show interfaces terse {interface}'.format(
                interface=interface))
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue

        # Interface               Admin Link Proto    Local                 Remote
        # ge-0/0/0                up    up
        # ge-0/0/0.0              up    up   inet     10.0.1.1/24
        #                                    multiservice

        # {   "ge-0/0/0": {
        #         "admin_state": "up",
        #         "enabled": True,
        #         "link_state": "up",
        #         "oper_status": "up",
        #     },
        #     "ge-0/0/0.0": {
        #         "admin_state": "up",
        #         "enabled": True,
        #         "link_state": "up",
        #         "oper_status": "up",
        #         "protocol": {
        #             "inet": {"10.0.1.1/24": {"local": "10.0.1.1/24"}},
        #             "multiservice": {},
        #         },
        #     }
        # }

        local_addresses = out.q.get_values('local', None)

        if local_addresses:

            # verify if there is expected interface
            if expected_interface:
                # local_addresses: ["10.0.1.1/24"]
                # expected_interface: "10.0.1.1"
                local_addresses_no_mask = [
                    i.split('/')[0] for i in local_addresses
                ]
                if expected_interface in local_addresses_no_mask:
                    return True
            else:
                # verify there is IPv6 address
                if invert:
                    if bool(':' in i for i in local_addresses):
                        return True

                # verify there is no IPv6 address
                else:
                    if all('.' in i for i in local_addresses):
                        return True

        timeout.sleep()
    return False
        


def verify_interface_minimum_links(device, 
                                      interface, 
                                      expected_num_of_links,
                                      max_time=60, 
                                      check_interval=10):
    """ Verify the minimum links needed via show interfaces {interface} extensive
        Args:
            device ('obj'): Device object
            interface('str'): Interface name    
            expected_num_of_links('int'): Expected minimum links needed
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds
        Returns:
            Boolean

        Raises:
            None
    """            
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show interfaces {interface} extensive'.format(
                interface=interface
            ))
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue
        
        # Example output
        # {'interface-information': {'physical-interface': [{'admin-status': {'@junos:format': 'Enabled'},
        #                                            'local-index': '192',
        #                                            'minimum-bandwidth-in-aggregate': '1bps',
        #                                            'minimum-links-in-aggregate': '1',
        #                                            'name': 'ae0',
        #                                            'oper-status': 'Up',
        #                                            'pad-to-minimum-frame-size': 'Disabled',
        #                                            'snmp-index': '822'}]}}        
        min_links = out.q.get_values("minimum-links-in-aggregate", 0)

        if min_links == str(expected_num_of_links):
            return True
        timeout.sleep()
    return False   

def verify_interface_minumum_bandwidth(device, 
                                      interface, 
                                      expected_bandwidth,
                                      max_time=60, 
                                      check_interval=10):
    """ Verify the minimum bandwidth needed via show interfaces {interface} extensive

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            expected_bandwidth('str'): Expected minimum bandwidth needed
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds
        Returns:
            Boolean

        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show interfaces {interface} extensive'.format(
                interface=interface
            ))
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue
        
        # Example output
        # {'interface-information': {'physical-interface': [{'admin-status': {'@junos:format': 'Enabled'},
        #                                            'local-index': '192',
        #                                            'minimum-bandwidth-in-aggregate': '1bps',
        #                                            'minimum-links-in-aggregate': '1',
        #                                            'name': 'ae0',
        #                                            'oper-status': 'Up',
        #                                            'pad-to-minimum-frame-size': 'Disabled',
        #                                            'snmp-index': '822'}]}}        
        min_bandwidth = out.q.get_values("minimum-bandwidth-in-aggregate", 0)

        if min_bandwidth == expected_bandwidth:
            return True
        timeout.sleep()
    return False

def verify_interface_protocol(device, 
                              interface, 
                              expected_protocol,
                              invert=False,
                              max_time=60, 
                              check_interval=10):
    """ Verify protocol shown via show interfaces terse {interface}

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            expected_protocol('str'): Expected protocol
            invert('bool'): Invert flag, default: False
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds
        Returns:
            Boolean

        Raises:
            None            
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse(
                'show interfaces terse {interface}'.format(interface=interface))
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue   

        #  Example output
        # {
        #     "em1.0": { 
        #         "admin_state": "up",
        #         "enabled": True,
        #         "link_state": "up",
        #         "oper_status": "up",
        #         "protocol": {
        #             "inet": { <---------------------------------------
        #                 "10.0.0.4/8": {"local": "10.0.0.4/8"},
        #                 "172.16.64.1/2": {"local": "172.16.64.1/2"},
        #                 "172.16.64.4/2": {"local": "172.16.64.4/2"},
        #             },
        #             "inet6": { 
        #                 "fe80::250:56ff:fe82:ba52/64": {"local": "fe80::250:56ff:fe82:ba52/64"},
        #                 "2001:db8:8d82:0:a::4/64": {"local": "2001:db8:8d82:0:a::4/64"},
        #             },
        #             "tnp": {"0x4": {"local": "0x4"}},
        #         },
        #     }
        # }

        # ['inet', 'inet6', 'tnp']
        all_protocols = out.q.get_values('protocol',None)

        if invert:
            if expected_protocol not in all_protocols:
                return True
        else:
            if expected_protocol in all_protocols:
                return True
        timeout.sleep()
    return False            

def verify_interface_pps(device, 
                            interface, 
                            pps_type,
                            pps_value,
                            invert=False,
                            max_time=60, 
                            check_interval=10):
    """ Verify interface packets via show interfaces {interface} extensive

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            pps_type('str'): PPS type, "Input" or "Output"
            pps_value('int'): PPS value
            invert('bool'): Invert flag, default: False
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds
        Returns:
            Boolean

        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse(
                'show interfaces {interface} extensive'.format(interface=interface))
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue  
        
        # Example output
        # {
        #     "interface-information": {
        #         "physical-interface": [
        #             {
        #                 "traffic-statistics": {
        #                     "input-bps": "3912",
        #                     "input-bytes": "1900",
        #                     "input-packets": "26",
        #                     "input-pps": "6", <-------------------
        #                     "ipv6-transit-statistics": {
        #                         "input-bytes": "256",
        #                         "input-packets": "4",
        #                         "output-bytes": "0",
        #                         "output-packets": "0"
        #                     },
        #                     "output-bps": "1544",
        #                     "output-bytes": "648",
        #                     "output-packets": "7",
        #                     "output-pps": "2" <--------------------
        #                 },      
        #             }]}}  

        pps_types_dict = {
            "Input":"input-pps",
            "Output":"output-pps",
        }

        compared_pps_type = pps_types_dict[pps_type]

        physical_interface_list = out.q.get_values("physical-interface")   

        for item in physical_interface_list:
            if invert:
                if item["traffic-statistics"][compared_pps_type] != str(pps_value):
                    return True
            else:
                if item["traffic-statistics"][compared_pps_type] == str(pps_value):
                    return True

        timeout.sleep()
    return False           

def verify_lacp_interface(device, 
                                interface, 
                                expected_interface,
                                invert=False,
                                max_time=60, 
                                check_interval=10):
    """ Verify if there is expected_interface via show lacp interfaces {interface}            
        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            expected_interface('str'): Expected interface
            invert('bool'): Invert flag, default: False            
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds
        Returns:
            Boolean

        Raises:
            None
    """    
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse(
                'show lacp interfaces {interface}'.format(
                    interface=interface))
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue   

        # Example output
        # {
        #     "lacp-interface-information-list": {
        #         "lacp-interface-information": {
        #             "lag-lacp-header": {"aggregate-name": "ae4"},
        #             "lag-lacp-protocol": [
        #                 {
        #                     "lacp-mux-state": "Collecting distributing",
        #                     "lacp-receive-state": "Current",
        #                     "lacp-transmit-state": "Fast periodic",
        #                     "name": "xe-3/0/1", <---------------------
        #                 }
        #             ],
        #             "lag-lacp-state": [
        #                 {
        #                     "lacp-activity": "Active",
        #                     "lacp-aggregation": "Yes",
        #                     "lacp-collecting": "Yes",
        #                     "lacp-defaulted": "No",
        #                     "lacp-distributing": "Yes",
        #                     "lacp-expired": "No",
        #                     "lacp-role": "Actor",
        #                     "lacp-synchronization": "Yes",
        #                     "lacp-timeout": "Fast",
        #                     "name": "xe-3/0/1", <---------------------
        #                 },
        #             ],
        #         }
        #     }
        # }

        names = out.q.get_values('name', None)

        if invert:
            if expected_interface not in names:
                return True

        else:
            if expected_interface in names:
                return True

        timeout.sleep()

    return False            

def verify_interface_mtu(device, 
                        interface, 
                        expected_mtu,
                        max_time=60, 
                        check_interval=10):
    """ Verify the interface mtu is the expected value via 'show interfaces {interface} extensive'           
        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            expected_mtu('str'): Expected mtu           
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds
        Returns:
            Boolean

        Raises:
            None
    """    
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse(
                'show interfaces {interface} extensive'.format(interface=interface))
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue

        # Sample output
        # {
        # "interface-information": {
        #     "physical-interface": [
        #         {
        #         "mru": "1522",
        #         "mtu": "1514", <-------------
        #         "name": "et-0/0/0",

        mtu = out.q.get_values("mtu", 0)

        if str(mtu) == str(expected_mtu):
            return True

        timeout.sleep()
    return False          
