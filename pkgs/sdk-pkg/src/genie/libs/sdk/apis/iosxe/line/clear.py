# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure


# Logger

log = logging.getLogger(__name__)

def clear_raw_socket_transport_statistics_all(device):
    """ clear raw-socket transport statistics all
        Args:
            device (`obj`): Device object of the router on which statistics has to be cleared
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.execute('clear raw-socket transport statistics all')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear raw-socket transport statistics on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )
