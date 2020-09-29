# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_cdp(device):
    """ Enables cdp on target device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """
    device.configure(['cdp enable'])

def unconfigure_cdp(device):
    """ Disable cdp on target device
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    device.configure(['no cdp enable'])