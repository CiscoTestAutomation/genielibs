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

def clear_authentication_session(device):
    """ clear all authenticated sessions
    Args:
        device ('obj'): Device object
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Clear authenticated sessions")
	
    cmd=f"clear authentication sessions"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not clear authenticated sessions. Error:\n{e}")
    