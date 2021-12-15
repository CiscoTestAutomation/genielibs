"""common iget  functions for authentication"""

# Python
import logging
import re

#Genie
#from genie.libs.parser.iosxe.show_authentication_sessions import AuthenticationDisplayConfigMode

# Unicon
from unicon.core.errors import SubCommandFailure


log = logging.getLogger(__name__)

def get_authentication_config_mode(device):
    """  Get current authentication config mode on device

        Args:
            device ('obj'): device to use

        Returns:
            config mode

        Raises:
            SubCommandFailure: Failed to configure authentication convert-to new-style
    """

    log.debug('Verify current authentication config mode on {device}'.format(device=device))

    try:
        config_mode = device.parse('authentication display config-mode')

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not get any output from cli command. Error:\n{error}".format(error=e
            ))
    
    return config_mode
