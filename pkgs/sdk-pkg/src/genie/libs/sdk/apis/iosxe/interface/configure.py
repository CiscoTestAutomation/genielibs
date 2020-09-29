"""Common configure functions for interface"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Steps
from pyats.aetest.steps import Steps

# Genie
from genie.conf.base import Interface
from genie.libs.conf.base import IPv4Address, IPv6Address
from genie.libs.conf.interface import IPv4Addr, IPv6Addr
from genie.harness.utils import connect_device

# Interface
from genie.libs.sdk.apis.iosxe.interface.get import (
    get_interface_running_config,
)
from genie.libs.sdk.apis.iosxe.interface.get import (
    get_interface_connected_adjacent_router_interfaces,
)

# utils
from genie.libs.sdk.apis.utils import mask_to_int

log = logging.getLogger(__name__)


def reset_interface(device, interface):
    """ Reset interface configuration

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info("Defaulting interface {interface}".format(interface=interface))

    try:
        device.configure(
            "default interface {interface}".format(interface=interface)
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not default {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )


def clear_interface_counters(device, interface):
    """ Clear interface counters

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Clearing counters on interface {interface}".format(
            interface=interface
        )
    )

    try:
        device.execute(
            "clear counters {interface}".format(interface=interface)
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear counters on {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )


def config_interface_negotiation(device, interface):
    """ Config negotiation auto on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring negotiation auto on interface {interface}".format(
            interface=interface
        )
    )

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "negotiation auto",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to config negotiation auto on interface {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )


def remove_interface_negotiation(device, interface):
    """ Remove negotiation auto on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Removing negotiation auto on interface {interface}".format(
            interface=interface
        )
    )
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "no negotiation auto",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfig negotiation auto on interface {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )


def shut_interface(device, interface):
    """ Shut interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    if not device.is_connected():
        connect_device(device=device)

    try:
        device.configure(
            ["interface {interface}".format(interface=interface), "shutdown"]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not shut interface {intf} on device {dev}. Error:\n{error}".format(
                intf=interface, dev=device.name, error=e
            )
        )


def unshut_interface(device, interface):
    """ Unshut interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    if not device.is_connected():
        connect_device(device=device)
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "no shutdown",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unshut interface {interface} on device {dev}. Error:\n{error}".format(
                interface=interface, dev=device.name, error=e
            )
        )


def shut_interface_adjacent_interfaces(
    device, link_name, adjacent_interfaces=None, steps=Steps(), num=1
):
    """ Shut adjacent interfaces

        Args:
            device ('obj'): Device object
            link_name ('str'): Interface alias in topology
            adjacent_interfaces ('list'): List of EthernetInterface objects
            steps ('obj'): Context manager object
            num ('int'): Number of interfaces to return

        Returns:
            None

        Raises:
            SubCommandFailure

    """

    if adjacent_interfaces is None:
        adjacent_interfaces = get_interface_connected_adjacent_router_interfaces(
            device=device, link_name=link_name, num=num
        )

    for interface in adjacent_interfaces:
        adjacent_device = interface.device
        interface_name = interface.name

        with steps.start(
            "Shut adjacent interface {interface} on "
            "device {device}".format(
                interface=interface_name, device=adjacent_device.name
            ),
            continue_=True,
        ) as step:

            shut_interface(device=adjacent_device, interface=interface_name)


def unshut_interface_adjacent_interfaces(
    device, link_name, adjacent_interfaces=None, steps=Steps(), num=1
):
    """ Unshut adjacent interfaces

        Args:
            device ('obj'): Device object
            link_name ('str'): Interface alias in topology
            num ('int'): Number of interfaces to return
            adjacent_interfaces ('list'): List of EthernetInterface objects
            steps ('obj'): Context manager object

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    if adjacent_interfaces is None:
        adjacent_interfaces = get_interface_connected_adjacent_router_interfaces(
            device=device, link_name=link_name, num=num
        )
    for interface in adjacent_interfaces:

        adjacent_device = interface.device
        interface_name = interface.name

        with steps.start(
            "No shut adjacent interface {interface} on "
            "device {device}".format(
                interface=interface_name, device=adjacent_device.name
            ),
            continue_=True,
        ) as step:

            unshut_interface(device=adjacent_device, interface=interface_name)


def config_interface_carrier_delay(device, interface, delay, delay_type):
    """ Configure interface carrier delay on device

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            delay (`int`): Delay time in second
            delay_type (`str`): Delay type

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    delay_types = ["up", "down"]
    if delay_type not in delay_types:
        raise Exception(
            "'{type}' not a supported type; only support '{types}'".format(
                type=delay_type, types=delay_types
            )
        )

    try:
        device.configure(
            "interface {interface}\n"
            "carrier-delay {delay_type} {delay}".format(
                interface=interface, delay_type=delay_type, delay=delay
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure carrier delay. Error:\n{error}".format(
                error=e
            )
        )


def remove_interface_carrier_delay(device, interface):
    """ Remove interface carrier delay on device

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "interface {interface}\n"
            "no carrier-delay up\n"
            "no carrier-delay down".format(interface=interface))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to remove carrier delay on {interface}. "
            "Error:\n{e}".format(interface=interface, e=e)) from e


def remove_interface_ospf_bfd(device, interface):
    """ Remove interface ospf bfd on device

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "interface {interface}\n"
            "no ip ospf bfd".format(interface=interface))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to remove ospf bfd on {interface}. "
            "Error:\n{e}".format(interface=interface, e=e)) from e


def config_interface_mtu(device, interface, mtu_bytes):
    """ Config MTU on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            mtu_bytes (`int`): MTU bytes

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring MTU {mtu_bytes} on interface {interface}".format(
            mtu_bytes=mtu_bytes, interface=interface
        )
    )

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "mtu {mtu_bytes}".format(mtu_bytes=mtu_bytes),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure MTU on {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )


def unconfig_interface_mtu(device, interface):
    """ Remove MTU config from interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Removing MTU config on interface {interface}".format(
            interface=interface
        )
    )

    try:
        device.configure(
            ["interface {interface}".format(interface=interface), "no mtu"]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure MTU on {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )


def config_interface_ospf(device, interface, ospf_pid, area):
    """ Config OSPF on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ospf_pid (`str`): Ospf process id
            area ('int'): Ospf area code

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring OSPF on interface {interface}".format(interface=interface)
    )

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "ip ospf {pid} area {area}".format(pid=ospf_pid, area=area),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ospf. Error:\n{error}".format(error=e)
        )


def config_ip_on_interface(
    device,
    interface,
    ip_address,
    mask,
    eth_encap_type=None,
    eth_encap_val=None,
    sub_interface=None,
):
    """ Configure IP on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            ip_address (`str`): IP addressed to be configured on interface
            mask (`str`): Mask address to be used in configuration
            eth_encap_type (`str`): Encapsulation type
            eth_encap_val (`str`): Encapsulation value
            sub_interface (`str`): Subinterface to be added to interface name

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    # Get interface name
    if sub_interface:
        interface_name = interface + "." + sub_interface
    else:
        interface_name = interface

    # Build config string
    cfg_str = "interface {intf}\n".format(intf=interface_name)

    # Add encap
    if eth_encap_type and eth_encap_val:
        cfg_str += "encapsulation {encap_type} {encap_val}\n".format(
            encap_type=eth_encap_type, encap_val=eth_encap_val
        )

    cfg_str += "ip address {ip} {mask}\n".format(
        intf=interface_name, ip=ip_address, mask=mask
    )

    # Configure device
    try:
        device.configure(cfg_str)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure IP address {ip} on interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                ip=ip_address,
                interface=interface_name,
                dev=device.name,
                error=e,
            )
        )


def config_interface_subinterface_and_secondary_addresses(
    device,
    interface,
    sub_interface_num,
    ip_address,
    prefix,
    encap_type,
    start,
    end,
):
    """ Configure sub-interface and secondary addresses on device

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            sub_interface_num (`int`): Subinterface to be added to
                                 interface name
            ip_address(`str`): IP addressed to be configured on interface
            prefix(`str`): prefix to be used in configuration
            encap_type (`str`): Encapsulation type
            start (`int`): start number on ip
            end (`int`): end number on ip

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    # interface {interface}.999
    #  encapsulation dot1Q 999
    #  ip address 10.4.0.1 255.255.255.0
    #  ip address 1.1.x.1 255.255.255.0 secondary (x -> 1 to 15)
    name = interface + "." + str(sub_interface_num)
    sub_intf = Interface(device=device, name=name)
    sub_intf.eth_encap_type1 = encap_type
    sub_intf.eth_encap_val1 = sub_interface_num
    ipv4a = IPv4Addr(device=device)
    ipv4a.ipv4 = IPv4Address(ip_address.format(x=start))
    ipv4a.prefix_length = prefix
    sub_intf.add_ipv4addr(ipv4a)

    for x in range(end - start):
        ipv4b = IPv4Addr(device=device)
        ipv4b.ipv4 = IPv4Address(ip_address.format(x=x + 1))
        ipv4b.prefix_length = prefix
        ipv4b.ipv4_secondary = True
        sub_intf.add_ipv4addr(ipv4b)

    try:
        config = str(sub_intf.build_config(apply=False))
        sub_intf.build_config()
    except Exception as e:
        log.error(str(e))
        raise Exception("Failed to config \n {}".format(config))
    return config


def remove_interface_configured_service_policy(device, interface, out=None):
    """ Remove any service policy configured under interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to remove service policy from
            out (`dict`): Show run interface <interface> output

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    configs = []

    if not out:
        out = get_interface_running_config(device, interface)

    for item in out:
        if "interface" in item:
            for serv_policy in out[item]:
                if "service-policy input" in serv_policy:
                    configs.append(
                        "no {service_policy_input}".format(
                            service_policy_input=serv_policy
                        )
                    )
                elif "service-policy output" in serv_policy:
                    configs.append(
                        "no {service_policy_output}".format(
                            service_policy_output=serv_policy
                        )
                    )

    if len(configs) >= 1:
        configs.insert(0, "interface {interface}".format(interface=interface))
        try:
            device.configure(configs)
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Failed to unconfigure service policy"
                " in/out under interface {interface}. Error:\n{error}".format(
                    interface=interface, error=e
                )
            )
    else:
        log.info(
            "No configured service policy found under interface {interface}".format(
                interface=interface
            )
        )


def clear_interface_config(device, interface):
    """ Clears interface config

        Args:
            device ('obj'): device to use
            interface ('str'): interface to clear

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info("Clearing {interface} config".format(interface=interface))

    try:
        device.configure(
            "default interface {interface}".format(interface=interface)
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not default interface {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )


def configure_interface_switchport_access_vlan(device, interface, vlan):
    """ Configures switchport on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            vlan ('str'): access_vlan to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring switchport on {interface} with access_vlan = {vlan}".format(
            interface=interface, vlan=vlan
        )
    )

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "switchport access vlan {vlan}".format(vlan=vlan),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure switchport access vlan. Error:\n{error}".format(
                error=e
            )
        )


def configure_interface_directed_broadcast(device, interfaces, configure=True):
    """ Configures directed-broadcast on interface

        Args:
            device ('obj'): device to run on
            interfaces ('list'): list of interfaces to configure
            configure ('bool'): config/unconfig

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = ""

    for intf in interfaces:
        if configure:
            cmd += (
                "interface {}\n"
                "ip directed-broadcast\n"
                "exit\n".format(intf)
            )
        else:
            cmd += (
                "interface {}\n"
                "no ip directed-broadcast\n"
                "exit\n".format(intf)
            )

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure directed broadcast. Error:\n{error}".format(
                error=e
            )
        )


def configure_interface_l3_port_channel(
    target,
    port_channel,
    neighbor_address,
    neighbor_netmask,
    interfaces,
    testbed,
):
    """ Configure Port channel and lag interfaces

        Args:
            target (`str`): Target device to configure on
            port_channel (`str`): Port Channel Interface
            neighbor_address (`str`): Peer IP address
            neighbor_netmask(`str`): Peer address Net-mask
            interfaces(`List`): List of interfaces to configure
            testbed (`obj`): Testbed object

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    ip = neighbor_address + "/" + str(mask_to_int(neighbor_netmask))
    config_cmd = [
        "set chassis aggregated-devices ethernet device-count 1",
        "set interfaces {} aggregated-ether-options lacp active".format(
            port_channel
        ),
        "set interfaces {} unit 0 family inet address {}".format(
            port_channel, ip
        ),
        "set interfaces {} gigether-options 802.3ad {}".format(
            interfaces[0], port_channel
        ),
        "set interfaces {} gigether-options 802.3ad {}".format(
            interfaces[1], port_channel
        ),
        "set interfaces {} gigether-options 802.3ad {}".format(
            interfaces[2], port_channel
        ),
        "set interfaces {} gigether-options 802.3ad {}".format(
            interfaces[3], port_channel
        ),
    ]

    dev = testbed.devices[target]

    try:
        dev.configure(config_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure l3 port channel. Error:\n{error}".format(
                error=e
            )
        )

def configure_interfaces_shutdown(device, interfaces):
    """ Shutdown the listed interfaces in the given list on the device

        Args:
            List['string']: Interfaces to shutdown
            device ('obj'): Device object
    """
    config_cmd = []
    for interface in interfaces:
        config_cmd = ["int {interface}".format(interface=interface), "shutdown"]
    try:
        device.configure(config_cmd)
    except SubCommandFailure as e:
        log.error('Failed to shutdown interfaces on device {}: {}'.format(device.name, e))

def configure_interfaces_unshutdown(device, interfaces):
    """ Enable the listed interfaces in the given list on the device

        Args:
            List['string']: Interfaces to enable
            device ('obj'): Device object
    """
    config_cmd = []
    for interface in interfaces:
        config_cmd = ["int {interface}".format(interface=interface), "no shutdown"]
    try:
        device.configure(config_cmd)
    except SubCommandFailure as e:
        log.error('Failed to enable interfaces on device {}: {}'.format(device.name, e))
        

def shutdown_interface(device, member):
    """ Shutdown a bundled Interface

        Args:
            device (`obj`): Device object
            member (`str`): Bundled interface

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    config_cmd = ["int {interface}".format(interface=member), "shutdown"]

    try:
        device.configure(config_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't shut down the port channel member"
            "{intf}. Error:\n{error}".format(intf=member, error=e)
        )


def configure_interface_interfaces_on_port_channel(
    device, interface, mode, channel_group, interfaces
):
    """ Add interface <interface> to port channel

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be added to port channel
            mode (`str`): Interface mode under Port channel
            interfaces(`List`): List of interfaces to configure
            channel_group (`obj`): Channel group

        Returns:
            None
    """
    config_cmd = [
        "interface {interface}".format(interface=interface),
        "no shutdown",
        "{channel_group} mode {mode}".format(
            mode=mode, channel_group=channel_group
        ),
    ]

    if interface == interfaces[3]:
        config_cmd.append("lacp rate fast")

    try:
        device.configure(config_cmd)
        log.info(
            "Successfully added {intf} on "
            "{channel_group} in {mode} mode".format(
                intf=interface, mode=mode, channel_group=channel_group
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't add {intf} on "
            "{channel_group} in {mode} mode. Error:\n{error}".format(
                intf=interface, mode=mode, channel_group=channel_group, error=e
            )
        )


def configure_lacp_on_interface(
    device, interface, min_max_bundle, minumum_bundle=False
):
    """ Configure LACP on the interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be added to port channel
            min_max_bundle (`int`): Number of minimum/maximum bundles
            minumum_bundle (`bool`): True if configuring minimum-bundle

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    if minumum_bundle:
        config_cmd = [
            "int {interface}".format(interface=interface),
            "lacp min-bundle {max}".format(max=min_max_bundle),
        ]
        mode = "minimum"
    else:
        config_cmd = [
            "int {interface}".format(interface=interface),
            "lacp max-bundle {max}".format(max=min_max_bundle),
        ]
        mode = "maximum"

    try:
        device.configure(config_cmd)
        log.info(
            "Successfully configured {mode} number "
            "of port channel members to {max}".format(
                mode=mode, max=min_max_bundle
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure {mode} number "
            "of port channel members to {max}. Error:\n{error}".format(
                mode=mode, max=min_max_bundle, error=e
            )
        )


def default_interface(device, interfaces):
    """ configure interface carrier delay on device

        Args:
            device (`obj`): Device object
            interfaces (`list`): List of interfaces to be defaulted

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    for intf in interfaces:
        config_cmd = "default interface {}".format(intf)

        try:
            device.configure(config_cmd)
            log.info("Successfully defaulted {}".format(intf))
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Couldn't default {interface}. Error:\n{error}".format(
                    interface=intf, error=e
                )
            )


def clear_interface_interfaces(device, interfaces):
    """ clear interface configuration

        Args:
            device ('obj'): device to use
            interfaces ('list'): List of interface to be cleared

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    for interface in interfaces:
        if "." in interface:
            cmd = "no interface {interface}".format(interface=interface)
        else:
            cmd = "default interface {interface}".format(interface=interface)
            log.info(
                'Clearing interface {interface} configuration with "{cmd}"'.format(
                    interface=interface, cmd=cmd
                )
            )

        try:
            device.configure(cmd)
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Could not clear interface {interface}. Error:\n{error}".format(
                    interface=interface, error=e
                )
            )


def configure_vrf_on_interface(device, interface, vrf):
    """ Configure interface to use VRF

        Args:
            device ('obj'): Device object
            interface ('str'): Interface
            vrf ('str'): VRF name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "vrf forwarding {vrf}".format(vrf=vrf),
            ]
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure VRF {vrf} on interface "
            "{interface}. Error:\n{error}".format(
                interface=interface, vrf=vrf, error=e
            )
        )


def configure_interface_description(device, interface, description):
    """configure interface description

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            description(`str`): Description

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "description {description}".format(description=description),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure description '{description}' on "
            "interface {interface}. Error:\n{error}".format(
                description=description, interface=interface, error=e
            )
        )


def unconfigure_interface_description(device, interface):
    """unconfigure interface description

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "no description",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove description from interface "
            "{interface}. Error:\n{error}".format(interface=interface, error=e)
        )


def configure_interface_monitor_session(device, monitor_config):
    """ configure monitor session on device
        Args:
            device (`obj`): Device object
            monitor_config (`list`): list of monitor session configuration
                ex.) 
                    monitor_config = [{
                            'session_name': 1,
                            'session_type': 'erspan-source',
                            'interface': 'GigabitEthernet10',
                            'erspan_id': 10,
                            'ip_address': '192.168.1.1'
                        },
                        {
                            'session_name': 2,
                            'session_type': 'erspan-destination',
                            'interface': 'GigabitEthernet11',
                            'erspan_id': 10,
                            'ip_address': '192.168.1.1'
                        }
                    ]

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    for mc in monitor_config:
        config = []
        if "source" in mc["session_type"]:
            config.append(
                "monitor session {} type {}\n".format(
                    mc["session_name"], mc["session_type"]
                )
            )
            config.append("source interface {}\n".format(mc["interface"]))
            config.append("destination\n")
            config.append("erspan-id {}\n".format(mc["erspan_id"]))
            config.append("ip address {}\n".format(mc["ip_address"]))
            config.append("origin ip address {}\n".format(mc["ip_address"]))
        else:
            unshut_interface(device=device, interface=mc["interface"])
            config.append(
                "monitor session {} type {}\n".format(
                    mc["session_name"], mc["session_type"]
                )
            )
            config.append("destination interface {}\n".format(mc["interface"]))
            config.append("source\n")
            config.append("erspan-id {}\n".format(mc["erspan_id"]))
            config.append("ip address {}\n".format(mc["ip_address"]))

        config.append("exit\n")
        config.append("no shutdown\n")

        try:
            device.configure("".join(config))
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Could not configure monitor session. Error:\n{error}".format(
                    error=e
                )
            )


def configure_subinterfaces_for_vlan_range(device, interface, vlan_id_start, vlan_id_step,
                                           vlan_id_count, network_start, network_step,
                                           host_address_step, netmask, ospf_network_type=None):
    """ Configures multiple subinterfaces looping through vlan range

        Args:
            device ('obj'): Device to use
            interface ('str'): Physical interface to configure
            vlan_id_start ('int'): Start of vlan range
            vlan_id_step ('int'): Size of vlan range step
            vlan_id_count ('int'): How many steps for vlan range
            netmask ('str'): Netmask to configure
            network_start ('str'): Start of network
            network_step ('str'): Size of network step
            ospf_network_type ('str'): Ospf network type to configure

        Raises:
            SubCommandFailure

        Returns:
            list of configured interfaces

    """
    cmds = []
    vlan_id = vlan_id_start
    network = IPv4Address(network_start)
    interfaces = []

    for i in range(vlan_id_count):
        interfaces.append('{interface}.{vlan_id}'.format(interface=interface, vlan_id=vlan_id))
        ip_address = network + int(IPv4Address(host_address_step))

        cmds.extend(['interface {interface}.{vlan_id}'.format(interface=interface, vlan_id=vlan_id),
                     'encapsulation dot1q {vlan_id}'.format(vlan_id=vlan_id),
                     'ip address {ip_address} {netmask}'.format(ip_address=ip_address, netmask=netmask)])

        if ospf_network_type:
            cmds.append('ip ospf network {ospf_network_type}'.format(ospf_network_type=ospf_network_type))

        cmds.append('exit')

        vlan_id += vlan_id_step
        network += int(IPv4Address(network_step))

    device.configure(cmds)

    return interfaces
