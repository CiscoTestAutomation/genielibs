'''IOSXE execute functions for security'''

# Python
import re
import logging
import time

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog

# Logger
log = logging.getLogger(__name__)

def set_platform_soft_trace_debug(device, sprocess, snumber, rp, feature_type, debug_type, switch=None):
    ''' set platform software trace aaa-acct debug
        Args:
            device ('obj'): Device object
            sprocess ('str'): process for trace logs
            snumber ('str', optional): switch number 1/2/active/standby
            rp ('str'): route processor r0/r1/RP
            feature_type ('str'): feature name
            debug_type ('str'): type of the debugs warning/debug etc
            switch ('str', optional): switch for SVL/Stack devices
    '''

    if switch:
        cmd = f"set platform software trace {sprocess} {switch} {snumber} {rp} {feature_type} {debug_type}"
    else:
        if rp == "RP":
            cmd = f"set platform software trace {sprocess} {rp} active {feature_type} {debug_type}"
        else:
            cmd = f"set platform software trace {sprocess} {rp} {feature_type} {debug_type}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not set platform software trace aaa-acct debug {device}. Error:\n{e}")

def show_logging_smd_output_to_file(device, sprocess, file_name):
    ''' show logging process sprocess start last clear to-file flash:file_name
        Args:
            device ('obj'): Device object
            sprocess ('str'): process for trace logs
            file_name ('str', optional): name of a file
    '''
    cmd = f'show logging process {sprocess} start last clear to-file flash:{file_name}'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not set platform software trace aaa-acct debug {device}. Error:\n{e}")

def execute_clear_aaa_counters_server(device, server_info='', server_id='all'):
    """ Execute clear aaa counters for servers
        Example: clear aaa counters servers all
        Args:
            device ('obj'): Device object
            server_info ('str'): specifying server information (eg. radius)
            server_id ('str'): server id displayed by show aaa servers(Range 0-2147483647)
        Returns:
            output
        Raises:
            SubCommandFailure
    """
    log.info("Clear aaa counters servers on the device")

    dialog = Statement(
        pattern=r".*clear aaa counters servers \[confirm\]",
        action='sendline()',
        loop_continue=True,
        continue_timer=False)
    cmd = f"clear aaa counters servers {server_info} {server_id}"
    try:
        device.execute(cmd, reply=Dialog([dialog]))
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not clear aaa counters servers on device. Error:\n{e}")


def _execute_debug(device, cmd, enable=True):
    """Helper to enable/disable a debug command in exec mode.

    Args:
        device ('obj'): Device object
        cmd ('str'): The full debug command (e.g. 'debug dot1x all')
        enable ('bool'): True to enable the debug, False to issue
                        the corresponding 'no <cmd>' to disable it.
    Returns:
        str: command output
    Raises:
        SubCommandFailure: when the command fails on the device
    """
    full_cmd = cmd if enable else f'no {cmd}'
    try:
        return device.execute(full_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute '{full_cmd}' on device "
            f"{device.name}. Error:\n{e}")


def debug_access_session_all(device, enable=True):
    """Enable/disable 'debug access-session all'.

    Args:
        device ('obj'): Device object
        enable ('bool'): True to enable, False to disable. Default True.
    Returns:
        str: command output
    Raises:
        SubCommandFailure: when the command fails on the device
    """
    return _execute_debug(device, 'debug access-session all', enable=enable)


def debug_dot1x_all(device, enable=True):
    """Enable/disable 'debug dot1x all'.

    Args:
        device ('obj'): Device object
        enable ('bool'): True to enable, False to disable. Default True.
    Returns:
        str: command output
    Raises:
        SubCommandFailure: when the command fails on the device
    """
    return _execute_debug(device, 'debug dot1x all', enable=enable)


def debug_mab_all(device, enable=True):
    """Enable/disable 'debug mab all'.

    Args:
        device ('obj'): Device object
        enable ('bool'): True to enable, False to disable. Default True.
    Returns:
        str: command output
    Raises:
        SubCommandFailure: when the command fails on the device
    """
    return _execute_debug(device, 'debug mab all', enable=enable)


def debug_aaa_authentication(device, enable=True):
    """Enable/disable 'debug aaa authentication'.

    Args:
        device ('obj'): Device object
        enable ('bool'): True to enable, False to disable. Default True.
    Returns:
        str: command output
    Raises:
        SubCommandFailure: when the command fails on the device
    """
    return _execute_debug(
        device, 'debug aaa authentication', enable=enable)


def debug_aaa_authorization(device, enable=True):
    """Enable/disable 'debug aaa authorization'.

    Args:
        device ('obj'): Device object
        enable ('bool'): True to enable, False to disable. Default True.
    Returns:
        str: command output
    Raises:
        SubCommandFailure: when the command fails on the device
    """
    return _execute_debug(
        device, 'debug aaa authorization', enable=enable)


def debug_epm_all(device, enable=True):
    """Enable/disable 'debug epm all'.

    Args:
        device ('obj'): Device object
        enable ('bool'): True to enable, False to disable. Default True.
    Returns:
        str: command output
    Raises:
        SubCommandFailure: when the command fails on the device
    """
    return _execute_debug(device, 'debug epm all', enable=enable)


def debug_radius_authentication(device, enable=True):
    """Enable/disable 'debug radius authentication'.

    Args:
        device ('obj'): Device object
        enable ('bool'): True to enable, False to disable. Default True.
    Returns:
        str: command output
    Raises:
        SubCommandFailure: when the command fails on the device
    """
    return _execute_debug(
        device, 'debug radius authentication', enable=enable)
