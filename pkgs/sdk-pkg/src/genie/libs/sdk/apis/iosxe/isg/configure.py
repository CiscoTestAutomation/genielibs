"""Common configure functions for ISG"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_class_map_type_traffic(device, class_name, match_type='match-any',
                                     access_groups=None):
    """ Configure class-map type traffic on device

        Args:
            device (`obj`): Device object
            class_name (`str`): Class-map name
            match_type (`str`, optional): Match type (e.g. 'match-any', 'match-all').
                Defaults to 'match-any'
            access_groups (`list`, optional): List of dicts with keys:
                - direction (`str`): 'input' or 'output'
                - name (`str`): Access-group name
                Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"class-map type traffic {match_type} {class_name}"]
    if access_groups:
        for ag in access_groups:
            cmd.append(f" match access-group {ag['direction']} name {ag['name']}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure class-map type traffic {class_name}. Error: {e}"
        )


def unconfigure_class_map_type_traffic(device, class_name, match_type='match-any'):
    """ Unconfigure class-map type traffic on device

        Args:
            device (`obj`): Device object
            class_name (`str`): Class-map name
            match_type (`str`, optional): Match type (e.g. 'match-any', 'match-all').
                Defaults to 'match-any'
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"no class-map type traffic {match_type} {class_name}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure class-map type traffic {class_name}. Error: {e}"
        )


def configure_redirect_server_group(device, group_name, servers=None):
    """ Configure redirect server-group on device

        Args:
            device (`obj`): Device object
            group_name (`str`): Server group name
            servers (`list`, optional): List of dicts with keys:
                - ip (`str`): Server IP address
                - port (`int`): Server port number
                Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"redirect server-group {group_name}"]
    if servers:
        for server in servers:
            cmd.append(f" server ip {server['ip']} port {server['port']}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure redirect server-group {group_name}. Error: {e}"
        )


def unconfigure_redirect_server_group(device, group_name):
    """ Unconfigure redirect server-group on device

        Args:
            device (`obj`): Device object
            group_name (`str`): Server group name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"no redirect server-group {group_name}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure redirect server-group {group_name}. Error: {e}"
        )


def configure_policy_map_type_service_isg(device, name, classes=None):
    """ Configure ISG policy-map type service on device

        Args:
            device (`obj`): Device object
            name (`str`): Policy-map name
            classes (`list`, optional): List of dicts with keys:
                - class_name (`str`): Traffic class name
                - sub_commands (`list`): List of sub-command strings
                    (e.g. ['accounting aaa list acct1', 'timeout idle 75'])
                Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"policy-map type service {name}"]
    if classes:
        if not isinstance(classes, list):
            raise SubCommandFailure(
                f"'classes' must be a list, got {type(classes).__name__}"
            )
        for cls in classes:
            cmd.append(f" class type traffic {cls['class_name']}")
            for sub in cls.get('sub_commands', []):
                cmd.append(f"  {sub}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure policy-map type service {name}. Error: {e}"
        )


def unconfigure_policy_map_type_service_isg(device, name):
    """ Unconfigure ISG policy-map type service on device

        Args:
            device (`obj`): Device object
            name (`str`): Policy-map name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"no policy-map type service {name}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure policy-map type service {name}. Error: {e}"
        )


def configure_policy_map_type_control(device, name, classes=None,
                                      error_pattern=None):
    """ Configure ISG policy-map type control on device

        Args:
            device (`obj`): Device object
            name (`str`): Policy-map name
            classes (`list`, optional): List of dicts with keys:
                - event (`str`): Event type
                    (e.g. 'session-start', 'session-restart', 'account-logon')
                - class_name (`str`, optional): class-map predicate name;
                    defaults to 'always' when omitted (e.g. 'ISG-IP-UNAUTH'
                    to render 'class type control ISG-IP-UNAUTH event ...')
                - actions (`list`): List of action strings with sequence numbers
                    (e.g. ['10 authorize identifier mac-address',
                           '20 service-policy type service name GOLD'])
                Defaults to None
            error_pattern (`list`, optional): Custom error patterns to pass to
                device.configure(). Use [] to suppress expected errors.
                Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"policy-map type control {name}"]
    if classes:
        if not isinstance(classes, list):
            raise SubCommandFailure(
                f"'classes' must be a list, got {type(classes).__name__}"
            )
        for cls in classes:
            class_name = cls.get('class_name', 'always')
            cmd.append(
                f" class type control {class_name} event {cls['event']}"
            )
            for action in cls.get('actions', []):
                cmd.append(f"  {action}")
    kwargs = {}
    if error_pattern is not None:
        kwargs['error_pattern'] = error_pattern
    try:
        device.configure(cmd, **kwargs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure policy-map type control {name}. Error: {e}"
        )


def unconfigure_policy_map_type_control(device, name):
    """ Unconfigure ISG policy-map type control on device

        Args:
            device (`obj`): Device object
            name (`str`): Policy-map name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"no policy-map type control {name}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure policy-map type control {name}. Error: {e}"
        )


def configure_ip_portbundle(device, length=None, source=None):
    """ Configure global ip portbundle on device

        Args:
            device (`obj`): Device object
            length (`int` or `str`, optional): Port-bundle length.
                Defaults to None
            source (`str`, optional): Source interface (e.g. 'Loopback3').
                Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = ["ip portbundle"]
    if length is not None:
        cmd.append(f"length {length}")
    if source is not None:
        cmd.append(f"source {source}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip portbundle on device "
            f"{device.name}. Error: {e}"
        )


def unconfigure_ip_portbundle(device):
    """ Unconfigure global ip portbundle on device

        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no ip portbundle")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip portbundle on device "
            f"{device.name}. Error: {e}"
        )


def configure_policy_map_type_service_default_l4r_redirect(
        device,
        policy_map_name='DEFAULT_L4R_REDIRECT_SERVICE',
        class_name='DEFAULT_L4R_REDIRECT_TC',
        group_name='DEFAULT_L4R_REDIRECT_GROUP',
        sequence=15):
    """ Configure ISG default L4R redirect service policy-map

        Args:
            device (`obj`): Device object
            policy_map_name (`str`, optional): Policy-map name.
                Defaults to 'DEFAULT_L4R_REDIRECT_SERVICE'
            class_name (`str`, optional): Traffic class-map name.
                Defaults to 'DEFAULT_L4R_REDIRECT_TC'
            group_name (`str`, optional): Redirect server-group name.
                Defaults to 'DEFAULT_L4R_REDIRECT_GROUP'
            sequence (`int` or `str`, optional): Class sequence.
                Defaults to 15
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"policy-map type service {policy_map_name}",
        f" {sequence} class type traffic {class_name}",
        f"  redirect to group {group_name}",
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure default L4R redirect service policy-map "
            f"{policy_map_name}. Error: {e}"
        )


def configure_policy_map_type_service_smtp_redirect(
        device,
        policy_map_name='SMTP_REDIRECT_SERVICE',
        class_name='SMTP_REDIRECT_TC',
        group_name='SMTP_REDIRECT_GROUP',
        sequence=15):
    """ Configure ISG SMTP redirect service policy-map

        Args:
            device (`obj`): Device object
            policy_map_name (`str`, optional): Policy-map name.
                Defaults to 'SMTP_REDIRECT_SERVICE'
            class_name (`str`, optional): Traffic class-map name.
                Defaults to 'SMTP_REDIRECT_TC'
            group_name (`str`, optional): Redirect server-group name.
                Defaults to 'SMTP_REDIRECT_GROUP'
            sequence (`int` or `str`, optional): Class sequence.
                Defaults to 15
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"policy-map type service {policy_map_name}",
        f" {sequence} class type traffic {class_name}",
        f"  redirect to group {group_name}",
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure SMTP redirect service policy-map "
            f"{policy_map_name}. Error: {e}"
        )


def configure_class_map_type_control_isg(device, class_name,
                                         match_type='match-all',
                                         matches=None):
    """ Configure ISG class-map type control on device

        Args:
            device (`obj`): Device object
            class_name (`str`): Class-map name
            match_type (`str`, optional): Match type. Defaults to 'match-all'
            matches (`list`, optional): Match commands without indentation.
                For example:
                    ['match vlan 130', 'match vlan 140']
                    ['match service-name DEFAULT_L4R_REDIRECT_SERVICE']
                    ['available remote-id',
                     'match not remote-id unauthenticated']
                Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"class-map type control {match_type} {class_name}"]
    if matches:
        for match in matches:
            cmd.append(f" {str(match).strip()}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ISG class-map type control "
            f"{class_name}. Error: {e}"
        )


def configure_redirect_server_group_without_port(device, group_name,
                                                 ip_address):
    """ Configure redirect server-group with server IP and no port

        Args:
            device (`obj`): Device object
            group_name (`str`): Server group name
            ip_address (`str`): Server IP address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"redirect server-group {group_name}",
        f" server ip {ip_address}",
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure redirect server-group {group_name} "
            f"without port. Error: {e}"
        )


def configure_policy_map_type_service_secure_dhcp_class(
        device,
        policy_map_name='SECURE_DHCP_CLASS',
        classname='orange_secure'):
    """ Configure ISG secure DHCP class service policy-map

        Args:
            device (`obj`): Device object
            policy_map_name (`str`, optional): Policy-map name.
                Defaults to 'SECURE_DHCP_CLASS'
            classname (`str`, optional): Classname value.
                Defaults to 'orange_secure'
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"policy-map type service {policy_map_name}",
        f" classname {classname}",
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure secure DHCP service policy-map "
            f"{policy_map_name}. Error: {e}"
        )


def configure_policy_map_type_service_opengarden(
        device,
        policy_map_name='OPENGARDEN_SERVICE',
        class_name='OPENGARDEN_TC',
        sequence=10,
        default_direction='input'):
    """ Configure ISG opengarden service policy-map

        Args:
            device (`obj`): Device object
            policy_map_name (`str`, optional): Policy-map name.
                Defaults to 'OPENGARDEN_SERVICE'
            class_name (`str`, optional): Traffic class-map name.
                Defaults to 'OPENGARDEN_TC'
            sequence (`int` or `str`, optional): Class sequence.
                Defaults to 10
            default_direction (`str`, optional): Default class direction.
                Defaults to 'input'
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"policy-map type service {policy_map_name}",
        f" {sequence} class type traffic {class_name}",
        f" class type traffic default {default_direction}",
        "  drop",
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure opengarden service policy-map "
            f"{policy_map_name}. Error: {e}"
        )


def configure_policy_map_type_service_https_l4r_redirect(
        device,
        policy_map_name='HTTPS_L4R_REDIRECT_SERVICE',
        class_name='HTTPS_L4R_REDIRECT_TC',
        group_name='HTTPS_L4R_REDIRECT_GROUP',
        sequence=25):
    """ Configure ISG HTTPS L4R redirect service policy-map

        Args:
            device (`obj`): Device object
            policy_map_name (`str`, optional): Policy-map name.
                Defaults to 'HTTPS_L4R_REDIRECT_SERVICE'
            class_name (`str`, optional): Traffic class-map name.
                Defaults to 'HTTPS_L4R_REDIRECT_TC'
            group_name (`str`, optional): Redirect server-group name.
                Defaults to 'HTTPS_L4R_REDIRECT_GROUP'
            sequence (`int` or `str`, optional): Class sequence.
                Defaults to 25
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"policy-map type service {policy_map_name}",
        f" {sequence} class type traffic {class_name}",
        f"  redirect to group {group_name}",
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure HTTPS L4R redirect service policy-map "
            f"{policy_map_name}. Error: {e}"
        )


def configure_policy_map_type_service_web_proxy_redirect(
        device,
        policy_map_name='WEB_PROXY_REDIRECT_SERVICE',
        class_name='WEB_PROXY_REDIRECT_TC',
        group_name='WEB_PROXY_REDIRECT_GROUP',
        sequence=10):
    """ Configure ISG web proxy redirect service policy-map

        Args:
            device (`obj`): Device object
            policy_map_name (`str`, optional): Policy-map name.
                Defaults to 'WEB_PROXY_REDIRECT_SERVICE'
            class_name (`str`, optional): Traffic class-map name.
                Defaults to 'WEB_PROXY_REDIRECT_TC'
            group_name (`str`, optional): Redirect server-group name.
                Defaults to 'WEB_PROXY_REDIRECT_GROUP'
            sequence (`int` or `str`, optional): Class sequence.
                Defaults to 10
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"policy-map type service {policy_map_name}",
        f" {sequence} class type traffic {class_name}",
        f"  redirect to group {group_name}",
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure web proxy redirect service policy-map "
            f"{policy_map_name}. Error: {e}"
        )


def configure_policy_map_type_service_arp_keepalive(
        device,
        policy_map_name='ARP_KEEPALIVE',
        idle=35,
        attempts=10,
        interval=20,
        protocol='ARP'):
    """ Configure ISG ARP keepalive service policy-map

        Args:
            device (`obj`): Device object
            policy_map_name (`str`, optional): Policy-map name.
                Defaults to 'ARP_KEEPALIVE'
            idle (`int` or `str`, optional): Idle value. Defaults to 35
            attempts (`int` or `str`, optional): Attempts value.
                Defaults to 10
            interval (`int` or `str`, optional): Interval value.
                Defaults to 20
            protocol (`str`, optional): Keepalive protocol. Defaults to 'ARP'
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"policy-map type service {policy_map_name}",
        (
            f" keepalive idle {idle} attempts {attempts} interval "
            f"{interval} protocol {protocol}"
        ),
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ARP keepalive service policy-map "
            f"{policy_map_name}. Error: {e}"
        )
