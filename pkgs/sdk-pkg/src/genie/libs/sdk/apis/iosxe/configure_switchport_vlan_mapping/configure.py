''' Common Config functions for mpls mtu'''

import logging
log = logging.getLogger(__name__)
# Unicon
from unicon.core.errors import SubCommandFailure

def configure_switchport_vlan_mapping(device, interface, vlan, translation_vlan=None):
    """configure switchport vlan mapping 
        Example : switchport vlan mapping 5

    Args:
        device('obj'): Device object
        interface('str'): Device interface
        vlan('str'): Device Vlan to Map
        translation('str',optional): translation vlan to map
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}"]
    if translation_vlan:
        cmd.append(f"switchport vlan mapping {vlan} {translation_vlan}")
    else:
        cmd.append(f"switchport vlan mapping {vlan}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure switchport vlan mapping") 

def unconfigure_switchport_vlan_mapping(device, interface, vlan, translation_vlan=None):
    """Unconfigure switchport vlan mapping 
        Example : no switchport vlan mapping 5

    Args:
        device('obj'): Device object
        interface('str'): Device interface
        vlan('str'): Device Vlan to Map
        translation('str',optional): translation vlan to map
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}"]
    if translation_vlan:
        cmd.append(f"no switchport vlan mapping {vlan} {translation_vlan}")
    else:
        cmd.append(f"no switchport vlan mapping {vlan}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure switchport vlan mapping") 