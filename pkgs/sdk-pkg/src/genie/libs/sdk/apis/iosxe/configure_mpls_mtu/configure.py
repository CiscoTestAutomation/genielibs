''' Common Config functions for mpls mtu'''

import logging
log = logging.getLogger(__name__)
# Unicon
from unicon.core.errors import SubCommandFailure

def configure_mpls_mtu(device, interface, size):
    """Configure mpls mtu on interface
        Example : mpls mtu 1400

    Args:
        device('obj'): Device object
        interface('str'): Device interface
        size('int'): Size of maximum size of the IP packet that can still be sent on a data link, without fragmenting the packet 
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}", f"mpls mtu {size}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure mpls mtu on interface") 