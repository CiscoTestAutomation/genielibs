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
from unicon.eal.dialogs import Dialog, Statement

# Interface
from genie.libs.sdk.apis.iosxe.interface.get import (
    get_interface_running_config,
)
from genie.libs.sdk.apis.iosxe.interface.get import (
    get_interface_connected_adjacent_router_interfaces,
)

# utils
from genie.libs.sdk.apis.utils import mask_to_int
from genie.libs.sdk.apis.utils import tftp_config

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
    config = f"default interface {interface}"
    try:
        output = device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not default {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )

    return output


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


def clear_interface_counters(device, interface, timeout=60):
    """ Clear interface counters

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            timeout ('int', optional): Timeout in seconds. Default is 60
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
    dialog = Dialog([Statement(pattern=r'.*\[confirm\].*', action='sendline(\r)',loop_continue=True, continue_timer=False)])
    try:
        device.execute(
            "clear counters {interface}".format(interface=interface), reply=dialog, timeout=timeout
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


def config_interface_ospfv3(device, interface, ospfv3_pid, area, ipv4=False, ipv6=True,
                            network=None, hello_interval=0):
    """config OSPF on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ospfv3_pid (`str`): Ospfv3 process id
            area ('int'): Ospf area code
            ipv4 ('boolean',optional): Flag to configure IPv4 (Default False)
            ipv6 ('boolean',optional): Flag to configure IPv6 (Default True)
            network(`str`,optional): network name
            hello_interval('int',optional): hello time

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring OSPF on interface {interface}".format(interface=interface)
    )
    cmd = []
    cmd.append("interface {interface}".format(interface=interface))
    if ipv4:
        cmd.append("ospfv3 {pid} ipv4 area {area}".format(pid=ospfv3_pid, area=area))
    if ipv6:
        cmd.append("ospfv3 {pid} ipv6 area {area}".format(pid=ospfv3_pid, area=area))
    if network:
        cmd.append("ospfv3 {pid} network {network}".format(pid=ospfv3_pid, network=network))
    if hello_interval:
        cmd.append("ospfv3 {pid} hello-interval {hello_interval}".format(pid=ospfv3_pid, hello_interval=hello_interval))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ospfv3 {pid}. Error:\n{error}"
            .format(pid=ospfv3_pid, error=e)
        )
def configure_interface_split_horizon_eigrp(device, interface, eigrp_value,ipv6 = None):
    """config split-horizon-eigrp on interface

        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            ipv6 ('int'): ipv6
            eigrp_value ('int'): eigrp process id

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring split_horizon eigrp on interface {interface}")
    cmd = [f"interface {interface}"]
    if ipv6 is None:
        cmd.append(f"ip split-horizon eigrp {eigrp_value}")
    else:
        cmd.append(f"ipv6 split-horizon eigrp {eigrp_value}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure split-horizon Error:\n{e}")

def unconfigure_interface_split_horizon_eigrp(device, interface, eigrp_value, ipv6 = None):
    """unconfig split-horizon-eigrp on interface

        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            ipv6 ('int'): ipv6
            eigrp_value ('int'): eigrp process id

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring split_horizon eigrp on interface {interface}")
    cmd = [f"interface {interface}"]
    if ipv6 is None:
        cmd.append(f"no ip split-horizon eigrp {eigrp_value}")
    else :
        cmd.append(f"no ipv6 split-horizon eigrp {eigrp_value}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure split-horizon Error:\n{e}")


def config_interface_ospfv3_cost(device, interface, ospfv3_pid, hysteresis_per=None, hysteresis_threshold=None, throughput_val=None,
                              resources_val=None, latency_val=None, l2_factor_val=None):
    """config OSPF on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ospfv3_pid (`str`): Ospfv3 process id
            hysteresis_per ('int',optional): hysteresis percentage
            throughput_val ('int',optional): throughput value
            hysteresis_threshold ('int',optional): hysteresis threshold
            resources_val ('int',optional): resources value
            latency_val ('int',optional): latency value
            l2_factor_val ('int',optional): l2_factor value

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring OSPF on interface {interface}".format(interface=interface)
    )
    cmd = []
    cmd.append("interface {interface}".format(interface=interface))
    if not any([hysteresis_per, hysteresis_threshold, throughput_val, resources_val, latency_val, l2_factor_val]):
        cmd.append(f"ospfv3 {ospfv3_pid} ipv6 cost dynamic")
    if hysteresis_per is not None:
        cmd.append(f"ospfv3 {ospfv3_pid} ipv6 cost dynamic hysteresis percent {hysteresis_per}")
    if hysteresis_threshold is not None:
        cmd.append(f"ospfv3 {ospfv3_pid} ipv6 cost dynamic hysteresis threshold {hysteresis_threshold}")
    if throughput_val is not None:
        cmd.append(f"ospfv3 {ospfv3_pid} ipv6 cost dynamic weight throughput {throughput_val}")
    if resources_val is not None:
        cmd.append(f"ospfv3 {ospfv3_pid} ipv6 cost dynamic weight resources {resources_val}")
    if latency_val is not None:
        cmd.append(f"ospfv3 {ospfv3_pid} ipv6 cost dynamic weight latency {latency_val}")
    if l2_factor_val is not None:
        cmd.append(f"ospfv3 {ospfv3_pid} ipv6 cost dynamic weight l2-factor {l2_factor_val}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ospfv3 {pid}. Error:\n{error}"
            .format(pid=ospfv3_pid, error=e)
        )


def config_interface_ospfv3_network_type(device, interface, process_id, network_type, ip_version):
    """Configure the OSPFv3 network type for an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Name of the interface
            process_id (`int`): Ospfv3 process id
            network_type (`str`): Network-type
            ip_version (`str`): Internet protocol version (`ipv4` or `ipv6` or `both`)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    if ip_version not in ["ipv4", "ipv6", "both"]:
        raise SubCommandFailure(
            "Internet protocol version not recognised: '{ip_version}'. "
            "Expected 'ipv4' or 'ipv6' or 'both'.".format(
                ip_version=ip_version
            )
        )
    log.info(
        "Configuring OSPFv3 {ip_version} network type for interface "
        "{interface} PID {process_id} as {network_type}".format(
            ip_version=ip_version,
            interface=interface,
            process_id=process_id,
            network_type=network_type
        )
    )
    cmd = "interface {interface}\n".format(interface=interface)
    cmd += "ospfv3 {process_id} ".format(process_id=process_id)
    if ip_version == "ipv6":
        cmd += "ipv6 "
    elif ip_version == "ipv4":
        cmd += "ipv4 "
    cmd += "network {network_type}".format(network_type=network_type)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ospfv3 network type for interface " \
            "{interface}, PID {process_id}, network type {network_type}. " \
            "Error:\n{error}".format(
                interface=interface,
                process_id=process_id,
                network_type=network_type,
                error=e
            )
        )


def unconfig_interface_ospfv3_network_type(device, interface, process_id, network_type, ip_version):
    """Unconfigure the OSPFv3 network type for an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Name of the interface
            process_id (`int`): Ospfv3 process id
            network_type (`str`): Network-type
            ip_version (`str`): Internet protocol version (`ipv4` or `ipv6` or `both`)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    if ip_version not in ["ipv4", "ipv6", "both"]:
        raise SubCommandFailure(
            "Internet protocol version not recognised: '{ip_version}'. "
            "Expected 'ipv4' or 'ipv6'.".format(
                ip_version=ip_version
            )
        )
    log.info(
        "Unconfiguring OSPFv3 {ip_version} network type for interface "
        "{interface} PID {process_id}".format(
            ip_version=ip_version,
            interface=interface,
            process_id=process_id
        )
    )
    cmd = "interface {interface}\n".format(interface=interface)
    cmd += "no ospfv3 {process_id} ".format(process_id=process_id)
    if ip_version == "ipv6":
        cmd += "ipv6 "
    elif ip_version == "ipv4":
        cmd += "ipv4 "
    cmd += "network {network_type}".format(network_type=network_type)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ospfv3 network type for interface " \
            "{interface}, PID {process_id}, network type {network_type}. " \
            "Error:\n{error}".format(
                interface=interface,
                process_id=process_id,
                network_type=network_type,
                error=e
            )
        )


def config_interface_ospfv3_flood_reduction(device, interface, process_id, ip_version):
    """Configure OSPFv3 flood reduction for an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Name of the interface
            process_id (`int`): Ospfv3 process id
            ip_version (`str`): Internet protocol version (`ipv4` or `ipv6`)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    if ip_version not in ["ipv4", "ipv6"]:
        raise SubCommandFailure(
            "Internet protocol version not recognised: '{ip_version}'. "
            "Expected 'ipv4' or 'ipv6'.".format(
                ip_version=ip_version
            )
        )
    log.info(
        "Configuring {ip_version} OSPFv3 flood reduction on {interface} "
        "for PID {process_id}".format(
            ip_version=ip_version,
            interface=interface,
            process_id=process_id
        )
    )
    cmd = "interface {interface}\n".format(interface=interface)
    cmd += "ospfv3 {process_id} ".format(process_id=process_id)
    if ip_version == "ipv6":
        cmd += "ipv6 "
    cmd += "flood-reduction"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure {ip_version} OSPFv3 flood-reduction for "
            "interface {interface} for PID {process_id}".format(
                ip_version=ip_version,
                interface=interface,
                process_id=process_id
            )
        )


def unconfig_interface_ospfv3_flood_reduction(device, interface, process_id, ip_version):
    """Unconfigure OSPFv3 flood reduction for an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Name of the interface
            process_id (`int`): Ospfv3 process id
            ip_version (`str`): Internet protocol version (`ipv4` or `ipv6`)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    if ip_version not in ["ipv4", "ipv6"]:
        raise SubCommandFailure(
            "Internet protocol version not recognised: '{ip_version}'. "
            "Expected 'ipv4' or 'ipv6'.".format(
                ip_version=ip_version
            )
        )
    log.info(
        "Unconfiguring {ip_version} OSPFv3 flood reduction on {interface} "
        "for PID {process_id}".format(
            ip_version=ip_version,
            interface=interface,
            process_id=process_id
        )
    )
    cmd = "interface {interface}\n".format(interface=interface)
    cmd += "no ospfv3 {process_id} ".format(process_id=process_id)
    if ip_version == "ipv6":
        cmd += "ipv6 "
    cmd += "flood-reduction"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure {ip_version} OSPFv3 flood-reduction for "
            "interface {interface} for PID {process_id}".format(
                ip_version=ip_version,
                interface=interface,
                process_id=process_id
            )
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
        disable_switchport=False,
        dhcpv4=False,
        dhcp_hostname="",
        vrf=None,
        link_local_address=None,
        secondary=False,
        prefix_name=None):
    """ Configure IP on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            ip_address (`str`, optional): IP addressed to be configured on interface, default value None
            mask (`str`, optional): Mask address to be used in configuration, default value None
            ipv6_address (`str`, optional): IPv6 address with subnet mask, default value None
            eth_encap_type (`str`, optional): Encapsulation type, default value None
            eth_encap_val (`str`, optional): Encapsulation value, default value None
            sub_interface (`str`, optional): Subinterface to be added to interface name, default value None
            disable_switchport (`bool`, optional): Set interface to operate on layer 3, default value False
            dhcpv4 (`bool`, optional): configure for ipv4 dhcp, default value False
            dhcp_hostname (`str`, optional): Optionally configure dhcp hostname as well, default value ""
            vrf (`str`, optional): vrf for in the interface, default value None
            link_local_address (`str`, optional): Link local address for an ipv6 interface, default value None
            secondary (`bool`, optional): Configure as secondary ipv4 address, default value False
            prefix_name (`str`, optional): Prefix name, truncated to 200 characters, default value None

        Returns:
            None
            Warning messages

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
        cfg_str += "no switchport \n"
    # configure vrf(vrf needs to configured before ip)
    if vrf:
        cfg_str += "vrf forwarding {vrf}\n".format(vrf=vrf)
    # configure ip and mask
    if ip_address and mask:
        cfg_str += "ip address {ip} {mask}".format(
            ip=ip_address, mask=mask
        )

        if secondary:
            cfg_str += " secondary"

        cfg_str += '\n'

    # Add ipv6 address configuration
    if ipv6_address:
        cfg_str += "ipv6 enable\n" \
                   "ipv6 address {ipv6}\n".format(
            ipv6=ipv6_address
        )
    # Configure ipv6 link-local address
    if link_local_address:
        cfg_str += "ipv6 enable\n" \
                   "ipv6 address {link_local_address} link-local\n".format(
            link_local_address=link_local_address
        )
    # configure port to receive ipv4 address via dhcp
    if dhcpv4:
        if dhcp_hostname:
            cfg_str += "ip address dhcp hostname " + dhcp_hostname + " \n"
        else:
            cfg_str += "ip address dhcp\n"
    # configure ipv6 dhcp client pd
    if prefix_name:
        cfg_str += "ipv6 dhcp client pd {prefix_name}\n".format(prefix_name=prefix_name)
    # Configure device
    try:
        out = device.configure(cfg_str)
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

    result = [line for line in out.splitlines() if line.startswith('%')]
    return result if result else None


def config_ip_subinterface(
        device,
        interface,
        sub_interface_num,
        ip_address,
        prefix,
        encap_type,
):
    """ Configure sub-interface with IP addresses on device
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            sub_interface_num (`int`): Subinterface to be added to
                                 interface name
            ip_address(`str`): IP addressed to be configured on interface
            prefix(`str`): prefix to be used in configuration
            encap_type (`str`): Encapsulation type
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    # interface {interface}.999
    #  encapsulation dot1Q 999
    #  ip address 10.4.0.1 255.255.255.0
    name = interface + "." + str(sub_interface_num)
    sub_intf = Interface(device=device, name=name)
    sub_intf.eth_encap_type1 = encap_type
    sub_intf.eth_encap_val1 = sub_interface_num
    ipv4a = IPv4Addr(device=device)
    ipv4a.ipv4 = IPv4Address(ip_address)
    ipv4a.prefix_length = prefix
    sub_intf.add_ipv4addr(ipv4a)

    try:
        config = str(sub_intf.build_config(apply=False))
        sub_intf.build_config()
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure sub-interface {interface}. Error:\n{error}".format(
                interface=sub_intf, error=e
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
    config_list.append("switchport")
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

    if len(interfaces) > 3:
        if interface == interfaces[-1]:
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


def configure_interface_switchport_trunk(device, interfaces, vlan_id, oper=None):

    """ configure switchport mode trunk to the interface

        Args:
            device (`obj`): Device object
            interface (`list`): list of Interface to be added to port channel
            vlan (`str`): vlan to be added to the port
            oper (`str`): "default(None) Vlan operation to be added"
        Returns:
            None
    """
    log.info(
        "Configuring switchport interface on {interfaces}".format(
            interfaces=interfaces
        )
    )

    try:
        config = []
        for intf in interfaces:
            config.append("interface {intf}".format(intf=intf))
            config.append("switchport")
            config.append("switchport mode trunk")
            if oper is None:
                config.append("switchport trunk allowed vlan {vlan_id}".format(
                                                        vlan_id=vlan_id))
            elif oper == 'add':
                config.append("switchport trunk allowed vlan add {vlan_id}".format(
                                                        vlan_id=vlan_id))
        device.configure('\n'.join(config))
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
            monitor_config (`list`) : List of monitor session configuration
                ex.)
                    monitor_config = [{
                            'session_name': 1,
                            'session_type': 'erspan-source',
                            'interface': 'GigabitEthernet10',
                            'vlan_id' : '100',
                            'erspan_id': 10,
                            'ip_address': '192.168.1.1',
                            'origin_ip_address': '192.168.1.2',
                            'ipv6_address': '2001::2',
                            'mtu': 1500,
                            'vrf': 'red',
                            'origin_ipv6_address': '2001::1'
                        },
                        {
                            'session_name': 2,
                            'session_type': 'erspan-destination',
                            'interface': 'GigabitEthernet11',
                            'erspan_id': 10,
                            'ip_address': '192.168.1.1'
                            'ipv6_address' : '2001::2'
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
            if 'interface' in mc:
               config.append("source interface {}\n".format(mc["interface"]))
            if 'vlan_id' in mc:
               config.append("source vlan {}\n".format(mc["vlan_id"]))
            config.append("destination\n")
            config.append("erspan-id {}\n".format(mc["erspan_id"]))
            if 'ip_address' in mc:
               config.append("ip address {}\n".format(mc["ip_address"]))
            if 'origin_ip_address' in mc:
               config.append("origin ip address {}\n".format(mc["origin_ip_address"]))
            if 'ipv6_address' in mc:
               config.append("ipv6 address {}\n".format(mc["ipv6_address"]))
            if 'origin_ipv6_address' in mc:
               config.append("origin ipv6 address {}\n".format(mc["origin_ipv6_address"]))
        else:
            unshut_interface(device=device, interface=mc["interface"])
            config.append(
                "monitor session {} type {}\n".format(
                    mc["session_name"], mc["session_type"]
                )
            )
            config.append("destination interface {}\n".format(mc["interface"]))
            if 'vlan_id' in mc:
               config.append("destination vlan {}\n".format(mc["vlan_id"]))
            config.append("source\n")
            config.append("erspan-id {}\n".format(mc["erspan_id"]))
            if 'ip_address' in mc:
               config.append("ip address {}\n".format(mc["ip_address"]))
            if 'ipv6_address' in mc:
               config.append("ipv6 address {}\n".format(mc["ipv6_address"]))
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


def configure_scale_subintfs_via_tftp(
    device, server, interface, vlan_id_start, vlan_id_step,
    vlan_id_count, ip_addr_start, ip_addr_step, netmask,
    pim=None, unconfig=False, tftp=False):
    """ Configures scale subinterfaces via tftp config

        Args:
            device ('obj'): Device to use
            server ('str'): Testbed.servers
            interface ('str'): Physical interface to configure
            vlan_id_start ('int'): Start of vlan range
            vlan_id_step ('int'): Size of vlan range step
            vlan_id_count ('int'): How many steps for vlan range
            ip_addr_start ('str'): Start of sub-intf ip addr
            ip_addr_step ('str'): Size of sub-intf ip addr
            netmask ('str'): Netmask to configure
            pim ('str'): pim mode
            unconfig ('bool'): Unconfig or not
            tftp ('bool'): Tftp config or not

        Raises:
            Failure

        Returns:
            None
            cmds_block str if not tftp configure

    """
    cmds = ''
    vlan_id = vlan_id_start
    if pim:
        pim = 'ip pim {}'.format(pim)

    if unconfig:
        for count in range(vlan_id_count):
            cmds += """
            no interface {interface}.{vlan_id}
            """.format(interface=interface,
                       vlan_id=vlan_id)

            vlan_id += vlan_id_step
    else:
        IPaddr = IPv4Address(ip_addr_start)
        for count in range(vlan_id_count):

            cmds += """
            interface {interface}.{vlan_id}
                encapsulation dot1q {vlan_id}
                ip address {ip_address} {netmask}
                {pim}
            exit
            """.format(interface=interface,
                       vlan_id=vlan_id,
                       ip_address=IPaddr,
                       netmask=netmask,
                       pim=pim)

            vlan_id += vlan_id_step
            IPaddr += int(IPv4Address(ip_addr_step))

    if tftp:
        try:
            tftp_config(device, server, cmds)
        except Exception:
            raise Exception('tftp_config failed.')
    else:
        return cmds


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

def remove_interface_ip(device,
                        interface,
                        ip_address="",
                        mask="",
                        secondary=False):
    """ Remove ip on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ip_address (`str`,optional): IPv4 address
            mask (`str`,optional): Mask
            secondary (`bool`,optional): Remove secondary IPv4 address

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

    cmd = "no ip address"
    if ip_address:
        cmd += f" {ip_address}"
    if mask:
        cmd += f" {mask}"
    if secondary:
        cmd += " secondary"


    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                cmd,
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfig ip address on interface {interface}.\n"
            "Command: {command}\n"
            "Error:\n{error}".format(interface=interface, command=cmd, error=e
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

def enable_ipv6_dhcp_server(device, interface, pool_name, rapid_commit=True):
    """ Enable IPv6 DHCP server on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to enable IPv6 DHCP server
            pool_name (`str`): Pool name
            rapid_commit ('bool'): Rapid commit. Default is True
        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = [f"interface {interface}"]

    if rapid_commit:
        cmd.append(f"ipv6 dhcp server {pool_name} rapid-commit")
    else:
        cmd.append(f"ipv6 dhcp server {pool_name}")
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
            port_channel (`str`): Port channel number to be removed

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure("no interface Port-channel {port_channel}".format(
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
                """
                interface {interface}
                  source template {template_name}
                """.format(interface=interface, template_name=template_name))

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
                """
                interface {interface}
                  no source template {template_name}
                """.format(interface=interface, template_name=template_name))

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
    ip_address=None,
    mask=None,
    tunnel_source=None,
    tunnel_destination=None,
    keepalive_timer = 10,
    ip_mtu = None,
    ipv6_address=None,
    v6_mask=None,
    mode=None,
    tunnel_protection=None,
    profile=None,
    in_vrf=None,
    out_vrf=None,
    acl_name=None,
    tunnel_protocol=None
):
    """ Configure tunnel interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            ip_address (`str`,optional): IPv4 addressed to be configured on interface
            mask (`str`,optional): IPv4 Mask address to be used in configuration
            tunnel_source (`str`): tunnel source address
            tunnel_destination (`str`): tunnel destination address
            keepalive_timer ('int',optional): tunnel keepalive timer,default value is 10
            ip_mtu ('str',optional): tunnel mtu, default value is None
            ipv6_address (`str`,optional): IPv6 address with subnet mask,default value is None
            v6_mask ('str',optional): IPv6 mask (Default None)
            mode ('str',optional): Tunnel mode. Default is gre
            tunnel_protection ('str',optional): Protection type (i.e ipsec,dike)
            profile ('str',optional): Tunnel protection profile name
            in_vrf ('str',optional): client vrf for  the tunnel
            out_vrf ('str',optional): wan vrf for  the tunnel
            acl_name('str',optional): acl policy applied on tunnel inetrface
            tunnel_protocol ('str',optional): Protocol type (i.e ipv4)

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("interface {intf}".format(intf=interface))
    #configure vrf (vrf to be configured before ip)
    if in_vrf:
        configs.append("vrf forwarding {vrf}".format(vrf=in_vrf))
    if ip_address:
        configs.append("ip address {ip} {mask}".format(ip=ip_address,mask=mask))

        if mode:
            # IOSXE Defaults to GRE
            configs.append("tunnel mode {mode} ipv4".format(mode=mode))

    configs.append("tunnel source {ip}".format(ip=tunnel_source))
    configs.append("tunnel destination {ip}".format(ip=tunnel_destination))
    if keepalive_timer:
        configs.append("keepalive {timer}".format(timer=keepalive_timer))
    if ip_mtu:
        configs.append("ip mtu {mtu}".format(mtu=ip_mtu))
    if ipv6_address:
        configs.append("tunnel mode {mode} ipv6".format(mode=mode))
        # Check if mask needs to be configured with IPv6 address
        if v6_mask:
            configs.append("ipv6 address {ipv6}/{v6_mask}".format(ipv6=ipv6_address, v6_mask=v6_mask))
        else:
            configs.append("ipv6 address {ipv6}".format(ipv6=ipv6_address))
    if out_vrf:
        configs.append("tunnel vrf {vrf}".format(vrf=out_vrf))
    if tunnel_protection:
        configs.append("tunnel protection {tunnel_protection} profile {profile}".
                       format(tunnel_protection=tunnel_protection,profile=profile))
    if tunnel_protection is not None and tunnel_protocol == 'ipv4' and acl_name is not None:
        configs.append(f"tunnel protection {tunnel_protection} policy {tunnel_protocol} {acl_name}")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure Tunnel interface "
            "{interface} on device {dev}. Error:\n{error}".format(
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


def disable_ipv6_dhcp_server(device, interface):
    """ Unconfigure IPv6 DHCP server from an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to enable IPv6 DHCP server

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = ["interface {intf}".format(intf=interface),
           "no ipv6 dhcp server"]

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to remove IPv6 DHCP server from interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e
            )
        )

def enable_ipv6_address_dhcp(device, interface):
    """ Enables DHCP for IPv6 address assignment on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to enable IPv6 address DHCP

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure([f'interface {interface}',
                          'ipv6 enable',
                          'ipv6 address dhcp'])

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to enable IPv6 address DHCP on interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e,
            )
        )


def disable_ipv6_address_dhcp(device, interface):
    """ Disables DHCP for IPv6 address assignment on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to disable IPv6 address DHCP

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure([f'interface {interface}',
                          'no ipv6 enable',
                          'no ipv6 address dhcp'])

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to disable IPv6 address DHCP on interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e
            )
        )

def unconfig_interface_ospfv3(device, interface, ospfv3_pid, area, ipv4=False, ipv6=True, manet=False):
    """unconfig OSPF on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ospfv3_pid (`str`): Ospfv3 process id
            area ('int'): Ospf area code
            ipv4 ('boolean',optional): Flag to remove IPv4 (Default False)
            ipv6 ('boolean',optional): Flag to remove IPv6 (Default True)
            manet ('boolean',optional): Flag to remove manet (Default False)

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    log.info(
        "Unconfiguring OSPF from interface {interface}".format(interface=interface)
    )
    cmd = []
    cmd.append("interface {interface}".format(interface=interface))
    if ipv4:
        cmd.append("no ospfv3 {pid} ipv4 area {area}".format(pid=ospfv3_pid, area=area))
    if ipv6:
        cmd.append("no ospfv3 {pid} ipv6 area {area}".format(pid=ospfv3_pid, area=area))
    if manet:
        cmd.append("no ospfv3 {pid} network manet".format(pid=ospfv3_pid))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ospfv3 {pid}. Error:\n{error}"
            .format(pid=ospfv3_pid, error=e)
        )

def unconfig_interface_ospfv3_cost(device, interface, ospfv3_pid, hysteresis_per=None, hysteresis_threshold=None, throughput_val=None,
              resources_val=None, latency_val=None, l2_factor_val=None):
    """config OSPF on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ospfv3_pid (`str`): Ospfv3 process id
            hysteresis_per ('int',optional): hysteresis percentage
            hysteresis_threshold ('int',optional): hysteresis threshold
            throughput_val ('int',optional): throughput value
            resources_val ('int',optional): resources value
            latency_val ('int',optional): latency value
            l2_factor_val ('int',optional): l2_factor value


        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring OSPF on interface {interface}".format(interface=interface)
    )
    cmd = []
    cmd.append("interface {interface}".format(interface=interface))
    if not any([hysteresis_per, hysteresis_threshold, throughput_val, resources_val, latency_val, l2_factor_val]):
        cmd.append(f"no ospfv3 {ospfv3_pid} ipv6 cost dynamic")
    if hysteresis_per is not None:
        cmd.append(f"no ospfv3 {ospfv3_pid} ipv6 cost dynamic hysteresis percent {hysteresis_per}")
    if hysteresis_threshold is not None:
        cmd.append(f"no ospfv3 {ospfv3_pid} ipv6 cost dynamic hysteresis threshold {hysteresis_threshold}")
    if throughput_val is not None:
        cmd.append(f"no ospfv3 {ospfv3_pid} ipv6 cost dynamic weight throughput {throughput_val}")
    if resources_val is not None:
        cmd.append(f"no ospfv3 {ospfv3_pid} ipv6 cost dynamic weight resources {resources_val}")
    if latency_val is not None:
        cmd.append(f"no ospfv3 {ospfv3_pid} ipv6 cost dynamic weight latency {latency_val}")
    if l2_factor_val is not None:
        cmd.append(f"no ospfv3 {ospfv3_pid} ipv6 cost dynamic weight l2-factor {l2_factor_val}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ospfv3 {pid}. Error:\n{error}"
            .format(pid=ospfv3_pid, error=e)
        )


def config_portchannel_range(device, portchannel_start, portchannel_end):
    """ Configure port channel
        e.g.
        interface range port-channel 1-50

        Args:
            device (`obj`): Device object
            portchannel_start(`int`): Port channel number start
            portchannel_end(`int`): Port channel number end

        Return:
            None
        Raise:
            SubCommandFailure
    """
    try:
        device.configure(f"interface range port-channel {portchannel_start} - {portchannel_end}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure port channel  on device. Error:\n{e}"
        )

def configure_interface_storm_control_level(
        device,
        interface,
        sc_type,
        sc_rising_threshold,
        sc_falling_threshold='',
        sc_calc_type=''):
    """ Config storm control level in
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            sc_type('str'): storm control filter traffic type
            sc_rising_threshold('float' or 'str'): storm control rising threshold
            sc_falling_threshold('float' or 'str', optional): storm control falling threshold, default is None
            sc_calc_type('str', optional): storm control suppression level type, default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Config storm control level on interface {interface}")

    if sc_calc_type:
        sc_calc_type = f' {sc_calc_type}'

    if sc_falling_threshold:
        sc_falling_threshold = f' {sc_falling_threshold}'

    cmd = f'storm-control {sc_type} level{sc_calc_type} {sc_rising_threshold}{sc_falling_threshold}'

    try:
        device.configure(
            [
                f"interface {interface}",
                cmd,
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to config storm control level on {interface}. Error:\n{e}")


def unconfigure_interface_storm_control_level(
        device,
        interface,
        sc_type):
    """ Unconfig storm control level in
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            sc_type('str'): storm control filter traffic type
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfig storm control level on interface {interface}")

    cmd = f'no storm-control {sc_type} level'

    try:
        device.configure(
            [
                f"interface {interface}",
                cmd,
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfig storm control level on {interface}. Error:\n{e}")


def configure_interface_storm_control_action(
        device,
        interface,
        action):
    """ Config storm control action in
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            action ('str'): storm control action
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Config storm control action on interface {interface}")

    cmd = f'storm-control action {action}'
    try:
        device.configure(
            [
                f"interface {interface}",
                cmd,
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to config storm control action on {interface}. Error:\n{e}")


def unconfigure_interface_storm_control_action(
        device,
        interface,
        action):
    """ Unconfig storm control action in
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            action('str'): storm control action
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfig storm control action on interface {interface}")

    cmd = f'no storm-control action {action}'

    try:
        device.configure(
            [
                f"interface {interface}",
                cmd,
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfig storm control action on {interface}. Error:\n{e}")


def config_port_security_on_interface(
    device,
    interface,
    maximum_addresses=1,
    aging_time=None,
    aging_type=None,
    violation_mode=None,
    mac_address=None,
):
    """ Configuring port security on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            maximum_addresses (`int`,optional): maximum mac addresses, default value is 1
            aging_time (`str`,optional): aging time for mac address, default value is None
            aging_type (`str`,optional): aging type for mac address, default value is None
            violation_mode (`str`,optional): violation mode, default value is None
            mac_address ('str' ,optional): mac address mode, default value is None

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    # Build config list
    cfg_lst = []
    cfg_lst.append("interface {intf}".format(intf=interface))
    cfg_lst.append("switchport port-security")

    if maximum_addresses:
        cfg_lst.append("switchport port-security maximum {maximum_addresses}".format(
            maximum_addresses=maximum_addresses))

    if aging_time:
        cfg_lst.append("switchport port-security  aging time {aging_time}".format(
            aging_time=aging_time))

    if aging_type:
        cfg_lst.append("switchport port-security  aging type {aging_type}".format(
            aging_type=aging_type))

    if violation_mode:
        cfg_lst.append("switchport port-security violation {violation_mode}".format(
             violation_mode=violation_mode))

    if mac_address:
        cfg_lst.append("switchport port-security mac-address {mac_address}".format(
             mac_address=mac_address))

    # Configure device
    try:
        device.configure(cfg_lst)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure switchport port-security on interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e,
            )
        )


def configure_control_policies(
    device,
    policy_name,
    event=None,
    match=None,
    class_number=None,
    class_name=None,
    class_action=None,
    action_number=None,
    action=None,
    action_method=None,
    auth_rest_timer=None,
    template_name=None,
    priority=None,
    dot1x_type=None,
    retries=None,
    retry_time=None
):
    """ Configure policy-map on an device

        Args:
            device (`obj`): Device object
            policy_name (`str`): name of the policy
            event (`str`,optional): event name, default value is None
            match (`str`,optional): match-all or match-first, default value is None
            class_number (`int`,optional): class number between 1 to 254, default value is None
            class_name (`str`,optional): class name if any exists, default value is None
            class_action (`str`,optional): class action to be perform, default value is None
            action_number (`int`,optional): action number between 1 to 254, default value is None
            action (`str`,optional): action to be perform under this class, default value is None
            action_method (`str`,optional): Mab or dot1x or webauth, default value is None
            auth_rest_timer ('int', optional): Authentication restart timer, default value is None
            template_name (`str`,optional): Template name, default value is None
            priority ('int', optional): Priority vlaue, default value is None
            dot1x_type (`str`,optional): Dot1x type. default value is None
            retries (`str`,optional): retries option. default value is None
            retry_time (`str`,optional): retry-time option. default value is None

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    # Build config list
    cfg_lst = []
    cfg_lst.append(f"policy-map type control subscriber {policy_name}")

    if event and match:
        cfg_lst.append(f"event {event} {match}")
    if class_number is not None and class_name is not None:
        cfg_lst.append(f"{class_number} class {class_name} {class_action}")
    elif class_number is not None:
        cfg_lst.append(f"{class_number} class always {class_action}")
    if action_number and action and action_method:
        if template_name:
            cfg_lst.append(f"{action_number} {action} {action_method} {template_name}")
        elif action == 'authenticate':

            if priority and retries:
                cfg_lst.append(f"{action_number} {action} using {action_method} retries {retries} retry-time {retry_time} priority {priority}")
            elif priority:
                cfg_lst.append(f"{action_number} {action} using {action_method} priority {priority}")
            elif dot1x_type:
                cfg_lst.append(f"{action_number} {action} using {action_method} {dot1x_type}")
            else:
                cfg_lst.append(f"{action_number} {action} using {action_method}")
        else:
            cfg_lst.append(f"{action_number} {action} {action_method}")
    elif auth_rest_timer:
        cfg_lst.append(f"{action_number} {action} {auth_rest_timer}")
    elif action_number and action:
        cfg_lst.append(f"{action_number} {action}")


    # Configure device
    try:
        device.configure(cfg_lst)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure policy-map type control on device"
            "device {dev}. Error:\n{error}".format(
                dev=device.name,
                error=e,
            )
        )

def configure_subinterface(
    device,
    physical_port,
    any_number,
    ip_address,
    sub_mask
):
    """ Configure subinterface
        Args:
            device ('obj'): device to use
            physical_port ('str'): physical port
            any_number ('str'): any number
            ip_address ('str'): Ip address
            sub_mask ('str'): Subnet mask
        Returns:
            console output
        Raises:
            SubCommandFailure: subinterface not enabled
    """
    cmd = [
            "interface {}.{}".format(physical_port,any_number),
            "encapsulation dot1q {} native".format(any_number),
            "ip address {} {}".format(ip_address,sub_mask)
          ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure subinterface")

def configure_interface_reg_segment(
        device,
        interface,
        segment_no,
        edge = False,
        preferred = False):
    """ Config Reg segment on interface
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            segment_no ('int'): rep segment number
            edge('bool'): edge preferred. Default is False
            preferred  ('bool'): neighbor preferred . Default is False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Config Reg segment on  interface {interface}")
    cmd = f"rep segment {segment_no}"
    if edge :
         cmd += " edge no-neighbor"
    if preferred:
         cmd += " preferred"
    try:
        device.configure(
            [
                f"interface {interface}",
                cmd,
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to config rep segment  on {interface}. Error:\n{e}")

def unconfigure_interface_reg_segment(
        device,
        interface,
        segment_no,
        edge = False,
        preferred = False):
    """ Unconfig Reg segment on interface
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            segment_no ('int'): rep segment number
            edge('bool'): edge preferred. Default is False
            preferred  ('bool'): neighbor preferred. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"unconfig Reg segment on  interface {interface}")
    cmd = f"no rep segment {segment_no}"
    if edge :
         cmd += " edge no-neighbor"
    if preferred:
         cmd += " preferred"

    try:
        device.configure(
            [
                f"interface {interface}",
                cmd,
            ]
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfig rep segment  on {interface}. Error:\n{e}")

def configure_interface_reg_segment_timer(
        device,
        interface,
        segment_timer):
    """ Config Reg segment timer on interface
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            segment_timer ('int'): rep segment timer
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Config Reg segment timer on interface {interface}")

    cmd = f'rep lsl-age-timer {segment_timer}'
    try:
        device.configure(
            [
                f"interface {interface}",
                cmd,
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to config rep segment timer on {interface}. Error:\n{e}")

def unconfigure_interface_reg_segment_timer(
        device,
        interface,
        segment_timer):
    """ Unconfig Reg segment timer on interface
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            segment_timer ('int'): rep segment timer
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"unconfig Reg segment timer on interface {interface}")

    cmd = f'no rep lsl-age-timer {segment_timer}'
    try:
        device.configure(
            [
                f"interface {interface}",
                cmd,
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfig rep segment timer on {interface}. Error:\n{e}")
def configure_switchport_nonegotiate(
        device,
        interface):
    """ Config switchport nonegotiate on interface
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Config switchport nonegotiate on interface {interface}")

    cmd = 'switchport nonegotiate'
    try:
        device.configure(
            [
                f"interface {interface}",
                cmd,
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to config switchport nonegotiate on {interface}. Error:\n{e}")

def unconfigure_switchport_nonegotiate(
        device,
        interface):
    """ Unconfig switchport nonegotiate on interface
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfig switchport nonegotiate on interface {interface}")

    cmd = 'no switchport nonegotiate'
    try:
        device.configure(
            [
                f"interface {interface}",
                cmd,
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unonfig switchport nonegotiate on {interface}. Error:\n{e}")

def configure_interface_pvlan_mode_with_submode(device, interface, primary_mode, sub_mode):
    """ Configures Private Vlan Switchport mode
        Args:
            device ('obj')            : device to use
            interface ('str')         : interface to configure
            primary_mode ('str')      : pvlan mode (i.e host or trunk)
            sub_mode ('str')          : pvlan mode (i.e promiscuous)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        f"Configuring switchport pvlan mode with submode on {interface} with mode = {primary_mode} and sub mode = {sub_mode} "
    )
    try:
        device.configure(
            [
                f"interface {interface}",
                f"switchport mode private-vlan {primary_mode} {sub_mode}",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure Primary Pvlan with primary and submodes.Error:\n{e}"
        )

def configure_interface_switchport_pvlan_and_native_vlan(device, interface, mode, vlan_id):
    """ Configures Private Vlan Switchport mode
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            mode ('str')      : pvlan mode (i.e trunk or association)
	    vlan_id ('int')   : VLAN ID of the native VLAN
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        f"Configuring switchport pvlan mode on {interface} with mode = {mode} and VLAN ID of {vlan_id}"
    )
    try:
        device.configure(
            [
                f"interface {interface}",
                f"switchport private-vlan {mode} native vlan {vlan_id}",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure Private vlan.Error:\n{e}"
        )

def configure_interface_switchport_pvlan_association(device, interface, mode, primary_vlan_id, secondary_vlan_id):
    """ Configures Private Vlan Switchport mode
        Args:
            device ('obj')    			: device to use
            interface ('str') 			: interface to configure
            mode ('str')      			: pvlan mode (i.e trunk or association)
	    primary_vlan_id ('int') 	        : Primary VLAN ID of the native VLAN
	    secondary_vlan_id ('int')   	: Secondary VLAN ID of the native VLAN
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        f"Configuring switchport pvlan association on {interface} with Primary vlan id of {primary_vlan_id} and Secondary vlan id of {secondary_vlan_id}"
    )
    try:
        device.configure(
            [
                f"interface {interface}",
                f"switchport private-vlan association {mode} {primary_vlan_id} {secondary_vlan_id}",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure Pvlan with primary/secondary vlan ID.Error:\n{e}"
        )

def configure_interface_switchport_pvlan_mapping(device, interface, mode, primary_vlan_id, secondary_vlan_id):
    """ Configures Private Vlan Switchport mode
        Args:
            device ('obj')    			: device to use
            interface ('str') 			: interface to configure
            mode ('str')      			: pvlan mode (i.e trunk or association)
	    primary_vlan_id ('int') 	        : Primary VLAN ID of the native VLAN
	    secondary_vlan_id ('int')	        : Secondary VLAN ID of the native VLAN
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        f"Configuring switchport pvlan mapping on {interface} with Primary vlan id of {primary_vlan_id} and Secondary vlan id of {secondary_vlan_id}"
    )
    try:
        device.configure(
            [
                f"interface {interface}",
                f"switchport private-vlan mapping {mode} {primary_vlan_id} {secondary_vlan_id}",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure Pvlan mapping with primary/secondary vlan ID.Error:\n{e}"
        )

def configure_virtual_template(device,
    virtual_template_number,
    unnumbered_interface,
    auth=False,
    authentication=None,
    mss=False,
    load_delay=False,
    mss_size=0,
    load_delay_interval=0,
    mtu='',
    ipv6_mtu='',
    no_ip_redirects=False,
    no_peer_ip=False,
    pool_name=None,
    ipv6_pool_name=None):
    """ Configure virtual-template interface

        Args:
            device (`obj`): Device object
            virtual_template_number ('int') : virtual template number
            unnumbered_interface (`str`): Interface name
            auth('bool', optional): check for authentication
            authentication ('str', optional) : PAP, CHAP
            mtu ('str', optional) : mtu value
            mss:('bool', optional): check for mss config
            mss_size('int', optional): Maximum segment size
            load_delay('bool', optional):load_delay check
            load_delay_interval('int', optional): load delay
            no_ip_redirects('bool', optional): no ip redirects option
            no_peer_ip('bool', optional): no peer ip default option
            pool_name('string', optional): peer default ip address pool <pool_name>
            ipv6_pool_name('string', optional): peer default ipv6 pool <ipv6_pool_name>
        For the arguments that are optional, the default value is None.

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    if not device.is_connected():
        connect_device(device=device)

    cli = []
    cli.append(f"interface Virtual-Template {virtual_template_number}")
    cli.append(f"ip unnumbered {unnumbered_interface}")
    if auth:
        cli.append(f"ppp authentication {authentication}")
    if mss:
        cli.append(f"ip tcp adjust-mss {mss_size}")
    if load_delay:
        cli.append(f"load-interval {load_delay_interval}")
    if len(mtu) != 0:
        cli.append(f"mtu {mtu}")
    if len(ipv6_mtu) != 0:
        cli.append(f"ipv6 mtu {ipv6_mtu}")
    if no_ip_redirects:
        cli.append("no ip redirects")
    if no_peer_ip:
        cli.append("no peer default ip address")
    if pool_name:
        cli.append(f"peer default ip address pool {pool_name}")
    if ipv6_pool_name:
        cli.append(f"peer default ipv6 pool {ipv6_pool_name}")

    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure virtual-template interface on device. Error:\n{e}"
        )

def unconfigure_virtual_template(device, virtual_template_number):

    """ Configure virtual-template interface

        Args:
            device (`obj`): Device object
            virtual_template_number ('int') : virtual template number

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    if not device.is_connected():
        connect_device(device=device)

    cli = []
    cli.append(f"no interface Virtual-Template {virtual_template_number}")

    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure virtual-template on device. Error:\n{e}"
        )

def configure_ipv6_enable(device, interface):
    """ Enable ipv6
        Args:
            device (`obj`): Device object
            interface ('str'): interface name to enable ipv6
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring ipv6 enable under {interface}".format(interface=interface))
    cmd = []
    cmd.append("interface {interface}".format(interface=interface))
    cmd.append("ipv6 enable")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ipv6 enable under {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )

def configure_uplink_interface(device, interfaces, vlan_range, vlan1, vlan2):

    """ configure uplink interface
        Args:
            device (`obj`): Device object
            interfaces (`list`): list of Interface to be added to port channel
            vlan_range (`str`): vlan range to be added
            vlan1 (`str`): vlan to be added to the port
            vlan2 (`str`): vlan to be added to the port
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure uplink interface
    """
    log.debug(f"Configuring uplink interface on {interfaces}")
    confg = []
    for intf in interfaces:
         confg.append(f'interface {intf}')
         confg.append('switchport')
         confg.append('switchport mode private-vlan trunk promiscuous')
         confg.append(f'switchport private-vlan trunk allowed vlan {vlan_range}')
         confg.append(f'switchport private-vlan mapping trunk {vlan1} {vlan2}')
         confg.append('ip dhcp snooping trust')
    try:
        device.configure(confg)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to uplink interface on {interfaces}. Error:\n{e}"
            )

def configure_downlink_interface(device, interfaces, vlan_range, vlan1, vlan2):

    """ configure downlink interface
        Args:
            device (`obj`): Device object
            interfaces (`list`): list of Interface to be added to port channel
            vlan_range (`str`): vlan range to be added
            vlan1 (`str`): vlan to be added to the port
            vlan2 (`str`): vlan to be added to the port
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure downlink interface
    """
    log.debug(f"Configuring downlink interface on {interfaces}")
    confg = []
    for intf in interfaces:
         confg.append(f'interface {intf}')
         confg.append('switchport mode private-vlan trunk')
         confg.append(f'switchport private-vlan trunk allowed vlan {vlan_range}')
         confg.append(f'switchport private-vlan association trunk {vlan1} {vlan2}')

    try:
        device.configure(confg)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to downlink interface on {interfaces}. Error:\n{e}")


def configure_switchport_trunk_native_vlan(device, interfaces, native_vlan):

    """ configure switchport trunk native vlan
        Args:
            device (`obj`): Device object
            interfaces (`list`): list of Interface to be added to port channel
            native_vlan (`str`): native vlan Id to be added
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure switchport trunk native vlan
    """
    log.debug(f"Configuring switchport trunk native vlan on {interfaces}")
    confg = []
    for intf in interfaces:
         confg.append(f'interface {intf}')
         confg.append(f'switchport trunk native vlan {native_vlan}')
         confg.append('switchport mode trunk')

    try:
        device.configure(confg)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure switchport trunk native vlan on {interfaces}. Error:\n{e}")

def configure_switchport_mode_trunk_snooping_trust(device, interfaces):

    """ configure switchport mode trunk snooping trust
        Args:
            device (`obj`): Device object
            interfaces (`list`): list of Interface to be added to port channel

        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure switchport mode trunk snooping trust
    """
    log.debug(f"Configuring switchport mode trunk snooping trust on {interfaces}")
    confg = []
    for intf in interfaces:
         confg.append(f'interface {intf}')
         confg.append('switchport mode trunk')
         confg.append('ip dhcp snooping trust')

    try:
        device.configure(confg)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure switchport mode trunk snooping trust on {interfaces}. Error:\n{e}"
        )

def configure_egress_interface(device, interfaces, native_vlan, vlan_range, vlan1, vlan2):

    """ configure egress interface
        Args:
            device (`obj`): Device object
            interfaces (`list`): list of Interface to be added to port channel
            native_vlan (`str`): native vlan Id to be added
            vlan_range (`str`): vlan range to be added
            vlan1 (`str`): vlan to be added to the port
            vlan2 (`str`): vlan to be added to the port

        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure egress interface
    """
    log.debug(f"Configuring egress interface on {interfaces}")

    confg = []
    for intf in interfaces:
         confg.append(f'interface {intf}')
         confg.append('switchport mode private-vlan trunk')
         confg.append(f'switchport trunk native vlan {native_vlan}')
         confg.append(f'switchport private-vlan trunk allowed vlan {vlan_range}')
         confg.append(f'switchport private-vlan association trunk {vlan1} {vlan2}')

    try:
        device.configure(confg)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure switchport mode trunk snooping trust on {interfaces}. Error:\n{e}")

def unconfigure_interfaces_on_port_channel(
    device, interfaces, mode, channel_group,
    channel_protocol=None, disable_switchport=False,
    ):
    """ Add interface <interface> to port channel

        Args:
            device (`obj`): Device object
            mode (`str`): Interface mode under Port channel.Default value is None
            interfaces(`List`): List of interfaces to configure.Default value is None
            channel_group (`obj`): Channel group.Default value is None
            channel_protocol (`str`,optional): protocol used for port-channel.Default value is False
            disable_switchport(`str`,optional): disable switchport.Default value is False
        Returns:
            None
    """

    for intf in interfaces:
        config_cmd="interface {interface}\n".format(interface=intf)
        if disable_switchport:
            config_cmd+="no switchport\n"
        config_cmd+="no shutdown\n"
        if channel_protocol:
            config_cmd+="no channel-protocol {channel_protocol}\n".format(
                                      channel_protocol=channel_protocol)
        config_cmd+="no channel-group {channel_group} mode {mode}\n".format(
                                  channel_group=channel_group, mode=mode)
        try:
            device.configure(config_cmd)
            log.info(
                "Successfully removed {intf} on "
                "channel-group {channel_group} in {mode} mode".format(
                    intf=intf, mode=mode, channel_group=channel_group
                )
            )
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Couldn't remove {intf} on"
                "channel-group {channel_group} in {mode} mode. Error:\n{error}"\
                    .format(intf=intf, mode=mode, channel_group=channel_group,
                            error=e
                )
            )

def unconfigure_ipv6_enable(device, interface):
    """ Disable ipv6
        Args:
            device (`obj`): Device object
            interface ('str'): interface name to disable ipv6
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfiguring ipv6 enable under {interface}".format(interface=interface))
    cmd = []
    cmd.append("interface {interface}".format(interface=interface))
    cmd.append("no ipv6 enable")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure ipv6 enable under {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )

def configure_interface_service_policy(device, interface, policy_name, direction):

    """ Configure any service policy configured under interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to remove service policy from
            policy_name ('str') : service policy name
            direction (`dict`): direction of service policy

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    configs = [f"interface {interface}", f"service-policy {direction} {policy_name}"]
    try:
        output = device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure service-policy on iterface:\n{e}"
        )
    return output

def configure_switchport_trunk_vlan(device, interface, vlan):

    """ configure switchport trunk vlan on Interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to port channel to be added
            vlan (`str`): vlan Id to be added
        Returns:
            None
    """
    log.debug(f"Configuring switchport trunk vlan on {interface}")

    try:
        device.configure(
            [
                f"interface {interface}",
                f"switchport access vlan {vlan}",
                "switchport mode access"
            ]
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure switchport trunk vlan on {interface}. Error:\n{e}"
        )

def configure_switchport_trunk_vlan_with_speed_and_duplex(device, interface, vlan, speed, duplex, service_policy_type, policy_map_name):

    """ configure switchport trunk vlan on Interface with speed and duplex type
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to port channel to be added
            vlan (`str`): vlan Id when this port is in access mode
            speed(`str`): Speed to added (i.e 10 Mbps/100 Mbps/1000 Mbps/auto)
            duplex(`str`): Duplex type to added (i.e auto/half/full)
            service_policy_type(`str`): Service-policy type to added (i.e input/output)
            policy_map_name(`str`): policy-map name to added
        Returns:
            None
    """
    log.debug(f"Configuring switchport trunk vlan on {interface} with speed and duplex")

    try:
        device.configure(
            [
                f"interface {interface}",
                f"switchport access vlan {vlan}",
                "switchport mode access",
                f"speed {speed}",
                f"duplex {duplex}",
                f"service-policy {service_policy_type} {policy_map_name}",
            ]
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure switchport trunk vlan with speed and duplex on {interface}. Error:\n{e}")

def configure_vfi(device, vlan,vpls):
    """ Vlan VFI configuration
        Args:
            device (`obj`): Device object
            vlan ('int'): VLAN id for VFI
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("interface vlan {vlan}".format(vlan=vlan))
    configs.append("member vfi {vpls}".format(vpls=vpls))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure VFI, VLAN {vlan} with the provided parameters".format(vlan=vlan)
        )

def unconfigure_vfi(device, vlan,vpls):
    """ Vlan VFI configuration
        Args:
            device (`obj`): Device object
            vlan ('int'): VLAN id for VFI
            vpls ('str'): vpls name to be configured
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("interface vlan {vlan}".format(vlan=vlan))
    configs.append("no member vfi {vpls}".format(vpls=vpls))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure VFI, VLAN {vlan} with the provided parameters".format(vlan=vlan)
        )

def configure_span_monitor_session(device, session_number, source_int, source_option, destination_int):

     """ Configure span monitor session
         Args:
             device ('obj'): Device object
             session_number ('int'): session number
             source_int ('str') : source interface name
             source_option ('str'): name of the source option
             destination_int ('str'): name of the destination interface
         Returns:
             None
         Raises:
             SubCommandFailure
     """
     configs = []
     configs.append(f"monitor session {session_number}  source interface {source_int} {source_option}")
     configs.append(f"monitor session {session_number}  destination interface {destination_int}")

     try:
         device.configure(configs)
     except SubCommandFailure as e:
         raise SubCommandFailure(
             f"Failed to configure span monitor session on interface:\n{e}"
         )

def unconfigure_span_monitor_session(device,session_number):

     """ Unconfigure span monitor session
         Args:
             device ('obj'): Device object
             session_number ('int'): session number
         Returns:
             None
         Raises:
             SubCommandFailure
     """
     configs = []
     configs.append(f"no monitor session {session_number}")

     try:
         device.configure(configs)
     except SubCommandFailure as e:
         raise SubCommandFailure(
             f"Failed to unconfigure span monitor session:\n{e}"
         )

def configure_port_channel_standalone_disable(device, port_channel_num):

    """ Configure no port-channel standalone disable command on Port-channel interface

        Args:
            device (`obj`): Device object
            port_channel_num('str'): Port-channel number for the Port-channel interface
            Example : interface Port-channel {100}
                         no port-channel standalone-disable
        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            [
            "interface Port-channel {po_interface_num}".
            format(po_interface_num=port_channel_num),
            "no port-channel standalone-disable"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure interface Port-channel {po_interface_num} standalone-disable command".
            format(po_interface_num =port_channel_num, error=e
            )
        )

def unconfigure_port_channel_standalone_disable(device,port_channel_num):

    """ Unconfigure port-channel standalone disable command on port-channel interface

        Args:
            device (`obj`): Device object
            port_channel_num('str'): Port-channel number for the Port-channel interface
            Example : interface Port-channel {100}
                          port-channel standalone-disable

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            [
            "interface Port-channel {po_interface_num}".
            format(po_interface_num=port_channel_num),
            "port-channel standalone-disable"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure interface Port-channel {po_interface_num} standalone-disable command".
            format(po_interface_num = port_channel_num, error=e
            )
        )


def configure_pppoe_enable_interface(device, interface, name, dial_pool_num=None,
                ppp_max_payload=None):
    """ Configure pppoe enable group on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            name (`str`): pppoe/bba group name
            dial_pool_num ('str'): pppoe-client dial-pool-member <dial_pool_num>
            ppp_max_payload ('str', optional): pppoe-client ppp-max-payload <ppp_max_payload>
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if not device.is_connected():
        connect_device(device=device)

    cli = []
    cli.append(f"interface {interface}")
    cli.append(f"pppoe enable group {name}")
    if dial_pool_num:
        cli.append(f"pppoe-client dial-pool-number {dial_pool_num}")
    if ppp_max_payload:
        cli.append(f"pppoe-client ppp-max-payload {ppp_max_payload}")

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not configure pppoe group on device. Error:\n{str(error)}"
        )

def unconfigure_pppoe_enable_interface(device, interface, name, dial_pool_num=None,
                ppp_max_payload=None):
    """ Configure pppone enable group on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            name (`str`): pppoe/bba group name
            ppp_max_payload ('str', optional): no pppoe-client ppp-max-payload <ppp_max_payload>
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    if not device.is_connected():
        connect_device(device=device)

    cli = []
    cli.append(f"interface {interface}")
    cli.append(f"no pppoe enable group {name}")
    if dial_pool_num:
        cli.append(f"no pppoe-client dial-pool-number {dial_pool_num}")
    if ppp_max_payload:
        cli.append(f"no pppoe-client ppp-max-payload {ppp_max_payload}")

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not unconfigure pppoe group on device. Error:\n{str(error)}"
        )


def configure_hsrp_interface(device, interface, version, ip_address=None, priority=None,
                             preempt=None, hello_interval=None, hold_time=None, group_number=None,
                             ipv6_address=None, mask=None, link_local=None, ipv6_prefix=None,
                             preempt_delay=None, auto_config=None, delay_type=None, delay_time=None):
    """ Configure hsrp on interface
        Args:
            device ('obj'): Device object
            interface ('str'): Interface to configure hsrp
            version ('int'): version number
            ip_address ('str', optional) : ipv4 address
            group_number ('int', optional) : group number limit 0-255
            priority ('str', optional) : config custom priority to hsrp , limit <0-255> (Default priority value is 100)
            preempt ('str', optional) : config custom preempt delay sync to hsrp
            hello_interval ('str', optional) : config the hello time for hsrp session , limit is 1 to 154 sec
            hold_time ('str', optional) : config the hold time for hsrp session , limit is 254 to 255 sec
            ipv6_address ('str', optional) : ipv6 address
            mask ('str', optional) : mask for ipv6 address
            link_local ('str', optional) : IPv6 link-local address
            ipv6_prefix ('str', optional) : IPv6 prefix address
            preempt_delay ('str', optional) : boolian , Wait before preempting
            auto_config ('str', optional) : boolian true to enable auto config
            delay_type ('str', optional) : preempt delay type can be minimum, reload or sync
            delay_time ('int', optional) : preempt delay timer <0-3600>  Number of seconds for delay type
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append(f"interface {interface}")
    configs.append(f"standby version {version}")
    if ip_address:
        configs.append(f"standby {group_number}  ip {ip_address}")
    if ipv6_address:
        if link_local:
            configs.append(f"standby {group_number} ipv6 {link_local}")
        if ipv6_prefix:
            configs.append(f"standby {group_number} ipv6 {ipv6_prefix}/{mask}")
        if auto_config:
            configs.append(f"standby {group_number} ipv6 autoconfig")
    if priority:
        configs.append(f"standby {group_number} priority {priority}")
    if preempt:
        configs.append(f"standby {group_number} preempt")
    if hello_interval and hold_time:
        configs.append(f"standby {group_number} timers {hello_interval} {hold_time}")
    if preempt_delay:
        configs.append(f"standby {group_number} preempt delay {delay_type} {delay_time}")

    try:
         device.configure(configs)
    except SubCommandFailure as e:
         raise SubCommandFailure(
            f"Failed to configure hsrp on interface. Error:\n{e}")


def configure_ipv6_mtu(device, intf, mtu):
    """ Configuring ipv6 mtu on  device
        Args:
            device ('obj'): Device object
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
             f"ipv6 mtu {mtu}",
            ]

        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 mtu  on interface. Error:\n{e}"
        )

def unconfigure_ipv6_mtu(device, intf, mtu):
    """ Unconfiguring ipv6 mtu on  device
        Args:
            device ('obj'): Device object
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
             f"no ipv6 mtu {mtu}",
            ]

        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ipv6 mtu  on interface. Error:\n{e}"
        )


def configure_crypto_map_on_interface(
    device,
    interface,
    map_name,
    ipv6=False
):
    """ Configure crypto map on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            map_name (`str`): Crypto Map name to be configured
            ipv6 ('bool'):  Indicate if this is ipv6 crypto map. Default false

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "configuring crypto map on interface {interface}"
    )

    # Build config string
    configs = f"interface {interface}\n"

    # Add ipv6 address configuration
    if not ipv6:
        configs += f"crypto map {map_name}\n"
    else:
        configs += f"ipv6 crypto map {map_name}\n"

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(f"Failed to configure crypto map in interface,"
             "Error:\n{e}"
        )
        raise

def unconfigure_crypto_map_on_interface(device, interface, ipv6=False):
    """ Unconfig crypto map on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ipv6 (`bool`): Indicate if this is ipv6 crypto map. Default false
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        f"Unconfiguring crypto map on interface {interface}"
    )

    # Build config string
    configs = f"interface {interface}\n"

    if not ipv6:
        configs += f"no crypto map\n"
    else:
        configs += f"no ipv6 crypto map\n"

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfig crypto map on interface {interface}. Error:\n{error}".format(
            interface=interface, error=e
            )
        )

def configure_mdns_on_interface_vlan(device, vlan, policy_name=None, act_qry_time=None):
    """ Configure mdns gateway on interface vlan
        Args:
            device ('obj'): Device object
            vlan ('int'): Vlan Id
            policy_name ('str'): LOCAL-AREA-POLICY which need to association to interface vlan
            act_qry_time ('int'): active-query timer value in seconds  <60-3600>
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if not device.is_connected():
        connect_device(device=device)

    cli = []
    cli.append(f"interface vlan {vlan}")
    cli.append(f"mdns-sd gateway")
    if policy_name:
        cli.append(f"service-policy {policy_name}")
    if act_qry_time:
        cli.append(f"active-query timer {act_qry_time}")

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not configure mdns gateway on interface vlan. Error:\n{str(error)}"
        )

def unconfigure_mdns_on_interface_vlan(device, vlan):
    """ Unconfigure mdns gateway on interface vlan
        Args:
            device ('obj'): Device object
            vlan ('int'): Vlan Id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if not device.is_connected():
        connect_device(device=device)

    cli = []
    cli.append(f"interface vlan {vlan}")
    cli.append(f"no mdns-sd gateway")

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not unconfigure mdns gateway on interface vlan. Error:\n{str(error)}"
        )

def enable_switchport_trunk_on_interface(device, interface):
    """ Enable switchport trunk on interface
        Args:
            device ('obj'): Device object
            interface ('str'): interface name to enable switchport trunk
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to enable switchport trunk on interface
    """
    log.debug(f"Enable switchport mode trunk on interface {interface}")

    configs = [
    f"interface {interface}",
    "switchport mode trunk"
    ]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to enable switchport mode trunk under {interface}. Error:\n{e}"
        )

def disable_autostate_on_interface(device, interface):
    """ Disable autostate on interface
        Args:
            device ('obj'): Device object
            interface ('str'): interface name to disable autostate
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to disable autostate on interface
    """
    log.debug(f"Disable autostate on interface {interface}")

    configs = [
        f"interface {interface}",
        "no autostate"
    ]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to disable autostate under {interface}. Error:\n{e}"
        )

def configure_access_session_port_control(device, interface, option='auto'):
    """ Disable autostate on interface
        Args:
            device ('obj'): Device object
            interface ('str'): interface name to disable autostate
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to disable autostate on interface
    """
    log.debug(f"configure_access_session_port_control on interface {interface}")

    configs = [
        f"interface {interface}",
        "access-session port-control " + option
    ]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure_access_session_port_control under {interface}. Error:\n{e}"
        )




def configure_ip_unnumbered_on_interface(device, interface, dest_interface, ipv6=False):
    """ configure ip unnumbered loopback on interface <interface>
        Args:
            device ('obj'): Device object
            interfaces('str'): interface details on which we config
            dest_interface('str'): Interface details on which ip unnumbered is going to apply (i.e - Loopback0)
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure ip unnumbered loopback on interface
    """

    log.debug(f"Add ip unnumbered loopback on interface {interface}")

    configs = [
        f"interface {interface}"
    ]

    if ipv6:
        configs.append(f"ipv6 unnumbered {dest_interface}")
    else:
        configs.append(f"ip unnumbered {dest_interface}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to add ip unnumbered loopback on interface {interface}. Error:\n{e}"
        )


def configure_switchport_trunk_allowed_vlan(device, interface, vlan_id):
    """ Configure switchport trunk allowed vlan on interface <interface>
        Args:
            device ('obj'): Device object
            interface('str'): interface details on which we config
            vlan_id('int'): VLAN IDs of the allowed VLANs
        Returns:
            None
        Raises:
            SubCommandFailure :Failed to Configure switchport trunk allowed vlan on interface
    """

    log.debug(f"Configure switchport trunk allowed vlan on interface {interface}")

    configs = [
        f"interface {interface}",
        f"switchport",
        f"switchport mode trunk",
        f"switchport trunk allowed vlan {vlan_id}"
    ]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to Configure switchport trunk allowed vlan on interface {interface}. Error:\n{e}"
        )

def configure_port_channel_lacp_max_bundle(device, port_channel_num, lacp_bundle_num):

    """ Configure lacp_max_bundle on the Port-channel interface

        Args:
            device (`obj`): Device object
            port_channel_num('str'): Port-channel number for the Port-channel interface
            lacp_bundle_num('str'): <1-8>  Max number of ports to bundle in this Port Channel
            Example : interface Port-channel {100}
                         lacp max-bundle {1}
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
            f"interface Port-channel {port_channel_num}",
            f"lacp max-bundle {lacp_bundle_num}"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure interface Port-channel {port_channel_num} lacp max_bundle {lacp_bundle_num} command"
            )

def unconfigure_port_channel_lacp_max_bundle(device, port_channel_num, lacp_bundle_num):

    """ UnConfigure lacp_max_bundle on the Port-channel interface

        Args:
            device (`obj`): Device object
            port_channel_num('str'): Port-channel number for the Port-channel interface
            lacp_bundle_num('str'): <1-8>  Max number of ports to bundle in this Port Channel
            Example : interface Port-channel {100}
                         no lacp max-bundle {1}
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
            f"interface Port-channel {port_channel_num}",
            f"no lacp max-bundle {lacp_bundle_num}"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure interface Port-channel {port_channel_num} lacp max_bundle {lacp_bundle_num} command"
            )

def configure_interface_speed(device, interface, speed_mbps):
    """ Configure speed on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            speed_mbps (`int`): speed mbps
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring speed {speed_mbps} on interface {interface}".format(
            speed_mbps=speed_mbps, interface=interface
        )
    )

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "speed {speed_mbps}".format(speed_mbps=speed_mbps),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure speed on {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )

def unconfigure_ip_route_cache(device, interface):
    """ Unconfigure ip route-cache on interface <interface>
        Args:
            device ('obj'): Device object
            interface('str'): interface details on which we config
        Returns:
            None
	    Raises:
            SubCommandFailure : Failed to unconfigure ip route-cache
    """

    log.debug(f"Unconfigure ip route-cache on interface {interface}")

    configs = [
        f"interface {interface}",
        "no ip route-cache"
    ]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip route-cache on interface {interface}. Error:\n{e}"
        )

def configure_interface_duplex(device, interface, duplex_mode):
    """ Configure duplex operation on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            duplex_mode (`str`): duplex operation
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring duplex {duplex_mode} on interface {interface}".format(
            duplex_mode=duplex_mode, interface=interface
        )
    )

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "duplex {duplex_mode}".format(duplex_mode=duplex_mode),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure duplex on {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )

def configure_ip_igmp_static_group(device, interface, static_group, source_ip=None):
    """ configures ip igmp static-group in interface level

    Args:
        device ('obj'): device to use
        interface ('str'): interface/svi to be configured
        static_group ('str'): static ip address to be configured
        source_ip ('str'): source_ip address to be configured

    Returns:
        None

    Raises:
        SubCommandFailure
    """


    cmd = [f"interface {interface}"]
    if source_ip:
        cmd.append(f"ip igmp static-group {static_group} source {source_ip}")
    else:
        cmd.append(f"ip igmp static-group {static_group}")
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure static-group Address on interface. Error:\n{e}"
        )


def configure_ipv6_mld_static_group(device, interface, static_group, ipv6_addr=None):
    """ configures ipv6 mld static-group in interface level

    Args:
        device ('obj'): device to use
        interface ('str'): interface/svi to be configured
        static_group ('str'): static group address to be configured
        ipv6_addr ('str'): ipv6_addr address to be configured

    Returns:
        None

    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}"]
    if ipv6_addr:
        cmd.append(f"ipv6 mld static-group {static_group} {ipv6_addr}")
    else:
        cmd.append(f"ipv6 mld static-group {static_group}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 mld static-group Address on interface "
            f"{interface}.Error:\n{e}"
        )

def configure_ip_igmp_join_group(device, interface, join_group, source_ip):
    """ configures ip igmp join-group in interface level

    Args:
        device ('obj'): device to use
        interface ('str'): interface/svi to be configured
        join_group ('str'): join group address to be configured
        source_ip ('str'): source_ip address to be configured

    Returns:
        None

    Raises:
        SubCommandFailure
    """
    cmd = [
            f"interface {interface}",
            f"ip igmp join-group {join_group} source {source_ip}",
          ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure join-group Address on interface. Error:\n{e}"
        )

def tunnel_range_shut_unshut(device,
        start,
        end,
        action="shut"):
    """ Perform shut or unshut of tunnel range interfaces
        Args:
             device (`obj`): Device object
             start ('int'): tunnel start number
             end (`int`): tunnel start number
             action ('str', optional) : shut or unshut(Default is shut)
    """
    configs = []
    configs.append(f"interface range Tunnel {start}-{end}")
    configs.append(f"{action}")

    try:
         device.configure(configs)
    except SubCommandFailure as e:
         raise SubCommandFailure(
             f"Failed to shut or unshut Tunnel range:\n{e}"
         )

def configure_ipv4_dhcp_relay_helper_vrf(device, interface, ip_address, vrf):
    """ Configure helper IP on an interface with VRF

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            ip_address (`str`): helper IP address to be configured on interface
            vrf ('str'): VRF to be configured

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd_1 = f"interface {interface}"
    cmd_2 = f"ip helper-address vrf {vrf} {ip_address}"

    # Configure device
    try:
        device.configure([cmd_1, cmd_2])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure helper IP address {ip} on interface with VRF"
            "{interface} on device {dev}. Error:\n{error}".format(
                ip=ip_address,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )


def unconfigure_ipv4_dhcp_relay_helper_vrf(device, interface, ip_address, vrf):
    """ Unconfigure helper IP on an interface with VRF

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            ip_address (`str`): helper IP address to be configured on interface
            vrf ('str'): VRF to be configured

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd_1 = f"interface {interface}"
    cmd_2 = f"no ip helper-address vrf {vrf} {ip_address}"

    # Configure device
    try:
        device.configure([cmd_1, cmd_2])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure helper IP address {ip} on interface with VRF"
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e,
            )
        )


def configure_vrf_select_source(device, interface):
    """ Configure VRF select source on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd_1 = f"interface {interface}"
    cmd_2 = f"ip vrf select source"

    # Configure device
    try:
        device.configure([cmd_1, cmd_2])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure VRF select source on interface"
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e,
            )
        )


def unconfigure_vrf_select_source(device, interface):
    """ Unconfigure VRF select source on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd_1 = f"interface {interface}"
    cmd_2 = f"no ip vrf select source"

    # Configure device
    try:
        device.configure([cmd_1, cmd_2])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure VRF select source on interface"
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e,
            )
        )

def configure_power_inline( device, interface, mode = 'auto', watts_value='', action='', portlevel_config = ''):

    """ Configure power inline on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to configure
            mode ('str') : Mode to configure (Default is auto)
            watts_value ('int') : Power value to configure
            action ('str') : Commands to configure under police mode
            portlevel_config ('str') : Commands to configure under port mode

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = f"interface {interface}\n"

    if watts_value and mode == 'consumption':
        cmd += f"power inline consumption {watts_value}"
    elif action and mode == 'police':
        cmd += f"power inline police action {action}"
    elif portlevel_config and mode == 'port':
        cmd += f"power inline port {portlevel_config}"
    elif watts_value:
        cmd += f"power inline {mode} max {watts_value}"
    elif mode == 'four-pair':
        cmd += f"power inline {mode} forced"
    else:
        cmd += f"power inline {mode}"
    # Configure power inline on interface
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure power line on interface"
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device,
                error=e,
            )
        )


def unconfigure_power_inline( device, interface, mode = 'auto', watts_value='', action='', portlevel_config = ''):

    """ Unconfigure power inline on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to unconfigure
            mode ('str') : Mode to unconfigure (Default is auto)
            watts_value ('int') : Power value to unconfigure
            action ('str') : Commands to unconfigure under police mode
            portlevel_config ('str') : Commands to unconfigure under port mode

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = f"interface {interface}\n"

    if watts_value and mode == 'consumption':
        cmd += f"no power inline consumption {watts_value}"
    elif action and mode == 'police':
        cmd += f"no power inline police action {action}"
    elif portlevel_config and mode == 'port':
        cmd += f"no power inline port {portlevel_config}"
    elif watts_value:
        cmd += f"no power inline {mode} max {watts_value}"
    else:
        cmd += f"no power inline {mode}"
    # Configure power inline on interface
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure power line on interface"
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device,
                error=e,
            )
        )

def confgiure_port_channel_min_link(device, port_channel_num, min_link):
    """ configure port-channel min links

        Args:
            device (`obj`): Device object
            port_channel_num('str'): Port-channel number for the Port-channel interface
            min_link('int'): <2-8>  The minimum number of bundled ports needed before this port channel can come up.

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface port-channel {port_channel_num}')
    cmd.append(f'port-channel min-links {min_link}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure {min_link} minimum links on port-channel {port_channel_num}. Error:\n{e}")

def unconfgiure_port_channel_min_link(device, port_channel_num):
    """ unconfigure port-channel min links

        Args:
            device (`obj`): Device object
            port_channel_num('str'): Port-channel number for the Port-channel interface

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface port-channel {port_channel_num}')
    cmd.append('no port-channel min-links')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure minimum links on port-channel {port_channel_num}. Error:\n{e}")

def configure_interface_channel_group_auto_lacp(device, interface):
    """ Configure auto Enable LACP auto on this interface

    Args:
        device ('obj'): device to use
        interface ('str') : interface to add configs
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('channel-group auto')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure auto Enable LACP auto on this interface {interface}. Error:\n{e}")

def unconfigure_interface_channel_group_auto_lacp(device, interface):
    """ Unconfigure auto Enable LACP auto on this interface

    Args:
        device ('obj'): device to use
        interface ('str') : interface to add configs
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no channel-group auto')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure auto Enable LACP auto on this interface {interface}. Error:\n{e}")

def unconfigure_interface_switchport_mode_access(device, interface):
    """ unconfigures switchport mode access on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to unconfigure

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config_list = []
    config_list.append(f'interface {interface}')
    config_list.append("no switchport mode access")

    try:
        device.configure(config_list)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigures switchport mode access on interface. Error:\n{error}"\
                .format(error=e
            )
        )

def configure_interface_macro_auto_port_sticky(device, interface):
    """ Configure macro auto port sticky on this interface
    Args:
        device ('obj'): device to use
        interface ('str') : interface to add configs

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('macro auto port sticky')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure macro auto port sticky on this interface {interface}. Error:\n{e}")

def unconfigure_interface_macro_auto_port_sticky(device, interface):
    """ Unconfigure macro auto port sticky on this interface
    Args:
        device ('obj'): device to use
        interface ('str') : interface to add configs

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no macro auto port sticky')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure macro auto port sticky on this interface {interface}. Error:\n{e}")

def configure_interface_template_sticky(device, interface, timer=None):
    """ configure interface-template sticky
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            timer ('int', optional): <1-65535>  Enter a value between 1 and 65535

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r'.*Do you wish to continue\?\s\[yes\]\:',
                action='sendline()',
                loop_continue=True,
                continue_timer=False
            )
        ]
    )

    cmd = []
    cmd.append(f'interface {interface}')
    if timer:
        cmd.append(f'access-session interface-template sticky timer {timer}')
    else:
        cmd.append('access-session interface-template sticky')
    try:
        device.configure(cmd,reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure interface-template sticky on this interface {interface}. Error:\n{e}")

def unconfigure_interface_template_sticky(device, interface, timer=None):
    """ unconfigure interface-template sticky
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            timer ('int', optional): <1-65535>  Enter a value between 1 and 65535

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    if timer:
        cmd.append(f'no access-session interface-template sticky timer {timer}')
    else:
        cmd.append('no access-session interface-template sticky')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure interface-template sticky on this interface {interface}. Error:\n{e}")

def configure_interface_inherit_disable(device, interface, disable_option):
    """ Configure access-session inherit disable
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            disable_option('str') : Select option to disable
            ex:)
                autoconf                   Auto Conf
                interface-template-sticky  Interface Template Sticky
                service-policy             Service Policy

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append(f'access-session inherit disable {disable_option}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure access-session inherit disable on this interface {interface}. Error:\n{e}")

def unconfigure_interface_inherit_disable(device, interface, disable_option):
    """ Unconfigure access-session inherit disable
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            disable_option('str') : Select option to disable
            ex:)
                autoconf                   Auto Conf
                interface-template-sticky  Interface Template Sticky
                service-policy             Service Policy

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append(f'no access-session inherit disable {disable_option}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure access-session inherit disable on this interface {interface}. Error:\n{e}")

def unconfigure_control_policies(device, policy_name):
    """ Unconfigure policy-map on an device

        Args:
            device (`obj`): Device object
            policy_name (`str`): name of the policy
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cfg_lst = []
    cfg_lst.append(f"no policy-map type control subscriber {policy_name}")

    try:
        device.configure(cfg_lst)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure policy-map on device. Error:\n{e}")

def unconfigure_subinterface(
    device,
    physical_port,
    any_number
):
    """ UnConfigure subinterface
        Args:
            device ('obj'): device to use
            physical_port ('str'): physical port
            any_number ('str'): any number
    """
    cmd = [
            f"no interface {physical_port}.{any_number}"
          ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure subinterface")

def configure_interface_span_vlan_priority(device, interface, vlan, priority):
    """ Configures Spanning Tree vlan priority on port
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            vlan ('int') : vlan to configure
            priority ('int') : priority to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = [f"interface {interface}", f"spanning-tree vlan {vlan} priority {priority}"]
    try:
        device.configure(config_list)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not configure Interface Spanning Tree Vlan Priority, Error-\n{error}'
        )

def unconfigure_interface_span_vlan_priority(device, interface, vlan):
    """ Configures Spanning Tree vlan priority on port
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            vlan ('int') : vlan to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config_list = [f"interface {interface}", f"no spanning-tree vlan {vlan} priority"]
    try:
        device.configure(config_list)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not unconfigure Interface Spanning Tree Vlan Priority, Error-\n{error}'
        )

def configure_interface_span_cost(device, interface, cost):
    """ Configures Spanning Tree cost on port
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            cost ('int')      : cost to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config_list = [f"interface {interface}", f"spanning-tree cost {cost}"]
    try:
        device.configure(config_list)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not configure Interface Spanning Tree cost, Error-\n{error}'
        )

def unconfigure_interface_span_cost(device, interface):
    """ Unconfigures Spanning Tree cost on port
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config_list = [f"interface {interface}", f"no spanning-tree cost"]
    try:
        device.configure(config_list)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not unconfigure Interface Spanning Tree cost, Error-\n{error}'
        )


def configure_interface_switchport_port_security_violation(device, interface, violation_type):
    """ Configure switchport port-security violation
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            violation_type('str') : Select violation type
            ex:)
                 protect   Security violation protect mode
                 report    Security violation report only mode
                 restrict  Security violation restrict mode
                shutdown  Security violation shutdown mode

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append(f'switchport port-security violation {violation_type}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure switchport port-security violation on this interface {interface}. Error:\n{e}")


def unconfigure_interface_switchport_port_security_violation(device, interface):
    """ Unconfigure switchport port-security violation
        Args:
            device ('obj'): device to use
            interface ('str') : interface to remove configs

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no switchport port-security violation')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure switchport port-security violation on this interface {interface}. Error:\n{e}")


def configure_interface_dot1x_timeout_txp(device, interface, timeout):
    """ Configure DOT1x timeout for suppplicant retries
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            timeout ('int') : Timeout for supplicant retries

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append(f'dot1x timeout tx-period {timeout}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure DOT1x timeout for suppplicant retries on this interface {interface}. Error:\n{e}")


def unconfigure_interface_dot1x_timeout_txp(device, interface):
    """ Unconfigure DOT1x timeout for suppplicant retries
        Args:
            device ('obj'): device to use
            interface ('str') : interface to remove configs

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no dot1x timeout tx-period')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure DOT1x timeout for suppplicant retries on this interface {interface}. Error:\n{e}")


def configure_interface_span_vlan_priority(device, interface, vlan, priority):
    """ Configures Spanning Tree vlan priority on port
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            vlan ('int') : vlan to configure
            priority ('int') : priority to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = [f"interface {interface}", f"spanning-tree vlan {vlan} priority {priority}"]
    try:
        device.configure(config_list)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not configure Interface Spanning Tree Vlan Priority, Error-\n{error}'
        )


def configure_interface_dot1x_max_req(device, interface, retries):
    """ Configure DOT1x Max No. of Retries
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            retires ('int') : Max No. of Retries

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append(f'dot1x max-req {retries}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure DOT1x Max No. of Retries on this interface {interface}. Error:\n{e}")


def unconfigure_interface_dot1x_max_req(device, interface):
    """ Unconfigure DOT1x Max No. of Retries
        Args:
            device ('obj'): device to use
            interface ('str') : interface to remove configs

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no dot1x max-req')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure DOT1x Max No. of Retries on this interface {interface}. Error:\n{e}")


def unconfigure_interface_span_vlan_priority(device, interface, vlan):
    """ Configures Spanning Tree vlan priority on port
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            vlan ('int') : vlan to configure
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    config_list = [f"interface {interface}", f"no spanning-tree vlan {vlan} priority"]
    try:
        device.configure(config_list)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not unconfigure Interface Spanning Tree Vlan Priority, Error-\n{error}'
        )


def configure_interface_dot1x_max_reauth_req(device, interface, reattempts):
    """ Configure DOT1x Max No. of Reauthentication Attempts
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            reattempts ('int') : Max No. of Reauthentication Attempts

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append(f'dot1x max-reauth-req {reattempts}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure DOT1x Max No. of Reauthentication Attempts on this interface {interface}. Error:\n{e}")


def configure_interface_span_cost(device, interface, cost):
    """ Configures Spanning Tree cost on port
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            cost ('int')      : cost to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config_list = [f"interface {interface}", f"spanning-tree cost {cost}"]
    try:
        device.configure(config_list)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not configure Interface Spanning Tree cost, Error-\n{error}'
        )


def unconfigure_interface_dot1x_max_reauth_req(device, interface):
    """ Unconfigure DOT1x Max No. of Reauthentication Attempts
        Args:
            device ('obj'): device to use
            interface ('str') : interface to remove configs

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no dot1x max-reauth-req')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure DOT1x Max No. of Reauthentication Attempts on this interface {interface}. Error:\n{e}")


def unconfigure_interface_span_cost(device, interface):
    """ Unconfigures Spanning Tree cost on port
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    config_list = [f"interface {interface}", f"no spanning-tree cost"]
    try:
        device.configure(config_list)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not unconfigure Interface Spanning Tree cost, Error-\n{error}'
        )


def configure_interface_dot1x_eap_profile(device, interface, profile_name):
    """ Configure DOT1x EAP supplicant profile configuration
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            profile_name ('name') : EAP supplicant profile name

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append(f'dot1x supplicant eap profile {profile_name}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure DOT1x EAP supplicant profile configuration on this interface {interface}. Error:\n{e}")


def unconfigure_interface_dot1x_eap_profile(device, interface):
    """ Unconfigure DOT1x EAP supplicant profile configuration
        Args:
            device ('obj'): device to use
            interface ('str') : interface to remove configs

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no dot1x supplicant eap profile')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure DOT1x EAP supplicant profile configuration on this interface {interface}. Error:\n{e}")


def configure_interface_ip_verify_unicast_source(device, interface, reachable_option, suboptions="", no_switchport=True):
    """ configure interface ip verify unicast source
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            reachable_option ('str') : option for source reachability
            no_switchport ('bool', optional): configure no switchport. Default is True
            ex:)
                any  Source is reachable via any interface
                rx   Source is reachable via interface on which packet was received
            suboptions ('str') : sub commands
            ex:)
                <1-199>          IP access list (standard or extended)
                <1300-2699>      IP expanded access list (standard or extended)
                allow-default    Allow default route to match when checking source address
                allow-self-ping  Allow router to ping itself (opens vulnerability in verification)
                l2-src           Check packets arrive with correct L2 source address
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    if no_switchport:
        cmd.append('no switchport')
    if suboptions:
        cmd.append(f'ip verify unicast source reachable-via {reachable_option} {suboptions}')
    else:
        cmd.append(f'ip verify unicast source reachable-via {reachable_option}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip verify unicast source on interface. Error:\n{e}")

def unconfigure_interface_ip_verify_unicast(device, interface):
    """ unconfigure interface ip verify unicast
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no ip verify unicast')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure ip verify unicast on interface. Error:\n{e}")


def configure_interface_auth_vlan(device, interface, vlan):
    """ Configure authorize vlan on interface
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            vlan ('int') : VLAN ID to be configured

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append(f'authentication event fail action authorize vlan {vlan}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure authorize vlan on this interface {interface}. Error:\n{e}")


def unconfigure_interface_auth_vlan(device, interface):
    """ Unconfigure authorize vlan on interface
        Args:
            device ('obj'): device to use
            interface ('str') : interface to remove configs

        Returns:
            None

       Raises:
            SubCommandFailure
    """
    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no authentication event fail action authorize vlan')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure authorize vlan on this interface {interface}. Error:\n{e}")


def configure_interface_ipv6_verify_unicast_source(device, interface, reachable_option, suboptions="", no_switchport=True):
    """ configure interface ipv6 verify unicast source
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            reachable_option ('str') : option for source reachability
            no_switchport ('bool', optional): no switchport. Default is True
            ex:)
                any  Source is reachable via any interface
                rx   Source is reachable via interface on which packet was received
            suboptions ('str') : sub commands
            ex:)
                WORD           Access-list name
                allow-default  Allow default route to match when checking source address
                <cr>           <cr>
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f'interface {interface}']
    if no_switchport:
        cmd.append('no switchport')
    if suboptions:
        cmd.append(f'ipv6 verify unicast source reachable-via {reachable_option} {suboptions}')
    else:
        cmd.append(f'ipv6 verify unicast source reachable-via {reachable_option}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ipv6 verify unicast source on interface. Error:\n{e}")


def configure_interface_auth_vlan_no_resp(device, interface, vlan):
    """ Configure authorize vlan for no response on interface
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            vlan ('int') : VLAN ID to be configured

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append(f'authentication event no-response action authorize vlan {vlan}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure authorize vlan for no response on this interface {interface}. Error:\n{e}")


def unconfigure_interface_auth_vlan_no_resp(device, interface):
    """ Unconfigure authorize vlan for no response on interface
        Args:
            device ('obj'): device to use
            interface ('str') : interface to remove configs

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no authentication event no-response action authorize vlan')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure authorize vlan for no response on this interface {interface}. Error:\n{e}")


def unconfigure_interface_ipv6_verify_unicast(device, interface):
    """ unconfigure interface ipv6 verify unicast
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no ipv6 verify unicast')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure ipv6 verify unicast on interface. Error:\n{e}")

def configure_eui_64_over_ipv6_enabled_interface(device, interface, ipv6_address):
    """ Configures eui-64 over ipv6 enabled interface
        Args:
            device ('obj')       : device to use
            interface ('str')    : interface to configure
            ipv6_address ('str') : ipv6 address
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f"interface {interface}", f"ipv6 address {ipv6_address} eui-64"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure eui-64 over ipv6 enabled interface")

def unconfigure_eui_64_over_ipv6_enabled_interface(device, interface, ipv6_address):
    """ UnConfigures eui-64 over ipv6 enabled interface
        Args:
            device ('obj')       : device to use
            interface ('str')    : interface to configure
            ipv6_address ('str') : ipv6 address
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f"interface {interface}", f"no ipv6 address {ipv6_address} eui-64"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure eui-64 over ipv6 enabled interface")

def configure_ipv6_nd_dad_processing(device, interface, no_of_attempts):
    """ Configures ipv6 nd dad processing
        Args:
            device ('obj')         : device to use
            interface ('str')      : interface to configure
            no_of_attempts ('str') : Set IPv6 Duplicate Address Detection Transmits
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f"interface {interface}", f"ipv6 nd dad attempts {no_of_attempts}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ipv6 nd dad processing")

def unconfigure_ipv6_nd_dad_processing(device, interface, no_of_attempts):
    """ UnConfigures ipv6 nd dad processing
        Args:
            device ('obj')         : device to use
            interface ('str')      : interface to configure
            no_of_attempts ('str') : Set IPv6 Duplicate Address Detection Transmits
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f"interface {interface}", f"no ipv6 nd dad attempts {no_of_attempts}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ipv6 nd dad processing")

def configure_interface_ip_verify_unicast_reversepath(device, interface, reversepath_option="", no_switchport=True):
    """ configure interface ip verify unicast reverse-path
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            reversepath_option ('str') : Reverse path validation of source address
            ex:)
                <1-199>          IP access list (standard or extended)
                <1300-2699>      IP expanded access list (standard or extended)
                allow-self-ping  Allow router to ping itself (opens vulnerability in verification)
            no_switchport ('bool', optional): configure no switchport. Default is True
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    if no_switchport:
        cmd.append('no switchport')
    if reversepath_option:
        cmd.append(f'ip verify unicast reverse-path {reversepath_option}')
    else:
        cmd.append('ip verify unicast reverse-path')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure interface ip verify unicast reverse-path on interface. Error:\n{e}")

def configure_interface_ip_verify_unicast_notification(device, interface, threshold, no_switchport=True):
    """ configure interface ip verify unicast notification threshold
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            threshold ('str') :  Urpf NOTIFY drop rate threshold
            ex:)
                <0-4294967295>  Drop rate in pps triggering notify - 0 is any drops
            no_switchport ('bool', optional): configure no switchport. Default is True
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    if no_switchport:
        cmd.append('no switchport')
    cmd.append(f'ip verify unicast notification threshold {threshold}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip verify unicast notification threshold on interface. Error:\n{e}")

def configure_interface_ipv6_verify_unicast_reversepath(device, interface, reversepath_option="", no_switchport=True):
    """ configure interface ipv6 verify unicast reverse-path
        Args:
            device ('obj'): device to use
            interface ('str') : interface to add configs
            reversepath_option ('str') : Reverse path validation of source address
            ex:)
                WORD  Access-list name
                <cr>  <cr>
            no_switchport ('bool', optional): configure no switchport. Default is True
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    if no_switchport:
        cmd.append('no switchport')
    if reversepath_option:
        cmd.append(f'ipv6 verify unicast reverse-path {reversepath_option}')
    else:
        cmd.append('ipv6 verify unicast reverse-path')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ipv6 verify unicast reverse-path on interface. Error:\n{e}")

def configure_interface_switchport_block_address(device, interface, address_type):
    """ Configures Interface Switchport block
        Args:
            device ('obj')       : device to use
            interface ('str')    : interface to configure
            address_type ('str') : address type to block (i.e multicast or unicast)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                f"interface {interface}",
                f"switchport block {address_type}",
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure Interface Switchport block'
        )

def unconfigure_interface_switchport_block_address(device, interface, address_type):
    """ Unconfigures Interface Switchport block
        Args:
            device ('obj')       : device to use
            interface ('str')    : interface to configure
            address_type ('str') : address type to unblock (i.e multicast or unicast)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                f"interface {interface}",
                f"no switchport block {address_type}",
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure Interface Switchport block'
        )

def configure_interface_logging_event(device, interface, event_type):
    """ Configures Interface Logging Event
        Args:
            device ('obj')       : device to use
            interface ('str')    : interface to configure
            event_type ('str')   : loggint event type (i.e bundle-status, link-status,
                                   nfas-status, power-inline-status, etc )
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                f"interface {interface}",
                f"logging event {event_type}",
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure Interface Logging Event'
        )

def unconfigure_interface_logging_event(device, interface, event_type):
    """ Unconfigures Interface Logging Event
        Args:
            device ('obj')       : device to use
            interface ('str')    : interface to configure
            event_type ('str')   : loggint event type (i.e bundle-status, link-status,
                                   nfas-status, power-inline-status, etc )
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                f"interface {interface}",
                f"no logging event {event_type}",
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure Interface Logging Event'
        )
def unconfigure_ipv4_dhcp_relay_helper(device, interface, ip_address):
    """ Unconfigure helper IP on an interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            ip_address (`str`): helper IP address to be unconfigured on interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
              f"interface {interface}",
              f"no ip helper-address {ip_address}"
          ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure helper IP address {ip_address} on interface {interface}"
            )

def unconfigure_ipv4_dhcp_relay_helper(device, interface, ip_address):
    """ Unconfigure helper IP on an interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            ip_address (`str`): helper IP address to be unconfigured on interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
              f"interface {interface}",
              f"no ip helper-address {ip_address}"
          ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure helper IP address {ip_address} on interface {interface}"
            )

def unconfigure_ipv6_dhcp_relay(device, interface, dest_ipv6, vlan):
    """ Unconfigure IPv6 DHCP Relay
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured
            dest_ipv6 ('str'): IPv6 destination address
            vlan ('int'): vlan number
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring IPv6 DHCP Relay
    """
    cmd = [
              f"interface {interface}",
              f"no ipv6 dhcp relay destination {dest_ipv6} {vlan}"
          ]
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            f"Could not unconfigure IPv6 DHCP Relay address {dest_ipv6} on interface {interface}"
            )

def configure_interface_switchport_dot1q_ethertype(device, interface, ethervalue):
    """ Configures switchport on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            ethervalue ('str'): Configure ethertype
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring switchport on {interface} with ethertype = {ethervalue}"\
            .format(interface=interface, ethervalue=ethervalue
        )
    )

    config_list=["interface {interface}".format(interface=interface),\
        "switchport dot1q ethertype {ethervalue}".format(ethervalue=ethervalue)]

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure switchport dot1q ethertype. Error:\n{error}"\
                .format(error=e
            )
        )
def unconfigure_interface_switchport_dot1q_ethertype(device, interface, ethervalue):
    """ unConfigures switchport on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to unconfigure
            ethervalue ('str'): unConfigure ethertype
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "unConfiguring switchport on {interface} with ethertype = {ethervalue}"\
            .format(interface=interface, ethervalue=ethervalue
        )
    )

    config_list=["interface {interface}".format(interface=interface),\
        "no switchport dot1q ethertype {ethervalue}".format(ethervalue=ethervalue)]

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure switchport dot1q ethertype. Error:\n{error}"\
                .format(error=e
            )
        )

def configure_hsrp_version_on_interface(device, interface, version):
    """ Configure hsrp version on interface
        Args:
             device (`obj`): Device object
             interface ('str'): Interface to configure hsrp
             version (`int`): version number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = [f"interface {interface}",
               f"standby version {version}"]
    try:
         device.configure(configs)
    except SubCommandFailure as e:
         raise SubCommandFailure(
             f"Failed to configure hsrp version on interface. Error:\n{e}"
         )

def configure_ipv6_address_on_hsrp_interface(device, interface, version, ipv6_address, priority=None,
        preempt=None, hello_interval=None, hold_time=None):
    """ Configure ipv6 address on hsrp interface
        Args:
             device (`obj`): Device object
             interface ('str'): Interface to configure hsrp
             version (`int`): version number
             ipv6_address ('str') : ipv6 address
             priority ('str', optional) : config custom priority to hsrp
             preempt ('str', optional) : config custom preempt delay sync to hsrp
             hello_interval ('str', optional) : config the hello time for hsrp session
             hold_time ('str', optional) : config the hold time for hsrp session
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = [f"interface {interface}",
               f"standby {version} ipv6 {ipv6_address}"]
    if priority:
        configs.append(f"standby {version}  priority {priority}")
    if preempt:
        configs.append(f"standby {version}  preempt delay sync {preempt}")
    if hello_interval and hold_time:
        configs.append(f"standby {version} timers {hello_interval} {hold_time}")

    try:
         device.configure(configs)
    except SubCommandFailure as e:
         raise SubCommandFailure(
             f"Failed to configure ipv6 address on hsrp interface. Error:\n{e}"
         )

def configure_interface_ip_tcp_adjust_mss(device, interface, mss_size):
    """ Configure ip tcp adjust-mss on interface
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            mss_size('int')   : Maximum segment size in bytes
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no switchport')
    cmd.append(f'ip tcp adjust-mss {mss_size}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip tcp adjust-mss on interface. Error:\n{e}")

def unconfigure_interface_ip_tcp_adjust_mss(device, interface):
    """ Unconfigure ip tcp adjust-mss on interface
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append(f'no ip tcp adjust-mss')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure ip tcp adjust-mss on interface. Error:\n{e}")

def configure_interface_ipv6_tcp_adjust_mss(device, interface, mss_size):
    """ Configure ipv6 tcp adjust-mss on interface
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            mss_size('int')   : Maximum segment size in bytes
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no switchport')
    cmd.append(f'ipv6 tcp adjust-mss {mss_size}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ipv6 tcp adjust-mss on interface. Error:\n{e}")

def unconfigure_interface_ipv6_tcp_adjust_mss(device, interface):
    """ Unconfigure ipv6 tcp adjust-mss on interface
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append(f'no ipv6 tcp adjust-mss')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure ipv6 tcp adjust-mss on interface. Error:\n{e}")


def unconfigure_interface_access_session(device, interface):
    """ Unconfigure interface access-session
        Args:
            device ('obj'): device to use
            interface ('str') : interface to remove configs

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append(f'no access-session closed')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure interface access-session closed on this interface {interface}. Error:\n{e}")


def configure_vrrp_version_on_device(device, version):
    """ Configure vrrp version on interface
        Args:
             device (`obj`): Device object
             version('str'): configure the version
    """
    configs = []
    configs.append(f"fhrp version vrrp {version}")
    try:
         device.configure(configs)
    except SubCommandFailure as e:
         raise SubCommandFailure(
             f"Failed to configure vrrp version on device:\n{e}"
         )

def configure_vrrp_on_interface(device, interface, group_number, address_family,
        advertise_timer=None,priority=None,ip_address=None,option=None):
    """configure vrrp version on interface
       Args:
           device (`obj`): Device object
           interface ('str'): Interface to configure vrrp
           group_number (`int`): group number
           address_family('str'): configure the address family
           advertise_timer(int, optional): configure the advertise timer
           priority ('str', optional) : config custom priority to vrrp
           ip_address ('str', optional): configure the ip_address
           option ('str', optional) : configure ip adress is primary (or) secondary
    """
    configs = []
    configs.append(f"interface {interface}")
    configs.append(f"vrrp {group_number} address-family {address_family}")
    if advertise_timer:
        configs.append(f"timers advertise {advertise_timer}")
    if priority:
        configs.append(f"priority {priority}")
    if ip_address and option:
        configs.append(f"address {ip_address} {option}")
    configs.append(f"exit-vrrp")
    try:
         device.configure(configs)
    except SubCommandFailure as e:
         raise SubCommandFailure(
             f"Failed to configure ip address on vrrp interface:\n{e}"
         )

def config_link_local_ip_on_interface(device, interface, ipv6_address=None):
    """ config link_local ip on interface
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            ipv6_address (`str`): IPv6 address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append(f"interface {interface}")
    if ipv6_address:
        configs.append(f"ipv6 address {ipv6_address} link-local")
    try:
         device.configure(configs)
    except SubCommandFailure as e:
         raise SubCommandFailure(
             f"Failed to configure link_local ip address on interface:\n{e}"
         )

def configure_tunnel_with_ipsec(
    device,
    tunnel_intf,
    overlay='ipv4',
    tunnel_ip=None,
    tunnel_mask=None,
    tunnel_src_ip=None,
    tunnel_dst_ip=None,
    keepalive_timer = None,
    ip_mtu = None,
    tunnel_ipv6=None,
    tunnel_maskv6=None,
    tunnel_mode='ipsec',
    tunnel_protection='ipsec',
    ipsec_profile_name=None,
    vrf=None,
    tunnel_vrf=None,
    v6_overlay=None
):
    """ Configure ipsec on Tunnel interface
        Args:
            device (`obj`): Device object
            tunnel_intf (`str`): Interface to get address
            overlay (`str`): Tunnel is eitehr IPv4 or Ipv6 or dual-overlay default value is ipv4
            tunnel_ip (`str`,optional): IPv4 addressed to be configured on interface
            tunnel_mask (`str`,optional): IPv4 Mask address to be used in configuration
            tunnel_src_ip (`str`): tunnel source address
            tunnel_dst_ip (`str`): tunnel destination address
            keepalive_timer ('int',optional): tunnel keepalive timer,default value is 10
            ip_mtu ('str',optional): tunnel mtu, default value is None
            tunnel_ipv6 (`str`,optional): IPv6 address with subnet mask,default value is None
            tunnel_maskv6 ('str',optional): IPv6 mask (Default None)
            tunnel_mode ('str',optional): Tunnel mode. Default is gre
            tunnel_protection ('str',optional): Protection type (i.e ipsec,dike)
            ipsec_profile_name ('str',optional): Tunnel protection profile name
            vrf ('str',optional): client vrf for  the tunnel
            tunnel_vrf ('str',optional): wan vrf for  the tunnel
            v6_overlay:('boolean', optional): True if v6-over-ipv4. Default is False
            """
    configs = []
    configs.append("interface {intf}".format(intf=tunnel_intf))
    #configure vrf (vrf to be configured before ip)
    if vrf:
        configs.append("vrf forwarding {vrf}".format(vrf=vrf))
    if tunnel_ip:
        configs.append("ip address {ip} {mask}".format(ip=tunnel_ip,mask=tunnel_mask))
    if tunnel_ipv6:
        if tunnel_maskv6:
            configs.append("ipv6 enable")
            configs.append("ipv6 address {ipv6}/{v6_mask}".format(ipv6=tunnel_ipv6, v6_mask=tunnel_maskv6))
        else:
            configs.append("ipv6 enable")
            configs.append("ipv6 address {ipv6}".format(ipv6=tunnel_ipv6))

    if tunnel_mode == 'gre':
        if overlay == 'ipv6':
            configs.append("tunnel mode {mode} ipv6".format(mode=tunnel_mode))
        else:
            configs.append("tunnel mode {mode} ip".format(mode=tunnel_mode))
    else:
        configs.append("tunnel mode {mode} {over}".format(mode=tunnel_mode, over=overlay))
    configs.append("tunnel source {ip}".format(ip=tunnel_src_ip))
    configs.append("tunnel destination {ip}".format(ip=tunnel_dst_ip))
    if keepalive_timer:
        configs.append("keepalive {timer}".format(timer=keepalive_timer))
    if ip_mtu:
        configs.append("ip mtu {mtu}".format(mtu=ip_mtu))
    if tunnel_vrf:
        configs.append("tunnel vrf {vrf}".format(vrf=tunnel_vrf))
    if tunnel_protection:
        configs.append("tunnel protection {tunnel_protection} profile {profile}".
                       format(tunnel_protection=tunnel_protection,profile=ipsec_profile_name))
    if v6_overlay:
        configs.append("tunnel mode ipsec {tunnel_mode} v6-overlay".format(tunnel_mode=tunnel_mode))
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure Tunnel interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=tunnel_intf,
                dev=device.name,
                error=e,
            )
        )

def configure_interface_lacp_fast_switchover(device, po_intf, dampening_time=None):
    """ configure interface lacp fast-switchover
        Args:
            device ('obj'): device to use
            po_intf ('str'): name of the port-channel interface to be configured
            dampening_time ('int', optional):  LACP Fast Switchover Hot-Standby Dampening Time in Seconds
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {po_intf}')
    if dampening_time:
        cmd.append(f'lacp fast-switchover dampening {dampening_time}')
    else:
        cmd.append('lacp fast-switchover')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure interface lacp fast-switchover on "
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=po_intf,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_interface_lacp_fast_switchover(device, po_intf):
    """ unconfigure interface lacp fast-switchover
        Args:
            device ('obj'): device to use
            po_intf ('str'): name of the port-channel interface to be unconfigured
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [
            f'interface {po_intf}',
            'no lacp fast-switchover'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure interface lacp fast-switchover on "
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=po_intf,
                dev=device.name,
                error=e,
            )
        )

def configure_interface_lacp_max_bundle(device, po_intf, max_port):
    """ configure interface lacp max-bundle
        Args:
            device ('obj'): device to use
            po_intf ('str'): name of the port-channel interface to be configured
            max_port ('int'): Max number of ports to bundle in this Port Channel
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [
            f'interface {po_intf}',
            f'lacp max-bundle {max_port}'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure interface lacp max-bundle on "
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=po_intf,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_interface_lacp_max_bundle(device, po_intf):
    """ unconfigure interface lacp max-bundle
        Args:
            device ('obj'): device to use
            po_intf ('str'): name of the port-channel interface to be unconfigured
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [
            f'interface {po_intf}',
            'no lacp max-bundle'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure interface lacp max-bundle on "
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=po_intf,
                dev=device.name,
                error=e,
            )
        )

def configure_interface_snmp_trap_mac_notification_change(device, interface, change_option):
    """ configure interface snmp trap mac-notification change
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured
            change_option ('str'): change option added/removed
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [
            f'interface {interface}',
            f'snmp trap mac-notification change {change_option}'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure interface snmp trap mac-notification change "
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_interface_snmp_trap_mac_notification_change(device, interface, change_option):
    """ unconfigure interface snmp trap mac-notification change
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be unconfigured
            change_option ('str'): change option added/removed
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [
            f'interface {interface}',
            f'no snmp trap mac-notification change {change_option}'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure interface snmp trap mac-notification change "
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e,
            )
        )

def configure_interface_default_snmp_trap_mac_notification_change(device, interface, change_option):
    """ configure interface default snmp trap mac-notification change
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured
            change_option ('str'): change option added/removed
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [
            f'interface {interface}',
            f'default snmp trap mac-notification change {change_option}'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure interface default snmp trap mac-notification change "
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e,
            )
        )

def configure_interface_flow_control(device, interface, flow_control_option):
    """ Configure flow control receive on this interface

    Args:
        device ('obj'): device to use
        interface ('str') : interface to add configs
        flow_control_option ('str') : flow control option to be configured
            ex:)
                desired  Allow but do not require flow-control packets on port
                off      Disable flow-control packets on port
                on       Enable flow-control packets on port
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f'interface {interface}',
           f'flowcontrol receive {flow_control_option}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure flow control receive on this interface {interface}. Error:\n{e}")

def unconfigure_interface_flow_control(device, interface):
    """ Unconfigure flow control receive on this interface

    Args:
        device ('obj'): device to use
        interface ('str') : interface to add configs
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f'interface {interface}',
           'no flowcontrol receive']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure flow control receive on this interface {interface}. Error:\n{e}")

def unconfigure_profile_on_tunnel_interface(
    device,
    interface,
    tunnel_protection=None,
    profile=None,
):
    """ Configure tunnel interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            tunnel_protection ('str',optional): Protection type (i.e ipsec,dike)
            profile ('str',optional): Tunnel protection profile name
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    configs = [f"interface {interface}"]
    if tunnel_protection is not None:
        configs.append(f"no tunnel protection {tunnel_protection} profile {profile}")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure profile on {interface}. Error:\n{e}")

def configure_power_efficient_ethernet_auto(device, interface):
    """ configure power efficient ethernet auto
	Args:
        device ('obj'): Device object
        interface ('str'): interface
    Returns:
        None
    Raises:
        SubCommandFailure: Failed configuring interface
    """
    cmd = [f"interface {interface}",
           "power efficient-ethernet auto"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
        'Could not configure power efficient ethernet auto on {interface}, Error:\n{e}'.format(
            interface=interface, error=e))


def configure_interface_monitor_session_shutdown(device, monitor_config):
    """ configure monitor session on device by doing no shut of the interface
        Args:
            device ('obj'): Device object
            monitor_config ('list') : List of monitor session configuration
                ex.)
                    monitor_config = [{
                            'session_name': 1,
                            'session_type': 'erspan-source',
                            'interface': 'GigabitEthernet10',
                            'vlan_id' : '100',
                            'erspan_id': 10,
                            'ip_address': '192.168.1.1',
                            'origin_ip_address': '192.168.1.2',
                            'ipv6_address': '2001::2',
                            'mtu': 1500,
                            'vrf': 'red',
                            'origin_ipv6_address': '2001::1'
                        },
                        {
                            'session_name': 2,
                            'session_type': 'erspan-destination',
                            'interface': 'GigabitEthernet11',
                            'erspan_id': 10,
                            'ip_address': '192.168.1.1'
                            'ipv6_address' : '2001::2'
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
                "monitor session {} type {}".format(
                    mc["session_name"], mc["session_type"]
                )
            )

            if 'interface' in mc:
               config.append("source interface {}".format(mc["interface"]))
            else:
               config.append("source vlan {}".format(mc["vlan_id"]))
            config.append("destination")
            config.append("erspan-id {}".format(mc["erspan_id"]))

            if 'ip_address' in mc:
               config.append("ip address {}".format(mc["ip_address"]))
               config.append("origin ip address {}".format(mc["origin_ip_address"]))
            else:
               config.append("ipv6 address {}".format(mc["ipv6_address"]))
               config.append("origin ipv6 address {}".format(mc["origin_ipv6_address"]))
        else:
            unshut_interface(device=device, interface=mc["interface"])
            config.append(
                "monitor session {} type {}".format(
                    mc["session_name"], mc["session_type"]
                )
            )
            config.append("destination interface {}".format(mc["interface"]))
            if 'vlan_id' in mc:
               config.append("destination vlan {}".format(mc["vlan_id"]))
            config.append("source")
            config.append("erspan-id {}".format(mc["erspan_id"]))
            if 'ip_address' in mc:
               config.append("ip address {}".format(mc["ip_address"]))
            else:
               config.append("ipv6 address {}".format(mc["ipv6_address"]))
        if 'description' in mc:
            config.append("description {}".format(mc["description"]))
        if 'source_vlan' in mc:
            config.append("source vlan {}".format(mc["source_vlan"]))
        if 'mtu' in mc:
            config.append("mtu {}".format(mc["mtu"]))
        if 'vrf' in mc:
            config.append("vrf {}".format(mc["vrf"]))
        config.append(f"exit")
        config.append(f"no shutdown")

        try:
            device.configure(config)
        except SubCommandFailure as e:
            raise SubCommandFailure(f"Could not configure monitor session. Error:\n{e}")


def configure_interface_switchport(device, interface):
    """ Configures Switchport interface
        Args:
            device ('obj') : device to use
            interface ('str') : interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f"interface {interface}", "switchport"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure switchport interface on {device}. Error:\n{error}".format(device=device, error=e)
        )


def configure_ip_dlep(device,
    physical_interface,
    virtual_template_number,
    udp_port=None,
    tcp_port=None,
    client_ip_address=None,
    client_tcp_port=None):
    """ Configure ip dlep on physical main/sub-interface

        Args:
            device (`obj`): Device object/device to use
            physical_interface('str'): physical interface(main or sub-interface)
            virtual_template_number ('int'): virtual template number
            udp_port ('int', optional): server/router udp port number
            tcp_port ('int', optional): server/router tcp port number
            client_ip_address ('str', optional): client/radio ip address
            client_tcp_port ('int', optional): client/radio tcp port number
        For the arguments that are optional, the default value is None.

        Returns:
            None

        Raises:
            SubCommandFailure

        Example:
            device.api.configure_ip_dlep(physical_interface='GigabitEthernet0/0/0',virtual_template_number=1)
    """

    cli = [f"interface {physical_interface}"]

    cmd = f"ip dlep vtemplate {virtual_template_number}"
    if udp_port:
        cmd += f" port {udp_port}"
    if  tcp_port:
        cmd += f" tcp port {tcp_port}"
    if client_ip_address:
        cmd += f" client ip {client_ip_address}"
    if client_tcp_port:
        cmd += f" port {client_tcp_port}"

    cli.append(cmd)

    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ip dlep on physical main/sub-interface interface on device. Error:\n{e}"
        )


def unconfigure_ip_dlep(device,
    physical_interface,
    virtual_template_number):
    """ Unconfigure ip dlep on physical main/sub-interface

        Args:
            device (`obj`): Device object/device to use
            physical_interface('str'): physical interface(main or sub-interface)
            virtual_template_number ('int'): virtual template number

        Returns:
            None

        Raises:
            SubCommandFailure

        Example:
            device.api.unconfigure_ip_dlep(physical_interface='GigabitEthernet0/0/0',virtual_template_number=1)
    """

    cli = [f"interface {physical_interface}",
           f"no ip dlep vtemplate {virtual_template_number}"]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ip dlep on physical main/sub-interface interface on device. Error:\n{e}"
        )


def configure_physical_interface_vmi(device, vmi_name, rar_interface_name, mode_op=None):
    """ configure vmi  interface
    Args:
        device (`obj`): Device object
        vmi_name(`str`): vmi interface name
        rar_interface_name (`str`): rar interface name
        mode_op(`str`, optional): vmi operation mode
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configure vmi interface
    Example:
        device.api.configure_physical_interface_vmi(vmi_name='vmi1',rar_interface_name='GigabitEthnernet0/0/0',mode_op='bypass')
    """

    log.info(f"Configure vmi  interface")

    cmd = [
            f"interface {vmi_name}",
            f"physical-interface {rar_interface_name}"
        ]
    if mode_op:
        cmd.append(f"mode {mode_op}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
                "Failed to configure vmi interface, Error:\n{e}"
            )

def unconfigure_interface_switchport_trunk_allowed_vlan(device, interfaces, vlan_id):

    """ unconfigure switchport mode trunk allowed vlan to the interface

        Args:
            device (`obj`): Device object
            interface (`list`): list of Interface to be added to port channel
            vlan (`str`): vlan to be added to the port
        Returns:
            None
    """
    log.info(
        "Unconfiguring switchport interface on {interfaces}".format(
            interfaces=interfaces
        )
    )
    config = []
    try:
        for intf in interfaces:
            config.append("interface {intf}".format(intf=intf))
            config.append("no switchport trunk allowed vlan {vlan_id}".format(vlan_id=vlan_id))
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure switchport on {interface}. Error:\n{error}"\
                        .format(interfaces=interfaces, error=e
            )
        )

def unconfigure_power_efficient_ethernet_auto(device, interface):
    """ Unconfigure power efficient ethernet auto
	Args:
        device ('obj'): Device object
        interface ('str'): interface
    Returns:
        None
    Raises:
        SubCommandFailure: Failed unconfiguring interface
    """
    cmd = [f'interface {interface}',
           f'no power efficient-ethernet auto']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
        f'Could not unconfigure power efficient ethernet auto on {interface}, Error:\n{e}')

def configure_ipv6_prefix_name_on_interface(device, interface, prefix_name, ipv6_prefix):
    """ configure ipv6 address with prefix name on interface
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            prefix_name ('str'): Prefix name
            ipv6_prefix (`str`): IPv6 address with prefix length. Ex: ::1/128.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f'interface {interface}', f'ipv6 address {prefix_name} {ipv6_prefix}']
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 address with prefix name on interface:\n{e}")


def configure_ipv6_dhcp_client_pd_on_interface(device, interface, prefix_name=None, rapid_commit=False,
                                               ipv6_prefix=None):
    """ configure ipv6 dhcp client pd on interface
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            prefix_name ('str', optional): Prefix name. Default is None.
            ipv6_prefix ('str', optional): IPv6 address with prefix length. Ex: ::1/128. Default is None.
            rapid_commit ('bool', optional): Rapid commit is valid if prefix name is not None. Default is False.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f'interface {interface}']
    if prefix_name:
        cmd.append(f"ipv6 dhcp client pd {prefix_name}{' rapid-commit' if rapid_commit else ''}")
    if ipv6_prefix:
        cmd.append(f'ipv6 dhcp client pd hint {ipv6_prefix}')
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 dhcp client pd on interface:\n{e}")

def configure_interface_ip_verify_source(device, interface, mode=''):
    """ Configures Ip Verify Source mode
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            mode ('str', optional) : Options are mac-chec. Default is '' (i.e no mode)
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f"interface {interface}", f"ip verify source {mode}"]
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure Ip verify source on Interface'
        )


def unconfigure_interface_ip_verify_source(device, interface):
    """ Unconfigures Ip Verify Source mode
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f"interface {interface}", f"no ip verify source"]
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure Ip verify source on Interface'
        )

def config_load_interval_on_interface(device, interface, interval):
    """ configure load interval on interface
        Args:
            device (`obj`): Device object
            interface ('str'): Interface to configure
            interval ('int'):  Load interval delay in seconds
        Returns:
            None
        Raise:
            SubCommandFailure: Failed to configure load interval on interface
    """
    log.debug("configure load interval on interface")
    try:
        device.configure([
                "interface {interface}".format(interface=interface),
                "load-interval {interval}".format(interval=interval)]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure load interval on interface. Error:\n{error}".format(
                error=e
            )
        )

def unconfig_diagnostic_monitor_threshold(device, switchnum, testid, allowedfailure):
    """ Unconfgure diagnostics monitor threshold on switch

        Args:
            device (`obj`): Device object
            switchnum (`int`): Switch Number
            testid (`int`): TestId
            allowedfailure (`int`): Number of allowed failure
        Return:
            None
        Raise:
            SubCommandFailure: Failed to unconfgure diagnostics monitor threshold on switch
    """

    try:
        device.configure(f"no diagnostic monitor threshold switch {switchnum} test {testid} failure count {allowedfailure}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfgure diagnostics monitor threshold on switch, Error: {error}'.format(error=e)
        )


def unconfigure_interface_switchport_port_security(device, interface, mode=None, mode_type=None):
    """ Unconfigure switchport port-security
        Args:
            device ('obj'): device to use
            interface ('str') : interface to remove configs
            mode ('str', optional): Port security mode. Ex: aging, maximum, violation. Default is None.
            mode_type ('str', optional): Mode type or address. Ex: static, time, mac address. Default is None.

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    cmd = [f'interface {interface}']
    if mode and mode_type:
        command = f'no switchport port-security {mode} {mode_type}'
    elif mode:
        command = f'no switchport port-security {mode}'
    else:
        command = 'no switchport port-security'

    cmd.append(command)
    try:

        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure switchport port-security on this interface {interface}. Error:\n{e}"
        )


def configure_switchport_protected(device, interface):
    """ Configure switchport protected
        Args:
            device ('obj'): device to use
            interface ('str') : Interface Name
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f'interface {interface}', 'switchport protected']
    try:

        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure switchport protected on this interface {interface}. Error:\n{e}"
        )


def unconfigure_switchport_protected(device, interface):
    """ Unconfigure switchport protected
        Args:
            device ('obj'): device to use
            interface ('str') : Interface Name
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f'interface {interface}', 'no switchport protected']
    try:

        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to Unconfigure switchport protected on this interface {interface}. Error:\n{e}"
        )


def configure_interface_keepalive(device, interface, timer=None):
    """ Configure interface keepalive timer
        Args:
            device ('obj'): device to use
            interface ('str') : Interface Name
            timer ('int', optional): Keepalive timer. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f'interface {interface}']
    if timer:
        cmd.append(f'keepalive {timer}')
    else:
        cmd.append(f'keepalive')
    try:

        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure interface keepalive timer on this interface {interface}. Error:\n{e}"
        )


def configure_interface_l2protocol_tunnel(device, interface, protocol=None, ptp_protocol=None, ptp_protocol_rate=None,
                                        threshold_rate=None, threshold_protocol=None):
    """ Configure interface l2protocol tunnel
        Args:
            device ('obj'): device to use
            interface ('str') : Interface Name
            protocol ('str', optional): l2protocol-tunnel protocol. Ex: cdp, lldp, drop-threshold. Default is None
            ptp_protocol ('str', optional): Point-to-Point protocol. Ex: lacp, pagp, udld. Default is None
            ptp_protocol_rate ('int', optional): Point-to-Point protocol packet rate. Default is None
            threshold_rate ('int', optional):  Packets/sec rate beyond which protocol packets will be
                                                    dropped. Default is None
            threshold_protocol ('str', optional): Threshold protocol. Ex: cdp, lldp, stp. Default is None

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f'interface {interface}']
    if protocol:
        command = f'l2protocol-tunnel {protocol}'
        if threshold_rate:
            command += f' {threshold_rate}'
        elif threshold_protocol:
            command += f' {threshold_protocol}'
        if ptp_protocol:
            command += f' {ptp_protocol}'
        if ptp_protocol_rate:
            command += f' {ptp_protocol_rate}'
    else:
        command = 'l2protocol-tunnel'

    cmd.append(command)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure interface l2protocol tunnel on this interface {interface}. Error:\n{e}"
        )


def unconfigure_interface_l2protocol_tunnel(device, interface, protocol=None, ptp_protocol=None, threshold_protocol=None
    ):
    """ Unconfigure interface l2protocol tunnel
        Args:
            device ('obj'): device to use
            interface ('str') : Interface Name
            protocol ('str', optional): l2protocol-tunnel protocol. Ex: cdp, lldp, drop-threshold. Default is None
            ptp_protocol ('str', optional): Point-to-Point protocol. Ex: lacp, pagp, udld. Default is None
            threshold_protocol ('str', optional): Threshold protocol. Ex: cdp, lldp, stp. Default is None

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f'interface {interface}']
    if protocol:
        command = f'no l2protocol-tunnel {protocol}'
        if threshold_protocol:
            command += f' {threshold_protocol}'
        if ptp_protocol:
            command += f' {ptp_protocol}'
    else:
        command = 'no l2protocol-tunnel'

    cmd.append(command)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to Unconfigure interface l2protocol tunnel on this interface {interface}. Error:\n{e}"
        )

def configure_interface_bandwidth(device, interface, bandwidth):
    """ Configures vlan group list
        Args:
            device ('obj'): device to use
            interface ('str'):  interface name
            bandwidth ('str'): bandwidth. Ex: '300000'
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring interface bandwidth on {device.name} {interface}")
    cmd = [f'interface {interface}',f'bandwidth {bandwidth}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure interface bandwidth. Error:\n{e}')

def unconfigure_interface_bandwidth(device, interface, bandwidth):
    """ unconfigures vlan group list
        Args:
            device ('obj'): device to use
            interface ('str'):  interface name
            bandwidth ('str'): bandwidth. Ex: '300000'
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring interface bandwidth on {device.name} {interface}")
    cmd = [f'interface {interface}',f'no bandwidth {bandwidth}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure interface bandwidth. Error:\n{e}')

def configure_monitor_erspan_source_interface(device, session, interface, traffic=''):
    """ Configures monitor erspan source on interface
        Example : monitor session 1 type erspan-source
                source interface TwentyFiveGigE2/0/33 rx
        Args:
            device ('obj'): device to use
            session ('int'): SPAN session number (Range: 1-66)
            interface ('str'): SPAN source interface (eg. Te 1/0/2)
            traffic ('str'): Monitor traffic type (eg. both, rx, tx)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring monitor erspan source on interface on {device.name}")
    config = [f'monitor session {session} type erspan-source',
                f'source interface {interface} {traffic}']
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure monitor erspan source on device {device.name}. Error:\n{e}'
        )

def unconfigure_monitor_erspan_source_interface(device, session, interface, traffic=''):
    """ Unconfigures monitor erspan source on interface
        Example : monitor session 1 type erspan-source
                no source interface TwentyFiveGigE2/0/33 rx
        Args:
            device ('obj'): device to use
            session ('int'): SPAN session number (Range: 1-66)
            interface ('str'): SPAN source interface (eg. Te 1/0/2)
            traffic ('str'): Monitor traffic type (eg. both, rx, tx)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring monitor erspan source on interface on {device.name}")
    config = [f'monitor session {session} type erspan-source',
                f'no source interface {interface} {traffic}']
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to unconfigure monitor erspan source on device {device.name}. Error:\n{e}'
        )


def configure_interface_authentication_violation(device, interface, violation_type):
    """ Configures Interface authentication violation
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            violation_type ('str'): authentication violation type. Ex: protect, replace, restrict
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = [f"interface {interface}", f"authentication violation {violation_type}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure Interface authentication violation. Error: {e}')


def unconfigure_interface_authentication_violation(device, interface):
    """ Unconfigures Interface authentication violation
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            violation_type ('str'): authentication violation type. Ex: protect, replace, restrict
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = [f"interface {interface}", "no authentication violation"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure Interface authentication violation. Error: {e}')

def config_ip_domain_lookup(device, interface=None, vlan_name=None):
    """ configure ip domain lookup
        Args:
            device ('obj'): Device object
            interface ('str', optional): interface to configure. Default is None
            vlan_name ('str', optional): vlan to configure. Default is None
        Returns:
            None
        Raise:
            SubCommandFailure: Failed to configure ip domain lookup
    """
    log.debug("configure ip domain lookup")
    try:
        if interface:
            device.configure("ip domain lookup source-interface {interface}".format(interface=interface))
        if vlan_name:
            device.configure("ip domain lookup source-interface vlan {vlan_name}".format(vlan_name=vlan_name))

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip domain lookup. Error:\n{error}".format(
                error=e
            )
        )

def unconfig_ip_domain_lookup(device, interface=None, vlan_name=None):
    """ Unconfigure ip domain lookup
        Args:
            device ('obj'): Device object
            interface ('str', optional): interface to unconfigure. Default is None
            vlan_name ('str', optional): vlan to unconfigure. Default is None
        Returns:
            None
        Raise:
            SubCommandFailure: Failed to un configure ip domain lookup
    """
    log.debug("un configure ip domain lookup")
    try:
        if interface:
            device.configure("no ip domain lookup source-interface {interface}".format(interface=interface))
        if vlan_name:
            device.configure("no ip domain lookup source-interface vlan {vlan_name}".format(vlan_name=vlan_name))

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not un configure ip domain lookup. Error:\n{error}".format(
                error=e
            )
        )


def unconfigure_ip_on_interface(
    device,
    interface,
    ip_address=None,
    mask=None,
    ipv6_address=None,
    eth_encap_type=None,
    eth_encap_val=None,
    sub_interface=None,
    dhcpv4=False,
    dhcp_hostname="",
    vrf=None,
    link_local_address=None,
    secondary=False):
    """ Unconfigure IP on an interface

        Args:
            device ('obj'): Device object
            interface ('str'): Interface to get address
            ip_address ('str', optional): IP addressed to be configured on interface. Default is None
            mask ('str', optional): Mask address to be used in configuration. Default is None
            ipv6_address ('str', optional): IPv6 address with subnet mask. Default is None
            eth_encap_type ('str', optional): Encapsulation type. Default is None
            eth_encap_val ('str', optional): Encapsulation value. Default is None
            sub_interface ('str', optional): Subinterface to be added to interface name. Default is None
            dhcpv4 ('bool', optional): configure for ipv4 dhcp. Default is False
            dhcp_hostname ('str', optional): Optionally configure dhcp hostname as well. Default is ''
            vrf ('str', optional): vrf for in the interface. Default is None
            link_local_address ('str', optional): Link local address. Default is None
            secondary ('bool', optional): configure as secondary ipv4 address. Default is False
        Returns:
            None
            Warning messages
        Raises:
            SubCommandFailure
    """

    # Get interface name
    interface_name = interface
    if sub_interface:
        interface_name += f'.{sub_interface}'

    # Build config string
    cli = [f'interface {interface_name}']

    # Unconfigure encap
    if eth_encap_type:
        cli.append(f"no encapsulation {eth_encap_type}{f' {eth_encap_val}' if eth_encap_val else ''}")

    #Unconfigure vrf(vrf needs to configured before ip)
    if vrf:
        cli.append(f'no vrf forwarding {vrf}')
    # Unconfigure port to receive ipv4 address via dhcp
    if dhcpv4:
        if dhcp_hostname:
            cli.append(f'no ip address dhcp hostname {dhcp_hostname}')
        else:
            cli.append('no ip address dhcp')
    else:
        #Unconfigure ip and mask
        if ip_address and mask:
            cli.append(f'no ip address {ip_address} {mask}{" secondary" if secondary else ""}')

    # Unconfigure ipv6 address configuration
    if ipv6_address:
        cli.append(f'no ipv6 address {ipv6_address}')
    # Unonfigure ipv6 link-local address
    if link_local_address:
        cli.append(f'no ipv6 address {link_local_address} link-local')
    # Configure device
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure IP address {ip_address} on interface "
            f"{interface} on device {device.name}. Error:\n{e}")


def unconfigure_interface_duplex_mode(device, interface):
    """ Unconfigures Interface duplex mode
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f"interface {interface}", "no duplex"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure Interface duplex mode. Error:{e}')

def configure_portchannel_dpi_algorithm(device, tunnel_type=None):
    """config port-channel load-balance-hash-algo dpi algorithm

        Args:
            device (`obj`): Device object
            tunnel_type (`str`): tunnel type

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring port-channel load-balance-hash-algo dpi algorithm"
    )
    cmd = "port-channel load-balance-hash-algo dpi algorithm"
    if tunnel_type is not None:
        cmd += f" {tunnel_type}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure load-balance-hash-algo dpi algorithm. Error:\n{e}"
        )

def unconfigure_portchannel_dpi_algorithm(device, tunnel_type=None):
    """config port-channel load-balance-hash-algo dpi algorithm

        Args:
            device (`obj`): Device object
            tunnel_type (`str`): tunnel type

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring port-channel load-balance-hash-algo dpi algorithm"
    )
    cmd = "no port-channel load-balance-hash-algo dpi algorithm"
    if tunnel_type is not None:
        cmd += f" {tunnel_type}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure load-balance-hash-algo dpi algorithm. Error:\n{e}"
        )

def configure_interface_ip_wccp(device, interface, id_nmber, redirect=None, group_listen=False):
    """ Configure interface ip wccp
        Args:
            device ('obj'): device to use
            interface ('str'): Interface Name
            id_nmber ('str'): Dynamically defined service identifier number
            redirect ('str', optional): inbound or outbound redirection. Ex: in, out. Default is None
            group_listen ('bool', optional): Listen for multicasted WCCP protocol packets. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = [f"interface {interface}", "no switchport"]
    if redirect:
        config.append(f"ip wccp {id_nmber} redirect {redirect}")
    if group_listen:
        config.append(f"ip wccp {id_nmber} group-listen")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure interface ip wccp. Error: {e}')


def unconfigure_port_channel_ip(device, port_channel, ip_version=None, shutdown=True):

    """ Unconfigure port-channel ip address on port-channel interface
        Args:
            device ('obj'): Device object
            port_channel ('str'): Port-channel number for the Port-channel interface
            ip_version ('str', optional): ip or ipv6 version. Default is None
            shutdown ('bool', optional): shutdown the port channel. Default is True

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    config = [f"interface Port-channel {port_channel}"]
    if ip_version:
        config.append(f"no {ip_version} address")
    if shutdown:
        config.append("shutdown")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure interface Port-channel {port_channel}. Error: {e}")


def unshut_port_channel(device, port_channel):
    """ Unconfigure port-channel ip address on port-channel interface
        Args:
            device ('obj'): Device object
            port_channel ('str'): Port-channel number for the Port-channel interface

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info('Unconfiguring the Portchannel interface {}'.format(port_channel))

    config = [f"interface Port-channel {port_channel}",
              f"no shutdown"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure interface Port-channel {port_channel}. Error: {e}")

def configure_print_timestamp_for_show_command(device):
    """ Configure print timestamp for show command
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure print timestamp for show commands
    """
    log.info("configuring print timestamp for show commands")

    cmd = ["line console 0", "exec prompt timestamp"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure print timestamp for show command, Error:\n{e}')


def configure_console_default_privilege_level(device, level):
    """ Configure console privilege level
        Args:
            device ('obj'): device to use
            level ('str'): Default privilege level for line
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure default privilege level
    """
    log.info("configuring default privilege level")

    cmd = ["line console 0", f"privilege level {level}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure default privilege level, Error:\n{e}')


def configure_ipv6_nd_suppress_ra(device, interface):
    '''Configure ipv6 nd suppress-ra
    Args:
        device ('obj'): Device Object
        interface('str'): Any Interface
     Returns:
            None
    Raise:
        SubCommandFailure
    '''
    cmd= [f'interface {interface}',
          f'ipv6 nd suppress-ra']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 nd suppress-ra. Error:\n{e}")

def unconfigure_ipv6_nd_suppress_ra(device, interface):
    """Unconfigure ipv6 nd suppress-ra
    Args:
        device ('obj'): Device Object
        interface('str'): Any Interface
     Returns:
            None
    Raise:
        SubCommandFailure
    """
    cmd= [f'interface {interface}',
          f'no ipv6 nd suppress-ra']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 nd suppress-ra. Error:\n{e}")

def unconfigure_ipv6_redirects(device, interface):
    """Unconfigure ipv6 redirects
    Args:
        device ('obj'): Device Object
        interface('str'): Any Interface
     Returns:
            None
    Raise:
        SubCommandFailure
    """
    cmd = [f'interface {interface}',
           f'no ipv6 redirects']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 redirects. Error:\n{e}")

def unconfigure_ipv6_address_test(device, interface, word, ipv6_prefix_value):
    '''Unconfigure ipv6 address test
    Args:
        device ('obj'): Device Object
        interface('str'): Any Interface
        word('str'): General prefix name
        ipv6_prefix_value('str'): X:X:X:X::X/<0-128>  IPv6 prefix
     Returns:
            None
    Raise:
        SubCommandFailure
    '''
    cmd = [f'interface {interface}',
           f'no ipv6 address {word} {ipv6_prefix_value}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 address test. Error:\n{e}")


def configure_ipv6_address_config(device, interface, nd_option):
    '''Configure ipv6 address config
    Args:
        device ('obj'): Device Object
        interface('str'): Any Interface
        nd_option('str'): advertisement-interval  Send an advertisement interval option in RA's
                        autoconfig              Automatic Configuration
                        cache                   Cache entry
                        dad                     Duplicate Address Detection
                        dad-proxy               Configure DAD proxy on the interface
                        destination-guard       Query destination-guard switch table
                        managed-config-flag     Hosts should use DHCP for address config
                        na                      Neighbor Advertisement control
                        ns-interval             Set advertised NS retransmission interval
                        nud                     Neighbor Unreachability Detection
                        other-config-flag       Hosts should use DHCP for non-address config
                        packet-priority         Set packet priority for ND
                        prefix                  Configure IPv6 Routing Prefix Advertisement
                        prefix-advertisement    Deprecated command: use 'ipv6 nd prefix' instead
                        ra                      Router Advertisement control
                        ra-interval             Deprecated command: use 'ipv6 nd ra interval' instead
                        ra-lifetime             Deprecated command: use 'ipv6 nd ra lifetime' instead
                        reachable-time          Set advertised reachability time
                        router-preference       Set default router preference value
                        suppress                Configure ND suppress on the interface
                        suppress-ra             Deprecated command: use 'ipv6 nd ra suppress' instead
     Returns:
            None
    Raise:
        SubCommandFailure
    '''
    cmd= [f'interface {interface}',
          f'ipv6 nd {nd_option}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 address config. Error:\n{e}")

def unconfigure_ipv6_address_config(device, interface, nd_option):
    """Unconfigure ipv6 address config
    Args:
        device ('obj'): Device Object
        interface('str'): Any Interface
        nd_option('str'): advertisement-interval  Send an advertisement interval option in RA's
                        autoconfig              Automatic Configuration
                        cache                   Cache entry
                        dad                     Duplicate Address Detection
                        dad-proxy               Configure DAD proxy on the interface
                        destination-guard       Query destination-guard switch table
                        managed-config-flag     Hosts should use DHCP for address config
                        na                      Neighbor Advertisement control
                        ns-interval             Set advertised NS retransmission interval
                        nud                     Neighbor Unreachability Detection
                        other-config-flag       Hosts should use DHCP for non-address config
                        packet-priority         Set packet priority for ND
                        prefix                  Configure IPv6 Routing Prefix Advertisement
                        prefix-advertisement    Deprecated command: use 'ipv6 nd prefix' instead
                        ra                      Router Advertisement control
                        ra-interval             Deprecated command: use 'ipv6 nd ra interval' instead
                        ra-lifetime             Deprecated command: use 'ipv6 nd ra lifetime' instead
                        reachable-time          Set advertised reachability time
                        router-preference       Set default router preference value
                        suppress                Configure ND suppress on the interface
                        suppress-ra             Deprecated command: use 'ipv6 nd ra suppress' instead
     Returns:
            None
    Raise:
        SubCommandFailure
    """
    cmd= [f'interface {interface}',
          f'no ipv6 nd {nd_option}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 address config. Error:\n{e}")

def unconfigure_ipv6_address_autoconfig(device, interface):
    """Unconfigure ipv6 address autoconfig
    Args:
        device ('obj'): Device Object
        interface('str'): Any Interface
     Returns:
            None
    Raise:
        SubCommandFailure
    """
    cmd= [f'interface {interface}',
          f'no ipv6 address autoconfig']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 address autoconfig. Error:\n{e}")


def unconfigure_interface_pvlan_mode_with_submode(device, interface):
    """ Unconfigures Private Vlan Switchport mode
        Args:
            device ('obj')            : device to use
            interface ('str')         : interface to unconfigure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        f"Unconfiguring switchport pvlan mode with submode on {interface}"
    )
    config = [f"interface {interface}", f"no switchport mode"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure Primary Pvlan Error:\n{e}"
        )


def configure_dialer_interface(device,
        dialer_intf,
        encap,
        auth_type,
        ip_add=None,
        pool_num=None,
        dialer_group=None,
        chap_hostname=None,
        chap_pass=None,
        pap_uname=None,
        pap_pass=None,
        ipcp_route=False):
    """ Configure Dialer interface
        Args:
            device (`obj`): Device object
            dialer_intf ('str'): Dialer interface
            encap ('str'): ppp encapsulation type
            ip_add ('str', optional): ip address
            pool_number ('int'): dialer pool <number>
            dialer_group ('int', optional): dialer-group <list>
            auth_type ('str'): ppp authentication type
            chap_hostname ('str', optional): ppp chap hostname
            chap_password ('str', optional): ppp chap password
            pap_username ('str', optional): ppp pap username
            pap_password ('str', optional): ppp pap password
            ipcp_route ('boolean' optional): ppp ipcp route
        For the arguments that are optional, the default value is None.
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    if not device.is_connected():
        connect_device(device=device)

    cli = []
    cli.append(f"interface {dialer_intf}")
    cli.append(f"encapsulation {encap}")
    cli.append(f"no shutdown")
    cli.append(f"dialer pool {pool_num}")
    cli.append(f"ip address {ip_add}")
    cli.append(f"ppp authentication {auth_type} callin")
    if dialer_group:
        cli.append(f"dialer-group {dialer_group}")
    if chap_hostname:
        cli.append(f"ppp chap hostname {chap_hostname}")
        cli.append(f"ppp chap password {chap_pass}")
    if pap_uname:
        cli.append(f"ppp pap sent-username {pap_uname} password {pap_pass}")
    if ipcp_route:
        cli.append(f"ppp ipcp route default")

    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure dialer interface on device. Error:\n{e}"
        )


def configure_interface_no_switchport_voice_vlan(device, interface, vlan):
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
        device.configure([ "interface {interface}".format(interface=interface),
            "no switchport voice vlan {vlan}".format(vlan=vlan)
            ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure no switchport trunk vlan. Error:\n{error}".format(
                error=e
            )
        )


def configure_global_interface_template_sticky(device):
    """ configure global interface-template sticky
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(["access-session interface-template sticky"])
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure global interface-template sticky. Error:\n{e}")

def unconfigure_interface_service_policy(device, interface, policy_name, direction):

    """ Unconfigure any service policy configured under interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to remove service policy from
            policy_name ('str') : service policy name
            direction ('str'): direction of service policy

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigure service policy on interface")

    configs = [f'interface {interface}',
              f'no service-policy {direction} {policy_name}']
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure service-policy on iterface:\n{e}"
        )

def unconfigure_interface_switchport_pvlan_association(device, interface, mode):
    """ unconfigures Private pvlan association
        Args:
            device ('obj')    			: device to use
            interface ('str') 			: interface to configure
            mode ('str')      			: pvlan mode (i.e trunk or host)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        f"unconfiguring switchport pvlan association on {interface}"
    )
    config = [f"interface {interface}",
              f"no switchport private-vlan association {mode}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure pvlan assiciation. Error:\n{e}"
        )

def unconfigure_interface_pvlan_host_assoc(device,interface):
    """ unconfigures Interface Private Vlan Host Association
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = [f"interface {interface}",
                   "no switchport private-vlan host-association"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not unconfigure Pvlan Host Association. Error:\n{e}'
        )

def unconfigure_interface_switchport_pvlan_mapping(device, interface, mode, primary_vlan_id, secondary_vlan_id):
    """ Unconfigures Private Vlan Switchport mode
        Args:
            device ('obj')    			: device to use
            interface ('str') 			: interface to configure
            mode ('str')      			: pvlan mode (i.e trunk )
	    primary_vlan_id ('int') 	        : Primary VLAN ID of the native VLAN
	    secondary_vlan_id ('int')	        : Secondary VLAN ID of the native VLAN
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = [f"interface {interface}",
              f"no switchport private-vlan mapping {mode} {primary_vlan_id} {secondary_vlan_id}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure Pvlan mapping with primary/secondary vlan ID.Error:\n{e}"
        )

def configure_switchport_pvlan_trunk_allowed_vlan(device, interface, allowed_vlan):

    """ Configure switchport private-vlan trunk allowed vlan
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be added

            allowed_vlan (`str`): allowed vlan Id to be added
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure switchport private-vlan trunk allowed vlan
    """
    log.debug(f"Configure switchport private-vlan trunk allowed vlan on {interface}")

    config = [f"interface {interface}",
               f"switchport private-vlan trunk allowed vlan {allowed_vlan}"]

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure switchport private-vlan trunk"
                                f"allowed vlan on {interface}. Error:\n{e}")

def unconfigure_switchport_pvlan_trunk_allowed_vlan(device, interface, allowed_vlan):

    """ Unconfigure switchport private-vlan trunk allowed vlan
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be added
            allowed_vlan (`str`): allowed vlan Id to be added
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to unconfigure switchport private-vlan trunk allowed vlan
    """
    log.debug(f"Configure switchport private-vlan trunk allowed vlan on {interface}")

    config = [f"interface {interface}",
              f"no switchport private-vlan trunk allowed vlan {allowed_vlan}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure switchport private-vlan trunk"
                                f" allowed vlan on {interface}. Error:\n{e}")

def configure_switchport_pvlan_trunk_native_vlan(device, interface, native_vlan):

    """ Configure switchport private-vlan trunk native vlan
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be added
            native_vlan (`str`): native vlan Id to be added
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure switchport private-vlan trunk native vlan
    """
    log.debug(f"Configure switchport private-vlan trunk native vlan on {interface}")

    config = [f"interface {interface}",
              f"switchport private-vlan trunk native vlan {native_vlan}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure switchport private-vlan trunk"
                                f" native vlan on {interface}. Error:\n{e}")

def unconfigure_switchport_pvlan_trunk_native_vlan(device, interface, native_vlan):

    """ Unconfigure switchport private-vlan trunk native vlan
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be added
            native_vlan (`str`): native vlan Id to be added
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to unconfigure switchport private-vlan trunk native vlan
    """
    log.debug(f"Configure switchport private-vlan trunk native vlan on {interface}")

    config = [f"interface {interface}",
              f"no switchport private-vlan trunk native vlan {native_vlan}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure switchport private-vlan trunk"
                                f" native vlan on {interface}. Error:\n{e}")

def configure_interface_pvlan_mapping(device, interface, primary_vlan_id, secondary_vlan_id):
    """ Configures private vlan mapping
        Args:
            device ('obj')    			: device to use
            interface ('str') 			: interface to configure
	    primary_vlan_id ('int') 	        : Primary VLAN ID of the native VLAN
	    secondary_vlan_id ('int')	        : Secondary VLAN ID of the native VLAN
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = [f"interface {interface}",
              f"switchport private-vlan mapping {primary_vlan_id} {secondary_vlan_id}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure Pvlan mapping with primary/secondary vlan ID.Error:\n{e}"
        )

def unconfigure_interface_pvlan_mapping(device, interface, primary_vlan_id, secondary_vlan_id):
    """ Unconfigures private vlan mapping
        Args:
            device ('obj')    			: device to use
            interface ('str') 			: interface to configure
	    primary_vlan_id ('int') 	        : Primary VLAN ID of the native VLAN
	    secondary_vlan_id ('int')	        : Secondary VLAN ID of the native VLAN
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = [f"interface {interface}",
              f"no switchport private-vlan mapping {primary_vlan_id} {secondary_vlan_id}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure Pvlan mapping with primary/secondary vlan ID.Error:\n{e}"
        )

def unconfigure_switchport_trunk_allowed_vlan(device, interface, vlan_id):
    """ Unconfigure switchport trunk allowed vlan on interface <interface>
        Args:
            device ('obj'): Device object
            interface('str'): interface details on which we config
            vlan_id('int'): VLAN IDs of the allowed VLANs
        Returns:
            None
        Raises:
            SubCommandFailure :Failed to unconfigure switchport trunk allowed vlan on interface
    """

    log.debug(f"Unconfigure switchport trunk allowed vlan on interface {interface}")

    config = [f"interface {interface}",
              f"no switchport trunk allowed vlan {vlan_id}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to Unconfigure switchport trunk allowed vlan on interface {interface}. Error:\n{e}"
        )

def unconfigure_switchport_trunk_native_vlan(device, interface, native_vlan):

    """ Unconfigure switchport trunk native vlan
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be added
            native_vlan (`str`): native vlan Id to be added
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure switchport trunk native vlan
    """
    log.debug(f"Unconfiguring switchport trunk native vlan on {interface}")

    config = [f"interface {interface}",
              f"no switchport trunk native vlan {native_vlan}"]
    try:
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure switchport trunk"
                                f" native vlan on {interface}. Error:\n{e}")

def disable_switchport_trunk_on_interface(device, interface):

    """ Disable switchport trunk on interface
        Args:
            device ('obj'): Device object
            interface ('str'): interface name to disable switchport trunk
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to disable switchport trunk on interface
    """
    log.debug(f"Disable switchport mode trunk on interface {interface}")

    config = [f"interface {interface}", "no switchport mode trunk"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to disable switchport mode trunk under {interface}. Error:\n{e}"
        )

def configure_glbp_details_on_interface(device, interface, group_number, ip_address=None, ipv6_address=None, priority=None,
        preempt=None, hello_interval=None, hold_time=None):
    """ Configure glbp details on interface
        Args:
            device (`obj`): Device object
            interface ('str'): Interface to configure glbp
            group_number (`int`): group_number
            ip_address ('str', optional) : ip address
            ipv6_address ('str', optional) : ipv6 address
            priority ('str', optional) : config custom priority to glbp
            preempt ('str', optional) : config custom preempt delay sync to glbp
            hello_interval ('str', optional) : config the hello time for glbp session
            hold_time ('str', optional) : config the hold time for glbp session
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append(f"interface {interface}")
    if ip_address:
        configs.append(f"glbp {group_number}  ip {ip_address}")
    if ipv6_address:
        configs.append(f"glbp {group_number} ipv6 {ipv6_address}")
    if priority:
        configs.append(f"glbp {group_number}  priority {priority}")
    if preempt:
        configs.append(f"glbp {group_number}  preempt delay sync {preempt}")
    if hello_interval and hold_time:
        configs.append(f"glbp {group_number} timers {hello_interval} {hold_time}")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure glbp details on interface. Error:\n{e}"
     )


def configure_service_instance(
        device,
        interface,
        service_num,
        dot1q_num=None,
	rewrite_option=None,
	bridge_dom_num=None):

    """ Configure service instance on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            service_num (`str`, optional): service instance number to be configured on interface
            dot1q_num (`str`, optional): dot1q encapsulation number to be configured, default value None
            rewrite_option (`str`, optional): rewrite option, default value None
            bridge_dom_num (`str`, optional): bridge-domain number, default value None

        Returns:
            None
            Warning messages

        Raises:
            SubCommandFailure
    """

    log.info(f"Configuring service instance on interface {interface}")

    cmd = []
    cmd.append(f"interface {interface}")
    cmd.append(f"service instance {service_num} ethernet")
    if dot1q_num:
        cmd.append(f"encapsulation dot1q {dot1q_num}")
    if rewrite_option:
        cmd.append(f"rewrite {rewrite_option}")
    if bridge_dom_num:
        cmd.append(f"bridge-domain {bridge_dom_num}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure service instance Error:\n{e}")


def unconfigure_service_instance(
        device,
        interface,
        service_num):

    """ Unconfigure service instance on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            service_num (`str`, optional): service instance number to be configured on interface

        Returns:
            None
            Warning messages

        Raises:
            SubCommandFailure
    """

    log.info(f"Unconfiguring service instance on interface {interface}")

    cmd = []
    cmd.append(f"interface {interface}")
    cmd.append(f"no service instance {service_num} ethernet")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure service instance Error:\n{e}")


def configure_interface_ip_nbar(device,interface):

    """ Configure ip nbar on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address

        Returns:
            None
            Warning messages

        Raises:
            SubCommandFailure
    """

    log.info(f"Configuring ip nbar on interface {interface}")

    cmd = []
    cmd.append(f"interface {interface}")
    cmd.append(f"ip nbar protocol-discovery")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ip nbar Error:\n{e}")


def unconfigure_interface_ip_nbar(device,interface):

    """ Unconfigure ip nbar on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address

        Returns:
            None
            Warning messages

        Raises:
            SubCommandFailure
    """

    log.info(f"Unconfiguring ip nbar on interface {interface}")

    cmd = []
    cmd.append(f"interface {interface}")
    cmd.append(f"no ip nbar protocol-discovery")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ip nbar Error:\n{e}")


def config_interface_prpchannel(
        device,
        interface,
        prpchannel_num):

    """ Configure prp-channel on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to which prp channel is added
            prpchannel_num (`str`): Prp channel group number

        Returns:
            None
            Warning messages

        Raises:
            SubCommandFailure
    """

    log.debug(f"Configuring PRP channel on interface {interface}")

    cmd = []
    cmd.append(f"interface {interface}")
    cmd.append(f"prp-channel-group {prpchannel_num}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure prp channel on interace Error:\n{e}")


def unconfig_interface_prpchannel(
        device,
        prpchannel_num):

    """ UnConfigure prp-channel on an interface

        Args:
            device (`obj`): Device object
            prpchannel_num (`str`): Prp channel group number

        Returns:
            None
            Warning messages

        Raises:
            SubCommandFailure
    """

    log.debug(f"UnConfiguring PRP channel")

    cmd = []
    cmd.append(f"no interface prp-channel {prpchannel_num}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure prp channel on interace Error:\n{e}")



def configure_interface_vlan(device, vlan_id):
    """ Configures interface vlan id
        Example : interface vlan 1
        Args:
            device ('obj'): device to use
            vlan_id ('int'): Vlan interface number (Range: 1-4093)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring interface vlan {vlan_id} on {device}")
    config = [
        f'interface vlan {vlan_id}',
        'no shutdown'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure interface vlan {vlan_id} on device {device}. Error:\n{e}")


def configure_interface_range_no_switchport(device, start_interface, end_interface):
    """ Configure interface range no switchport
        Args:
            device ('obj'): device to use
            start_interface('str'): Starting Interface
            end_interface('str'): Ending Interface number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f'Configuring interface range no switchport on {device}')
    config = [
        f'interface range {start_interface} - {end_interface}',
        'no switchport'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure interface range no switchport on device {device}. Error:\n{e}")

def enable_switchport_protected_on_interface(device, interface):
    """ Enable switchport protected on interface
        Args:
            device ('obj'): Device object
            interface ('str'): interface name to enable switchport protected
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to enable switchport protected on interface
    """
    log.debug(f"Enable switchport protected on interface {interface}")

    configs = [
    f"interface {interface}",
    "switchport protected"
    ]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to enable switchport protected under {interface}. Error:\n{e}"
        )

def unconfigure_interface_speed(device, interface):
    """ unconfigure speed on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = [
        f'interface {interface}',
        'no speed'
    ] 
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure speed on {interface}. Error:\n{e}")

def configure_ip_on_atm_interface(
    device,
    interface,
    vpi_vci,
    vlan_id=None,
    ip_address=None,
    mask=None,
    ipv6_address=None,
    atm_encap_type=None,
    protocol=None,
    dialer_num=None,
    atm_qos=None,
    pcr="",
    scr="",
    bc=""):
    """ Configure IP on an atm interface
    Args:
        device (`obj`): Device object
        interface (`str`): Interface to get address
        vpi_vci ('str'): atm vpi/vci value
        vlan_id ('str', optional): sub-interface number, eg: interface ATM0/3/0.213 point-to-point
        ip_address (`str`, optional): IP addressed to be configured on interface, default value None
        mask (`str`, optional): Mask address to be used in configuration, default value None
        ipv6_address (`str`, optional): IPv6 address with subnet mask, default value None
        atm_encap_type (`str`, optional): Encapsulation type, default value None
        protocol (`str`, optional): atm pvc protocol type, eg: ppp, pppoe-client
        dialer_num (`str`, optional): dialer pool number, default value None
        atm_qos ('str', optional): ATM PVC qos eg: vbr-rt, vbr-nrt, cbr
        pcr ('str', optional): pcr in string; default value ""
        scr ('str', optional): scr in string; default value ""
        bc ('str', optional): bc in string; default value ""
    Returns:
        None
        Warning messages
    Raises:
        SubCommandFailure
    """

    # Get interface name
    if vlan_id:
        interface_name = f"{interface}.{vlan_id}"
    else:
        interface_name = interface

    # Build config list
    cfg_lst = []
    cfg_lst.append(f"interface {interface_name} point-to-point")

    if ip_address and mask:
        cfg_lst.append(f"ip address {ip_address} {mask}")

    if ipv6_address:
        cfg_lst.append(f"ipv6 enable")
        cfg_lst.append(f"ipv6 address {ipv6_address}")

    if vpi_vci:
        cfg_lst.append(f"pvc {vpi_vci}")

    if dialer_num and protocol == 'pppoe-client':
        if atm_encap_type == 'aal5mux':
            cfg_lst.append(f"encapsulation {atm_encap_type} pppoe-client")
            cfg_lst.append(f"dialer pool-member {dialer_num}")
        if atm_encap_type == 'aal5snap':
            cfg_lst.append(f"encapsulation {atm_encap_type}")
            cfg_lst.append(f"pppoe-client dial-pool-number {dialer_num}")
        else:
            cfg_lst.append(f"pppoe-client dial-pool-number {dialer_num}")

    if protocol == 'ppp':
        if atm_encap_type == 'aal5mux':
            cfg_lst.append("encapsulation aal5mux ppp dialer")
        elif atm_encap_type == 'aal5snap':
            cfg_lst.append("encapsulation aal5snap")
            cfg_lst.append("protocol ppp  dialer")
        else:
            cfg_lst.append("protocol ppp dialer")
        if dialer_num:
            cfg_lst.append(f"dialer pool-member {dialer_num}")

    if atm_qos and pcr and scr and bc:
        cfg_lst.append(f"{atm_qos} {pcr} {scr} {bc}")
    elif atm_qos and pcr:
        cfg_lst.append(f"{atm_qos} {pcr}")


    # Configure device
    try:
        out = device.configure(cfg_lst)
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

def unconfigure_ip_on_atm_interface(
    device,
    interface,
    vpi_vci=None,
    vlan_id=None,
    ip_address=None,
    mask=None,
    ipv6_address=None):
    """ Unconfigure IP on an atm interface
    Args:
        device (`obj`): Device object
        interface (`str`): Interface to get address
        vpi_vci ('str'): atm vpi/vci value
        vlan_id ('str', optional): sub-interface number, eg: interface ATM0/3/0.213 point-to-point
        ip_address (`str`, optional): IP addressed to be configured on interface, default value None
        mask (`str`, optional): Mask address to be used in configuration, default value None
        ipv6_address (`str`, optional): IPv6 address with subnet mask, default value None
    Raises:
        SubCommandFailure
    """

    # Get interface name
    if vlan_id:
        interface_name = f"{interface}.{vlan_id}"
    else:
        interface_name = interface

    # Build config list
    cfg_lst = []
    cfg_lst.append(f"interface {interface_name} point-to-point")

    if ip_address and mask:
        cfg_lst.append(f"no ip address {ip_address} {mask}")

    if ipv6_address:
        cfg_lst.append(f"no ipv6 enable")
        cfg_lst.append(f"no ipv6 address {ipv6_address}")

    if vpi_vci:
        cfg_lst.append(f"no pvc {vpi_vci}")


    # Configure device
    try:
        out = device.configure(cfg_lst)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure IP address {ip} on interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                ip=ip_address,
                interface=interface_name,
                dev=device.name,
                error=e,
            )
        )

