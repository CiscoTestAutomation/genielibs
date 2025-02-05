'''IOSXE execute functions for platform'''

# Python
import re
import logging
import time

# pyATS
from pyats.async_ import pcall
from pyats.utils.fileutils import FileUtils

# Genie
from genie.utils import Dq
from genie.harness.utils import connect_device
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import StateMachineError,SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def execute_set_config_register():
    '''Set config register to load image in boot variable        
    '''

    log.info("Config register configuration not supported on IOT platforms")


def execute_locate_switch(device, seconds, switch_number=None, switch_type=None):
    """ Execute locate switch
        Args:
            device ('obj'): Device object
            switch_number ('int'): Switch number
            seconds ('str'): Time in seconds
            switch_type ('str'): Switch type(active/standby)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if switch_number:
        cmd = f"locate-switch {switch_number} {seconds}"
    elif switch_type:
        cmd = f"locate-switch {switch_type} {seconds}"
    else:
        cmd = f"locate-switch {seconds}"
    
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute locate switch on {device.name}. Error:\n{e}"
        )