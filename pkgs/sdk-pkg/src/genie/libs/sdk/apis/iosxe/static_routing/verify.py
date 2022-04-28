"""Common verify functions for static routing"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


# Note: Keep this API in line with verify_routing_route_attrs() if extending.
def verify_static_routing_route_attrs(device, route, address_family='ipv4',
                                      vrf_name=None, route_attrs=None,
                                      next_hop_info=None, max_time=60,
                                      check_interval=10):
    """Verify default IPv4 static route exists with given properties.

    Args:
        device (obj): Device to verify route on.
        route (str): route to verify.
        address_family (str, optional): address family of route ("ipv4" or "ipv6"). Defaults to "ipv4".
        vrf_name (str, optional): vrf name to verify route on. Defaults to None.
        route_attrs (obj, optional): If specified, verify the specified attributes in the route. Defaults to None.
        next_hop_info (obj, optional): If specified, next hop info to confirm a matching entry in the route. Defaults to None.
            next_hop_info is of format:
                {
                    "active": True,
                    "next_hop": "192.168.1.1",
                    "outgoing_interface": "GigabitEthernet1",
                    "preference": 3,
                    "owner_code": "M",
                }
            where all keys are optional; ony the keys specified will be
            checked. If no keys are given, then no keys are checked and this
            will be considered a match.
        max_time (int, optional): Maximum timeout (seconds). Defaults to 60.
        check_interval (int, optional): Check interval (seconds). Defaults to 10.

    Returns:
        bool: True if static route is verified, False otherwise.
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        routes = None
        if address_family == 'ipv4':
            routes = device.api.get_static_routing_routes(vrf=vrf_name,
                                                          address_family='ipv4')
        elif address_family == 'ipv6':
            routes = device.api.get_static_routing_ipv6_routes(vrf=vrf_name)

        if routes and route in routes:
            match = True
            if route_attrs != None:
                for k, v in route_attrs.items():
                    if k not in routes[route] or v != routes[route][k]:
                        log.info(f"Route attr key {k}, value {v} does not match. Route: {routes[route]}")
                        match = False
                        break
            if next_hop_info != None:
                def check_next_hop_info_match():
                    for nh_type in ['outgoing_interface', 'next_hop_list']:
                        if nh_type in routes[route]['next_hop']:
                            for _, nh in routes[route]['next_hop'][nh_type].items():
                                nh_match = True
                                for k, v in next_hop_info.items():
                                    if k not in nh or v != nh[k]:
                                        log.info(f"No match found in next hop for key {k}, value {v}. Next hop: {nh}")
                                        nh_match = False
                                        break
                                if nh_match:
                                    return True
                    return False
                match = match and check_next_hop_info_match()
            if match:
                return True
        timeout.sleep()
    log.info(f"Could not verify route {route}")
    return False
