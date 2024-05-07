"""Common configure functions for PTP"""

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

def configure_ptp_modes(device, mode, interface=None):
    """ PTP global configuration
        Args:
            device ('obj'): Device object
            mode ('str'): PTP mode
            interface ('str', optional): PTP interface , default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    if mode == "bcdelay":
        configs.append("ptp mode boundary delay-req")
    elif mode == "bcpdelay":
        configs.append("ptp mode boundary pdelay-req")
    elif mode == "dot1as":
        configs.append("ptp profile dot1as")
    elif mode == "tce2e":
        configs.append("ptp mode e2etransparent")
    elif mode == "tcp2p":
        configs.append("ptp mode p2ptransparent")
    elif mode == "g8275bc":
        configs.append("ptp profile 8275.1 clock-mode boundary")
        if interface:
            configs.append("interface {interface}".format(interface=interface))
            configs.append("ptp destination-mac non-forwardable")
    elif mode == "g8275tc":
        configs.append("ptp profile 8275.1 clock-mode transparent")
    else:
        configs.append("ptp mode boundary delay-req")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure PTP modes as per provided argument"
        )

def configure_ptp_transport_ipv4(device, transport):
    """ PTP global configuration
        Args:
            device (`obj`): Device object
            transport (`str`): PTP transport l3 mode
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("ptp transport {transport} udp".format(transport=transport))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure PTP transport as per provided argument"
        )

def configure_ptp_domain(device, domain):
    """ PTP global configuration
        Args:
            device (`obj`): Device object
            domain (`str`): PTP domain
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(["ptp domain {domain}".format(domain=domain)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure PTP domain as per provided argument"
        )

def configure_ptp_priority(device, priority1=None, priority2=None):
    """ PTP global configuration
        Args:
            device (`obj`): Device object
            priority1 ('str', optional): PTP priority1. Default is None
            priority2 ('str', optional): PTP priority2. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    if priority1:
        configs.append(f"ptp priority1 {priority1}")
    if priority2:
        configs.append(f"ptp priority2 {priority2}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure PTP transport as per provided argument"
        )

def configure_ptp_dscp_message(device, dscp_event, dscp_general):
    """ PTP dscp message configuration
        Args:
            device (`obj`): Device object
            dscp_event ('str'): PTP DSCP event message
            dscp_general ('str'): PTP DSCP general message
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("ptp ip dscp {dscp_event} message event".format(dscp_event=dscp_event))
    configs.append("ptp ip dscp {dscp_general} message general".format(dscp_general=dscp_general))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure PTP aes67 profile rates as per provided argument"
        )

def unconfigure_ptp_dscp_message(device, dscp_event, dscp_general):
    """ PTP dscp message configuration removal
        Args:
            device (`obj`): Device object
            dscp_event ('str'): PTP DSCP event message
            dscp_general ('str'): PTP DSCP general message
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("no ptp ip dscp message event")
    configs.append("no ptp ip dscp message general")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure PTP aes67 profile rates as per provided argument"
        )

def unconfigure_ptp_modes(device, mode):
    """ PTP global configuration removal
        Args:
            device (`obj`): Device object
            mode (`str`): PTP mode
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    if mode == "dot1as" or mode == "g8275":
        configs.append("no ptp profile")
    elif mode == "bcdelay":
        configs.append("no ptp mode boundary delay-req")
    elif mode == "g8275bc":
        configs.append("no ptp profile 8275.1 clock-mode boundary")       
    else:
        configs.append("no ptp mode")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure PTP modes  on device {device}. Error:\n{e}")


def configure_ptp_aes67_rates(device, mode, intf_list, sync=0, delay=0, announce=0, announce_timeout=3):
    """ PTP global configuration
        Args:
            device ('obj'): Device object
            mode ('str'): PTP mode
            intf_list ('list'): PTP interface list
            sync ('int'): PTP sync interval. Default: 0.
            delay ('int'): PTP delay-req interval. Default: 0.
            announce ('int'): PTP announce interval. Default: 0.
            announce_timeout ('int'): PTP announce timeout. Default: 3.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    for intf in intf_list:
        configs.append("interface {intf}".format(intf=intf))
        configs.append("ptp sync interval {sync}".format(sync=sync))
        if mode != 'dot1as':
            configs.append("ptp {mode} interval {delay}".format(mode=mode,delay=delay))
            configs.append("ptp announce interval {announce}".format(announce=announce))
            configs.append("ptp announce timeout {announce_timeout}".format(announce_timeout=announce_timeout))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure PTP aes67 profile rates as per provided argument"
        )
    
def unconfigure_ptp_transport_ipv4(device, transport):
    """ PTP global configuration
        Args:
            device (`obj`): Device object
            transport (`str`): PTP transport l3 mode
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no ptp transport {transport} udp".format(transport=transport))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure PTP transport as per provided argument"
        )

def unconfigure_ptp_domain(device, domain):
    """ PTP global configuration
        Args:
            device (`obj`): Device object
            domain (`str`): PTP domain
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no ptp domain")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure PTP domain as per provided argument"
        )

def configure_ptp_8275_local_priority(device, priority, intf_list=None):
    """ PTP 8275 local priority global and interface configuration
        Args:
            device (`obj`): Device object
            priority (`str`): PTP local priority
            intf_list ('list', optional): PTP interface list, default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    if not intf_list:
        configs.append("ptp local-clock priority {priority}".format(priority=priority))
    else:
        for intf in intf_list:
            configs.append("interface {intf}".format(intf=intf))
            configs.append("ptp localPriority {priority}".format(priority=priority))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure PTP 8275 local priority as per provided argument"
        )

def unconfigure_ptp_8275_local_priority(device, priority, intf_list=None):
    """ PTP 8275 local priority global and interface unconfiguration
        Args:
            device (`obj`): Device object
            priority (`str`): PTP local priority
            intf_list ('list', optional): PTP interface list, default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    if not intf_list:
        configs.append("no ptp local-clock priority {priority}".format(priority=priority))
    else:
        for intf in intf_list:
            configs.append("interface {intf}".format(intf=intf))
            configs.append("no ptp localPriority {priority}".format(priority=priority))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure PTP 8275 local priority as per provided argument"
        )

def configure_ptp_role_primary(device, intf_list):
    """ PTP role interface configuration
        Args:
            device (`obj`): Device object
            intf_list ('list'): PTP interface list
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    for intf in intf_list:
        configs.append("interface {intf}".format(intf=intf))
        configs.append("ptp role primary")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure PTP role interface as per provided argument"
        )

def unconfigure_ptp_role_primary(device, intf_list):
    """ PTP role interface configuration
        Args:
            device (`obj`): Device object
            intf_list ('list'): PTP interface list
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    for intf in intf_list:
        configs.append("interface {intf}".format(intf=intf))
        configs.append("no ptp role primary")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure PTP role interface as per provided argument"
        )

def configure_ptp_8275_holdover_spec_duration(device, holdover):
    """ PTP 8275 holdover spec-duration configuration
        Args:
            device (`obj`): Device object
            holdover (`int`): PTP holdover spec-duration in seconds
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(["ptp holdover 8275.1 spec-duration {holdover}".format(holdover=holdover)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure PTP 8275 holdover spec-duration"
        )

def unconfigure_ptp_8275_holdover_spec_duration(device):
    """ PTP 8275 holdover spec-duration unconfiguration
        Args:
            device (`obj`): Device object
            domain (`str`): PTP domain
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no ptp holdover 8275.1 spec-duration")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure PTP 8275 holdover spec-duration"
        )


def configure_ptp_vlan(device, interface, vlan):
    """ PTP vlan configuration
        Args:
            device ('obj'): Device object
            interface ('str'): PTP interface configuration
            vlan ('str'): PTP vlan configuration Default: 0
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = [
        f"interface {interface}",
        f"ptp vlan {vlan}"]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure PTP vlan on {device}. Error:\n{error}"
            .format(device=device, error=e))

def unconfigure_ptp_vlan(device, interface, vlan):
    """ PTP vlan unconfiguration
        Args:
            device ('obj'): Device object
            interface ('str'): PTP interface configuration
            vlan ('str'): PTP vlan unconfiguration Default: 0
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = [
        f"interface {interface}",
        f"no ptp vlan {vlan}"]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure PTP vlan on {device}. Error:\n{error}"
            .format(device=device, error=e))


def configure_ptp_announce_transmit(device, intf):
    """ Configure ptp announce transmit on interface
        Args:
            device (`obj`): Device object
            intf (str): PTP interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ptp announce transmit on {device}".format(device=device))
    configs = []
    configs.append("interface {intf}".format(intf=intf))
    configs.append("ptp announce transmit")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ptp announce transmit on {device}. Error:\n{error}".format(device=device, error=e)
        )

def unconfigure_ptp_announce_transmit(device, intf):
    """ Unconfigure ptp announce transmit on interface
        Args:
            device (`obj`): Device object
            intf (str): PTP interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigure ptp announce transmit on {device}".format(device=device))
    configs = []
    configs.append("interface {intf}".format(intf=intf))
    configs.append("no ptp announce transmit")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Unconfigure ptp announce transmit on {device}. Error:\n{error}".format(device=device, error=e)
        )


def unconfigure_ptp_aes67_rates(device, intf_list, sync=0, delay=0, announce=0, announce_timeout=3):
    """ PTP global unconfiguration
        Args:
            device ('obj'): Device object
            intf_list ('list'): PTP interface
            sync ('int' optional): PTP sync interval. Default: 0  unconfiguration.
            delay ('int' optional): PTP delay-req interval. Default: 0 unconfiguration.
            announce ('int' optional): PTP announce interval. Default: 0 unconfiguration.
            announce_timeout ('int' optional): PTP announce timeout. Default: 3 unconfiguration.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    for intf in intf_list:
        configs.append("interface {intf}".format(intf=intf))
        configs.append("no ptp sync interval {sync}".format(sync=sync))
        configs.append("no ptp delay-req interval {delay}".format(delay=delay))
        configs.append("no ptp announce interval {announce}".format(announce=announce))
        configs.append("no ptp announce timeout {announce_timeout}".format(announce_timeout=announce_timeout))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure PTP aes67 profile rates on {device}. Error:\n{error}"
            .format(device=device, error=e))


def configure_ptp_source(device, ip_address=None):
    """ PTP source configuration
        Args:
            device ('obj'): Device object
            ip address ('str'): PTP Ip address , default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = [
        f"ptp transport ipv4 udp",
        f"ptp mode p2ptransparent",
        f"ptp source {ip_address}"]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure PTP source on {device}. Error:\n{error}"
            .format(device=device, error=e))

def configure_no_ptp_enable_on_interface(device, interface):
    """ Configure no ptp enable on interface
        Args:
            device (`obj`): Device object
            interface ('str'): PTP interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring no ptp enable on {device.name} {interface}")
    cmd = [f"interface {interface}",f"no ptp enable"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure no ptp enable on device interface. Error:\n{e}')

def configure_ptp_enable_on_interface(device, interface):
    """ Configure ptp enable on interface
        Args:
            device (`obj`): Device object
            interface ('str'): PTP interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring no ptp enable on {device.name} {interface}")
    cmd = [f"interface {interface}",f"ptp enable"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure ptp enable on device interface. Error:\n{e}')

def configure_ptp_neighbor_propagation_delay_threshold(device, delay = 60):
    """ Configure ptp neighbor propagation delay threshold
        Args:
            device (`obj`): Device object
            delay ('str'): PTP neighbor-propagation-delay-threshold value in nanoseconds.Default value is 60. Eg: <1-2147483646> nano seconds
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring ptp neighbor-propagation-delay-threshold on {device.name}")
    cmd = [f"ptp neighbor-propagation-delay-threshold {delay}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure ptp neighbor-propagation-delay-threshold on device. Error:\n{e}')

def unconfigure_ptp_neighbor_propagation_delay_threshold(device):
    """ Unconfigure ptp neighbor propagation delay threshold
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring ptp neighbor-propagation-delay-threshold on {device.name}")
    cmd = [f"no ptp neighbor-propagation-delay-threshold"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure ptp neighbor-propagation-delay-threshold on device. Error:\n{e}')
