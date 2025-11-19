from genie.libs.sdk.apis.iosxe.platform.get import get_platform_default_dir as generic_default_dir
import logging

def get_platform_default_dir(device, output=None, all_rp=False):
    """Get the default directory of this device

        Args:
            device (`obj`): Device object
            output (`str`): Output of `dir` command
            all_rp(`bool`): Flag to return for all the rp's
        Returns: 
            str or list: default directory or List of default directories if all_rp passed
           
    """
    default_dir = generic_default_dir(device, output=output)
    if all_rp:
       return [default_dir, 'stby-'+default_dir]
    return default_dir