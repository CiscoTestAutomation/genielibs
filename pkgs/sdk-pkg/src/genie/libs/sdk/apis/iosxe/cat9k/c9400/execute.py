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

def execute_install_one_shot(device, file_path=None, prompt=True, issu=False,
                             negative_test=False, timeout=900, connect_timeout=10, xfsu=False, reloadfast=False, force=False):
    """
    Performs install one shot on the device
    Args:
        device ('obj'): Device object.
        file_path ('str, optional'): Path of the image. Default is None.
        prompt ('bool, optional'): True sets the command to ask for a prompt and
                                   False sets the prompt level to none. Default is True.
        issu ('bool, optional'): Force the operation to use ISSU technique. Default is False.
        negative_test ('bool, optional'): Flag for install add pass/Fail cases. Default is False.
        timeout ('int, optional'): Timeout value in seconds. Default is 900.
        connect_timeout ('int, optional'): Time to wait before sending the prompt. Default is 10.
        xfsu ('bool, optional'): Force the operation to use xfsu. Default is False.
        reloadfast ('bool, optional'): Force the operation to use reloadfast. Default is False.
        force('bool, optional'):  Default is False.
    Returns:
        True if install one shot is successful
        False if install one shot is not successful
    Raises:
        Exception
    """

    def slow_sendline(spawn):
        time.sleep(connect_timeout)
        spawn.sendline('')

    dialog = Dialog ([
        Statement(pattern = r".*\[y/n\]\s*$",
                  action = "sendline(y)",
                  args = None,
                  loop_continue = True,
                  continue_timer = False),
        Statement(pattern = r".*you may save configuration and re-enter the command\. \[y/n/q\]",
                  action = "sendline(y)",
                  args = None,
                  loop_continue = True,
                  continue_timer = False),
        Statement(pattern = r".*Press RETURN to get started.*",
                  action = slow_sendline,
                  args = None,
                  loop_continue = False,
                  continue_timer = False),
        Statement(pattern = r".*SUCCESS\: install_add_activate_commit.*",
                  action = None,
                  args = None,
                  loop_continue = False,
                  continue_timer = False),
        Statement(pattern = r".*FAILED\: install_add_activate_commit.*",
                  action = None,
                  args = None,
                  loop_continue = False,
                  continue_timer = False),
        ])

    log.info(f"Perform install one shot {device.name}")

    cmd = f"install add file {file_path} activate"
    if issu:
        cmd += f" issu"

    if xfsu:
        cmd += f" xfsu"

    if reloadfast:
        cmd += f" reloadfast"

    cmd += " commit"

    if force:
        cmd += f" force"

    if not prompt:
        cmd += " prompt-level none"

    output = ""
    try:
        device.api.execute_write_memory()
        output = device.execute(cmd, reply=dialog, timeout=timeout)
    except Exception as e:
        log.error(f"Error while executing {cmd} on {device.name}: {e}")

    pattern = 'SUCCESS' if negative_test else 'FAILED'
    result = 'fail' if pattern in str(output) else 'successful'
    log.info(f"install one shot operation {result} on {device.name}")
    return (output if result == 'successful' else False)

def execute_diagnostic_start_module_port(device, module_number, test_id, port_num):
    """ execute diagnostic start module test
        Args:
            device ('obj'): Device object
            module_number ('int'): Module number on which diagnostic has to be performed 
            test_id ('str'): Test ID list (e.g. 1,3-6) or Test Name or minimal or complete
            port_num ('str'): word (e.g. 1-8 or all)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"diagnostic start module {module_number} test {test_id} port {port_num}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute diagnostic start module {module_number} test {test_id} port {port_num} on device. Error:\n{e}")
