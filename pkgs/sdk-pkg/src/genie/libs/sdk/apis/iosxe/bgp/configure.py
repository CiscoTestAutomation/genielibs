"""Common configure functions for bgp"""

# Python
import logging
import re
import jinja2

# Genie
from genie.utils.timeout import Timeout

# Utils
from genie.libs.sdk.apis.iosxe.running_config.get import (
    get_running_config_section_dict,
)

# Steps
from pyats.aetest.steps import Steps

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_bgp_import_path_selection(
    device, bgp_as, address_family, vrf, selection_type
):
    """ Configures import path selection on BGP router
        Args:
            device('obj'): device to configure
            bgp_as('str'): bgp id
            address_family:('str'): address family
            vrf('str'): vrf name
            type('str'): type of selection to configure
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info('Configuring "import path selection {}"'.format(selection_type))
    try:
        device.configure(
            "router bgp {bgp_as}\n"
            "address-family {address_family} vrf {vrf}\n"
            "import path selection {selection_type}".format(
                bgp_as=bgp_as,
                address_family=address_family,
                vrf=vrf,
                selection_type=selection_type,
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure import path selection on BGP router {bgp_as}".format(
                bgp_as=bgp_as
            )
        )


def configure_bgp_router_id(device, bgp_as, router_id):
    """ Configures router-id on BGP router

        Args:
            device('obj'): device to configure on
            bgp_as('str'): bgp_as to configure
            router_id('str'): router_id of device
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """

    log.info(
        "Configuring router BGP on {hostname}\n"
        "    -local AS number: {bgp_as}\n"
        "    -bgp router-id: {router_id}".format(
            hostname=device.hostname, bgp_as=bgp_as, router_id=router_id
        )
    )

    try:
        device.configure(
            "router bgp {bgp_as}\n"
            "bgp router-id {router_id}\n".format(
                bgp_as=bgp_as, router_id=router_id
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure router-id {router_id} on "
            "BGP router {bgp_as}".format(router_id=router_id, bgp_as=bgp_as)
        )


def configure_bgp_neighbor(
    device,
    bgp_as,
    neighbor_as,
    neighbor_address,
    source_interface=None,
    ebgp=None,
):
    """ Configures bgp neighbor on bgp router

        Args:
            device('obj'): device to configure on
            bgp_as('str'): bgp_as to configure
            neighbor_as('str'): neighbor_as to configure
            neighbor_address('str'): address of neighbor
            source_interface('str'): used to configure update-source on neighbor
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log_msg = (
        "Configuring BGP on {hostname}\n"
        "    -local AS number: {bgp_as}\n"
        "    -remote AS number: {neighbor_as}\n"
        "    -neighbor: {neighbor_address}".format(
            hostname=device.hostname,
            bgp_as=bgp_as,
            neighbor_as=neighbor_as,
            neighbor_address=neighbor_address,
        )
    )

    cmd = (
        "router bgp {bgp_as}\n"
        "neighbor {neighbor_address} remote-as {neighbor_as}".format(
            bgp_as=bgp_as,
            neighbor_as=neighbor_as,
            neighbor_address=neighbor_address,
        )
    )

    if source_interface:
        log_msg += "\n    -update-source: {}".format(source_interface)
        cmd += "\nneighbor {neighbor_address} update-source {source_interface}".format(
            neighbor_address=neighbor_address,
            source_interface=source_interface,
        )

    if ebgp:
        log_msg += "\n    -ebgp-multihop: {}".format(ebgp)
        cmd += "\nneighbor {neighbor_address} ebgp-multihop {ebgp}".format(
            neighbor_address=neighbor_address, ebgp=ebgp
        )

    log.info(log_msg)
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Coult not configure bgp neighbor {neighbor_as} "
            "on router {bgp_as}".format(neighbor_as=neighbor_as, bgp_as=bgp_as)
        )


def configure_bgp_soo_on_inbound_from_neighbor(
    device, soo_rt, bgp_as, vrf, neighbor_address
):
    """ Configures extended community SoO on inbound from neighbor using soo_rt

        Args:
            device('obj'): device to execute on
            soo_rt('str'): route to configure SoO with
            bgp_as('str'): what router bgp to configure on
            vrf('str'): what vrf to configure on
            neighbor_address('str'): what neighbor to configure on
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands

    """
    log.info(
        "Configuring extended community SoO with {} value on the "
        "inbound from {}".format(soo_rt, neighbor_address)
    )
    try:
        device.configure(
            "route-map setsoo permit 10\n"
            "set extcommunity soo {}".format(soo_rt)
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure extended community SoO {}".format(soo_rt)
        )
    try:
        device.configure(
            "router bgp {}\n"
            "address-family ipv4 vrf {}\n"
            "neighbor {} route-map "
            "setsoo in".format(bgp_as, vrf, neighbor_address)
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure SoO in from neighbor {}".format(
                neighbor_address
            )
        )


def configure_prefix_list_prefix_list_to_bgp_neighbor(
    device, bgp_as, address_family, vrf, prefix_list=None
):
    """ Configure prefix list to bgp neighbor

        Args:
            device ('obj'): Device object
            bgp_as (str): bgp AS number
            vrf ('str'): vrf name
            address_family ('str'): address family
            prefix_list ('list'): A list of dictionaries following below format:
                [{
                    'neighbor': neighbor address,
                    'prefix_list': prefix,
                    'direction': direction
                }]
            ex.) 
                [
                    {
                        'neighbor': '192.168.1.4',
                        'prefix_list': 'in'
                        'direction': 'in'
                    },
                    {
                        'neighbor': '192.168.1.5',
                        'prefix_list': 'out'
                        'direction': 'out'
                    }
                ]
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
            TypeError: prefix_list is not a list
    """
    config = []

    config.append("router bgp {bgp_as}".format(bgp_as=bgp_as))

    config.append(
        "\naddress-family {address_family} vrf {vrf}".format(
            address_family=address_family, vrf=vrf
        )
    )

    if not isinstance(prefix_list, list):
        raise TypeError("prefix_list must be a list")

    for pf in prefix_list:
        config.append(
            "\nneighbor {neighbor} prefix-list {prefix_list} {direction}".format(
                neighbor=pf["neighbor"],
                prefix_list=pf["prefix_list"],
                direction=pf["direction"],
            )
        )

    try:
        device.configure("".join(config))
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure prefix-liston router bgp "
            "{bgp_as}".format(bgp_as=bgp_as)
        )


def configure_maximum_prefix_to_bgp_neighbor(
    device, bgp_as, address_family, vrf, maximum_prefix=None
):
    """ Configure maximum prefix to router bgp neighbor

        Args:
            device ('obj'): Device object
            bgp_as (str): bgp AS number
            vrf ('str'): vrf name
            address_family ('str'): address family
            maximum_prefix ('list'): A list of dictionaries following below format:
                [{
                    'neighbor': neighbor address,
                    'maximum_prefix': maximum prefix number
                }]
            ex.) 
                [
                    {
                        'neighbor': '192.168.1.6,
                        'maximum_prefix': 5,
                    }
                ]
        Returns:
            None
        Raises:
            SubCommandFailure: Failed executing configure commands
            TypeError: maximum_prefix is not a list

    """
    config = []

    config.append("router bgp {bgp_as}".format(bgp_as=bgp_as))

    config.append(
        "\naddress-family {address_family} vrf {vrf}".format(
            address_family=address_family, vrf=vrf
        )
    )

    if not isinstance(maximum_prefix, list):
        raise ValueError("prefix_list must be a list")

    for pf in maximum_prefix:
        config.append(
            "\nneighbor {neighbor} maximum-prefix {maximum_prefix}".format(
                neighbor=pf["neighbor"], maximum_prefix=pf["maximum_prefix"]
            )
        )

    try:
        device.configure("".join(config))
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure maximum prefixes on bgp "
            "router {bgp_as}".format(bgp_as=bgp_as)
        )


def configure_route_map_route_map_to_bgp_neighbor(
    device,
    bgp_as,
    address_family="",
    route_map=None,
    vrf="",
    vrf_address_family="",
):
    """ Configure route map to bgp neighbors

        Args:
            device ('obj'): Device object
            bgp_as ('int'): BGP AS number
            address_family ('str'): address family
            vrf ('str'): vrf name
            vrf_address_family ('str'): address family for vrf
            route_map ('list'): route map list which contains dictionary
                dictionary contains following 5 keys:
                    neighbor ('str'): neighbor value
                    route_map ('str'): route-map name
                    direction ('str'): direction type
            ex.)
                [
                    {
                        'neighbor': '192.168.60.10',
                        'route_map': 'community_test_out',
                        'direction': 'out'
                    },
                    {
                        'neighbor': '192.168.60.11',
                        'route_map': 'community_test_out',
                        'direction': 'out'
                    },
                    {
                        'neighbor': '192.168.6.10',
                        'route_map': 'community_test_in',
                        'direction': 'in'
                    },
                ]
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
            TypeError: route_map is not a list
    """

    # router bgp 65109
    # address-family vpnv4
    # neighbor 192.168.36.119 route-map community_test_out out
    # neighbor 192.168.36.120 route-map community_test_out out
    # address-family ipv4 vrf
    # neighbor 192.168.10.253 route-map community_test_in in

    if route_map is None:
        route_map = []

    config = []
    config.append("router bgp {bgp_as}\n".format(bgp_as=bgp_as))

    if address_family:
        config.append(
            "address-family {address_family}\n".format(
                address_family=address_family
            )
        )

    if route_map:

        if not isinstance(route_map, list):
            raise TypeError("route_map must be a list")

        for routemap in route_map:
            direction = routemap["direction"]
            if direction == "in" and vrf and vrf_address_family:
                config.append(
                    "address-family {vrf_address_family} vrf {vrf}\n".format(
                        vrf_address_family=vrf_address_family, vrf=vrf
                    )
                )

            config.append(
                "neighbor {neighbor} route-map {route_map_name} {route_map_direction}\n".format(
                    neighbor=routemap["neighbor"],
                    route_map_name=routemap["route_map"],
                    route_map_direction=direction,
                )
            )
    try:
        device.configure("".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure route map to bgp neighbors"
        )


def configure_bgp_neighbor_activate(
    device, address_family, bgp_as, neighbor_address, steps=Steps()
):
    """ Activate bgp neighbor on bgp router 

        Args:
            device ('obj')             : Device to be configured
            bgp_as ('str')             : Bgp Id to be added to configuration
            neighbor_address ('str')   : Address of neighbor to be added to configuration
            address_family ('str')     : Address family to be configured
            steps('obj')               : Context manager steps
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
            
    """
    with steps.start(
        "Configure device {dev}".format(dev=device.name), continue_=True
    ) as step:

        try:
            device.configure(
                [
                    "router bgp {bgp_as}".format(bgp_as=bgp_as),
                    "address-family {address_family}".format(
                        address_family=address_family
                    ),
                    "neighbor {device_address} activate".format(
                        device_address=neighbor_address
                    ),
                ]
            )
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Could not ativate bgp neighbor on bgp "
                "router {bgp_as}".format(bgp_as=bgp_as)
            )


def configure_shut_bgp_neighbors(
    device, bgp_as, neighbors=None, address_family=None, vrf=None, noshut=False
):
    """ Configures shut/enable on bgp neighbors if provided otherwise the ones found in running config

        Args:
            device ('obj'): device under test
            bgp_as ('int'): router bgp_as to configure on
            address_family ('str'): address_family to configure under
            vrf ('str'): vrf to configure under
            neighbors ('list'): List of neighbors to shut/enable
            noshut ('bool'): does the opposite of shut if True
        Returns:        
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
            ValueError: Some information is missing

    """
    search = None
    if noshut:
        if neighbors:
            log.info("Enabling router bgp neighbors {}".format(neighbors))
        elif address_family and vrf:
            log.info(
                "Enabling router bgp neighbors under address_family {} and vrf {}".format(
                    address_family, vrf
                )
            )
            search = "address-family {} vrf {}".format(address_family, vrf)
        elif address_family:
            log.info(
                "Enabling router bgp neighbors under address_family {}".format(
                    address_family
                )
            )
            search = "address-family {}".format(address_family)
    else:
        if neighbors:
            log.info("Shutting down router bgp neighbors {}".format(neighbors))
        elif address_family and vrf:
            log.info(
                "Shutting down router bgp neighbors under address_family {} and vrf {}".format(
                    address_family, vrf
                )
            )
            search = "address-family {} vrf {}".format(address_family, vrf)
        elif address_family:
            log.info(
                "Shutting down router bgp neighbors under address_family {}".format(
                    address_family
                )
            )
            search = "address-family {}".format(address_family)

    p1_active_neighbor = re.compile(
        r"^neighbor +(?P<neighbor>[\d\.]+) +activate"
    )
    p2_shutdown_neighbor = re.compile(
        r"^neighbor +(?P<neighbor>[\d\.]+) +shutdown"
    )
    p3_neighbor = re.compile(r"^neighbor +(?P<neighbor>[\d\.]+)")
    cmd = "router bgp {}\n".format(bgp_as)

    if neighbors:
        if noshut:
            for neighbor in neighbors:
                cmd += "no neighbor {} shutdown".format(neighbor)
        else:
            for neighbor in neighbors:
                cmd += "neighbor {} shutdown".format(neighbor)
        try:
            device.configure(cmd)
        except SubCommandFailure:
            if noshut:
                raise SubCommandFailure("Could not enable bgp neighbors")
            else:
                raise SubCommandFailure("Could not shut bgp neighbors")

    else:
        already_shut = []
        config_dict = get_running_config_section_dict(
            device, "router bgp"
        )
        if config_dict:
            for sub_level in config_dict.get(
                "router bgp {}".format(bgp_as), {}
            ):

                # Following if/else block is used for neighbors under 'router bgp id' level
                if noshut:
                    m = p2_shutdown_neighbor.match(sub_level)
                    if m:
                        cmd += "no neighbor {} shutdown\n".format(
                            m.groupdict()["neighbor"]
                        )
                else:
                    m = p3_neighbor.match(sub_level)
                    if m:
                        if m.groupdict()["neighbor"] not in already_shut:
                            already_shut.append(m.groupdict()["neighbor"])
                            cmd += "neighbor {} shutdown\n".format(
                                m.groupdict()["neighbor"]
                            )

                # Following if block is used for neighbors under address_family level
                if search and search in sub_level:

                    # enter address-family
                    cmd += sub_level + "\n"

                    # shut / no shut neighbor
                    for command in config_dict["router bgp {}".format(bgp_as)][
                        sub_level
                    ]:
                        if noshut:
                            m = p2_shutdown_neighbor.match(command)
                            if m:
                                cmd += "no neighbor {} shutdown\n".format(
                                    m.groupdict()["neighbor"]
                                )
                        else:
                            m = p1_active_neighbor.match(command)
                            if m:
                                cmd += "neighbor {} shutdown\n".format(
                                    m.groupdict()["neighbor"]
                                )

                    # exit address-family
                    cmd += "exit-address-family\n"

            if "neighbor" in cmd:
                try:
                    device.configure(cmd)
                except SubCommandFailure:
                    if noshut:
                        raise SubCommandFailure(
                            "Could not enable bgp neighbors"
                        )
                    else:
                        raise SubCommandFailure("Could not shut bgp neighbors")

            else:
                if vrf:
                    raise ValueError(
                        "No neighbors found in running config "
                        "under {} address_family and {} vrf.".format(
                            address_family, vrf
                        )
                    )
                else:
                    raise ValueError(
                        "No neighbors found in running config "
                        "under {} address_family.".format(address_family)
                    )
        else:
            raise ValueError("No running configuration under router bgp.")


def configure_no_shut_bgp_neighbors(
    device, bgp_as, neighbors=None, address_family=None, vrf=None
):
    """ Enables bgp neighbors if provided otherwise it enabled the ones found in running config

        Args:
            device ('obj'): device under test
            bgp_id ('int'): router bgp_id to configure on
            address_family ('str'): address_family to configure under
            vrf ('str'): vrf to configure under
            neighbors('list'): Libs with BGP neighbors
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
            ValueError: Some information is missing
    """
    try:
        configure_shut_bgp_neighbors(
            device, bgp_as, neighbors, address_family, vrf, noshut=True
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(e)
    except ValueError as e:
        raise ValueError(str(e))


def configure_bgp_neighbor_remote_as(
    device, bgp_as, vrf, neighbor_as, neighbor_address, address_family
):
    """ Configure destination in vrf
        Args:
            device ('obj'): Device object
            bgp_as ('str'): Router bgp
            vrf ('str'): Vrf name
            neighbor_as ('str'): Destination
            neighbor_address ('str'): Neighbor address
            address_family ('str'): Address family
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """

    try:
        device.configure(
            [
                "router bgp {as_n}".format(as_n=bgp_as),
                "address-family {address_family} vrf {vrf}".format(
                    vrf=vrf, address_family=address_family
                ),
                "neighbor {neighbor} remote-as {neighbor_as}".format(
                    neighbor=neighbor_address, neighbor_as=neighbor_as
                ),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure destination {dest} on "
            "on device {dev}".format(dest=neighbor_as, dev=device.name)
        )


def remove_bgp_configuration(device, bgp_as):
    """ Remove bgp configuration
        Args:
            device ('obj'): Device object
            bgp_as ('str'): Router bgp
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """

    try:
        device.configure("no router bgp {as_n}".format(as_n=bgp_as))
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove BGP router {bgp_as} "
            "configuration from device {dev}".format(
                bgp_as=bgp_as, dev=device.name
            )
        )


def configure_bgp_neighbor_as_override(
    device, vrf, bgp_as, address_family, neighbor_address
):
    """ Configure AS override in VRF
        Args:
            device ('obj'): Device object
            bgp_as ('str'): Router bgp
            vrf ('str'): Vrf name
            neighbor_address ('str'): Neighbor address
            address_family ('str'): Address family
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """

    try:
        device.configure(
            [
                "router bgp {as_n}".format(as_n=bgp_as),
                "address-family {address_family} vrf {vrf}".format(
                    vrf=vrf, address_family=address_family
                ),
                "neighbor {neighbor} as-override".format(
                    neighbor=neighbor_address
                ),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure as-override on {dev} "
            "for vrf {vrf}".format(vrf=vrf, dev=device.name)
        )


def configure_bgp_additional_paths(device, bgp_as):
    """ Configure additional_paths on bgp router

        Args:
            device ('obj'): device to use
            bgp_as ('int'): bgp router to configure
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """
    log.info("Configuring bgp router {} with additional paths".format(bgp_as))
    try:
        device.configure(
            [
                "router bgp {}".format(bgp_as),
                "bgp additional-paths select all",
                "bgp additional-paths send receive",
                "bgp additional-paths install",
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure additional paths on bgp "
            "router {}".format(bgp_as)
        )


def configure_bgp_advertise_additional_paths(device, bgp_as, neighbor):
    """ Configures advertisement for additional paths

        Args:
            device ('obj'): device to configure
            bgp_as ('str'): router bgp number
            neighbor ('str'): neighbor to advertise to
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """
    log.info(
        "Configuring bgp router {} with advertisement of additional-paths".format(
            bgp_as
        )
    )
    try:
        device.configure(
            [
                "router bgp {}".format(bgp_as),
                "neighbor {} advertise additional-paths all".format(neighbor),
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure advertisement for "
            "additional paths on bgp router {}".format(bgp_as)
        )


def configure_bgp_address_advertisement(
    device, bgp_as, address_family, ip_address, mask
):
    """ Configure address advertisement on router bgp

        Args:
            device ('obj'): device to use
            bgp_as ('int'): bgp router to configure
            address_family ('str'): address family to configure under
            ip_address ('str'): ip address
            mask ('str'): mask
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """
    log.info(
        "Enabling address advertisement for ip: {} mask {}".format(
            ip_address, mask
        )
    )
    try:
        device.configure(
            [
                "router bgp {}".format(bgp_as),
                "address-family {}".format(address_family),
                "network {} mask {}".format(ip_address, mask),
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure address advertisement on "
            "router bgp {bgp_as}".format(bgp_as)
        )
