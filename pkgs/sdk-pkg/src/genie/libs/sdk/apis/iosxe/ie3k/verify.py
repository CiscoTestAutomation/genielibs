# Python
import re

# Genie
from genie.libs.sdk.apis.verify import verify_current_image as generic_verify_current_image

# Unicon
from unicon.core.errors import SubCommandFailure


def verify_current_image(device, images, delimiter_regex=None, ignore_flash=True, **kwargs):
    '''Verify current images on the device
        Args:
            device (`obj`): Device object
            images (`list`): List of images expected on the device
            delimiter_regex (`regex string`): Regex of delimeters, default ':|\\/'
            ignore_flash (`bool`): Ignore flash directory names. Default: True
        Returns:
            None
    '''
    return generic_verify_current_image(
        device, images, delimiter_regex=delimiter_regex, ignore_flash=ignore_flash, **kwargs)


def verify_ignore_startup_config(device):
    """ To verify ignore startup config
        Args:
            device (`obj`): Device object
        Returns:
            True or False
        Raises:
            SubCommandFailure : Failed to verify ignore startup config on the device
            ValueError : Failed to find the config register value or the value
            is invalid
    """
    cmd = 'show romvar'
    
    try:
        output = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not verify the ignore startup config on {device.name}. Error:\n{e}"
        )

    match = re.search(r"ConfigReg\s*=\s*(?P<confreg>\w+)", output)
    if not match:
        raise ValueError(
            f"Could not find config register value in the output of '{cmd}' "
            f"on {device.name}"
        )
    config_reg = match.group("confreg")

    try:
        config_reg = int(config_reg, 16)
    except ValueError as e:
        raise ValueError(
            f"Could not convert config register value '{config_reg}' to a "
            f"hexadecimal integer. Error:\n{e}"
        )
    return config_reg & 0x40 != 0
