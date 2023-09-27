"""Common get functions for linux"""

import logging
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def get_file_contents(device, filename):
    """
    Args:
        device(`obj`)
        filename(`str`): Absolute path to the file
    Returns:
        File contents as a string
    """
    cmd = f"cat {filename}"

    try:
        return str(device.execute(cmd))
    except SubCommandFailure as e:
        SubCommandFailure(f"Failed to get supported elliptic curves. Error\n {e}")
