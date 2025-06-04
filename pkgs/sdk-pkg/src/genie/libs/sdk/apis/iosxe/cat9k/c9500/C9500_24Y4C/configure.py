# Python
import logging

# Import functions from C9500_48Y4C
from genie.libs.sdk.apis.iosxe.cat9k.c9500.C9500_48Y4C.configure import (
    configure_ignore_startup_config as iosxe_configure_ignore_startup_config, 
    unconfigure_ignore_startup_config as iosxe_unconfigure_ignore_startup_config
)

logger = logging.getLogger(__name__)

# inheriting the functions from /C9500_48Y4C/configure.py
def configure_ignore_startup_config(device):
    '''  To configure ignore startup config.
    Args:
        device (`obj`): Device object
    Returns:
        None
    Raises:
        SubCommandFailure : Failed to configure the device
    '''
    return iosxe_configure_ignore_startup_config(device)

def unconfigure_ignore_startup_config(device):
    '''  To configure ignore startup config.
    Args:
        device (`obj`): Device object
    Returns:
        None
    Raises:
        SubCommandFailure : Failed to configure the device
    '''
    return iosxe_unconfigure_ignore_startup_config(device)