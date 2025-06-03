'''IOSXE configure functions for ie3k platform '''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

# Logger
log = logging.getLogger(__name__)

def configure_sd(device, timeout=30):
    '''
    Configure - no platform sd disable
    Enables connected SD on device
    Args:
        device ('obj') : Device object
        timeout ('int'): timeout arg for Unicon configure for this CLI (Default value - 30s)
    Returns:
        None
    '''

    try:
        device.configure("no platform sd disable" , timeout=timeout)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable SD - Error:\n{error}".format(error=e)
        )

def unconfigure_sd(device, timeout=30):
    '''
    Configure - platform sd disable
    Disables connected SD on device
    Args:
        device ('obj') : Device object
        timeout ('int'): timeout arg for Unicon configure for this CLI (Default value - 30s)
    Returns:
        None
    '''

    try:
        device.configure("platform sd disable" , timeout=timeout)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable SD - Error:\n{error}".format(error=e)
        )
