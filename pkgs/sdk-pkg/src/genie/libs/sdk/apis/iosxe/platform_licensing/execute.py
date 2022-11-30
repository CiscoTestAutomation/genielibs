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