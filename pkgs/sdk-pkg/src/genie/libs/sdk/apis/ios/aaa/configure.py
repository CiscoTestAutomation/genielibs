"""Common configure functions for aaa on IOS"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_aaa_new_model(device):
    """Configure aaa new-model.

        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(["aaa new-model"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure AAA new-model. Error:\n{e}"
        )


def unconfigure_aaa_new_model(device):
    """Unconfigure aaa new-model.

        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(["no aaa new-model"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure AAA new-model. Error:\n{e}"
        )


def configure_aaa_authentication_login(device, auth_list, auth_type,
                                       group_name=""):
    """Configure aaa authentication login.

        Args:
            device ('obj'): Device object
            auth_list ('str'): Authentication list name
            auth_type ('str'): Authentication type (e.g. local/none)
            group_name ('str', optional): Server-group name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"aaa authentication login {auth_list} {auth_type}"
    if group_name:
        cmd += f" {group_name}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure aaa authentication login. Error:\n{e}"
        )


def unconfigure_aaa_authentication_login(device, auth_list, auth_type,
                                         group_name=""):
    """Unconfigure aaa authentication login.

        Args:
            device ('obj'): Device object
            auth_list ('str'): Authentication list name
            auth_type ('str'): Authentication type (e.g. local/none)
            group_name ('str', optional): Server-group name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"no aaa authentication login {auth_list} {auth_type}"
    if group_name:
        cmd += f" {group_name}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure aaa authentication login. Error:\n{e}"
        )


def configure_aaa_authorization_exec(device, auth_list, auth_type,
                                     group_name=""):
    """Configure aaa authorization exec.

        Args:
            device ('obj'): Device object
            auth_list ('str'): Authorization list name
            auth_type ('str'): Authorization type (e.g. local/none)
            group_name ('str', optional): Server-group name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"aaa authorization exec {auth_list} {auth_type}"
    if group_name:
        cmd += f" {group_name}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure aaa authorization exec. Error:\n{e}"
        )


def unconfigure_aaa_authorization_exec(device, auth_list, auth_type,
                                       group_name=""):
    """Unconfigure aaa authorization exec.

        Args:
            device ('obj'): Device object
            auth_list ('str'): Authorization list name
            auth_type ('str'): Authorization type (e.g. local/none)
            group_name ('str', optional): Server-group name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"no aaa authorization exec {auth_list} {auth_type}"
    if group_name:
        cmd += f" {group_name}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure aaa authorization exec. Error:\n{e}"
        )
