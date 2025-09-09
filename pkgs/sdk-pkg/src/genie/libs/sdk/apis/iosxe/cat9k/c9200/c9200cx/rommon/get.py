# Python
import logging

from genie.libs.sdk.apis.iosxe.cat9k.c9200.rommon.get import get_recovery_details as _get_recovery_details

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

    return _get_recovery_details(device=device,
                                 golden_image=golden_image,
                                 tftp_boot=tftp_boot)
