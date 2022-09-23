"""Common configure functions for interface"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Steps
from pyats.aetest.steps import Steps

# Genie
from genie.harness.utils import connect_device

log = logging.getLogger(__name__)

def config_standby_console_enable(device):
    """ Enable standby console

        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    log.info("Configuring standby console enable cli")

    try:
        device.configure(
            [
                "redundancy",
                "main-cpu",
                "standby console enable"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Enabling Standby Console failed. Error: {error}".format(error=e)
        )
