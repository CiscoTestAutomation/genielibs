"""common configure functions for single policy"""
import logging
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog

log = logging.getLogger(__name__)
DIALOG = Dialog([Statement(pattern=r'\(yes\/\[no\]\).*',
         action='sendline(yes)',loop_continue=False,
        continue_timer=False)])

def configure_authentication_convert_to_new_style_single_policy_interface(device, interface, force=False,max_time=30):
    """Common funtion to configure authentication convert-to new-style
        single-policy interface for both forced and without forced 
        Args:
            device ('obj'): device to use
            interface (`str`): Interface name
            force (`bool`): Force the CLI. Defaults to False
            max_time (`int`): Timeout for Dialog
        Returns:
            None
        Raises:
            SubCommandFailure:Failed to configure authentication convert-to new-style single-policy interface
            """
    cmd = "authentication convert-to new-style single-policy interface {interface}".format(interface=interface)
    if force:
        cmd += " forced"
    try:
        device.configure(cmd, reply=DIALOG,timeout=max_time)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure authentication convert-to new-style single-policy interface {interface}. Error:\n{error}".format(
                interface=interface,error=e
            ))
def configure_access_session_single_policy_interface(device, interface, force=False,max_time=30):
    """Common funtion to configure access-session single-policy interface for both forced and without forced
        Args:
            device ('obj'): device to use
            interface (`str`): Interface name
            force (`bool`): Force the CLI. Defaults to False
            max_time (`int`): Timeout for Dialog
        Returns:
            None
        Raises:
            SubCommandFailure:Failed to configure access-session single-policy interface
            """
    cmd = "access-session single-policy interface {interface}".format(interface=interface)
    if force:
        cmd += " forced"
    try:
        device.configure(cmd, reply=DIALOG,timeout=max_time)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure access-session single-policy interface {interface}. Error:\n{error}".format(
                interface=interface,error=e
            ))
def configure_access_session_single_policy_policy_name(device, policy_name, force=False,max_time=30):
    """Common function to configure access-session single-policy policy-name for both forced and without forced 
        Args:
            device ('obj'): device to use
            policy_name (`str`): Policy name
            force (`bool`): Force the CLI. Defaults to False
            max_time (`int`): Timeout for Dialog
        Returns:
            None
        Raises:
            SubCommandFailure:Failed to configure access-session single-policy policy-name
            """
    cmd = "access-session single-policy policy-name {policy_name}".format(policy_name=policy_name)
    if force:
        cmd += " forced"
    try:
        device.configure(cmd, reply=DIALOG,timeout=max_time)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not access-session single-policy policy-name {policy_name}. Error:\n{error}".format(
                policy_name=policy_name,error=e
            ))
def configure_authentication_convert_to_new_style(device, force=False,max_time=30):
    """Common function to configure authentication convert-to new-style for both forced and without forced
        Args:
            device ('obj'): device to use
            force (`bool`): Force the CLI. Defaults to False
            max_time (`int`): Timeout for Dialog
        Returns:
            None
        Raises:
            SubCommandFailure:Failed to configure authentication convert-to new-style
            """
    cmd = "authentication convert-to new-style"
    if force:
        cmd += " forced"
    try:
        device.configure(cmd, reply=DIALOG,timeout=max_time)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure authentication convert-to new-style. Error:\n{error}".format(error=e
            ))

