import logging

log = logging.getLogger(__name__)

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

def get_recovery_details(device, golden_image: list = None, tftp_boot: dict = None):
    """
    Get recovery details for C9200-48P supporting BOTH golden image (from drec0:)
    and TFTP boot.

    Args:
        device: device object
        golden_image(`list`): Golden image to boot the device.
        tftp_boot:
            image(`list`): Image to boot.
            tftp_server('str'): tftp server information.

    Return:
        dict: Recovery data with images to boot

    Raises:
        Exception: If both golden_image and TFTP image are None or empty.
    """
    recovery_details = {}
    try:
        recovery_info = device.clean.get('device_recovery', {})
    except AttributeError:
        log.warning(f'There is no recovery info for device {device.name}')
        recovery_info = {}
    
    # parsing golden image from drec0:
    try:
        output = device.parse('dir drec0:')
        drec0_files = output.get('dir', {}).get('drec0:', {}).get('files', {})
    except SchemaEmptyParserError:
        drec0_files = {}

    if drec0_files:
        golden_image_file = next(iter(drec0_files))
        recovery_details['golden_image'] = [f"drec0:{golden_image_file}"]
        log.info(f"{device.name}: Found golden image {recovery_details['golden_image']}")
    else:
        recovery_details['golden_image'] = None
        log.warning(f"{device.name}: No golden image found in drec0:")

    # tftp info from device recovery
    tftp_boot = tftp_boot or recovery_info.get('tftp_boot', {})
    # get the image and tftp server info
    tftp_image = tftp_boot.get('image', []) or getattr(device.clean, 'images', [])
    recovery_details.update({
        'tftp_boot': tftp_boot,
        'tftp_image': tftp_image,
    })
    
    # Raise exception if both golden_image and tftp_image are None or empty
    if not recovery_details['golden_image'] and not recovery_details['tftp_image']:
        raise Exception(f"{device.name}: No golden image or TFTP image available for recovery")

    return recovery_details

def get_tftp_boot_command(device, recovery_info):
    """
    Build the full TFTP boot command and image-to-boot for ROMMON.
    This helper returns the ROMMON TFTP boot command "tftp://<tftp_server>/<image_filename>" and
    the image filename from the recovery_info

    Args:
        device (obj): Device object.
        recovery_info (dict):
           tftp_boot (dict):
               tftp_server (str): IP or hostname of TFTP server
               image (list): List of image filenames/paths

    Returns:
        cmd: Full TFTP URL ROMMON boot command, e.g.
                    'tftp://<tftp_server>/<image_filename>'.
        image_to_boot: The image filename/path to boot.

    Raises:
        Exception: If either the TFTP server address or boot image is missing
                   in the provided recovery_info.
    """
    tftp_boot_info = recovery_info.get('tftp_boot', {})
    tftp_server = tftp_boot_info.get('tftp_server', '')
    tftp_image_list = tftp_boot_info.get('image', [])
    image_to_boot = tftp_image_list[0] if tftp_image_list else None

    if not tftp_server or not image_to_boot:
        raise Exception(f"{device.name}: Missing TFTP server or image for TFTP boot")
    cmd = f"tftp://{tftp_server}/{image_to_boot}"
    log.info(f"{device.name}: Using  TFTP command: {cmd}")

    return cmd, image_to_boot