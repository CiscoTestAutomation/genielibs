"""Common verification functions for OSPF"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_ospf3_interface_type(device, interface, interface_type, 
    max_time=60, check_interval=10):
    """ Verifies ospf interface type

        Args:
            device ('obj'): device to use
            interface ('str'): Interface to use
            interface_type ('str'): Interface type
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show ospf3 interface extensive')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        for ospf_interface in out.q.get_values('ospf3-interface'):
            intf = ospf_interface.get('interface-name', None)
            intf_type = ospf_interface.get('interface-type', None)
            if intf == interface and intf_type == interface_type:
                return True
        timeout.sleep()
    return False