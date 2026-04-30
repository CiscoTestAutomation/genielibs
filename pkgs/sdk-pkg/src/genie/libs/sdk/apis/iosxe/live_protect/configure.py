"""Common configure functions for live protect."""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_platform_security_live_protect_shield_enforcing(device, shield_id):
    """Configure live-protect shield in enforcing mode.

    Args:
        device ('obj'): Device object
        shield_id ('str'): Live-protect shield identifier

    Returns:
        None

    Raises:
        SubCommandFailure: Failed configuring the shield
    """

    cmd = f"platform security live-protect shield {shield_id} enforcing"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure platform security live-protect shield "
            "{shield_id} enforcing on {device}. Error:\n{error}".format(
                shield_id=shield_id, device=device, error=e
            )
        )


def unconfigure_platform_security_live_protect_shield_enforcing(device, shield_id):
    """Unconfigure live-protect shield enforcing mode.

    Args:
        device ('obj'): Device object
        shield_id ('str'): Live-protect shield identifier

    Returns:
        None

    Raises:
        SubCommandFailure: Failed unconfiguring the shield
    """

    cmd = f"no platform security live-protect shield {shield_id} enforcing"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure platform security live-protect shield "
            "{shield_id} enforcing on {device}. Error:\n{error}".format(
                shield_id=shield_id, device=device, error=e
            )
        )
