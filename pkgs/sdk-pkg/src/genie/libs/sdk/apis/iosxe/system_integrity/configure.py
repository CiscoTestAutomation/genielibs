''' Common Config and UnConfig functions for system integrity'''
import logging
log = logging.getLogger(__name__)
# Unicon
from unicon.core.errors import SubCommandFailure

def enable_system_integrity(device):
    """Configure system integrity
    Args:
        device('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    try:
        device.configure("system integrity")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure system integrity on {device}.Error:\n{e}") 

def disable_system_integrity(device):
    """UnConfigure system integrity
    Args:
        device('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    try:
        device.configure("no system integrity")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure system integrity on {device}.Error:\n{e}")


