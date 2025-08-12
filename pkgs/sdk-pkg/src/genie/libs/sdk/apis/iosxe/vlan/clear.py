"""Common clear functions for vlan"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def clear_errdisable_intf_vlan(device, intf, vlan=None):
    """ clear errdisable interface {} vlan
        Args:
            device (`obj`): Device object
            intf('str'): Name of the interface to clear errdisable
            Vlan('str', optional): Name of the vlan to to clear errdisable, default value is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        if not vlan == None:
            device.execute('clear errdisable interface {intf} vlan {vlan}'.format(intf=intf,vlan=vlan))
        else:
            device.execute('clear errdisable interface {intf} vlan'.format(intf=intf))
    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear errdisable interface on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def clear_vlan(device, vlan_id=None, interface=None, statistics=False):
    """
    Execute 'clear vlan' commands on the device.

    Args:
        device (`obj`): Genie device object
        vlan_id (`int` or `str`, optional): VLAN ID to clear
        interface (`str`, optional): Interface name (e.g., 'GigabitEthernet1/0/2')
        statistics (`bool`): Whether to clear all VLAN statistics

    Returns:
        output (`str`): Raw output from the executed command
    """
    cmd = "clear vlan"

    if statistics:
        cmd += " statistics"
    elif vlan_id:
        cmd += f" {vlan_id}"
    elif interface:
        cmd += f" {interface}"

    try:
        device.execute(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear vlan on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )