"""Execute redundancy related command"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def execute_redundancy_reload(device,switch):
    """
        Args:
            device ('obj'): device to use
            switch ('str'): switch arg on which reload as to be done
        Returns:
            Return the reload command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "redundancy reload {switch}".format(switch=switch)

    try:
        out = device.execute(cmd)
    except SubCommandFailure:
        raise SubCommandFailure('Failed to perform redundancy reload')
    return out

