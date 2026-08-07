# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

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


def get_mld_snooping_address_count(device):
    """
    Retrieve ipv6 mld snooping address count
    Args:
        device ('obj'): device object
    Returns:
        Dictionary
    Raises:
        None
    """
    cli = "show ipv6 mld snooping address count"
    try:
        out = device.parse(cli)
    except SchemaEmptyParserError:
        log.debug("Command has not returned any results")
        return {}
    return out


def get_ipv6_mld_snooping_address_summary(device, vlan, group):
    """
    Retrieve ipv6 mld snooping groups
    Args:
        device ('obj'): device object
        vlan ('int'): vlan
        group ('str'): multicast group
    Returns:
        Dictionary
    Raises:
        None
    """
    cli = f"show ipv6 mld snooping address vlan {vlan} {group}"
    try:
        out = device.parse(cli)
    except SchemaEmptyParserError:
        log.debug("Command has not returned any results")
        return {}
    return out


def get_mld_snooping(device, vlan=None):
    """
    Get ipv6 mld snooping information
    Args:
        device ('obj'): device object
        vlan ('int', optional): vlan id
    Returns:
        Dictionary
    Raises:
        None
    """
    if vlan:
        cli = f"show ipv6 mld snooping vlan {vlan}"
    else:
        cli = "show ipv6 mld snooping"
    try:
        out = device.parse(cli)
    except SchemaEmptyParserError:
        log.debug("Command has not returned any results")
        return {}
    return out
