"""Execute Management related command"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def execute_debug_ip(device, protocol, debug_type=None):
    
    """ Execute debug ip commands
        Args:
            device ('obj'): Device object
            protocol('str'): protocol to debug. Ex: ssh, nat, ospf
            debug_type('str', optional): Protocol debug type. Ex: client, detail, packet. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'debug ip {protocol}{f" {debug_type}" if debug_type else ""}'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to execute debug ip {protocol} on device {device}. Error:\n{e}")

def execute_no_debug_ip(device, protocol, debug_type=None):
    
    """ Execute no debug ip commands
        Args:
            device ('obj'): Device object
            protocol('str'): protocol to debug. Ex: ssh, nat, ospf
            debug_type('str', optional): Protocol debug type. Ex: client, detail, packet. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'no debug ip {protocol}{f" {debug_type}" if debug_type else ""}'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to execute no debug ip {protocol} on device {device}. Error:\n{e}")

def execute_clear_console(device, via='telnet'):
    """Clear console on device via another connection
    Args:
        via (str): Connection name from testbed to connect to device
    """
    device.connect(via=via, alias=via)
    device.execute('clear line 0')
    device.telnet.disconnect()
