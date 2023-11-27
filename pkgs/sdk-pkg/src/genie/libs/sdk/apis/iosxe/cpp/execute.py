"""Execute cpp related command"""

# Python
import re
import time
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog
from unicon.eal.expect import Spawn, TimeoutError

log = logging.getLogger(__name__)

def execute_clear_control_plane(device):
    """ execute clear control-plane all in switch
        Args:
            device ('obj'): Device object
        Returns:
            Execution output
        Raises:
            SubCommandFailure
    """
    log.debug(f"execute clear control-plane all on {device}")

    cmd = 'clear control-plane *'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to do clear control-plane all on device {device}. Error:\n{e}"
            )
            