"""Execute Switch related command"""

# Python
import logging

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def execute_switch_renumber(device, switch_number, switch_renumber):
    """ 
        Args:
            device ('obj'): device to use  
            switch_number ('int'): Switch id of node which should be renumbered
            switch_renumber ('int'): New switch id to which the node should be renumbered
        Returns:
            None
        Raises:
            SubCommandFailure
    """
        # Unicon Statement/Dialog
    execute_switch_renumber = Statement(
        pattern=r".*Do you want to continue\?\[y/n\]\? \[yes\]: ",
        action="sendline(yes)",
        loop_continue=False,
        continue_timer=False
    )

    cmd = f"switch {switch_number} renumber {switch_renumber}"

    try:
        device.execute(cmd, reply=Dialog([execute_switch_renumber]), error_pattern=["% No such resource", "% Invalid input detected .*"])
    except SubCommandFailure as err:
        log.error(f"Failed to execute {cmd}': {err}".format(err=err))
        raise
