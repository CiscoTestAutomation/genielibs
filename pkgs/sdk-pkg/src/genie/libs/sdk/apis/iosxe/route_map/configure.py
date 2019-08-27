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
