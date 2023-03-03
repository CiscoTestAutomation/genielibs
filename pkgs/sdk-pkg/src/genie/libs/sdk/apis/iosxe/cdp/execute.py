"""Execute cdp related command"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def clear_cdp_table(device):
    """ Clear CDP table on target device globally on the device
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to clear cdp table
    """
    log.info("Executing clear_cdp_table API")
    try:
        device.execute('clear cdp table')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to clear cdp table on device {device} . Error:\n{e}")