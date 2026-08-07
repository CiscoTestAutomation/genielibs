"""Common configure functions for IOS platform"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_line_console(
    device,
    line_number,
    exec_timeout_minutes=None,
    exec_timeout_seconds=None,
    login_authentication=None,
    password=None,
    transport_input=None,
):
    """Configure line console on device

        Args:
            device (`obj`): Device object
            line_number (`int`): Console line number (e.g. 0)
            exec_timeout_minutes (`int`, optional): Exec timeout minutes.
                Defaults to None
            exec_timeout_seconds (`int`, optional): Exec timeout seconds.
                Defaults to None
            login_authentication (`str`, optional): Login authentication
                list name. Defaults to None
            password (`str`, optional): Line password. Defaults to None
            transport_input (`str`, optional): Transport input protocol
                (e.g. 'all', 'ssh'). Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"line console {line_number}"]
    if exec_timeout_minutes is not None and exec_timeout_seconds is not None:
        cmd.append(
            f" exec-timeout {exec_timeout_minutes} {exec_timeout_seconds}"
        )
    elif exec_timeout_minutes is not None:
        cmd.append(f" exec-timeout {exec_timeout_minutes}")
    if login_authentication:
        cmd.append(f" login authentication {login_authentication}")
    if password:
        cmd.append(f" password {password}")
    if transport_input:
        cmd.append(f" transport input {transport_input}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure line console {line_number}. Error: {e}"
        )


def configure_line_vty(
    device,
    first_vty,
    last_vty,
    exec_timeout_minutes=None,
    exec_timeout_seconds=None,
    login_authentication=None,
    password=None,
    transport_input=None,
):
    """Configure line vty on device

        Args:
            device (`obj`): Device object
            first_vty (`int`): First vty line number (e.g. 0)
            last_vty (`int`): Last vty line number (e.g. 4)
            exec_timeout_minutes (`int`, optional): Exec timeout minutes.
                Defaults to None
            exec_timeout_seconds (`int`, optional): Exec timeout seconds.
                Defaults to None
            login_authentication (`str`, optional): Login authentication
                list name. Defaults to None
            password (`str`, optional): Line password. Defaults to None
            transport_input (`str`, optional): Transport input protocol
                (e.g. 'all', 'ssh'). Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"line vty {first_vty} {last_vty}"]
    if exec_timeout_minutes is not None and exec_timeout_seconds is not None:
        cmd.append(
            f" exec-timeout {exec_timeout_minutes} {exec_timeout_seconds}"
        )
    elif exec_timeout_minutes is not None:
        cmd.append(f" exec-timeout {exec_timeout_minutes}")
    if password:
        cmd.append(f" password {password}")
    if login_authentication:
        cmd.append(f" login authentication {login_authentication}")
    if transport_input:
        cmd.append(f" transport input {transport_input}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure line vty {first_vty} {last_vty}. Error: {e}"
        )


def configure_bba_group(device, name, vt_number,
                        service_profile_name=None,
                        tag=None,
                        session_per_vlan_limit=None,
                        session_per_mac_limit=None):
    """Configure bba-group pppoe on device.

        Args:
            device (`obj`): Device object
            name (`str`): bba-group name
            vt_number (`str`): virtual-template interface number
            service_profile_name (`str`, optional): service profile name.
                Defaults to None
            tag (`str`, optional): ppp-max-payload value.
                Defaults to None
            session_per_vlan_limit (`str`, optional): Per-VLAN session limit.
                Defaults to None
            session_per_mac_limit (`str`, optional): Per-MAC session limit.
                Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cli = [
        f"bba-group pppoe {name}",
        f"virtual-template {vt_number}",
    ]
    if service_profile_name:
        cli.append(f"service profile {service_profile_name}")
    if tag:
        cli.append(f"tag ppp-max-payload {tag}")
    if session_per_vlan_limit is not None:
        cli.append(f"sessions per-vlan limit {session_per_vlan_limit}")
    if session_per_mac_limit is not None:
        cli.append(f"sessions per-mac limit {session_per_mac_limit}")

    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not config bba-group on {device}. Error:\n{e}"
        )


def unconfigure_bba_group(device, name, vt_number=None):
    """Unconfigure bba-group pppoe on device.

        Args:
            device (`obj`): Device object
            name (`str`): bba-group name
            vt_number (`str`, optional): virtual-template interface number.
                If provided, only the virtual-template is removed from the
                bba-group (the bba-group itself is kept). Defaults to None.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if vt_number is not None:
        cli = [
            f"bba-group pppoe {name}",
            f"no virtual-template {vt_number}",
        ]
    else:
        cli = [f"no bba-group pppoe {name}"]

    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfig bba-group on {device}. Error:\n{e}"
        )
