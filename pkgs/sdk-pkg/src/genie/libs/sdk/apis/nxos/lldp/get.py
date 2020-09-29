"""Common get info functions for illdp"""

# Python
import re
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)
def get_lldp_neighbors_info(device):
    """ Get details about lldp neighbors from device
        Args:
            device ('obj'): Device object
        Returns:
            Dict with lldp info
    """
    try:
        return device.parse('show lldp neighbors detail')
    except SchemaEmptyParserError as e:
        return None
