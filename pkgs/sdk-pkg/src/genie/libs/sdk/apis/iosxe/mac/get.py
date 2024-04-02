"""Common get info functions for mac"""

# Python
import logging
import re 

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def get_mac_aging_timer(device, bridge_domain):
    """ Get Aging-Timer from bridge domain

        Args:
            device (`obj`): device object
            bridge_domain (`int`): bridge domain id
        Return:
            aging_time (`int`): aging-time in second
            None 
        Raises:
            None
    """
    try:
        out = device.parse("show bridge-domain {}".format(bridge_domain))
    except SchemaEmptyParserError as e:
        return None

    aging_time = out["bridge_domain"][bridge_domain]["aging_timer"]

    return aging_time


def get_mac_table(device, bridge_domain):
    """ Get mac table from bridge domain

        Args:
            device (`obj`): device object
            bridge_domain (`int`): bridge domain id
        Return:
            mac_table (`dict`): mac table dict
            {}: When nothing has been found
        Raises:
            None
    """
    try:
        out = device.parse("show bridge-domain {}".format(bridge_domain))
    except SchemaEmptyParserError as e:
        return {}

    mac_table = out["bridge_domain"][bridge_domain].get("mac_table")

    return mac_table


def get_mac_table_from_address_family(device, address_family):
    """ Gets mac table from address_family

        Args:
            device (`obj`): device object
            address_family ('str'): address_family
        Return:
            mac_table (`dict`): mac table dict
            {}: When nothing has been found
        Raises:
            None
    """
    try:
        mac_output = device.parse("show {} mac".format(address_family))
    except SchemaEmptyParserError as e:
        return {}

    mac_table = dict()
    for evi in mac_output['evi']:
        mac_table[evi] = []
        for bdid in mac_output['evi'][evi]['bd_id']:
            for eth_tag in mac_output['evi'][evi]['bd_id'][bdid]['eth_tag']:
                for mac in mac_output['evi'][evi]['bd_id'][bdid]['eth_tag'][eth_tag]['mac_addr']:
                    # Adding list of mac addresses to corresponding evi's
                    mac_table[evi].append(mac)

    return mac_table

def get_mac_table_entries(device):
    """
    Generate MAC table entries with VLAN, MAC address, interfaces, and associated VRFs.

    Args:
        device (obj): Device object

    Returns:
        dict: Dictionary containing MAC table entries in the desired format
    """
    try:
        # Execute 'show mac address_table' command
        mac_table_output = device.parse("show mac address-table")

        # Execute 'show vrf' command
        vrf_output = device.parse("show vrf")
        
    except SchemaEmptyParserError as e:
        # Log errors and return an empty dictionary if the parser returns empty results
        log.error(f"Failed to retrieve MAC table entries: {e}")
        return {}
        
    # Initialize dictionary to store MAC table entries
    mac_entries = {'vrf': [], 'vlan': [], 'mac_address': [], 'interfaces': []}
    
    # Iterate over VLANs and MAC addresses
    for vlan_id, vlan_info in mac_table_output['mac_table']['vlans'].items():
        if vlan_id != 'all':
            for mac_address, mac_details in vlan_info['mac_addresses'].items():
                # Get interfaces associated with MAC address
                interfaces = 'Unknown'
                if isinstance(mac_details['interfaces'], dict):
                    interfaces = next(iter(mac_details['interfaces'].keys()))
                else:
                    interfaces = ', '.join(interface['interface'] for interface in mac_details['interfaces'].values() if isinstance(interface, dict))
                
                # Get VRF associated with VLAN
                vrf_name = next((vrf_name for vrf_name, vrf_info in vrf_output['vrf'].items() if 'interfaces' in vrf_info and f'Vlan{vlan_id}' in vrf_info['interfaces']), 'default')
                
                # Append data to the MAC entries dictionary
                mac_entries['vrf'].append(vrf_name if vrf_name != 'default' else 'default')
                mac_entries['vlan'].append(vlan_id)
                mac_address_cleaned = mac_address.replace('.', '')
                mac_entries['mac_address'].append(':'.join([mac_address_cleaned[i:i+2] for i in range(0, len(mac_address_cleaned), 2)]))
                mac_entries['interfaces'].append(interfaces)

    return mac_entries
