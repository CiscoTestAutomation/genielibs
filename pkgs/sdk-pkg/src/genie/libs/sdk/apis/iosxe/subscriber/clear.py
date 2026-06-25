"""Common clear functions for subscriber"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

log = logging.getLogger(__name__)


def clear_subscriber_session_all(device, timeout=60):
    """ Clear all subscriber sessions on device

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
        output = device.execute("clear subscriber session all",
                                reply=dialog, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to clear subscriber session all. Error: {e}"
        )

    return output
