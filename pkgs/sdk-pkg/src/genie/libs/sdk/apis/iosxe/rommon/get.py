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
