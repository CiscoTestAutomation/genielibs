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

def verify_no_access_session(device, interface):
    '''
    Verify access-session monitor present in the interface 
    Args:
        device ('obj'): device object
        interface ('str'): interface to check
    Returns:
        result(bool): True if present else false
    Raises:
        SubCommandFailure: If command not executed raises subcommand failure error
    '''

    log.info('Verify if Access session monitor present on the interface')
    cmd = f'show derived-config interface {interface}'

    try:
        sh_derived_conf = device.execute(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure('Could not execute CLI on {device}. Error: {error}'.format(device = device, error = e))

    access_session = re.search('no access-session monitor', sh_derived_conf)
    if access_session:
        log.info('No Access session monitor present on the interface {}'.format(interface))
        return True
    else:
        log.info('No Access session monitor not present on the interface {}'.format(interface))
        return False
