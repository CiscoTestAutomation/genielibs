'''IOSXE execute functions for acm replace'''

# Python
import re
import logging

# pyATS
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def acm_replace(device, storage_type, configlet_name, vrf=None, timeout=None, validate=False):
    """
    Replaced the new configuration with the existing configuration.

    Args:
        device ('obj'): Device object
        storage_type ('str'): The type of storage where the configlet is located.
        configlet_name ('str'): The name of the configlet to be replaced.
        vrf ('str', optional): VRF to use for the operation. Defaults to None.
        timeout (int): Timeout for the replace operation.
        validate (bool, optional): Whether to add 'validate' at the end of the command. Defaults to False.

    Returns:
        None

    Raises:
        SubCommandFailure
    """

    cmd = f"acm replace {storage_type}:{configlet_name}"

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
            f"Could not execute acm replace operation on {device}. Error:\n{e}"
        )