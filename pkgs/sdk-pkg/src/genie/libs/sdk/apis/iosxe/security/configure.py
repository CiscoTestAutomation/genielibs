'''IOSXE execute functions for platform'''

# Python
import logging
import time

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

# Logger
log = logging.getLogger(__name__)

def configure_switchport_port_security_aging_time(device, interface, time):
    """ Configure switchport port-security aging time
        Args:
            device ('obj'): Device object
            time ('str'); aging time in minutes
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f'interface {interface}',
        f'switchport port-security aging time {time}'
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure switchport port-security aging time on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_switchport_port_security_aging_type(device, interface, aging="absolute"):
    """ Configure switchport port-security aging type
        Args:
            device ('obj'): Device object
            aging ('str', optional); Absolute aging / aging based on inactivity time period, default value 'absolute'
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f'interface {interface}',
        f'switchport port-security aging type {aging}'
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure switchport port-security aging type on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_switchport_port_security_maximum(device, interface, address, vlan_type=None):
    """ Configure switchport port-security maximum
        Args:
            device ('obj'): Device object
            address ('str'); maximum address
            vlan_type ('str', optional): voice or access vlan. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f'interface {interface}',
        f'switchport port-security maximum {address}{f" vlan {vlan_type}" if vlan_type else ""}'
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure switchport port-security aging type on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_switchport_port_security_mac_address(device, interface, address, vlan_type=None):
    """ Configure switchport port-security mac-address
        Args:
            device ('obj'): Device object
            address ('str'); sticky / 48 bit mac address
            vlan_type ('str', optional): voice or access vlan. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f'interface {interface}',
        f'switchport port-security mac-address {address}{f" vlan {vlan_type}" if vlan_type else ""}'
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure switchport port-security mac-address on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )