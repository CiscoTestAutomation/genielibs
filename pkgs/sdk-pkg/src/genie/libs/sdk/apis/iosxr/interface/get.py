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
