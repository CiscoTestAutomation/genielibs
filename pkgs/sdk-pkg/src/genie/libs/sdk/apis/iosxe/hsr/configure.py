"""Common configure functions for hsr"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError


log = logging.getLogger(__name__)

def configure_fpga_profile(device, profile):
    """
    Configures the FPGA profile on the device.

    Args:
        device (`obj`): Device object
        profile (`str`): FPGA profile to activate. Options are:
                         - "default"
                         - "hsr-quadbox"
                         - "redundancy"

    Returns:
        None

    Raises:
        SubCommandFailure: If the command fails to execute.
    """
    valid_profiles = ["default", "hsr-quadbox", "redundancy"]
    if profile not in valid_profiles:
        raise ValueError(f"Invalid profile '{profile}'. Valid options are: {valid_profiles}")

    command = f"fpga-profile activate {profile}"
    try:
        device.execute(command)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure FPGA profile '{profile}' on device: {e}")

def configure_hsr_hsr_mode(device, pair_type, confirm="yes"):
    """
    Configures HSR-HSR mode on the device.

    Args:
        device (`obj`): Device object
        pair_type (`str`): Pair type to configure. Options are:
                          - "copper"
                          - "mixed"
                          - "sfp"
        confirm (`str`): Confirmation response for the prompt. Options are:
                         - "yes"
                         - "no"

    Returns:
        None

    Raises:
        ValueError: If invalid pair_type or confirm is provided.
        SubCommandFailure: If the command fails to execute.
    """
    valid_pair_types = ["copper", "mixed", "sfp"]
    valid_confirm_responses = ["yes", "no"]

    if pair_type not in valid_pair_types:
        raise ValueError(f"Invalid pair_type '{pair_type}'. Valid options are: {valid_pair_types}")
    if confirm not in valid_confirm_responses:
        raise ValueError(f"Invalid confirm response '{confirm}'. Valid options are: {valid_confirm_responses}")

    command = f"hsr-hsr-mode enable pair {pair_type}"

    # Define a Dialog to handle the interactive prompt
    dialog = Dialog([
        Statement(
            pattern=r"ACCEPT\? \(yes/\[no\]\):",
            action=lambda spawn: spawn.sendline(confirm),
            loop_continue=True,
            continue_timer=False
        )
    ])

    try:
        device.configure(command, reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure HSR-HSR mode with pair '{pair_type}' on device: {e}")

def unconfigure_hsr_hsr_mode(device, confirm="yes"):
    """
    Unconfigures HSR-HSR mode on the device.

    Args:
        device (`obj`): Device object
        confirm (`str`): Confirmation response for the prompt. Options are:
                         - "yes"
                         - "no"

    Returns:
        None

    Raises:
        ValueError: If invalid confirm is provided.
        SubCommandFailure: If the command fails to execute.
    """
    valid_confirm_responses = ["yes", "no"]

    if confirm not in valid_confirm_responses:
        raise ValueError(f"Invalid confirm response '{confirm}'. Valid options are: {valid_confirm_responses}")

    command = "no hsr-hsr-mode enable"

    # Define a Dialog to handle the interactive prompt
    dialog = Dialog([
        Statement(
            pattern=r"ACCEPT\? \(yes/\[no\]\):",
            action=lambda spawn: spawn.sendline(confirm),
            loop_continue=True,
            continue_timer=False
        )
    ])

    try:
        device.configure(command, reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to deactivate HSR-HSR mode on device: {e}")

def configure_hsr_multicast_filter(device, ring_id, group_id, multi_mac, mask=None):
    """
    Configures HSR multicast filter deny group on the device.

    Args:
        device (`obj`): Device object
        ring_id (`int`): HSR ring ID (e.g., 1)
        group_id (`int`): Multicast filter group ID (e.g., 1-260)
        multi_mac (`str`): Multicast MAC address (e.g., "0000.0000.0011")
        mask (`str`, optional): Mask value (e.g., "ffff.ffff.ffff"). Required for group_id 1-4.

    Returns:
        None

    Raises:
        ValueError: If invalid input is provided.
        SubCommandFailure: If the command fails to execute.
    """
    # Validate inputs
    if not isinstance(ring_id, int) or ring_id <= 0:
        raise ValueError("Invalid ring_id. It must be a positive integer.")
    if not isinstance(group_id, int) or group_id < 1 or group_id > 260:
        raise ValueError("Invalid group_id. It must be in the range 1-260.")
    if not isinstance(multi_mac, str):
        raise ValueError("Invalid multi_mac. It must be a string.")

    # Determine if mask is required
    if 1 <= group_id <= 4:
        if not mask:
            raise ValueError("Mask is required for group_id in the range 1-4.")
        command = f"hsr-ring {ring_id} multicast_filter_deny_group {group_id} {multi_mac} {mask}"
    elif 5 <= group_id <= 260:
        command = f"hsr-ring {ring_id} multicast_filter_deny_group {group_id} {multi_mac}"

    try:
        # Execute the command on the device
        device.configure(command)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure HSR multicast filter deny group on device: {e}")

def unconfigure_hsr_multicast_filter(device, ring_id, group_id, multi_mac, mask=None):
    """
    Unconfigures HSR multicast filter deny group on the device.

    Args:
        device (`obj`): Device object
        ring_id (`int`): HSR ring ID (e.g., 1)
        group_id (`int`): Multicast filter group ID (e.g., 1-260)
        multi_mac (`str`): Multicast MAC address (e.g., "0000.0000.0011")
        mask (`str`, optional): Mask value (e.g., "ffff.ffff.ffff"). Required for group_id 1-4.

    Returns:
        None

    Raises:
        ValueError: If invalid input is provided.
        SubCommandFailure: If the command fails to execute.
    """
    # Validate inputs
    if not isinstance(ring_id, int) or ring_id <= 0:
        raise ValueError("Invalid ring_id. It must be a positive integer.")
    if not isinstance(group_id, int) or group_id < 1 or group_id > 260:
        raise ValueError("Invalid group_id. It must be in the range 1-260.")
    if not isinstance(multi_mac, str):
        raise ValueError("Invalid multi_mac. It must be a string.")

    # Determine if mask is required
    if 1 <= group_id <= 4:
        if not mask:
            raise ValueError("Mask is required for group_id in the range 1-4.")
        command = f"no hsr-ring {ring_id} multicast_filter_deny_group {group_id} {multi_mac} {mask}"
    elif 5 <= group_id <= 260:
        command = f"no hsr-ring {ring_id} multicast_filter_deny_group {group_id} {multi_mac}"

    try:
        # Execute the command on the device
        device.configure(command)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure HSR multicast filter deny group on device: {e}")
    
    

    


