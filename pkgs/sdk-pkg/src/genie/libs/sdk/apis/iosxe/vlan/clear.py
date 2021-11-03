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
