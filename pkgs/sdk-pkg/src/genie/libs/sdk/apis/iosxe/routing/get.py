"""Common get info functions for routing"""

# Python
import os
import logging
import re

# pyATS
from ats.easypy import runtime

# Genie
from genie.utils.config import Config
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_routing_outgoing_interface(
    device, ip_address, vrf=None, address_family=None
):
    """ Execute 'show ip cef <address>' and retrieve the outgoing interface

        Args:
            device (`obj`): Device object
            ip_address ('str'): ip_address
            vrf ('str'): vrf to search under
            address_family ('str'): address_family to search under

        Returns:
            ('list'): [interface name, ip_address]

        Raises:
            SchemaEmptyParserError

    """

    log.info("Get the outgoing interface ('show ip cef <ip>')")

    outgoing_interface = None
    new_ip = None

    try:
        out = device.parse("show ip cef {ip}".format(ip=ip_address))
    except SchemaEmptyParserError:
        return []

    vrf = vrf if vrf else "default"
    address_family = address_family if address_family else "ipv4"

    for prefix, p_data in out["vrf"][vrf]["address_family"][address_family][
        "prefix"
    ].items():
        for next_hop, nh_data in p_data.get("nexthop", {}).items():
            for key in nh_data.get("outgoing_interface", {}):
                outgoing_interface = key
                new_ip = next_hop
                break
        else:
            continue

    return [outgoing_interface, new_ip]


def get_routing_route_count(device, vrf=None):
    """ Get route count for all vrfs

        Args:
            device(`str`): Device str
            vrf ('str'): VRF name

        Returns:
            int: route count

        Raises:
            SchemaEmptyParserError
    """

    commands = ["show ip route vrf {} summary", "show ip route summary"]

    if vrf:
        cmd = commands[0].format(vrf)
    else:
        cmd = commands[1]

    try:
        output = device.parse(cmd)
    except SchemaEmptyParserError:
        raise SchemaEmptyParserError(
            "Command '{}' has " "not returned any results".format(cmd)
        )
    if not vrf:
        vrf = "default"

    return output["vrf"][vrf]["total_route_source"]["networks"]


def get_routing_route_count_all_vrf(device):
    """ Get route count for every VRF

        Args:
            device ('obj'): Device object

        Returns:
            Integer: Route count

        Raises:
            SchemaEmptyParserError
    """
    log.info("Getting route count for all vrf")
    try:
        out = device.parse("show vrf")
    except SchemaEmptyParserError as e:
        raise SchemaEmptyParserError("Could not find any VRF")

    route_count = 0

    # Gets route count when VRF is 'default'
    try:
        route_count += get_routing_route_count(device=device)
    except SchemaEmptyParserError as e:
        pass

    for vrf in out["vrf"]:
        try:
            route_count += get_routing_route_count(device=device, vrf=vrf)
        except SchemaEmptyParserError as e:
            pass

    log.info("Route count for all vrf is {}".format(route_count))
    return route_count


def get_routing_routes(device, vrf, address_family):
    """Execute 'show ip route vrf <vrf>' and retrieve the routes

        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name
            address_family (`str`): Address family name

        Returns:
            Dictionary: received routes

        Raises:
            SchemaEmptyParserError
            KeyError

    """
    try:
        out = device.parse("show ip route vrf {}".format(vrf))
    except SchemaEmptyParserError:
        raise SchemaEmptyParserError(
            "Parser did not return any routes for " "vrf {vrf}".format(vrf=vrf)
        )
    try:
        routes_received = out["vrf"][vrf]["address_family"][address_family][
            "routes"
        ]
    except KeyError as e:
        raise KeyError("Key issue with exception : {}".format(str(e)))

    return routes_received
