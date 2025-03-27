"""Execute DHCP related command"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def clear_ipv6_dhcp_conflict(device):
    """execute 'clear ipv6 dhcp conflict *' on device
       Args:
            device('obj'): device object
       Returns:
            None
       Raises:
            SubCommandFailure
    """
    log.debug("Executing clear_ipv6_dhcp_conflict API")
    try:
        device.execute("clear ipv6 dhcp conflict *")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to clear ipv6 dhcp conflict\n{e}'
        )