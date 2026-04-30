"""Enable debug for mentioned parameters"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def enable_debug(device, parameter):
    """ Enable debug for the mentioned parameter
        Args:
            device ('obj'): device to use
            parameter ('str'): parameter for which debug has to be enabled
        Returns:
            None
        Raises:
            SubCommandFailure: Failed enabling debug
    """
    log.info(
        "Enabling debug for name={parameter} "
        .format(parameter=parameter)
    )

    try:
        device.execute(
            "debug {parameter}".format(parameter=parameter)
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not enable debug for {parameter}".format(
                parameter=parameter
            )
         )


def disable_debug(device, parameter):
    """ Disable debug for the mentioned parameter
        Args:
            device ('obj'): device to use
            parameter ('str'): parameter for which debug has to be disabled
        Returns:
            None
        Raises:
            SubCommandFailure: Failed disabling debug
    """
    log.debug(
        "Disabling debug for name={parameter} "
        .format(parameter=parameter)
    )

    try:
        device.execute(
            "no debug {parameter}".format(parameter=parameter)
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not disable debug for {parameter}".format(
                parameter=parameter
            )
        )
