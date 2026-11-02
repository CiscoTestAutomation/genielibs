import logging
import re

log = logging.getLogger(__name__)

# Matches size and filename for any .SSA.bin image in `dir` output.
# Format: <size>   <filename.SSA.bin>
# Example: -rw-rw-rw-   603742837   ie9k_iosxe.BLD_V1718_THROTTLE_LATEST_20251208_231224.SSA.bin
SSA_IMAGE_PATTERN = r'(\d+)\s+(\S+\.SSA\.bin)'


def _as_list(value):
    """Return a list for a scalar or iterable image value."""
    if not value:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def _get_configured_recovery_images(device, golden_image):
    """Get an explicit image or the image published by Clean recovery."""
    if golden_image:
        return _as_list(golden_image)

    try:
        recovery_info = device.clean.get('device_recovery', {}) or {}
    except AttributeError:
        recovery_info = {}

    return _as_list(recovery_info.get('golden_image'))


def _get_image_names(pattern, output):
    """Extract bootable image names from ROMMON ``dir`` output.

    The regular expression is evaluated with :func:`re.findall`. If it has
    multiple capture groups, the last group must contain the filename. The
    first group may contain a decimal file size; a zero value rejects the
    match. With a single capture group (or a full-match pattern), that string
    is treated as the filename. As a fallback for patterns that do not capture
    the size, the matching output line is tokenized and the numeric token
    immediately preceding the filename is checked for zero.

    Args:
        pattern (str): Regular expression that matches an image filename. For
            multi-group expressions, the filename must be the last capture
            group and an optional decimal size may be the first group.
        output (str): Raw output from a ROMMON ``dir <filesystem>`` command.

    Returns:
        list[str]: Matched filenames in output order, excluding zero-byte
            images.
    """
    image_names = []
    for match in re.findall(pattern, output):
        if isinstance(match, tuple):
            if match[0].isdigit() and int(match[0]) == 0:
                continue
            match = match[-1]
        for line in output.splitlines():
            fields = line.split()
            if match not in fields:
                continue
            image_index = fields.index(match)
            if (image_index and fields[image_index - 1].isdigit() and
                    int(fields[image_index - 1]) == 0):
                match = None
            break
        if not match:
            continue
        image_names.append(match)
    return image_names


def _find_boot_images(device, filesystems, image_patterns):
    """Find boot images using regex priority and filesystem order.

    Each filesystem is listed once. Images matching the first regular
    expression are ranked ahead of images matching later expressions, while
    filesystem and directory-listing order are preserved within each regex
    rank. If one path matches multiple expressions, only its highest-priority
    match is retained for that filesystem.

    Args:
        device (obj): Device whose ``execute`` service runs the ROMMON
            directory commands.
        filesystems (str | list[str] | tuple[str, ...]): One filesystem prefix
            or an ordered collection of prefixes, such as ``'flash:'`` or
            ``['flash:', 'sdflash:']``.
        image_patterns (str | list[str] | tuple[str, ...]): One regular
            expression or an ordered collection of expressions. Earlier
            expressions have higher priority. See :func:`_get_image_names`
            for the supported capture-group format.

    Returns:
        list[str]: Filesystem-qualified image paths ordered first by regex
            priority and then by filesystem and directory-listing order.
    """
    if not filesystems or not image_patterns:
        return []
    if not isinstance(filesystems, (list, tuple)):
        filesystems = [filesystems]
    if not isinstance(image_patterns, (list, tuple)):
        image_patterns = [image_patterns]

    ranked_images = [[] for _ in image_patterns]
    for drive in filesystems:
        output = device.execute(f'dir {drive}', timeout=600)
        seen = set()
        for rank, pattern in enumerate(image_patterns):
            for image_name in _get_image_names(pattern, output):
                image_path = f'{drive}{image_name}'
                if image_path not in seen:
                    ranked_images[rank].append(image_path)
                    seen.add(image_path)

    return [
        image_path
        for ranked_group in ranked_images
        for image_path in ranked_group
    ]


def get_recovery_details(
    device,
    golden_image: list | None = None,
    tftp_boot: dict | None = None
):
    """
    Get ordered recovery details for IE3k platforms.
    IE3k does not support TFTP booting in ROMMON. Images are returned in this
    order:

        1. Any .bin images in ROMMON-only emergency filesystems.
        2. A provided golden image, or the image published by Clean recovery.
        3. Images in the normal boot filesystems, using the platform's
           BOOT_FILE_REGEX priority.

    Args:
        device: device object
        golden_image(`list`): Golden image to boot the device.
        tftp_boot(`dict`): TFTP boot information. Unused in this function.

    Return:
        dict: Recovery data with images to boot.
    """
    emergency_filesystems = getattr(
        device.settings, 'EMERGENCY_FILESYSTEMS', [])
    emergency_image_pattern = getattr(
        device.settings, 'EMERGENCY_IMAGE_PATTERN', None)
    emergency_images = _find_boot_images(
        device, emergency_filesystems, emergency_image_pattern)

    recovery_images = _get_configured_recovery_images(device, golden_image)

    boot_filesystems = getattr(device.settings, 'BOOT_FILESYSTEM', [])
    boot_file_regex = getattr(
        device.settings, 'BOOT_FILE_REGEX', SSA_IMAGE_PATTERN)
    filesystem_images = _find_boot_images(
        device, boot_filesystems, boot_file_regex)

    images = list(dict.fromkeys(
        emergency_images + recovery_images + filesystem_images
    ))

    if emergency_images:
        log.info(f'{device.name}: Found emergency images: {emergency_images}')
    if recovery_images:
        log.info(f'{device.name}: Found recovery images: {recovery_images}')
    if filesystem_images:
        log.debug(
            f'{device.name}: Found boot filesystem images: '
            f'{filesystem_images}'
        )
    if not images:
        log.warning(
            f'{device.name}: No bootable image found in emergency '
            f'filesystems {emergency_filesystems} or normal boot filesystems '
            f'{boot_filesystems}'
        )

    return {'golden_image': images}
