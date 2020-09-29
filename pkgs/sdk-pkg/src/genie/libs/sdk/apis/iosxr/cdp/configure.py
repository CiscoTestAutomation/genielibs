"""Common configure functions for cdp"""

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
    device.configure(['cdp'])

def unconfigure_cdp(device):
    """ Disable cdp on target device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """
    device.configure(['no cdp'])
    