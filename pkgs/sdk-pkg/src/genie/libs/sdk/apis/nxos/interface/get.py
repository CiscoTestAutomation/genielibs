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
    """ Get interface information from device for a  interfaces

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
            data = device.parse('show interface ' + interface)
        except SchemaEmptyParserError:
            empty_ints.append(interface)
            data = None
        results[interface] = data
    if empty_ints:
        log.error('No interface information found for {}'.format(empty_ints))
    return results

def get_interface_ipv4_address(device, interface):
    """ Get the ip address for an interface on target device

        Args:
            interface ('string'): interface to get address for
            device: ('obj'): Device Object
        Returns:
            None
            String with interface ip address
    """
    try:
        data = device.parse('show interface ' + interface)
    except SchemaEmptyParserError as e:
        log.error('No interface information found for {}: {}'.format(interface, e))
        return None
    ip_dict = data[interface].get('ipv4')
    ip = None
    if ip_dict:
        ip = list(ip_dict)[0]
    return ip
    

def get_interface_names(device):
    """Gets the names of all interfaces on the device

    Args:
        device (obj): Device object

    Returns:
        list: List of interface names
    """

    try:
        out = device.parse('show interface brief').get('interface', {})
    except Exception:
        try:
            out = device.parse('show interfaces')
        except SchemaEmptyParserError as e:
            log.error('No interface information found')
            return None

    ret_list = list()
    for interfaces in list(out.values()):
        ret_list += [intf for intf in list(interfaces.keys())]

    return ret_list