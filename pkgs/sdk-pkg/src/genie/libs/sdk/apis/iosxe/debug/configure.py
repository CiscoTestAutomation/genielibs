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
            [
            "debug {parameter}".format(parameter=parameter)
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not enable debug for {parameter}".format(
                parameter=parameter
            )
         )

def set_filter_packet_capture_inject(device, filter):
    """ Set filter for packet capture inject
        Args:
            device (`obj`): Device object
            filter (`str`): Filter to be set

        Return:
            None

        Raise:
            SubCommandFailure: Failed setting filter for packet capture inject
    """

    try:
        device.execute(['debug platform software fed active inject packet-capture '
                          'set-filter "{filter}"'.format(filter=filter)])

    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not Set filter for packet capture inject'
        )

def start_packet_capture_inject(device):
    """ Start packet capture inject
        Args:
            device (`obj`): Device object

        Return:
            None

        Raise:
            SubCommandFailure: Failed start packet capture inject
    """

    try:
        device.execute(["debug platform software fed active inject packet-capture start"])

    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not start packet capture inject'
        )

def stop_packet_capture_inject(device):
    """ Stop packet capture inject
        Args:
            device (`obj`): Device object

        Return:
            None

        Raise:
            SubCommandFailure: Failed stop packet capture inject
    """

    try:
        device.execute(["debug platform software fed active inject packet-capture stop"])

    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not stop packet capture inject'
        )

