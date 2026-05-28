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
            


def configure_subinterface_dot1q_encapsulation(device, interface, vlan):
    """ configure subinterface dot1q encapsulation
        Args:
            device ('obj')    : device to use
            interface ('str') : interface name
            vlan ('str')      : vlan id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"interface {interface}.{vlan}",
           f"encapsulation dot1q {vlan}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure {cmd} on device {device.name}. Error:\n{e}")


def unconfigure_subinterface_dot1q_encapsulation(device, interface, vlan):
    """ unconfigure subinterface dot1q encapsulation
        Args:
            device ('obj')    : device to use
            interface ('str') : interface name
            vlan ('str')      : vlan id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
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
