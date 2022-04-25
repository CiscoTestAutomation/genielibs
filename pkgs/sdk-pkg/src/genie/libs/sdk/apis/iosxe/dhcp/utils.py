"""Utility type functions for DHCPv4"""
# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def clear_dhcpv4_server_stats(device):
    """Clear dhcp server statistics on device
       Args:
            device('obj'): device object
       Returns:
            None
       Raises:
            SubCommandFailure
    """

    try:
        device.execute("clear ip dhcp server statistics")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to clear DHCPv4 server statistics\n{e}'
        )
