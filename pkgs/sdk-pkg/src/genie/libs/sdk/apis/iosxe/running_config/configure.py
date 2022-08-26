"""Utility type functions that do not fit into another category"""

# Python
import logging

# pyATS
from pyats.easypy import runtime

# Running-Config
from genie.libs.sdk.apis.iosxe.running_config.get import (
    get_running_config,
    get_running_config_section
)

# unicon
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def save_running_config(
    device, source="running-config", destination="startup-config"
):
    """ Save config

        Args:
            device (`obj`): Device object
            source (`str`): source to copy from
            destination (`str`): destination to copy to
        Returns:
            None
    """
    try:
        device.copy(source=source, dest=destination)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Failed to save configuration from "{source}" '
            "to {dest}".format(source=source, dest=destination)
        )


def copy_file_to_running_config(device, path, file, timeout=60):
    """ Restore config from local file using copy function
        Args:
            device (`obj`): Device object
            path (`str`): directory
            file (`str`): file name
            timeout (`str`): timeout
        Returns:
            None
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r".*Destination filename.*",
                action="sendline()",
                loop_continue=True,
                continue_timer=False,
            )
        ]
    )
    try:
        device.execute(
            "copy {path}{file} running-config".format(path=path, file=file),
            reply=dialog, timeout=timeout
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not copy saved configuration on "
            "device {device}.\nError: {e}".format(device=device.name, e=str(e))
        )


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


def remove_running_config(device, remove_config):
    """ Remove running configuration starting with passed keyword from device

        Args:
            device ('obj')        : Device object to modify configuration
            remove_config ('str') : Configuration to be removed from device

        Returns:
            None
    """

    config_list = get_running_config(
        device=device, keyword=remove_config
    )

    config_list = list(map(lambda conf: "no " + conf, config_list))

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to remove {config} configuration on device "
            "{device}".format(device=device.name, config=config_list)
        ) from e


def remove_tacacs_server(device, remove_config=None, keyword='tacacs'):
    """ Remove tacacs server configuration from device

        Args:
            device ('obj')        : Device object to modify configuration
            remove_config ('list') : Configuration to be removed from device
            keyword ('str') : keyword the configuration should start with 

        Returns:
            None
    """
    config_list = []
    if not remove_config:
        remove_config = get_running_config_section(device=device, keyword=keyword)

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
            "{device}".format(device=device.name, config=config_list)
        ) from e

def copy_config_from_tftp_to_media(device,
        host,
        config_file_with_path,
        file,
        timeout=30,
        vrf=None,
        media="bootflash"
    ):
    """ Copy configuration file from tftp location to media

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
        Statement(pattern=r'.*Address or name of remote host.*',
            action=f'sendline({host})',
            loop_continue=True,
            continue_timer=False),
        Statement(pattern=r'.*Source filename.*',
            action=f'sendline({config_file_with_path})',
            loop_continue=True,
            continue_timer=False),
        Statement(pattern=r'.*Destination filename',
            action=f'sendline({file})',
            loop_continue=True,
            continue_timer=False),
        Statement(pattern=r'.*Do you want to over write.*',
            action=f'sendline(yes)',
            loop_continue=True,
            continue_timer=False)
        ])
    error_patterns = [f'.*%Error opening.*']

    log.debug("Copy configuration file from tftp to device")
    if vrf is None:
        command = (f"copy tftp: {media}:")
    else:
        command = (f"copy tftp: {media}: vrf {vrf}")
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
            "tftp copy did'nt happen for {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

