
from genie.libs.sdk.apis.verify import verify_current_image as generic_verify_current_image


def verify_current_image(device, images, delimiter_regex=None, ignore_flash=True, **kwargs):
    '''Verify current images on the device
        Args:
            device (`obj`): Device object
            images (`list`): List of images expected on the device
            delimiter_regex (`regex string`): Regex of delimeters, default ':|\/'
            ignore_flash (`bool`): Ignore flash directory names. Default: True
        Returns:
            None
    '''
    return generic_verify_current_image(
        device, images, delimiter_regex=delimiter_regex, ignore_flash=ignore_flash, **kwargs)
