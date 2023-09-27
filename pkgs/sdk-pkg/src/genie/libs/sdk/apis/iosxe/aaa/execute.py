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
            rp ('str'): route processor r0/r1/rp
            feature_type ('str'): feature name
            debug_type ('str'): type of the debugs warning/debug etc
            switch ('str', optional): switch for SVL/Stack devices
            snumber ('str', optional): switch number 1/2/active/standby
    '''
    if switch:
        cmd = f"set platform software trace {sprocess} {switch} {snumber} {rp} {feature_type} {debug_type}"
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
