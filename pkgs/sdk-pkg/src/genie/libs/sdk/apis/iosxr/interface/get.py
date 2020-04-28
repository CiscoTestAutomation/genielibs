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
    for interface in interface_list:
        try:
            data = device.parse('show interfaces ' + interface)
        except Exception as e:
            log.error('Failed to parse command due to: {}'.format(e))
            data = None
        results[interface] = data
    return results    