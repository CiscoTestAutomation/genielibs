"""Common configure functions for lldp"""

# Python
import logging

log = logging.getLogger(__name__)

def configure_lldp(device):
    """ Enables lldp on target device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """
    device.configure('lldp run')


def unconfigure_lldp(device):
    """ Disables lldp on target device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """
    device.configure('no lldp run')