# Genie
from genie.libs.sdk.apis.iosxe.ie3k.platform.execute import (
    touch_file as ie3k_touch_file,
)


def touch_file(device, directory, file_name):
    """
    Create an empty file at the specified path on the device using the 'touch' command in
    bash console of device.

    IE9k is similar to IE3k, hence reusing IE3k's implementation.

    Args:
        device (obj): Device object
        directory (str): The directory where the file will be created (e.g., 'bootflash:/')
        file_name (str): The name of the file to be created on the device (e.g., 'testfile.txt')

    Returns:
        None

    Raises:
        SubCommandFailure: If the command execution fails
    """
    ie3k_touch_file(device, directory, file_name)
