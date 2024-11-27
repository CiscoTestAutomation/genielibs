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
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not verify the ignore startup config on {device.name}. Error:\n{e}")
    # first check the next config register if its not there check the current config register
    config_reg = output['version'].get('next_config_register') or output['version'].get('curr_config_register')

    if config_reg != '0x2102':
        return False

    return True
