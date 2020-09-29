"""Common verify functions for cdp"""

# Python
import logging
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)

def verify_cdp_in_state(device, max_time=60, check_interval=10):
    """ Verify that cdp is enabled on the device
        Args:
            device = device to check status on
        returns:
            True if cdp is enabled, false in all other cases
    """
    timeout = Timeout(max_time, check_interval, True)
    while timeout.iterate():
        try:
            device.parse('show cdp neighbors')
            return True
        except Exception:
            timeout.sleep()
    return False