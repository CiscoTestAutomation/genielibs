
from genie.libs.sdk.apis.iosxr.ncs5k.get import get_software_version as get_software_version_ncs540

def get_software_version(device):
    """ Gets the version of the current running image
        Args:
            device (`obj`): Device object
        Returns:
            Image or None
    """
    return get_software_version_ncs540(device)

