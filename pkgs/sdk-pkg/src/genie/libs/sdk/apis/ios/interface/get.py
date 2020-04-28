"""Common get info functions for interfaces"""

# Python
import re
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Unicon
from unicon.core.errors import SubCommandFailure



log = logging.getLogger(__name__)

def get_interface_information(device, interface_list):
    """Get interface information from device for a list of interfaces

        Args:
            List['string']: Interfaces to query information on
            device ('obj'): Device object
        Returns:
            List containing Dictionaries for sucesses
    """
    results = {}        
    for interface in interface_list:
        try:
            data = device.parse('show interfaces ' + interface)
        except Exception as e:
            log.error('Failed to parse command due to: {}'.format(e))
            data = None
        results[interface] = data
    return results