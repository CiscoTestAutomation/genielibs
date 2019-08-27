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
