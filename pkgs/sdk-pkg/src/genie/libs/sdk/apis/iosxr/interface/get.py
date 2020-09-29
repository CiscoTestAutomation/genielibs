"""Common get info functions for interface"""

# Python
import re
import logging

# unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_interface_ip_address(device, interface):
    """ Get interface ip_address from device

        Args:
            interface('str'): Interface to get address
            device ('obj'): Device object

        Returns:
            None
            interface ip_address ('str')

        Raises:
            None
    """
    log.info("Getting interface address for {interface} on {device}"
        .format(interface=interface, device=device.name))

    cmd = "show ip interface brief"
    try:
        out = device.parse(cmd)
    except SubCommandFailure:
        log.error("Invalid command")
    except Exception as e:
        log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
        return

    address = out["interface"].get(interface, {}).get("ip_address", None)
    if interface not in out["interface"]:
        return
    elif (address == "unassigned" or 
        "ip_address" not in out["interface"][interface]):
        return

    return address

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