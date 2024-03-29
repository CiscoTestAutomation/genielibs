"""Common configure functions for traceroute"""

# Python
import logging
log = logging.getLogger(__name__)
# Unicon
from unicon.core.errors import SubCommandFailure

def configure_l2_traceroute(device):
    """ Configure l2 traceroute
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring l2 traceroute
    """
    log.debug(" Configuring l2 traceroute")

    try:
        device.configure("l2 traceroute")
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure l2 traceroute {e}"
        )

def unconfigure_l2_traceroute(device):
    """ Unconfigure l2 traceroute
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring l2 traceroute
    """
    log.debug(" Unconfiguring l2 traceroute")

    try:
        device.configure("no l2 traceroute")
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure l2 traceroute {e}"
        )