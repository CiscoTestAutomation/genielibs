# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_monitor(device, option):
    """ Configure monitor
        Args:
            device ('obj'): Device object
            option ('str'): Monitor option
        Returns:
            None
        Raises:
            SubCommandFailure
        Example:
            >>> configure_monitor(device, 'event-trace')
    """
    config = f'monitor {option}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure 'monitor {option}' on {device}. Error:\n{e}"
        )


def unconfigure_monitor(device, option):
    """ unconfigure monitor
        Args:
            device ('obj'): Device object
            option ('str'): Monitor option
        Returns:
            None
        Raises:
            SubCommandFailure
        Example:
            >>> unconfigure_monitor(device, 'event-trace')
    """
    config = f'no monitor {option}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure 'monitor {option}' on {device}. Error:\n{e}"
        )
