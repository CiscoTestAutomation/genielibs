# Python
import logging

log = logging.getLogger(__name__)

def get_recovery_details(device, golden_image: list = None, tftp_boot: dict = None):
    '''
    Get recovery details for the device
        Args:
            device: device object
            golden_image(`list`): Golden image to boot the device.
            tftp_boot:
                image(`list`): Image to boot.
                tftp_server('str'): tftp server information.

        Return:
            dict: Recovery data with images to boot
    '''

    recovery_details = {}
    try:
        recovery_info = device.clean.get('device_recovery', {})
    except AttributeError:
        log.warning(f'There is no recovery info for device {device.name}')
        recovery_info = {}

    # golden_image info from device recovery
    if not golden_image:
        recovery_details.setdefault("golden_image", recovery_info.get('golden_image', []))
    else:
        recovery_details.setdefault("golden_image", golden_image)

    # tftp info from device recovery
    tftp_boot = tftp_boot or recovery_info.get('tftp_boot', {})
    # get the image and tftp server info
    tftp_image = tftp_boot.get('image', []) or getattr(device.clean, 'images', [])
    recovery_details.update({
        'tftp_boot': tftp_boot,
        'tftp_image': tftp_image,
    })

    return recovery_details

def get_tftp_boot_command(device, recovery_info):
    """
    Build the TFTP boot command and image to boot for generic IOS-XE platforms.

    This helper returns the ROMMON TFTP boot command "tftp:" and
    the image filename from the recovery_info.

    Args:
        device: device object
        recovery_info (dict):
           tftp_boot (dict):
               image (list): List of image filenames/paths

    Returns:
        cmd : ROMMON TFTP command, always "tftp:" for generic IOS-XE platforms.
        image_to_boot : The image filename.

    """
    tftp_image_list = recovery_info['tftp_boot'].get('image', [])
    image_to_boot = tftp_image_list[0] if tftp_image_list else None
    cmd = "tftp:"
    return cmd, image_to_boot