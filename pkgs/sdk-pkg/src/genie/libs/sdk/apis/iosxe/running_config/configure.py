"""Utility type functions that do not fit into another category"""

# Python
import logging

from genie.utils.timeout import Timeout

# Running-Config
from genie.libs.sdk.apis.iosxe.running_config.get import (
    get_running_config,
    get_running_config_section,
)

# unicon
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def save_running_config(device,
                        source="running-config",
                        destination="startup-config",
                        timeout=60):
    """Save config

    Args:
        device (`obj`): Device object
        source (`str`): source to copy from
        destination (`str`): destination to copy to
        timeout (`str`, optional): timeout (secs)
    Returns:
        None
    """
    try:
        device.copy(source=source, dest=destination, timeout=timeout)
    except SubCommandFailure:
        raise SubCommandFailure('Failed to save configuration from "{source}" '
                                "to {dest}".format(source=source,
                                                   dest=destination))


def copy_file_to_running_config(device, path, file, timeout=60):
    """Restore config from local file using copy function
    Args:
        device (`obj`): Device object
        path (`str`): directory
        file (`str`): file name
        timeout (`str`): timeout
    Returns:
        None
    """
    dialog = Dialog([
        Statement(
            pattern=r".*Destination filename.*",
            action="sendline()",
            loop_continue=True,
            continue_timer=False,
        )
    ])
    try:
        device.execute(
            "copy {path}{file} running-config".format(path=path, file=file),
            reply=dialog,
            timeout=timeout,
        )
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not copy saved configuration on "
                                "device {device}.\nError: {e}".format(
                                    device=device.name, e=str(e)))


def restore_running_config(device,
                           path,
                           file,
                           timeout=60,
                           delete_after=False,
                           max_time=300,
                           check_interval=30):
    """Restore config from local file

    Args:
        device (`obj`): Device object
        path (`str`): directory
        file (`str`): file name
        timeout (`int`): Timeout for applying config
        delete_after (`bool`): if True, delete the file after restoring
        max_time ('int', optional): maximum time to wait in seconds,
            default is 300
        check_interval ('int', optional): how often to check in seconds,
            default is 30
    Returns:
        boolean
    """
    dialog = Dialog([
        Statement(
            pattern=r".*\[(yes|no)\].*",
            action="sendline(y)",
            loop_continue=True,
            continue_timer=False,
        )
    ])

    tm = Timeout(max_time, check_interval)

    while tm.iterate():

        try:
            out = device.execute(
                "configure replace {path}{file}".format(path=path, file=file),
                reply=dialog,
                timeout=timeout,
                error_pattern=[],
            )
            if out and "Rollback Done" in out:
                if delete_after:
                    device.api.delete_files(locations=[path], filenames=[file])
                return True
        except Exception:
            raise Exception("Could not restore configuration.")

        tm.sleep()

    return False


def remove_running_config(device, remove_config):
    """Remove running configuration starting with passed keyword from device

    Args:
        device ('obj')        : Device object to modify configuration
        remove_config ('str') : Configuration to be removed from device

    Returns:
        None
    """

    config_list = get_running_config(device=device, keyword=remove_config)

    config_list = list(map(lambda conf: "no " + conf, config_list))

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to remove {config} configuration on device "
            "{device}".format(device=device.name, config=config_list)) from e


def remove_tacacs_server(device, remove_config=None, keyword="tacacs"):
    """Remove tacacs server configuration from device

    Args:
        device ('obj')        : Device object to modify configuration
        remove_config ('list') : Configuration to be removed from device
        keyword ('str') : keyword the configuration should start with

    Returns:
        None
    """
    config_list = []
    if not remove_config:
        remove_config = get_running_config_section(device=device,
                                                   keyword=keyword)

    for line in remove_config:
        line = line.strip()
        if line.startswith(keyword):
            config_list.append(line)

    unconfig_list = list(map(lambda conf: "no " + conf, config_list))

    try:
        device.configure(unconfig_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to remove {config} configuration on device "
            "{device}".format(device=device.name, config=config_list)) from e


def copy_config_from_tftp_to_media(device,
                                   host,
                                   config_file_with_path,
                                   file,
                                   timeout=30,
                                   vrf=None,
                                   media="bootflash"):
    """Copy configuration file from tftp location to media

    Args:
        device ('obj'): Device object to modify configuration
        host ('str'): tftp host ip address
        config_file_with_path ('str') : configuration file name along with tftp path
        file('str'): configuration file name
        timeout('int', Optional): timeout for configuration file load to device(Deafult is 30)
        vrf('str', Optional): vrf for tftp connectivity(Deafult is None)
        media('str', Optional): where to copy the file in device(Deafult is bootflash)

    Returns:
        True or False
    """
    dialog = Dialog([
        Statement(
            pattern=r".*Address or name of remote host.*",
            action=f"sendline({host})",
            loop_continue=True,
            continue_timer=False,
        ),
        Statement(
            pattern=r".*Source filename.*",
            action=f"sendline({config_file_with_path})",
            loop_continue=True,
            continue_timer=False,
        ),
        Statement(
            pattern=r".*Destination filename",
            action=f"sendline({file})",
            loop_continue=True,
            continue_timer=False,
        ),
        Statement(
            pattern=r".*Do you want to over write.*",
            action="sendline(yes)",
            loop_continue=True,
            continue_timer=False,
        ),
    ])
    error_patterns = [".*%Error opening.*"]

    log.debug("Copy configuration file from tftp to device")
    if vrf is None:
        command = f"copy tftp: {media}:"
    else:
        command = f"copy tftp: {media}: vrf {vrf}"
    try:
        out = device.execute(command,
                             reply=dialog,
                             error_pattern=error_patterns,
                             timeout=timeout)
        if "[OK -" in out and "bytes copied in" in out:
            return True
        else:
            return False
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "tftp copy did'nt happen for {device}. Error:\n{error}".format(
                device=device, error=e))


def configure_replace(device,
                      path,
                      file,
                      config_replace_options="",
                      timer=1,
                      timeout=60):
    """Restore config from local file
    Args:
        device ('obj'): Device object
        path ('str'): directory
        file ('str'): file name
        config_replace_options ('str'): configure replace command suboption
            ex:)
                force       Forcibly replace without prompting for user input
                ignorecase  Ignore case
                list        List the commands applied in each pass
                nolock      Do not acquire config lock
                revert      Options for reverting back to the original config
                time        Time for which to wait for confirmation
        time ('int', optional): config_replace_options selected as time (default is 1 second)
        timeout ('int'): Timeout for applying config (default is 30 second)

    Returns:
        execution output
    Raises:
        SubCommandFailure
    """
    dialog = Dialog([
        Statement(
            pattern=r".*\[no\].*",
            action="sendline(Y)",
            loop_continue=True,
            continue_timer=True,
        )
    ])
    cmd = f"configure replace {path}{file}"
    if config_replace_options:
        if config_replace_options == "revert":
            cmd += " revert trigger"
        elif config_replace_options == "time":
            cmd += f" time {timer}"
        else:
            cmd += f" {config_replace_options}"
    try:
        device.state_machine.learn_hostname = True
        output = device.execute(cmd, reply=dialog, timeout=timeout, append_error_pattern=['Error:'])
        learned_hostname = device._get_learned_hostname(device.spawn)
        device.default.learned_hostname = learned_hostname
        device.state_machine.learn_hostname = False
        return output
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to replace saved configuration on device {device}. Error:\n{e}"
        )
