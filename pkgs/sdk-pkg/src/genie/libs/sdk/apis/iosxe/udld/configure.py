"""Common configure functions for udld"""
import logging
# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_udld_alert_mode(device, interface):
    """ Configures UDLD alert mode on Interface 
        Args:
            device (`obj`): Device object
            interface (`str`): interface
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    try:
        output = device.configure([
                         f"interface {interface}", 
                         "udld port alert"
                         ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure udld alert on {interface}, Error: {error}'.format(
                interface=interface, error=e))
    return output
        
def configure_udld(device, interface):
    """ Configures UDLD on Interface 
    Args:
        device (`obj`): Device object
        interface (`str`): interface
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring interface
    """
    try:
        output = device.configure([
                         f"interface {interface}",
                         "udld port"
                        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
        'Could not configure udld on {interface}, Error: {error}'.format(
            interface=interface, error=e))
    return output

def configure_interface_udld_port(device, interface, aggressive_mode=False):
    """ Configures Interface UDLD Port 
        Args:
            device ('obj')                       : device to use
            interface ('str')                    : interface to configure
            aggressive_mode ('boolean',optional) : Enable udld protocol in aggressive mode (Default False)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Configure UDLD Port on interface {interface}")
    configs = list()
    configs.append(f"interface {interface}")
    configs.append('udld port aggressive' if aggressive_mode else 'udld port')
    try:
        device.configure(configs)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not configure Interface UDLD Port. Error: {error}'
        )

def unconfigure_interface_udld_port(device, interface, aggressive_mode=False):
    """ Unconfigures Interface UDLD Port
        Args:
            device ('obj')                       : device to use
            interface ('str')                    : interface to configure
            aggressive_mode ('boolean',optional) : udld protocol in aggressive mode (Default False)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfigure UDLD Port on interface {interface}")
    configs = list()
    configs.append(f"interface {interface}")
    configs.append('no udld port aggressive' if aggressive_mode else 'no udld port')
    try:
        device.configure(configs)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not Unconfigure Interface UDLD Port. Error: {error}'
        )

def configure_udld_message_time(device, message_time):
    """ Configures UDLD Message Time on Target Device globally 
        Args:
            device ('obj')        : device to use
            message_time ('int')  : Time in seconds between sending of messages 1-90
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Configure UDLD message time")
    try:
        device.configure(f"udld message time {message_time}")
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not configure UDLD Message Time. Error: {error}'
        )

def unconfigure_udld_message_time(device):
    """ Unconfigures UDLD Message Time on Target Device globally
        Args:
            device ('obj')  : device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfigure UDLD message time")
    try:
        device.configure('no udld message time')
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not Unconfigure UDLD Message Time. Error: {error}'
        )
