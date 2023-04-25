''' Common Config functions for mpls mtu'''

import logging
log = logging.getLogger(__name__)
# Unicon
from unicon.core.errors import SubCommandFailure

def configure_switchport_vlan_mapping(device, interface, vlan):
    """configure switchport vlan mapping 
        Example : switchport vlan mapping 5

    Args:
        device('obj'): Device object
        interface('str'): Device interface
        vlan('str'): Device Vlan to Map
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}", f"switchport vlan mapping {vlan}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure switchport vlan mapping") 

def unconfigure_switchport_vlan_mapping(device, interface, vlan):
    """Unconfigure switchport vlan mapping 
        Example : no switchport vlan mapping 5

    Args:
        device('obj'): Device object
        interface('str'): Device interface
        vlan('str'): Device Vlan to Map
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}", f"no switchport vlan mapping {vlan}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure switchport vlan mapping") 