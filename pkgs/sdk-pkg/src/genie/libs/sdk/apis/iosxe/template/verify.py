"""Common verification functions for interface templates"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.libs.parser.utils.common import Common
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_show_template(device, template_name, interface=None):
    """ Verify show template {template_name}
        Args:
            device('obj'): device object
            template_name('str'): template_name name
            interface('str', Optional): interface
        Returns:
            Bool
        Raises:
            None
    """
    output = device.parse(f"show template {template_name}")
    template = output.get('template', None)
    interfaces = output.get('bound', [])
    interfaces = [Common.convert_intf_name(intf) for intf in interfaces]

    if template != template_name:
        log.info(f"Failed to find the template. actual: {template}, expected: {template_name}")
        return False

    if interface not in interfaces:
        log.info(f"Failed to find the bound interface. {interface} in list {interfaces}")
        return False

    return True

def verify_show_template_empty(device, template_name):
    """ Verify show template {template_name}
        Args:
            device('obj'): device object
            template_name('str'): template_name name
        Returns:
            Bool
        Raises:
            None
    """
    try:
        device.parse(f"show template {template_name}")
    except SchemaEmptyParserError:
        return True
    return False
