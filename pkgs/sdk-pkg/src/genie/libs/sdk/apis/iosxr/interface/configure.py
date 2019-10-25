"""Common configure functions for Interface"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_interface_point_to_point(device, process_id, interface):
    """ Configure Interface point to point

        Args:
            device ('obj'): Device object
            process_id ('str'): Router ISIS process ID
            interface ('str'): Interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            "router isis {process_id}\n"
            " interface {interface}\n"
            "  point-to-point\n"
            " !\n".format(
                process_id=process_id,
                interface=interface,
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure interface point-to-point on {device}".format(
                device=device.name,
            )
        )

def configure_interface_passive(device, process_id, interface):
    """ Configure Interface passive

        Args:
            device ('obj'): Device object
            process_id ('str'): Router ISIS process ID
            interface ('str'): Interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            "router isis {process_id}\n"
            " interface {interface}\n"
            "  passive\n"
            " !\n".format(
                process_id=process_id,
                interface=interface,
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure interface passive on {device}".format(
                device=device.name,
            )
        )