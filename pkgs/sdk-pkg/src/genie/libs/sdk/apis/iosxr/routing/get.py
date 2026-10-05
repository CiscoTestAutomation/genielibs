"""Common get functions for IOSXR routing"""

# Python
import logging
import ipaddress

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_routing_address_family(address):
    """ Determine the address family keyword for an IP address

        Args:
            address ('str'): IPv4 or IPv6 address (prefix length allowed)

        Returns:
            'ipv4' or 'ipv6'

        Raises:
            ValueError: if the address is not a valid IP address
    """
    value = str(address).split('/')[0]
    return 'ipv6' if ipaddress.ip_address(value).version == 6 else 'ipv4'


def get_routing_route_next_hop(device,
                               route,
                               address_family=None,
                               vrf=None):
    """ Get the next hop details for a route on an IOSXR device

        This is a single shot lookup (no polling). It normalizes the
        ``show route`` output so callers can reason about missing routes,
        connected routes and routes with one or more next hops.

        Args:
            device ('obj'): Device object
            route ('str'): Route/address to look up
            address_family ('str', optional): 'ipv4' or 'ipv6'. Defaults to
                None, in which case it is derived from ``route``.
            vrf ('str', optional): VRF name. Defaults to None.

        Returns:
            dict: with the following keys

                * ``route`` ('str' or None): route as reported by the device
                * ``next_hops`` ('list'): list of next hop IP addresses
                * ``outgoing_interfaces`` ('list'): list of outgoing interfaces
                * ``known_via`` ('str' or None)
                * ``source_protocol`` ('str' or None)
                * ``connected`` ('bool'): True when the route resolves
                  directly through an interface with no next hop address

            None: when the device has no route for the address. ``None`` means
            "the device answered and has no route", never "the lookup did not
            complete".

        Raises:
            ValueError: when the address family cannot be derived from
                ``route``.
            Exception: any failure that leaves reachability unknown (connection
                loss, unexpected parser failure, ...) is propagated unchanged
                so callers can tell it apart from a genuinely missing route.
    """
    if not address_family:
        # A bad address is a caller error, not an answer about reachability.
        address_family = get_routing_address_family(route)

    if vrf:
        cmd = 'show route vrf {vrf} {af} {route}'.format(
            vrf=vrf, af=address_family, route=route)
    else:
        cmd = 'show route {af} {route}'.format(
            af=address_family, route=route)

    try:
        out = device.parse(cmd)
    except SchemaEmptyParserError:
        # The device answered, the output just held no route (typically
        # '% Network not in table'). This is a real 'no route' answer.
        log.info("Route lookup %r on %s: parser returned no data",
                 cmd, device.name)
        return None
    except Exception:
        # Anything else (connection loss, unexpected parser failure, ...)
        # leaves reachability unknown. Do not disguise that as 'no route';
        # let the caller decide.
        log.warning("Route lookup %r on %s failed, reachability is unknown",
                    cmd, device.name, exc_info=True)
        raise

    if not out:
        log.info("Route lookup %r on %s: empty parsed output",
                 cmd, device.name)
        return None

    # Walk the schema explicitly rather than using Dq.get_values('next_hop').
    # The IOSXR schema nests next hops as
    #   routes.<net>.next_hop.next_hop_list.<index>.next_hop
    # and 'next_hop' names both the outer container and the leaf. A plain
    # get_values('next_hop') matches the container first and flattens it to
    # its keys, yielding the literal 'next_hop_list' instead of an address.
    next_hops = []
    outgoing_interfaces = []
    for vrf_data in (out.get('vrf') or {}).values():
        for af_data in (vrf_data.get('address_family') or {}).values():
            for route_data in (af_data.get('routes') or {}).values():
                next_hop = route_data.get('next_hop') or {}
                for hop in (next_hop.get('next_hop_list') or {}).values():
                    if hop.get('next_hop'):
                        next_hops.append(hop['next_hop'])
                    if hop.get('outgoing_interface'):
                        outgoing_interfaces.append(hop['outgoing_interface'])
                for intf in (next_hop.get('outgoing_interface')
                             or {}).values():
                    if intf.get('outgoing_interface'):
                        outgoing_interfaces.append(intf['outgoing_interface'])

    routes = out.q.get_values('route')
    known_via = out.q.get_values('known_via')
    source_protocol = out.q.get_values('source_protocol')

    log.info("Route lookup %r on %s extracted route=%r next_hops=%r "
             "outgoing_interfaces=%r", cmd, device.name, routes,
             next_hops, outgoing_interfaces)

    if not (next_hops or outgoing_interfaces or routes):
        log.info("Route lookup %r on %s: parsed output had no route, "
                 "next hop or outgoing interface values (parsed=%r)",
                 cmd, device.name, out)
        return None

    return {
        'route': routes[0] if routes else None,
        'next_hops': next_hops,
        'outgoing_interfaces': outgoing_interfaces,
        'known_via': known_via[0] if known_via else None,
        'source_protocol': source_protocol[0] if source_protocol else None,
        'connected': bool(outgoing_interfaces) and not next_hops,
    }
