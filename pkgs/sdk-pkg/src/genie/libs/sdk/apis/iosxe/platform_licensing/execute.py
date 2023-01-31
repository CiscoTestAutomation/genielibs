'''IOSXE execute functions for platform-licensing'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def license_smart_factory_reset(device):
    """ Clears licensing information from the trusted store and memory
        Example : license smart factory reset

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Clearing licensing info on {device.name}')
    config = 'license smart factory reset'
    try:
        device.execute(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to clear licensing info on device {device.name}. Error:\n{e}')

def disable_debug_all(device):
    """ Turns off debugging
        Example : no debug all

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Turns off debugging on {device.name}')
    config = 'no debug all'
    try:
        device.execute(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to turn off debugging on device {device.name}. Error:\n{e}')

def enable_license_smart_authorization_return(device, device_type, mode, path_name=''):
    """ Enable license smart authorization return
        Example : license smart authorization return all online

        Args:
            device ('obj'): device to use
            device_type ('str'): type of device for authorization code return (eg. all, local)
            mode ('str'): authorization code return mode (eg. offline, online)
            path_name ('str'): offline path name
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Enable license smart authorization return on {device.name}')
    if mode.lower() == "offline":
        config = f'license smart authorization return {device_type} {mode} {path_name}'
    else:
        config = f'license smart authorization return {device_type} {mode}'
    try:
        device.execute(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to enable license smart authorization on device {device.name}. Error:\n{e}')

def enable_license_smart_clear_eventlog(device):
    """ Enable license smart clear eventlog
        Example : license smart clear eventlog

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Enable license smart clear eventlog on {device.name}')
    config = 'license smart clear eventlog'
    try:
        device.execute(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to enable license smart clear eventlog on device {device.name}. Error:\n{e}')
