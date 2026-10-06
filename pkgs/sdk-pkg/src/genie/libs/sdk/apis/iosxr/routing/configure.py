"""Common configure functions for IOSXR static routing"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def build_static_routing_route_config(prefix,
                                      next_hop,
                                      address_family='ipv4',
                                      vrf=None,
                                      unconfigure=False):
    """ Build the IOSXR ``router static`` configuration lines for a route

        Args:
            prefix ('str'): Destination prefix, e.g. '10.1.1.1/32'
            next_hop ('str'): Next hop address or interface
            address_family ('str'): 'ipv4' or 'ipv6'. Default: 'ipv4'
            vrf ('str'): Optional VRF name. Default: None, meaning the
                route is built for the default VRF
            unconfigure ('bool'): Prefix the route line with 'no'.
                Default: False

        Returns:
            list: configuration lines
    """
    if address_family not in ('ipv4', 'ipv6'):
        raise ValueError(
            "address_family must be 'ipv4' or 'ipv6', got {!r}".format(
                address_family))

    route_line = '{prefix} {next_hop}'.format(prefix=prefix,
                                              next_hop=next_hop)
    if unconfigure:
        route_line = 'no ' + route_line

    config = ['router static']
    indent = ' '
    if vrf:
        config.append('{}vrf {}'.format(indent, vrf))
        indent += ' '
    config.append('{}address-family {} unicast'.format(indent,
                                                       address_family))
    indent += ' '
    config.append('{}{}'.format(indent, route_line))
    return config


def configure_static_routing_route(device,
                                   prefix,
                                   next_hop,
                                   address_family='ipv4',
                                   vrf=None):
    """ Configure a static route on an IOSXR device

        Args:
            device ('obj'): Device object
            prefix ('str'): Destination prefix, e.g. '10.1.1.1/32'
            next_hop ('str'): Next hop address or interface
            address_family ('str'): 'ipv4' or 'ipv6'. Default: 'ipv4'
            vrf ('str'): Optional VRF name. Default: None, meaning the
                route is configured in the default VRF

        Returns:
            list: the configuration that was applied

        Raises:
            SubCommandFailure: when the configuration fails
    """
    config = build_static_routing_route_config(prefix,
                                               next_hop,
                                               address_family=address_family,
                                               vrf=vrf)
    try:
        device.configure(config)
    except Exception as e:
        raise SubCommandFailure(
            "Could not configure static route {prefix} via {next_hop} on "
            "{device}".format(prefix=prefix,
                              next_hop=next_hop,
                              device=device.name)) from e
    return config


def unconfigure_static_routing_route(device,
                                     prefix,
                                     next_hop,
                                     address_family='ipv4',
                                     vrf=None):
    """ Remove a static route from an IOSXR device

        Args:
            device ('obj'): Device object
            prefix ('str'): Destination prefix, e.g. '10.1.1.1/32'
            next_hop ('str'): Next hop address or interface
            address_family ('str'): 'ipv4' or 'ipv6'. Default: 'ipv4'
            vrf ('str'): Optional VRF name. Default: None, meaning the
                route is removed from the default VRF

        Returns:
            list: the configuration that was applied

        Raises:
            SubCommandFailure: when the configuration fails
    """
    config = build_static_routing_route_config(prefix,
                                               next_hop,
                                               address_family=address_family,
                                               vrf=vrf,
                                               unconfigure=True)
    try:
        device.configure(config)
    except Exception as e:
        raise SubCommandFailure(
            "Could not remove static route {prefix} via {next_hop} on "
            "{device}".format(prefix=prefix,
                              next_hop=next_hop,
                              device=device.name)) from e
    return config
