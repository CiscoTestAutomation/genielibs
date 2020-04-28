"""Common configure functions for lldp"""

# Python
import logging

log = logging.getLogger(__name__)

def configure_device_lldp(device):
    """ Enables lldp on target device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """
    try:
        device.configure('feature lldp')
    except Exception as e:
        log.error('Failed to configure device: {}'.format(e))
        raise(e)