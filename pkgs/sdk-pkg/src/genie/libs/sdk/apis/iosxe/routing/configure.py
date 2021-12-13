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


def enable_ip_routing(device):
    """ Enables ip routing on device

        Args:
            device ('str'): Device str

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        'Enabling ip routing on device '
    )

    try:
        device.configure(
            "ip routing"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable ip routing on device. Error:\n{e}".format(e=e)
        )

def enable_ipv6_unicast_routing(device):
    """ Enables ipv6 unicast routing on device

        Args:
            device ('obj'): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        'Enabling ipv6 unicast routing on device '
    )

    try:
        device.configure(
            "ipv6 unicast-routing"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable ipv6 unicast routing on "
            "device. Error:\n{e}".format(e=e)
        )

def disable_ip_routing(device):
    """ Disables ip routing on device

        Args:
            device ('str'): Device str

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        'Disabling ip routing on device '
    )

    try:
        device.configure(
            "no ip routing"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable ip routing on device. Error:\n{e}".format(e=e)
        )


def set_system_mtu(device, mtu_value):
    """ Sets mtu value on device

        Args:
            device ('str'): Device str
            mtu_value ('str'): MTU value to be set

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        'Setting mtu value on device '
    )

    try:
        device.configure(
            "system mtu {mtu_value}".format(mtu_value=mtu_value)
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not set mtu value on device. Error:\n{e}".format(e=e)
        )


def disable_keepalive_on_interface(device, interface):
    """ Disables keepalive on interface 

        Args:
            device ('str'): Device str
            interface ('str'): MTU value to be configured

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        'Disabling keepalive on interface '
    )

    try:
        device.configure(["interface {interface}".format(interface=interface), "no keepalive"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable keepalive on interface {interface}. Error:\n{error}".format(interface=interface, error=e)
        )

def configure_routing_ip_route_vrf(
    device,
    ip_address,
    mask,
    vrf,
    interface=None,
    dest_add=None
    ):
    """ Configure ip route on device

        Args:
            device ('str'): Device str
            ip_address ('str'): ip address to reach
            mask (str): mask the ip address
            vrf(str)  : vrf name
            interface ('str'): interface name to configure,default is None.
            dest_add('str'): gateway address to configure,default is None.
            
        Returns:
            None
            
        Raises:
            SubCommandFailure
    """
    
    try:
        if interface and dest_add:
            device.configure(
                "ip route vrf {vrf} {ip_address} {mask} {interface} {dest_add}".format(
                vrf=vrf,ip_address=ip_address,mask=mask,interface=interface,dest_add=dest_add               
                )
            )
        elif interface:
            device.configure(
                "ip route vrf {vrf} {ip_address} {mask} {interface}".format(
                vrf=vrf,ip_address=ip_address,mask=mask,interface=interface              
                )
            )
        elif dest_add:
            device.configure(
                "ip route vrf {vrf} {ip_address} {mask} {dest_add}".format(
                vrf=vrf,ip_address=ip_address,mask=mask,dest_add=dest_add               
                )
            )
        log.info(
            "Configuration successful for {ip_address} ".format(
                ip_address=ip_address
            )
        )
    except SubCommandFailure:
        log.error('Failed to configure the vrf static route')
        raise
                
def configure_default_gateway(device, gateway_ip):
    """ Configures default gateway

        Args:
            device ('obj'): Device obj
            gateway_ip ('str'): IP address of gateway to be configured
              
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    
    log.info(
        'Configuring default gateway'
    )

    try:
        device.configure(["ip default-gateway {gateway_ip}".format(gateway_ip=gateway_ip)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure default gateway. Error:\n{error}".format(error=e)
        )

def configure_system_jumbomtu(device, mtu_value):
    """ Sets mtu value on device
        Args:
            device ('str'): Device str
            mtu_value ('int'): MTU value to be set
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            "system jumbomtu {mtu_value}".format(mtu_value=mtu_value)
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not set mtu value on device. Error:\n{e}".format(e=e)
        )

def enable_ipv6_multicast_routing(device):
    """ Enables ipv6 multicast routing on device

        Args:
            device ('obj'): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        'Enabling ipv6 multicast routing on device '
    )

    try:
        device.configure(
            "ipv6 multicast-routing"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable ipv6 multicast routing on "
            "device. Error:\n{e}".format(e=e)
        )

def disable_ipv6_multicast_routing(device):
    """ Disables ipv6 multicast routing on device

        Args:
            device ('obj'): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        'Disabling ipv6 multicast routing on device '
    )

    try:
        device.configure(
            "no ipv6 multicast-routing"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable ipv6 multicast routing on "
            "device. Error:\n{e}".format(e=e)
        )
