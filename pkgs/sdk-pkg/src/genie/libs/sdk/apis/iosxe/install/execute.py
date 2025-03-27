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

def execute_install_remove_version(device, version=None, timeout=60, connect_timeout = 10):
    """
    Performs install remove for the version provided on the device
    Args:
        device ('obj'): Device object
        version ('str, optional'): Base Version to remove
        timeout ('int, optional'): Timeout value
        connect_timeout ('int, optional'): Time to wait before sending the promt
                                            (when pattern "SUCCESS: install_remove"
                                             matches)
    Returns:
        True if install remove is successful
        False if install remove is not successful
    Raises:
        SubCommandFailure
    """

    log.info(f"Performing install remove for version {version} on {device.name}")

    def slow_sendline(spawn):
            time.sleep(connect_timeout)
            spawn.sendline('')

    dialog = Dialog([
        Statement(pattern=r".*\[y/n\]",
                  action="sendline(y)",
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*Nothing to clean\.",
                  action=None,
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r"%s#" % device.name,
                  action=None,
                  args=None,
                  loop_continue=False,
                  continue_timer=False),
        Statement(pattern=r".*SUCCESS\: install_remove.*",
                  action=slow_sendline,
                  args=None,
                  loop_continue=False,
                  continue_timer=False),
    ])
    
    if version:
        cmd = f"install remove version {version}"

        try:
            output = device.execute(cmd, reply=dialog, timeout=timeout)
        except Exception as e:
            log.error(f"Error while executing {cmd} on {device.name}: {e}")
            return False

        match = re.search(r"FAILED: install_remove.*", output)
        result = 'failed' if match else 'successful'
        log.info(f"install remove version {result} on {device.name}")
        return True if not match else match

    
def execute_install_activate(device, abort_timer=None, prompt=True, issu=False,
                     smu=False, file_name=None, timeout=900, connect_timeout=10):
    """
        Performs install activate with auto abort timer on the device
        Args:
            device ('obj'): Device object
            abort_timer ('str, optional'): abort timer value
            prompt ('bool, optional'): True sets the command to ask for prompt and
                                       False sets the prompt level to none
            issu ('bool, optional'): Force the operation to use issu technique
            smu ('bool, optional'): Force the operation to use smu technique
            file_name ('str, optional'): Path of the image file for smu operation
            timeout ('int, optional'): Timeout value
            connect_timeout ('int, optional'): Time to wait before sending the prompt
                                               (when pattern "Press RETURN to get 
                                                started" matches)
        Returns:
            True if install activate is successful
            False if install activate is not successful
        Raises:
            SubCommandFailure
    """

    def slow_sendline(spawn):
        time.sleep(connect_timeout)
        spawn.sendline('')

    dialog = Dialog([
        Statement(pattern=r".*\[y/n\]",
                  action="sendline(y)",
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*Please confirm you have changed boot config to .*\/packages\.conf \[y/n\]",
                  action="sendline(y)",
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*you may save configuration and re-enter the command\. \[y/n/q\]",
                  action="sendline(y)",
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r"%s.*# " % device.name,
                  action=None,
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*Press RETURN to get started.*",
                  action=slow_sendline,
                  args=None,
                  loop_continue=False,
                  continue_timer=False),
        Statement(pattern = r".*SUCCESS: install_activate.*",
                  action = None,
                  args = None,
                  loop_continue = False, 
                  continue_timer = False),
    ])

    cmd = "install activate "

    # no smu, no issu, abort_timer and prompt none
    if not smu and not issu and abort_timer and not prompt:
        cmd +=f" auto-abort-timer {abort_timer} prompt-level none"

    # smu, no issu, abort_timer, prompt none
    elif smu and not issu and abort_timer and not prompt:
        cmd += f" file {file_name} auto-abort-timer {abort_timer} prompt-level none"
    
    # smu, no issu, no abort_timer, prompt none
    elif smu and not issu and not abort_timer and not prompt:
        cmd += f" file {file_name} prompt-level none"

    # smu, no issu, abort_timer, with prompt 
    elif smu and not issu and abort_timer:
        cmd += f" file {file_name} auto-abort-timer {abort_timer}"

    # smu, no issu, abort_timer, with prompt
    elif smu and not issu and not abort_timer:
        cmd += f" file {file_name}"

    # smu, issu,  abort_timer, with prompt
    elif smu and issu and abort_timer:
        cmd += f" file {file_name} issu auto-abort-timer {abort_timer}"

    # smu, issu, no abort_timer, with prompt
    elif smu and issu and not abort_timer:
        cmd += f" file {file_name} issu"

    # no smu, no issu, and prompt none
    elif not smu and not issu and abort_timer:
        cmd += f" auto-abort-timer {abort_timer}"

    # no smu, issu, abort_timer
    elif issu and not smu and abort_timer:
        cmd += f" issu auto-abort-timer {abort_timer}"

    # no smu, issu, not abort_timer
    elif issu and not smu and not abort_timer:
        cmd += " issu"


    log.info(f"Performing {cmd} on device {device.name}")
    try:
        device.api.execute_write_memory()
        output = device.execute(cmd, reply=dialog, timeout=timeout)
        log.info(f"{cmd} is successful on device {device.name}")
    except Exception as e:
        log.error(f"Error while executing {cmd} on {device.name}: {e}")
        return False

    match = re.search(r".*SUCCESS: install_activate.*", output)
    result = 'successful' if match else 'failed'
    log.info(f"install activate operation is {result} on {device.name}")
    return output if match else match


def execute_install_remove(device, file_path=None, timeout=60, connect_timeout=10):
    """
    Performs install remove on the device
    Args:
        device ('obj'): Device object
        file_path ('str, optional'): Path of the file on device to remove
        timeout ('int, optional'): Timeout value
        connect_timeout ('int, optional'): Time to wait before sending the promt
                                            (when pattern "SUCCESS: install_remove"
                                             matches)
    Returns:
        True if install remove is successful
        False if install remove is not successful
    Raises:
        SubCommandFailure
    """
    log.info("Performing install remove on {hostname} to remove the "
             "unused files ".format(hostname=device.name))

    def slow_sendline(spawn):
        time.sleep(connect_timeout)
        spawn.sendline('')

    dialog = Dialog([
        Statement(pattern=r".*\[y/n\]",
                  action="sendline(y)",
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*Nothing to clean\.",
                  action=None,
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r"%s#" % device.name,
                  action=None,
                  args=None,
                  loop_continue=False,
                  continue_timer=False),
        Statement(pattern=r".*SUCCESS\: install_remove.*",
                  action=slow_sendline,
                  args=None,
                  loop_continue=False,
                  continue_timer=False),
    ])

    cmd = 'install remove'

    if file_path:
        cmd += f' file {file_path}'
    else:
        cmd += ' inactive'

    try:
        device.api.execute_write_memory()
        output = device.execute(cmd, reply=dialog, timeout=timeout)
    except Exception as e:
        log.error(f"Error while executing {cmd} on {device.name}: {e}")
        return False

    match = re.search(r"FAILED:*", output)
    result = 'failed' if match else 'successful'
    log.info(f"install remove inactive is {result} on {device.name}")
    return True if not match else match


def execute_install_one_shot(device, file_path=None, prompt=True, issu=False,
                             negative_test=False, timeout=900, connect_timeout=10, xfsu=False, reloadfast=False, post_reload_wait_time=None, error_pattern=None):
    """
    Performs install one shot on the device
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
        reloadfast('bool, optional'):  Force the operation to use reloadfast.
        post_reload_wait_time ('int, optional'): Time to wait after reload
        error_pattern ('list, optional'): List of error patterns to check in the output
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

    if not prompt:
        cmd += " prompt-level none"

    output = ""
    try:
        device.api.execute_write_memory()
        _, output = device.reload(cmd, reply=dialog, timeout=timeout, return_output=True, prompt_recovery=True, post_reload_wait_time=post_reload_wait_time, error_pattern=error_pattern)
    except Exception as e:
        log.error(f"Error while executing {cmd} on {device.name}: {e}")

    pattern = 'SUCCESS' if negative_test else 'FAILED'
    result = 'fail' if pattern in output else 'successful'
    log.info(f"install one shot operation {result} on {device.name}")
    return (output if result == 'successful' else False)


def execute_install_add(device, file_path=None, prompt=True, negative_test=False,
                timeout=900, connect_timeout=10):
    """
    Performs install add on the device
    Args:
        device ('obj'): Device object
        file_path ('str, optional'): Path of the image
        prompt ('bool, optional'): True sets the command to ask for prompt and
                                   False sets the prompt level to none
        negative_test ('str, optional'): Flag for install add pass/Fail cases
        timeout ('int, optional'): Timeout value
        connect_timeout ('int, optional'): Time to wait before sending the prompt
                                            (when pattern "Press RETURN to get 
                                            started" matches)
    Returns:
        True if install one shot is successful
        False if install one shot is not successful
    Raises:
        SubCommandFailure
    """
    def slow_sendline(spawn):
        time.sleep(connect_timeout)
        spawn.sendline('')

    if negative_test == False:
        dialog = Dialog ([
            Statement(pattern = r".*Finished initial file syncing",
                      action = None,
                      args = None,
                      loop_continue = True,
                      continue_timer = False),
            Statement(pattern = r".*SUCCESS\: install_add",
                      action = None,
                      args = None,
                      loop_continue = True,
                      continue_timer = False),
            Statement(pattern = r".*FAILED\: install_add",
                      action = None,
                      args = None,
                      loop_continue = False,
                      continue_timer = False),
            Statement(pattern = r"%s.*#"%device.name,
                      action = None,
                      args = None,
                      loop_continue = False,
                      continue_timer = False),
            Statement(pattern = r"Press RETURN to get started!",
                      action = slow_sendline,
                      args = None,
                      loop_continue = True,
                      continue_timer = False),
            ])
    else:
        dialog = Dialog ([
            Statement(pattern = r".*Finished initial file syncing",
                      action = None,
                      args = None,
                      loop_continue = True,
                      continue_timer = False),
            Statement(pattern = r".*SUCCESS\: install_add",
                      action = None,
                      args = None,
                      loop_continue = True,
                      continue_timer = False),
            Statement(pattern = r".*Copying.*",
                      action = slow_sendline,
                      args = None,
                      loop_continue = False,
                      continue_timer = False),
            Statement(pattern = r".*FAILED\: install_add",
                      action = None,
                      args = None,
                      loop_continue = True,
                      continue_timer = False),
            Statement(pattern = r"Press RETURN to get started!",
                      action = slow_sendline,
                      args = None,
                      loop_continue = True,
                      continue_timer = False),
            ])

    log.info(f"Perform install add on device {device.name}")

    cmd = f"install add file {file_path}"
    if not prompt:
        cmd += " prompt-level none"

    try:
        device.api.execute_write_memory()
        output = device.execute(cmd, reply=dialog, timeout=timeout)
    except Exception as e:
        log.error(f"Error while executing {cmd} on {device.name}: {e}")
        return False

    pattern = 'SUCCESS' if negative_test else 'FAILED'
    result = 'fail' if pattern in output else 'successful'
    log.info(f"Install add {result} on {device.name}")
    return( output if result == 'successful' else False)



def execute_install_commit(device, timeout=900, connect_timeout=10):
    """
    Performs install commit on the device
    Args:
        device ('obj'): Device object
        timeout ('int, optional'): Timeout value
        connect_timeout ('int, optional'): Time to wait before sending the prompt
                                            (when pattern SUCCESS: install_commit"
                                             matches)
    Returns:
        True if install commit is successful
        False if install commit is not successful
    Raises:
        SubCommandFailure
    """

    log.info("Executing Install Commit on {0}" .format(device.name))

    def slow_sendline(spawn):
        time.sleep(connect_timeout)
        spawn.sendline('')

    dialog = Dialog ([
        Statement(pattern = r".*SUCCESS\: install_commit",
                  action = slow_sendline,
                  args = None,
                  loop_continue = True,
                  continue_timer = False),
        Statement(pattern=r"%s#" % device.name,
                  action = None,
                  args = None,
                  loop_continue = False,
                  continue_timer = False),
        ])

    try:
        device.api.execute_write_memory()
        output = device.execute("install commit", reply=dialog, timeout=timeout)
    except Exception as e:
        log.error(f"Error while executing install commit on {device.name}: {e}")
        return False

    match = re.search(r"SUCCESS\: install_commit", output)

    result = 'successful' if match else 'failed'
    log.info(f"install commit operation {result} on {device.name}")
    return output if match else match


def execute_create_rollback_label(device, rollback_id, rollback_label):
    """
    Creates rollback label for rollback id
    Args:
        device ('obj'): Device object
        rollback_id ('str'): rollback id for which label has to be created .
        rollback_label ('str'): rollback label
    Returns:
        True if rollback label is successfully created
        False if failed to creted rollback label
    Raises:
        SubCommandFailure
    """

    log.info(f"Creating rollback label for rollback id {rollback_id}")

    try:
        device.execute(f"install label {rollback_id} label-name {rollback_label}")
    except Exception as e:
        log.error(f"Failed to create label for rollback id {rollback_id}: {e}")
        return False
    
    log.info(f"Created label for rollback id {rollback_id}")
    return True


def execute_create_rollback_description(device, rollback_id, rollback_description):
    """
    Creates rollback description for rollback id
    Args:
        device ('obj'): Device object
        rollback_id ('str'): rollback id for which label has to be created .
        rollback_description ('str'): rollback description
    Returns:
        True if rollback description is successfully created
        False if failed to creted rollback label
    Raises:
        SubCommandFailure
    """

    log.info(f"Creating rollback description for rollback id {rollback_id}")

    try:
        device.execute(f"install label {rollback_id} description \"{rollback_description}\"")
    except Exception as e:
        log.error(f"Failed to create description for rollback id {rollback_id}: {e}")
        return False
    
    log.info(f"Created description for rollback id {rollback_id}")
    return True


def execute_clear_install_state(device, timeout=900, connect_timeout=10):
    """
    Performs clear install state on device
    Args:
        device ('obj'): Device object
        timeout ('int, optional'): Timeout value
        connect_timeout ('int, optional'): Time to wait before sending the prompt
                                            (when pattern "Press RETURN to get 
                                            started" matches)
    Returns:
        True if clear install state is successfull
        False if clear install state is not successfull
    Raises:
        SubCommandFailure
    """
    def slow_sendline(spawn):
        time.sleep(connect_timeout)
        spawn.sendline('')

    dialog = Dialog ([
        Statement(pattern = r".*\[y/n\]",
                  action = "sendline(y)",
                  args = None,
                  loop_continue = True,
                  continue_timer = False),
        Statement(pattern = r".*Press RETURN to get started.*",
                  action = slow_sendline,
                  args = None,
                  loop_continue = False,
                  continue_timer = False),
        Statement(pattern=r"%s#" % device.name,
                  action = None,
                  args = None,
                  loop_continue = False,
                  continue_timer = False),
        ])

    log.info(f"Performing clear install state on {device.name}")
    cmd = "clear install state "
    try:
        device.api.execute_write_memory()
        device.execute(cmd, reply=dialog, prompt_recovery=True, error_pattern=[],
                       timeout=timeout)
    except Exception as e:
        log.error(f"Error while executing clear install state on device {device.name}: {e}")
        return False

    return True


def execute_install_auto_abort_timer_stop(device, timeout=120):
    """
    Performs install auto-abort-timer stop on device
    Args:
        device ('obj'): Device object
        timeout ('int, optional'): Timeout value
    Returns:
        True if install auto-abort-timer stop is successful
        False if install auto-abort-timer stop is not successful
    Raises:
        SubCommandFailure
    """

    try:
        output = device.execute("install auto-abort-timer stop", timeout=timeout)
    except Exception as e:
        log.error("Error thrown while executing is {0}".format(e))

    match = re.search('.*SUCCESS.*', output)
    result = 'successful' if match else 'failed'
    log.info(f"ISSU auto-abort timer stop command execution is {result} on {device.name}")
    return(True if result == 'successful' else False )


def execute_clear_install_label(device, timeout=900, connect_timeout=10, id = None ,label_name = None):
    """
    Performs clear install state on device
    Args:
        device ('obj'): Device object
        timeout ('int, optional'): Timeout value
        id = ('str optional'): rollback_label id
        label_name = ('str optional'): rollback_label name
        connect_timeout ('int, optional'): Time to wait before sending the prompt
                                            (when pattern "Press RETURN to get 
                                            started" matches)
    Returns:
        True if clear install state is successfull
        False if clear install state is not successfull
    Raises:
        SubCommandFailure
    """
    def slow_sendline(spawn):
        time.sleep(connect_timeout)
        spawn.sendline('')

    dialog = Dialog ([
        Statement(pattern = r".*SUCCESS\: clear_install_label",
                  action = slow_sendline,
                  args = None,
                  loop_continue = True,
                  continue_timer = False),
        Statement(pattern=r"%s#" % device.name,
                  action = None,
                  args = None,
                  loop_continue = False,
                  continue_timer = False),
        ])

    log.info(f"Performing clear install label on {device.name}")
    cmd = cmd = f"clear install label "
    if id:
        cmd += f" id {id}"
    elif label_name:
        cmd += f" label-name {label_name}"
    else:
        log.info("No proper values provided")
        return False
    try:
        device.execute("wr mem")
        device.execute(cmd, reply=dialog, timeout=timeout)

    except Exception as e:
        log.error(f"Error while executing clear install label on device {device.name}: {e}")
        return False

    return True


def execute_install_abort(device, issu=False, timeout=900, connect_timeout=10):
    """
        Performs install abort on the device
        Args:
            device ('obj'): Device object
            issu ('bool, optional'): True Forces the operation to use issu technique
            timeout ('int, optional'): Timeout value
            connect_timeout ('int, optional'): Time to wait before sending the promt
                                               (when pattern "Press RETURN to get 
                                                started" matches)
        Returns:
            True if install abort is successful
            False if install abort is not successful
        Raises:
            SubCommandFailure
    """
    log.info("Executing Install abort on {0}".format(device.name))

    def slow_sendline(spawn):
        time.sleep(connect_timeout)
        spawn.sendline('')

    dialog = Dialog([
        Statement(pattern=r".*\[y/n\]",
                  action="sendline(y)",
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(
            pattern=r".*you may save configuration and re-enter the command\. \[y/n/q\]",
            action="sendline(y)",
            args=None,
            loop_continue=True,
            continue_timer=False),
        Statement(pattern=r"%s.*# " % device.name,
                  action=None,
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*Press RETURN to get started.*",
                  action=slow_sendline,
                  args=None,
                  loop_continue=False,
                  continue_timer=False),
    ])

    cmd = "install abort"
    if issu:
        cmd += " issu"

    try:
        device.api.execute_write_memory()
        output = device.execute(cmd, reply=dialog, timeout=timeout)
        log.info("Successfully completed install abort on {}".format(device.name))
    except Exception as e:
        log.error(f"Failed to execute install abort on device {device.name}: {e}")
        return False
    
    match = re.search(r"^FAILED\:\s+install_abort.*", output)
    result = 'failed' if match else 'successful'
    log.info(f"install abort operation {result} on {device.name}")
    return output if not match else match


def execute_install_deactivate(device, abort_timer=None, prompt=True, issu=False,
                      file_name=None, timeout=900, connect_timeout=10):
    """
        Performs install deactivate with auto abort timer on the device
        Args:
            device ('obj'): Device object
            abort_timer ('str, optional'): abort timer value
            prompt ('bool, optional'): True sets the command to ask for prompt and
                                       False sets the prompt level to none
            issu ('bool, optional'): Force the operation to use issu technique
            file_name ('str, optional'): Path of the image file for smu operation
            timeout ('int, optional'): Timeout value
            connect_timeout ('int, optional'): Time to wait before sending the prompt
                                               (when pattern "Press RETURN to get 
                                                started" matches)
        Returns:
            True if install activate is successful
            False if install activate is not successful
        Raises:
            SubCommandFailure
    """

    def slow_sendline(spawn):
        time.sleep(connect_timeout)
        spawn.sendline('')

    dialog = Dialog ([

        Statement(pattern = r".*\[y/n\]",
                  action = "sendline(y)",
                  args = None,
                  loop_continue = True,
                  continue_timer = False),

        Statement(pattern = r".*Please confirm you have changed boot config to .*\/packages\.conf \[y/n\]",
                  action = "sendline(y)",
                  args = None,
                  loop_continue = True,
                  continue_timer = False),

        Statement(pattern = r".*you may save configuration and re-enter the command\. \[y/n/q\]",
                  action = "sendline(y)",
                  args = None,
                  loop_continue = True,
                  continue_timer = False),

        Statement(pattern = r".*This operation may require a reload of the system. Do you want to proceed\?\. \[y/n\]",
                  action = "sendline(y)",
                  args = None,
                  loop_continue = True,
                  continue_timer = False),
        Statement(pattern = r".*Press RETURN to get started.*",
                  action = slow_sendline,
                  args = None,
                  loop_continue = False,
                  continue_timer = False),

        Statement(pattern = r".*SUCCESS:*install_deactivate.*",
                  action = slow_sendline,
                  args = None,
                  loop_continue = False,
                  continue_timer = False),

        ])

    cmd = f"install deactivate file {file_name} "
    if not issu and abort_timer and not prompt:
        cmd += f" auto-abort-timer {abort_timer} prompt-level none"
    elif not issu and abort_timer:
        cmd += f" auto-abort-timer {abort_timer}"
    elif issu and abort_timer:
        cmd += f" issu auto-abort-timer {abort_timer}"
    elif issu and not abort_timer:
        cmd += f" issu"
    elif not issu and abort_timer:
        cmd += f" auto-abort-timer {abort_timer}"
    elif not issu and not abort_timer and not prompt:
        cmd += f" prompt-level none"

    log.info(f"Performing {cmd} on device {device.name}")
    try:
        device.api.execute_write_memory()
        output = device.execute(cmd, reply=dialog, timeout=timeout, error_pattern=[])
        log.info(f"{cmd} is successful on device {device.name}")
    except Exception as e:
        log.error(f"Error while executing {cmd} on {device.name}: {e}")
        return False

    match = re.search(r"^FAILED:*install_deactivate.*", output)
    result = 'failed' if match else 'successful'
    log.info(f"install deactivate operation {result} on {device.name}")
    return output if not match else match


def execute_install_rollback(device, rollback_point=None, rollback_id=None, issu=False,
                     rollback_label=None, timeout=900, connect_timeout=10, prompt=True):
    """
    Performs rollback on the device
    Args:
         device ('obj'): Device object
         rollback_point ('str, optional'): Last committed/base installation point
         rollback_id ('str, optional'): specific install point id
         rollback_label ('str, optional'): specific install point label
         issu ('bool, optional'): Force the operation to use issu technique
         timeout ('int, optional'): Timeout value
         prompt ('bool, optional'): True sets the command to ask for prompt and
                        False sets the prompt level to none
         connect_timeout ('int, optional'): Time to wait before sending the promt
                                            (when pattern "Press RETURN to get 
                                            started" matches)
    Returns:
            True if rollback is successfull
            False if rollback is not successfull or rollback point not provided
    Raises:
        SubCommandFailure
    """
    def slow_sendline(spawn):
        time.sleep(connect_timeout)
        spawn.sendline('')

    dialog = Dialog([
        Statement(pattern=r".*\[y/n\]",
                  action="sendline(y)",
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*Please confirm you have changed boot config to .*\/packages\.conf \[y/n\]",
                  action="sendline(y)",
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*you may save configuration and re-enter "
                          r"the command\. \[y/n/q\]",
                  action="sendline(y)",
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r"%s.*# " % device.name,
                  action=None,
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*Press RETURN to get started.*",
                  action=slow_sendline,
                  args=None,
                  loop_continue=False,
                  continue_timer=False),
                 ])

    log.info("Executing Install rollback on {0}" .format(device.name))
    log.info("rollback label is : {rollback_label}" .format(
                 rollback_label=rollback_label))

    cmd = "install rollback to "

    if rollback_point == "committed":
        cmd += f"{rollback_point}"
    elif rollback_point == "base":
        cmd += f"{rollback_point}"
    elif rollback_id:
        cmd += f"id {rollback_id}"
    elif rollback_label:
        cmd += f"label {rollback_label}"
    else:
        log.info("rollback point not provided")
        return False

    if issu:
        cmd += " issu"
    if not prompt:
        cmd += " prompt-level none"

    try:
        device.execute("wr mem")
        output = device.execute(cmd, reply=dialog, timeout=timeout)
        log.info(f"Successfully completed install rollback on {device.name}")
    except Exception as e:
        log.error(f"Error while executing {cmd} on {device.name}: {e}")
        return False

    match = re.search(r"^FAILED\:\s+install_rollback.*", output)
    result = 'failed' if match else 'successful'
    log.info(f"install rollback operation got {result} on {device.name}")
    return output if not match else match

def execute_install_package_reload_fast(device, image_dir, image, reload_fast=True, timeout=1600, connect_timeout=300):
    """
    Install package reloadfast
    Args:
        device ("obj"): Device object
        image_dir ("str"): Directory where the image is located
        image ("str"): Image filename
        reload_fast ("bool"): Whether to use reloadfast. Default is True.
        timeout ("int", optional): Timeout value. Default is 1600 seconds.
        connect_timeout ("int", optional): Time to wait before sending the prompt
                                           (when pattern "Press RETURN to get started" matches)
    Returns:
        True if install succeeded else False
    Raises:
        SubCommandFailure
    """

    def slow_sendline(spawn):
        time.sleep(connect_timeout)
        spawn.sendline('')

    dialog = Dialog([
        Statement(pattern=r".*\[y/n\]",
                  action="sendline(y)",
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*Please confirm you have changed boot config to .*\/packages\.conf \[y/n\]",
                  action="sendline(y)",
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*you may save configuration and re-enter the command\. \[y/n/q\]",
                  action="sendline(y)",
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r"%s.*# " % device.name,
                  action=None,
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*Press RETURN to get started.*",
                  action=slow_sendline,
                  args=None,
                  loop_continue=False,
                  continue_timer=False),
        Statement(pattern = r".*SUCCESS: install_add_activate_commit.*",
                  action = None,
                  args = None,
                  loop_continue = False,
                  continue_timer = False),
    ])

    cmd = "install add file {image_dir}{image} activate".format(image_dir=image_dir, image=image)
    if reload_fast:
        cmd += " reloadfast"

    cmd += " commit"

    log.info(f"Perform install reloadfast {device.name}")

    try:
        device.api.execute_write_memory()
        output = device.execute(cmd, reply=dialog, timeout=timeout)
        log.info(f"{cmd} is successful on {device.name}")
    except Exception as e:
        log.error(f"Error while executing {cmd} on {device.name}: {e}")
        return False

    match = re.search(r".*SUCCESS: install_add_activate_commit.*", output)
    result = 'successful' if match else 'failed'
    log.info(f"install reloadfast {result} on {device.name}")
    return output if match else match

