"""Common configure functions for ipv6"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def config_enable_ipv6_routing(device):
    """ Configure ipv6 unicast-routing on device

        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("ipv6 unicast-routing")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configure ipv6 unicast-routing. Error {e}".format(e=e)
        )


def unconfig_disable_ipv6_routing(device):
    """ Unconfigure ipv6 unicast-routing on device

        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no ipv6 unicast-routing")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ipv6 unicast routing. Error {e}".format(e=e)
        )
