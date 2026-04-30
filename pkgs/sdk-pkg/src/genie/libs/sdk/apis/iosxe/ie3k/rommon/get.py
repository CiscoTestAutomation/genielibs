import logging
import re

log = logging.getLogger(__name__)

# Matches size and filename for any .SSA.bin image in `dir` output.
# Format: <size>   <filename.SSA.bin>
# Example: -rw-rw-rw-   603742837   ie9k_iosxe.BLD_V1718_THROTTLE_LATEST_20251208_231224.SSA.bin
SSA_IMAGE_PATTERN = r'(\d+)\s+(\S+\.SSA\.bin)'


def get_recovery_details(
    device,
    golden_image: list | None = None,
    tftp_boot: dict | None = None
):
    """
    Get recovery details for IE3k platforms.
    IE3k does not support TFTP booting in ROMMON.

    Args:
        device: device object
        golden_image(`list`): Golden image to boot the device.
        tftp_boot(`dict`): TFTP boot information. Unused in this function.

    Return:
        dict: Recovery data with images to boot.
    """
    if golden_image:
        return {
            'golden_image': golden_image
        }

    ssa_images = []
    for drive in device.settings.BOOT_FILESYSTEM:
        output = device.execute(f'dir {drive}')
        matches = re.findall(SSA_IMAGE_PATTERN, output)
        # Filter out zero-size images (empty/corrupt files that cannot be booted).
        ssa_images.extend([f"{drive}{name}" for size, name in matches if int(size) > 0])

    if ssa_images:
        log.debug(f"{device.name}: Found SSA images: {ssa_images}")
        return {
            'golden_image': ssa_images
        }

    log.warning(f"{device.name}: No SSA image found in {device.settings.BOOT_FILESYSTEM}")
    return {
        'golden_image': []
    }
