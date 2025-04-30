# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def redirect_igmp_snooping_group_info(device, file_name, group_ip, vlan_id):
    """
    Redirect the igmp snooping from the command output to a file in bootflash of the device

    Args:
        device (obj): Device object
        file_name (str): File name to redirect the output of the device to bootflash
        group_ip (str): IGMP group IP address
        vlan_id (int): VLAN IDs from 1-4094
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to execute command
    """
    log.debug(f"Redirecting the output of the command to a file in bootflash of the device")
    try:
        device.execute(f"show tech-support platform igmp-snooping group_ipAddr {group_ip} vlan {vlan_id} | redirect bootflash:{file_name}")
    except SubCommandFailure as e:
        log.error(f"Failed to execute the command: {e}")
