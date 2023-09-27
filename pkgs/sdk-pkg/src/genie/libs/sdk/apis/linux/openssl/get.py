"""Common get functions for openssl"""

import logging
from re import findall
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def get_supported_elliptic_curves(device):
    """
    Args:
        device(`obj`)
    Returns:
        Supported Curves
    """
    cmd = "openssl ecparam -list_curves"

    try:
        curves = findall(r'(\w+)\s*:', device.execute(cmd))
        return curves
    except SubCommandFailure as e:
        SubCommandFailure(f"Failed to get supported elliptic curves. Error\n {e}")
