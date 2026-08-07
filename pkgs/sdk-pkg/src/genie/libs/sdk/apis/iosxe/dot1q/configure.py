import logging
import re
from genie.libs.parser.utils.common import Common
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import (
    SubCommandFailure,
    StateMachineError,
    TimeoutError,
    ConnectionError,
)

log = logging.getLogger(__name__)

def configure_vlan_dot1q_tag_native(device):
    """ configure vlan dot1q tag native
        Args:
            device ('obj')    : device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f'configure vlan dot1q tag native on {device}')
    cmd = ["vlan dot1q tag native"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure vlan dot1q tag native on {device}.Error:\n{e}')

def unconfigure_vlan_dot1q_tag_native(device):
    """ unconfigure vlan dot1q tag native
        Args:
            device ('obj')    : device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f'unconfigure vlan dot1q tag native on {device}')
    cmd = ["no vlan dot1q tag native"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not unconfigure vlan dot1q tag native on {device}.Error:\n{e}')            
            


def configure_subinterface_dot1q_encapsulation(
    device,
    interface,
    vlan,
    vrf_name=None,
    ip_address=None,
    mask=None,
    no_shutdown=False,
):
    """ configure subinterface dot1q encapsulation
        Args:
            device ('obj')    : device to use
            interface ('str') : interface name
            vlan ('str')      : vlan id
            vrf_name ('str', optional): VRF name for ip vrf forwarding
            ip_address ('str', optional): IPv4 address to configure
            mask ('str', optional): IPv4 subnet mask
            no_shutdown ('bool', optional): Configure no shutdown
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if ip_address and not mask:
        raise ValueError("mask must be provided when ip_address is provided")

    cmd = [f"interface {interface}.{vlan}",
           f"encapsulation dot1q {vlan}"]
    if vrf_name:
        cmd.append(f"ip vrf forwarding {vrf_name}")
    if ip_address:
        cmd.append(f"ip address {ip_address} {mask}")
    if no_shutdown:
        cmd.append("no shutdown")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure {cmd} on device {device.name}. Error:\n{e}")


def unconfigure_subinterface_dot1q_encapsulation(
    device,
    interface,
    vlan,
    remove_subinterface=False,
):
    """ unconfigure subinterface dot1q encapsulation
        Args:
            device ('obj')    : device to use
            interface ('str') : interface name
            vlan ('str')      : vlan id
            remove_subinterface ('bool', optional): Remove the full
                subinterface with ``no interface <interface>.<vlan>``
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if remove_subinterface:
        cmd = [f"no interface {interface}.{vlan}"]
    else:
        cmd = [f"interface {interface}.{vlan}",
               f"no encapsulation dot1q {vlan}"]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure {cmd} on device {device.name}. Error:\n{e}")


def configure_subinterface_qinq_encapsulation(device, interface, qinq):
    """ configure subinterface qinq encapsulation
        Args:
            device ('obj')    : device to use
            interface ('str') : interface name
            qinq ('str')      : qinq vlan id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"interface {interface}.{qinq}",
        f"encapsulation dot1q {qinq} second {qinq}"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure {cmd} on device {device.name}. Error:\n{e}")


def unconfigure_subinterface_qinq_encapsulation(device, interface, qinq):
    """ unconfigure subinterface qinq encapsulation
        Args:
            device ('obj')    : device to use
            interface ('str') : interface name
            qinq ('str')      : qinq vlan id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"interface {interface}.{qinq}",
        f"no encapsulation dot1q {qinq} second {qinq}"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure {cmd} on device {device.name}. Error:\n{e}")
