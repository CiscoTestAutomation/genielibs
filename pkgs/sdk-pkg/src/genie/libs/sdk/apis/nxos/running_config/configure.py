""" Configure type APIs for NXOS """

from unicon.eal.dialogs import Dialog, Statement
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
    dialog = Dialog(
        [
            Statement(
                pattern=r".*\[(yes|no)\].*",
                action="sendline(y)",
                loop_continue=True,
                continue_timer=False,
            )
        ]
    )
    try:
        device.execute(
            "configure replace {path}{file}".format(path=path, file=file),
            reply=dialog,
            timeout=timeout
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not replace saved configuration on "
            "device {device}\nError: {e}".format(device=device.name, e=str(e))
        )