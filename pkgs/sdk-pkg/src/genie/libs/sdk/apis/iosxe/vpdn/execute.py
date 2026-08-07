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


def execute_clear_vpdn_tunnel_pptp(
    device, remote_hostname, local_hostname, timeout=60
):
    """Execute ``clear vpdn tunnel pptp {remote_hostname} {local_hostname}``.

    Args:
        device ('obj'): Device object
        remote_hostname ('str'): Remote hostname filter
        local_hostname ('str'): Local hostname filter
        timeout ('int'): Execute timeout in seconds
    """

    command = (
        "clear vpdn tunnel pptp {remote_hostname} {local_hostname}".format(
            remote_hostname=remote_hostname, local_hostname=local_hostname
        )
    )

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute '{command}' on {device}. Error:\n{e}"
        )


def execute_clear_vpdn_counters(device, timeout=60):
    """Execute ``clear vpdn counters``."""

    command = "clear vpdn counters"

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute '{command}' on {device}. Error:\n{e}"
        )


def execute_clear_vpdn_counters_tunnel_all(device, protocol, timeout=60):
    """Execute ``clear vpdn counters tunnel {protocol} all``.

    Args:
        device ('obj'): Device object
        protocol ('str'): Tunnel protocol, for example ``l2tp`` or ``pptp``
        timeout ('int'): Execute timeout in seconds
    """

    command = "clear vpdn counters tunnel {protocol} all".format(
        protocol=protocol
    )

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute '{command}' on {device}. Error:\n{e}"
        )


def execute_clear_vpdn_counters_tunnel_id(
    device, protocol, tunnel_id, timeout=60
):
    """Execute ``clear vpdn counters tunnel {protocol} id {tunnel_id}``.

    Args:
        device ('obj'): Device object
        protocol ('str'): Tunnel protocol, for example ``l2tp`` or ``pptp``
        tunnel_id ('str'): Local tunnel ID
        timeout ('int'): Execute timeout in seconds
    """

    command = "clear vpdn counters tunnel {protocol} id {tunnel_id}".format(
        protocol=protocol, tunnel_id=tunnel_id
    )

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute '{command}' on {device}. Error:\n{e}"
        )


def execute_clear_vpdn_counters_tunnel_hostname(
    device, protocol, remote_hostname, local_hostname, timeout=60
):
    """Execute ``clear vpdn counters tunnel {protocol} hostname
    {remote_hostname} {local_hostname}``.

    Args:
        device ('obj'): Device object
        protocol ('str'): Tunnel protocol, for example ``l2tp`` or ``pptp``
        remote_hostname ('str'): Remote hostname filter
        local_hostname ('str'): Local hostname filter
        timeout ('int'): Execute timeout in seconds
    """

    command = (
        "clear vpdn counters tunnel {protocol} hostname "
        "{remote_hostname} {local_hostname}".format(
            protocol=protocol,
            remote_hostname=remote_hostname,
            local_hostname=local_hostname,
        )
    )

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute '{command}' on {device}. Error:\n{e}"
        )


def execute_clear_vpdn_counters_tunnel_ip(
    device, protocol, ip_filter, ip_address, timeout=60
):
    """Execute ``clear vpdn counters tunnel {protocol} ip {ip_filter}
    {ip_address}``.

    Args:
        device ('obj'): Device object
        protocol ('str'): Tunnel protocol, for example ``l2tp`` or ``pptp``
        ip_filter ('str'): IP filter keyword, ``local`` or ``remote``
        ip_address ('str'): IP address filter
        timeout ('int'): Execute timeout in seconds
    """

    command = (
        "clear vpdn counters tunnel {protocol} ip {ip_filter} "
        "{ip_address}".format(
            protocol=protocol, ip_filter=ip_filter, ip_address=ip_address
        )
    )

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute '{command}' on {device}. Error:\n{e}"
        )


def execute_clear_vpdn_counters_session_username(
    device, username, timeout=60
):
    """Execute ``clear vpdn counters session username {username}``.

    Args:
        device ('obj'): Device object
        username ('str'): Username filter
        timeout ('int'): Execute timeout in seconds
    """

    command = "clear vpdn counters session username {username}".format(
        username=username
    )

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute '{command}' on {device}. Error:\n{e}"
        )


def execute_clear_vpdn_counters_session_id(
    device, tunnel_id, session_id, timeout=60
):
    """Execute ``clear vpdn counters session id {tunnel_id} {session_id}``.

    Args:
        device ('obj'): Device object
        tunnel_id ('str'): Local tunnel ID filter
        session_id ('str'): Local session ID filter
        timeout ('int'): Execute timeout in seconds
    """

    command = (
        "clear vpdn counters session id {tunnel_id} {session_id}".format(
            tunnel_id=tunnel_id, session_id=session_id
        )
    )

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute '{command}' on {device}. Error:\n{e}"
        )


def execute_clear_vpdn_counters_session_interface_virtual_access(
    device, virtual_access_interface, timeout=60
):
    """Execute ``clear vpdn counters session interface virtual-access
    {virtual_access_interface}``.

    Args:
        device ('obj'): Device object
        virtual_access_interface ('str'): Virtual-Access interface number
        timeout ('int'): Execute timeout in seconds
    """

    command = (
        "clear vpdn counters session interface virtual-access "
        "{virtual_access_interface}".format(
            virtual_access_interface=virtual_access_interface
        )
    )

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute '{command}' on {device}. Error:\n{e}"
        )


def execute_clear_vpdn_history_failure(device, timeout=60):
    """Execute ``clear vpdn history failure``."""

    command = "clear vpdn history failure"

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
