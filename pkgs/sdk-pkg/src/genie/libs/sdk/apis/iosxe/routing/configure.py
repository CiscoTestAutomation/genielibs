"""Common configure functions for routing"""

# Python
import os
import logging

# Genie
from genie.conf.base import Interface
from genie.libs.conf.base import IPv4Address, IPv6Address
from genie.libs.conf.interface import IPv4Addr, IPv6Addr
from genie.libs.sdk.apis.utils import tftp_config

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_routing_ip_route(
    device, ip_address, mask, interface=None, dest_add=None
):
    """ Configure ip route on device

        Args:
            device ('obj'): Device obj
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

def configure_routing_ip_route_track(device, ip_address, mask, interface, dest_add, next_hop_name, track_obj, vrf = None):
    """ Configure ip route on device

        Args:
            device ('obj'): Device obj
            vrf ('str') : vrf name
            ip_address ('str'): ip address for interface
            mask (str): mask the ip address
            interface ('str'): interface name to configure
            dest_add('str'): destination address to configure
            next_hop_name(str) : name of the next hop
            track_obj(int)  : tracked object

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = []
    if vrf:
        cmd.append(f"ip route vrf {vrf} {ip_address} {mask} {interface} {dest_add} name {next_hop_name} track {track_obj}")
    else:
        cmd.append(f"ip route {ip_address} {mask} {interface} {dest_add} name {next_hop_name} track {track_obj}")
 

    try:
        device.configure(cmd)    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure object tracking. Error:\n{error}".format(
                error=e
            )
        )

        
def unconfigure_routing_ip_route_track(device, ip_address, mask, interface, dest_add, next_hop_name, track_obj, vrf = None):
    """ Configure ip route on device

        Args:
            device ('obj'): Device obj
            vrf ('str') : vrf name
            ip_address ('str'): ip address for interface
            mask (str): mask the ip address
            interface ('str'): interface name to configure
            dest_add('str'): destination address to configure
            next_hop_name(str) : name of the next hop
            track_obj(int)  : tracked object

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = []
    if vrf:
        cmd.append(f"no ip route vrf {vrf} {ip_address} {mask} {interface} {dest_add} name {next_hop_name} track {track_obj}")
    else:
        cmd.append(f"no ip route {ip_address} {mask} {interface} {dest_add} name {next_hop_name} track {track_obj}")


    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure object tracking. Error:\n{error}".format(
                error=e
            )
        )
        

def configure_routing_static_routev6(
    device, routev6, mask, vrf=None, interface=None, destination_addressv6=None
):
    """ Configure static ip route on device

        Args:
            device ('str'): Device str
            routev6 ('str'): ip address for route
            mask (str): mask the ip address
            vrf ('str',optional): Vrf for static route
            interface ('str'): interface name to configure
            destination_addressv6 ('str'): destination address to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    if vrf and destination_addressv6:
        configs.append(
            f"ipv6 route vrf {vrf} {routev6}/{mask} {destination_addressv6}")
    elif vrf and interface:
        configs.append(
             f"ipv6 route vrf {vrf} {routev6}/{mask} {interface}")
    elif interface:
        configs.append(
            f"ipv6 route vrf {vrf} {routev6}/{mask} {interface}")
    elif destination_addressv6:
        configs.append(
            f"ipv6 route vrf {vrf} {routev6}/{mask} {destination_addressv6}")
    try:
        device.configure(configs)
        log.info("Configuration successful for {route} ".format(route=routev6))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for {route}.".format(route=routev6)
        )

def unconfigure_routing_static_routev6(
    device, routev6, mask, vrf=None, interface=None, destination_addressv6=None
):
    """ Configure static ip route on device

        Args:
            device ('str'): Device str
            routev6 ('str'): ip address for route
            mask (str): mask the ip address
            vrf ('str',optional): Vrf for static route
            interface ('str'): interface name to configure
            destination_addressv6 ('str'): destination address to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    if vrf and destination_addressv6:
        configs.append(
            f"ipv6 route vrf {vrf} {routev6}/{mask} {destination_addressv6}")
    elif vrf and interface:
        configs.append(
             f"ipv6 route vrf {vrf} {routev6}/{mask} {interface}")

    elif interface:
        configs.append(
            f"ipv6 route vrf {vrf} {routev6}/{mask} {interface}")
    elif destination_addressv6:
        configs.append(
            f"ipv6 route vrf {vrf} {routev6}/{mask} {destination_addressv6}")

    try:
        device.configure(configs)
        log.info("Configuration successful for {route} ".format(route=routev6))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for {route}.".format(route=routev6)
        )


def configure_routing_static_route(
    device, route, mask, interface=None, destination_address=None, vrf=None, dhcp=False, dhcp_metirc=None
):
    """ Configure static ip route on device

        Args:
            device ('obj'): Device obj
            route ('str'): ip address for route
            mask (str): mask the ip address
            interface ('str'): interface name to configure
            destination_address('str'): destination address to configure
            vrf ('str',optional): Vrf for static route            
            dhcp ('boolean',optional): Flag to configure default Gateway obtained from DHCP (Default False)
            dhcp_metirc('int',optional ): Distance metric for this dhcp route 
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    if interface and destination_address:
        configs.append(
            f"ip route {route} {mask} {interface} {destination_address}")
    elif vrf and destination_address:
        configs.append(
            f"ip route vrf {vrf} {route} {mask} {destination_address}")
    elif vrf and interface:
        configs.append(
            f"ip route vrf {vrf} {route} {mask} {interface}")
    elif vrf and destination_address and interface:
        configs.append(
            f"ip route vrf {vrf} {route} {mask} {interface} {destination_address} global")
    elif interface:
        configs.append(
            f"ip route {route} {mask} {interface}")
    elif destination_address:
        configs.append(
            f"ip route {route} {mask} {destination_address}")
    elif dhcp:
        if dhcp_metirc:
            configs.append(
                f"ip route {route} {mask} dhcp {dhcp_metirc}")
        else:
            configs.append(
                f"ip route {route} {mask} dhcp")
    try:
        device.configure(configs)
        log.info("Configuration successful for {route} ".format(route=route))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for {route}.".format(route=route)
        )
def unconfigure_routing_static_route(
    device, route, mask, vrf=None, interface=None, destination_address=None
):
    """ Configure static ip route on device

        Args:
            device ('obj'): Device obj
            route ('str'): ip address for route
            mask (str): mask the ip address
            vrf ('str',optional): Vrf for static route
            interface ('str'): interface name to configure
            destination_address('str'): destination address to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    if interface and destination_address:
        configs.append(
            f"no ip route {route} {mask} {interface} {destination_address}")
    elif vrf and destination_address:
        configs.append(
            f"no ip route {vrf} {route} {mask} {destination_address}")
    elif vrf and interface:
        configs.append(
            f"no ip route {vrf} {route} {mask} {interface}")
    elif interface:
        configs.append(
            f"no ip route {route} {mask} {interface}")
    elif destination_address:
        configs.append(
            f"no ip route {route} {mask} {destination_address}")
    try:
        device.configure(configs)
        log.info("Configuration successful for {route} ".format(route=route))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for {route}.".format(route=route)
        )


def configure_scale_static_route_via_tftp(
    device, server, scale_count,
    network_start, network_step, netmask,
    next_hop_start=None, next_hop_step=None, next_intf=None,
    unconfig=False, tftp=False
):
    """ Configure scale static ip route on device via tftp
        Examples:
        ip route 192.168.1.0 255.255.255.0 10.0.0.1
        ip route 192.168.2.0 255.255.255.0 10.0.1.1

        Args:
            device ('obj'): Device obj
            server ('str'): Testbed.servers
            scale_count (int): How many static routes
            network_start ('str'): Prefix eg. 192.168.1.0
            network_step ('str'): Prefix step eg. 0.0.1.0
            netmask ('str'): Netmask of prefix eg. 255.255.255.0
            next_hop_start ('str'): Next hop. eg. 10.0.0.1
            next_hop_step ('str'): Step of next hop. eg. 0.0.1.0
            next_intf ('str'): Next hop interface name. eg. G2
            unconfig ('bool'): Unconfig or not
            tftp ('bool'): Tftp config or not

        Returns:
            None
            cmds_block str if not tftp configure

        Raises:
            Failure
    """
    if not next_hop_start and not next_intf:
        raise Exception('Please specify either next_hop nor next_intf')
    elif next_hop_start and not next_intf:
        next_hop = IPv4Address(next_hop_start)
        next_intf = ''
    elif next_intf and not next_hop_start:
        next_intf = next_intf
        next_hop = ''
    else:
        next_hop = IPv4Address(next_hop_start)
        next_intf = next_intf

    cmds = ''
    network = IPv4Address(network_start)

    if unconfig:
        no_str = 'no'
    else:
        no_str = ''

    for count in range(scale_count):

        cmds += '''
        {no_str} ip route {network} {netmask} {next_hop} {next_intf}
        '''.format(no_str=no_str, network=network, netmask=netmask,
                   next_hop=next_hop, next_intf=next_intf)

        network += int(IPv4Address(network_step))

        if next_hop != '':
            next_hop += int(IPv4Address(next_hop_step))

    if tftp:
        try:
            tftp_config(device, server, cmds)
        except Exception:
            raise Exception('tftp_config failed.')
    else:
        return cmds


def enable_routing_debug_static_route(device, route, mask):
    """ Enables debug route on device

        Args:
            device ('obj'): Device obj
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
            device ('obj'): Device obj

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


def unconfigure_ipv6_unicast_routing(device):
    """ Disables ipv6 unicast routing on device
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        'Disables ipv6 unicast routing on device '
    )

    try:
        device.configure(
            "no ipv6 unicast-routing"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable ipv6 unicast routing on "
            "device. Error:\n{e}".format(e=e)
        )

def disable_ip_routing(device):
    """ Disables ip routing on device

        Args:
            device ('obj'): Device obj

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
            device ('obj'): Device obj
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
            device ('obj'): Device obj
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
    """ Configure ip vrf route on device

        Args:
            device ('obj'): Device obj
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

def unconfigure_routing_ip_route_vrf(
    device,
    ip_address,
    mask,
    vrf,
    interface=None,
    dest_add=None
    ):
    """ Unconfigure ip vrf route on device

        Args:
            device ('obj'): Device obj
            ip_address ('str'): ip address to reach
            mask (str): mask the ip address
            vrf(str)  : vrf name
            interface ('str',optional): interface name to configure, default is None
            dest_add('str',optional): gateway address to configure, default is None
            
        Returns:
            None
            
        Raises:
            SubCommandFailure
    """
    cmd = []
    if interface and dest_add:
        cmd.append("no ip route vrf {vrf} {ip_address} {mask} {interface} {dest_add}".format(
            vrf=vrf, ip_address=ip_address, mask=mask, interface=interface, dest_add=dest_add               
            ))
    elif interface:
        cmd.append("no ip route vrf {vrf} {ip_address} {mask} {interface}".format(
            vrf=vrf, ip_address=ip_address, mask=mask, interface=interface              
            ))
    elif dest_add:
        cmd.append("no ip route vrf {vrf} {ip_address} {mask} {dest_add}".format(
            vrf=vrf, ip_address=ip_address, mask=mask, dest_add=dest_add               
            ))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for removing vrf static route for {ip_address}.\
                Error:\n{error}".format(ip_address=ip_address, error=e\
            )
        )
              
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
            device ('obj'): Device obj
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

def configure_tftp_source_interface(
    device,
    interface
    ):
    """ Configure tftp source interface on device

        Args:
            device ('obj'): Device obj
            interface ('str'): interface name to configure
        Returns:
            None
            
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "ip tftp source-interface {interface}".format(interface=interface
            )
        )

    except SubCommandFailure:
        log.error('Failed to configure tftp source interface')
        raise

def unconfigure_tftp_source_interface(
    device,
    interface
    ):
    """ Unconfigure tftp source interface on device

        Args:
            device ('obj'): Device obj
            interface ('str'): interface name to configure
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "no ip tftp source-interface {interface}".format(interface=interface
            )
        )

    except SubCommandFailure:
        log.error('Failed to Unconfigure tftp source interface')
        raise

def configure_ipv6_static_route(
    device, route, mask, interface=None, destination_address=None
):
    """ Configure static ip route on device
        Args:
            device ('obj'): Device obj
            route ('str'): ip address for route
            mask (str): mask the ip address
            interface ('str', optional): interface name to configure. Default is None
            destination_address('str', optional): destination address to configure. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    if interface:
        cmd.append("ipv6 route {route}/{mask} {interface}".format(
            route=route, mask=mask, interface=interface
        ))
    elif destination_address:
        cmd.append("ipv6 route {route}/{mask} {destination_address}".format(
            route=route, mask=mask, destination_address=destination_address
        ))
    else:
        raise Exception("missing required argument: 'interface/destination_address'")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for {route}. Error:\n{error}".
            format(route=route,error=e)
        )

def unconfigure_ipv6_static_route(
    device, route, mask, interface=None, destination_address=None
):
    """ Configure static ip route on device
        Args:
            device ('obj'): Device obj
            route ('str'): ip address for route
            mask (str): mask the ip address
            interface ('str', optional): interface name to configure. Default is False
            destination_address('str', optional): destination address to configure. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    if interface:
        cmd.append("no ipv6 route {route}/{mask} {interface}".format(
            route=route, mask=mask, interface=interface
        ))
    elif destination_address:
        cmd.append("no ipv6 route {route}/{mask} {destination_address}".format(
            route=route, mask=mask, destination_address=destination_address
        ))
    else:
        raise Exception("missing required argument: 'interface/destination_address'")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for {route}.Error:\n{error}".
            format(route=route,error=e)
        )
def configure_routing_ipv6_route(
    device, ipv6_address, interface=None, dest_add=None
):
    """ Configure ipv6 route on device

        Args:
            device ('obj'): Device obj
            ipv6_address ('str'): ipv6 address/mask for interface
            interface ('str',optional): interface name to configure, default is None
            dest_add('str',optional): destination address to configure, default is None

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = []
    if interface and dest_add:
        cmd.append("ipv6 route {ipv6_address} {interface} {dest_add}".format(
            ipv6_address=ipv6_address, interface=interface, dest_add=dest_add
        ))
    elif interface:
        cmd.append("ipv6 route {ipv6_address} {interface}".format(
            ipv6_address=ipv6_address, interface=interface
        ))
    elif dest_add:
        cmd.append("ipv6 route {ipv6_address} {dest_add}".format(
            ipv6_address=ipv6_address, dest_add=dest_add
        ))
    try:
        device.configure(cmd)
    except (UnboundLocalError, SubCommandFailure) as e:
        raise SubCommandFailure(
            "Configuration failed for adding route for {ipv6_address}. Error:\n{error}".format(
                ipv6_address=ipv6_address, error=e
            )
        )

def unconfigure_routing_ipv6_route(
    device, ipv6_address, interface=None, dest_add=None
):
    """ Unconfigure ipv6 route on device

        Args:
            device ('obj'): Device obj
            ipv6_address ('str'): ipv6 address/mask for interface
            interface ('str',optional): interface name to configure, default is None
            dest_add('str',optional): destination address to configure, default is None

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = []
    if interface and dest_add:
        cmd.append("no ipv6 route {ipv6_address} {interface} {dest_add}".format(
            ipv6_address=ipv6_address, interface=interface, dest_add=dest_add
        ))
    elif interface:
        cmd.append("no ipv6 route {ipv6_address} {interface}".format(
            ipv6_address=ipv6_address, interface=interface
        ))
    elif dest_add:
        cmd.append("no ipv6 route {ipv6_address} {dest_add}".format(
            ipv6_address=ipv6_address, dest_add=dest_add
        ))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for removing route for {ipv6_address}. Error:\n{error}".format(
                ipv6_address=ipv6_address, error=e
            )
        )

def configure_routing_ipv6_route_vrf(
    device,
    ipv6_address,
    vrf,
    interface=None,
    dest_add=None
    ):
    """ Configure ipv6 vrf route on device

        Args:
            device ('obj'): Device obj
            ipv6_address ('str'): ipv6 address/mask to reach
            vrf(str)  : vrf name
            interface ('str',optional): interface name to configure, default is None.
            dest_add('str',optional): gateway address to configure, default is None.

        Returns:
            None

        Raises:
            SubCommandFailure
    """            
    cmd = []
    if interface and dest_add:
        cmd.append("ipv6 route vrf {vrf} {ipv6_address} {interface} {dest_add}".format(
            vrf=vrf, ipv6_address=ipv6_address, interface=interface, dest_add=dest_add               
            ))
    elif interface:
        cmd.append("ipv6 route vrf {vrf} {ipv6_address} {interface}".format(
            vrf=vrf, ipv6_address=ipv6_address, interface=interface              
            ))
    elif dest_add:
        cmd.append("ipv6 route vrf {vrf} {ipv6_address} {dest_add}".format(
            vrf=vrf, ipv6_address=ipv6_address, dest_add=dest_add               
            ))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for adding vrf static route for {ipv6_address}.\
                Error:\n{error}".format(ipv6_address=ipv6_address, error=e
            )
        )

def unconfigure_routing_ipv6_route_vrf(
    device,
    ipv6_address,
    vrf,
    interface=None,
    dest_add=None
    ):
    """ Unconfigure ipv6 vrf route on device

        Args:
            device ('obj'): Device obj
            ipv6_address ('str'): ipv6 address/mask to reach
            vrf(str)  : vrf name
            interface ('str',optional): interface name to configure, default is None.
            dest_add('str',optional): gateway address to configure, default is None.

        Returns:
            None

        Raises:
            SubCommandFailure
    """  
    cmd = []
    if interface and dest_add:
        cmd.append("no ipv6 route vrf {vrf} {ipv6_address} {interface} {dest_add}".format(
            vrf=vrf, ipv6_address=ipv6_address, interface=interface, dest_add=dest_add               
            ))
    elif interface:
        cmd.append("no ipv6 route vrf {vrf} {ipv6_address} {interface}".format(
            vrf=vrf, ipv6_address=ipv6_address, interface=interface              
            ))
    elif dest_add:
        cmd.append("no ipv6 route vrf {vrf} {ipv6_address} {dest_add}".format(
            vrf=vrf, ipv6_address=ipv6_address, dest_add=dest_add
            ))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for removing vrf static route for {ipv6_address}.\
                Error:\n{error}".format(ipv6_address=ipv6_address, error=e
            )
        )

def configure_stack_mac_persistent_timer(device, mac_timer):
    """ configure stack-mac persistent timer on device

        Args:
            device ('str'): Device str
            mac_timer ('str'): mac timer need to be set

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        'configuring stack-mac persistent timer on device'
    )

    try:
        device.configure(
            "stack-mac persistent timer {mac_timer}".format(mac_timer=mac_timer)
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mac timer on device. Error:\n{e}".format(e=e)
        )

def configure_ipv6_route_nexthop_vrf(
    device,
    ipv6_address,
    interface,
    vrf_name
):
    """ Configure ipv6 route nexthop vrf
        Args:
            device ('obj'): device to use
            ipv6_address ('str'): Ipv6 address
            interface ('str'): interface name
            vrf_name ('str'): vrf name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"ipv6 route {ipv6_address} {interface} nexthop-vrf {vrf_name}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ipv6 route nexthop vrf. Error:\n{error}".format(error=e)
        )

def unconfigure_ipv6_route_nexthop_vrf(
    device,
    ipv6_address,
    interface,
    vrf_name
):
    """ UnConfigure ipv6 route nexthop vrf
        Args:
            device ('obj'): device to use
            ipv6_address ('str'): Ipv6 address
            interface ('str'): interface name
            vrf_name ('str'): vrf name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"no ipv6 route {ipv6_address} {interface} nexthop-vrf {vrf_name}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ipv6 route nexthop vrf. Error:\n{error}".format(error=e)
        )

def unconfigure_system_mtu(device, size=None):
    """ Unconfigures system mtu
        Example : no system mtu 9216
        Args:
            device ('obj'): device to use
            size ('int'): mtu size (eg. 9216)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = 'no system mtu'
    if size:
        config += f' {size}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to unconfigure system mtu on device {device.name}. Error:\n{e}')

def unconfigure_stack_mac_persistent_timer(device):
    """ unconfigure stack-mac persistent timer on device

        Args:
            device ('str'): Device str

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info('unconfiguring stack-mac persistent timer on device')

    cmd = [f"no stack-mac persistent timer"]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure mac timer on device. Error:\n{e}")

def remove_static_route_all(device):
    """ remove ip route 
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """
    log.info(f'removing static route all in {device}')
    cmd = ('no ip route *')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not remove the static routes on {device}. Error:\n{e}')

def enable_keepalive_on_interface(device, interface):
    """ Enables keepalive on interface
        Args:
            device ('obj'): Device obj
            interface ('str'): be keepalive
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        'Enabling keepalive on interface '
    )
    cmd = [f"interface {interface}", "keepalive"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable  keepalive on interface {interface}. Error:\n{error}".format(interface=interface, error=e)
        )

def enable_ip_classless(device):
    '''Enable ip classless on device
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure: Failed executing command
    '''
    log.debug('Enabling ip classless on device')
    cmd = f'ip classless'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to enable ip classless on device {device}. Error:\n{e}')
