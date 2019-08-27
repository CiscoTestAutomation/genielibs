"""Common configure functions for routing"""

# Python
import os
import logging

# Genie
from genie.conf.base import Interface

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_routing_ip_route(
    device, ip_address, mask, interface=None, dest_add=None
):
    """ Configure ip route on device

        Args:
            device ('str'): Device str
            ip_address ('str'): ip address for interface
            mask (str): mask the ip address
            interface ('str'): interface name to configure
            dest_add('str'): destination address to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        if interface and dest_add:
            device.configure(
                "ip route "
                + ip_address
                + " "
                + mask
                + " "
                + interface
                + " "
                + dest_add
            )
        elif interface:
            device.configure(
                "ip route " + ip_address + " " + mask + " " + interface
            )
        elif dest_add:
            device.configure(
                "ip route " + ip_address + " " + mask + " " + dest_add
            )
        log.info(
            "Configuration successful for {ip_address} ".format(
                ip_address=ip_address
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for {ip_address}. Error:\n{error}".format(
                ip_address=ip_address, error=e
            )
        )


def remove_routing_ip_route(
    device, ip_address, mask, interface=None, dest_add=None
):
    """ Remove ip route on device

        Args:
            device ('str'): Device str
            ip_address ('str'): ip address for interface
            mask (str): mask the ip address
            interface ('str'): interface name to configure
            dest_add('str'): destination address to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        if interface and dest_add:
            device.configure(
                "no ip route "
                + ip_address
                + " "
                + mask
                + " "
                + interface
                + " "
                + dest_add
            )
        elif interface:
            device.configure(
                "no ip route " + ip_address + " " + mask + " " + interface
            )
        elif dest_add:
            device.configure(
                "no ip route " + ip_address + " " + mask + " " + dest_add
            )
        log.info(
            "Configuration removed for {ip_address} ".format(
                ip_address=ip_address
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for {ip_address}. Error:\n{error}".format(
                ip_address=ip_address, error=e
            )
        )


def configure_routing_static_route(
    device, route, mask, interface=None, destination_address=None
):
    """ Configure static ip route on device

        Args:
            device ('str'): Device str
            route ('str'): ip address for route
            mask (str): mask the ip address
            interface ('str'): interface name to configure
            destination_address('str'): destination address to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        if interface and destination_address:
            device.configure(
                "ip route "
                + route
                + " "
                + mask
                + " "
                + interface
                + " "
                + destination_address
            )
        elif interface:
            device.configure(
                "ip route " + route + " " + mask + " " + interface
            )
        elif destination_address:
            device.configure(
                "ip route " + route + " " + mask + " " + destination_address
            )
        log.info("Configuration successful for {route} ".format(route=route))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for {route}.".format(route=route)
        )


def enable_routing_debug_static_route(device, route, mask):
    """ Enables debug route on device

        Args:
            device ('str'): Device str
            route ('str'): route
            mask (str): mask the ip address

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        'Enabling debug route "debug ip routing static route {} {}"'.format(
            route, mask
        )
    )

    try:
        device.execute(
            "debug ip routing static route {} {}".format(route, mask)
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable debug on static route. Error:\n{}".format(e)
        )
