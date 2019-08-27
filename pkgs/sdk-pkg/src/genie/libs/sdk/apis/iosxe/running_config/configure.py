"""Utility type functions that do not fit into another category"""

# Python
import logging

# pyATS
from ats.easypy import runtime

# Running-Config
from genie.libs.sdk.apis.iosxe.running_config.get import (
    get_running_config,
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


def copy_file_to_running_config(device, path, file):
    """ Restore config from local file using copy function

        Args:
            device (`obj`): Device object
            path (`str`): directory
            file (`str`): file name
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
            reply=dialog,
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not copy saved configuration on "
            "device {device}".format(device=device.name)
        )


def restore_running_config(device, path, file):
    """ Restore config from local file

        Args:
            device (`obj`): Device object
            path (`str`): directory
            file (`str`): file name
        Returns:
            None
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r".*Enter Y.*",
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
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not replace saved configuration on "
            "device {device}".format(device=device.name)
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
