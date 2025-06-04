# Python
import logging

logger = logging.getLogger(__name__)

# Import functions from cat9k
from genie.libs.sdk.apis.iosxe.cat9k.configure import (
    configure_ignore_startup_config as iosxe_configure_ignore_startup_config, 
    unconfigure_ignore_startup_config as iosxe_unconfigure_ignore_startup_config
)

# inheriting the functions from /cat9k/configure.py
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