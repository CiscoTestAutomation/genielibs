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