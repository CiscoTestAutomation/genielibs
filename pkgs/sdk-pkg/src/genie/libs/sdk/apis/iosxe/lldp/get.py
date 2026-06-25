"""Common get info functions for illdp"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.metaparser.util.exceptions import InvalidCommandError

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
        log.debug(f"Could not get device show lldp neighbors detail: {e}")
        return None


def get_lldp_info(device):
    """ Get lldp config from device
        Args:
            device ('obj'): Device object
        Returns:
            Dict with lldp info
    """
    try:
        return device.parse('show lldp')
    except SchemaEmptyParserError as e:
        log.debug(f"Could not get device show lldp: {e}")
        return None


def get_lldp_interface_info(device, interface):
    """ Get lldp interface config from device
        Args:
            device ('obj'): Device object
            interface (str): Interface name
        Returns:
            Dict with lldp info
    """
    try:
        return device.parse(f'show lldp interface {interface}')
    except (SchemaEmptyParserError, InvalidCommandError) as e:
        log.debug(f"Could not get device show lldp interface {interface} "
                  f"detail: {e}")
        return None


def get_lldp_interface_list(device):
    """ Get lldp interfaces from device
        Args:
            device ('obj'): Device object
        Returns:
            List of lldp interfaces
    """
    res_list = []
    try:
        output = device.parse('show lldp interface')
    except (SchemaEmptyParserError, InvalidCommandError) as e:
        log.debug(f"Could not get device show lldp interface"
                  f"detail: {e}")
        return res_list
    if output and output.get('interfaces'):
        for intf in output.get('interfaces'):
            res_list.append(intf)
    return res_list


def get_lldp_neighbors_brief_info(device):
    """ Get brief about lldp neighbors from device
        Args:
            device ('obj'): Device object
        Returns:
            Dict with lldp neighbors info
    """
    try:
        return device.parse('show lldp neighbors')
    except SchemaEmptyParserError as e:
        log.debug(f"Could not get device show lldp neighbors: {e}")
        return None


def get_lldp_neighbors_interface_info(device, interface):
    """ Get detail about lldp neighbors intf from device
        Args:
            device ('obj'): Device object
            interface (str): Interface name
        Returns:
            Dict with lldp neighbors info
    """
    try:
        return device.parse(f'show lldp neighbors {interface} detail')
    except (SchemaEmptyParserError, InvalidCommandError) as e:
        log.debug(f"Could not get device show lldp neighbors {interface} "
                  f"detail: {e}")
        return None


def get_lldp_entry_info(device, neighbor_id):
    """ Get detail about lldp neighbors intf from device
        Args:
            device ('obj'): Device object
            neighbor_id (str): The id of neighbor, * stand for any
        Returns:
            Dict with lldp entry info
    """
    try:
        return device.parse(f'show lldp entry {neighbor_id}')
    except SchemaEmptyParserError as e:
        log.debug(f"Could not get device show lldp entry {neighbor_id} detail:"
                  f"{e}")
        return None


def get_total_lldp_entries_displayed(device):
    """Get the Total lldp entries displayed of the device

    Args:
        device (obj): Device object

    Return:
        int: Device Total lldp entries displayed
    """
    try:
        out = device.parse('show lldp neighbors')
    except SchemaEmptyParserError as e:
        log.debug(f"Could not get device show lldp neighbors: {e}")
        return None
    return out.get('total_entries')


def get_lldp_traffic_info(device):
    """ Get lldp traffic info from device
        Args:
            device ('obj'): Device object
        Returns:
            Dict with lldp traffic info
    """
    try:
        return device.parse('show lldp traffic')
    except SchemaEmptyParserError as e:
        log.debug(f"Could not get device show lldp traffic: {e}")
        return None


def get_lldp_error_info(device):
    """ Get lldp error info from device
        Args:
            device ('obj'): Device object
        Returns:
            Dict with lldp error info
    """
    try:
        return device.parse('show lldp errors')
    except SchemaEmptyParserError as e:
        log.debug(f"Could not get device show lldp errors: {e}")
        return None
