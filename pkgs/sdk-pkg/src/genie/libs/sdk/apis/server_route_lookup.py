"""
server_route_lookup.py

Utility to find which server interface IP to use when connecting to a device,
based on management static routes and longest-prefix match.

Expects a pyATS testbed servers AttrDict (testbed.servers):
  - Routes read from server.management.routes.ipv4 and .ipv6
  - Interface IP resolved from server.interfaces dict (matched by key)
  - Interface ipv4/ipv6 may be an IP interface object or a plain string

Route selection uses longest-prefix match across both address families:
the most specific (highest prefix length) matching subnet wins.

Example usage (device.api — recommended, device is injected automatically):
    server_ip = device.api.find_server_ip_for_device_ip(
        '11.43.5.10', testbed.servers
    )
    if server_ip:
        print(f"Use {server_ip}")

Direct-call example (must pass device explicitly as first arg):
    from genie.libs.sdk.apis.server_route_lookup import find_server_ip_for_device_ip
    server_ip = find_server_ip_for_device_ip(
        device, '11.43.5.10', testbed.servers
    )

IPv6 example:
    server_ip = device.api.find_server_ip_for_device_ip(
        '2001:db8::1', testbed.servers
    )
"""

import ipaddress
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def _longest_prefix_match(device_ip: str, routes: list) -> Optional[dict]:
    """Return the most specific route whose subnet contains *device_ip*.

    Args:
        device_ip: IP address string (e.g. '11.43.5.10' or '2001:db8::1')
        routes:    List of route dicts, each with at least a 'subnet' key
                   (e.g. [{'subnet': '11.43.0.0/16', 'interface': 'eth0'}])

    Returns:
        The matching route dict with the longest prefix length, or None.
    """
    try:
        addr = ipaddress.ip_address(device_ip)
    except ValueError:
        raise ValueError(f"Invalid IP address: {device_ip!r}")

    best_route: Optional[dict] = None
    best_prefixlen: int = -1

    for route in routes:
        subnet = route.get('subnet')
        if not subnet:
            continue
        try:
            network = ipaddress.ip_network(subnet, strict=False)
        except ValueError:
            logger.error("Invalid subnet %r in route %r", subnet, route)
            continue
        if network.version != addr.version:
            continue
        if addr in network and network.prefixlen > best_prefixlen:
            logger.debug("  Route %s (prefix_len=%d) covers %s",
                         subnet, network.prefixlen, device_ip)
            best_route = route
            best_prefixlen = network.prefixlen

    if best_route:
        logger.debug("  Best matching route: %s (prefix_len=%d)",
                     best_route.get('subnet'), best_prefixlen)
    else:
        logger.debug("  No route covers %s", device_ip)

    return best_route


def _nested_get(obj, *keys):
    """Traverse nested dicts/AttrDicts by keys, return None if missing."""
    for k in keys:
        if obj is None:
            return None
        if hasattr(obj, 'get'):
            obj = obj.get(k)
        else:
            obj = getattr(obj, k, None)
    return obj


def _get_routes_testbed(server) -> list:
    """Extract all management routes (ipv4 + ipv6) from a testbed server."""
    routes = []
    mgmt_routes = _nested_get(server, 'management', 'routes')
    if mgmt_routes is None:
        logger.debug("  No management.routes found on server")
        return routes
    ipv4 = _nested_get(mgmt_routes, 'ipv4')
    if ipv4:
        routes += ipv4
    ipv6 = _nested_get(mgmt_routes, 'ipv6')
    if ipv6:
        routes += ipv6
    logger.debug("  Found %d route(s) (ipv4=%d, ipv6=%d)",
                 len(routes), len(ipv4 or []), len(ipv6 or []))
    return routes


def _get_interface_ip_testbed(
        server, iface_name: str, family: str = 'ipv4') -> Optional[str]:
    """Resolve an interface IP from a pyATS testbed server AttrDict or dict.

    Args:
        server:     pyATS testbed server AttrDict or plain dict.
        iface_name: interface key to look up.
        family:     'ipv4' or 'ipv6'.
    """
    interfaces = _nested_get(server, 'interfaces')
    if interfaces is None:
        logger.debug("  No interfaces found on server")
        return None
    if hasattr(interfaces, 'get'):
        iface = interfaces.get(iface_name)
    else:
        iface = getattr(interfaces, iface_name, None)
    if iface is None:
        logger.debug("  Interface '%s' not found in server interfaces",
                     iface_name)
        return None

    if hasattr(iface, 'get'):
        addr = iface.get(family)
    else:
        addr = getattr(iface, family, None)
    if addr is None:
        logger.debug("  Interface '%s' has no %s address", iface_name, family)
        return None
    # addr may be a list (ipv6 can be multi-valued per schema)
    if isinstance(addr, list):
        if not addr:
            logger.debug("  Interface '%s' has empty %s address list",
                         iface_name, family)
            return None
        addr = addr[0]
    resolved = str(ipaddress.ip_interface(str(addr)).ip)
    logger.debug("  Resolved interface '%s' %s -> %s",
                 iface_name, family, resolved)
    return resolved


def _find_server_entry_by_hostname(hostname: str, servers) -> Optional[tuple]:
    """Find the server entry whose address matches *hostname*.

    Checks the following fields on each server entry (in order):
      1. ``address`` field
      2. ``server`` field
      3. All interface IPs (ipv4/ipv6)

    Args:
        hostname: IP address or FQDN to match against server entries.
        servers:  pyATS testbed.servers AttrDict.

    Returns:
        ``(name, server_obj)`` for the first matching server, or ``None``.
    """
    for name, srv in servers.items():
        addr = _nested_get(srv, 'address')
        if addr and str(addr) == hostname:
            logger.debug("  Matched server '%s' by address '%s'", name, addr)
            return (name, srv)
        srv_field = _nested_get(srv, 'server')
        if srv_field and str(srv_field) == hostname:
            logger.debug("  Matched server '%s' by server field '%s'",
                         name, srv_field)
            return (name, srv)
        # Check interface IPs
        interfaces = _nested_get(srv, 'interfaces')
        if interfaces:
            items = (interfaces.items() if hasattr(interfaces, 'items')
                     else [])
            for _iname, iface in items:
                for fam in ('ipv4', 'ipv6'):
                    raw = (iface.get(fam) if hasattr(iface, 'get')
                           else getattr(iface, fam, None))
                    if raw is None:
                        continue
                    vals = raw if isinstance(raw, list) else [raw]
                    for v in vals:
                        ip_str = str(ipaddress.ip_interface(str(v)).ip)
                        if ip_str == hostname:
                            logger.debug(
                                "  Matched server '%s' by interface "
                                "'%s' %s=%s", name, _iname, fam, ip_str)
                            return (name, srv)
    return None


def find_server_ip_for_device_ip(
    device,
    device_ip: str,
    servers,
    server_hostname: Optional[str] = None,
) -> Optional[str]:
    """Find the server interface IP that should be used to reach *device_ip*.

    Iterates over servers, performs longest-prefix match against each
    server's management static routes, and returns the interface IP address
    for the best match.

    When *server_hostname* is provided the search is scoped to ONLY the
    server whose address/server-field/interface-IP matches that hostname.
    This prevents switching to a different server (important when the URL
    path contains server-specific resources like short-path symlinks).
    If the identified server has no covering route, ``None`` is returned —
    no fallback to other servers.

    When *server_hostname* is ``None`` (default), all servers are searched
    and the best match across all of them wins.

    Args:
        device:           pyATS device object.
        device_ip:        IP address of the device (str, e.g. '11.43.5.10').
        servers:          pyATS testbed.servers AttrDict.
        server_hostname:  Optional hostname/IP to scope search to a single
                          server.  Must match a server's ``address``,
                          ``server`` field, or one of its interface IPs.

    Returns:
        Server interface IP address (str), or None if no server covers
        *device_ip* with a resolvable interface IP.

    Raises:
        ValueError: if *device_ip* is not a valid IP address.
    """
    # Validate device_ip early so we raise even if servers is empty
    try:
        ipaddress.ip_address(device_ip)
    except ValueError:
        raise ValueError(f"Invalid IP address: {device_ip!r}")

    # Scope to a single server when server_hostname is provided
    if server_hostname:
        entry = _find_server_entry_by_hostname(server_hostname, servers)
        if entry is None:
            logger.info(
                "Find server IP for device IP: server_hostname='%s' not "
                "found in %d server(s) — returning None",
                server_hostname, len(servers))
            return None
        server_name, server_obj = entry
        candidates = {server_name: server_obj}
        logger.info(
            "Find server IP for device IP: scoped to server '%s' "
            "(hostname='%s') for device IP %s",
            server_name, server_hostname, device_ip)
    else:
        candidates = servers
        logger.info(
            "Find server IP for device IP: searching %d server(s) for "
            "route covering device IP %s", len(servers), device_ip)

    best_server_ip: Optional[str] = None
    best_prefixlen: int = -1
    best_server_name: Optional[str] = None

    for name, server in candidates.items():
        logger.debug("Checking server '%s'", name)
        routes = _get_routes_testbed(server)
        if not routes:
            logger.debug("  Skipping '%s' — no routes", name)
            continue

        route = _longest_prefix_match(device_ip, routes)
        if route is None:
            logger.debug("  Skipping '%s' — no route covers %s", name, device_ip)
            continue

        # Compare against global best (more specific route wins)
        matched_network = ipaddress.ip_network(route['subnet'], strict=False)
        if matched_network.prefixlen <= best_prefixlen:
            logger.debug("  Server '%s' matched %s (/%d) but not better than "
                         "current best /%d", name, route['subnet'],
                         matched_network.prefixlen, best_prefixlen)
            continue

        iface_name = route.get('interface') or route.get('next-hop')
        if not iface_name:
            logger.debug("  Server '%s' route %s has no interface/next-hop",
                         name, route['subnet'])
            continue

        family = 'ipv6' if ':' in route['subnet'] else 'ipv4'
        interface_ip = _get_interface_ip_testbed(server, iface_name, family)
        if interface_ip is None:
            logger.debug("  Server '%s' could not resolve interface IP for '%s'",
                         name, iface_name)
            continue

        logger.debug("  Server '%s' is new best: route %s -> interface %s (%s)",
                     name, route['subnet'], iface_name, interface_ip)
        best_prefixlen = matched_network.prefixlen
        best_server_ip = interface_ip
        best_server_name = name

    if best_server_ip:
        logger.info("Find server IP for device IP: best match is server '%s' "
                    "interface IP %s (prefix_len=%d) for device %s",
                    best_server_name, best_server_ip, best_prefixlen, device_ip)
        return best_server_ip

    logger.info("Find server IP for device IP: no server found with route "
                "covering device IP %s — URL will not be rewritten "
                "(checked %d server(s)%s)",
                device_ip, len(candidates),
                f", scoped to '{server_hostname}'" if server_hostname else "")
    return None
