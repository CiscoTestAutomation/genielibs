"""Common clear functions for mka"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def clear_mka_session(device, timeout=30):
    """ clear_mka_session
        Args:
            device (`obj`): Device object
            timeout (`int`, optional): Timeout in seconds, default value 30
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    cmd = "clear mka sessions"
    
    try: 
        device.execute(cmd, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear mka session on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

