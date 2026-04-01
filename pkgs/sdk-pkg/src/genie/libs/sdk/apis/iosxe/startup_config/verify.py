# Python
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
            ValueError : Invalid config register value
    """
    cmd = 'show version'
    
    try:
        output = device.parse(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not verify the ignore startup config on {device.name}. Error:\n{e}")
    # first check the next config register if its not there check the current config register
    config_reg = output['version'].get('next_config_register') or output['version'].get('curr_config_register')

    try:
        config_reg = int(config_reg, 16)
    except ValueError as e:
        raise ValueError(
            f"Could not convert config register value '{config_reg}' to a "
            f"hexadecimal integer. Error:\n{e}"
        )
    return config_reg & 0x40 != 0
