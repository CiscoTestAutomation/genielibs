"""Common configure functions for interface"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def config_enable_ipv6_routing(device):

    """ configure ipv6 routing on device

        Args:
            device (`obj`): Device object
        Returns:
            None
    """
    try:
        device.configure("ipv6 unicast-routing")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configure ipv6 unicast-routing. Error {e}".format(e=e)
        )

