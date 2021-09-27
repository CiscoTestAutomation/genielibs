"""common configure functions for authentication"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure


log = logging.getLogger(__name__)


def authentication_convert_to_new_style(device, force=None):
    """Common function to configure authentication convert-to new-style for both forced and without forced
    
        Args:
            device ('obj'): device to use
            force (`str`): Cli input to continue (default value is None)
            
        Returns:
            None
            
        Raises:
            SubCommandFailure: Failed to configure authentication convert-to new-style
            """
    
    log.debug("Configuring authentication convert-to new-style")
    if force:
        cmd = ["authentication convert-to new-style forced"]
    else:
        cmd = ["authentication display new-style"]

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure authentication convert-to new-style. Error:\n{error}".format(error=e
            ))
