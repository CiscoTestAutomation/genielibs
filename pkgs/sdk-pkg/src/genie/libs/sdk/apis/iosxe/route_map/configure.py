"""Common configure functions for route-map"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_route_map_route_map(device, route_map):
    """ Configures route-map on device

        Args:
            device('obj'): device to configure on
            route_map('list'): route-map list which contains dictionary
                dictionary contains following 6 keys:
                    seq ('int'): sequence number
                    route_map ('str'): route-map name
                    prefix_list ('str'): prefix-list value
                    set_community ('str'): set community value
                    match_community ('str'): match community value
                    set_as_path ('str') : set as-path values
                ex.)
                    [
                    {
                        'seq': 10,
                        'route_map': 'community_test_out',
                        'match_community': 2
                    },
                    {
                        'seq': 10,
                        'route_map': 'community_test',
                        'set_community': '62000:1'
                    },
                    ]
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring route map
    """
    config = []

    # route-map community-test permit 10
    #  match ip address prefix-list 1
    #   set community 62000:1
    #  route-map community_test permit 20
    #   match ip address prefix-list 2
    #    set community 62000:2
    #  route-map community_test permit 30
    #  end

    for rm in route_map:

        config.append(
            "route-map {route_map} permit {seq}\n".format(
                route_map=rm["route_map"], seq=rm["seq"]
            )
        )

        if "prefix_list" in rm:
            config.append(
                "match ip address prefix-list {x}\n".format(
                    x=rm["prefix_list"]
                )
            )

        if "match_community" in rm:
            config.append(
                " match community {match_community}\n".format(
                    match_community=rm["match_community"]
                )
            )

        if "set_community" in rm:
            config.append(
                "set community {set_community}\n".format(
                    set_community=rm["set_community"]
                )
            )

        if "set_as_path" in rm:
            config.append(
                "set as-path {map_name} {as_path}".format(
                    map_name=rm["route_map"], as_path=rm["set_as_path"]
                )
            )

    try:
        device.configure("".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to execute configuration command")


def configure_route_map_permit(
        device, route_map, seq, prefix_list=None, set_community=None,
        match_community=None, set_metric=None, set_weight=None,
        set_as_path_prepend=None, local_preference=None,
        match_as_path=None, continue_id=None, match_interface=None):
    """ Configures route-map on device
        Args:
            device('obj'): device to configure on
            route_map('list'): route-map
            seq ('int'): sequence number
            prefix_list ('str'): prefix-list value
            match_interface ('str'): Interface that needs to be matched
            set_community ('int'): set community value
            match_community ('int'): match community value
            set_as_path ('int') : set as-path values
            set_metric ('int'): set metric value
            set_weight ('int'): set weight value
            set_as_path_prepend ('int'): set aspat prepend value
            local_preference ('int'): set local preference value
            match_as_path ('int'): set as path value
           continue_id ('int'): set continue id value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring route map
    """
    cmd = [f"route-map {route_map} permit {seq}"]
    if prefix_list:
        cmd.append(f"match ip address prefix-list {prefix_list}")
    if match_interface:
        cmd.append(f"match interface {match_interface}")
    if match_community:
        cmd.append(f"match community {match_community}")
    if set_community:
        cmd.append(f"set community {set_community}")
    if set_metric:
        cmd.append(f"set metric {set_metric}")
    if set_weight:
        cmd.append(f"set weight {set_weight}")
    if set_as_path_prepend:
        cmd.append(f"set as-path prepend {set_as_path_prepend}")
    if local_preference:
        cmd.append(f"set local-preference {local_preference}")
    if match_as_path:
        cmd.append(f"match as-path {match_as_path}")
    if continue_id:
        cmd.append(f"continue {continue_id}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to execute configuration command on device{device}. Error:\n{error}"
            .format(device=device, error=e))


def unconfigure_route_map_permit(
        device, route_map, seq, prefix_list=None, set_community=None,
        match_community=None, set_metric=None, set_weight=None,
        set_as_path_prepend=None, local_preference=None,
        match_as_path=None, continue_id=None):
    """ unconfigures route-map on device
        Args:
            device('obj'): device to configure on
            route_map('list'): route-map
            seq ('int'): sequence number
            prefix_list ('str'): prefix-list value
            set_community ('int'): set community value
            match_community ('int'): match community value
            set_as_path ('int') : set as-path values
            set_metric ('int'): set metric value
            set_weight ('int'): set weight value
            set_as_path_prepend ('int'): set aspat prepend value
            local_preference ('int'): set local preference value
            match_as_path ('int'): set as path value
           continue_id ('int'): set continue id value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfigure route map
    """
    cmd = [f"route-map {route_map} permit {seq}"]
    if prefix_list:
        cmd.append(f"no match ip address prefix-list {prefix_list}")
    if match_community:
        cmd.append(f"no match community {match_community}")
    if set_community:
        cmd.append(f"no set community {set_community}")
    if set_metric:
        cmd.append(f"no set metric {set_metric}")
    if set_weight:
        cmd.append(f"no set weight {set_weight}")
    if set_as_path_prepend:
        cmd.append(f"no set as-path prepend {set_as_path_prepend}")
    if local_preference:
        cmd.append(f"no set local-preference {local_preference}")
    if match_as_path:
        cmd.append(f"no match as-path {match_as_path}")
    if continue_id:
        cmd.append(f"no continue {continue_id}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure route_map on device{device}. Error:\n{error}"
            .format(device=device, error=e))


def configure_route_map_match_length(device, route_map, min_packet_length, max_packet_length):
    """ Configures route-map match length on device
        Args:
            device('obj'): device to configure on
            route_map('list'): route-map
            min_packet_length ('str'): minimum packet length
            max_packet_length ('str'): maximum packet length
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring route map
    """
    cmd = [f"route-map {route_map}", f"match length {min_packet_length} {max_packet_length}"]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute configuration command on device{device}. Error:\n{e}")

def configure_route_map_with_description(device, route_map_name, permit, description):

    """ configure route map

        Args:
            device ('obj'): device to execute on
            route_map_name ('int'): route map name
            permit ('int'): Sequence to insert to existing route-map entry
            description ('str'): Description about the route-map entry

        Return:
            None

        Raises:
            SubCommandFailure
    """
    # Build config string
    cmd = [f"route-map {route_map_name} permit {permit}"]

    cmd.append(f"description {description}")
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure route map {route_map_name}, Error: {error}"\
                .format(route_map_name=route_map_name, error=e
            )
        )

def route_map_unconfigure_description(device, route_map_name, permit, description):

    """ unconfigure route map description

        Args:
            device ('obj'): device to execute on
            route_map_name ('int'): route map name
            permit ('int'): Sequence to insert to existing route-map entry
            description ('str'): Description about the route-map entry

        Return:
            None

        Raises:
            SubCommandFailure
    """
    # Build config string
    cfg_str = [f"route-map {route_map_name} permit {permit}"]

    cfg_str.append(f"no description {description}")
    try:
        device.configure(cfg_str)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to un-configure route map {route_map_name} description, Error: {error}"\
                .format(route_map_name=route_map_name, error=e
            )
        )

def unconfigure_route_map(device, route_map_name):

    """ un configure route map

        Args:
            device ('obj'): device to execute on
            route_map_name ('int'): route map name

        Return:
            None

        Raises:
            SubCommandFailure
    """
    # Build config string
    cfg_str = [f"no route-map {route_map_name}"]

    try:
        device.configure(cfg_str)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to un-configure route map {route_map_name}, Error: {error}"\
                .format(route_map_name=route_map_name, error=e
            )
        )


