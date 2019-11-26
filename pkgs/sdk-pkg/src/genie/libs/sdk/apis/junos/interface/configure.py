"""Common configure functions for junos interface"""

# Python
import logging

# unicon
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def default_interface(device, interfaces):
    """ Reset junos interface configuration 

        Args:
            device (`obj`): Device object
            interfaces (`list`): List of interfaces to be defaulted
        Returns:
            None
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r"Delete everything under this level?.*",
                action="sendline(yes)",
                loop_continue=True,
                continue_timer=False,
            )
        ]
    )

    for intf in interfaces:
        config_cmd = ["edit interfaces {}".format(intf), "delete"]

        try:
            device.configure(config_cmd, reply=dialog)
            log.info("Successfully defaulted {}".format(intf))
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Couldn't default {interface}. Error:\n{error}".format(
                    interface=intf, error=e
                )
            )


def shut_interface(device, interface):
    """ Shut interface on device

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    config_command = "set interfaces {interface} disable".format(
        interface=interface
    )

    try:
        device.configure(config_command)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not disable interface {interface} on device {device}".format(
                interface=interface, device=device.name
            )
        )

def unshut_interface(device, interface):
    """ Unshut interface on device

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    config_command = "delete interfaces {interface} disable".format(
        interface=interface
    )

    try:
        device.configure(config_command)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not enabled interface {interface} on device {device}".format(
                interface=interface, device=device.name
            )
        )
