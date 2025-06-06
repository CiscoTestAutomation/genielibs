"""Common get info functions for vlan"""

# Python
import re
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def get_vlan_info(device):
    '''
    Api method to call parser and return device vlan information
    Args:
            device ('obj'): Device object
    Returns:
            Dictionary: Vlan information
    '''    
    try:
        return device.parse('show vlan') 
    except SchemaEmptyParserError as e:
        log.error('Device {} has no vlan information: {}'.format(device.name, e))
        return None

def get_vlan_name_status(device):
    """
    Generate VLAN information with VLAN ID, VLAN name, VLAN state, and associated VRFs.

    Args:
        device (obj): Device object

    Returns:
        dict: Dictionary containing VLAN information in the desired format
    """
    try:
        # Execute 'show vlan' command
        vlan_output = device.parse("show vlan")

        # Execute 'show vrf' command
        vrf_output = device.parse("show vrf")
        
    except SchemaEmptyParserError as e:
        # Log errors and return an empty dictionary if the parser returns empty results
        log.error(f"Failed to retrieve VLAN information: {e}")
        return {}

    # Initialize dictionary to store VLAN information
    vlan_info = {'vlan_id': [], 'vlan_name': [], 'vlan_state': [], 'vrf': []}

    # Iterate over VLANs
    for vlan_id, vlan_details in vlan_output.get('vlans', {}).items():
        # Get VLAN name and state
        vlan_name = vlan_details.get('name', 'Unknown')
        vlan_state = vlan_details.get('state', 'Unknown')

        # Capitalize VLAN state
        vlan_state = vlan_state.upper()

        # Replace 'unsupport' with 'SUSPENDED'
        if vlan_state == 'UNSUPPORT':
            vlan_state = 'SUSPENDED'

        # Get VRF associated with VLAN
        vrf_name = next((vrf_name for vrf_name, vrf_info in vrf_output.get('vrf', {}).items() if 'interfaces' in vrf_info and f'Vlan{vlan_id}' in vrf_info['interfaces']), 'default')

        # Append data to the VLAN info dictionary
        vlan_info['vlan_id'].append(vlan_id)
        vlan_info['vlan_name'].append(vlan_name)
        vlan_info['vlan_state'].append(vlan_state)
        vlan_info['vrf'].append(vrf_name if vrf_name != 'default' else 'default')

    return vlan_info

def show_tech_support_platform_l2(device, file_name, vlan_id, interface=None, po=None):
    """
    Redirect the VLAN, interface, or port-channel-specific information from the command output to a file in bootflash of the device.
    Args:
        device (`obj`): Device object
        file_name (`str`): Name of file to save the output in bootflash
        vlan_id (`int`): VLAN IDs from 1-4094
        interface (`str`, Optional): Interface name
        po (`str`, Optional): Layer2 vp interface value
    Returns:
        None
    """
    try:
        if interface:
            command = f"show tech-support platform layer2 vp interface {interface} vlan {vlan_id} | redirect bootflash:{file_name}"
        elif po:
            command = f"show tech-support platform layer2 vp {po} vlan {vlan_id} | redirect bootflash:{file_name}"
        else:
            command = f"show tech-support platform layer2 vlan {vlan_id} | redirect bootflash:{file_name}"
        device.execute(command)
    except SubCommandFailure as e:
        log.error(f"Failed to redirect the output to bootflash: {e}")
