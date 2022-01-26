# Python
import logging
import time

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)


def enable_http_server(device):
    """Configure ip http server
    Args:
        device (obj): Device object
    Returns:
            None
    Raises:
            SubCommandFailure
    """

    try:
        device.configure("ip http server")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in enable http server "
            "on device {device} "
            "Error: {e}".format(
                device=device.name,
                e=str(e)
            )
        ) from e

    else:
        log.info("Successfully enabled http server for {}".format(device.name))


def set_clock_calendar(device):
    """Configure clock calendar-valid 
    Args:
        device (obj): Device object
    Returns:
            None
    Raises:
            SubCommandFailure
    """

    try:
        device.configure("clock calendar-valid")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in set valid clock calender "
            "on device {device} "
            "Error: {e}".format(
                device=device.name,
                e=str(e)
            )
        ) from e

    else:
        log.info("Successfully set clock calendar for {}".format(device.name))

