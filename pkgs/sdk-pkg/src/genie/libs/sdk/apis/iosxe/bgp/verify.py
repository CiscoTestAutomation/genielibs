"""Common verification functions for bgp"""

# Python
import logging
import copy
import re

from prettytable import PrettyTable

# import Steps
from pyats.aetest.steps import Steps
from pyats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# BGP
from genie.libs.sdk.apis.iosxe.bgp.get import (
    get_bgp_routes,
    get_bgp_summary,
    get_ip_bgp_route,
    get_ip_bgp_neighbors,
    get_show_run_bgp_dict,
    get_bgp_routing_table,
    get_bgp_running_config,
    get_bgp_route_ext_community,
    get_bgp_neighbor_capabilities,
    get_bgp_neighbor_session_state,
    get_bgp_neighbors_in_state,
    get_bgp_neighbors_not_in_state,
    get_bgp_networks_from_neighbor,
    get_bgp_status_codes_from_neighbor,
)

# utils
from genie.libs.sdk.apis.utils import time_to_int, has_configuration

from genie.libs.sdk.apis.iosxe.running_config.get import (
    get_running_config_section_dict,
)

log = logging.getLogger(__name__)


def verify_bgp_configuration_and_operation_state(
    device, sr_dict=None, sm_dict=None
):
    """ Verify bgp configuration is matched with operational state
        - "ipv4 vrf xxxx" and "vpnv4" in running config are in 
          "VPNv4 Unicast" address family in bgp all summary
        - "l2vpn vpls" in running config are in 
          "L2VPN Vpls" address family in bgp all summary
        - BGP AS number is same as configured
        - All configured neighbors exist and the status can be checked

        Args:
            device ('obj'): Device object
            sr_dict(`dict`): Parsed output from libs.bgp.get.get_show_run_bgp_dict
            sm_dict(`dict`): Parsed output of command 'show ip bgp all summary'
        Returns:
            result(`bool`): verified result
            info(`str`): compared information
        Raises:
            None
    """

    result = True
    info = []

    if not sr_dict:
        sr_dict = get_show_run_bgp_dict(device=device)
        if sr_dict is None:
            return None, None

    if not sm_dict:
        try:
            sm_dict = device.parse("show ip bgp all summary")
        except SchemaEmptyParserError as e:
            return None, None

    if sr_dict["bgp_as"] != sm_dict["bgp_id"]:
        result = False
        info.append(
            "BGP AS Number: configured {} -> operation {}".format(
                sr_dict["bgp_as"], sm_dict["bgp_id"]
            )
        )
    else:
        log.info(
            "BGP AS Number: configured {} -> operation {}".format(
                sr_dict["bgp_as"], sm_dict["bgp_id"]
            )
        )

    if "vpnv4" in sr_dict:
        for nbr in sr_dict["vpnv4"]["neighbors"]:
            sm_sub_dict = sm_dict["vrf"]["default"]["neighbor"]
            if (
                nbr in sm_sub_dict
                and "vpnv4 unicast" in sm_sub_dict[nbr]["address_family"]
            ):
                log.info(
                    "vpnv4 neighbor '{}' is in vpnv4 unicast "
                    "address-family".format(nbr)
                )
            else:
                result = False
                info.append(
                    "vpnv4 neighbor '{}' is not in vpnv4 unicast "
                    "address-family".format(nbr)
                )

    if "l2vpn vpls" in sr_dict:
        for nbr in sr_dict["l2vpn vpls"]["neighbors"]:
            sm_sub_dict = sm_dict["vrf"]["default"]["neighbor"]
            if (
                nbr in sm_sub_dict
                and "l2vpn vpls" in sm_sub_dict[nbr]["address_family"]
            ):
                log.info(
                    "l2vpn vpls neighbor '{}' is in l2vpn vpls "
                    "address-family".format(nbr)
                )
            else:
                result = False
                info.append(
                    "l2vpn vpls neighbor '{}' is not in l2vpn vpls "
                    "address-family".format(nbr)
                )

    if "ipv4" in sr_dict:
        for vrf, vrf_dict in sr_dict["ipv4"].items():
            nbr = vrf_dict.get("neighbor", '')
            remote_as = vrf_dict.get("remote_as", '')
            sm_vrf_dict = sm_dict.get("vrf", {})

            if not nbr or not remote_as:
                result = False
                info.append("ipv4 vrf '{}' don't have neighbor or remote-as".format(vrf))
                continue

            try:
                nbr_as = sm_vrf_dict[vrf]["neighbor"][nbr]["address_family"]\
                                    ["vpnv4 unicast"]["as"]
                if nbr_as != remote_as:
                    result = False
                    info.append(
                        "ipv4 vrf '{}' neighbor '{}' with AS '{}' but "
                        "configured AS is '{}'".format(
                            vrf, nbr, nbr_as, remote_as
                        )
                    )
                else:
                    log.info(
                        "ipv4 vrf '{}' neighbor '{}' with AS '{}' is in "
                        "vpnv4 unicast address-family".format(
                            vrf, nbr, remote_as
                        )
                    )
            except Exception as e:
                result = False
                info.append(
                    "ipv4 vrf '{}' neighbor '{}' with AS '{}' is not in "
                    "vpnv4 unicast address-family".format(vrf, nbr, remote_as)
                )

    return result, "\n".join(info)


def verify_bgp_last_reset(prev_list, curr_list):
    """ Verify last reset is always greater than previous value

        Args:
            prev_list(`list`): list of previous last reset value
            curr_list(`list`): list of current last reset value
        Returns:
            result(`bool`): verified result
            table(`obj`): table to display
        Raises:
            None
    """
    result = True
    table = PrettyTable()
    table.field_names = [
        "Vrf",
        "Neighbor",
        "Prev Count",
        "Curr Count",
        "Pass Evaluation",
    ]

    for prev, curr in zip(prev_list, curr_list):
        if prev["reset"] == curr["reset"] == "never":
            evl = "Skip"
        elif time_to_int(prev["reset"]) > time_to_int(curr["reset"]):
            result = False
            evl = False
        else:
            evl = True
        # display in table
        table.add_row(
            [prev["vrf"], prev["ip"], prev["reset"], curr["reset"], evl]
        )

    return result, table


def verify_bgp_syslog(device):
    """ Verify syslog messages don't contain BGP-5-ADJCHANGE mnemonic

        Args:
            device(`obj`): device object
        Returns:
            result (`str`): verified result
        Raises:
            None
    """
    result = []
    logs = device.parse("show logging")
    for line in logs["logs"]:
        if "BGP-5-ADJCHANGE" in line:
            result.append(line)

    return "\n".join(result)


def is_router_bgp_configured_with_four_octet(
    device, neighbor_address, vrf, max_time=35, check_interval=10
):
    """ Verifies that router bgp has been enabled with four
        octet capability and is in the established state

        Args:
            device('obj'): device to check
            vrf('vrf'): vrf to check under
            neighbor_address('str'): neighbor address to match
            max_time('int'): maximum time to wait
            check_interval('int'): how often to check

        Returns:
            True
            False
        Raise:
            None
    """
    log.info(
        "Verifying {} has bgp configured with four octet capability".format(
            device.hostname
        )
    )

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = device.parse("show ip bgp neighbors")
        if out:
            if vrf in out.get("vrf", {}):
                for neighbor in out["vrf"][vrf].get("neighbor", {}):
                    if neighbor_address in neighbor:
                        neighbor_dict = out["vrf"][vrf]["neighbor"][neighbor]
                        if (
                            "established"
                            in neighbor_dict.get("session_state", "").lower()
                        ):
                            if "bgp_negotiated_capabilities" in neighbor_dict and "advertised and received" in neighbor_dict[
                                "bgp_negotiated_capabilities"
                            ].get(
                                "four_octets_asn", ""
                            ):
                                return True

        timeout.sleep()
    return False


def is_bgp_import_path_selection(
    device, vrf, selection_type, max_time=30, check_interval=10
):
    """ Verifies that import path selection of type is in running
        config

        Args:
            device('obj'): device to use
            vrf('str'): vrf name
            selection_type('str'): import path selection type to verify
            max_time('int'): max time to wait
            check_interval('int'): how often to check        
        Returns:
            True
            False
        Raises:
            None
    """
    options = "vrf {}".format(vrf)

    log.info(
        'Verifying "import path selection {}" is configured'.format(
            selection_type
        )
    )

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = get_running_config_section_dict(
            device, section="router bgp", options=options
        )
        if has_configuration(
            out, "import path selection {}".format(selection_type)
        ):
            return True
        timeout.sleep()

    return False


def verify_bgp_soo_on_route(
    device,
    address_family,
    route,
    soo_rt,
    vrf=None,
    rd=None,
    max_time=60,
    check_interval=15,
):
    """ Verifies soo exists on route 

        Args:
            Required:
                device('obj'): device to verify on
                address_family('str'): address_family to verify under
                route('str'): route to verify
            
            One or the other:
                vrf('str'): verify using vrf
                rd('str'): verify using rd

            Optional:
                timeout('obj'): timeout object to override default

        Returns:
            True
            False
        Raise:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if vrf:
            result = get_bgp_route_ext_community(
                device, address_family, route, vrf=vrf
            )
            if not result:
                return False
        elif rd:
            result = get_bgp_route_ext_community(
                device, address_family, route, rd=rd
            )
            if not result:
                return False

        if result and "SoO:{}".format(soo_rt) in result:
            return True

        timeout.sleep()

    return False


def verify_bgp_as_path_prepend(
    route_dict, as_path_prepend, as_path, device, route, steps=Steps()
):
    """ Verify if AS value is added at the beginning of the AS path on route
        Args:
            route_dict ('obj')      : Dict containing all routes on device
            as_path_prepend ('int') : AS number to be checked on route
            as_path ('int')         : AS path on route            
            route ('str')           : Route beeing checked
            steps ('obj')           : Context manager step
        Returns:
            None
        
        Raises:
            pyATS Results
    """

    if not route_dict:
        raise Exception("Route list has not been passed")

    for index in list(route_dict.get("index", {})):

        with steps.start(
            "Verify Route {route}".format(route=route), continue_=True
        ) as step:
            path = route_dict["index"].get(index, {}).get("path", "")

            path_prepend = "{as_number} {as_path}".format(
                as_number=as_path_prepend, as_path=as_path
            )

            if path != path_prepend:
                step.failed(
                    "AS number {as_n} was not added at the beginning "
                    "of AS path on route {route}".format(
                        as_n=as_path_prepend, route=route
                    )
                )
            else:
                step.passed(
                    "AS number {as_n} was added at the beginning "
                    "of AS path on route {route}".format(
                        as_n=as_path_prepend, route=route
                    )
                )


def verify_bgp_rd_table(
    device,
    address_family,
    vrf,
    default_rd,
    routes_list,
    as_path_prepend,
    as_path,
    steps=Steps(),
):
    """Verify BGP table on neighbors

        Args:
            device ('obj')             : Device object
            address_family ('str')     : Address family to be used in show command
            routes_list ('dict')       : Routes to be verified 
            vrf ('str')           : VRF value 
            default_rd ('str')         : Route distinguisher value
            as_path_prepend ('str')    : AS path prepend value to be checked on routes
            as_path ('str')            : AS path from routes
            steps ('obj')              : Context manager object
        Raises:
            Exception
        Returns:
            None
    """

    with steps.start(
        "Verifying AS path in BGP table on device {device}".format(
            device=device.name
        ),
        continue_=True,
    ) as step:

        try:
            output = device.parse(
                "show ip bgp {address_family} rd {rd}".format(
                    address_family=address_family, rd=default_rd
                )
            )
        except SchemaEmptyParserError as e:
            step.failed(
                "Could not parse the following command\n"
                "show ip bgp {address_family} rd {rd}".format(
                    address_family=address_family, rd=default_rd
                )
            )

        for route in routes_list:
            routes_dict = (
                output["vrf"]
                .get(vrf, {})
                .get("address_family", {})
                .get(
                    "{address_family} RD {default_rd}".format(
                        address_family=address_family, default_rd=default_rd
                    ),
                    {},
                )
                .get("routes", {})
                .get(route, {})
            )

            try:
                verify_bgp_as_path_prepend(
                    route_dict=routes_dict,
                    route=route,
                    as_path_prepend=as_path_prepend,
                    as_path=as_path,
                    device=device,
                    steps=step,
                )

            except (AssertionError, Exception) as e:
                step.failed(e)


def verify_bgp_table_uut(
    address_family,
    device,
    routes_list,
    default_rd,
    as_path,
    as_path_prepend,
    neighbor_address,
    vrf=None,
    steps=Steps(),
):
    """Verify BGP table on device under test

        Args:                
            device ('obj')             : Device object            
            address_family ('str')     : Address family to be used in show command
            vrf ('str')           : VRF value of neighbors
            as_path_prepend ('str')    : AS path prepend value to be checked on routes
            routes_list ('dict')       : Routes to be verified
            default_rd ('str')         : Route distinguisher value
            as_path_prepend ('str')    : AS path prepend value to be checked on routes
            as_path ('str')            : AS path from routes
            steps ('obj')              : Context manager object
        Raises:
            Exception
        Returns:
            None
    """

    try:
        output = device.parse(
            "show ip bgp {address_family} vrf {vrf} "
            "neighbors {neighbor} routes".format(
                address_family=address_family,
                vrf=vrf,
                neighbor=neighbor_address,
            )
        )
    except SchemaEmptyParserError as e:
        log.info("Command has not returned any results")
        return False

    vrf = vrf if vrf else "default"

    with steps.start(
        "Verifying AS path in BGP table on device {device}".format(
            device=device.name
        ),
        continue_=True,
    ) as step:

        for route in routes_list:
            route_dict = (
                output["vrf"]
                .get(vrf, {})
                .get("neighbor", {})
                .get(neighbor_address, {})
                .get("address_family", {})
                .get(
                    "{address_family} RD {default_rd}".format(
                        address_family=address_family, default_rd=default_rd
                    ),
                    {},
                )
                .get("routes", {})
                .get(route, {})
            )
            try:
                verify_bgp_as_path_prepend(
                    route_dict=route_dict,
                    route=route,
                    as_path_prepend=as_path_prepend,
                    as_path=as_path,
                    device=device.name,
                    steps=step,
                )

            except Exception as e:
                step.failed(str(e))


def verify_capabilities_bgp_neighbor(
    device,
    vrf_name,
    neighbor_address,
    address_family,
    output=None,
    expected_capabilities=["advertised", "received"],
):
    """ Verify if capabilities of bgp neighbor matches expected capabilities
        Args:
            device ('obg')                    : Device object
            output ('dict')                   : Parsed output
            address_family ('str')            : Address family to be verified
            neighbor_address ('str')          : Address family to be searched under
            expected_capabilities  ('list')   : List of expected capabilities
            vrf_name ('str')                  : VRF name
        Returns:
            True
            False
        Raises:
            None

    """

    if output is None:
        output = {}

    capabilities = get_bgp_neighbor_capabilities(
        device=device,
        output=output,
        vrf=vrf_name,
        neighbor_address=neighbor_address,
        address_family=address_family,
    )

    if not capabilities:
        return None

    for capability in expected_capabilities:
        if capability not in capabilities:
            return False

    log.info(
        "On device {dev} under address family {address_family} neighbor "
        "{neighbor} has the following capabilities:\n{cap}".format(
            dev=device.name,
            address_family=address_family,
            neighbor=neighbor_address,
            cap=capabilities,
        )
    )

    return True


def verify_session_state_bgp_neighbor(
    device,
    neighbor_address,
    vrf_name=None,
    output=None,
    address_family="",
    address_families=None,
    expected_session_state="Established",
    max_time=60,
    check_interval=10,
    all_neighbors=False,
):
    """ Verify if session state matches expected state
        Args:
            device ('obg')                    : Device object
            output ('dict')                   : Parsed output
            address_family ('str')            : Address family to be verified
            address_families ('list')         : List of address families to check in session
                ex.) address_families = ['VPNv4 Unicast', 'L2VPN Vpls']
            neighbor_address ('str')          : Address family to be searched under
            expected_session_state  ('str')   : List of expected state
            vrf_name ('str')                  : VRF value
            max_time ('int'): max time
            check_interval ('int'): check interval
        Returns: 
            True
            False
        Raises:
            None
    """

    if output is None:
        output = {}

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():

        try:
            session_state, new_output = get_bgp_neighbor_session_state(
                device=device,
                vrf=vrf_name,
                address_family=address_family,
                address_families=address_families,
                neighbor_address=neighbor_address,
                output=output,
                all_neighbors=all_neighbors,
            )

            if session_state.lower() == expected_session_state.lower():
                log.info(
                    "Session state for neighbor {neighbor} is {st}".format(
                        dev=device.name,
                        address_family=address_family,
                        neighbor=neighbor_address,
                        st=session_state,
                    )
                )
                return True, new_output
            else:
                log.info(
                    "Current session state is {cur_state}. "
                    "Expecting {exp_state}".format(
                        cur_state=session_state,
                        exp_state=expected_session_state,
                    )
                )

            output = get_ip_bgp_neighbors(
                device=device,
                address_family=address_family,
                vrf=vrf_name,
                neighbor_address=neighbor_address,
                all_neighbors=all_neighbors,
            )

        except SchemaEmptyParserError as e:
            return False, None

        timeout.sleep()

    log.error(
        "Session state for neighbor {neighbor} is {session_state}. "
        "Expecting {exp_state}".format(
            neighbor=neighbor_address,
            session_state=session_state,
            exp_state=expected_session_state,
        )
    )

    return False, new_output


def verify_bgp_routes_have_community(
    device,
    neighbor_address,
    community,
    vrf=None,
    rd_export=None,
    address_family="",
    check_not_match=False,
    max_time=60,
    check_interval=10,
):
    """ Verify routes have community or not

        Args:
            device ('str'): Device str
            neighbor ('str'): neighbor address
            community ('str'): community name to search
            vrf ('str'): vrf name
            rd_export ('str'): rd export value
            check_not_match ('bool'): flag check community match or not
        Returns:
            True
            False
        Raises:
            None
    """
    neighbor_modified = neighbor_address.split("/")[0]
    timeout = Timeout(max_time=max_time, interval=check_interval)
    community_found = []
    while timeout.iterate():
        neighbor_output = None
        community_found = []
        if vrf and not rd_export:

            try:
                neighbor_output = device.parse(
                    "show bgp vrf {vrf} {route}".format(
                        vrf=vrf, route=neighbor_modified
                    )
                )

            except SchemaEmptyParserError as e:
                log.error(str(e))

        elif rd_export and not vrf:

            neighbor_output = get_ip_bgp_route(
                device=device,
                rd=rd_export,
                route=neighbor_modified,
                address_family=address_family,
            )

        else:
            log.error(
                "Argument rd and vrf are mutually exclusive, "
                "Only rd export or vrf name can be inserted"
            )
            return False

        reqs = R(['instance','default','vrf','(?P<vrf>.*)',
                  'address_family',address_family,'prefixes',
                  neighbor_address,'index','(?P<index>.*)',
                  'community','(?P<community>.*)'])
        found = find([neighbor_output], reqs, filter_=False, all_keys=True)
        if found:
            keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={},
                                        source=found, all_keys=True)
            for item in keys:
                community_found.append(item['community'])

        if check_not_match:
            if community in community_found:
                log.error("Found community {} in the command output"
                    .format(community))
            else:
                log.info("No community {} in the command output"
                    .format(community))
                return True
        else:
            if community in community_found:
                log.info("Found community {} in the command output"
                    .format(community))
                return True
            else:
                log.error("Failed to find community {} in the command output"
                    .format(community))

        timeout.sleep()

    return False


def is_bgp_neighbors_state(
    device, neighbors, address_family, state, max_time=15, check_interval=5
):
    """ Verifies BGP neighbor is in state

        Args:
            device('obj'): device to use
            neighbors('list'): neighbors to verify are shutdown
            address_family('str'): address_family neighbor is under
            state('regex str'): regex to match
            timeout('obj'): Use to override default timeout

        Returns:
            True
            False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        neighbors_in_state = get_bgp_neighbors_in_state(
            device=device, address_family=address_family, state=state
        )

        if set(neighbors).issubset(neighbors_in_state):
            return True

        log.info(
            "{} are not in state. Trying again.".format(
                set(neighbors) - set(neighbors_in_state)
            )
        )

        timeout.sleep()

    return False


def is_bgp_neighbors_shutdown(
    device, neighbors, address_family, max_time=15, check_interval=5
):
    """ Helper function for is_bgp_neighbors_state.
        Verifies BGP neighbor is shutdown

        Args:
            device('obj'): device to use
            neighbors('list'): neighbors to verify are shutdown
            address_family('str'): address_family neighbor is under
            timeout('obj'): Use to override default timeout

        Returns:
            True
            False
        Raises:
            None
    """
    return is_bgp_neighbors_state(
        device,
        neighbors,
        address_family,
        state="^idle \(admin\)$",
        max_time=max_time,
        check_interval=check_interval,
    )


def is_bgp_neighbors_enabled(
    device, neighbors, address_family, max_time=15, check_interval=5
):
    """ Helper function for is_bgp_neighbors_state.
        Verifies BGP neighbor is enabled and in either Idle or Active

        Args:
            device('obj'): device to use
            neighbors('list'): neighbors to verify are established
            address_family('str'): address_family neighbor is under
            timeout('obj'): Use to override default of 3 checks over 15 seconds

        Returns:
            True
            False
        Raises:
            None
    """
    return is_bgp_neighbors_state(
        device,
        neighbors,
        address_family,
        state="^(Idle|Active)$",
        max_time=max_time,
        check_interval=check_interval,
    )


def is_bgp_neighbors_established(
    device, neighbors, address_family, max_time=15, check_interval=5
):
    """ Helper function for is_bgp_neighbors_state.
        Verifies BGP neighbor is established

        Args:
            device('obj'): device to use
            neighbors('list'): neighbors to verify are established
            address_family('str'): address_family neighbor is under
            timeout('obj'): Use to override default of 3 checks over 15 seconds

        Returns:
            True
            False
        Raises:
            None
    """
    return is_bgp_neighbors_state(
        device,
        neighbors,
        address_family,
        state="^\d+$",
        max_time=max_time,
        check_interval=check_interval,
    )


def verify_bgp_routes_from_neighbors(
    device, address_family, vrf, route, source_address, rr_loopback
):
    """ Verify if routes are advertised by a particular source

        Args:
            device ('obj'): device object
            address_family ('str'): address family name
            vrf ('str'): vrf name
            route ('str'): IP address
            source_address ('str'): source address to check in output
            rr_loopback ('list'): loopback address list to check in output for route reflactor device
            ex.)
                loopback1 = '192.168.36.40'
                loopback2 = '192.168.36.41'
                rr_loopback = [ loopback1, loopback2 ]
        Returns:
            True
            False
        Raises:
            None
    """
    rr_lp = copy.deepcopy(rr_loopback)
    prefixes = {}

    # Get prefixes in order to get all routes
    prefixes = get_bgp_routes(
        device=device, address_family=address_family, vrf=vrf, route=route
    )

    if not prefixes:
        return False

    index = {}
    # Convert and iterate each prefix keys as to check if the key starts with that route
    # As input will be IP address while ouput in dictionary will be (IP address + Mask) as key
    for k in prefixes.keys():
        if k.startswith(route):
            try:
                index = prefixes[k]["index"]
            except KeyError as e:
                return False

    # Check if both routes exists till end. We need both routes to be from same source
    for v in index.values():
        next_hop = v.get("next_hop", "")
        gateway = v.get("gateway", "")

        if next_hop == source_address and gateway in rr_lp:
            rr_lp.remove(gateway)

    # True if all routes are found and list will be empty from search
    return rr_lp == []


def verify_bgp_as_in_as_path(
    device, route, bgp_as, vrf="", address_family="", output=""
):
    """ Verify if a route has an AS number in its AS path

        Args:
            device ('obj'): Device object
            route ('str'): Route to be verified
            bgp_as ('str'): AS number to be verified in route AS path
            vrf ('str'): VRF name
            address_family ('str'): Address family
            output ('str'): Parsed output of one of the following commands:
                * 'show ip bgp {address_family} vrf {vrf}'
                * 'show ip bgp {address_family}'
                * 'show ip bgp'
        Returns:
            True
            False
        Raises:
            None
    """

    if not output:
        try:
            output = get_bgp_routing_table(device=device, vrf=vrf)
        except SchemaEmptyParserError as e:
            return False

    if not vrf:
        vrf = "default"

    routes_index = list(
        output["vrf"][vrf]["address_family"][address_family]
        .get("routes", {})
        .get(route, {})
        .get("index", {})
        .values()
    )

    for index in routes_index:
        as_path = index.get("path", "")

        if bgp_as in as_path:
            return True

    return False


def verify_bgp_peers_are_present(
    device,
    address_family,
    vrf=None,
    rd=None,
    all_summary=False,
    bgp_peers=None,
):
    """ Verify if BGP peers are present

        Args:
            device ('obj'): device object
            address_family ('str'): address family name
            vrf ('str'): vrf name
            rd ('str'): RD export value
            all_summary ('bool'): Flag to get all summary
            bgp_peers ('dict'): Dictionary containing peer details - Neigbor and AS number
                ex.)
                    bgp_peers = {
                        '192.168.1.1': 65532,
                        '192.168.1.2': 65532,
                    }
        Returns:
            True
            False
    """
    result = True
    out = get_bgp_summary(
        device=device,
        address_family=address_family,
        vrf=vrf,
        rd=rd,
        all_summary=all_summary,
    )
    if not out:
        return False

    if bgp_peers:

        if not isinstance(bgp_peers, dict):
            raise Exception("bgp_peers must of type dict")

        for k, v in bgp_peers.items():
            try:
                as_number = out[k]["address_family"][address_family.lower()][
                    "as"
                ]

                if as_number != int(v):
                    log.error(
                        "BGP AS number for neighbor {} on device {}: \n"
                        "    Expected: {}\n"
                        "    Found: {}\n".format(k, device.name, v, as_number)
                    )
                    result = False
                else:
                    log.info(
                        "BGP AS number for neighbor {} on device {}: \n"
                        "    Expected: {}\n"
                        "    Found: {}\n".format(k, device.name, v, as_number)
                    )
            except KeyError as e:
                log.error(
                    "BGP peer {} with AS number {} is not present on device {}".format(
                        k, v, device.name
                    )
                )
                result = False

        return result

    return False


def verify_bgp_config_operational_state_neighbors(
    device,
    bgp_neighbors,
    vrf,
    bgp_config="",
    steps=Steps(),
    address_family_config="ipv4",
):
    """ Verify that bgp running config matches operational state from:
            'show ip bgp {address_family} vrf {vrf} neighbors'
            'show ip bgp {address_family} all neighbors'
        Args:
            device ('obj'): Device object
            bgp_config ('dict'): Parsed output from libs.bgp.get.get_bgp_running_config
                 Example {'VRF1': 
                            {'neighbors': {
                                '192.168.0.1': {
                                    'remote_as': 65555}}}}

            bgp_neighbors ('dict'): Parsed output from: 
                'show ip bgp {address_family} vrf {vrf} neighbors'
                'show ip bgp {address_family} all neighbors'
            vrf ('str'): VRF name to be verified
            address_family_config ('str'): Address family to be searched under in show running-config | section router bgp
            steps ('obj'): Context manager object
    """
    if not bgp_config:
        bgp_config = get_bgp_running_config(
            device=device, address_family=address_family_config
        )
        if not bgp_config:
            return False

    for vrf_config, neighbors in bgp_config.items():
        if vrf_config == vrf:
            for neighbors_dict in neighbors.values():
                for neighbor, remote_as_dict in neighbors_dict.items():
                    remote_as = remote_as_dict["remote_as"]

                    with steps.start(
                        "Verify Neighbor {neighbor}, Vrf {vrf}, AS number {as_n}".format(
                            neighbor=neighbor, vrf=vrf_config, as_n=remote_as
                        ),
                        continue_=True,
                    ) as step:

                        if not bgp_neighbors["vrf"].get(vrf_config, None):
                            step.failed(
                                "VRF {vrf} does not match operational state".format(
                                    vrf=vrf_config
                                )
                            )
                        else:
                            log.info(
                                "VRF {vrf} matches operational state".format(
                                    vrf=vrf_config
                                )
                            )

                        if (
                            not bgp_neighbors["vrf"]
                            .get(vrf_config, {})
                            .get("neighbor", {})
                            .get(neighbor, None)
                        ):
                            step.failed(
                                "Peer address {ip} does not match operational state".format(
                                    ip=neighbor
                                )
                            )
                        else:
                            log.info(
                                "Peer address {ip} matches operational state".format(
                                    ip=neighbor
                                )
                            )

                        session_state = (
                            bgp_neighbors["vrf"]
                            .get(vrf_config, {})
                            .get("neighbor", {})
                            .get(neighbor, {})
                            .get("session_state", None)
                        )
                        if not session_state:
                            step.failed("State not found ")
                        elif session_state != "Established":
                            step.failed(
                                "State is not Established. \n"
                                "Current state is {st}".format(
                                    st=session_state
                                )
                            )
                        else:
                            log.info(
                                "State {st} matches operational state".format(
                                    st=session_state
                                )
                            )

                        as_bgp_neighbor = (
                            bgp_neighbors["vrf"]
                            .get(vrf_config, {})
                            .get("neighbor", {})
                            .get(neighbor, {})
                            .get("remote_as", None)
                        )
                        if not as_bgp_neighbor:
                            step.failed("Could not find AS number")
                        elif as_bgp_neighbor == remote_as:
                            log.info(
                                "AS number {as_n} matches operational state".format(
                                    as_n=remote_as
                                )
                            )
                        else:
                            step.failed(
                                "AS number {as_n} does not match operational state\n"
                                "AS number found {as_n_op}".format(
                                    as_n=remote_as, as_n_op=as_bgp_neighbor
                                )
                            )


def verify_bgp_config_operational_state_summary(
    device,
    bgp_summary,
    vrf,
    address_family,
    bgp_config="",
    address_family_config="ipv4",
    steps=Steps(),
):
    """ Verify that bgp running config matches operational state from:

            'show ip bgp {address_family} vrf {vrf} summary'
            'show ip bgp {address_family} all summary'
        Args:
            device ('obj'): Device object
            bgp_config ('dict'): Parsed output from libs.bgp.get.get_bgp_running_config
                 Example {'VRF1': 
                            {'neighbors': {
                                '192.168.0.1': {
                                    'remote_as': 65555}}}}

            bgp_summary ('dict'): Parsed output from:
                'show ip bgp {address_family} vrf {vrf} summary'
                'show ip bgp {address_family} all summary'
            vrf ('str'): VRF name
            address_family_config ('str'): Address family to be searched under in show running-config | section router bgp
            steps ('obj'): Context manager object

    """

    if not bgp_config:
        bgp_config = get_bgp_running_config(
            device=device, address_family=address_family_config
        )
        if not bgp_config:
            return False

    for vrf_config, neighbors in bgp_config.items():
        if vrf_config == vrf:
            for neighbors_dict in neighbors.values():
                for neighbor, remote_as_dict in neighbors_dict.items():
                    remote_as = remote_as_dict["remote_as"]

                    with steps.start(
                        "Verify Neighbor {neighbor}, Vrf {vrf}, AS number {as_n}".format(
                            neighbor=neighbor, vrf=vrf, as_n=remote_as
                        ),
                        continue_=True,
                    ) as step:

                        peer_address = (
                            bgp_summary["vrf"]
                            .get(vrf, {})
                            .get("neighbor", {})
                            .get(neighbor, None)
                        )
                        if not peer_address:
                            step.failed(
                                "Peer address {ip} does not match operational state".format(
                                    ip=neighbor
                                )
                            )
                        else:
                            log.info(
                                "Peer address {ip} matches operational state".format(
                                    ip=neighbor
                                )
                            )

                        bgp_summary_as = (
                            bgp_summary["vrf"]
                            .get(vrf, {})
                            .get("neighbor", {})
                            .get(neighbor, {})
                            .get("address_family", {})
                            .get(address_family)
                            .get("as", None)
                        )

                        if not bgp_summary_as:
                            step.failed("Could not find AS number")
                        elif bgp_summary_as == remote_as:
                            log.info(
                                "AS number {as_n} matches operational state".format(
                                    as_n=remote_as
                                )
                            )
                        else:
                            step.failed(
                                "AS number {as_n} does not match operational state\n"
                                "AS number found {as_n_op}".format(
                                    as_n=remote_as, as_n_op=bgp_summary_as
                                )
                            )

                        state_pfxrcd = (
                            bgp_summary["vrf"]
                            .get(vrf, {})
                            .get("neighbor", {})
                            .get(neighbor, {})
                            .get("address_family", {})
                            .get(address_family)
                            .get("state_pfxrcd", None)
                        )
                        if not state_pfxrcd:
                            step.failed("Could not find prefix information")
                        elif state_pfxrcd.isdigit() or state_pfxrcd in [
                            "Active",
                            "Idle",
                        ]:
                            log.info(
                                "Prefix {prfx} matches operational state".format(
                                    prfx=state_pfxrcd
                                )
                            )
                        else:
                            step.failed(
                                "Prefix {prfx} does not match operational state".format(
                                    prfx=state_pfxrcd
                                )
                            )


def verify_bgp_route_is_advertised(
    device,
    vrf,
    address_family,
    neighbor_address,
    default_vrf,
    default_rd,
    advertised_routes=None,
):
    """ Verify if a route is advertised for a VRF and Router Distinguisher

        Args:
            vrf('str')                  : VRF name to be verified
            address_family('str')       : Address family 
            neighbor_address ('str')            : Neighbor interface address
            default_rd('str')           : Route distinguisher from VRF list
            default_vrf('str')          : VRF from VRF list
            advertised_routes ('dict'): Advertised routes from command:
                'show bgp {address_family} all neighbors {neighbor} advertised-routes'
        Returns:
            True
            False
        Raises:
            Exception
    """

    if not advertised_routes:
        try:
            advertised_routes = device.parse(
                "show bgp {address_family} all neighbors "
                "{neighbor} advertised-routes".format(
                    address_family=address_family, neighbor=neighbor_address
                )
            )
        except SchemaEmptyParserError:
            log.info("Command has not returned any results")
            return False

    address_family_dict = (
        advertised_routes["vrf"]
        .get(vrf, {})
        .get("neighbor", {})
        .get(neighbor_address, {})
        .get("address_family", {})
        .get(address_family, {})
    )

    route_distinguisher = address_family_dict.get("route_distinguisher", None)
    route_vrf = address_family_dict.get("default_vrf", None)
    advertised_list = address_family_dict.get("advertised", {}).keys()

    if advertised_list:
        if route_distinguisher == default_rd and route_vrf == default_vrf:

            log.info(
                "The following routes were advertised for VRF "
                "{vrf} and route distinguisher {rd}:\n{routes}".format(
                    vrf=default_vrf,
                    rd=default_rd,
                    routes="\n".join(advertised_list),
                )
            )
            return True

        else:
            return False
    else:
        return False


def verify_bgp_route_is_received(
    device,
    vrf,
    neighbor_address,
    default_rd,
    default_vrf,
    address_family,
    received_routes,
):
    """ Verify if VRF and Router Distinguisher have at least one received route
        Args:
            device ('obj')              : Device object
            address_family ('str')      : Address family to be used in show command
            vrf ('str')                 : VRF name to be verified 
            neighbor_address ('str')   : Neighbor interface address
            default_rd ('str')          : Route distinguisher from VRF list
            default_vrf ('str')         : Default VRF name
            address_family ('str')      : Address family
            received_routes ('dict')    : Parsed output to be verified
        Returns:
            True
            False
        Raises:
            None
    """

    address_family_dict = (
        received_routes["vrf"]
        .get(vrf, {})
        .get("neighbor", {})
        .get(neighbor_address, {})
        .get("address_family", {})
        .get(address_family, {})
    )

    route_distinguisher = address_family_dict.get("route_distinguisher", None)
    route_vrf = address_family_dict.get("default_vrf", None)
    advertised_list = address_family_dict.get("routes", {}).keys()

    if advertised_list:
        if route_distinguisher == default_rd and route_vrf == default_vrf:

            log.info(
                "The following routes were received for VRF "
                "{vrf} and route distinguisher {rd}:\n{routes}".format(
                    vrf=default_vrf,
                    rd=default_rd,
                    routes="\n".join(advertised_list),
                )
            )
            return True

        else:
            return False
    else:
        return False


def is_route_in_bgp_table(
    device, address_family, default_rd, default_vrf, routes_dict
):
    """ Verify if route is in BGP table
        Args:
            device ('obj')          : Device object
            address_family('str')   : Address family to be used in show command
            default_rd('str')       : Route distinguisher from VRF list
            default_vrf('str')      : Default VRF name
            routes_dict ('dict')    : Parsed output to be verified
        Returns:
            True
            False
        Raises:
            None

    """

    routes = (
        routes_dict["vrf"]
        .get(default_vrf, {})
        .get("address_family", {})
        .get(address_family, {})
    )

    route_distinguisher = routes.get("route_distinguisher", None)
    route_vrf = routes.get("default_vrf", None)
    routes_list = routes.get("routes", {}).keys()

    if routes_list:
        if route_distinguisher == default_rd and route_vrf == default_vrf:

            log.info(
                "VRF {vrf} and route distinguishe {rd} have "
                "the following routes in BGP table for address "
                "family {address_family} on device {dev}:\n{routes}".format(
                    vrf=default_vrf,
                    rd=default_rd,
                    address_family=address_family,
                    dev=device.name,
                    routes="\n".join(routes_list),
                )
            )
            return True

        else:
            return False
    else:
        return False


def verify_bgp_address_received(
    device, neighbor_address, address, max_time=60, check_interval=10
):
    """ Verifies that address is recieved from neighbor

        Args:
            device ('obj'): device to use
            neighbor ('str'): neighbor to check under
            address ('str'): address to verify

        Returns:
            True/False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        networks = get_bgp_networks_from_neighbor(device, neighbor_address)

        if networks and address in networks:
            return True

        timeout.sleep()

    return False


def verify_bgp_status_codes_exist(
    device,
    neighbor_address,
    route,
    status_codes,
    max_time=90,
    check_interval=15,
    check_all=True,
):
    """ Verifies status exists in status_codes

        Args:
            device ('obj'): device to use
            neighbor ('str'): neighbor to check under
            route ('str'): route to check under
            status_codes ('str'): status codes from parser
            max_time ('int'): maximum time to wait
            check_interval ('int'): how often to check
            check_all ('bool'): wether or not to check all status_codes passed or atleast one

        Returns:
            codes ('str') or None
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():

        codes = get_bgp_status_codes_from_neighbor(
            device, neighbor_address=neighbor_address, route=route
        )

        if codes:
            if check_all:
                flag_found = True

                for status in status_codes:
                    if status not in codes:
                        flag_found = False
                        break

                if flag_found:
                    return codes

            else:
                for status in status_codes:
                    if status in codes:
                        return status

        timeout.sleep()

    return False


def verify_bgp_neighbor_exist(device, neighbor, address_family, vrf='',
                              max_time=60, check_interval=10):
    """ Verify bgp neighbor exists in 'show ip bgp {address_family} summary'

        Args:
            device ('obj'): device to use
            neighbor ('str'): neighbor to check under
            address_family ('str'): address family
            vrf ('str'): vrf
            max_time ('int'): maximum time to wait
            check_interval ('int'): how often to check

        Returns:
            result ('bool'): verified result
    """
    if vrf:
        cmd = 'show ip bgp {address_family} vrf {vrf} summary'.format(
                address_family=address_family, vrf=vrf)
    else:
        cmd = 'show ip bgp {address_family} summary'.format(
                address_family=address_family)
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
            timeout.sleep()
            continue

        reqs = R(['vrf', '(?P<vrf>.*)', 'neighbor', neighbor, '(.*)'])
        found = find([out], reqs, filter_=False, all_keys=True)
        if found:
            log.info("BGP neighbor {nbr} is present".format(nbr=neighbor))
            return True

        timeout.sleep()

    return False

def verify_extended_community_color(device, address_family, rd, route,
                                    expected_color=None, max_time=90,
                                    check_interval=10):
    """ Verify color exists in 'show ip bgp {address_family} rd {rd} {route}'

        Args:
            device ('obj'): device to use
            address_family ('str'): address family
            rd ('str'): Route distinguisher
            route ('str'): Route to check
            expected_color ('str'): Color value
            max_time ('int'): maximum time to wait
            check_interval ('int'): how often to check

        Returns:
            result ('bool'): verified result
    """
    reqs = R(
        [
            'instance',
            'default',
            'vrf',
            'default',
            'address_family',
            address_family,
            'prefixes',
            route,
            'index',
            '(?P<index>.*)',
            'ext_community',
            '(.*Color: *{}.*)'.format(expected_color if expected_color else '')
        ]
    )

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = get_ip_bgp_route(device=device, route=route,
                               address_family=address_family, rd=rd)
        if not out:
            log.info('Could not get information about ip bgp route')
            timeout.sleep()
            continue
        
        found = find([out], reqs, filter_=False, all_keys=True)
        if not found and not expected_color:
            return True
        elif found and expected_color:
            return True

        timeout.sleep()

    return False

def verify_bgp_each_path(
    device,
    vrf,
    route,
    expected_endpoint_ip=None,
    expected_metric=None,
    max_time=30,
    address_family=None,
    check_interval=10,
):
    """ Verify each endpoint is same 'show ip bgp vrf {vrf} {route}'

        Args:
            device ('obj'): device to use
            address_family ('str'): address family
            vrf ('str'): VRF name
            route ('str'): Route to check
            expected_endpoint_ip ('str', None): Expected endpoint ip
            expected_metric ('str'): Expected metric ip
            max_time ('int'): maximum time to wait
            check_interval ('int'): check interval

        Returns:
            result ('bool'): verified result
    """
    timeout = Timeout(max_time=max_time, interval=check_interval)
    while timeout.iterate():
        neighbor_output = get_ip_bgp_route(
                device=device,
                vrf=vrf,
                route=route,
                address_family=address_family,
            )
        result = True
        if neighbor_output:
            reqs = R(['instance','default','vrf','(?P<vrf>.*)',
                    'address_family', '(?P<address_family>.*)' ,'prefixes',
                    '(?P<route>{}.*)'.format(route),'index','(?P<index>.*)', '(?P<route_dict>.*)'])
            found = find([neighbor_output], reqs, filter_=False)
            if found:
                key_list = GroupKeys.group_keys(
                    reqs=reqs.args, ret_num={}, source=found
                )
                for v in key_list:
                    v = v.get('route_dict', {})
                    endpoint_ip = v.get('next_hop', None)
                    if expected_endpoint_ip:
                        end_point_check = endpoint_ip == expected_endpoint_ip
                        if not end_point_check:
                            log.info('Expected endpoint is "{expected_endpoint_ip}" actual is "{endpoint_ip}"'
                            .format(expected_endpoint_ip=expected_endpoint_ip,
                                    endpoint_ip=endpoint_ip))
                            result = False
                            continue
                    metric = v.get('metric', None)
                    if expected_metric:
                        metric_check = metric == expected_metric
                        if not metric_check:
                            log.info('Expected metric is "{expected_metric}" actual is "{metric}"'
                            .format(expected_metric=expected_metric,
                                    metric=metric))
                            result = False
                            continue
        else:
            result = False
        
        if result:
            return True
        timeout.sleep()
        
    return result

def verify_ip_bgp_route(device, route, max_time=90, check_interval=10, 
    expected_state_pfxrcd=None):
    """ Verify state/pfxrcd exists in 'show ip bgp summary'

        Args:
            device ('obj'): device to use
            route ('str'): Route to check
            max_time ('int'): maximum time to wait
            check_interval ('int'): how often to check
            expected_state_pfxrcd ('str'): Expected State/Pfxrcd

        Returns:
            result ('bool'): verified result
    """
    
    reqs = R(
        [
            'vrf',
            'default',
            'neighbor',
            route,
            'address_family',
            '(?P<address_family>.*)',
            '(?P<val>.*)'
        ]
    )

    timeout = Timeout(max_time, check_interval)
    result = True
    while timeout.iterate():
        out = device.api.get_ip_bgp_summary(device=device)
        if not out:
            log.info('Could not get information about show ip bgp summary')
            result = False
            timeout.sleep()
            continue        
        found = find([out], reqs, filter_=False, all_keys=True)
        if found and expected_state_pfxrcd:
            key_list = GroupKeys.group_keys(
                    reqs=reqs.args, ret_num={}, source=found
                )
            for v in key_list:
                state_pfxrcd = v.get('val', {}).get('state_pfxrcd', None)
                result = state_pfxrcd == expected_state_pfxrcd
                if not result:
                    log.info('Expected state/pfxrcd is "{expected_state_pfxrcd}" '
                        'actual is "{state_pfxrcd}"'.format(
                            expected_state_pfxrcd=expected_state_pfxrcd,
                            state_pfxrcd=state_pfxrcd
                        ))
        
        if result:
            return True
        timeout.sleep()
    return False
    
def verify_bgp_mvpn_route_count(device, route_type, vrf, max_time=90, check_interval=10):
    """ Verify count of metioned routes 

        args:
            device ('obj'): Device to use
            route_type ('dict') : contains all the route type and route count
            vrf ('str'): vrf name
        raises:
            N/A

        returns:
            dict
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        result = True
        out = device.api.get_bgp_mvpn_route_count(route_type, vrf)
        if not out:
            log.info('Could not get information about show bgp ipv4 mvpn vrf')
            result = False
            timeout.sleep()
            continue     

        for route, count in route_type.items():
            if out.get(route,None):
                if count == out[route]:
                    log.info("Got the expected number of routes {count} for {route}".format(count=count,route=route))
                else:
                    log.error("Got unexpected number of routes {count} for {route}, expected number of routes {count1}".format(count=out[route],route=route,count1=count))
                    result = False            
            else:
                log.error("{route} not found in the output, please verify!".format(route=route)) 
                result = False
        if result:
            return True
        timeout.sleep()

def verify_bgp_rt2_route_target(
    device, address_family, eti, mac_addr, ip_addr, vrf_id, expected_rt, 
    max_time=30, check_interval=10
):
    """ Verify bgp RT-2 host route(s) exists in 'show ip bgp {address_family}
        route-type 2 {eti} {mac} {ip}'

        Args:
            device ('obj'): device to use
            address_family ('str'): address family
            eti ('str'):Ethernet tag in decimal <0-4294967295>
            mac_addr('str'): mac address
            ip_addr('str'): Ip address
            vrf_id ('str'): vrf
            expected_rt('str' or 'list'): Expected route target
            max_time ('int', optional): maximum time to wait in seconds, 
                default 30
            check_interval ('int'. optional): how often to check in seconds, 
                default 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        rt2_dict = device.api.get_bgp_rt2_community_label(
             device=device,
             address_family=address_family,
             eti=eti,
             mac=mac_addr,
             ip=ip_addr,
             vrf_id=vrf_id)

        if rt2_dict:
            comm_list = rt2_dict["ext_community"]

            if isinstance(expected_rt, str):
                if expected_rt in comm_list:
                    return True
            else:
                # comparing expected list with actual for diff using sets
                if not set(expected_rt).difference(set(comm_list)):
                    return True

        timeout.sleep()

    if not rt2_dict:
        log.error(
            "Unable to get RT-2 route for host {} in 'show ip bgp {} route-type"
            "2 {} {} {}".format(ip_addr, address_family, eti, mac_addr, ip_addr)
        )
    else:
        log.error(
            'Expected route target is {expected_rt} actual is '
            '{actual_rt}'.format(expected_rt=expected_rt, actual_rt=comm_list)
        )

    return False


def verify_bgp_rt5_reoriginated_from(
    device, address_family, eti, ip_addr, ip_length, vrf_id, expected_path, 
    max_time=30, check_interval=10
):
    """ re-originated RT-5 host IP route indicates route is re-originated 
        from RT-2 in 'show ip bgp {address_family} route-type 5 
        {eti} {ip} {ip_len}'

        Args:
            device ('obj'): device to use
            address_family ('str'): address family
            eti ('str'):Ethernet tag in decimal <0-4294967295>
            ip_addr('str'): Ip address
            ip_length('str'): Ip length
            vrf_id('str'): VRF name
            expected_path('str'): Expected path
            max_time ('int', optional): maximum time to wait in seconds,
                default 30
            check_interval ('int', optional): how often to check in seconds, 
                default 10
        Example: 
            Paths: (1 available, best #1, table evi_101, 
            re-originated from [2][30.0.1.11:101][0][48]
                [009999888888][32][20.101.1.3]/24)
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        path_dict = device.api.get_bgp_rt5_community_paths_label(
             device=device,
             address_family=address_family,
             eti=eti,
             ip=ip_addr,
             ip_len=ip_length,
             vrf_id=vrf_id)

        if path_dict:
            path_list = path_dict["paths"]

            for path in path_list.split(","):

                if path.find(expected_path) >= 0:
                    return True
                else:
                    continue
        timeout.sleep()

    if not path_dict:
        log.error('Output is empty')
    else:
        log.error('Expected reoriginated path is "{expected_path}" '
            'actual is "{path_list}"'.format(expected_path=
            expected_path, path_list=path_list))

    return False


def verify_bgp_rt5_route_target(
    device, address_family, eti, ip_addr, ip_length, vrf_id, expected_rt, 
    max_time=30, check_interval=10
):
    """ Verify bgp for specific route target host(s) in
        'show ip bgp {address_family} route-type 5 {eti} {ip} {ip_len}' 

        Args:
            device ('obj'): device to use
            address_family ('str'): address family
            eti ('str'):Ethernet tag in decimal <0-4294967295>
            ip_addr('str'): ipv4/ipv6 address
            ip_length('str'): Ip length
            vrf_id ('str'): vrf
            expected_rt ('str' or 'list'): Expected RT
            max_time ('int', optional): maximum time to wait in seconds, 
                default 30
            check_interval ('int', optional): how often to check in seconds, 
                default 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        rt5_dict = device.api.get_bgp_rt5_community_paths_label(
             device=device,
             address_family=address_family,
             eti=eti,
             ip=ip_addr,
             ip_len=ip_length,
             vrf_id=vrf_id)

        if rt5_dict:
            comm_list = rt5_dict["ext_community"]

            if isinstance(expected_rt, str):
                if expected_rt in comm_list:
                    return True
            else:
                if not set(expected_rt).difference(set(comm_list)):
                    return True
             
        timeout.sleep()

    if not rt5_dict:
        log.error("Unable to get rt5 data")
    else:
        log.error('Expected route target is {expected_rt} actual is'
            '{actual_rt}'.format(expected_rt=expected_rt, actual_rt=comm_list)
        )

    return False


def verify_bgp_rt5_label(
    device, address_family, eti, ip_addr, ip_length, vrf_id, expected_label, 
    max_time=30, check_interval=10
):
    """ Verify bgp for specific label existstance in 
        'show ip bgp {address_family} route-type 5 {eti} {ip_addr} {ip_length}'

        Args:
            device ('obj'): device to use
            address_family ('str'): address family
            eti ('str'):Ethernet tag in decimal <0-4294967295>
            ip_addr('str'): IP ADDRESS
            ip_length('str'): Ip length
            vrf_id ('str'): vrf
            expected_label('str'): Expected Label
            max_time ('int', optional): maximum time to wait in seconds, 
                default is 30
            check_interval ('int', optional): how often to check  in seconds, 
                default is 10
        Example:
            EVPN ESI: 00000000000000000000, Gateway Address: 0.0.0.0, 
            VNI Label 3000101, MPLS VPN Label 0
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        label_dict = device.api.get_bgp_rt5_community_paths_label(
             device=device,
             address_family=address_family,
             eti=eti,
             ip=ip_addr,
             ip_len=ip_length,
             vrf_id=vrf_id)

        if label_dict:
            label_list = label_dict["vni_labels"]

            if expected_label in label_list:
                return True

        timeout.sleep()

    if not label_dict:
        log.error("Could not get the vrf {} data".format(vrf_id))
    else:
        log.error('Expected route target label is "{expected_label}" '
            'actual is "{actual_label}"'.format(expected_label=
                expected_label, actual_label=label_list)
        )
   
    return False


def verify_bgp_rt2_label(
    device, address_family, eti, mac_addr, ip_addr, vrf_id, 
    expected_label, max_time=30, check_interval=10
):
    """ Verify bgp label for routetype 2 in 'show ip bgp {address_family}
        route-type 2 {eti} {mac} {ip}'

        Args:
            device ('obj'): device to use
            address_family ('str'): address family
            eti ('str'):Ethernet tag in decimal <0-4294967295>
            mac_addr('str'): Mac address
            ip_addr('str'): Ip address
            vrf_id ('str'): vrf
            expected_label('str'): Expected label 
            max_time ('int', optional): maximum time to wait in seconds,
                default is 30
            check_interval ('int', optional): how often to check in seconds,
                default is 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():

        rt2_dict = device.api.get_bgp_rt2_community_label(
             device=device,
             address_family=address_family,
             eti=eti,
             mac=mac_addr,
             ip=ip_addr,
             vrf_id=vrf_id)

        if rt2_dict:
            label_list = rt2_dict["labels"]

            if expected_label in label_list:
                return True

        timeout.sleep()

    if not rt2_dict:
        log.error("Could not get rt2 data, output is empty")
    else:
        log.error('Expected route target label is "{expected_label}" '
            'actual is "{actual_label}"'.format(expected_label=
                expected_label, actual_label=label_list)
        )

    return False


def verify_bgp_evi_rt2_mac_localhost(
    device, address_family, evi, mac, expected_host, max_time=30, check_interval=10
):
    """ Verify bgp local host in for route type 2 mac in 'show ip bgp 
         {address_family} evi route-type 2 0 {mac} *'
 
         Args:
             device ('obj'): device to use
             address_family ('str'): address family
             evi ('str'): evi instance
             mac('str'): Mac address
             expected_host('str'): Expected local host
             max_time ('int', optional): maximum time to wait in seconds,
                 default is 30
             check_interval ('int', optional): how often to check in seconds,
                 default is 10
         Returns:
             result ('bool'): verified result
         Raises:
             None
    """
    timeout = Timeout(max_time, check_interval)
    rt2_evi_out = ''
    while timeout.iterate():
        try:
            rt2_evi_out = device.parse("show ip bgp {} evi {} route-type " \
                " 2 0 {} *".format(address_family,evi,mac)
            )
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        if rt2_evi_out:
            actual_evi = 'evi' + "_" + evi
            addr_family = rt2_evi_out['instance']['default']['vrf'][actual_evi]\
                          ['address_family'][address_family]
            for prefix in addr_family.get('prefixes', {}):
                nlr = addr_family['prefixes'][prefix].get('nlri_data', {})
                rd = nlr['rd']
                actual_host = rd.split(":")
                if actual_host[0] == expected_host:
                    return True
    return False


def verify_bgp_neighbor_state(
    device, address_family, expected_state, neighbor_address=None,
    vrf=None, max_time=30, check_interval=10
):
    """ Verify bgp neighbor state in 'show ip bgp l2vpn evpn summary' or
        state for particular neighbor if neighbor_address is given.
             
        Args:
            device ('obj'): device to use
            address_family ('str'): address family
            expected_state ('str'): Expected state(Idle or number)
            neighbor_address ('str',optional): Neighbor ip address
                default is none
            vrf('str',optional): vrf id, default is none 
            max_time ('int', optional): maximum time to wait in seconds,
                default is 30
            check_interval ('int', optional): how often to check in seconds,
                default is 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """ 
    timeout = Timeout(max_time, check_interval)
    # Assigning vrf as 'default' incase of no vrf
    # to get states related to default vrf
    if not vrf:
        new_vrf = "default"
    else:
        new_vrf = vrf

    while timeout.iterate():
        summary = device.api.get_ip_bgp_summary(
             address_family=address_family,
             vrf=vrf,
             )
        if summary:
            # verifying for neghbor state incase of neghbor address is given
            if neighbor_address:
                state_rcvd = summary["vrf"][new_vrf]["neighbor"][neighbor_address]\
                    ["address_family"][address_family]["state_pfxrcd"]
                if expected_state == state_rcvd:
                    return True
            else:
                all_states = []
                # Collecting all states of all neigbors
                for neighbor in summary["vrf"][new_vrf].get("neighbor",{}):
                    state = summary['vrf'][new_vrf]['neighbor'][neighbor]\
                        ["address_family"][address_family]["state_pfxrcd"]
                    all_states.append(state)
                #Verifying state in actual states
                if expected_state in all_states:
                    return True
        timeout.sleep()

    if not summary:
        log.error("Could not get neighbors and states data, output is empty")

    return False


def verify_bgp_neighbor_route_zero_prefixes(device, address_family, neighbor):
    """ Verify for zero number of prefixes in 'show ip bgp {address_family} 
        neighbors {neighbor} routes'

        Args:
            device ('obj'): device to use
            address_family ('str'): address family
            neighbor ('str'): neighbor ip 
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    total_prefixes = ""
    try:
        total_prefixes = device.parse("show ip bgp {} neighbors {} routes".format \
               (address_family, neighbor)
            )
    except SchemaEmptyParserError as e:
        return False
    
    if total_prefixes.get("total_num_of_prefixes") == 0:
        return True

    return False


def verify_bgp_evi_orig_route(
    device, address_family, evi, rd, expected_orig_route, max_time=30, check_interval=10
):
    """ Verify bgp evi originated route related to particular rd in 'show ip
        bgp {address_family} evi {evi} detail'

        Args:
            device ('obj'): device to use
            address_family ('str'): address family
            evi ('str'):Ethernet tag in decimal <0-4294967295>
            rd ('str'): Route distinguisher
            expected_orig_route ('str'): Expected originated route
            max_time ('int', optional): maximum time to wait in seconds,
                default is 30
            check_interval ('int', optional): how often to check in seconds,
                default is 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    evi_out = ''
    while timeout.iterate():
        try:
            evi_out = device.parse("show ip bgp {} evi {} detail".format( \
                address_family,evi)
            )
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        if evi_out:
            actual_evi = 'evi' + "_" + evi
            addr_family = evi_out['instance']['default']['vrf'][actual_evi] \
                ['address_family'][address_family]
            for prefix in addr_family.get('prefixes', {}):
                nlr = addr_family['prefixes'][prefix].get('nlri_data', {})
                actual_rd = nlr["rd"].split(":")
                if (actual_rd[0] == rd) and ("orig_rtr_id" in nlr.keys()):
                    if nlr['orig_rtr_id'] == expected_orig_route:
                        return True
    return False


def verify_bgp_evi_mac_ipprefix(
    device, address_family, evi, expected_rd, expected_mac, expected_ipprx, \
    max_time=30, check_interval=10
):
    """ Verify bgp evi ip prefix related to particular rd and mac in 
        'show ip bgp {address-family} evi {evi} detail'

        Args:
            device ('obj'): device to use
            address_family ('str'): address family
            evi ('str'): evi instance
            expected_rd ('str'): expected rd 
            expected_mac ('str'): Expected mac
            expected_ipprx ('str'): Expected ip prefix
            max_time ('int', optional): maximum time to wait in seconds,
                default is 30
            check_interval ('int', optional): how often to check in seconds,
                default is 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    evi_out = ''
    while timeout.iterate():
        try:
            evi_out = device.parse("show ip bgp {} evi {} detail".format( \
                address_family,evi)
            )
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        actual_evi = 'evi' + "_" + evi
        if evi_out:
            addr_family = evi_out['instance']['default']['vrf'][actual_evi] \
            ['address_family'][address_family]
            for prefix in addr_family.get('prefixes', {}):
                nlr = addr_family['prefixes'][prefix].get('nlri_data', {})
                actual_rd = nlr["rd"].split(":")
                if (actual_rd[0] == expected_rd) and ('mac' and 'ip_prefix' in nlr.keys()):
                    if (nlr['mac'] == expected_mac.upper()) and (nlr['ip_prefix'] == expected_ipprx):
                        return True
    return False


def verify_bgp_l2vpn_evpn_rt2_ipprefix(
    device, expected_ipprefix, expected_rd=None, max_time=30, check_interval=10
):
    """ Verify bgp l2vpn evpn rt2 ip prefix related to particular rd  in 
        'show ip bgp l2vpn evpn all'

        Args:
            device ('obj'): device to use
            expected_ipprefix ('list'): expected ip prefix
            expected_rd ('str'): expected rd 
            max_time ('int', optional): maximum time to wait in seconds,
                default is 30
            check_interval ('int', optional): how often to check in seconds,
                default is 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show ip bgp l2vpn evpn all")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        if out:    
            # collecting all the routes 
            routes = out.q.get_values("routes")
            route_type_2_prefixes = dict()
            for route in routes:
                # [2][1.1.1.1:1][0][48][DEC856540245][128][2000::DCC8:56FF:FE54:245]/36
                # [2][1.1.1.1:1][0][48][A03D6EC594E4][0][*]/20
                data_found = re.search("\[2\]\[(.*)\].*\[(.*)\]",route)
                if data_found:
                    # 1.1.1.1:1][0][48]
                    rd_list=data_found.groups()[0].split("][")
                    # 1.1.1.1:1                    
                    rd = rd_list[0]
                    # 2000::DCC8:56FF:FE54:245
                    prfx=data_found.groups()[1]
                    # Adding to a dictionary
                    if rd not in route_type_2_prefixes.keys():
                        route_type_2_prefixes[rd]=[]
                    # Appending prefixes to correspondin
                    route_type_2_prefixes[rd].append(prfx)  
            # checking for matching list of routetype 2 prefixes related to RD        
            if expected_rd and (expected_rd in route_type_2_prefixes.keys()): 
                not_exists_ipprfx_list = [prfx for prfx in expected_ipprefix if \
                    prfx not in route_type_2_prefixes[expected_rd]]            
                if len(not_exists_ipprfx_list) == 0:         
                    return True  
            # checking for matching list of routetype 5 prefixes incase of no RD given
            if (not expected_rd):
                all_prfx = []
                for each_record in route_type_2_prefixes.values():
                    if isinstance(each_record,list):
                        for prefix in each_record:
                            all_prfx.append(prefix)
                    else:
                        all_prfx.append(each_record)
                not_exists_ipprfx_list = [prfx for prfx in expected_ipprefix if prfx not in all_prfx]
                if len(not_exists_ipprfx_list) == 0:         
                    return True
        
        timeout.sleep()

    if out and expected_rd:
        log.error("Unable to find route-type 2 expected ipprefix i.e {} for "\
        " rd {} in actual list {}".format(expected_ipprefix,\
            expected_rd,route_type_2_prefixes))
    elif out and (not expected_rd):
        log.error("Unable to find route-type 2 expected ipprefix i.e {} in "\
        "actual list {}".format(expected_ipprefix,route_type_2_prefixes))
    else:
        log.error("Unable to get the parsed output")

    return False


def verify_bgp_l2vpn_evpn_rt5_ipprefix(
    device, expected_ipprefix, expected_rd=None,max_time=30, check_interval=10
):
    """ Verify bgp l2vpn evpn rt5 ip prefix related to particular rd  in 
        'show ip bgp l2vpn evpn all'

        Args:
            device ('obj'): device to use
            expected_ipprefix ('str'): expected ip prefix
            expected_rd ('str'): expected rd optional
            max_time ('int', optional): maximum time to wait in seconds,
                default is 30
            check_interval ('int', optional): how often to check in seconds,
                default is 10
            Internally have a dictionary that have 'rd' as keys and 'ip prefixes' as values
            example:
                {
                '1.1.1.1': ['*', '2000::22', '2000::21', '20.20.20.21', '2000::14F7:9FF:FE42:9AF5'], 
                '2.2.2.2': ['20.20.20.21', '20.20.20.1', '2000::1', '*', '2000::14F7:9FF:FE42:9AF5']
                }
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show ip bgp l2vpn evpn all")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue   
        if out:     
            # collecting all the routes 
            routes = out.q.get_values("routes")
            route_type_5_prefixes = dict()
            for route in routes:
                # [5][1002:1][0][24][6.6.6.0]/17
                # [5][1002:1][0][64][2060::]/29
                data_found = re.search("\[5\]\[(.*)\].*\[(.*)\]",route)
                if data_found:
                    # 1002:1][0][64]
                    rd_list=data_found.groups()[0].split("][")
                    # 1002:1                    
                    rd=rd_list[0]
                    # 6.6.6.0
                    prfx=data_found.groups()[1]
                    if rd not in route_type_5_prefixes.keys():
                        route_type_5_prefixes[rd]=[]
                    # appending prefixes to corresponding rd
                    route_type_5_prefixes[rd].append(prfx)                  
            
            # checking for matching list of routetype 5 prefixes related to RD 
            if expected_rd and (expected_rd in route_type_5_prefixes.keys()): 
                not_exists_ipprfx_list = []           
                not_exists_ipprfx_list = [prfx for prfx in expected_ipprefix if \
                    prfx not in route_type_5_prefixes[expected_rd]]
                if len(not_exists_ipprfx_list) == 0:         
                    return True  
            # checking for matching list of routetype 5 prefixes incase of no RD given
            if (not expected_rd):
                all_prfx = []
                not_exists_ipprfx_list = []
                for each_record in route_type_5_prefixes.values():
                    if isinstance(each_record,list):
                        for prefix in each_record:
                            all_prfx.append(prefix)
                    else:
                        all_prfx.append(each_record)
                not_exists_ipprfx_list = [prfx for prfx in expected_ipprefix if prfx not in all_prfx]
                if len(not_exists_ipprfx_list) == 0:
                    return True
                
        timeout.sleep()

    if out and expected_rd:
        log.error("Unable to find route-type 5 expected ipprefix i.e {} for "\
        " rd {} in actual list {}".format(expected_ipprefix,\
            expected_rd,route_type_5_prefixes))
    elif out and (not expected_rd):
        log.error("Unable to find route-type 5 expected ipprefix i.e {} in "\
        "actual list {}".format(expected_ipprefix,route_type_5_prefixes))
    else:
        log.error("Unable to get the parsed output")

    return False


def verify_bgp_rt5_mvpn_all_ip_mgroup(
    device, ip_family,expected_ip, expected_mgroup, expected_rd=None,
    max_time=30, check_interval=10
):
    """ Verify bgp rd(if given),ip and mgroup for routetype 5 route in 
        'show ip bgp ipv4/ipv6 mvpn all'

        Args:
            device ('obj'): device to use
            ip_family ('str'): ipv4 or ipv6
            expected_ip ('str'): expected ip
            expected_mgroup ('str'): expected multicast group
            expected_rd ('str', optional): rd if given
            vrf ('str', optional): vrf if given
            max_time ('int', optional): maximum time to wait in seconds,
                default is 30
            check_interval ('int', optional): how often to check in seconds,
                default is 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    if ip_family not in ['ipv4','ipv6']:
        log.error("Please provide ip_family either as ipv4 or ipv6,provided value is {}".format(ip_family))
        return False
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show ip bgp {ip_family} mvpn all".format\
                (ip_family=ip_family))
        except SchemaEmptyParserError as e:
            log.error("Failed to parse command 'show ip bgp {ip_family} "\
                "mvpn all': {e}".format(ip_family=ip_family, e=str(e)))
            timeout.sleep()
            continue
            
        # incase of empty output
        if out:
            routes = out.q.get_values("routes")
            for route in routes:                
                data_found = re.search("\[5\]\[(.*)\]+",route)
                if data_found:
                    local_lis = []
                    # 1002:1][16843009][20.20.20.22/32][232.1.1.6/32
                    whole_data = (data_found.groups()[0]).split("][")
                    entry_len = len(whole_data)
                    # Adding rd, ip, mgroup ip
                    data=[whole_data[0],whole_data[entry_len-2],whole_data[entry_len-1]]
                    for values in data:
                        # 20.20.20.22/32
                        if "/" in values:
                            local_lis.append((values.split("/"))[0])
                        else:
                            local_lis.append(values)
                    if expected_rd:                      
                        if (local_lis[0] == expected_rd) and (local_lis[1] == expected_ip)\
                             and (local_lis[2] == expected_mgroup):
                            return True
                    if (not expected_rd):
                        if (local_lis[1] == expected_ip) and \
                            (local_lis[2] == expected_mgroup):
                            return True
        timeout.sleep()
    return False


def verify_bgp_rt7_mvpn_all_ip_mgroup(
    device,ip_family, expected_ip, expected_mgroup, expected_rd=None,
    max_time=30, check_interval=10
):
    """ Verify bgp rd(if given),ip and mgroup for routetype 7 route in 
        'show ip bgp ipv4/ipv6 mvpn all'

        Args:
            device ('obj'): device to use
            ip_family ('str'): either ipv4 or ipv6
            expected_ip ('str'): expected ip
            expected_mgroup ('str'): expected multicast group
            expected_rd ('str', optional): rd if given
            vrf ('str', optional): vrf if given
            max_time ('int', optional): maximum time to wait in seconds,
                default is 30
            check_interval ('int', optional): how often to check in seconds,
                default is 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    if ip_family not in  ['ipv4','ipv6']:
        log.error("Please provide ip_family either as ipv4 or ipv6")
        return False
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show ip bgp {ip_family} mvpn all".format\
                (ip_family=ip_family))
        except SchemaEmptyParserError as e:
            log.error("Failed to parse command 'show ip bgp {ip_family} "\
                "mvpn all': {e}".format(ip_family=ip_family, e=str(e)))
            timeout.sleep()
            continue
            
        # incase of empty output
        if out:
            routes = out.q.get_values("routes")
            for route in routes:                
                data_found = re.search("\[7\]\[(.*)\]+",route)
                if data_found:
                    local_lis = []
                    # 1002:1][16843009][20.20.20.22/32][232.1.1.6/32
                    whole_data = (data_found.groups()[0]).split("][")
                    entry_len = len(whole_data)
                    # Adding rd, ip, mgroup ip
                    data=[whole_data[0],whole_data[entry_len-2],whole_data[entry_len-1]]
                    for values in data:
                        # 20.20.20.22/32
                        if "/" in values:
                            local_lis.append((values.split("/"))[0])
                        else:
                            local_lis.append(values)
                    if expected_rd:             
                        if (local_lis[0] == expected_rd) and (local_lis[1] == expected_ip)\
                             and (local_lis[2] == expected_mgroup):
                            return True
                    if (not expected_rd): 
                        if (local_lis[1] == expected_ip) and \
                            (local_lis[2] == expected_mgroup):
                            return True
        timeout.sleep()
    return False


def verify_bgp_l2vpn_evpn_rt2_nxthop(
    device, expected_rd, expected_nexthop, expected_prefix=None, max_time=30, check_interval=10
):
    """ Verify bgp l2vpn evpn rt2 ip nexthop related to particular rd  and 
        related to particular source ip (if given)in 'show ip bgp l2vpn evpn all'

        Args:
            device ('obj'): device to use            
            expected_rd ('str'): expected rd 
            expected_nexthop ('str'): expected next hop
            expected_prefix ('str'): expected source ip
            max_time ('int', optional): maximum time to wait in seconds,
                default is 30
            check_interval ('int', optional): how often to check in seconds,
                default is 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
        Example:
            *>   [2][3.3.3.3:1][0][48][A03D6EC594E4][128][FE80::A23D:6EFF:FEC5:94E4]/36
                      3.3.3.3                                0 1000 1003 ?
            where rd - 3.3.3.3:1, prefix- FE80::A23D:6EFF:FEC5:94E4, nexthop - 3.3.3.3

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show ip bgp l2vpn evpn all")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        if out:        
            # collecting all the routes 
            routes = out.q.get_values("routes")
            for route in routes:
                # [2][1.1.1.1:1][0][48][DEC856540245][128][2000::DCC8:56FF:FE54:245]/36
                # [2][1.1.1.1:1][0][48][A03D6EC594E4][0][*]/20
                data_found = re.search("\[2\]\[(.*)\].*\[(.*)\]",route)
                if data_found:
                    # 1.1.1.1:1][0][48]
                    rd_list=data_found.groups()[0].split("][")
                    # 1.1.1.1:1
                    rd = rd_list[0]
                    # 2000::DCC8:56FF:FE54:245
                    prfx=data_found.groups()[1]
                    if expected_prefix:
                        if expected_rd == rd and expected_prefix == prfx:
                            # Getting next hop ip address
                            actual_nxthop = out.q.contains("routes").contains(route).get_values('next_hop')
                            if expected_nexthop in actual_nxthop:
                                return True
                    else:
                        if expected_rd == rd :
                            actual_nxthop = out.q.contains("routes").contains(route).get_values('next_hop')
                            if expected_nexthop in actual_nxthop:
                                return True

        timeout.sleep()
    return False


def verify_bgp_l2vpn_evpn_rt5_nxthop(
    device, expected_rd, expected_nexthop, expected_prefix=None, max_time=30, check_interval=10
):
    """ Verify bgp l2vpn evpn rt5 ip nexthop related to particular rd  and 
        related to particular source ip(if given) in 'show ip bgp l2vpn evpn all'

        Args:
            device ('obj'): device to use            
            expected_rd ('str'): expected rd 
            expected_nexthop ('str'): expected next hop
            expected_prefix ('str'): expected source ip
            max_time ('int', optional): maximum time to wait in seconds,
                default is 30
            check_interval ('int', optional): how often to check in seconds,
                default is 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
        Example:
             *>   [5][1003:1][0][64][2069::]/29
                      3.3.3.3                                0 1000 1003 ?
             where rd - 1003:1, prefix - 2069::, nexthop - 3.3.3.3

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show ip bgp l2vpn evpn all")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        if out:        
            # collecting all the routes 
            routes = out.q.get_values("routes")
            for route in routes:
                # [5][1002:1][0][24][6.6.6.0]/17
                # [5][1002:1][0][64][2060::]/29
                data_found = re.search("\[5\]\[(.*)\].*\[(.*)\]",route)
                if data_found:
                    # 1002:1][0][64]
                    rd_list=data_found.groups()[0].split("][")
                    # 1002:1
                    rd=rd_list[0]
                    # 6.6.6.0
                    prfx=data_found.groups()[1]
                    if expected_prefix:
                        if expected_rd == rd and expected_prefix == prfx:
                            actual_nxthop = out.q.contains("routes").contains(route).get_values('next_hop')
                            if expected_nexthop in actual_nxthop:
                                return True
                    else:
                        if expected_rd == rd :
                            actual_nxthop = out.q.contains("routes").contains(route).get_values('next_hop')
                            if expected_nexthop in actual_nxthop:
                                return True
        timeout.sleep()
    return False
