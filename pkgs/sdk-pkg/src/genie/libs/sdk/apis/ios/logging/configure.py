"""Common configure functions for logging"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_logging(device, timestamp=True, queue_limit=False,
                      rate_limit=False, buffer_level='debug',
                      buffer_size=5000000):
    """ Configure logging on device

        Args:
            device (`obj`): Device object
            timestamp (`bool`, optional): Enable service timestamp. Defaults to True
            queue_limit (`bool`, optional): If False, sends 'no logging queue-limit'.
                Defaults to False
            rate_limit (`bool`, optional): If False, sends 'no logging rate-limit'.
                Defaults to False
            buffer_level (`str`, optional): Logging buffer level
                (e.g. 'debug', 'informational'). Defaults to 'debug'
            buffer_size (`int`, optional): Logging buffer size in bytes.
                Defaults to 5000000
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    if timestamp:
        cmd.append("service timestamp")
    if not queue_limit:
        cmd.append("no logging queue-limit")
    if not rate_limit:
        cmd.append("no logging rate-limit")
    if buffer_level:
        cmd.append(f"logging buffer {buffer_level}")
    if buffer_size:
        cmd.append(f"logging buffer {buffer_size}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure logging. Error: {e}"
        )


def unconfigure_logging(device, timestamp=True, queue_limit=False,
                        rate_limit=False, buffer_level='debug',
                        buffer_size=5000000):
    """ Unconfigure logging on device

        Args:
            device (`obj`): Device object
            timestamp (`bool`, optional): Disable service timestamp. Defaults to True
            queue_limit (`bool`, optional): If False, restores logging queue-limit.
                Defaults to False
            rate_limit (`bool`, optional): If False, restores logging rate-limit.
                Defaults to False
            buffer_level (`str`, optional): Logging buffer level to remove.
                Defaults to 'debug'
            buffer_size (`int`, optional): Logging buffer size to remove.
                Defaults to 5000000
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    if timestamp:
        cmd.append("no service timestamp")
    if not queue_limit:
        cmd.append("logging queue-limit")
    if not rate_limit:
        cmd.append("logging rate-limit")
    if buffer_level:
        cmd.append(f"no logging buffer {buffer_level}")
    if buffer_size:
        cmd.append(f"no logging buffer {buffer_size}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure logging. Error: {e}"
        )
