"""Common configure functions for dns"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def unconfigure_ip_domain_lookup(device):
    """ Unconfigure ip domain lookup on device

        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no ip domain lookup")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip domain lookup. Error: {e}"
        )


def configure_ip_domain_lookup(device):
    """ Configure ip domain lookup on device

        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("ip domain lookup")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip domain lookup. Error: {e}"
        )
