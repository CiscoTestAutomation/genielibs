# Genie
from genie.libs.sdk.apis.iosxe.ie3k.platform.get import (
    get_boot_variables as ie3k_get_boot_variables,
)


def get_boot_variables(device, boot_var, output=None):
    '''Get current or next-reload boot variables on the device.

    IE9k is similar to IE3k, hence reusing IE3k's implementation.

    Args:
        device (`obj`): Device object
        boot_var (`str`): Type of boot variable to return to caller(Eg:current, next)
        output (`str`): output from show boot

    Returns:
        List of boot images or []
    '''
    return ie3k_get_boot_variables(device, boot_var, output)
