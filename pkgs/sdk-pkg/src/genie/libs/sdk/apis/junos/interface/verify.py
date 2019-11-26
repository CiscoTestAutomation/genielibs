"""Common verify functions for interface"""

# Python
import re
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def verify_interfaces_terse_state(device, interface, expected_admin_state=None, expected_link_state=None, expected_oper_status=None, max_time=30, check_interval=10, expected_result=True):
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
                interface_terse_out = device.parse('show interfaces {interface} terse'.format(
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
