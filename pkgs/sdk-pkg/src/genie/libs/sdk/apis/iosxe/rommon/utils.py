''' Utility functions for rommon'''

import logging
from pyats.log.utils import banner
log = logging.getLogger(__name__)

def device_rommon_boot(device, golden_image=None, tftp_boot=None, error_pattern=[]):
    '''Boot device using golden image or using tftp image
        Args:
            device: device object
            golden_image(`list`): Golden image to boot the device.
            tftp_boot:
                image(`list`): Image to boot.
                tftp_server('str'): tftp server information.

        Return:
            None
        Raise:
            Exception
    '''

    log.info(f'Get the recovery details from clean for device {device.name}')
    try:
        recovery_info = device.clean.get('device_recovery', {})
    except AttributeError:
        log.warning(f'There is no recovery info for device {device.name}')
        recovery_info = {}

    # golden_image info from device recovery
    if not golden_image:
        golden_image = recovery_info.get('golden_image', "")

    # tftp info from device recovery
    tftp_boot = tftp_boot or recovery_info.get('tftp_boot', {})
    # get the image and tftp server info
    image = tftp_boot.get('image', [])
    tftp_server = tftp_boot.get('tftp_server', "")


    # To boot using golden image
    if golden_image:
        log.info(banner("Booting device '{}' with the Golden images".\
                        format(device.name)))
        log.info("Golden image information found:\n{}".format(golden_image))
        golden_image = golden_image[0]
        cmd = f"{golden_image}"

    # To boot using tftp rommon variable
    # In this case, we assume the rommon variable TFTP_FILE is set already
    # and booting it using the "boot tftp:" command
    elif getattr(device.clean, 'images', []):
        log.warning('Assuming the rommon variable TFTP_FILE is set and boot using "boot tftp:" command')
        cmd = "tftp:"

    # To boot using tftp information
    elif tftp_server and image:
        log.info(banner("Booting device '{}' with the Tftp images".\
                        format(device.name)))
        log.info("Tftp boot information found:\n{}".format(tftp_boot))

        # To process the image path
        if image[0][0] != '/':
            image[0] = '/' + image[0]

        # To build the tftp command
        cmd_info = ("tftp://", tftp_server, image[0])
        cmd = ''.join(cmd_info)

    else:
        raise Exception('Global recovery only support golden image and tftp '
                         'boot recovery and neither was provided')

    # Timeout for device to reload
    timeout = device.clean.get('device_recovery', {}).get('timeout', 900)

    try:
        # To boot the image from rommon
        device.reload(image_to_boot=cmd, error_pattern=error_pattern, timeout=timeout)
    except Exception as e:
        log.error(str(e))
        raise Exception(f"Failed to boot the device {device.name}", from_exception=e)
    else:
        log.info(f"Successfully boot the device {device.name}")


