"""Common clear functions for logging"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

log = logging.getLogger(__name__)


def clear_logging(device, timeout=60):
    """ Clear logging on device

        Args:
            device (`obj`): Device object
            timeout (`int`, optional): Timeout in seconds. Defaults to 60
        Returns:
            output (`str`): Output of execution
        Raises:
            SubCommandFailure
    """
    dialog = Dialog([
        Statement(
            pattern=r'\[confirm\].*',
            action='sendline(\r)',
            loop_continue=True,
            continue_timer=False
        )
    ])

    try:
        output = device.execute("clear logging", reply=dialog, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not clear logging on {device}. Error: {e}"
        )

    return output
