"""Common get info functions for static routing"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_static_routing_routes(device, vrf, address_family):
    """Execute 'show ip static route vrf <vrf>' and retrieve the routes

        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name or None
            address_family (`str`): Address family name

        Returns:
            Dictionary: received routes

        Raises:
            None

    """
    # only accept ipv4 address family
    address_family = address_family.split()[0]
    try:
        if vrf:
            command = "show ip static route vrf {}".format(vrf)
        else:
            command = "show ip static route"
        out = device.parse(command)
        if not vrf:
            vrf = "default"
        routes_received = out["vrf"][vrf]["address_family"][address_family][
            "routes"]
    except SchemaEmptyParserError:
        log.error(
            "Parser did not return any routes for vrf {vrf}".format(vrf=vrf))
        return None
    except KeyError as e:
        log.error("Key issue with exception : {}".format(str(e)))
        return None

    return routes_received


def get_static_routing_ipv6_routes(device, vrf):
    """Execute 'show ipv6 static vrf <vrf>' and retrieve the routes

        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name or None

        Returns:
            Dictionary: received routes

        Raises:
            None

    """
    try:
        if vrf:
            command = "show ipv6 static vrf {} detail".format(vrf)
        else:
            command = "show ipv6 static detail"
        out = device.parse(command)
        if not vrf:
            vrf = "default"
        routes_received = out["vrf"][vrf]["address_family"]['ipv6']["routes"]
    except SchemaEmptyParserError:
        log.error(
            "Parser did not return any routes for vrf {vrf}".format(vrf=vrf))
        return None
    except KeyError as e:
        log.error("Key issue with exception : {}".format(str(e)))
        return None

    return routes_received
