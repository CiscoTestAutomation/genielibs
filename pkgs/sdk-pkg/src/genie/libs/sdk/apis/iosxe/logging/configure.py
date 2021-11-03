
# Python
import logging
from unicon.eal.dialogs import Statement, Dialog

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def configure_logging_console(device):
    """ logging console
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('logging console')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure logging console on {device}. Error:\n{error}".format(device=device, error=e))


def unconfigure_logging_console(device):
    """ no logging console
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('no logging console')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure logging console on {device}. Error:\n{error}".format(device=device, error=e))
           
def configure_logging_monitor(device):
    """ logging monitor
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('logging monitor')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure logging monitor on {device}. Error:\n{error}".format(device=device, error=e))


def unconfigure_logging_monitor(device):
    """ no logging monitor
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('no logging monitor')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure logging monitor on {device}. Error:\n{error}".format(device=device, error=e))
