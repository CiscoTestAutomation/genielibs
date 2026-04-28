"""Execute CLI functions for VPDN."""

from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

_CONFIRM_DIALOG = Dialog(
    [
        Statement(
            pattern=r".*\[confirm\].*",
            action="sendline()",
            loop_continue=True,
            continue_timer=False,
        )
    ]
)


def execute_clear_vpdn_dead_cache_all(device, timeout=60):
    """Execute ``clear vpdn dead-cache all``."""

    command = "clear vpdn dead-cache all"

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute '{command}' on {device}. Error:\n{e}"
        )


def execute_clear_vpdn_dead_cache_ip_address(device, ip_address, timeout=60):
    """Execute ``clear vpdn dead-cache ip-address {ip_address}``."""

    command = "clear vpdn dead-cache ip-address {ip_address}".format(
        ip_address=ip_address
    )

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute '{command}' on {device}. Error:\n{e}"
        )


def execute_clear_vpdn_dead_cache_group(device, group_name, timeout=60):
    """Execute ``clear vpdn dead-cache group {group_name}``."""

    command = "clear vpdn dead-cache group {group_name}".format(
        group_name=group_name
    )

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute '{command}' on {device}. Error:\n{e}"
        )


def execute_clear_vpdn_tunnel_l2tp_all(device, timeout=60):
    """Execute ``clear vpdn tunnel l2tp all``."""

    command = "clear vpdn tunnel l2tp all"

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute '{command}' on {device}. Error:\n{e}"
        )


def execute_clear_l2tp_all(device, timeout=60):
    """Execute ``clear l2tp all``."""

    command = "clear l2tp all"

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute '{command}' on {device}. Error:\n{e}"
        )
