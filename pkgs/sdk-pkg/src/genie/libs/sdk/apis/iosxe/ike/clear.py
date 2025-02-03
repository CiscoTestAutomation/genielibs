"""Common clear functions for IKEv2"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def clear_ikev2_sa(device,
                fast=False,
                local=False,
                remote=False,
                psh=False,
                fvrf=None,
                timeout=30):
    """ clear_ikev2_sa
        Args:
            device (`obj`): Device object
            fast('boolean', optional): clearing sa fast, default is False
            local('boolean', optional): Clear all ikev2 SAs with local address, default is False
            remote('boolean', optional): Clear all ikev2 SAs with remote address, default is False
            psh('boolean', optional): Platform Service Handler, default is False
            fvrf('str', optional): Front door VRF name, default is None
            timeout('int', optional): timeout for exec command execution, default is 30
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    cmd = f"clear crypto ikev2 sa"
    if fast:
        cmd += " fast"
        
    if remote:
        cmd += " remote"
        
    if local:
        cmd += " local"

    if psh:
        cmd += " psh"

    if fvrf is not None:
        cmd += f" fvrf {fvrf}"

    try:    
        device.execute(cmd, 
            error_pattern=[f' No VRF named {fvrf} exists',r'% Invalid input detected at \'\^\' marker\.'], 
            timeout=timeout)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ikev2 sa on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )