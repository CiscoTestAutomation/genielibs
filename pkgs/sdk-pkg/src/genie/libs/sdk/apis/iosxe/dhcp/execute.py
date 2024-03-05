"""Execute DHCP related command"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def clear_ip_dhcp_binding(device):
    """execute 'clear ip dhcp binding *' on device
       Args:
            device('obj'): device object
       Returns:
            None
       Raises:
            SubCommandFailure
    """
    log.info("Executing clear_ip_dhcp_binding API")
    try:
        device.execute("clear ip dhcp binding *")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to clear DHCPv4 server statistics\n{e}'
        )
        
def clear_ip_dhcp_snooping_binding(device):
    """execute 'clear ip dhcp snooping binding *' on device
       Args:
            device('obj'): device object
       Returns:
            None
       Raises:
            SubCommandFailure
    """
    log.info("Executing clear_ip_dhcp_snooping_binding API")
    try:
        device.execute("clear ip dhcp snooping binding *")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to clear DHCPv4 server statistics\n{e}'
        )

def clear_ipv6_dhcp_binding(device):
    """execute 'clear ipv6 dhcp binding *' on device
       Args:
            device('obj'): device object
       Returns:
            None
       Raises:
            SubCommandFailure
    """
    log.info("Executing clear_ipv6_dhcp_binding API")
    try:
        device.execute("clear ipv6 dhcp binding *")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to clear DHCPv6 server statistics\n{e}'
        )

def clear_ip_dhcp_snooping_statistics(device):
    """execute 'clear ip dhcp snooping statistics' on device
       Args:
            device('obj'): device object
       Returns:
            None
       Raises:
            SubCommandFailure
    """
    log.debug("Executing clear_ip_dhcp_snooping_statistics API")

    try:
        device.execute("clear ip dhcp snooping statistics")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to clear dhcp snooping statistics\n{e}'
        )
