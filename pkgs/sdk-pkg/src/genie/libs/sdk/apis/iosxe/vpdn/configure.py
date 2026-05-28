"""Common configure functions for VPDN."""

import logging
import re

from genie.utils import Dq
from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.vpdn.utils import _resolve_local_names

log = logging.getLogger(__name__)

_DEFAULT = object()


def _has_running_config_line(device, config_line):
    """Return True when the exact global config line exists in running-config.

    Args:
        device ('obj'): Device object
        config_line ('str'): Configuration line to search for

    Returns:
        bool: True if the exact config line exists, otherwise False

    Raises:
        SubCommandFailure: Failed to retrieve running-config
    """

    exact_config_line = r"^{config_line}$".format(
        config_line=re.escape(config_line)
    )

    try:
        config_dict = device.api.get_running_config_dict()
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to check running-config for '{config_line}' on {device}. "
            "Error:\n{error}".format(
                config_line=config_line,
                device=getattr(device, "name", device),
                error=e,
            )
        ) from e

    matched_config = Dq(config_dict).contains(
        exact_config_line,
        regex=True,
    ).reconstruct()

    return bool(matched_config and config_line in matched_config)


def _get_vpdn_group_section(device, vpdn_group_number):
    """Return the parsed running-config section for a VPDN group.

    Args:
        device ('obj'): Device object
        vpdn_group_number ('str'): VPDN group name or number

    Returns:
        dict: Parsed running-config section for the VPDN group

    Raises:
        SubCommandFailure: Failed to retrieve running-config
    """

    group_key = "vpdn-group {group}".format(group=vpdn_group_number)
    exact_group_key = r"^{group_key}$".format(group_key=re.escape(group_key))

    try:
        config_dict = device.api.get_running_config_dict()
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to get running-config section for vpdn-group "
            "{vpdn_group_number} on {device}. Error:\n{error}".format(
                vpdn_group_number=vpdn_group_number,
                device=getattr(device, "name", device),
                error=e,
            )
        ) from e

    group_section = Dq(config_dict).contains(
        exact_group_key,
        regex=True,
    ).reconstruct()

    if not group_section:
        return {}

    return group_section.get(group_key, {})


def _has_vpdn_group_config_line(device, vpdn_group_number, config_line):
    """Return True when the exact submode config line exists under a VPDN group.

    Args:
        device ('obj'): Device object
        vpdn_group_number ('str'): VPDN group name or number
        config_line ('str'): Submode configuration line to search for

    Returns:
        bool: True if the exact config line exists under the group, otherwise False

    Raises:
        SubCommandFailure: Failed to retrieve running-config
    """

    group_section = _get_vpdn_group_section(device, vpdn_group_number)

    return bool(
        Dq(group_section).contains(
            r"^{config_line}$".format(config_line=re.escape(config_line)),
            regex=True,
        ).reconstruct()
    )


def _build_initiate_to_commands(initiate_to=None, initiate_to_entries=None):
    """Build ``initiate-to ip`` commands from supported entry formats.

    Args:
        initiate_to ('str', optional): Single initiate-to IP address
        initiate_to_entries ('list', optional): Additional initiate-to entries.
            Each item can be a string IP, ``(ip, priority)``, or
            ``{'ip': ip, 'priority': priority}``

    Returns:
        list: Formatted ``initiate-to ip`` commands

    Raises:
        ValueError: An initiate-to entry does not include an IP address
    """

    commands = []
    entries = []

    if initiate_to:
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
            raise ValueError("Each initiate-to entry must include an IP address")

        command = "initiate-to ip {ip}".format(ip=ip_address)
        if priority is not None:
            command += " priority {priority}".format(priority=priority)
        commands.append(command)

    return commands


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
            cli.extend(
                _build_initiate_to_commands(
                    initiate_to=initiate_to,
                    initiate_to_entries=initiate_to_entries,
                )
            )

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
    """Unconfigure VPDN group.

    Args:
        device ('obj'): Device object
        vpdn_group_number ('str'): VPDN group name or number

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to unconfigure VPDN group
    """

    cli = ["no vpdn-group {group}".format(group=vpdn_group_number)]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure the vpdn group. Error:\n{error}".format(error=e)
        )


def configure_vpdn_l2tp_attribute_initial_received_lcp_confreq(device):
    """Configure ``vpdn l2tp attribute initial-received-lcp-confreq``.

    Args:
        device ('obj'): Device object

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to configure the VPDN L2TP attribute
    """

    cli = ["vpdn l2tp attribute initial-received-lcp-confreq"]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure vpdn l2tp attribute "
            "initial-received-lcp-confreq. Error:\n{error}".format(error=e)
        )


def configure_vpdn_group_local_name(
    device, vpdn_group_number, local_name, check_existing=True
):
    """Configure ``local name`` under a VPDN group.

    Args:
        device ('obj'): Device object
        vpdn_group_number ('str'): VPDN group name or number
        local_name ('str'): Local name to configure
        check_existing ('bool', optional): When True, skip configuration if
            the exact line already exists

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to configure local name or retrieve
            running-config
    """

    cli = "local name {local_name}".format(local_name=local_name)

    if check_existing and _has_vpdn_group_config_line(device, vpdn_group_number, cli):
        log.info(
            "%s is already configured under vpdn-group %s on %s",
            cli,
            vpdn_group_number,
            device.name,
        )
        return

    try:
        device.configure(
            ["vpdn-group {group}".format(group=vpdn_group_number), cli]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure local name under vpdn-group "
            "{vpdn_group_number} on {device}. Error:\n{error}".format(
                vpdn_group_number=vpdn_group_number,
                device=getattr(device, "name", device),
                error=e,
            )
        ) from e


def configure_vpdn_group_l2tp_tunnel_busy_timeout(
    device, vpdn_group_number, busy_timeout, check_existing=True
):
    """Configure ``l2tp tunnel busy timeout`` under a VPDN group.

    Args:
        device ('obj'): Device object
        vpdn_group_number ('str'): VPDN group name or number
        busy_timeout ('str'): Busy timeout value to configure
        check_existing ('bool', optional): When True, skip configuration if
            the exact line already exists

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to configure busy timeout or retrieve
            running-config
    """

    cli = "l2tp tunnel busy timeout {timeout}".format(timeout=busy_timeout)

    if check_existing and _has_vpdn_group_config_line(device, vpdn_group_number, cli):
        log.info(
            "%s is already configured under vpdn-group %s on %s",
            cli,
            vpdn_group_number,
            device.name,
        )
        return

    try:
        device.configure(
            ["vpdn-group {group}".format(group=vpdn_group_number), cli]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure l2tp tunnel busy timeout under vpdn-group "
            "{vpdn_group_number} on {device}. Error:\n{error}".format(
                vpdn_group_number=vpdn_group_number,
                device=getattr(device, "name", device),
                error=e,
            )
        ) from e


def unconfigure_vpdn_group_l2tp_tunnel_busy_timeout(
    device, vpdn_group_number, busy_timeout, check_existing=True
):
    """Unconfigure ``l2tp tunnel busy timeout`` under a VPDN group.

    Args:
        device ('obj'): Device object
        vpdn_group_number ('str'): VPDN group name or number
        busy_timeout ('str'): Busy timeout value to unconfigure
        check_existing ('bool', optional): When True, skip unconfiguration if
            the exact line is not present

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to unconfigure busy timeout or retrieve
            running-config
    """

    cli = "l2tp tunnel busy timeout {timeout}".format(timeout=busy_timeout)

    if check_existing and not _has_vpdn_group_config_line(
        device, vpdn_group_number, cli
    ):
        log.info(
            "%s is not configured under vpdn-group %s on %s",
            cli,
            vpdn_group_number,
            device.name,
        )
        return

    try:
        device.configure(
            [
                "vpdn-group {group}".format(group=vpdn_group_number),
                "no {cli}".format(cli=cli),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure l2tp tunnel busy timeout under vpdn-group "
            "{vpdn_group_number} on {device}. Error:\n{error}".format(
                vpdn_group_number=vpdn_group_number,
                device=getattr(device, "name", device),
                error=e,
            )
        ) from e


def configure_vpdn_logging_dead_cache(device, check_existing=True):
    """Configure global VPDN dead-cache logging.

    Args:
        device ('obj'): Device object
        check_existing ('bool', optional): When True, skip configuration if
            the exact line already exists

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to configure VPDN dead-cache logging or
            retrieve running-config
    """

    cli = "vpdn logging dead-cache"

    if check_existing and _has_running_config_line(device, cli):
        log.info(
            "%s is already configured on %s",
            cli,
            device.name,
        )
        return

    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure VPDN dead-cache logging on {device}. "
            "Error:\n{error}".format(
                device=getattr(device, "name", device),
                error=e,
            )
        ) from e


def unconfigure_vpdn_logging_dead_cache(device, check_existing=True):
    """Unconfigure global VPDN dead-cache logging.

    Args:
        device ('obj'): Device object
        check_existing ('bool', optional): When True, skip unconfiguration if
            the exact line is not present

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to unconfigure VPDN dead-cache logging or
            retrieve running-config
    """

    cli = "vpdn logging dead-cache"

    if check_existing and not _has_running_config_line(device, cli):
        log.info(
            "%s is not configured on %s",
            cli,
            device.name,
        )
        return

    try:
        device.configure("no {cli}".format(cli=cli))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure VPDN dead-cache logging on {device}. "
            "Error:\n{error}".format(
                device=getattr(device, "name", device),
                error=e,
            )
        ) from e


def configure_vpdn_session_limit(device, session_limit, check_existing=True):
    """Configure the global VPDN session limit.

    Args:
        device ('obj'): Device object
        session_limit ('str'): Global VPDN session limit
        check_existing ('bool', optional): When True, skip configuration if
            the exact line already exists

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to configure global session limit or retrieve
            running-config
    """

    cli = "vpdn session-limit {session_limit}".format(session_limit=session_limit)

    if check_existing and _has_running_config_line(device, cli):
        log.info(
            "%s is already configured on %s",
            cli,
            device.name,
        )
        return

    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure global VPDN session-limit on {device}. "
            "Error:\n{error}".format(
                device=getattr(device, "name", device),
                error=e,
            )
        ) from e


def unconfigure_vpdn_session_limit(device, session_limit, check_existing=True):
    """Unconfigure the global VPDN session limit.

    Args:
        device ('obj'): Device object
        session_limit ('str'): Global VPDN session limit
        check_existing ('bool', optional): When True, skip unconfiguration if
            the exact line is not present

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to unconfigure global session limit or
            retrieve running-config
    """

    cli = "vpdn session-limit {session_limit}".format(session_limit=session_limit)

    if check_existing and not _has_running_config_line(device, cli):
        log.info(
            "%s is not configured on %s",
            cli,
            device.name,
        )
        return

    try:
        device.configure("no {cli}".format(cli=cli))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure global VPDN session-limit on {device}. "
            "Error:\n{error}".format(
                device=getattr(device, "name", device),
                error=e,
            )
        ) from e


def configure_vpdn_group_session_limit(
    device, vpdn_group_number, session_limit, check_existing=True
):
    """Configure a per-group VPDN session limit under vpdn-group.

    Args:
        device ('obj'): Device object
        vpdn_group_number ('str'): VPDN group name or number
        session_limit ('str'): Per-group VPDN session limit
        check_existing ('bool', optional): When True, skip configuration if
            the exact line already exists

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to configure per-group session limit or
            retrieve running-config
    """

    cli = "session-limit {session_limit}".format(session_limit=session_limit)

    if check_existing and _has_vpdn_group_config_line(device, vpdn_group_number, cli):
        log.info(
            "%s is already configured under vpdn-group %s on %s",
            cli,
            vpdn_group_number,
            device.name,
        )
        return

    try:
        device.configure(
            ["vpdn-group {group}".format(group=vpdn_group_number), cli]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure vpdn-group {vpdn_group_number} session-limit "
            "on {device}. Error:\n{error}".format(
                vpdn_group_number=vpdn_group_number,
                device=getattr(device, "name", device),
                error=e,
            )
        ) from e


def unconfigure_vpdn_group_session_limit(
    device, vpdn_group_number, session_limit, check_existing=True
):
    """Unconfigure a per-group VPDN session limit under vpdn-group.

    Args:
        device ('obj'): Device object
        vpdn_group_number ('str'): VPDN group name or number
        session_limit ('str'): Per-group VPDN session limit
        check_existing ('bool', optional): When True, skip unconfiguration if
            the exact line is not present

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to unconfigure per-group session limit or
            retrieve running-config
    """

    cli = "session-limit {session_limit}".format(session_limit=session_limit)

    if check_existing and not _has_vpdn_group_config_line(
        device, vpdn_group_number, cli
    ):
        log.info(
            "%s is not configured under vpdn-group %s on %s",
            cli,
            vpdn_group_number,
            device.name,
        )
        return

    try:
        device.configure(
            [
                "vpdn-group {group}".format(group=vpdn_group_number),
                "no {cli}".format(cli=cli),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure vpdn-group {vpdn_group_number} session-limit "
            "on {device}. Error:\n{error}".format(
                vpdn_group_number=vpdn_group_number,
                device=getattr(device, "name", device),
                error=e,
            )
        ) from e


def unconfigure_vpdn_group_initiate_to_entries(
    device,
    vpdn_group_number,
    initiate_to_entries,
):
    """Unconfigure one or more ``initiate-to ip`` entries under a VPDN group.

    Args:
        device ('obj'): Device object
        vpdn_group_number ('str'): VPDN group name or number
        initiate_to_entries ('list'): Initiate-to entries to unconfigure. Each
            item can be a string IP, ``(ip, priority)``, or
            ``{'ip': ip, 'priority': priority}``

    Returns:
        None

    Raises:
        ValueError: An initiate-to entry does not include an IP address
        SubCommandFailure: Failed to unconfigure initiate-to entries
    """

    cli = ["vpdn-group {group}".format(group=vpdn_group_number)]

    for command in _build_initiate_to_commands(
        initiate_to_entries=initiate_to_entries
    ):
        cli.append("no {command}".format(command=command))

    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure initiate-to ip entries under the vpdn group. "
            "Error:\n{error}".format(error=e)
        )


def unconfigure_vpdn_l2tp_attribute_initial_received_lcp_confreq(device):
    """Unconfigure ``vpdn l2tp attribute initial-received-lcp-confreq``.

    Args:
        device ('obj'): Device object

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to unconfigure the VPDN L2TP attribute
    """

    cli = ["no vpdn l2tp attribute initial-received-lcp-confreq"]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure vpdn l2tp attribute "
            "initial-received-lcp-confreq. Error:\n{error}".format(error=e)
        )


def configure_vpdn_l2tp_attribute_physical_channel_id(device):
    """Configure ``vpdn l2tp attribute physical-channel-id``.

    Args:
        device ('obj'): Device object

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to configure the VPDN L2TP attribute
    """

    cli = ["vpdn l2tp attribute physical-channel-id"]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure vpdn l2tp attribute physical-channel-id. "
            "Error:\n{error}".format(error=e)
        )


def unconfigure_vpdn_l2tp_attribute_physical_channel_id(device):
    """Unconfigure ``vpdn l2tp attribute physical-channel-id``.

    Args:
        device ('obj'): Device object

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to unconfigure the VPDN L2TP attribute
    """

    cli = ["no vpdn l2tp attribute physical-channel-id"]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure vpdn l2tp attribute physical-channel-id. "
            "Error:\n{error}".format(error=e)
        )
