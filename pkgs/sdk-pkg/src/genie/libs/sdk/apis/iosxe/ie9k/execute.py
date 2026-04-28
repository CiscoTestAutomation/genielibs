# Genie
from genie.libs.sdk.apis.iosxe.ie3k.execute import (
    execute_rommon_reset as ie3k_execute_rommon_reset
)


def execute_rommon_reset(device, timeout=300):
    '''Execute the reset command in rommon mode.

    IE9k is similar to IE3k, hence reusing IE3k's implementation.

    Args:
        device ('obj'): Device object.
        timeout ('int'): Max time to set config-register in seconds.

    Returns:
        None

    Raises:
        Exception: If failed to execute reset command in rommon mode.
    '''
    ie3k_execute_rommon_reset(device, timeout)
