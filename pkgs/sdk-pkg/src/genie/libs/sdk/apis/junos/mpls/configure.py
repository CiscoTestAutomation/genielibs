"""Common configure functions for mpls on junos"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def config_mpls_ldp_on_interface(device, interface):
    """ Config ldp on interface on junos device

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Return:
            None
    """
    log.info("Configuring ldp on {} on {}".format(interface, device.name))

    try:
        device.configure("set protocols ldp interface {}".format(interface))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ldp on {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )


def remove_mpls_ldp_from_interface(device, interface):
    """ Remove ldp on interface on junos device

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Return:
            None
    """
    log.info("Removing ldp on {} on {}".format(interface, device.name))

    try:
        device.configure("delete protocols ldp interface {}".format(interface))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove ldp configuration on {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )
