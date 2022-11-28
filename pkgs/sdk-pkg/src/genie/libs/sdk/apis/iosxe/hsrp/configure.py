"""Common configure functions for HSRP"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_interface_vlan_standby_ip(device, vlan_number, group, ip_address):
    """ Configures vlan interface standby group IP
        Example: standby 0 ip 10.1.0.3

    Args:
        device ('obj'): Device object
        vlan_number ('int'): Vlan interface number (Range 1-4093) 
        group ('int'): Group number (Range 0-255)
        ip_address ('str'): Virtual IP address

    Return:
        None

    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring vlan interface standby group on {device.name}")
    cmd = [
            f"interface vlan {vlan_number}",
            f"standby {group} ip {ip_address}"
          ]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure vlan interface standby group on {device.name}. Error:\n{e}")

def unconfigure_interface_vlan_standby_ip(device, vlan_number, group, ip_address):
    """ Unconfigures vlan interface standby group IP
        Example: no standby 0 ip 10.1.0.3

    Args:
        device ('obj'): Device object
        vlan_number ('int'): Vlan interface number (Range 1-4093) 
        group ('int'): Group number (Range 0-255)
        ip_address ('str'): Virtual IP address

    Return:
        None

    Raise:
        SubCommandFailure
    """
    log.info(f"Unconfiguring vlan interface standby group on {device.name}")
    cmd = [
            f"interface vlan {vlan_number}",
            f"no standby {group} ip {ip_address}"
          ]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure vlan interface standby group on {device.name}. Error:\n{e}")

def configure_interface_vlan_standby_timers(device, vlan_number, group, interval, hold_time):
    """ Configures vlan interface standby timers
        Example: standby 0 timers 1 4

    Args:
        device ('obj'): Device object
        vlan_number ('int'): Vlan interface number (Range 1-4093) 
        group ('int'): Group number (Range 0-255)
        interval ('int'): Hello interval in seconds (Rang 1-254)
        hold_time ('int'): Hold time in seconds (Range 2-255)

    Return:
        None

    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring vlan interface standby timers on {device.name}")
    cmd = [
            f"interface vlan {vlan_number}",
            f"standby {group} timers {interval} {hold_time}"
          ]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure vlan interface standby timers on {device.name}. Error:\n{e}")

def unconfigure_interface_vlan_standby_timers(device, vlan_number, group):
    """ Unconfigures vlan interface standby timers
        Example:  no standby 0 timers

    Args:
        device ('obj'): Device object
        vlan_number ('int'): Vlan interface number (Range 1-4093) 
        group ('int'): Group number (Range 0-255)

    Return:
        None

    Raise:
        SubCommandFailure
    """
    log.info(f"Unconfiguring vlan interface standby timers on {device.name}")
    cmd = [
            f"interface vlan {vlan_number}",
            f"no standby {group} timers"
          ]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure vlan interface standby timers on {device.name}. Error:\n{e}")

def configure_interface_vlan_standby_preempt(device, vlan_number, group):
    """ Configures vlan interface standby preempt
        Example: standby 0 preempt

    Args:
        device ('obj'): Device object
        vlan_number ('int'): Vlan interface number (Range 1-4093) 
        group ('int'): Group number (Range 0-255)

    Return:
        None

    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring vlan interface standby preempt on {device.name}")
    cmd = [
            f"interface vlan {vlan_number}",
            f"standby {group} preempt"
          ]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure vlan interface standby preempt on {device.name}. Error:\n{e}")

def unconfigure_interface_vlan_standby_preempt(device, vlan_number, group):
    """ Unconfigures vlan interface standby preempt
        Example: no standby 0 preempt

    Args:
        device ('obj'): Device object
        vlan_number ('int'): Vlan interface number (Range 1-4093) 
        group ('int'): Group number (Range 0-255)

    Return:
        None

    Raise:
        SubCommandFailure
    """
    log.info(f"Unconfiguring vlan interface standby preempt on {device.name}")
    cmd = [
            f"interface vlan {vlan_number}",
            f"no standby {group} preempt"
          ]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure vlan interface standby preempt on {device.name}. Error:\n{e}")
