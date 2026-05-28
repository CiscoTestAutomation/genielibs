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
