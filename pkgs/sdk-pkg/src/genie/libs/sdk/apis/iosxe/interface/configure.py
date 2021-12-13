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

def config_enable_ip_routing(device):
    """ Enable IP Routing

        Args:
            device (`obj`): Device object
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info("Configuring ip routing")

    try:
        device.configure("ip routing")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configure ip routing"
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
            "Failed to config negotiation auto on interface {interface}. Error:"
            "\n{error}".format(interface=interface, error=e
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
            "Failed to unconfig negotiation auto on interface {interface}. "
            "Error:\n{error}".format(interface=interface, error=e
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
            "Could not shut interface {intf} on device {dev}. Error:\n{error}"\
                .format(intf=interface, dev=device.name, error=e
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
            "Could not unshut interface {interface} on device {dev}. Error:\n"
            "{error}".format(interface=interface, dev=device.name, error=e
                             )
        )


def config_mpls_on_device(device, loopback_intf):
    """ configure mpls on device
        Args:
            device (`obj`): Device object
            loopback_intf (`str`): Interface name
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info("Configuring mpls ip on device")

    try:
        device.configure(
            [
                "mpls ip",
                "mpls label protocol ldp",
                "mpls ldp router-id {loopback_intf} force".format(
                                       loopback_intf=loopback_intf),
                "mpls ldp graceful-restart"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Basic mpls configuration failed. Error: {e}".format(e=e)
        )

def config_mpls_on_device(device, loopback_intf):
    """ configure mpls on device
        Args:
            device (`obj`): Device object
            loopback_intf (`str`): Interface name
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info("Configuring mpls ip on device")

    try:
        device.configure(
            [
                "mpls ip",
                "mpls label protocol ldp",
                "mpls ldp router-id {loopback_intf} force".format(
                                       loopback_intf=loopback_intf),
                "mpls ldp graceful-restart"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Basic mpls configuration failed. Error: {e}".format(e=e)
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
        adjacent_interfaces = \
            get_interface_connected_adjacent_router_interfaces(
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
        adjacent_interfaces = \
            get_interface_connected_adjacent_router_interfaces(
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


def config_interface_ospfv3(device, interface, ospfv3_pid, area):
    """config OSPF on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ospfv3_pid (`str`): Ospfv3 process id
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
                "ospfv3 {pid} ipv6 area {area}".format(pid=ospfv3_pid,
                                                       area=area),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ospfv3 {pid}. Error:\n{error}"
            .format(pid=ospfv3_pid, error=e)
        )


def config_ip_on_interface(
    device,
    interface,
    ip_address=None,
    mask=None,
    ipv6_address=None,
    eth_encap_type=None,
    eth_encap_val=None,
    sub_interface=None,
    disable_switchport=False
):
    """ Configure IP on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            ip_address (`str`): IP addressed to be configured on interface
            mask (`str`): Mask address to be used in configuration
            ipv6_address (`str`): IPv6 address with subnet mask
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

    if disable_switchport:
        cfg_str+="no switchport \n"

    if ip_address and mask:
        cfg_str += "ip address {ip} {mask}\n".format(
             ip=ip_address, mask=mask
        )

    # Add ipv6 address configuration
    if ipv6_address:
        cfg_str += "ipv6 enable\n" \
                   "ipv6 address {ipv6}\n".format(
            ipv6=ipv6_address
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
            "No configured service policy found under interface {interface}"\
                .format(interface=interface
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

def configure_interface_switchport_access_vlan(device, interface, vlan,mode=None):
    """ Configures switchport on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            vlan ('str'): access_vlan to configure
            mode ('str',optional) Switchport mode (i.e access)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring switchport on {interface} with access_vlan = {vlan}"\
            .format(interface=interface, vlan=vlan
        )
    )

    config_list = []
    config_list.append("interface {interface}".format(interface=interface))
    if mode:
        config_list.append("switchport mode {mode}".format(mode=mode))
    config_list.append("switchport access vlan {vlan}".format(vlan=vlan))

    try:
        device.configure(config_list)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure switchport access vlan. Error:\n{error}"\
                .format(error=e
            )
        )


def unconfigure_interface_switchport_access_vlan(device, interface, vlan):
    """ Unconfigures switchport on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to unconfigure
            vlan ('str'): access_vlan to unconfigure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f'Unconfiguring switchport on {interface} with access_vlan {vlan}')

    try:
        device.configure([
                f'interface {interface}',
                f'no switchport access vlan {vlan}',
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not unconfigure switchport access vlan on {vlan}, '
            f'Error:\n{e}'
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

        Raises:
            SubCommandFailure
    """
    config_cmd = []
    for interface in interfaces:
        config_cmd += ["int {interface}".format(interface=interface),
                       "shutdown"]
    try:
        device.configure(config_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Failed to shutdown interfaces on device {}: {}'.format(device.name, e
            )
        )


def configure_interfaces_unshutdown(device, interfaces):
    """ Enable the listed interfaces in the given list on the device

        Args:
            List['string']: Interfaces to enable
            device ('obj'): Device object

        Raises:
            SubCommandFailure
    """
    config_cmd = []
    for interface in interfaces:
        config_cmd += ["int {interface}".format(interface=interface),
                       "no shutdown"]
    try:
        device.configure(config_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Failed to enable interfaces on device {}: {}'.format(device.name, e
            )
        )

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
        "channel-group {channel_group} mode {mode}".format(
            mode=mode, channel_group=channel_group
        ),
    ]

    if len(interfaces) > 2:
        if interface == interfaces[3]:
            config_cmd.append("lacp rate fast")
    else:
        pass

    try:
        device.configure(config_cmd)
        log.info(
            "Successfully added {intf} on "
            "channel-group {channel_group} in {mode} mode".format(
                intf=interface, mode=mode, channel_group=channel_group
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't add {intf} on "
            "channel-group {channel_group} in {mode} mode. Error:\n{error}"\
                .format(intf=interface, mode=mode, channel_group=channel_group,
                        error=e
            )
        )


def configure_interfaces_on_port_channel(
    device, interfaces, mode, channel_group,
    channel_protocol=None, disable_switchport=False,
    ):
    """ Add interface <interface> to port channel

        Args:
            device (`obj`): Device object
            mode (`str`): Interface mode under Port channel
            interfaces(`List`): List of interfaces to configure
            channel_group (`obj`): Channel group
            channel_protocol (`str`): protocol used for port-channel
            disable_switchport('str'): disable switchport
        Returns:
            None
    """

    for intf in interfaces:
        config_cmd="interface {interface} \n".format(interface=intf)
        if disable_switchport:
            config_cmd+="no switchport \n"
        config_cmd+="no shutdown \n"
        if channel_protocol:
            config_cmd+="channel-protocol {channel_protocol} \n".format(
                                      channel_protocol=channel_protocol)
        config_cmd+="channel-group {channel_group} mode {mode} \n".format(
                                  channel_group=channel_group, mode=mode)
        try:
            device.configure(config_cmd)
            log.info(
                "Successfully added {intf} on "
                "channel-group {channel_group} in {mode} mode".format(
                    intf=intf, mode=mode, channel_group=channel_group
                )
            )
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Couldn't add {intf} on "
                "channel-group {channel_group} in {mode} mode. Error:\n{error}"\
                    .format(intf=intf, mode=mode, channel_group=channel_group,
                            error=e
                )
            )


def configure_interface_switchport_trunk(device, interfaces, vlan_id=None):

    """ configure switchport mode trunk to the interface

        Args:
            device (`obj`): Device object
            interface (`list`): list of Interface to be added to port channel
            vlan (`str`): vlan to be added to the port
        Returns:
            None
    """
    log.info(
        "Configuring switchport interface on {interfaces}".format(
            interfaces=interfaces
        )
    )

    try:
        for intf in interfaces:
            confg="interface {intf} \n".format(intf=intf)
            confg+="switchport \n"
            confg+="switchport mode trunk \n"
            confg+="switchport trunk allowed vlan {vlan_id}".format(
                                                    vlan_id=vlan_id)
            device.configure(confg)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure switchport on {interface}. Error:\n{error}"\
                .format(interfaces=interfaces, error=e
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
    """ configure default interface on device

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


def clear_interface_interfaces(device, interfaces, pseudowire=None):
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
            if pseudowire:
                cmd = "no interface {interface}".format(interface=interface)
            else:
                cmd = "default interface {interface}".format(interface=interface)
                log.info(
                    'Clearing interface {interface} configuration '
                    'with "{cmd}"'.format(
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

def remove_virtual_interface(device,interfaces):

    """ Remove virtual interface created

        Args:
            device ('obj'): device to use
            interfaces ('list'): List of interface to be cleared

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    for interface in interfaces:
        cmd = "no interface {interface}".format(interface=interface)

        try:
            device.configure(cmd)
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Could not remove interface {interface}. Error:\n{error}"\
                    .format(interface=interface, error=e
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

        if 'description' in mc:
            config.append("description {}\n".format(mc["description"]))
        if 'source_vlan' in mc:
            config.append("source vlan {}\n".format(mc["source_vlan"]))
        if 'mtu' in mc:
            config.append("mtu {}\n".format(mc["mtu"]))
        if 'vrf' in mc:
            config.append("vrf {}\n".format(mc["vrf"]))
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


def unconfigure_interface_monitor_session(device, session_name, session_type):
    """ configure monitor session on device
        Args:
            device (`obj`): Device object
            session_name (`str`): session_name
            session_type (`str`): session_type

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "no monitor session {session_name} type {session_type}".format(
                session_name=session_name,
                session_type=session_type))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure monitor session. Error:\n{error}".format(
                error=e
            )
        )
            

def configure_subinterfaces_for_vlan_range(
    device, interface, vlan_id_start, vlan_id_step, vlan_id_count,
    network_start, network_step,host_address_step, netmask,
    ospf_network_type=None):
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
        interfaces.append('{interface}.{vlan_id}'\
            .format(interface=interface, vlan_id=vlan_id))
        ip_address = network + int(IPv4Address(host_address_step))

        cmds.extend([
            'interface {interface}.{vlan_id}'.format(interface=interface,
                                                     vlan_id=vlan_id),
            'encapsulation dot1q {vlan_id}'.format(vlan_id=vlan_id),
            'ip address {ip_address} {netmask}'.format(ip_address=ip_address,
                                                       netmask=netmask)])

        if ospf_network_type:
            cmds.append('ip ospf network {ospf_network_type}'\
                .format(ospf_network_type=ospf_network_type))

        cmds.append('exit')

        vlan_id += vlan_id_step
        network += int(IPv4Address(network_step))

    device.configure(cmds)

    return interfaces


def configure_interface_for_authentication(device, config_list,
                                           auth_type='dot1x'):
    """
    Interface configuration for Dot1x
    Args:
        device(obj): Device object
        config_list(list): List of configurations to configure
        auth_type(str): Authentication method type(dot1x/mab)
    Returns:
        None if configuration is failed
        config_list if configuration is succeded
    Raises:
        SubCommandFailure
    """

    try:
        device.configure(config_list)
        return config_list
    except SubCommandFailure as error:
        raise SubCommandFailure(
            "Could not configure interface for {a} on device {d}. Error {e}"\
                .format(a=auth_type, d=device, e=error
            )
        )


def configure_interface_for_dot1x(
    device, interface, role='authenticator', order='dot1x', priority='dot1x',
    port_control='auto', additional_config=None):
    """
    Interface configuration for Dot1x
    Args:
        device (obj): Device object
        interface (str): Interface to configure
        role (str): Device role(authenticator/supplicant)
        order (str): Add an authentication method to the order list
        priority (str): Add an authentication method to the priority list
        port_control (str): Set the port-control value(auto, force-authorized, force-unauthorized)
        additional_config (list): List of configurations to be performed additionally
    Returns:
        None
    Raises:
        SubCommandFailure

    ex.)
        configures below cli commands on interface if role is authenticator:
            'interface GigabitEthernet1/0/2',
            'authentication open',
            'authentication order dot1x,
            'authentication priority dot1x,
            'authentication port-control auto,
            'dot1x pae authenticator'
        configures below cli commands on interface if role is supplicant:
            'interface GigabitEthernet1/0/2',
            'dot1x pae supplicant'
    """

    if role == 'authenticator':
        default_config_list = [
            'interface {}'.format(interface),
            'authentication open',
            'authentication order {o}'.format(o=order),
            'authentication priority {p}'.format(p=priority),
            'authentication port-control {p}'.format(p=port_control),
            'dot1x pae authenticator']
    elif role == 'supplicant':
        default_config_list = ['interface {}'.format(interface),
                               'dot1x pae supplicant']

    config_list = \
        default_config_list+additional_config if additional_config is not None \
            else default_config_list

    configure_interface_for_authentication(device, config_list,
                                           auth_type='dot1x')


def configure_interface_for_mab(
    device, interface, role='authenticator', order='mab', priority='mab',
    port_control='auto', additional_config=None):
    """
    Interface configuration for Mac authentication bypass
    Args:
        device (obj): Device object
        interface (str): Interface to configure
        role (str): Device role(authenticator/supplicant)
        order (str): Add an authentication method to the order list
        priority (str): Add an authentication method to the priority list
        port_control (str): Set the port-control value(auto, force-authorized, force-unauthorized)
        additional_config (list): List of configurations to be performed additionally
    Returns:
        None
    Raises:
        SubCommandFailure

    ex.)
        configures below cli commands on interface if role is authenticator:
            'interface GigabitEthernet1/0/2',
            'authentication open',
            'authentication order mab,
            'authentication priority mab,
            'authentication port-control auto',
            'dot1x pae authenticator',
            'mab'
        configures below cli commands on interface if role is supplicant:
            'interface GigabitEthernet1/0/2',
            'dot1x pae supplicant'
    """

    if role == 'authenticator':
        default_config_list = [
            'interface {}'.format(interface),
            'authentication open',
            'authentication order {o}'.format(o=order),
            'authentication priority {p}'.format(p=priority),
            'authentication port-control {p}'.format(p=port_control),
            'dot1x pae authenticator',
            'mab']
    elif role == 'supplicant':
        default_config_list = ['interface {}'.format(interface),
                               'dot1x pae supplicant']

    config_list = \
        default_config_list+additional_config if additional_config is not None \
            else default_config_list

    configure_interface_for_authentication(device, config_list, auth_type='mab')


def unconfigure_interface_for_dot1x(device, interface, role='authenticator',
                                    additional_config=None):
    """
    Interface un-configuration for Dot1x
    Args:
        device (obj): Device object
        interface (str): Interface to configure
        role (str): Device role(authenticator/supplicant)
        additional_config (list): List of configurations to be performed additionally
    Returns:
        None
    Raises:
        SubCommandFailure

    ex.)
        configures below cli commands on interface if role is authenticator:
            'interface GigabitEthernet1/0/2',
            'no authentication open',
            'no authentication order',
            'no authentication priority',
            'no authentication port-control',
            'no dot1x pae'
        configures below cli commands on interface if role is supplicant:
            'interface GigabitEthernet1/0/2',
            'no dot1x pae'
    """

    if role == 'authenticator':
        default_config_list = ['interface {}'.format(interface),
                               'no authentication open',
                               'no authentication order',
                               'no authentication priority',
                               'no authentication port-control',
                               'no dot1x pae',
                               ]
    elif role == 'supplicant':
        default_config_list = ['interface {}'.format(interface),
                               'no dot1x pae',
                               ]

    config_list = default_config_list + additional_config \
        if additional_config is not None else default_config_list

    configure_interface_for_authentication(device, config_list,
                                           auth_type='dot1x')


def unconfigure_interface_for_mab(device, interface, role='authenticator',
                                  additional_config=None):
    """
    Interface un-configuration for Mac authentication bypass
    Args:
        device (obj): Device object
        interface (str): Interface to configure
        role (str): Device role(authenticator/supplicant)
        additional_config (list): List of configurations to be performed additionally
    Returns:
        None
    Raises:
        SubCommandFailure

    ex.)
        configures below cli commands on interface if role is authenticator:
            'interface GigabitEthernet1/0/2',
            'no authentication open',
            'no authentication order',
            'no authentication priority',
            'no authentication port-control',
            'no dot1x pae',
            'no mab'
        configures below cli commands on interface if role is supplicant:
            'interface GigabitEthernet1/0/2',
            'no dot1x pae'
    """

    if role == 'authenticator':
        default_config_list = ['interface {}'.format(interface),
                               'no authentication open',
                               'no authentication order',
                               'no authentication priority',
                               'no authentication port-control',
                               'no mab',
                               'no dot1x pae']
    elif role == 'supplicant':
        default_config_list = ['interface {}'.format(interface),
                               'no dot1x pae']

    config_list = \
        default_config_list+additional_config if additional_config is not None \
            else default_config_list

    configure_interface_for_authentication(device, config_list, auth_type='mab')


def configure_ipv4_dhcp_relay_helper(device, interface, ip_address):
    """ Configure helper IP on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            ip_address (`str`): helper IP address to be configured on interface

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd_1 = "interface {intf}".format(intf=interface)
    cmd_2 = "ip helper-address {ip}".format(ip=ip_address)

    # Configure device
    try:
        device.configure([cmd_1, cmd_2])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure helper IP address {ip} on interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                ip=ip_address,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )

def attach_ipv6_raguard_policy_to_interface(device, interface, policy_name):
    """ Attach IPv6 RA Guard Policy to an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to attach policy
            policy_name (`str`): Policy name to be attached to interface

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd_1 = "interface {intf}".format(intf=interface)
    cmd_2 = "ipv6 nd raguard attach-policy {policy_name}"\
        .format(policy_name=policy_name)

    # Configure device
    try:
        device.configure([cmd_1, cmd_2])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to attach IPv6 RA Guard policy {policy_name} on interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                policy_name=policy_name,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )

def remove_interface_ip(device, interface):
    """ Remove ip on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Removing ip on interface {interface}".format(
            interface=interface
        )
    )
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "no ip address",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfig ip address on interface {interface}. "
            "Error:\n{error}".format(interface=interface, error=e
            )
        )


def configure_ipv6_dhcp_relay(device, interface, dest_ipv6, vlan):
    """ Configure IPv6 DHCP Relay
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured
            dest_ipv6 ('str'): IPv6 destination address
            vlan ('int'): vlan number
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring IPv6 DHCP Relay
    """
    log.info(
        "Configuring IPv6 DHCP Relay on int={int}, for dest_ipv6={dest_ipv6} "
        "and vlan={vlan}".format(int=int,dest_ipv6=dest_ipv6,vlan=vlan)
    )

    try:
       device.configure(
            [
            "interface {interface}\n".format(interface=interface),
            "ipv6 dhcp relay destination {dest_ipv6} {vlan}"\
                .format(dest_ipv6=dest_ipv6,vlan=vlan)
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure IPv6 DHCP Relay on int={int}, "
            "for dest_ipv6={dest_ipv6} and vlan={vlan} ".format(
                int=int,dest_ipv6=dest_ipv6,vlan=vlan
            )
        )

def configure_ipv6_nd(device, interface, lifetime, pref_lifetime, router_pref,
                      ra_lifetime,ra_interval):
    """ Configure IPv6 ND parameters
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured
            lifetime ('int') : Valid Lifetime in secs
            pref_lifetime ('int') : Preferred Lifetime in secs
            router_pref ('str') : default router preference
            ra_lifetime ('int') : IPv6 Router Advertisement Lifetime
            ra_interval ('int') : IPv6 Router Advertisement Interval

        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring IPv6 DHCP ND parameters
    """
    log.info(
        "Configuring IPv6 DHCP ND parameters on int={int} "
        .format(int=interface)
    )

    try:
       device.configure(
            [
            "interface {interface}\n".format(interface=interface),
            "ipv6 nd prefix default {} {}".format(lifetime, pref_lifetime),
            "ipv6 nd router-preference {}".format(router_pref),
            "ipv6 nd ra lifetime {}".format(ra_lifetime),
            "ipv6 nd ra interval {}".format(ra_interval)
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure IPv6 DHCP ND parameters on int={int}"\
                .format(int=interface)
        )

def attach_dhcpv6_guard_policy_to_interface(device, interface, policy_name):
    """ Attach DHCPv6 Guard Policy to an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to attach policy
            policy_name (`str`): Policy name to be attached to interface

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = ["interface {intf}".format(intf=interface),
           "ipv6 dhcp guard attach-policy {policy_name}"
           .format(policy_name=policy_name)]

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        log.error(
            "Failed to attach DHCPv6 Guard policy {policy_name} on interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                policy_name=policy_name,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )
        raise

def enable_ipv6_dhcp_server(device, interface, pool_name):
    """ Enable IPv6 DHCP server on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to enable IPv6 DHCP server
            pool_name (`str`): Pool name

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = ["interface {intf}".format(intf=interface),
           "ipv6 dhcp server {pool_name} rapid-commit"
           .format(pool_name=pool_name)]

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        log.error(
            "Failed to enable IPv6 DHCP server for {pool_name} on interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                pool_name=pool_name,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )
        raise

def detach_dhcpv6_guard_policy_to_interface(device, interface, policy_name):
    """ Detach DHCPv6 Guard Policy from an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to attach policy
            policy_name (`str`): Policy name to be attached to interface

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = ["interface {intf}".format(intf=interface),
           "no ipv6 dhcp guard attach-policy {policy_name}"
           .format(policy_name=policy_name)]

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        log.error(
            "Failed to detach DHCPv6 Guard policy {policy_name} on interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                policy_name=policy_name,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )
        raise


def detach_ipv6_raguard_policy_to_interface(device,interface,policy_name):
    """ Detach IPv6 RA Guard Policy from an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to detach policy
            policy_name (`str`): Policy name to be attached to interface

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = ["interface {intf}".format(intf=interface),
           "no ipv6 nd raguard attach-policy {policy_name}"
           .format(policy_name=policy_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(
            "Failed to detach IPv6 RA Guard policy {policy_name} on interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                policy_name=policy_name,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )
        raise

def attach_ipv6_raguard_policy_to_vlan(device, vlan, policy_name):
    """ Attach IPv6 RA Guard Policy to a vlan

        Args:
            device (`obj`): Device object
            vlan (`str`): vlan to attach policy
            policy_name (`str`): Policy name to be attached to interface

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = ["vlan configuration {vlan}".format(vlan=vlan),
           "ipv6 nd raguard attach-policy {policy_name}"
           .format(policy_name=policy_name)]

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        log.error(
            "Failed to attach IPv6 RA Guard policy {policy_name} on vlan "
            "{vlan} on device {dev}. Error:\n{error}".format(
                policy_name=policy_name,
                vlan=vlan,
                dev=device.name,
                error=e,
            )
        )
        raise

def detach_ipv6_raguard_policy_to_vlan(device, vlan, policy_name):
    """ Detach IPv6 RA Guard Policy from Vlan

        Args:
            device (`obj`): Device object
            vlan (`str`): vlan to detach policy
            policy_name (`str`): Policy name to be attached to interface

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = ["vlan configuration {vlan}".format(vlan=vlan),
           "no ipv6 nd raguard attach-policy {policy_name}"
           .format(policy_name=policy_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(
            "Failed to detach IPv6 RA Guard policy {policy_name} on vlan "
            "{vlan} on device {dev}. Error:\n{error}".format(
                policy_name=policy_name,
                vlan=vlan,
                dev=device.name,
                error=e,
            )
        )
        raise


def remove_channel_group_from_interface(device, interface, channel_group, mode):
    """ Remove channel group from an Interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface on which the channel group command is to be applied
            channel_group (`str`): Channel group number
            mode (`str`): Channel group mode

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "no channel-group {channel_group} mode {mode}".format(
                    channel_group=channel_group, mode=mode)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't remove channel group {channel_group} "
            "from interface {interface}. Error:\n{error}".format(
                channel_group=channel_group, interface=interface, error=e)
        )


def remove_port_channel_interface(device, port_channel):
    """ Remove port channel interface

        Args:
            device (`obj`): Device object
            port_channel (`str`): Port channel to be removed

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure("no interface port-channel{port_channel}".format(
            port_channel=port_channel))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't remove port channel {port_channel} from device. "
            "Error:\n{error}".format(port_channel=port_channel, error=e)
        )


def config_edge_trunk_on_interface(device, interface):
    """ Configure spanning portf edge trunk on Interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface on which the edge trunk config to be applied

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "spanning portf edge trunk"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure spanning portf edge trunk "
            "on interface {interface}. Error:\n{error}".format(
                interface=interface, error=e)
        )


def configure_interface_ospfv3(device, interface, ospf_pid, area):
    """ Config OSPFV3 on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ospf_pid (`str`): OspfV3 process id
            area ('int'): Ospf area code
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring OSPFV3 on interface {interface}"\
            .format(interface=interface)
    )

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "ospfv3 {pid} ipv6 area {area}".format(pid=ospf_pid, area=area),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ospfv3. Error:\n{error}".format(error=e)
        )


def attach_dhcpv6_guard_policy_to_vlan(device, vlan, policy_name):
    """ Attach DHCPv6 Guard Policy to a vlan

        Args:
            device (`obj`): Device object
            vlan (`str`): vlan to attach policy
            policy_name (`str`): Policy name to be attached to interface

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = ["vlan configuration {vlan}".format(vlan=vlan),
           "ipv6 dhcp guard attach-policy {policy_name}".format(policy_name=policy_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(
            "Failed to attach DHCPv6 Guard policy {policy_name} on vlan "
            "{vlan} on device {dev}. Error:\n{error}".format(
                policy_name=policy_name,
                vlan=vlan,
                dev=device.name,
                error=e,
            )
        )
        raise


def detach_dhcpv6_guard_policy_vlan(device, vlan, policy_name):
    """ Detach DHCPv6 Guard Policy from a vlan

        Args:
            device (`obj`): Device object
            vlan (`str`): vlan to attach policy
            policy_name (`str`): Policy name to be attached to interface

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = ["vlan configuration {vlan}".format(vlan=vlan),
           "no ipv6 dhcp guard attach-policy {policy_name}".format(
         policy_name=policy_name
    )]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(
            "Failed to detach DHCPv6 Guard policy {policy_name} from vlan "
            "{vlan} on device {dev}. Error:\n{error}".format(
                policy_name=policy_name,
                vlan=vlan,
                dev=device.name,
                error=e,
            )
        )
        raise


def attach_device_tracking_policy_to_interface(device, policy_name, interface):
    """ Attach Device Tracking Policy to a interface

        Args:
            device (`obj`): Device object
            policy_name (`str`): Policy name to be attached to interface
            interface (`str`): interface to attach policy

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = ["interface {interface}".format(interface=interface),
           "device-tracking attach-policy {policy_name}".format(
         policy_name=policy_name
    )]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(
            "Failed to attach Device Tracking policy {policy_name} on interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                policy_name=policy_name,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )
        raise


def configure_authentication_parameters_interface(device, interface):
    """ Configure authentication parameters on interface

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure the authentication parameters

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = ["interface {interface}".format(interface=interface),
           "authentication port-control auto",
           "authentication periodic",
           "authentication timer reauthenticate server"]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(
            "Failed to Configure authentication parameters on interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e,
            )
        )
        raise


def configure_interface_switchport_mode(device, interface, mode):
    """ Configures switchport mode on interface
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            mode ('str')      : interface mode
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring switchport mode on {interface} with mode = {mode}".format(
            interface=interface, mode=mode
        )
    )

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "switchport mode {mode}".format(mode=mode),
            ]
        )
    except SubCommandFailure:
        log.error('Failed to configure switchport mode on the interface')
        raise


def configure_interface_no_switchport(device, interface):
    """ Configures no switchport on interface
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring no switchport on {interface}".format(
            interface=interface
        )
    )

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "no switchport",
            ]
        )
    except SubCommandFailure:
        log.error('Failed to configure no switchport on the interface')
        raise


def unconfigure_vlan_interface(device, vlan):
    """ Unconfigure vlan from device

        Args:
            device (`obj`): Device object
            vlan (`str`): vlan to be unconfigured

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = "no interface {vlan}".format(vlan=vlan)

    # Configure device
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to Unconfigure Vlan {vlan} from device"
            "on device {dev}. Error:\n{error}".format(
                vlan=vlan,
                dev=device.name,
                error=e,
            )
        )


def configure_interface_template(device, interface_list=[], template_name="sample-template"):
    """ Configure Template on a list of interfaces
    interface GigabitEthernet1/0/1
      source template sample-template

    Args:
        device ('obj'): Device object
        template_name ('str'): Template name
        interface_list ('list'): List of Interface names - can directly pass in device.interfaces from testbed yaml

    Returns:
        None

    Raises:
        SubCommandFailure
    """
    for interface in interface_list:
        try:
            device.configure(
                '''
                interface {interface}
                  source template {template_name}
                '''.format(interface=interface, template_name=template_name))

        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Could not configure template on {interface}. Error:\n{error}".format(
                    interface=interface, error=e
                )
        )


def unconfigure_interface_template(device, interface_list=[], template_name="test"):
    """ UnConfigures Template on a list of interfaces
    interface GigabitEthernet1/0/1
      no source template sample-template

        Args:
            device ('obj'): Device object
            template_name ('str'): Template name
            interface_list ('list'): List of Interface names - can directly pass in device.interfaces from testbed yaml

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    for interface in interface_list:
        try:
            device.configure(
                '''
                interface {interface}
                  no source template {template_name}
                '''.format(interface=interface, template_name=template_name))

        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Could not unconfigure template on {interface}. Error:\n{error}".format(
                    interface=interface, error=e
                )
                )


def configure_interface_switchport_voice_vlan(device, interface, vlan):
    """ Configures switchport on interface
    Args:
        device ('obj'): device to use
        interface ('str'): interface to configure
        vlan ('str'): voice_vlan to configure
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    try:
        device.configure(
            [
            "interface {interface}".format(interface=interface),
            "switchport voice vlan {vlan}".format(vlan=vlan),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure switchport trunk vlan. Error:\n{error}".format(
                error=e
            )
        )


def configure_interface_switchport_trunk_vlan(device, interface, trunk_mode, vlan):
    """ Configures switchport trunk on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            trunk_mode('str'): trunk mode to configure
            vlan ('str'): trunk_vlan to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring switchport on {interface} with trunk_vlan = {vlan}".format(
            interface=interface, vlan=vlan
        )
    )
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "switchport trunk {trunk_mode} vlan {vlan}".format(trunk_mode=trunk_mode, vlan=vlan),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure switchport voice vlan. Error:\n{error}".format(
            error=e)
        )


def configure_ip_on_tunnel_interface(
    device,
    interface,
    ip_address,
    mask,
    tunnel_source,
    tunnel_destination,
    keepalive_timer = 10,
    ip_mtu = None,
    ipv6_address=None
):
    """ Configure tunnel interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            ip_address (`str`): IP addressed to be configured on interface
            mask (`str`): Mask address to be used in configuration
            tunnel_source (`str`): tunnel source address
            tunnel_destination (`str`): tunnel destination address
            keepalive_timer ('int',optional): tunnel keepalive timer,default value is 10
            ip_mtu ('str',optional): tunnel mtu, default value is None
            ipv6_address (`str`,optional): IPv6 address with subnet mask,default value is None


        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("interface {intf}".format(intf=interface))
    configs.append("ip address {ip} {mask}".format(ip=ip_address,mask=mask))
    configs.append("tunnel source {ip}".format(ip=tunnel_source))
    configs.append("tunnel destination {ip}".format(ip=tunnel_destination))
    configs.append("keepalive {timer}".format(timer=keepalive_timer))

    if ip_mtu:
        configs.append("ip mtu {mtu}".format(mtu=ip_mtu))

    if ipv6_address:
        configs.append("tunnel mode gre ipv6")
        configs.append("ipv6 address {ipv6}".format(ipv6=ipv6_address))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure IP address {ip} on Tunnel interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                ip=ip_address,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )


def unconfigure_tunnel_interface(device, interface):
    """ Unconfigure tunnel interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
        Returns:
            None

        Raises:
            SubCommandFailure
    """

    configs = "no interface {intf}".format(intf=interface)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure tunnel on interface {interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e,
            )
        )


def configure_ip_mtu(device, intf, mtu):
    """ Configuring ip mtu on  device

        Args:
            device ('str'): Device str
            intf ('str') : interface to configure
            mtu ('str'): mtu size to configure
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
             f"interface {intf}",
             f"ip mtu {mtu}",
            ]

        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ip mtu  on interface. Error:\n{e}"
        )

def unconfigure_ip_mtu(device, intf, mtu):
    """ Unconfiguring ip mtu on  device

        Args:
            device ('str'): Device str
            intf ('str') : interface to configure
            mtu ('str'): mtu size to configure
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
             f"interface {intf}",
             f"no ip mtu {mtu}",
            ]

        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ip mtu  on interface. Error:\n{e}"
        )


def configure_switchport_trunk(device, intf_list):
    """ Switch port mode trunk interface configuration
        Args:
            device (`obj`): Device object
            intf_list ('list'): List of interfaces to be configured as trunks
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    for intf in intf_list:
        configs.append("interface {intf}".format(intf=intf))
        configs.append("no shutdown")
        configs.append("switchport")
        configs.append("switchport mode trunk")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure switchport trunk on {intf}".format(intf=intf)
        )


def configure_svi(device, vlan, ipaddr, mask):
    """ Vlan SVI configuration
        Args:
            device (`obj`): Device object
            vlan ('int'): VLAN id for SVI
            ipaddr ('str'): IP address for SVI
            mask ('str'): Subnet mask for ip address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("interface vlan {vlan}".format(vlan=vlan))
    configs.append("no shutdown")
    configs.append("ip address {ipaddr} {mask}".format(ipaddr=ipaddr,mask=mask))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure SVI, VLAN {vlan} with the provided parameters".format(vlan=vlan)
        )


def configure_eapol_dest_address_interface(device, interface, dest_address):
    """ Configures EAPOL Destination Address on interface

    Args:
        device ('obj'): device to use
        interface ('str'): interface to be configured
        dest_address ('str'): destination address to be configured

    Returns:
        None

    Raises:
        SubCommandFailure
    """

    try:
        device.configure(
            [
            "interface {interface}".format(interface=interface),
            "eapol destination-address {dest_address}".format(dest_address=dest_address),
            ]
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure EAPOL Destination Address on interface. Error:\n{error}".format(
            error=e)
        )


def unconfigure_eapol_dest_address_interface(device, interface, dest_address):
    """ Unconfigures EAPOL Destination Address on interface

    Args:
        device ('obj'): device to use
        interface ('str'): interface to be unconfigured
        dest_address ('str'): destination address to be unconfigured

    Returns:
        None

    Raises:
        SubCommandFailure
    """

    try:
        device.configure(
            [
            "interface {interface}".format(interface=interface),
            "no eapol destination-address {dest_address}".format(dest_address=dest_address),
            ]
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure EAPOL Destination Address on interface. Error:\n{error}".format(
            error=e)
        )


def configure_eapol_eth_type_interface(device, interface, eth_type):
    """ Configures EAPOL Ethernet Type on interface

    Args:
        device ('obj'): device to use
        interface ('str'): interface to be configured
        eth_type ('str'): eth_type to be configured

    Returns:
        None

    Raises:
        SubCommandFailure
    """

    try:
        device.configure(
            [
            "interface {interface}".format(interface=interface),
            "eapol eth-type {eth_type}".format(eth_type=eth_type),
            ]
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure EAPOL Ethernet Type on interface. Error:\n{error}".format(
            error=e)
        )


def unconfigure_eapol_eth_type_interface(device, interface, eth_type):
    """ Unconfigures EAPOL Ethernet Type on interface

    Args:
        device ('obj'): device to use
        interface ('str'): interface to be unconfigured
        eth_type ('str'): eth_type to be unconfigured

    Returns:
        None

    Raises:
        SubCommandFailure
    """

    try:
        device.configure(
            [
            "interface {interface}".format(interface=interface),
            "no eapol eth-type {eth_type}".format(eth_type=eth_type),
            ]
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure EAPOL Ethernet Type on interface. Error:\n{error}".format(
            error=e)
        )


def configure_interface_mac_address(device,interface,mac):
    """ Configure static mac address on interface
    Args:
        device (`obj`): Device object
        interface ('str'): Interface to configure
        mac ('str'): Mac address with format H.H.H
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    configs = []
    configs.append("interface {interface}".format(interface=interface))
    configs.append("mac-address {mac}".format(mac=mac))

    try:
        device.configure(configs)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure mac address on interface"
        )


def unconfigure_interface_mac_address(device,interface):
    """ Unconfigure static mac address on interface
    Args:
        device (`obj`): Device object
        interface ('str'): Interface to unconfigure mac
    Return:
        None
    Raise:
        SubCommandFailure: Failed unconfiguring
    """
    configs = []
    configs.append("interface {interface}".format(interface=interface))
    configs.append("no mac-address")

    try:
        device.configure(configs)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure mac address on interface"
        )

def unconfigure_svi(device, vlan):
    """ Vlan SVI configuration removal
        Args:
            device (`obj`): Device object
            vlan ('list'): Vlan value
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("no interface vlan {vlan}".format(vlan=vlan))
    configs.append("no vlan {vlan}".format(vlan=vlan))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure SVI, VLAN {vlan}".format(vlan=vlan)
        )

def configure_interface_span_portfast(device,interface,mode=''):
    """ Configures Spanning Tree Portfast on port
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            mode ('str',optional) : Options are disable/trunk. Default is '' (i.e no mode)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    #initialize list variable
    config_list = []
    config_list.append("interface {interface}".format(interface=interface))
    config_list.append("spanning-tree portfast {mode}".format(mode=mode))
    try:
        device.configure(config_list)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure Primary Pvlan'
        )

def configure_interface_switchport_pvlan_mode(device, interface, mode):
    """ Configures Private Vlan Switchport mode
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            mode ('str')      : pvlan mode (i.e host or promiscuous)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring switchport pvlan mode on {interface} with mode = {mode}".format(
            interface=interface, mode=mode
        )
    )
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "switchport mode private-vlan {mode}".format(mode=mode),
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure Primary Pvlan'
        )

def configure_interface_pvlan_host_assoc(device,interface,primary_vlan,sec_vlan):
    """ Configures Interface Private Vlan Host Association
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            primary_vlan ('str'): Primary private vlan
            sec_vlan ('str'): Secondary private vlan
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    #initialize list variable
    config_list = []
    config_list.append("interface {interface}".format(interface=interface))
    config_list.append("switchport private-vlan host-association {primary_vlan} {sec_vlan}".format(
        primary_vlan=primary_vlan,sec_vlan=sec_vlan))
    try:
        device.configure(config_list)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure Primary Pvlan Host Association'
        )
