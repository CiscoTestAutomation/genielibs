"""Configure cpp related command"""

# Python
import re
import logging

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

logger = logging.getLogger(__name__)

def enable_cpp_system_default_on_device(device):
    """ Enable cpp system-default on device
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to enable cpp system-default on device
    """
    logger.debug(f"Enable cpp system-default on device {device}")

    configs = [
    "cpp system-default"
    ]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to enable cpp system-default under {device}. Error:\n{e}"
        )
