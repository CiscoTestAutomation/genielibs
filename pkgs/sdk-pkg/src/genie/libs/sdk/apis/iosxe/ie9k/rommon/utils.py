# Genie
from genie.libs.sdk.apis.iosxe.ie3k.rommon.utils import (
    device_rommon_boot as ie3k_device_rommon_boot
)


def device_rommon_boot(device, golden_image=None, tftp_boot=None, error_pattern=[],
                       grub_activity_pattern=None, timeout=None):
    '''Boot device using `golden_image` or with images obtained from `get_recovery_details`.

    IE9k is similar to IE3k, hence reusing IE3k's implementation.

    Args:
        device: device object
        golden_image(`list`): Golden image to boot the device.
        tftp_boot: Unused, TFTP boot is not supported for IE9k.
        error_pattern(`list`): Unused.
        grub_activity_pattern(`str`): Unused, Grub boot is not supported for IE9k.
        timeout(`int`, optional): Timeout for boot operation. If not provided,
            uses device_recovery timeout or defaults to 3600 seconds.

    Return:
        None

    Raise:
        Exception if:
            1. If no golden image obtained from get_recovery_details.
            2. If device fails to boot within the timeout period.
            3. If device remains in rommon state after boot attempt.
    '''
    ie3k_device_rommon_boot(device, golden_image, tftp_boot, error_pattern,
                            grub_activity_pattern, timeout)
