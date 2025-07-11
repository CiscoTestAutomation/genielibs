'''IOSXE execute functions for acm'''

# Python
import re
import logging

# pyATS
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def acm_merge(device, storage_type, configlet_name, vrf=None, timeout=None, validate=False):
    """
    Merges the new configuration with the existing configuration.

    Args:
        device ('obj'): Device object
        storage_type ('str'): The type of storage where the configlet is located (e.g., 'tftp', 'scp').
        configlet_name ('str'): The name or path of the configlet to be merged.
        vrf ('str', optional): VRF to use for the operation. Defaults to None.
        timeout (int, optional): Timeout for the merge operation. Defaults to None.
        validate (bool, optional): Whether to add 'validate' at the end of the command. Defaults to False.

    Returns:
        None

    Raises:
        SubCommandFailure: If the merge operation fails.
    """
    cmd = f"acm merge {storage_type}:{configlet_name}"
    
    if vrf:
        cmd += f" vrf {vrf}"

    if timeout:
        cmd += f" timeout {timeout}"

    if validate:
        cmd += " validate"

    try:
        device.execute(cmd, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute ACM merge operation on {device.name}. Error:\n{e}"
        )