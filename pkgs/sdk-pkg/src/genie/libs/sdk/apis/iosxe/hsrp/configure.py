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


def unconfigure_hsrp_interface(device, interface, version, group):
    """ unonfigures vlan interface standby group IP
        Example: standby 0 ip 10.1.0.3
    Args:
        device ('obj'): Device object
        interface ('int'): Vlan <vlan Id> (Range 1-4093) / physical interface  
        group ('int'): Group number (Range 0-255)
        version('int'): Version number (Range 1-2)
        
    Return:
        None
    Raises:
            SubCommandFailure: Failed to unconfigure hsrp interface
    """

    cmd = []
    cmd.append(f"interface {interface}")
    cmd.append(f"no standby version {version}")
    cmd.append(f"no standby {group}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure interface hsrp standby group on {device.name}. Error:\n{e}")

def configure_vrrp_interface(device, interface, group_number, advertisement_interval,
                             priority_level, address_family, ipv4_or_ipv6_address):
    """ Configures vlan interface standby group IP
        make sure this command is already enabled in device fhrp version vrrp v3
        
    Args:
        device ('obj'): Device object
        interface ('str'): Vlan <vlan Id> (Range 1-4093) / physical interface  
        group_number('int'): group number (Range 1-255)
        advertisement_interval('int'): Advertisement interval range <100-40950> 
        Advertisement interval in milliseconds
        priority_level('int'): priority level range <1-254>
        address_family ('str'): address family ipv4 or ipv6 to use
        ipv4_or_ipv6_address ('str'): based on the address family 
        please use the ipv4 or ipv6 address to configure
        
    Return:
        None
    Raises:
            SubCommandFailure: Failed to configure vrrp interface
    """
    
    config_cmd = [
        f"interface {interface}",
        f"vrrp {group_number} address-family {address_family}",
        f"timers advertise {advertisement_interval}",
        f"priority {priority_level}",
        f"address {ipv4_or_ipv6_address} primary"
        ]
  
    try:
        device.configure(config_cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure interface vrrp standby group on {device.name}. Error:\n{e}")

def unconfigure_vrrp_interface(device, interface, group_number, address_family):
    """ unconfigures vlan interface standby group IP
        make sure this command is already enabled in device fhrp version vrrp v3
        
    Args:
        device ('obj'): Device object
        interface ('str'): Vlan <vlan Id> (Range 1-4093) / physical interface  
        group_number('int'): group number (Range 1-255)
        address_family ('str'): address family ipv4 or ipv6 to use
    Return:
        None
    Raises:
            SubCommandFailure: Failed to unconfigure vrrp interface
    """
    config_cmd = [
        f"interface {interface}",
        f"no vrrp {group_number} address-family {address_family}"
        ]
  
    try:
        device.configure(config_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure interface vrrp standby group on {device.name}. Error:\n{e}")