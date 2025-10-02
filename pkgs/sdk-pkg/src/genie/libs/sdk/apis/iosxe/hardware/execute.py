"""Execute Interface related command"""

# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog
from unicon.eal.expect import Spawn, TimeoutError


log = logging.getLogger(__name__)

def execute_hw_module_subslot_oir(device, line_card, action, switch_num=None):
    """
    Execute 
    'hw-module switch {switch_num} subslot {line_card}/0 oir {oir_oper}' or
    'hw-module subslot {line_card}/0 oir {oir_oper}' on the device.

    Args:
        device (obj): Device object
        line_card (
        int): Line card number
        oir_oper (str): OIR operation/action (e.g., 'insert', 'remove', 'power-cycle')
        switch_num (int, optional): Switch number. If provided, uses the switch command.

    Returns:
        str: Output of the command

    Raises:
        SubCommandFailure: If command execution fails
    """
    if switch_num is not None:
        cmd = f"hw-module switch {switch_num} subslot {line_card}/0 oir {action}"
    else:
        cmd = f"hw-module subslot {line_card}/0 oir {action}"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        log.error(f"Failed to execute '{cmd}': {e}")
        raise SubCommandFailure(f'Failed to perform Slot {line_card} {action}')
    return out

def execute_hw_module_beacon_fan_tray(device, fan_tray_number, action, switch_num=None):
    """
    Execute 'hw-module beacon switch {switch_num} fan-tray {fan_tray_number} {action}' or
    'hw-module beacon fan-tray {fan_tray_number} {action}' on the device.

    Args:
        device (obj): Device object
        fan_tray_number (int): Fan tray number
        action (str): Action to perform (e.g., 'on', 'off', 'blink-fast', 'blink-slow')
        switch_num (int, optional): Switch number. If provided, uses the switch command.

    Returns:
        str: Output of the command

    Raises:
        SubCommandFailure: If command execution fails
    """
    if switch_num is not None:
        cmd = f"hw-module beacon switch {switch_num} fan-tray {fan_tray_number} {action}"
    else:
        cmd = f"hw-module beacon fan-tray {fan_tray_number} {action}"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        log.error(f"Failed to execute '{cmd}': {e}")
        raise SubCommandFailure(f'Failed to perform Fan-tray {action} on {fan_tray_number}')
    return out