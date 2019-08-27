""" Common get info functions for system """

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_current_system_datetime(device):
    """ Returns current time of system

        Args:
            device ('obj'): device to use

        Returns:
            current time ('str')
        Raises:
            None
    """
    log.info("Getting current system time")

    try:
        out = device.parse("show clock")
    except SchemaEmptyParserError:
        return None

    if out and "time" in out and "month" in out and "day" in out:
        return "{} {} {}".format(out["month"], out["day"], out["time"])
