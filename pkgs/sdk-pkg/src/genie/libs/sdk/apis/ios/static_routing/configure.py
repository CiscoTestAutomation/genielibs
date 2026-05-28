"""Common configure functions for static_routing"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_static_route(device, network, mask, next_hop):
    """ Configure IPv4 static route on device

        Args:
            device (`obj`): Device object
            network (`str`): IPv4 destination network
            mask (`str`): IPv4 subnet mask
            next_hop (`str`): IPv4 next hop address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"ip route {network} {mask} {next_hop}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure static route. Error: {e}"
        )


def unconfigure_static_route(device, network, mask, next_hop):
    """ Unconfigure IPv4 static route on device

        Args:
            device (`obj`): Device object
            network (`str`): IPv4 destination network
            mask (`str`): IPv4 subnet mask
            next_hop (`str`): IPv4 next hop address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"no ip route {network} {mask} {next_hop}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure static route. Error: {e}"
        )


def configure_ipv6_static_route(device, ipv6_network, ipv6_prefix_length, ipv6_next_hop):
    """ Configure IPv6 static route on device

        Args:
            device (`obj`): Device object
            ipv6_network (`str`): IPv6 destination network
            ipv6_prefix_length (`str`): IPv6 prefix length
            ipv6_next_hop (`str`): IPv6 next hop address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            f"ipv6 route {ipv6_network}/{ipv6_prefix_length} {ipv6_next_hop}"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure IPv6 static route. Error: {e}"
        )


def unconfigure_ipv6_static_route(device, ipv6_network, ipv6_prefix_length, ipv6_next_hop):
    """ Unconfigure IPv6 static route on device

        Args:
            device (`obj`): Device object
            ipv6_network (`str`): IPv6 destination network
            ipv6_prefix_length (`str`): IPv6 prefix length
            ipv6_next_hop (`str`): IPv6 next hop address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            f"no ipv6 route {ipv6_network}/{ipv6_prefix_length} {ipv6_next_hop}"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure IPv6 static route. Error: {e}"
        )
