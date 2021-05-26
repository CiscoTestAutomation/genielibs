
import re


def get_firmware_version_from_image_name(device, image_name):
    """ Get the firmware version from the image name.

    Args:
        image_name (str): image filename

    Returns:
        string with image version
    """
    m = re.search(r'n9000-dk9\.(\d+\.\d+)\.(\w+)', image_name)
    if m:
        version_major_minor = m.group(1)
        version_patch = m.group(2)
        version = 'n9000-{}({})'.format(version_major_minor, version_patch)
        return version
