# Python
import logging
import time
import re

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog
from unicon.eal.expect import Spawn, TimeoutError


log = logging.getLogger(__name__)

def execute_set_memory_debug_incremental_starting_time(device, starting_time=None):
    """
        Args:
            device ('obj'): device to use
            starting_time ('str'): start time for memory debug
            
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "set memory debug incremental starting-time".format(starting_time=starting_time)

    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to perform set memory debug incremental starting time {device.name}. Error:\n{e}")