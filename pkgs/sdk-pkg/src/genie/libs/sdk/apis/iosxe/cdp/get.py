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

def get_total_cdp_entries_displayed(device):
    """Get the Total cdp entries displayed of the device

    Args:
        device (obj): Device object

    Return:
        int: Device Total cdp entries displayed
    """
    try:
        out = device.parse('show cdp neighbors detail')
    except SchemaEmptyParserError as e:
        log.error("Could not get device show cdp neighbors detail: {e}".format(e=e))
        return None
    return out.q.get_values('total_entries_displayed', 0)