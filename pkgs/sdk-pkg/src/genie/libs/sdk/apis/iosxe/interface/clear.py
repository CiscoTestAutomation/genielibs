# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure


# Logger

log = logging.getLogger(__name__)

def clear_interface_range(device, interface, interface_range):
    """ clear interface range
        Args:
            device (`obj`): Device object
            interface('str'): interface name
            interface_range('str'): interface range
        Return:
            None
        Raise:
            SubCommandFailure
    """
    cmd = []
    cmd.append(f'default interface range {interface} {interface_range}')
    cmd.append(f'no interface range {interface} {interface_range}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not clear interface range on {interface}. Error:\n{e}"
        )

def clear_ip_dhcp_snooping_binding_on_interface(device, interface):
    """ Clear ip dhcp snooping binding on interface
        Args:
            device (`obj`): Device object
            interface('str'): interface name
        Return:
            None
        Raise:
            SubCommandFailure
    """
    log.debug("Executing clear_ip_dhcp_snooping_binding_on_interface API")
    cmd = [f'clear ip dhcp snooping binding interface {interface}']
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to clear DHCPv4 server statistics on {interface} \n{e}'
        )