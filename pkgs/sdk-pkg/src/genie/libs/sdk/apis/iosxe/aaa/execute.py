'''IOSXE execute functions for security'''

# Python
import re
import logging
import time

# Unicon
from unicon.core.errors import SubCommandFailure

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
