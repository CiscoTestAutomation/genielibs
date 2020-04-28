"""Common configure functions for cdp"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_device_cdp(device):
    """ Enables cdp on target device
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    interface_list = device.parse('show interfaces description')
    command_list = ['cdp run']
    for interface in interface_list['interfaces']:
        command_list.append('interface ' + interface)
        command_list.append('cdp enable')
    try:
        device.configure(command_list)
    except Exception as e:
        log.error('Failed to configure device: {}'.format(e))
        raise(e)