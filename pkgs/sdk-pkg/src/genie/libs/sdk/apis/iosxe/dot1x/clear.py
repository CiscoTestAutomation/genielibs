# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure


# Logger

log = logging.getLogger(__name__)

def clear_access_session_intf(device, intf):
    """ clear access-session interface {}
        Args:
            device (`obj`): Device object
            intf('str'): Name of the interface to clear access-session
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.execute('clear access-session interface {intf}'.format(intf=intf))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear access-session interface on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )
