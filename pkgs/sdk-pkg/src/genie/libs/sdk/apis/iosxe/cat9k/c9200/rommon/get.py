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
                tftp_server('str'): tftp server name.

        Return:
            dict: Golden image to boot the device
    '''

    recovery_details = {}

    try:
        recovery_info = device.clean.get('device_recovery', {})
    except AttributeError:
        log.warning(f'There is no recovery info for device {device.name}')
        recovery_info = {}

    # tftp boot is not supported in c9200 devices
    # However we use the golden image from the parser output
    try:
        output = device.parse('dir drec0:')
        drec0_files = output.get('dir', {}).get('drec0:', {}).get('files', {})
        if drec0_files:
            golden_image = next(iter(drec0_files), None)
            recovery_details.update({
                'golden_image': [f"drec0:{golden_image}"]
            })

        recovery_details.update({
            'tftp_image': None, # Boot from tftp image not supported
        })
    except Exception as e:
        log.exception(f"Golden image not found for the {device.name}:\n{e}")

    return recovery_details
