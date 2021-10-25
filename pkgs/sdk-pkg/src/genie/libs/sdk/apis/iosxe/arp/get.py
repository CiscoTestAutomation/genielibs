"""Common get info functions for routing"""

# Python
import os
import logging
import re

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_arp_table_count(device):
    """
    Get arp table count

    Args:
        device(`obj`): Device str
    Returns:
        arp table count
    """
    try:
        output_arp = device.parse("show arp summary")
    except SchemaEmptyParserError as e:
        log.error(
            "Failed to parse 'show arp summary', Error: {}".format(str(e))
        )
        return None

    arp_count = output_arp["total_num_of_entries"].get("arp_table_entries", 0)

    return arp_count


def get_arp_interface_mac_from_ip(device, ip_address, vrf=None):
    """
    Get the outgoing interface along with mac address of particular
    host in 'show arp vrf <vrf> <ip>' / 'show arp <ip>'  arp table

    Args:
        device(`obj`): Device str
        ip_address ('str'): ip
        vrf ('str', optional): vrf interface, default None
    Returns:
        interface and mac (tuple)
        None
    """
    if vrf:
        command = "show arp vrf {vrf} {ip}".format(
            vrf=vrf, ip=ip_address)
    else:
        command = "show arp {ip}".format(ip=ip_address)

    try:
        output = device.parse(command)
    except SchemaEmptyParserError:
        log.error("Command has not returned any results")
        return None

    intf_mac_tuple = tuple()
    found = False
    for intf in output.get("interfaces", {}):
        for neighbor in output['interfaces'][intf]['ipv4'].get("neighbors", {}):
            if neighbor == ip_address:
                found = True
                mac = output['interfaces'][intf]['ipv4']['neighbors']\
                      [neighbor].get('link_layer_address', "")
                intf_mac_tuple=(intf, mac)

    if not found:
        return None

    return intf_mac_tuple
