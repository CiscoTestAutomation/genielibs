""" Configure type APIs for IOSXR """

from unicon.core.errors import SubCommandFailure

def restore_running_config(device, path, file, timeout=60):
    """ Restore config from local file

        Args:
            device (`obj`): Device object
            path (`str`): directory
            file (`str`): file name
            timeout (`int`): Timeout for applying config
        Returns:
            None
    """
    try:
        device.execute(
            "copy {path}{file} running-config replace".format(path=path, file=file),
            timeout=timeout
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not replace saved configuration on "
            "device {device}\nError: {e}".format(device=device.name, e=str(e))
        )