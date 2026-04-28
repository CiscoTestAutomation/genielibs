"""Common configure functions for cef"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_ip_cef(device):
    """ Configure ip cef on device

        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("ip cef")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ip cef. Error {e}".format(e=e)
        )


def unconfigure_ip_cef(device):
    """ Unconfigure ip cef on device

        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no ip cef")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure ip cef. Error {e}".format(e=e)
        )
