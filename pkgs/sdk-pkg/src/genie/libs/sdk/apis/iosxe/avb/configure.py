"""Common configure functions for avb"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

log = logging.getLogger(__name__)

def configure_avb(device):
    """ enable avb on device
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure avb
    """
    log.debug("configure avb on device")
    try:
        device.configure("avb")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure avb. Error:\n{e}")

def unconfigure_avb(device):
    """ Unconfigure avb on device
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Unconfigure avb
    """
    log.debug("Unconfigure avb on device")
    try:
        device.configure("no avb")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure avb on device. Error:\n{e}")        