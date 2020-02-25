"""Common verification functions for bgp"""

# Python
import logging
import copy

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
    get_routing_routes,
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
    prefixes = get_routing_routes(
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