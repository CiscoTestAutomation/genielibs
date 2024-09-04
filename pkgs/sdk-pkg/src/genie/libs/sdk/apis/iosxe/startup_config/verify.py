import logging

# Unicon
from unicon.core.errors import SubCommandFailure

logger = logging.getLogger(__name__)

def verify_ignore_startup_config(device):
    """ To verify ignore startup config
        Args:
            device (`obj`): Device object
        Returns:
            True or False
        Raises:
            SubCommandFailure : Failed to verify ignore startup config on the device
    """
    cmd = 'show version'
    
    try:
        output = device.parse(cmd)
        if output['version']['next_config_register'] != '0x2102':
            return False
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not verify the ignore startup config on {device.name}. Error:\n{e}")

    return True