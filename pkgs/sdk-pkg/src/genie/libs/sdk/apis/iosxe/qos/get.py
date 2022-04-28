"""Common configure functions for api"""

# Python
import logging
import re

# unicon
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.utils import has_configuration

log = logging.getLogger(__name__)

def get_run_configuration(device, option):
    """ search config in show running-config output and return
        Args:
            device (`obj`): Device object
            option (`str`): key word to search
        Returns:
            config (`str`): search result
        Raises:
            None
    """
    try:
        out = device.execute("show run | include {}".format(option))
        config = None
        
        m = re.search(r"^(?P<cfg>[\w\s]+)$".format(option), out)
        if m:
            config = m.groupdict()["cfg"]
        return config
    except SubCommandFailure as e:
        log.error('No running configuration information found')
        return

def get_startup_configuration(device, option):
    """ search config in show startup-config output
        Args:
            device (`obj`): Device object
            option (`str`): key word to search
        Returns:
            config (`str`): search result
        Raises:
            None
    """
    try:
        out = device.execute("show startup-config | include {}".format(option))
        
        config = None
        
        m = re.search(r"^(?P<cfg>[\w\s]+)$".format(option), out)
        if m:
            config = m.groupdict()["cfg"]
        return config
            
    except SubCommandFailure as e:
        log.error('No startup configuration information found')
        return
    

def get_status_for_rollback_replacing_in_flash(device):
    """ search the status for rollback while replacing in flash memory
        Args:
            device (`obj`): Device object
        Returns:
            config (`str`): search result
        Raises:
            None
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r".*This will apply all necessary additions and deletions.*",
                action="sendline(y)",
                loop_continue=False,
                continue_timer=False,
            )
        ]
    )
    try:
        out = device.execute("configure replace flash:backup_config",reply=dialog)
        
        config = None
        m = re.search(r"Rollback +(?P<rollback_status>\w+)$", out)
        if m:
            config = m.groupdict()["rollback_status"]
        return config
    except SubCommandFailure as e:
        log.error('No configuration information found')
        return

