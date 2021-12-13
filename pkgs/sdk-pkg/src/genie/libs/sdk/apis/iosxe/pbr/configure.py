"""Common configure functions for PBR"""

import logging
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_route_map_under_interface(device, interface, route_map):
    """ Configure route-map on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            route_map (`str`): Route-map to be configured on interface

        Returns:
            None

        Raises:
            SubCommandFailure

    """
    configs = [
        "interface {intf}".format(intf=interface),
        "ip policy route-map  {policy}".format(policy=route_map),
    ]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure route-map under interface {interface} on device {dev}. Error:\n{error}"
            .format(
                interface=interface,
                dev=device.name,
                error=e,
            ))


def unconfigure_route_map_under_interface(device, interface, route_map):
    """ unonfigure route-map on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            route_map (`str`): Route-map to be configured on interface

        Returns:
            None

        Raises:
            SubCommandFailure

    """
    configs = [
        "interface {intf}".format(intf=interface),
        "no ip policy route-map  {policy}".format(policy=route_map),
    ]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure route-map under interface {interface} on device {dev}. Error:\n{error}"
            .format(
                interface=interface,
                dev=device.name,
                error=e,
            ))


def configure_pbr_route_map(device,
                            route_map_name,
                            acl_name,
                            next_hop_ip,
                            default_next_hop=None):
    """ Configure route-map

        Args:
            device (`obj`): Device object
            route_map_name (`str`): Route-map to be configured on interface
            acl_name (`str`): Route-map to be attached on interface
            next_hop_ip (`str`): Next-hop ip address
            default_next_hop (`str`, optional): Default Next-hop ip address, default value is None

        Returns:
            None

        Raises:
            SubCommandFailure

    """
    configs = [
        "route-map {pbr}".format(pbr=route_map_name),
        "match ip address {acl}".format(acl=acl_name),
    ]

    if default_next_hop:
        configs.append("set ip default next-hop {ip}".format(ip=next_hop_ip))

    else:
        configs.append("set ip next-hop {ip}".format(ip=next_hop_ip))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure route map {pbr} on device {dev}. Error:\n{error}"
            .format(
                pbr=route_map_name,
                dev=device.name,
                error=e,
            ))


def unconfigure_pbr_route_map(device, route_map_name):
    """ Unconfigure route-map

        Args:
            device (`obj`): Device object
            route_map_name (`str`): Route-map to be configured on interface

        Returns:
            None

        Raises:
            SubCommandFailure

    """
    configs = ["no route-map {pbr}".format(pbr=route_map_name)]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure route map {pbr} on device {dev}. Error:\n{error}"
            .format(
                pbr=route_map_name,
                dev=device.name,
                error=e,
            ))
