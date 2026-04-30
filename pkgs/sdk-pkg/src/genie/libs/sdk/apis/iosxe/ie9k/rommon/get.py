# Genie
from genie.libs.sdk.apis.iosxe.ie3k.rommon.get import (
    get_recovery_details as ie3k_get_recovery_details
)


def get_recovery_details(
    device,
    golden_image: list | None = None,
    tftp_boot: dict | None = None
):
    """Get recovery details for IE9k platforms.

    IE9k is similar to IE3k, hence reusing IE3k's implementation.

    Args:
        device: device object
        golden_image(`list`): Golden image to boot the device.
        tftp_boot(`dict`): Unused, IE9k does not support tftp boot in rommon.

    Return:
        dict: Recovery data with images to boot.
    """
    return ie3k_get_recovery_details(device, golden_image, tftp_boot)
