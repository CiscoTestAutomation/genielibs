import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

"""Execute CLI functions for flow"""
def execute_set_fnf_debug(device):
    """ set platform software trace fed switch active fnf debug
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"set platform software trace fed switch active fnf debug"
    try:
        device.execute(cmd)
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not set platform software trace fed switch active fnf debug on device. Error:\n{e}')
        
def execute_set_fnf_verbose(device):
    """ set platform software trace fed switch active fnf verbose
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"set platform software trace fed switch active fnf verbose"
    try:
        device.execute(cmd)
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not set platform software trace fed switch active fnf verbose on device. Error:\n{e}')
