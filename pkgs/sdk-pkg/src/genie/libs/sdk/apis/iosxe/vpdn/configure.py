"""Common configure functions for VPDN."""

import logging

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.vpdn.utils import _resolve_local_names

log = logging.getLogger(__name__)

_DEFAULT = object()


def configure_vpdn_group(
    device,
    authen_before_forward=False,
    vpdn_group_number=None,
    request_dialin=False,
    accept_dialin=False,
    domain=None,
    initiate_to=None,
    tunnel_hello_interval=None,
    tunnel_password=None,
    virtual_template_number=None,
    local_name=None,
    vpdn_enable=False,
    protocol=_DEFAULT,
    tunnel_password_encryption="0",
    tunnel_receive_window=None,
    request_local_name=None,
    accept_local_name=None,
    initiate_to_entries=None,
    busy_timeout=None,
):
    """Configure VPDN and optional VPDN group subcommands.

    Args:
        device ('obj'): Device object
        authen_before_forward ('bool'): Configure ``vpdn authen-before-forward``
        vpdn_group_number ('str'): VPDN group name/number
        request_dialin ('bool'): Configure ``request-dialin``
        accept_dialin ('bool'): Configure ``accept-dialin``
        domain ('str'): Domain name under ``request-dialin``
        initiate_to ('str'): IP address for ``initiate-to ip``
        tunnel_hello_interval ('str'): Value for ``l2tp tunnel hello``
        tunnel_password ('str'): Value for ``l2tp tunnel password``
        virtual_template_number ('str'): Value for ``virtual-template``
        local_name ('str'): Backward-compatible local name placement
        vpdn_enable ('bool'): Configure ``vpdn enable``
        protocol ('str' or None): Protocol value, default ``l2tp`` when
            request/accept dial-in is configured. Set to ``None`` to skip it.
        tunnel_password_encryption ('str'): Encryption type for
            ``l2tp tunnel password``
        tunnel_receive_window ('str'): Value for ``l2tp tunnel receive-window``
        request_local_name ('str'): Local name under ``request-dialin``
        accept_local_name ('str'): Local name under ``accept-dialin``
        initiate_to_entries ('list'): Additional ``initiate-to ip`` entries.
            Each item can be a string IP, ``(ip, priority)``, or
            ``{'ip': ip, 'priority': priority}``
        busy_timeout ('str'): Value for ``l2tp tunnel busy timeout``

    Returns:
        None

    Raises:
        ValueError: When group-only options are used without a VPDN group
        SubCommandFailure: Failed to configure VPDN
    """

    cli = []

    if protocol is _DEFAULT:
        protocol = "l2tp" if (request_dialin or accept_dialin) else None

    resolved_request_local_name, resolved_accept_local_name = _resolve_local_names(
        request_dialin=request_dialin,
        accept_dialin=accept_dialin,
        local_name=local_name,
        request_local_name=request_local_name,
        accept_local_name=accept_local_name,
    )

    group_specific_requested = any(
        [
            request_dialin,
            accept_dialin,
            tunnel_hello_interval is not None,
            tunnel_password is not None,
            tunnel_receive_window is not None,
            busy_timeout is not None,
            request_dialin and (resolved_request_local_name is not None),
            accept_dialin and (resolved_accept_local_name is not None),
        ]
    )

    if group_specific_requested and vpdn_group_number is None:
        raise ValueError(
            "vpdn_group_number must be provided when configuring vpdn-group options"
        )

    if vpdn_enable or authen_before_forward:
        cli.append("vpdn enable")

    if authen_before_forward:
        cli.append("vpdn authen-before-forward")

    if vpdn_group_number is not None:
        cli.append("vpdn-group {group}".format(group=vpdn_group_number))

        if request_dialin:
            cli.append("request-dialin")
            if protocol is not None:
                cli.append("protocol {protocol}".format(protocol=protocol))
            if domain is not None:
                cli.append("domain {domain}".format(domain=domain))

            entries = []
            if initiate_to is not None:
                entries.append(initiate_to)
            if initiate_to_entries:
                entries.extend(initiate_to_entries)

            for entry in entries:
                priority = None

                if isinstance(entry, dict):
                    ip_address = entry.get("ip") or entry.get("initiate_to")
                    priority = entry.get("priority")
                elif isinstance(entry, (tuple, list)):
                    ip_address = entry[0] if entry else None
                    if len(entry) > 1:
                        priority = entry[1]
                else:
                    ip_address = entry

                if not ip_address:
                    raise ValueError(
                        "Each initiate-to entry must include an IP address"
                    )

                command = "initiate-to ip {ip}".format(ip=ip_address)
                if priority is not None:
                    command += " priority {priority}".format(priority=priority)
                cli.append(command)

            if resolved_request_local_name is not None:
                cli.append(
                    "local name {local_name}".format(
                        local_name=resolved_request_local_name
                    )
                )

        if accept_dialin:
            cli.append("accept-dialin")
            if protocol is not None:
                cli.append("protocol {protocol}".format(protocol=protocol))
            if virtual_template_number is not None:
                cli.append(
                    "virtual-template {template}".format(
                        template=virtual_template_number
                    )
                )
            if resolved_accept_local_name is not None:
                cli.append(
                    "local name {local_name}".format(
                        local_name=resolved_accept_local_name
                    )
                )

        if tunnel_hello_interval is not None:
            cli.append(
                "l2tp tunnel hello {interval}".format(
                    interval=tunnel_hello_interval
                )
            )
        if tunnel_password is not None:
            cli.append(
                "l2tp tunnel password {password_type} {password}".format(
                    password_type=tunnel_password_encryption,
                    password=tunnel_password,
                )
            )
        if tunnel_receive_window is not None:
            cli.append(
                "l2tp tunnel receive-window {receive_window}".format(
                    receive_window=tunnel_receive_window
                )
            )
        if busy_timeout is not None:
            cli.append(
                "l2tp tunnel busy timeout {timeout}".format(timeout=busy_timeout)
            )

    if not cli:
        return

    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure the vpdn group. Error:\n{error}".format(error=e)
        )


def unconfigure_vpdn_group(device, vpdn_group_number):
    """Unconfigure VPDN group."""

    cli = ["no vpdn-group {group}".format(group=vpdn_group_number)]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure the vpdn group. Error:\n{error}".format(error=e)
        )


def configure_vpdn_l2tp_attribute_initial_received_lcp_confreq(device):
    """Configure ``vpdn l2tp attribute initial-received-lcp-confreq``."""

    cli = ["vpdn l2tp attribute initial-received-lcp-confreq"]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure vpdn l2tp attribute "
            "initial-received-lcp-confreq. Error:\n{error}".format(error=e)
        )


def unconfigure_vpdn_group_initiate_to_entries(
    device,
    vpdn_group_number,
    initiate_to_entries,
):
    """Unconfigure one or more ``initiate-to ip`` entries under a VPDN group."""

    cli = ["vpdn-group {group}".format(group=vpdn_group_number)]

    for entry in initiate_to_entries:
        priority = None

        if isinstance(entry, dict):
            ip_address = entry.get("ip") or entry.get("initiate_to")
            priority = entry.get("priority")
        elif isinstance(entry, (tuple, list)):
            ip_address = entry[0] if entry else None
            if len(entry) > 1:
                priority = entry[1]
        else:
            ip_address = entry

        if not ip_address:
            raise ValueError("Each initiate-to entry must include an IP address")

        command = "no initiate-to ip {ip}".format(ip=ip_address)
        if priority is not None:
            command += " priority {priority}".format(priority=priority)
        cli.append(command)

    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure initiate-to ip entries under the vpdn group. "
            "Error:\n{error}".format(error=e)
        )


def unconfigure_vpdn_l2tp_attribute_initial_received_lcp_confreq(device):
    """Unconfigure ``vpdn l2tp attribute initial-received-lcp-confreq``."""

    cli = ["no vpdn l2tp attribute initial-received-lcp-confreq"]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure vpdn l2tp attribute "
            "initial-received-lcp-confreq. Error:\n{error}".format(error=e)
        )


def configure_vpdn_l2tp_attribute_physical_channel_id(device):
    """Configure ``vpdn l2tp attribute physical-channel-id``."""

    cli = ["vpdn l2tp attribute physical-channel-id"]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure vpdn l2tp attribute physical-channel-id. "
            "Error:\n{error}".format(error=e)
        )


def unconfigure_vpdn_l2tp_attribute_physical_channel_id(device):
    """Unconfigure ``vpdn l2tp attribute physical-channel-id``."""

    cli = ["no vpdn l2tp attribute physical-channel-id"]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure vpdn l2tp attribute physical-channel-id. "
            "Error:\n{error}".format(error=e)
        )
