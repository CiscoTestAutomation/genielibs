"""Common clear functions for nhrp"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def clear_ip_nhrp(device,
                counters=False,
                shortcut=False,
                stats=False,
                vrf=None,
                timeout=30):
    """ clear_ip_nhrp
        Args:
            device (`obj`): Device object
            counters('boolean', optional): NHRP Counters, default is False
            shortcut('boolean', optional): NHRP shortcut entries, default is False
            stats('boolean', optional): Clears all IPv4 Stats Information for all Interfaces, default is False
            vrf('str', optional) : vrf name, default is None
            timeout('int', optional): timeout for exec command execution, default is 30
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = "clear ip nhrp"
    if counters:
        cmd += " counters"
        
    if shortcut:
        cmd += " shortcut"
        
    if stats:
        cmd += " stats"

    if vrf is not None:
        cmd += f" vrf {vrf}"

    try:   
        device.execute(cmd, 
                    error_pattern=[f'VRF \"{vrf}\" is not valid.','% Invalid input detected at \'\^\' marker\.'], 
                    timeout=timeout)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ip nhrp on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def clear_dmvpn(device,
                peer=None,
                static=False,
                vrf=None,
                timeout=30):
    """ clear_dmvpn
        Args:
            device (`obj`): Device object
            peer('str', optional): DMVPN peer, default is None
            static('boolean', optional): static dmvpn entries, default is False
            vrf('str', optional) : vrf name, default is None
            timeout('int', optional): timeout for exec command execution, default is 30
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = "clear dmvpn session"
    if peer is not None:
        cmd += f" peer {peer}"
        
    if static:
        cmd += " static"

    if vrf is not None:
        cmd += f" vrf {vrf}"

    try:   
        device.execute(cmd, 
                    error_pattern=[f'VRF \"{vrf}\" is not valid.','% Invalid input detected at \'\^\' marker\.'], 
                    timeout=timeout)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear dmvpn on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def clear_dmvpn_statistics(device,
                interface=None,
                vrf=None,
                timeout=30):
    """ clear_dmvpn_statistics
        Args:
            device (`obj`): Device object
            interface('str', optional): Tunnel interface name, default is None
            vrf('str', optional) : vrf name, default is None
            timeout('int', optional): timeout for exec command execution, default is 30
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    
    cmd = "clear dmvpn statistics"
    if interface is not None:
        cmd += f" interface Tunnel {interface}"

    if vrf is not None:
        cmd += f" vrf {vrf}"
    
    try:
        device.execute(cmd, 
                    error_pattern=[f'VRF \"{vrf}\" is not valid.','% Invalid input detected at \'\^\' marker\.'], 
                    timeout=timeout)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear dmvpn statistics on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )