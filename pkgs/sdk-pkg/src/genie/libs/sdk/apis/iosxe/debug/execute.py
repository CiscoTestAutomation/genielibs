"""Execute debug related commands"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def execute_show_debug(device, filter_string=None):
    """ Execute show debug command with optional filter
        Args:
            device ('obj'): Device object
            filter_string ('str', optional): Filter string to append to the command
                                          Examples: 'include <pattern>', 'exclude <pattern>', 
                                          'begin <pattern>', 'section <pattern>'
        Returns:
            str: Command output
        Raises:
            SubCommandFailure: Failed to execute show debug command
    """
    
    # Build the base command
    cmd = "show debug"
    
    # Add filter if specified
    if filter_string:
        cmd = f"{cmd} | {filter_string}"
    
    try:
        return device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to execute '{cmd}' on device {device}. Error:\n{e}")