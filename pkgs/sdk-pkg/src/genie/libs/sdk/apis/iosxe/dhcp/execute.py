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

def clear_ip_dhcp_snooping_track_server(device):
    """execute 'clear ip dhcp snooping binding *' on device
       Args:
            device('obj'): device object
       Returns:
            None
       Raises:
            SubCommandFailure
    """
    log.info("Executing clear_ip_dhcp_snooping_track_server API")
    try:
        device.execute("clear ip dhcp snooping track server all")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to clear dhcp snooping track server\n{e}'
        )
    
def release_dhcp(device, interface):
    """Release DHCP lease on interface
       Args:
            device('obj'): device object
            interface('str'): Interface to release
       Returns:
            None
       Raises:
            SubCommandFailure
    """
    log.debug("Executing release_dhcp API")
    try:
        device.execute("release dhcp {interface}".format(interface=interface))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to release DHCP lease\n{e}'
        )

def renew_dhcp(device, interface):
    """Renew DHCP lease on interface
       Args:
            device('obj'): device object
            interface('str'): Interface to renew
       Returns:
            None
       Raises:
            SubCommandFailure
    """
    log.debug("Executing renew_dhcp API")
    try:
        device.execute("renew dhcp {interface}".format(interface=interface))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to renew DHCP lease\n{e}'
        )