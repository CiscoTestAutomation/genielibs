"""Common configure functions for PBR"""

import logging
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_route_map_under_interface(device, interface, route_map, ipv6=False):
    """ Configure route-map on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            route_map (`str`): Route-map to be configured on interface
            ipv6 ('bool'): Indicate if this is ipv6 route map. Default false
        Returns:
            None

        Raises:
            SubCommandFailure

    """
    if not ipv6:
        configs = [
            "interface {intf}".format(intf=interface),
            "ip policy route-map {policy}".format(policy=route_map),
        ]  
    else:
        configs = [
            "interface {intf}".format(intf=interface),
            "ipv6 policy route-map {policy}".format(policy=route_map),
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


def unconfigure_route_map_under_interface(device, interface, route_map, ipv6=False):
    """ unonfigure route-map on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            route_map (`str`): Route-map to be configured on interface
            ipv6 ('bool'): Indicate if this is ipv6 route map. Default false

        Returns:
            None

        Raises:
            SubCommandFailure

    """
    if not ipv6:
        configs = [
            "interface {intf}".format(intf=interface),
            "no ip policy route-map  {policy}".format(policy=route_map),
        ]
    else:
        configs = [
            "interface {intf}".format(intf=interface),
            "no ipv6 policy route-map  {policy}".format(policy=route_map),
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
                            default_next_hop=None,
                            vrf=None,
                            set_int=None ):
    """ Configure route-map

        Args:
            device (`obj`): Device object
            route_map_name (`str`): Route-map to be configured on interface
            acl_name (`str`): Route-map to be attached on interface
            next_hop_ip (`str`): Next-hop ip address
            default_next_hop (`str`, optional): Default Next-hop ip address, default value is None
            vrf ('str',optional): Vrf for pbr
            set_int ('str',optional): Set interface for pbr
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

    if next_hop_ip:
        configs.append("set ip next-hop {ip}".format(ip=next_hop_ip))
    if vrf:
        configs.append("set ip {vrf} next-hop {ip}".format(vrf=vrf,ip=next_hop_ip))
    if set_int:
        configs.append("set interface {set_int}".format(set_int=set_int))
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
