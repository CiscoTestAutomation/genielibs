"""Common verify functions for routing"""

# Python
import re
import logging
from prettytable import PrettyTable

# pyATS
from genie.utils import Dq

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def verify_interface_output_pps(device,
                                target_interface,
                                target_expected_pps,
                                non_target_expected_pps=None,
                                target_expected_pps_operator='==',
                                non_target_expected_pps_operator='==',
                                max_time=60,
                                check_interval=10):
    """
        Execute the command "monitor interface traffic" and verify that the target
        interfaces output-pps matches {target_expected_pps} and verify that all
        other interfaces output-pps matches {non_target_expected_pps}.
        {non_target_expected_pps} and {target_expected_pps} are strings that
        contain integers with the possibly of "<" or ">" to allow a range".

        Example:
            uut.api.verify_interface_output_pps(
                target_interface='ge-0/0/0',
                target_expected_pps='0',
                target_expected_pps_operator='>',
                non_target_expected_pps_operator='0',
                non_target_expected_pps='=='
            )

        Args:
            target_interface ('str'): Interface to target
            non_target_expected_pps ('str'): output-pps to expect on non target interfaces
            target_expected_pps ('str'): output-pps to expect on the target interface
            target_expected_pps_operator ('str'): Comparison operator
            non_target_expected_pps_operator ('str'): Comparison operator
            max_time (`int`): Max time, default: 60
            check_interval (`int`): Check interval, default: 10
        Raises:
            Parser exceptions

        Returns:
            Boolean
    """
    target_expected_pps = str(target_expected_pps)
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("monitor interface traffic")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dict
        # {
        #     "monitor-time": {
        #         "06:01:12": {
        #             "hostname": "genie",
        #             "interface": {
        #                 "ge-0.0.0": {
        #                     "output-packets": 0
        #                 },
        #             }
        #         }
        #     }
        # }

        # when there is no output:
        # out = '''
        # 
        # {master}
        # '''
        if out == {'no-output': True}:
            timeout.sleep()
            continue
        
        # Check target interface output pps values
        target_interface_output_pps = out.q.contains(
            '{target_interface}'.format(target_interface=target_interface),
            regex=True).value_operator('output-pps',
                                       target_expected_pps_operator,
                                       target_expected_pps)

        if not target_interface_output_pps:
            timeout.sleep()
            continue

        if non_target_expected_pps is not None:
            non_target_expected_pps = str(non_target_expected_pps)

            # Check non targeted interface output pps values
            non_target_interface_output_pps = out.q.not_contains(
                '{target_interface}'.format(target_interface=target_interface),
                regex=True)

            result = False
            for intf in non_target_interface_output_pps.get_values(
                    'interface'):
                result = non_target_interface_output_pps.contains(
                    '{}|output-pps'.format(intf), regex=True).value_operator(
                        'output-pps', non_target_expected_pps_operator,
                        non_target_expected_pps)
                if not result:
                    log.info('Interface {} found without output pps value: {}'.
                             format(intf, non_target_expected_pps))
                    break
            if not result:
                timeout.sleep()
                continue
        return True
    return False


def verify_interface_output_pps_load_balance(device,
                                             interfaces,
                                             expected_tolerance=10,
                                             max_time=60,
                                             check_interval=10):
    """
        Execute the command "monitor interface traffic" and verify
        output-pps of interfaces is within tolerance

        Example:
            device.api.verify_interface_output_pps_load_balance(
                interfaces=['ge-0/0/0.1', 'ge-0/0/1.1'],
                expected_tolerance=10,
                max_time=60,
                check_interval=10)

        Args:
            Device ('obj'): Device object
            interfaces ('list'): List of interfaces 
            expected_tolerance ('int'): Expected tolerance value
            max_time (`int`): Max time, default: 60
            check_interval (`int`): Check interval, default: 10
        Raises:
            Parser exceptions

        Returns:
            Boolean
    """

    if len(interfaces) <= 1:
        log.error('interfaces must contain two or more items in list')
        return False

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("monitor interface traffic")
        except SchemaEmptyParserError:
            result = False
            timeout.sleep()
            continue

        # Example dict
        # {
        #     "monitor-time": {
        #         "06:01:12": {
        #             "hostname": "genie",
        #             "interface": {
        #                 "ge-0.0.0": {
        #                     "output-packets": 0
        #                 },
        #             }
        #         }
        #     }
        # }

        # Get first interface inorder to compare output-pps with other interfaces
        # Convert Logical interface to Physcial interface
        intf = interfaces[0].split('.')[0]
        try:
            # Get first interface output-pps value
            intf_output_pps = out.q.contains(intf). \
                get_values('output-pps').pop()

            # Check if output-pps is not 0 else skip
            if int(intf_output_pps) == 0:
                result = False
                timeout.sleep()
                continue
        except IndexError:
            result = False
            log.error(
                'Cannot find output-pps value for interface {}'.format(intf))
            timeout.sleep()
            continue

        # Expected tolerance %
        tolerance = (intf_output_pps * expected_tolerance) / 100

        # Minimum tolerance value
        min_value = abs(intf_output_pps - tolerance)

        # Maximum tolerance value
        max_value = abs(intf_output_pps + tolerance)

        result = True
        # Loop interfaces starting from 2nd index
        for interface in interfaces[1:]:

            # Convert Logical interface to Physcial interface
            interface = interface.split('.')[0]
            try:

                # Get output-pps for current interface
                output_pps = out.q.contains(interface). \
                    get_values('output-pps').pop()

                # Check if output-pps is not 0 else skip
                if int(output_pps) == 0:
                    result = False
                    timeout.sleep()
                    continue
            except IndexError:
                result = False
                log.error(
                    'Cannot find output-pps value for interface {}'.format(
                        interface))
                break

            # Check load balance is within tolerance
            if output_pps < min_value or output_pps > max_value:
                result = False
                log.error(
                    'Difference between interfaces is more than tolerance {}'.
                    format(expected_tolerance))
                break

        if result:
            return True
        timeout.sleep()
    return False
