"""Execute Crypto related commands"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def execute_show_monitor_event_trace_crypto_all(device, timeout=30):
    """Execute show monitor event-trace crypto all
    
    Args:
        device ('obj'): Device object
        timeout ('int', optional): Maximum time to wait for command execution. Defaults to 30.
        
    Returns:
        str: Command output
        
    Raises:
        SubCommandFailure: Failed to execute command
    """
    cmd = "show monitor event-trace crypto all"
    
    try:
        return device.execute(cmd, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute '{cmd}' on device {device.name}. Error: {e}"
        )

def execute_show_monitor_event_trace_crypto_ipsec_event_clock(device, hour, minute, timeout=30):
    """Execute show monitor event-trace crypto ipsec event clock
    
    Args:
        device ('obj'): Device object
        hour (str or int): Hour value (0-23)
        minute (str or int): Minute value (0-59)
        timeout ('int', optional): Maximum time to wait for command execution. Defaults to 30.
        
    Returns:
        str: Command output
        
    Raises:
        SubCommandFailure: Failed to execute command
    """
    # Validate hour and minute
    assert (0 <= int(hour) <= 23), f"Hour must be between 0 and 23, got {hour}"
    assert (0 <= int(minute) <= 59), f"Minute must be between 0 and 59, got {minute}"

    # Format hour and minute with leading zeros if needed
    hour_str = f"{int(hour):02d}"
    minute_str = f"{int(minute):02d}"

    cmd = f"show monitor event-trace crypto ipsec event clock {hour_str}:{minute_str}"
    
    try:
        return device.execute(cmd, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute '{cmd}' on device {device.name}. Error: {e}"
        )
