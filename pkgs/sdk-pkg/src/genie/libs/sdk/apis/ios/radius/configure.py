"""Common configure functions for radius"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_radius_server_key(device, key):
    """ Configure radius-server key on device

        Args:
            device (`obj`): Device object
            key (`str`): Shared secret key
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"radius-server key {key}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure radius-server key. Error: {e}"
        )


def unconfigure_radius_server_key(device, key):
    """ Unconfigure radius-server key on device

        Args:
            device (`obj`): Device object
            key (`str`): Shared secret key
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"no radius-server key {key}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure radius-server key. Error: {e}"
        )
