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

def configure_ptp_modes(device, mode):
    """ PTP global configuration
        Args:
            device (`obj`): Device object
            mode (`str`): PTP mode
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

def configure_ptp_priority(device, priority1, priority2):
    """ PTP global configuration
        Args:
            device (`obj`): Device object
            priority1 (`str`): PTP priority1
            priority2 (`str`): PTP priority2
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("ptp priority1 {priority1}".format(priority1=priority1))
    configs.append("ptp priority2 {priority2}".format(priority2=priority2))

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
    if mode == "dot1as":
        configs.append("no ptp profile dot1as")
    else:
        configs.append("no ptp mode")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure PTP modes as per provided argument"
        )

def configure_ptp_aes67_rates(device, mode, intf_list, sync=0, delay=0, announce=0, announce_timeout=3):
    """ PTP global configuration
        Args:
            device (`obj`): Device object
            mode (`str`): PTP mode
            intf_list ('list'): PTP interface list
            sync (`int`): PTP sync interval. Default: 0.
            delay (`int`): PTP delay-req interval. Default: 0.
            announce (`int`): PTP announce interval. Default: 0.
            announce_timeout (`int`): PTP announce timeout. Default: 3.
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
