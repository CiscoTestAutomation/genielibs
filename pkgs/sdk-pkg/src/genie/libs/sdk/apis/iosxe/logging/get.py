""" Common retrieve functions for logging """

# Unicon
from unicon.core.errors import SubCommandFailure

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
            list of entries from logging system
        Raises:
            None
    """
    log.info("Getting logs on {}".format(device.hostname))

    try:
        out = device.parse("show logging")
    except SchemaEmptyParserError:
        return None

    return out.get("logs", None)

def execute_clear_logging(device):
    """ Clears logging logs
        execute - clear logging

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            None
    """
    log.info("Clearing logs on {}".format(device.hostname))

    try:
        out = device.execute("clear logging")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not Clear Logging, Error: {error}'.format(
                error=e)
        )
