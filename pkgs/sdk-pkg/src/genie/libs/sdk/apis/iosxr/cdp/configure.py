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
    """
    try:
        device.configure(['cdp', 'commit'])
    except Exception as e:
        log.error('Failed to configure device: {}'.format(e))
        raise(e)
    
    