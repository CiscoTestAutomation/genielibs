# Python
import logging
import re
import time

# Genie
from genie.utils.timeout import Timeout

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def execute_install_one_shot(
    device,
    file_path=None,
    prompt=True,
    issu=False,
    negative_test=False,
    timeout=900,
    connect_timeout=10,
    xfsu=False,
    reloadfast=False,
    post_reload_wait_time=None,
    error_pattern=None,
):
    """
    Performs install one shot on the c9500x device
    Args:
        device ('obj'): Device object
        file_path ('str, optional'): Path of the image
        prompt ('bool, optional'): True sets the command to ask for prompt and
                                   False sets the prompt level to none
        issu ('bool, optional'): Force the operation to use issu technique
        negative_test ('bool, optional'): Flag for install add pass/Fail cases
        timeout ('int, optional'): Timeout value
        connect_timeout ('int, optional'): Time to wait before sending the prompt
                                            (when pattern "Press RETURN to get
                                            started" matches))
        xfsu ('bool, optional'):  Force the operation to use xfsu.
        reloadfast('bool, optional'):  Force the operation to use reloadfast.
        post_reload_wait_time ('int, optional'): Time to wait after reload
        error_pattern ('list, optional'): List of error patterns to check in the output
    Returns:
        True if install one shot is successful
        False if install one shot is not successful
    Raises:
        Exception
    """

    dialog = Dialog(
        [
            Statement(
                pattern=r".*\[y/n\]\s*$",
                action="sendline(y)",
                args=None,
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r".*you may save configuration and re-enter the command\. \[y/n/q\]",
                action="sendline(y)",
                args=None,
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r".*SUCCESS\: install_add_activate_commit.*",
                action=None,
                args=None,
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r".*FAILED\: install_add_activate_commit.*",
                action=None,
                args=None,
                loop_continue=False,
                continue_timer=False,
            ),
        ]
    )

    log.debug(f"Perform install one shot {device.name}")

    cmd = f"install add file {file_path} activate"
    if issu:
        cmd += f" issu"

    if xfsu:
        cmd += f" xfsu"

    if reloadfast:
        cmd += f" reloadfast"

    cmd += " commit"

    if not prompt:
        cmd += " prompt-level none"

    output = ""
    try:
        device.api.execute_write_memory()
        _, output = device.reload(
            cmd,
            reply=dialog,
            timeout=timeout,
            return_output=True,
            prompt_recovery=True,
            post_reload_wait_time=post_reload_wait_time,
            error_pattern=error_pattern,
        )
    except Exception as e:
        log.error(f"Error while executing {cmd} on {device.name}: {e}")

    pattern = "SUCCESS" if negative_test else "FAILED"
    result = "failure" if pattern in output else "successful"
    log.debug(f"install one shot operation {result} on {device.name}")
    return output if result == "successful" else False
