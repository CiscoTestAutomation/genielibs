""" Common utility functions for static routing"""

# Python
import logging
# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)
LOG = log

def unconfigure_static_ip_route_all(device):
    """
        no ip route *
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """
    log.debug("no ip route *")

    try:
        device.configure("no ip route *")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure static ip route on {device}. Error:\n{error}".format(
                device=device, error=e
            )
        ) 