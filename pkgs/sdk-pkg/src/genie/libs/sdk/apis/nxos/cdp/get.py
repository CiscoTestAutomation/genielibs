"""Common get info functions for cdp"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)
def get_cdp_neighbors_info(device):
    """ Get details about cdp neighbors from device
        Args:
            device ('obj'): Device object
        Returns:
            Dict with cdp info
    """
    try:
        return device.parse('show cdp neighbors detail')
    except SchemaEmptyParserError as e:
        return None