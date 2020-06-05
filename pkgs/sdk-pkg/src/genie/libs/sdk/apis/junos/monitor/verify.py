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


def verify_interface_output_pps(device, target_interface,
                                        target_expected_pps,
                                        non_target_expected_pps=None,
                                        target_expected_pps_operator='==',
                                        non_target_expected_pps_operator='==',
                                        max_time=60, check_interval=10):
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
        
        # Check target interface output pps values
        target_interface_output_pps = out.q.contains('{target_interface}'.format(
            target_interface=target_interface
        ), regex=True).value_operator('output-pps', 
            target_expected_pps_operator, target_expected_pps)
        
        if not target_interface_output_pps:
            timeout.sleep()
            continue
        
        if non_target_expected_pps is not None:
            non_target_expected_pps = str(non_target_expected_pps)
            
            # Check non targeted interface output pps values
            non_target_interface_output_pps = out.q.not_contains('{target_interface}'.format(
                target_interface=target_interface
            ), regex=True)
            
            result = False
            for intf in non_target_interface_output_pps.get_values('interface'):
                result = non_target_interface_output_pps.contains('{}|output-pps'.format(intf), 
                regex=True).value_operator('output-pps', 
                    non_target_expected_pps_operator, non_target_expected_pps)
                if not result:
                    log.info('Interface {} found without output pps value: {}'.format(
                        intf,
                        non_target_expected_pps
                    ))
                    break
            if not result:
                timeout.sleep()
                continue
        return True
    return False