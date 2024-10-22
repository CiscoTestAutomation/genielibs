"""Common verify functions for platform"""

# Python
import re
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)

def verify_boot_variable(device, boot_images, output=None):
    ''' Verifies given boot_images are set to the next-reload BOOT vars
        Args:
            device ('obj'): Device object
            boot_images ('str'): System images
    '''

    if boot_images == device.api.get_boot_variables(boot_var='next', output=output):
        log.info(f"Given boot images '{boot_images}' are set to 'BOOT' variable")                 
        return True
    else:
        log.info(f"Given boot images '{boot_images}' are not set to 'BOOT' variable")                 
        return False
 