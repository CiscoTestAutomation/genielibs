"""Common configure functions for mpls"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def config_mpls_ldp_on_interface(device, interface):
    """ Config ldp on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Configuring ldp on {} on {}".format(interface, device.name))

    try:
        device.configure(["interface {}".format(interface), "mpls ip"])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not activate "mpls ip" on interface {interface}'.format(
                interface=interface
            )
        )


def remove_mpls_ldp_from_interface(device, interface):
    """ Remove ldp on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Removing ldp on {} on {}".format(interface, device.name))

    try:
        device.configure(["interface {}".format(interface), "no mpls ip"])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not remove "mpls ip" from interface {interface}'.format(
                interface=interface
            )
        )
