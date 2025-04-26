# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def show_tech_support_platform_l2_matm(device, file_name, vlan_id, mac_address=None):
    """
    Redirect the VLAN or MAC address-specific information from the command output to a file in bootflash of the device
    Args:
        device (`obj`): Device object
        file_name (`str`): name of file to save the output in bootflash
        vlan_id (`int`, Optional): VLAN ID
        mac_address (`str`, Optional): MAC address
    Returns:
        None
    """
    try:
        if mac_address:
            device.execute(f"show tech-support platform layer2 matm vlan {vlan_id} mac {mac_address} | redirect bootflash:{file_name}")
        else:
            device.execute(f"show tech-support platform layer2 matm vlan {vlan_id} | redirect bootflash:{file_name}")
    except SubCommandFailure as e:
        log.error(f"Failed to redirect the output to bootflash: {e}")

