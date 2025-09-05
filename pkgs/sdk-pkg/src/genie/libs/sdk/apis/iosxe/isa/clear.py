"""Common clear functions for ISAkmp"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def clear_cry_ISAkmp(device,
                timeout=10):
    """ clear_cry_ISAkmp
        Args:
            device (`obj`): Device object
            timeout('int', optional): timeout for exec command execution, default is 10
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    cmd = f"clear crypto isakmp"
    try:    
        device.execute(cmd,
            timeout=timeout)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear isa on {device}. Error:\n{error}"
                .format(device=device, error=e)
        ) 