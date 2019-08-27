"""Common verify functions for vrf"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# BGP
from genie.libs.sdk.apis.iosxe.bgp.verify import (
    verify_bgp_route_is_advertised,
    is_route_in_bgp_table,
    verify_bgp_route_is_received,
)


# Utils
from genie.libs.sdk.apis.iosxe.running_config.get import (
    get_running_config_section_dict,
)

log = logging.getLogger(__name__)


def verify_vrf_advertised_routes(
    device,
    neighbor,
    address_family,
    config_vrf_list,
    vrf_name_routes,
    advertised_routes=None,
):
    """ Verify if each VRF/route distinguisher have at least one advertised route

        Args:
            device ('obj'): Device object
            neighbor ('str'): Neighbor
            address_family ('address_family'): Address family
            config_vrf_list ('dict'): Dictionary with VRF config from command 'show config'
            vrf_name_routes ('str'): VRf name to be search under in advertised routes
            advertised_routes ('dict'): Advertised routes from command:
                'show bgp {address_family} all neighbors {neighbor} advertised-routes'

        Returns:
            True
            False

        Raises:
            SchemaEmptyParserError
    """

    if not advertised_routes:
        try:
            advertised_routes = device.parse(
                "show bgp {address_family} all "
                "neighbors {neighbor} "
                "advertised-routes".format(
                    neighbor=neighbor, address_family=address_family
                )
            )
        except SchemaEmptyParserError as e:
            return False

    for vrf, vrf_data in config_vrf_list.get("vrf", {}).items():
        default_rd = vrf_data.get("route_distinguisher", "")

        if not default_rd:
            continue

        log.info(
            "VRF {vrf} and route distinguisher {rd}".format(
                vrf=vrf, rd=default_rd
            )
        )

        rd_address_family = "{address_family} RD {rd}".format(
            address_family=address_family, rd=default_rd
        )

        if not verify_bgp_route_is_advertised(
            device=device,
            advertised_routes=advertised_routes,
            address_family=rd_address_family,
            neighbor_address=neighbor,
            vrf=vrf_name_routes,
            default_vrf=vrf,
            default_rd=default_rd,
        ):

            log.error(
                "VRF {vrf} and route distinguisher {rd} do not"
                "have any advertised route on device {dev}".format(
                    vrf=vrf, rd=default_rd, dev=device.name
                )
            )
            return False

        else:
            log.info(
                "VRF {vrf} and route distinguishe {rd} have "
                "advertised routes on device {dev}".format(
                    vrf=vrf, rd=default_rd, dev=device.name
                )
            )

    return True


def verify_vrf_routes_in_bgp_table(
    device, config_vrf_list, address_family, routes_dict=None
):
    """ Verify that each VRF and route distinguisher has at least one route in BGP table

        Args:
            device ('obj'): Device object
            config_vrf_list ('dict'): Dictionary with VRF config from command 'show config'
            address_family ('address_family'): Address family
            routes_dict ('dict'): Parsed output from command 'show ip bgp all'

        Returns:
            True
            False

        Raises:
            SchemaEmptyParserError
    """

    if routes_dict is None:
        try:
            routes_dict = device.parse("show ip bgp all")
        except SchemaEmptyParserError as e:
            return False

    for vrf, vrf_data in config_vrf_list.get("vrf", {}).items():

        default_rd = vrf_data.get("route_distinguisher", "")

        if not default_rd:
            continue

        rd_address_family = "{address_family} RD {rd}".format(
            address_family=address_family, rd=default_rd
        )

        log.info(
            "VRF {vrf} and route distinguisher {rd}".format(
                vrf=vrf, rd=default_rd
            )
        )

        if not is_route_in_bgp_table(
            device=device,
            routes_dict=routes_dict,
            address_family=rd_address_family,
            default_rd=default_rd,
            default_vrf=vrf,
        ):

            log.error(
                "VRF {vrf} and route distinguishe {rd} do not "
                "have any route on BGP table in address family "
                "{address_family} on device {dev}".format(
                    vrf=vrf,
                    rd=default_rd,
                    address_family=address_family,
                    dev=device.name,
                )
            )
            return False
        else:
            log.info(
                "VRF {vrf} and Route Distinguisher {rd} have routes "
                "in BGP table on device {dev}".format(
                    vrf=vrf, rd=default_rd, dev=device.name
                )
            )

    return True


def verify_vrf_received_routes(
    device,
    address_family,
    neighbor,
    config_vrf_list,
    vrf_name_routes,
    received_routes,
):

    """ Verify if each neighbor has at least one received route

        Args:
            device ('obj'): Device object
            neighbor ('str'): Neighbor
            address_family ('address_family'): Address family
            config_vrf_list ('dict'): Dictionary with VRF config from command 'show config'
            vrf_name_routes ('str'): VRf name to be searched under in received routes
            received_routes ('dict'): Advertised routes from command:
                 'show bgp {address_family} all neighbors {neighbor} routes

        Returns:
            True
            False

        Raises:
            None
    """

    for vrf, vrf_data in config_vrf_list.get("vrf", {}).items():

        default_rd = vrf_data.get("route_distinguisher", "")

        if not default_rd:
            continue

        rd_address_family = "{address_family} RD {rd}".format(
            address_family=address_family, rd=default_rd
        )
        log.info(
            "VRF {vrf} and route distinguisher {rd}".format(
                vrf=vrf, rd=default_rd
            )
        )
        if not verify_bgp_route_is_received(
            device=device,
            neighbor_address=neighbor,
            vrf=vrf_name_routes,
            address_family=rd_address_family,
            default_rd=default_rd,
            default_vrf=vrf,
            received_routes=received_routes,
        ):

            log.error(
                "VRF {vrf} and route distinguisher {rd} do not "
                "have any received route on device {dev}".format(
                    vrf=vrf, rd=default_rd, dev=device.name
                )
            )
            return False
        else:
            log.info(
                "VRF {vrf} and Route Distinguisher {rd} have received "
                "routes on device {dev}".format(
                    vrf=vrf, rd=default_rd, dev=device.name
                )
            )

    return True


def verify_vrf_description_in_show_ip_vrf_detail(device, vrf, description):
    """Verify vrf description in show ip vrf detail <vrf>

        Args:
            device (`obj`): Device object
            vrf (`str`): Vrf name
            description (`str`): Description

        Returns:
            True
            False

        Raises:
            SchemaEmptyParserError
            Exception
    """

    cmd = "show ip vrf detail {vrf}".format(vrf=vrf)
    try:

        output = device.parse(cmd)
    except Exception as e:
        log.error(str(e))
        raise Exception("Failed to execute '{cmd}'".format(cmd=cmd))
    except SchemaEmptyParserError:
        raise SchemaEmptyParserError(
            "Command '{cmd}' has not returned any " "results".format(cmd=cmd)
        )

    if output[vrf].get("description", "") == description:
        return True

    return False


def verify_vrf_description_in_running_config(device, vrf, description):
    """Verify vrf description in show running-config

        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name
            description (`str`): Description

        Returns:
            True
            False

        Raises:
            Exception
            KeyError
    """
    try:
        output = get_running_config_section_dict(
            device, vrf + "$"
        )
    except Exception as e:
        log.error(str(e))
        raise Exception(
            "Failed to find vrf {vrf} through show running-config".format(
                vrf=vrf
            )
        )

    vrf = "vrf definition {vrf}".format(vrf=vrf)
    desc = "description {description}".format(description=description)
    try:
        result = isinstance(output[vrf][desc], dict)
    except KeyError:
        return False

    return result
