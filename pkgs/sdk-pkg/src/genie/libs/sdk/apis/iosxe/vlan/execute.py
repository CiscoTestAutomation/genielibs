'''IOSXE execute functions for vlan'''

# Python
import logging

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

# Logger
log = logging.getLogger(__name__)

def configure_vtp_primary(device):
    """ Configure vtp primary vlan on target device globally on the device
    
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable vtp
    """
    try:
        device.execute('vtp primary vlan')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not enable vtp primary vlan. Error: {e}")