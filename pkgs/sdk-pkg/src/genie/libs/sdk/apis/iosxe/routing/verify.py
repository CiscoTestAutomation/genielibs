"""Common verify functions for routing"""

# Python
import re
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError


# BGP
from genie.libs.sdk.apis.iosxe.bgp.get import (
    get_ip_bgp_summary,
    get_bgp_route_from_neighbors,
    get_bgp_neighbors_advertised_routes,
)

# ROUTING
from genie.libs.sdk.apis.iosxe.routing.get import get_routing_routes
from genie.libs.sdk.apis.iosxe.routing.get import (
    get_routing_repair_path_information,
)

log = logging.getLogger(__name__)


def verify_routing_local_and_connected_route(device, vrf):
    """ Verify there is local and connected route registered for the vrf

        Args:
            device (`obj`): Device object
            vrf (`str`): Vrf name
        Returns:
            (`dict`): Interface dict contain ip route info
            False
        Raises:
            None
     """
    intf_dict = {}

    out = device.execute("show ip route vrf {} connected".format(vrf))
    if not out:
        return False

    p = re.compile(
        r"(?m)^\s*(?P<type>L|C) +(?P<ip>[\d\.]+).*, +(?P<intf>[\w\.\/]+)"
    )
    route_list = p.findall(out)

    for route in route_list:
        intf_dict.setdefault(route[2], {}).update({route[0]: route[1]})

    for intf, route_data in intf_dict.items():
        if len(route_data) < 2:
            return False

    return intf_dict


def verify_routing_route_ip_on_interface(device, interface_dict):
    """ Verify routes match the configured IP address in running config

        Args:
            device (`obj`): Device object
            interface_dict (`dict`): Interface dict contain ip route info. Get from libs/routing/verify.py::verify_routing_local_and_connected_route
        Returns:
            True / False
        Raises:
            None
    """
    for intf, data in interface_dict.items():
        log.info("Verify configured route ip on {}".format(intf))

        ip = data["L"]
        out = device.execute("show running-config interface {}".format(intf))

        if ip in out:
            log.info(
                "Matched route ip {ip} on {intf}".format(ip=ip, intf=intf)
            )
            return True
        else:
            return False


def verify_routing_ip_routes(
    device,
    route,
    interface=None,
    destination_address=None,
    output=None,
    repeat=0,
):
    """ Verify ip route exists

        Args:
            device ('str'): Device str
            route ('str'): ip address to verify
            interface ('str'): interface name to verify
            destination_address ('str'): detsination ip address to verify
            output ('str'): output provided as argument
            repeat ('int'): repeat value
        Returns:
            True / False
        Raises:
            None
    """
    if not output:
        output = device.execute("show running-config | include ip route")
    route_format = route
    if repeat > 0:
        for i in range(repeat):
            route = route.format(x=str(i + 1))
            result = verify_routing_ip_routes(
                device=device,
                route=route,
                interface=interface,
                destination_address=destination_address,
                output=output,
                repeat=0,
            )
            if not result:
                return False
            route = route_format
        return True
    else:
        m = None

        if interface and destination_address:
            p1 = re.compile(
                r"ip +route +{route} +[\d\.]+ +"
                "{interface} +{destination_address}".format(
                    route=route,
                    interface=interface,
                    destination_address=destination_address,
                )
            )
        elif interface:
            p1 = re.compile(
                r"ip +route +{route} +[\d\.]+ +{interface}".format(
                    route=route, interface=interface
                )
            )
        elif destination_address:
            p1 = re.compile(
                r"ip +route +{route} +[\d\.]+ +{destination_address}".format(
                    route=route, destination_address=destination_address
                )
            )

        m = p1.search(output)

        if m:
            return True
        else:
            return False


def verify_routing_static_routes(
    device,
    route,
    interface=None,
    destination_address=None,
    output=None,
    repeat=0,
):
    """ Verify static route exists

        Args:
            device ('str'): Device str
            route ('str'): ip address to verify
            interface ('str'): interface name to verify
            destination_address ('str'): detsination ip address to verify
            output ('str'): output from 'show ip route static'
            repeat ('int'): repeat value
        Returns:
            True / False
        Raises:
            None
    """
    route_format = route
    if not output:
        output = device.execute("show ip route static")

    if repeat > 0:
        for i in range(repeat):
            route = route.format(x=str(i + 1))
            result = verify_routing_static_routes(
                device=device,
                route=route,
                interface=interface,
                destination_address=destination_address,
                output=output,
                repeat=0,
            )
            if not result:
                return False
            route = route_format
        return True
    else:
        m = None
        if interface and destination_address:
            p1 = re.compile(
                r"{route}(\/\d+)? +\[\d+\/\d+\] +via +{destination_address}"
                ", +{interface}".format(
                    route=route,
                    destination_address=destination_address,
                    interface=interface,
                )
            )
        elif interface:
            p1 = re.compile(
                r"{route}(\/\d+)? +is +directly +connected, +{interface}".format(
                    route=route, interface=interface
                )
            )
        elif destination_address:
            p1 = re.compile(
                r"{route}(\/\d+)? +\[\d+\/\d+\] +via +{destination_address}".format(
                    route=route, destination_address=destination_address
                )
            )

        m = p1.search(output)
        if m:
            return True
        else:
            return False


def verify_routing_ip_bgp_neighbors_routes_exists(
    device,
    address_family,
    neighbor,
    vrf,
    initial_route,
    rd=None,
    max_time=60,
    check_interval=10,
    expected_result=True,
    output=None,
):
    """ Verify if the initial_route provided exists

        Args:
            device ('obj'): Device object
            address_family ('str'): address family
            rd ('str'): rd export value
            neighbor ('str'): neighbor address to find routes
            vrf ('str'): vrf name
            initial_route ('str'): intial route to search
            max_time ('int') : max time for Timeout
            check_interval ('int'): interval for Timeout
            expected_result ('bool'): expected result to check
        Returns:
            True / False
        Raises:
            None
    """
    timeout = Timeout(max_time=max_time, interval=check_interval)
    while timeout.iterate():
        route_exists = False
        if not output:
            out = get_bgp_route_from_neighbors(
                device=device,
                address_family=address_family,
                rd=rd,
                neighbor_address=neighbor,
                vrf=vrf,
            )
        else:
            out = output
            output = None
        if not out:
            return None

        routes = out.keys()
        for route in routes:
            if initial_route in route:
                route_exists = True

        if route_exists == expected_result:
            return route_exists

        timeout.sleep()
    return route_exists


def verify_routing_neighbors_advertised_routes_exists(
    device,
    address_family,
    neighbor,
    vrf,
    initial_route,
    rd=None,
    max_time=60,
    check_interval=10,
    output=None,
):
    """ Verify if neighbors advertised routes exists

        Args:
            device ('obj'): Device object
            address_family ('str'): address family
            rd ('str'): rd export value
            neighbor ('str'): neighbor address to find routes
            vrf ('str'): vrf name
            initial_route ('str'): intial route to search
            max_time ('int') : max time for Timeout
            check_interval ('int'): interval for Timeout
            output ('list'): list of neighbors advertised routes (get_bgp_neighbors_advertised_routes)
        Returns:
            True
            False
    """
    result = False
    timeout = Timeout(max_time=max_time, interval=check_interval)
    while timeout.iterate():
        if not output:
            advertised_routes = list(
                get_bgp_neighbors_advertised_routes(
                    device=device,
                    address_family=address_family,
                    neighbor_address=neighbor,
                    rd=rd,
                    vrf=vrf,
                )
            )
            if not advertised_routes:
                return False
        else:
            advertised_routes = output

        if advertised_routes:
            for route in advertised_routes:
                if route == initial_route:
                    result = True

            return result
        else:
            timeout.sleep()

    return result


def is_routing_route_targets_present(
    device, vrf, routes, address_family, ignore_routes=None
):
    """ Verify route target is present

        Args:
            device ('obj'): Device object
            vrf ('str'): VRF name
            address_family ('str'): address family to check
            routes ('list'): list of routes to compare
                ex.) routes = ['192.168.1.1', '192.168.1.2']
            ignore_routes ('list'): list of routes to ignore with type
                ex.) ignore_routes = ['L', 'B', 'C']
        Returns:
            True
            False
        Raises:
            None
    """
    if not routes:
        return False

    result = True
    routes_received = get_routing_routes(device, vrf, address_family)

    for route in routes_received.keys():
        try:
            source_protocol_codes = routes_received[route][
                "source_protocol_codes"
            ]
            if ignore_routes and source_protocol_codes in ignore_routes:
                continue
            if route not in routes:
                result = False
        except KeyError as e:
            log.error("Key issue with exception {}".format(str(e)))
            result = False

    return result


def is_routing_repair_path_in_route_database(
    device, route, max_time=60, check_interval=10
):
    """ Verify if 'repair path' is present in route database

        Args:
            device ('obj'): Device object
            route ('str'): Route address
            max_time ('int'): Max time in seconds checking output
            check_interval ('int'): Interval in seconds of each checking 
        Return:
            True/False
        Raises:
            None
    """

    log.info("Getting 'repair path' information")

    timeout = Timeout(max_time=max_time, interval=check_interval)
    while timeout.iterate():
        next_hop, outgoing_interface = get_routing_repair_path_information(
            device=device, route=route
        )
        if next_hop and outgoing_interface:
            return True

        timeout.sleep()

    log.info("Could not find any information about repair path")
    return False
