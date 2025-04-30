# Python
import logging


log = logging.getLogger(__name__)

def show_tech_support_platform_mld_snooping(device, file_name, grp_ipv6, vlan_id):
    '''
    Redirects mld snooping output to the device bootflash
    
    Args:
        device (`obj`): Device object
        file_name (`str`): File name
        grp_ipv6 (`str`): mld snooping ipv6 Group address
        vlan_id (`str`): VLAN IDs from 1-4094 mld
    Returns:
        None
    Raises:
        Exception: If failed to execute command
    '''
    
    log.debug("Redirecting mld snooping output to the device bootflash")
    try:
        device.execute(f'show tech-support platform mld_snooping Group_ipv6Addr {grp_ipv6} vlan {vlan_id} | redirect bootflash:{file_name}')
    except Exception as e:
        log.error(f"Failed to execute command: {e}")
