import logging
import re

log = logging.getLogger(__name__)

# Regex pattern to match the golden image filename for IR1100
SPARROW_IMAGE = r'ir1101-universalk9.BLD_.*\.bin'


def get_recovery_details(
    device,
    golden_image: list | None = None,
    tftp_boot: dict | None = None
):
    """
    Get recovery details for IR1100.
    Supports ONLY golden image from usbflash0: or bootflash:.
    IR1100 does not support TFTP booting in ROMMON.

    Args:
        device: device object
        golden_image(`list`): Golden image to boot the device.
        tftp_boot(`dict`): TFTP boot information. Unused in this function.

    Return:
        dict: Recovery data with images to boot

    Raises:
        Exception: If golden_image is empty or no image found in usbflash0: or bootflash:.
    """
    recovery_details = {}

    if golden_image:
        recovery_details['golden_image'] = golden_image
    else:
        # Parse golden image from usbflash0: or bootflash:
        output = device.execute('dir usbflash0:')
        usbflash0_images = re.findall(SPARROW_IMAGE, output)
        if usbflash0_images:
            golden_image_file = next(iter(usbflash0_images))
            recovery_details['golden_image'] = [f"usbflash0:{golden_image_file}"]
            log.info(f"{device.name}: Found golden image {recovery_details['golden_image']}")
        else:
            # Try bootflash: if not found in usbflash0:
            output = device.execute('dir bootflash:')
            bootflash_images = re.findall(SPARROW_IMAGE, output)
            if bootflash_images:
                golden_image_file = next(iter(bootflash_images))
                recovery_details['golden_image'] = [f"bootflash:{golden_image_file}"]
                log.info(f"{device.name}: Found golden image {recovery_details['golden_image']}")
            else:
                # No golden image found
                raise Exception(f"{device.name}: No golden image found in either usbflash0: or bootflash:")

    return recovery_details
