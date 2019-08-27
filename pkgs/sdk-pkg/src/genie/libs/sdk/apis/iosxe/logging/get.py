""" Common retrieve functions for logging """

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_logging_logs(device):
    """ Returns list of entries in the logging system

        Args:
            device ('obj'): device to use

        Returns:
            list of enteries from logging system
        Raises:
            None
    """
    log.info("Getting logs on {}".format(device.hostname))

    try:
        out = device.parse("show logging")
    except SchemaEmptyParserError:
        return None

    return out.get("logs", None)
