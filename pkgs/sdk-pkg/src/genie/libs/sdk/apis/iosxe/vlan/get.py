"""Common get info functions for vlan"""

# Python
import re
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

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