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
            cmd.append(f" class type control always event {cls['event']}")
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
