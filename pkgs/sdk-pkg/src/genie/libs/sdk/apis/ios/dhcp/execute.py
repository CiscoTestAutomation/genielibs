"""Common execute functions for dhcp"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


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


def clear_ip_dhcp_binding(device):
    """execute 'clear ip dhcp binding *' on device
       Args:
            device('obj'): device object
       Returns:
            None
       Raises:
            SubCommandFailure
    """
    log.debug("Executing clear_ip_dhcp_binding API")
    try:
        device.execute("clear ip dhcp binding *")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to clear ip dhcp binding\n{e}'
        )
