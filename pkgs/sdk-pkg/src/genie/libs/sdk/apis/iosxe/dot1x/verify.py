"""Common verify functions for dot1x"""

# Python
import re
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.libs.parser.utils.common import Common
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_template_bind(device, interface, template_name, method='dynamic'):
    '''
    check if template is bound to an interface
    Arg:
        device('obj'):Name of the dut
        interface('str'): switch interface
        template_name('str'): template name
        method(`str`, optional): {static|dynamic}. Default value is dynamic.
    returns:
            True if given template is bound to an interface with given method type
            False otherwise
    '''
    intf = Common.convert_intf_name(interface)
    cmd = "show template binding target {interface}".format(interface=intf)
    try:
        output = device.parse(cmd)
    except SchemaEmptyParserError as e:
        log.error(str(e))
        raise SchemaEmptyParserError("Failed to parse {}".format(cmd))

    for bind_template in output[intf]['interface_templates']:
        if bind_template == template_name:
            if output[intf]['interface_templates'][bind_template]['method'] == method:
                return True
    
    return False
