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
            "Could not configure import path selection on BGP router {bgp_as}"\
                .format(bgp_as=bgp_as
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
    address_family=None,
    vrf=None
):
    """ Configures bgp neighbor on bgp router

        Args:
            device('obj'): device to configure on
            bgp_as('str'): bgp_as to configure
            neighbor_as('str'): neighbor_as to configure
            neighbor_address('str'): address of neighbor
            source_interface('str',optional): used to configure update-source on neighbor ( Default is None )
            ebgp('str',optional): used to configure ebgp-mulithop ( Default is None )
            address_family('str',optional): address family ( Default is None )
            vrf('str',optional): vrf to configure address_family with ( Default is None )
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

    cmd = []
    cmd.append("router bgp {bgp_as}".format(bgp_as=bgp_as))
    if address_family:
        cmd2 = f"address-family {address_family}"
        if vrf:
            cmd2 += f" vrf {vrf}"
        cmd.append(cmd2)

    cmd.append("neighbor {neighbor_address} remote-as {neighbor_as}".format(
        neighbor_address=neighbor_address, 
        neighbor_as=neighbor_as))

    if source_interface:
        log_msg += "\n    -update-source: {}".format(source_interface)
        cmd.append("neighbor {neighbor_address} update-source {source_interface}"\
            .format(neighbor_address=neighbor_address,
                    source_interface=source_interface,
        ))

    if ebgp:
        log_msg += "\n    -ebgp-multihop: {}".format(ebgp)
        cmd.append("neighbor {neighbor_address} ebgp-multihop {ebgp}".format(
            neighbor_address=neighbor_address, ebgp=ebgp
        ))

    log.info(log_msg)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure bgp neighbor {neighbor_as} "
            "on router {bgp_as}.\nError: {e}".format(neighbor_as=neighbor_as, bgp_as=bgp_as, e=e)
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
            "\nneighbor {neighbor} prefix-list {prefix_list} {direction}"\
                .format(neighbor=pf["neighbor"],
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
                "neighbor {neighbor} route-map {route_map_name} "
                "{route_map_direction}\n".format(
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
    device, address_family, bgp_as, neighbor_address, steps=Steps(), 
    peer_policy=None, vrf=None):
    """ Activate bgp neighbor on bgp router 

        Args:
            device ('obj')             : Device to be configured
            bgp_as ('str')             : Bgp Id to be added to configuration
            neighbor_address ('str')   : Address of neighbor to be added to configuration
            address_family ('str')     : Address family to be configured
            steps('obj')               : Context manager steps
            peer_policy('str')         : peer policy to be configured
            vrf ('str')                : vrf name
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
            
    """
    with steps.start(
        "Configure device {dev}".format(dev=device.name), continue_=True
    ) as step:
        cnfg=[f"router bgp {bgp_as}"]
        if vrf:
            cnfg.append(f"address-family {address_family} vrf {vrf}")
        else:
            cnfg.append(f"address-family {address_family}")

        cnfg.append(f"neighbor {neighbor_address} activate")
        if peer_policy:
            cnfg.append(
                "neighbor {neighbor_address} inherit peer-policy {peer_policy}"\
                    .format(neighbor_address=neighbor_address, 
                            peer_policy=peer_policy))
        try:
            device.configure(cnfg)
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Could not ativate bgp neighbor on bgp "
                "router {bgp_as}".format(bgp_as=bgp_as)
            )

def configure_inherit_peer_session(
    device, bgp_as, neighbor_address, peer_policy=None
):
    """ configure inherit peer session under bgp

        Args:
            device ('obj')             : Device to be configured
            bgp_as ('str')             : Bgp Id to be added to configuration
            neighbor_address ('str')   : Address of neighbor to be added to configuration
            peer_policy('str')         : peer policy to be configured
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
            
    """
    try:

        cnfg=["router bgp {bgp_as}".format(bgp_as=bgp_as)]
        cnfg.append(
            "neighbor {neighbor_address} inherit peer-session {peer_policy}"\
                .format(neighbor_address=neighbor_address, 
                        peer_policy=peer_policy))
        device.configure(cnfg)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not inherit peer session in "
            "router {bgp_as}".format(bgp_as=bgp_as)
        )
            
def configure_bgp_l2vpn_neighbor_activate(
            device, address_family, bgp_as, neighbor_address, 
            address_family_modifier="", community=""
            ):
    """ Activate bgp neighbor on bgp router 

        Args:
            device ('obj')             : Device to be configured
            bgp_as ('str')             : Bgp Id to be added to configuration
            neighbor_address ('str')   : Address of neighbor to be added to configuration
            address_family ('str')     : Address family to be configured
            address_family_modifier ('str') : the endpoint provisioning information to be distributed
                                              to BGP peers.
            community('str') :  Specifies the communities attribute to be sent to a BGP neighbor.

        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
            
    """
    log.info("configure l2vpn vpls address-family on router bgp {bgp_as}"
                              .format(bgp_as=bgp_as))
    try:
        device.configure([
            "router bgp {bgp_as}".format(bgp_as=bgp_as),
            "address-family {address_family} {address_family_modifier}".format(
                address_family=address_family, 
                address_family_modifier=address_family_modifier),
            "neighbor {neighbor_address} activate".format(
                neighbor_address=neighbor_address),
            "neighbor {neighbor_address} send-community {community}".format(
                neighbor_address=neighbor_address, community=community)               
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not ativate l2vpn bgp neighbor on bgp "
            "router {bgp_as}. Error:{e}".format(bgp_as=bgp_as, e=e)
        )

def configure_shut_bgp_neighbors(
    device, bgp_as, neighbors=None, address_family=None, vrf=None, 
    noshut=False):
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
                "Enabling router bgp neighbors under address_family {} and vrf "
                "{}".format(address_family, vrf)
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
                "Shutting down router bgp neighbors under address_family {} and"
                " vrf {}".format(address_family, vrf)
            )
            search = "address-family {} vrf {}".format(address_family, vrf)
        elif address_family:
            log.info(
                "Shutting down router bgp neighbors under address_family {}"\
                    .format(address_family)
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
        "Configuring bgp router {} with advertisement of additional-paths"\
            .format(bgp_as)
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

    cmd = []
    cmd.append("router bgp {}".format(bgp_as))
    cmd.append("address-family {}".format(address_family))
    if address_family == 'ipv4':
        cmd.append("network {} mask {}".format(ip_address, mask))
    else:
        cmd.append("network {}".format(ip_address))

    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure address advertisement on "
            "router bgp {bgp_as}".format(bgp_as)
        )

def configure_redistribute_connected(device, bgp_as, address_family, vrf=None):
    """ configure redistribute connected in bgp

        Args:
            device ('obj'): device to use
            bgp_as ('str'): bgp as number
            address_family ('str'): address family under bgp 
            vrf ('str'): vrf in address_family default to None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring redistribute
                            connected under bgp address_family
    """
    log.info(
        "configure redistribute connected under bgp {}".format(bgp_as)
    )
    confg = ["router bgp {}".format(bgp_as)]
    if vrf:
        confg.append("address-family {address_family} vrf {vrf}".format(
                             address_family=address_family, vrf=vrf))
    else:
        confg.append("address-family {address_family}".format(
                             address_family=address_family))
    confg.append("redistribute connected")              
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure redistribute connected under bgp {bgp_as}"\
                .format(bgp_as=bgp_as)
        )

def configure_bgp_address_family_attributes(
    device, bgp_as, address_family, neighbor, send_label=False, 
    route_reflector_client=False, next_hop_self_all=False,
    next_hop_unchanged=False
):
    """ configure attributes for bgp 

        Args:
            device ('obj'): device to use
            bgp_as ('int'): bgp router to configure
            address_family ('str'): address family to configure under
            neighbor ('str'): neighbor address to send label
            send_label (`boolean`) :  send MPLS labels with the routes if true
            route_reflector_client (`boolean`) : sets a device as routing information exchange server if true
            next-hop-self all (`boolean`) : sets a device as routing information exchange server if true
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """
    try:
        confg = ["router bgp {}".format(bgp_as)]
        confg.append("address-family {}".format(address_family))
        if send_label:
            confg.append("neighbor {} send-label".format(neighbor))
        if route_reflector_client:
            confg.append("neighbor {} route-reflector-client".format(neighbor))
        if next_hop_self_all:
            confg.append("neighbor {} next-hop-self all".format(neighbor))
        if next_hop_unchanged:
            confg.append("neighbor {} next-hop-unchanged".format(neighbor))

        device.configure(confg)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure bgp attribute Error: {e} "
            "router bgp {bgp_as}".format(e=e, bgp_as=bgp_as)
        )
        
def configure_no_bgp_default(
    device, bgp_as, ipv4_unicast=False, route_target_filter=False
):
    """ configure no bgp default attributes under bgp

        Args:
            device ('obj'): device to use
            bgp_as ('int'): bgp router to configure
            ipv4_unicast ('boolean'): disable the default behavior of the BGP routing process 
                                  exchanging IPv4 address info, if set to true
            route_target_filter ('boolean'): disable automatic route-target filtering globally for all VRFs.
                                            if set to true.
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command                                            
    """
    try:
        confg = ["router bgp {}".format(bgp_as)]
        if ipv4_unicast:
            confg.append("no bgp default ipv4-unicast")
        if route_target_filter:
            confg.append("no bgp default route-target filter")
        device.configure(confg)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure bgp attribute Error: {e} "
            "router bgp {bgp_as}".format(e=e, bgp_as=bgp_as)
        )
        
def configure_bgp_graceful_restart(device, bgp_as):
    """ Configures graceful-restart on BGP router

        Args:
            device('obj'): device to configure on
            bgp_as('str'): bgp_as to configure
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    try:
        device.configure(
            "router bgp {bgp_as}\n"
            "bgp graceful-restart\n".format(
                bgp_as=bgp_as
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure graceful-restart on "
            "BGP router {bgp_as}".format(bgp_as=bgp_as)
        )

def configure_bgp_log_neighbor_changes(device, bgp_as):
    """ Configures log-neighbor-changes on BGP router

        Args:
            device('obj'): device to configure on
            bgp_as('str'): bgp_as to configure
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    try:
        device.configure(
            "router bgp {bgp_as}\n"
            "bgp log-neighbor-changes\n".format(
                bgp_as=bgp_as
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure log-neighbor-changes on "
            "BGP router {bgp_as}".format(bgp_as=bgp_as)
        )

def configure_bgp_neighbor_send_community(
    device, bgp_as, neighbor_address, address_family=None, vrf=None, 
    send_community=None):
    """ Add send-community attribute for bgp neighbor on bgp router

        Args:
            device ('obj')             : Device to be configured
            bgp_as ('str')             : Bgp Id to be added to configuration
            neighbor_address ('str')   : Address of neighbor to be added to configuration
            address_family ('str')     : Address family to be configured
            vrf ('str')                : vrf name
            send_community ('str')     : send-community attribute to be configured
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """
    cmd = "router bgp {bgp_as}\n".format(bgp_as=bgp_as)
    if address_family:
        if vrf:
            cmd += ("address-family {address_family} vrf {vrf}\n".format(
                        address_family=address_family,
                        vrf = vrf
                    )
                )
        else:
            cmd += ("address-family {address_family}\n".format(
                        address_family=address_family
                    )
                )

    if send_community:
        cmd += ("neighbor {neighbor_address} send-community {send_community}"\
            .format(neighbor_address=neighbor_address,
                    send_community=send_community
                )
            )
    else:
        cmd += ("neighbor {neighbor_address} send-community".format(
                    neighbor_address=neighbor_address,
                )
            )
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure send-community {send_community}"
            "For router bgp {bgp_as}".format(
                send_community=send_community, 
                bgp_as=bgp_as)
        )

        
def configure_ospf_internal_external_routes_into_bgp(
    device, bgp_as, process_id, vrf=None, address_family=None
):
    """ redistributes all(internal and external) OSPF routes into BGP

        Args:
            device ('obj'): device to use
            bgp_as ('int'): bgp router to configure
            process_id ('int'): ospf process_id
            address_family ('str'): address family to configure under
            vrf ('str'): vrf under which routes to be redistribute
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """
    try:
        confg = ["router bgp {}".format(bgp_as)]
        if not vrf:
            confg.append("redistribute ospf {process_id} match internal "
                         "external 1 external 2".format(process_id=process_id))
        else:
            confg.append("address-family {address_family} vrf {vrf}".format(
                address_family=address_family, vrf=vrf))
            confg.append("redistribute ospf {process_id} match internal "
                         "external 1 external 2".format(process_id=process_id))
            
        device.configure(confg)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not redistribute all ospf routes into bgp {bgp_as}"
            " Address family {address_family}.  Error: {e} ".format(
                bgp_as=bgp_as, address_family=address_family, e=e)
        )
        
def configure_ospf_include_connected_in_bgp(
    device, bgp_as, process_id, vrf=None, address_family=None
):
    """ redistributes IPv6 routes under bgp

        Args:
            device ('obj'): device to use
            bgp_as ('int'): bgp router to configure
            process_id ('int'): ospf process id
            address_family ('str'): address family to configure under
            vrf ('str'): vrf under which routes to be redistribute
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """
    try:
        confg = ["router bgp {}".format(bgp_as)]
        if not vrf:
            confg.append("redistribute ospf {process_id} include-connected"\
                 .format(process_id=process_id))
        else:
            confg.append("address-family {address_family} vrf {vrf}".format(
                address_family=address_family, vrf=vrf))
            confg.append("redistribute ospf {process_id} match internal "
                         "external 1 external 2 include-connected"\
                         .format(process_id=process_id))
            
        device.configure(confg)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure include-connected under bgp {bgp_as}"
            " for address-family {address_family} ,Error: {e} ".format(
                        address_family=address_family, bgp_as=bgp_as, e=e)
        )

def configure_bgp_redistribute_ospf(
    device, bgp_as, address_family=None, ospf_instance=None, vrf=None):
    """ Configures redistribute ospf on BGP router
        Args:
            device('obj'): device to configure
            bgp_as('str'): bgp id
            address_family:('str'): address family
            ospf_instance('str'): ospf redistribute to configure
            vrf('str'): vrf name
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    cmd="router bgp {bgp_as}\n".format(
                bgp_as=bgp_as)    
    if address_family:
        if vrf:
            cmd += ("address-family {address_family} vrf {vrf}\n"
                    "redistribute ospf {ospf_instance}".format(
                        address_family=address_family,
                        vrf=vrf,
                        ospf_instance=ospf_instance
                    )
                )
    else:
        cmd += ("redistribute ospf {ospf_instance}".format(
                    ospf_instance=ospf_instance
                )
            )
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure redistribute ospf on BGP router {bgp_as}"\
                .format(bgp_as=bgp_as)
        )

def configure_bgp_template_peer_policy(
    device, bgp_as, policy=None, send_community=None, 
    route_reflect_client=False, next_hop_self=None):
    """ Configures template peer-policy on BGP
        Args:
            device('obj'): device to configure
            bgp_as('str'): bgp id
            policy:('str'): policy to be configured
            send_community('str'): community to be configured
            route_reflect_client('str') : enable router to acts as a routing information exchange server for all other iBGP routers.
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    confg = ["router bgp {}".format(bgp_as)]
    confg.append("template peer-policy {policy}".format(
                                     policy=policy))
    if route_reflect_client:
        confg.append("route-reflector-client")
    if send_community:
        confg.append("send-community {send_community}".format(\
            send_community=send_community))
    if next_hop_self:
        confg.append("next-hop-self")    
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure bgp template peer policy on BGP router "
            "{bgp_as}".format(bgp_as=bgp_as)
        )

def configure_bgp_template_peer_session(
    device, bgp_as, session_name=None, remote_as=None,
    source_intf=None, neighbor=None):
    """ Configures template peer-session on BGP
        Args:
            device('obj'): device to configure
            bgp_as('str'): bgp id
            session_name:('str'): session name to be used
            remote_as('str'): remote as to configured
            source_intf('str'): source interface to be used
            neighbor('str'): neighbor ip
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    confg = ["router bgp {}".format(bgp_as)]
    if not neighbor:
        confg.append("template peer-session {session_name}".format(
                                         session_name=session_name))
        confg.append("remote-as {remote_as}".format(remote_as=remote_as))
        confg.append("update-source {source_intf}".format(
            source_intf=source_intf))
    else:
        confg.append("neighbor {neighbor} inherit peer-session {session_name}"\
            .format(neighbor=neighbor, session_name=session_name))
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure bgp template peer session on BGP router "
            "{bgp_as}".format(bgp_as=bgp_as)
        )

def configure_bgp_redistribute_connected(
    device, bgp_as, address_family=None, vrf=None):
    """ Configures redistrubute connected on BGP router
        Args:
            device('obj'): device to configure
            bgp_as('str'): bgp id
            address_family:('str'): address family
            vrf('str'): vrf name
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    cmd="router bgp {bgp_as}\n".format(
                bgp_as=bgp_as)
    if address_family:
        if vrf:
            cmd += ("address-family {address_family} vrf {vrf}\n"
             "redistribute connected".format(
                 address_family=address_family,
                 vrf=vrf
                    )
                )
        else:
            cmd += ("address-family {address_family}\n"
             "redistribute connected".format(
                 address_family=address_family
                    )
                )
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure redistribute connected on BGP router {bgp_as}"\
                .format(bgp_as=bgp_as)
        )

def enable_bgp_forwarding(
    device, interface_name):
    """ enables bgp forwarding under interface
        Args:
            device('obj'): device to configure
            interface_name('str'): interface name
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    cmd="interface {interface_name}\n".format(
                interface_name=interface_name)
    cmd += "mpls bgp forwarding"
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure bgp forwarding for interface {interface_name}"\
                .format(interface_name=interface_name
            )
        )

def unconfigure_bgp_neighbor_send_community(
    device, bgp_as, neighbor_address, address_family=None, vrf=None, 
    send_community=None):
    """ Remove send-community attribute for bgp neighbor on bgp router

        Args:
            device ('obj')             : Device to be configured
            bgp_as ('str')             : Bgp Id to be added to configuration
            neighbor_address ('str')   : Address of neighbor to be added to configuration
            address_family ('str')     : Address family to be configured
            vrf ('str')                : vrf name
            send_community ('str')     : send-community attribute to be configured
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands

    """

    cmd = "router bgp {bgp_as}\n".format(bgp_as=bgp_as)
    if address_family:
        if vrf:
            cmd += ("address-family {address_family} vrf {vrf}\n".format(
                        address_family=address_family,
                        vrf = vrf
                    )
                )
        else:
            cmd += ("address-family {address_family}\n".format(
                        address_family=address_family
                    )
                )

    if send_community:
        cmd += ("no neighbor {neighbor_address} send-community {send_community}"
            .format(neighbor_address=neighbor_address,
                    send_community=send_community
                )
            )
    else:
        cmd += ("no neighbor {neighbor_address} send-community".format(
                    neighbor_address=neighbor_address,
                )
            )
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure send-community {send_community}"
            "For router bgp {bgp_as}".format(
                send_community=send_community,
                bgp_as=bgp_as)
        )

def unconfigure_bgp_neighbor_activate(
    device, address_family, bgp_as, neighbor_address, vrf=None
):
    """ Unconfigure Activate bgp neighbor on bgp router

        Args:
            device ('obj')             : Device to be configured
            bgp_as ('str')             : Bgp Id to be added to configuration
            neighbor_address ('str')   : Address of neighbor to be added to configuration
            address_family ('str')     : Address family to be configured
            vrf ('str')                : vrf name
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands

    """

    cmd = "router bgp {bgp_as}\n".format(bgp_as=bgp_as)
    if address_family:
        if vrf:
            cmd += ("address-family {address_family} vrf {vrf}\n"
                     "no neighbor {neighbor_address} activate".format(
                        address_family=address_family,
                        neighbor_address=neighbor_address,
                        vrf = vrf
                    )
                )
        else:
            cmd += ("address-family {address_family}\n"
                     "no neighbor {neighbor_address} activate".format(
                        address_family=address_family,
                        neighbor_address=neighbor_address
                    )
                )
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not deativate bgp neighbor on bgp for router bgp {bgp_as}"\
                .format(bgp_as=bgp_as
            )
        )

def unconfigure_bgp_neighbor_remote_as(
    device, bgp_as, neighbor_as, neighbor_address, address_family=None, vrf=None
):
    """ unonfigure destination in vrf
        Args:
            device ('obj'): Device object
            bgp_as ('str'): Router bgp
            neighbor_as ('str'): Destination
            neighbor_address ('str'): Neighbor address
            address_family ('str'): Address family
            vrf ('str'): Vrf name
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """

    cmd = "router bgp {bgp_as}\n".format(bgp_as=bgp_as)
    if address_family and vrf:
        cmd += ("address-family {address_family} vrf {vrf}\n"
                "no neighbor {neighbor_address} remote-as {neighbor_as}".format(
                    vrf=vrf,address_family=address_family,
                    neighbor_address=neighbor_address, neighbor_as=neighbor_as
                )
            )
    else:
        cmd += ("no neighbor {neighbor_address} remote-as {neighbor_as}".format(
                neighbor_address=neighbor_address,neighbor_as=neighbor_as
               )
            )
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure destination {neighbor_address}"
            "for router bgp {bgp_as}".format(neighbor_address=neighbor_address,
                bgp_as=bgp_as)
        )
     
def configure_bgp_update_delay(device, bgp_as, delay):
    """ Configures update_delay time on BGP router
        Args:
            device('obj'): device to configure on
            bgp_as('str'): bgp_as to configure
            delay('int'): router_id of device
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """

    log.debug(
        "Configuring update_delay time BGP on {hostname}\n"
        "    -local AS number: {bgp_as}\n"
        "    -bgp update_delay: {delay}".format(
            hostname=device.hostname, bgp_as=bgp_as, delay=delay
        )
    )

    
    config = [
                'router bgp {bgp_as}'.format(bgp_as=bgp_as),
                'bgp update-delay {delay}'.format(delay=delay)
            ]
    
    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure update_delay {delay} on "
            "BGP router {bgp_as}".format(delay=delay, bgp_as=bgp_as)
        )
        
def configure_bgp_router_id_peergroup_neighbor(device, bgp_as, neighborname, as_id):
    """ Configures router-id on BGP router

        Args:
            device('obj'): device to configure on
            bgp_as('str'): bgp id (autonomous system number) to configure
            neighborname('str'): neighbor peer-group-name  to configure
            as_id('str'): ASN of the peer group to configure
        Return:
            None
        Raises:
            SubCommandFailure: Failed executing command
    """

    log.info(
        "Configuring router BGP on {hostname}\n"
        "    -local AS number: {bgp_as}\n"
        "    -bgp neighborname: {neighborname}"
		"    -remote AS number: {as_id}".format(
            hostname=device.hostname, bgp_as=bgp_as, neighborname=neighborname, as_id=as_id 
        )
    )
    config = [
                'router bgp {bgp_as}'.format(bgp_as=bgp_as),
				'bgp log-neighbor-changes',
                'neighbor {neighborname} peer-group'.format(neighborname=neighborname),
				'neighbor {neighborname} remote-as {as_id}'.format(neighborname=neighborname, as_id=as_id)
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure router-id {router_id} on "
            "BGP router {bgp_as}:\n{e}".format(neighborname=neighborname, as_id=as_id, bgp_as=bgp_as, e=e)
        )

def configure_bgp_router_id_neighbor_ip_peergroup_neighbor(device, bgp_as, neighbor_ip, neighborname):
    """ Configures router-id on BGP router

        Args:
            device('obj'): device to configure on
            bgp_as('str'): bgp id (autonomous system number) to configure
            neighbor_ip 'str'): neighbor_ip address to peer-group 
            neighborname('str'): neighbor peer-group-name  to configure
        Return:
            None
        Raises:
            SubCommandFailure: Failed executing command
    """

    log.info(
        "Configuring router BGP on {hostname}\n"
        "    -local AS number: {bgp_as}\n"
		"    -bgp neighbour_ip: {neighbor_ip}\n"
        "    -bgp neighborname: {neighborname}".format(
            hostname=device.hostname, bgp_as=bgp_as, neighbor_ip=neighbor_ip, neighborname=neighborname
        )
    )
    config = [
                'router bgp {bgp_as}'.format(bgp_as=bgp_as),
				'neighbor {neighbor_ip} peer-group {neighborname}'.format(neighbor_ip=neighbor_ip, neighborname=neighborname)
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure router-id {router_id} on "
            "BGP router {bgp_as}:\n{e}".format(bgp_as=bgp_as, neighbor_ip=neighbor_ip, neighborname=neighborname, e=e)
        )

def configure_bgp_sso_route_refresh_enable(device, bgp_as):
    """ Configures SSO route referesh on BGP router

        Args:
            device('obj'): device to configure on
            bgp_as('str'): bgp_as to configure
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    try:
        device.configure(
            "router bgp {bgp_as}\n"
            "bgp sso route-refresh-enable\n".format(
                bgp_as=bgp_as
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure SSO route refersh enable "
            "BGP router {bgp_as}".format(bgp_as=bgp_as)
        )


def configure_bgp_refresh_max_eor_time(device, bgp_as, max_eor_time):
    """ Configures refersh max-eor-time on BGP router

        Args:
            device('obj'): device to configure on
            bgp_as('str'): bgp_as to configure
            max_eor_time('str): max_eor_time to configure
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    try:
        device.configure(
            "router bgp {bgp_as}\n"
            "bgp sso route-refresh-enable\n"
            "bgp refresh max-eor-time {max_eor_time}\n".format(
                bgp_as=bgp_as, max_eor_time=max_eor_time
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure bgp refresh max-eor-time "
            "BGP router {bgp_as}".format(bgp_as=bgp_as)
        )

def configure_bgp_router_id_interface(device, bgp_as, interface):
    """ Configure bgp router-id interface on interface <interface>
        Args:
            device ('obj'): Device object
            bgp_as('int'): bgp id
            interface('str'): interface details on which we config
        Returns:
            None
        Raises: 
            SubCommandFailure : Failed to configure bgp router-id on interface
    """

    log.debug(f"Configure bgp router-id interface on interface {interface}")
    
    configs = [
        f"router bgp {bgp_as}",
        f"bgp router-id interface {interface}"
    ]
    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure bgp router-id interface on interface {interface}. Error:\n{e}"
        )

def configure_bgp_redistribute_static(device, bgp_as, address_family, vrf=None):
    """ configure redistribute static in bgp
        Args:
            device ('obj'): device to use
            bgp_as ('int'): bgp as number
            address_family ('str'): address family under bgp 
            vrf ('str'): vrf in address_family
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring redistribute
                            static under bgp address_family
    """
    log.info(
        f"configure redistribute static under bgp {bgp_as}"
    )
    confg = ["router bgp {}".format(bgp_as)]
    if vrf:
        confg.append(f"address-family {address_family} vrf {vrf}")
    else:
        confg.append(f"address-family {address_family}")
    confg.append("redistribute static")              
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            f"Could not configure redistribute static under bgp {bgp_as}"
        )
        

def configure_bgp_advertise_l2vpn_evpn(device, bgp_as, address_family, vrf):
    """ Configure bgp advertise l2vpn evpn on device <device>
        Args:
            device ('obj'): Device object
            bgp_as('int'): bgp id
            address_family('str'): address family (i.e - ipv4/ipv6)
            vrf('str'): vrf for in the device
        Returns:
            None
        Raises: 
            SubCommandFailure : Failed to configure bgp advertise l2vpn evpn on device            

    """

    log.debug(f"Configure bgp advertise l2vpn evpn on device {device}")
    
    configs = [
        f"router bgp {bgp_as}",
        f"address-family {address_family} vrf {vrf}",
        "advertise l2vpn evpn"
    ]
    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure bgp advertise l2vpn evpn on device {device}. Error:\n{e}"
        )
        

def configure_bgp_neighbor_advertisement_interval(
    device,
    bgp_as,
    address_family,
    neighbor_address,
    advert_interval,       
    vrf=None
):
    """ Configures bgp neighbor advertisement interval on bgp router

        Args:
            device('obj'): device to configure on
            bgp_as('str'): bgp_as to configure
            neighbor_address('str'): address of neighbor
            address_family('str'): address family ( Default is None )
            advert_interval('str'): advertisement interval to be configured
            vrf('str',optional): vrf to configure address_family with ( Default is None )
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log_msg = (
        "Configuring BGP on {hostname}\n"
        "    -local AS number: {bgp_as}\n"
        "    -advertisement interval: {advert_interval}\n"
        "    -neighbor: {neighbor_address}".format(
            hostname=device.hostname,
            bgp_as=bgp_as,
            advert_interval=advert_interval,
            neighbor_address=neighbor_address,
        )
    )

    cmd = [f"router bgp {bgp_as}"]

    if address_family and vrf:
        cmd.append(f"address-family {address_family} vrf {vrf}")
    else:
        cmd.append(f"address-family {address_family}")

    cmd.append(f"neighbor {neighbor_address} advertisement-interval {advert_interval}")

    log.info(log_msg)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure advertisement interval {advert_interval} for"\
            f" bgp neighbor {neighbor_address} on router {bgp_as}.Error:\n{e} "
        )


def configure_bgp_l2vpn_evpn_rewrite_evpn_rt_asn(
    device,
    bgp_as,
):
    """ Configures bgp rewrite-evpn-rt-asn for l2vpn evpn family on bgp router

        Args:
            device('obj'): device to configure on
            bgp_as('str'): bgp_as to configure
            address_family('str'): address family ( Default is None )
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log_msg = (
        "Configuring rewrite evpn rt asn BGP on {hostname}\n"
        "    -local AS number: {bgp_as}\n".format(
            hostname=device.hostname,
            bgp_as=bgp_as,
        )
    )

    config = [
                f'router bgp {bgp_as}',
                'address-family l2vpn evpn',
                'rewrite-evpn-rt-asn'
            ]

    log.info(log_msg)
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure rewrite-evpn-rt-asn for BGP router {bgp_as}"
            f".Error:\n{e}"
        )

def configure_router_bgp_maximum_paths(device, system, paths):
    """ Configures the maximum paths on router bgp
        Example: router bgp 100
                maximum-paths 3
        Args:
            device ('obj'): device to configure on
            system ('int'): Autonomous system number (Range 1-4294967295 or 1.0-XX.YY)
            paths ('int'): Number of paths (Range 1-32)
        Return:
            None
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(f"Configuring maximum-paths on router bgp on device {device.name}")
    config = [
        f'router bgp {system}',
        f'maximum-paths {paths}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure maximum-paths on router bgp on {device.name}. Error:\n{e}")

def unconfigure_router_bgp_maximum_paths(device, system, paths):
    """ Unconfigures the maximum paths on router bgp
        Example: router bgp 100
                no maximum-paths 3
        Args:
            device ('obj'): device to configure on
            system ('int'): Autonomous system number (Range 1-4294967295 or 1.0-XX.YY)
            paths ('int'): Number of paths (Range 1-32)
        Return:
            None
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(f"Unconfiguring maximum-paths on router bgp on {device.name}")
    config = [
        f'router bgp {system}',
        f'no maximum-paths {paths}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure maximum-paths on router bgp on {device.name}. Error:\n{e}")

def configure_router_bgp_synchronization(device, system):
    """ Configures the synchronization on router bgp
        Example: router bgp 100
                synchronization
        Args:
            device ('obj'): device to configure on
            system ('int'): Autonomous system number (Range 1-4294967295 or 1.0-XX.YY)
        Return:
            None
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(f"Configuring synchronization on router bgp on device {device.name}")
    config = [
        f'router bgp {system}',
        f'synchronization'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not configure synchronization on router bgp on {device.name}. Error:\n{e}")

def unconfigure_router_bgp_synchronization(device, system):
    """ Unconfigures the synchronization on router bgp
        Example: router bgp 100
                no synchronization
        Args:
            device ('obj'): device to configure on
            system ('int'): Autonomous system number (Range 1-4294967295 or 1.0-XX.YY)
        Return:
            None
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(f"Unconfiguring synchronization on router bgp on {device.name}")
    config = [
        f'router bgp {system}',
        f'no synchronization'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not unconfigure synchronization on router bgp on {device.name}. Error:\n{e}")

def unconfigure_bgp_log_neighbor_changes(device, system):
    """ Unconfigures the log neighbor changes on router bgp
        Example: router bgp 100
                no log-neighbor-changes
        Args:
            device ('obj'): device to configure on
            system ('int'): Autonomous system number (Range 1-4294967295 or 1.0-XX.YY)
        Return:
            None
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(f"Unconfiguring log-neighbor-changes on router bgp on {device.name}")
    config = [
        f'router bgp {system}',
        f'no bgp log-neighbor-changes'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure log neighbor changes on router bgp on {device.name}. Error:\n{e}")

def configure_bgp_auto_summary(device, system):
    """ Configures the auto-summary on router bgp
        Example: router bgp 100
                auto-summary
        Args:
            device ('obj'): device to configure on
            system ('int'): Autonomous system number (Range 1-4294967295 or 1.0-XX.YY)
        Return:
            None
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(f"Configuring auto-summary on router bgp on device {device.name}")
    config = [
        f'router bgp {system}',
        f'auto-summary'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure auto summary on router bgp on {device.name}. Error:\n{e}")

def unconfigure_bgp_auto_summary(device, system):
    """ Configures the auto-summary on router bgp
        Example: router bgp 100
                no auto-summary
        Args:
            device ('obj'): device to configure on
            system ('int'): Autonomous system number (Range 1-4294967295 or 1.0-XX.YY)
        Return:
            None
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(f"Unconfiguring auto-summary on router bgp on {device.name}")
    config = [
        f'router bgp {system}',
        f'no auto-summary'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure auto summary on router bgp on {device.name}. Error:\n{e}")