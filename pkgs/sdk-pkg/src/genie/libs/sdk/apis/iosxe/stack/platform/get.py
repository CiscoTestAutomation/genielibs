from genie.libs.sdk.apis.iosxe.platform.get import get_platform_default_dir as generic_default_dir
import logging

def get_platform_default_dir(device, output=None, all_rp=False):
    """Get the default directory of this device

        Args:
            device (`obj`): Device object
            output (`str`): Output of `dir` command
            all_rp(`bool`): Flag to get default dir for all the members
        Returns: 
            (list or str): str if not all_rp is set to True otherwise list
           
    """
    if all_rp:
        switch_info = device.parse('show switch')
        switch_ids = switch_info.get('switch', {}).get('stack', {}).keys()
        if switch_ids:
            default_dir = [f'flash-{switch_id}:' for switch_id in switch_ids]
        else:
            # Get files for standalone device
            default_dir = generic_default_dir(device, output=output)
            default_dir = [default_dir]
        return default_dir
    else:
        return  generic_default_dir(device, output=output)


