"""Common get info functions for cdp"""

# Python
import re
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


def get_cdp_neighbour_port_id(device, interface):
    """ Get the port_id from 'show cdp neighbors <interface>' for a single interface

    Args:
        device (`obj`): Device object
        interface (str): Interface name

    Returns:
        list: List of port_id values

    Raises:
        SchemaEmptyParserError: If the 'show cdp neighbors <interface>' output is empty
        KeyError: If the expected keys are not present in the output structure
    """
    try:
        cdp_output = device.parse(f"show cdp neighbors {interface}")
    except Exception as e:
        log.error(f"Could not get device show cdp neighbors detail: {e}")
        return None

    try:
        cdp_entries = cdp_output['cdp']['index']
        port_ids = [entry['port_id'] for entry in cdp_entries.values()]
        return port_ids
    except Exception as e:
        log.error(f"Could not get device show cdp neighbors detail: {e}")
        return None
