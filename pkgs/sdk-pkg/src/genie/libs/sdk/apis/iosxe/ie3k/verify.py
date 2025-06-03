
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
    """
    cmd = 'show romvar'
    
    try:
        output = device.parse(cmd)
        if output.get('rommon_variables', {}).get('switch_ignore_startup_config', 0) != 0:
            return False
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not verify the ignore startup config on {device.name}. Error:\n{e}")

    return True
