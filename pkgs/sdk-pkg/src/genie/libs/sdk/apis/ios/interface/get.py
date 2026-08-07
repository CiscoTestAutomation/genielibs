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
    empty_ints = [] 

    for interface in interface_list:
        try:
            data = device.parse('show interfaces ' + interface)
        except SchemaEmptyParserError:
            empty_ints.append(interface)
            data = None
        results[interface] = data
    if empty_ints:
        log.error('No interface information found for {}'.format(empty_ints))
    
    return results

def get_interface_ipv4_address(device, interface):
    """Get the ip address for an interface on target device

        Args:
            interface ('string'): interface to get address for
            device: ('obj'): Device Object
        Returns:
            None
            String with interface ip address
    """

    try:
        data = device.parse('show interfaces ' + interface)
    except SchemaEmptyParserError as e:
        log.error('No interface information found for {}: {}'.format(interface, e))
        return None
    ip_dict = data[interface].get('ipv4')
    ip = None
    if ip_dict:
        ip = list(ip_dict)[0]
    return ip


def get_interface_ip_address(device, interface, address_family=None):
    """ Get interface ip_address from device

        Args:
            device ('obj'): Device object
            interface ('str'): Interface to get address
            address_family ('str'): Used only for junos api

        Returns:
            None
            interface ip_address ('str')

        Raises:
            None
    """
    log.debug(
        "Getting interface address for %s on %s",
        interface, device.name,
    )
    cmd = "show ip interface brief {i}".format(i=interface)
    try:
        out = device.parse(cmd)
    except SubCommandFailure:
        log.debug("Invalid command")
        return
    except Exception as e:
        log.debug("Failed to parse '%s': %s", cmd, e)
        return

    if interface not in out.get("interface", {}):
        return
    intf_data = out["interface"][interface]
    address = intf_data.get("ip_address")
    if not address or address == "unassigned":
        return
    return address