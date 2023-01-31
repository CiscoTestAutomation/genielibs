"""Common verify functions for routing"""

# Python
import re
import logging
from prettytable import PrettyTable
from time import sleep

# pyATS
from pyats.utils.objects import find, R

# Genie
from genie.libs.sdk.apis.iosxe.routing import util as util
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# BGP
from genie.libs.sdk.apis.iosxe.bgp.get import (
    get_bgp_route_from_neighbors,
    get_bgp_neighbors_advertised_routes,
)

# ROUTING
from genie.libs.sdk.apis.iosxe.routing.get import get_routing_routes
from genie.libs.sdk.apis.iosxe.routing.get import (
    get_routing_repair_path_information,
)

log = logging.getLogger(__name__)


def verify_ip_cef_nexthop_label(device, ip, expected_label=None, vrf='default',
                                table=None, max_time=30, check_interval=10):
    """ Verify ip cef nexthop does (not) have expected label

        Args:
            device (`obj`): Device object
            ip (`str`): IP address
            expected_label (`str`): Expected label. None if no label expected
            vrf (`str`): Vrf name
            table (`str`): Not used on IOSXE
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    if vrf and vrf != 'default':
        cmd = 'show ip cef vrf {vrf} {ip} detail'.format(vrf=vrf, ip=ip)
    else:
        cmd = 'show ip cef {} detail'.format(ip)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{}':\n{}".format(cmd, e))
            timeout.sleep()
            continue

        reqs = R(['vrf', vrf, 'address_family', '(.*)', 
                  'prefix', '(.*)', 'nexthop', '(.*)', 
                  'outgoing_interface', '(?P<interface>.*)',
                  'outgoing_label', '(?P<outgoing_label>.*)'])
        found = find([out], reqs, filter_=False, all_keys=True)

        if expected_label:
            if found:
                for item in found:
                    interface = item[1][-2]
                    label = ' '.join(item[0])
                    log.info("Found outgoing interface '{}' has outgoing label '{}', "
                             "expected to have label '{}'"
                             .format(interface, label, expected_label))

                    if expected_label in label:
                        return True
            else:
                log.error("Failed to get outgoing label for '{}'".format(ip))
                timeout.sleep()
                continue
        else:
            if found:
                log.error("Found outgoing label for '{}', "
                          "but expected no label".format(ip))
                timeout.sleep()
                continue
            else:
                log.info("No outgoing label aftar the nexthop info for '{}'"
                         .format(ip))
                return True

        timeout.sleep()

    return False


def verify_rib_fib_lfib_consistency(device, route, none_pattern='', 
                                    max_time=30, check_interval=10):
    """ Verify the outgoing label for route are the same in:
        - show ip route <route>
        - show ip cef <route>
        - show mpls forwarding-table <route>

        Args:
            device (`obj`): Device object
            route (`str`): Route or ipn
            none_pattern (`list`): None label pattern
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
        Returns:
            result (`bool`): Verified result
    """
    route = route.split('/')
    if len(route) > 1:
        route = '{} {}'.format(route[0], device.api.int_to_mask(int(route[1])))
    else:
        route = route[0]

    patterns = ['No Label', 'implicit-null', 'Pop Label', 'none', '']
    if none_pattern:
        patterns.extend(none_pattern)

    cmd1 = "show ip route {}".format(route)
    cmd2 = "show ip cef {}".format(route)
    cmd3 = "show mpls forwarding-table {}".format(route)

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        result = True
        table = PrettyTable()
        table.field_names = ['RIB (INTF)', 'RIB (NH)', 'RIB (LABEL)', 
                             'FIB (INTF)', 'FIB(NH) ', 'FIB (LABEL)', 
                             'FIB (LOCAL LABEL)', 'LFIB (INTF)', 'LFIB(NH)', 
                             'LFIB (LABEL)', 'LFIB (LOCAL LABEL)', 'PASS/FAIL']

        try:
            out1 = device.parse(cmd1)
        except Exception as e:
            log.error("Failed to parse '{}':\n{}".format(cmd1, e))
            result = False
            timeout.sleep()
            continue

        try:
            out2 = device.parse(cmd2)
        except Exception as e:
            log.error("Failed to parse '{}':\n{}".format(cmd2, e))
            result = False
            timeout.sleep()
            continue

        try:
            out3 = device.parse(cmd3)
        except Exception as e:
            log.error("Failed to parse '{}':\n{}".format(cmd3, e))
            result = False
            timeout.sleep()
            continue

        reqs1 = R(['entry', '(.*)',
                   'paths', '(.*)',
                   '(?P<route>.*)'])
        found1 = find([out1], reqs1, filter_=False, all_keys=True)
        route_dict1 = {}
        # eg: {"GigabitEthernet2": {
        #         "nexthop": "10.0.0.5",
        #         "from": "10.16.2.2",
        #         "age": "2w0d",
        #         "interface": "GigabitEthernet2",
        #         "prefer_non_rib_labels": true,
        #         "merge_labels": true,
        #         "metric": "3",
        #         "share_count": "1",
        #         "mpls_label": "16002",
        #         "mpls_flags": "NSF"}}

        if found1:
            for item in found1:
                route_dict1.update({item[0]['interface']: item[0]})
        else:
            log.error("Failed to find route from '{}'".format(cmd1))
            result = False
            timeout.sleep()
            continue

        reqs2 = R(['vrf', '(.*)',
                   'address_family', '(.*)',
                   'prefix', '(.*)', 'nexthop', '(?P<nexthop>.*)',
                   'outgoing_interface', '(?P<interface>.*)', '(?P<sub>.*)'])
        found2 = find([out2], reqs2, filter_=False, all_keys=True)
        route_dict2 = {}
        # eg: {'GigabitEthernet2': {
        #        'local_label': 16002, 
        #        'outgoing_label': ['16002'], 
        #        'nexthop': '10.0.0.5'}}

        if found2:
            for item in found2:
                interface = item[1][-1]
                nexthop = item[1][-3]
                item[0].update({'nexthop': nexthop})
                route_dict2.update({interface: item[0]})
        else:
            log.error("Failed to find outgoing interface from '{}'".format(cmd2))
            result = False
            timeout.sleep()
            continue

        reqs3 = R(['vrf', '(.*)',
                   'local_label', '(?P<local_label>.*)',
                   'outgoing_label_or_vc', '(?P<outgoing_label>.*)',
                   'prefix_or_tunnel_id', '(?P<prefix>.*)',
                   'outgoing_interface', '(?P<interface>.*)',
                   'next_hop', '(?P<next_hop>.*)'])
        found3 = find([out3], reqs3, filter_=False, all_keys=True)
        route_dict3 = {}
        # eg: {'GigabitEthernet4': {
        #         "local_label": 16,
        #         "outgoing_label": "Pop Label",
        #         "prefix": "10.0.0.13-A",
        #         "interface": "GigabitEthernet4",
        #         "next_hop": "10.0.0.13"}}

        if found3:
            keys = GroupKeys.group_keys(reqs=reqs3.args, ret_num={}, 
                                        source=found3, all_keys=True)
            for item in keys:
                route_dict3.update({item['interface']: item})
        else:
            log.error("Failed to get outgoing interface from '{}'".format(cmd3))
            result = False
            timeout.sleep()
            continue

        if len(route_dict1) != len(route_dict2) != len(route_dict3):
            log.error("The number of routes are different in the 3 output")
            result = False
            timeout.sleep()
            continue

        for interface in route_dict1.keys():
            # get info from show ip route
            rib_intf = interface
            rib_nh = route_dict1[interface].get('nexthop', '')
            rib_label = route_dict1[interface].get('mpls_label', '')
            tmp_rib_label = None if rib_label in patterns else rib_label

            # get info from show ip cef
            fib_intf = interface if route_dict2.get(interface, '') else ''
            fib_nh = route_dict2.get(interface, {}).get('nexthop', '')
            fib_label = ' '.join(route_dict2.get(interface, {}).get('outgoing_label', []))
            fib_local = route_dict2.get(interface, {}).get('local_label', '')
            tmp_fib_label = None if fib_label in patterns else fib_label

            # get info from show mpls forwarding table
            lfib_intf = interface if route_dict3.get(interface, '') else ''
            lfib_nh = route_dict3.get(interface, {}).get('next_hop', '')
            lfib_label = route_dict3.get(interface, {}).get('outgoing_label', '')
            lfib_local = route_dict3.get(interface, {}).get('local_label', '')
            tmp_lfib_label = None if lfib_label in patterns else lfib_label

            # if multiple entried forwarding table and prefer not rib labels, only check rib and lfib lable
            # other wise check all labels
            if (len(found3)>1 and route_dict1[interface].get('prefer_non_rib_labels') and (
                    tmp_rib_label == tmp_lfib_label and
                    rib_intf == fib_intf == lfib_intf and
                    rib_nh == fib_nh == lfib_nh)) \
                or (rib_intf == fib_intf == lfib_intf and
                 rib_nh == fib_nh == lfib_nh and
                 tmp_rib_label == tmp_fib_label == tmp_lfib_label):

                status='PASS'

            else:
                result = False
                status = 'FAIL'

            table.add_row([rib_intf, rib_nh, rib_label,
                           fib_intf, fib_nh, fib_label, fib_local,
                           lfib_intf, lfib_nh, lfib_label, lfib_local, status])

        log.info("Summary Result for {}:\n{}".format(route, table))

        if result is True:
            return result

        timeout.sleep()

    return result


def verify_routing_local_and_connected_route(device, vrf):
    """ Verify there is local and connected route registered for the vrf

        Args:
            device (`obj`): Device object
            vrf (`str`): Vrf name
        Returns:
            (`dict`): Interface dict contain ip route info
            False
        Raises:
            None
     """
    intf_dict = {}

    out = device.execute("show ip route vrf {} connected".format(vrf))
    if not out:
        return False

    p = re.compile(
        r"(?m)^\s*(?P<type>L|C) +(?P<ip>[\d\.]+).*, +(?P<intf>[\w\.\/]+)"
    )
    route_list = p.findall(out)

    for route in route_list:
        intf_dict.setdefault(route[2], {}).update({route[0]: route[1]})

    for intf, route_data in intf_dict.items():
        if len(route_data) < 2:
            return False

    return intf_dict


def verify_routing_route_ip_on_interface(device, interface_dict):
    """ Verify routes match the configured IP address in running config

        Args:
            device (`obj`): Device object
            interface_dict (`dict`): Interface dict contain ip route info. Get from libs/routing/verify.py::verify_routing_local_and_connected_route
        Returns:
            True / False
        Raises:
            None
    """
    for intf, data in interface_dict.items():
        log.info("Verify configured route ip on {}".format(intf))

        ip = data["L"]
        out = device.execute("show running-config interface {}".format(intf))

        if ip in out:
            log.info(
                "Matched route ip {ip} on {intf}".format(ip=ip, intf=intf)
            )
            return True
        else:
            return False


def verify_routing_ip_routes(
    device,
    route,
    interface=None,
    destination_address=None,
    output=None,
    repeat=0,
):
    """ Verify ip route exists

        Args:
            device ('str'): Device str
            route ('str'): ip address to verify
            interface ('str'): interface name to verify
            destination_address ('str'): detsination ip address to verify
            output ('str'): output provided as argument
            repeat ('int'): repeat value
        Returns:
            True / False
        Raises:
            None
    """
    if not output:
        output = device.execute("show running-config | include ip route")
    route_format = route
    if repeat > 0:
        for i in range(repeat):
            route = route.format(x=str(i + 1))
            result = verify_routing_ip_routes(
                device=device,
                route=route,
                interface=interface,
                destination_address=destination_address,
                output=output,
                repeat=0,
            )
            if not result:
                return False
            route = route_format
        return True
    else:
        m = None

        if interface and destination_address:
            p1 = re.compile(
                r"ip +route +{route} +[\d\.]+ +"
                "{interface} +{destination_address}".format(
                    route=route,
                    interface=interface,
                    destination_address=destination_address,
                )
            )
        elif interface:
            p1 = re.compile(
                r"ip +route +{route} +[\d\.]+ +{interface}".format(
                    route=route, interface=interface
                )
            )
        elif destination_address:
            p1 = re.compile(
                r"ip +route +{route} +[\d\.]+ +{destination_address}".format(
                    route=route, destination_address=destination_address
                )
            )

        m = p1.search(output)

        if m:
            return True
        else:
            return False


def verify_routing_static_routes(
    device,
    route,
    interface=None,
    destination_address=None,
    output=None,
    repeat=0,
):
    """ Verify static route exists

        Args:
            device ('str'): Device str
            route ('str'): ip address to verify
            interface ('str'): interface name to verify
            destination_address ('str'): detsination ip address to verify
            output ('str'): output from 'show ip route static'
            repeat ('int'): repeat value
        Returns:
            True / False
        Raises:
            None
    """
    route_format = route
    if not output:
        output = device.execute("show ip route static")

    if repeat > 0:
        for i in range(repeat):
            route = route.format(x=str(i + 1))
            result = verify_routing_static_routes(
                device=device,
                route=route,
                interface=interface,
                destination_address=destination_address,
                output=output,
                repeat=0,
            )
            if not result:
                return False
            route = route_format
        return True
    else:
        m = None
        if interface and destination_address:
            p1 = re.compile(
                r"{route}(\/\d+)? +\[\d+\/\d+\] +via +{destination_address}"
                ", +{interface}".format(
                    route=route,
                    destination_address=destination_address,
                    interface=interface,
                )
            )
        elif interface:
            p1 = re.compile(
                r"{route}(\/\d+)? +is +directly +connected, +{interface}".format(
                    route=route, interface=interface
                )
            )
        elif destination_address:
            p1 = re.compile(
                r"{route}(\/\d+)? +\[\d+\/\d+\] +via +{destination_address}".format(
                    route=route, destination_address=destination_address
                )
            )

        m = p1.search(output)
        if m:
            return True
        else:
            return False


# Note: Keep this API in line with verify_static_routing_route_attrs() if
# extending.
def verify_routing_route_attrs(device, route, address_family='ipv4',
                               vrf_name=None, route_attrs=None,
                               next_hop_info=None, max_time=60,
                               check_interval=10):
    """Verify default IPv4 route exists with given properties.

    Args:
        device (obj): Device to verify route on.
        route (str): route to verify.
        address_family (str, optional): address family of route ("ipv4" or "ipv6"). Defaults to "ipv4".
        vrf_name (str, optional): vrf name to verify route on. Defaults to None.
        route_attrs (obj, optional): If specified, verify the specified attributes in the route. Defaults to None.
        next_hop_info (obj, optional): If specified, next hop info to confirm a matching entry in the route. Defaults to None.
            next_hop_info is of format:
                {
                    "next_hop": "172.20.190.110",
                    "updated": "5w6d",
                    "outgoing_interface": "TenGigabitEthernet1/1/4"
                }
            where all keys are optional; ony the keys specified will be
            checked. If no keys are given, then no keys are checked and this
            will be considered a match.
        max_time (int, optional): Maximum timeout (seconds). Defaults to 60.
        check_interval (int, optional): Check interval (seconds). Defaults to 10.

    Returns:
        bool: True if route is verified, False otherwise.
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        routes = None
        if address_family == 'ipv4':
            routes = device.api.get_routing_routes(vrf=vrf_name,
                                                   address_family='ipv4')
        elif address_family == 'ipv6':
            routes = device.api.get_routing_ipv6_routes(vrf=vrf_name)

        if routes and route in routes:
            match = True
            if route_attrs != None:
                for k, v in route_attrs.items():
                    if k not in routes[route] or v != routes[route][k]:
                        log.info(f"Route attr key {k}, value {v} does not match. Route: {routes[route]}")
                        match = False
                        break
            if next_hop_info != None:
                def check_next_hop_info_match():
                    for nh_type in ['outgoing_interface', 'next_hop_list']:
                        if nh_type in routes[route]['next_hop']:
                            for _, nh in routes[route]['next_hop'][nh_type].items():
                                nh_match = True
                                for k, v in next_hop_info.items():
                                    if k not in nh or v != nh[k]:
                                        log.info(f"No match found in next hop for key {k}, value {v}. Next hop: {nh}")
                                        nh_match = False
                                        break
                                if nh_match:
                                    return True
                    return False
                match = match and check_next_hop_info_match()
            if match:
                return True
        timeout.sleep()
    log.info(f"Could not verify route {route}")
    return False


def verify_routing_ip_bgp_neighbors_routes_exists(
    device,
    address_family,
    neighbor,
    vrf,
    initial_route,
    rd=None,
    max_time=60,
    check_interval=10,
    expected_result=True,
    output=None,
):
    """ Verify if the initial_route provided exists

        Args:
            device ('obj'): Device object
            address_family ('str'): address family
            rd ('str'): rd export value
            neighbor ('str'): neighbor address to find routes
            vrf ('str'): vrf name
            initial_route ('str'): intial route to search
            max_time ('int') : max time for Timeout
            check_interval ('int'): interval for Timeout
            expected_result ('bool'): expected result to check
        Returns:
            True / False
        Raises:
            None
    """
    timeout = Timeout(max_time=max_time, interval=check_interval)
    while timeout.iterate():
        route_exists = False
        if not output:
            out = get_bgp_route_from_neighbors(
                device=device,
                address_family=address_family,
                rd=rd,
                neighbor_address=neighbor,
                vrf=vrf,
            )
        else:
            out = output
            output = None
        if not out:
            return None

        routes = out.keys()
        for route in routes:
            if initial_route in route:
                route_exists = True

        if route_exists == expected_result:
            return route_exists

        timeout.sleep()
    return route_exists


def verify_routing_neighbors_advertised_routes_exists(
    device,
    address_family,
    neighbor,
    vrf,
    initial_route,
    rd=None,
    max_time=60,
    check_interval=10,
    output=None,
):
    """ Verify if neighbors advertised routes exists

        Args:
            device ('obj'): Device object
            address_family ('str'): address family
            rd ('str'): rd export value
            neighbor ('str'): neighbor address to find routes
            vrf ('str'): vrf name
            initial_route ('str'): intial route to search
            max_time ('int') : max time for Timeout
            check_interval ('int'): interval for Timeout
            output ('list'): list of neighbors advertised routes (get_bgp_neighbors_advertised_routes)
        Returns:
            True
            False
    """
    result = False
    timeout = Timeout(max_time=max_time, interval=check_interval)
    while timeout.iterate():
        if not output:
            advertised_routes = list(
                get_bgp_neighbors_advertised_routes(
                    device=device,
                    address_family=address_family,
                    neighbor_address=neighbor,
                    rd=rd,
                    vrf=vrf,
                )
            )
            if not advertised_routes:
                return False
        else:
            advertised_routes = output

        if advertised_routes:
            for route in advertised_routes:
                if route == initial_route:
                    result = True

            return result
        else:
            timeout.sleep()

    return result


def is_routing_route_targets_present(
    device, vrf, routes, address_family, ignore_routes=None
):
    """ Verify route target is present

        Args:
            device ('obj'): Device object
            vrf ('str'): VRF name
            address_family ('str'): address family to check
            routes ('list'): list of routes to compare
                ex.) routes = ['192.168.1.1', '192.168.1.2']
            ignore_routes ('list'): list of routes to ignore with type
                ex.) ignore_routes = ['L', 'B', 'C']
        Returns:
            True
            False
        Raises:
            None
    """
    if not routes:
        return False

    result = True
    routes_received = get_routing_routes(device, vrf, address_family)

    for route in routes_received.keys():
        try:
            source_protocol_codes = routes_received[route][
                "source_protocol_codes"
            ]
            if ignore_routes and source_protocol_codes in ignore_routes:
                continue
            if route not in routes:
                result = False
        except KeyError as e:
            log.error("Key issue with exception {}".format(str(e)))
            result = False

    return result


def is_routing_repair_path_in_route_database(
    device, route, max_time=60, check_interval=10
):
    """ Verify if 'repair path' is present in route database

        Args:
            device ('obj'): Device object
            route ('str'): Route address
            max_time ('int'): Max time in seconds checking output
            check_interval ('int'): Interval in seconds of each checking 
        Return:
            True/False
        Raises:
            None
    """

    log.info("Getting 'repair path' information")

    timeout = Timeout(max_time=max_time, interval=check_interval)
    while timeout.iterate():
        next_hop, outgoing_interface = get_routing_repair_path_information(
            device=device, route=route
        )
        if next_hop and outgoing_interface:
            return True

        timeout.sleep()

    log.info("Could not find any information about repair path")
    return False

def verify_route_known_via(device, route, known_via, ipv6=False, max_time=90, check_interval=10):
    """ Verify route known via

        Args:
            device ('obj'): Device object
            route ('str'): Route address
            known_via ('str'): Known via value
            max_time ('int'): Max time in seconds checking output
            check_interval ('int'): Interval in seconds of each checking 
        Return:
            True/False
        Raises:
            None
    """
    reqs = R(
        [
            'entry',
            '(.*)',
            'known_via',
            '(.*{}.*)'.format(known_via),
        ]
    )
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            if ipv6:
                out = device.parse('show ipv6 route {}'.format(route))
            else:
                out = device.parse('show ip route {}'.format(route))
        except Exception:
            timeout.sleep()
            continue
        if not out:
            log.info('Could not get information about show ip route {}'.format(route))
            timeout.sleep()
            continue        
        found = find([out], reqs, filter_=False, all_keys=True)
        if found:
            return True
        timeout.sleep()
    return False

def verify_cef_labels(device, route, expected_first_label, expected_last_label=None, max_time=90, 
    check_interval=10):
    """ Verify first and last label on route

        Args:
            device ('obj'): Device object
            route ('str'): Route address
            expected_first_label ('str'): Expected first label
            expected_last_label ('str'): Expected last label
            max_time ('int'): Max time in seconds checking output
            check_interval ('int'): Interval in seconds of each checking 
        Return:
            True/False
        Raises:
            None
    """
    reqs = R(
        [
            'vrf',
            '(.*)',
            'address_family',
            '(.*)',
            'prefix',
            '(.*{}.*)'.format(route),
            'nexthop',
            '(.*)',
            'outgoing_interface',
            '(.*)',
            '(?P<val>.*)'
        ]
    )
    timeout = Timeout(max_time, check_interval)
    
    while timeout.iterate():
        result = True
        out = None
        try:
            out = device.parse('show ip cef {}'.format(route))
        except SchemaEmptyParserError:
            out = None
        if not out:
            result = False
            log.info('Could not get information about show ip cef {}'.format(route))
            timeout.sleep()
            continue        
        found = find([out], reqs, filter_=False, all_keys=True)
        if found:
            keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={}, 
                                        source=found)
            for item in keys:
                first_label = item.get('val',{}).get('outgoing_label', None)
                if first_label and str(expected_first_label) not in str(first_label):
                    result = False
                if expected_last_label:
                    sid = item.get('val',{}).get('sid', None)
                    if str(expected_last_label) != str(sid):
                        result = False
            
            if result:
                return True
        timeout.sleep()
    return False


def verify_routing_subnet_entry(
    device, prefix, vrf=None, max_time=30, check_interval=10
):
    """ Verify route entry is present in
        'show ip route vrf {vrf} {prefix}'/'show ip route {prefix}'

        Args:
            device ('obj'): Device object
            prefix ('str'): prefix
            max_time ('int', optional): maximum time to wait in seconds, 
                default is 30
            check_interval ('int', optional): how often to check in seconds, 
                default is 10
            vrf ('str', optional): VRF name, default None
        Returns:
            Result('bool'): verified result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        actual_entries = device.api.get_routing_vrf_entries(
            device=device,
            prefix=prefix,
            vrf=vrf,
        )

        if actual_entries:
 
            if prefix in actual_entries:
                return True

        timeout.sleep()

    if not actual_entries:
        log.error("Unable to get subnet details for {}".format(prefix))
    else:
        log.error("Did not get entry in {} for prefix {}".format(
            actual_entries, prefix)
        )

    return False


def verify_route_vrf_nexthop_with_source_protocol(
    device, vrf, route_ip, address_family, protocol, out_intf, expected_nexthop, max_time=20, check_interval=2
):
    """ Verify route target is present
        Args:
            device ('obj'): Device object
            vrf ('str'): VRF name
            address_family ('str'): address family to check
            route_ip ('list'): list of routes to compare
                ex.) routes = ['192.168.1.1', '192.168.1.2']
            ignore_routes ('list'): list of routes to ignore with type
                ex.) ignore_routes = ['L', 'B', 'C']
        Returns:
            True
            False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():

        if address_family == "ipv6":
            routes_received = device.api.get_routing_ipv6_routes(vrf)
        else:
            routes_received = device.api.get_routing_routes(vrf,address_family)

        if routes_received:
            for route in routes_received.keys():
                actual_route=route.split("/")
            # Getting specific route ip
                if route_ip == actual_route[0]:
                # Matching with specific source protocol
                    if routes_received[route]['source_protocol'] == 'bgp':
                        n_hop_list = routes_received[route]['next_hop'].get("next_hop_list","")
                        for indx in n_hop_list.keys():
                        # Verifying for specific outgoing interface
                            if n_hop_list[indx]['outgoing_interface'] == out_intf:
                                if n_hop_list[indx]['next_hop'] == expected_nexthop:
                                    return True
        timeout.sleep()
         
    return False

def verify_source_protocol(device, route, expected_source):
    """
    Verifies that route's source protocol matches that of expected_source.

    Args:
        device (): Device used to run commands
        route ('str'): Route whose source protocol will be checked
        expected_source ('str'): Source protocol that route is expected to match
    
    Returns True expected source protocol matches device source protocol, False otherwise
    """
    log.info("Checking that route {} has source protocol {}".format(route, expected_source))
    device_source = device.api.get_routing_route_source_protocol(route)
    if expected_source != device_source:
        log.error("Route {} does not have source protocol {}. Has {} instead".format(route, expected_source, device_source))
        return False
    log.info("Route {} has source protocol {}.".format(route, expected_source))
    return True

def verify_source_protocols(device, routes, expected_source):
    """
    Verifies that multiple routes' source protocols match that of expected_source.

    Args:
        device (): Device used to run commands
        routes ('list'): List of routes whose source protocols will be checked
        expected_source ('str'): Source protocol that all routes are expected to match
    
    Returns True if all routes' souce protocols match the expected source protocol, False otherwise
    """
    success = True
    for route in routes:
        if not device.api.verify_source_protocol(route, expected_source):
            success = False
    return success

def verify_next_hop(device, route, expected_next_hop):
    """
    Verifies that route's next hop matches that of expected_next_hop.

    Args:
        device (): Device used to run commands
        route ('str'): Route whose next hop will be checked
        expected_next_hop ('str'): Next hop that route is expected to match

    Returns True if route's next hop matches expected_next_hop, False otherwise
    """
    log.info("Checking that route {} has next hop {}".format(route, expected_next_hop))
    #device_next_hop = cef_get.get_cef_next_hop_ip_address(device, route)
    device_next_hops = device.api.get_next_hops(route)
    # Nesting because things aren't working as expected, trying things
    if device_next_hops is not None:
        if expected_next_hop in device_next_hops:
            log.info("Route {} has next hop {}".format(route, expected_next_hop))
            return True
    log.error("Route {} does not have next hop {}\nHas next hops {}".format(route, expected_next_hop, device_next_hops))
    return False

def verify_next_hops(device, routes, expected_next_hop):
    """
    Verifies that the routes' next hops match that of expected_next_hop.

    Args:
        device (): Device used to run commands
        routes ('list'): Routes whose next hops will be checked
        expected_next_hop ('str'): Next hops that routes are expected to match
    """
    success = True
    for route in routes:
        if not verify_next_hop(device, route, expected_next_hop):
            success = False
    return success

def verify_num_routes_equal_before_and_after_clear(device, show_cmd, clr_cmd):
    """
    Verifies that the number of routes before
    and after running the clr_cmd are equal

    Args:
        device (): Device used to run commands
        show_cmd ('str'): show command to run
        clr_cmd ('str'): clear command to run

    Returns True if number of routes before and after clear are equal, None if exception,
    False otherwise
    """ 
    try:
        # 1. Run show command
        preclean_out = device.parse(show_cmd)
        preclean_routes = util.get_routes_from_parsed(output=preclean_out)
    except SchemaEmptyParserError as e:
        # if SchemaEmptyParserError, set preclean_routes to empty list
        log.error("A SchemaEmptyParserError exception has occurred\n{}".format(e))
        preclean_routes = []
    except Exception as e:
        log.error("An exception has occurred\n{}".format(e))
        return None

    # 2. Run clear command
    device.execute(clr_cmd)
    sleep(10)

    # 3. Run show 
    try:
        postclean_out = device.parse(show_cmd)
        postclean_routes = util.get_routes_from_parsed(output=preclean_out)
    except SchemaEmptyParserError as e:
        # if SchemaEmptyParserError, set postclean_routes to empty list
        log.error("A SchemaEmptyParserError exception has occurred\n{}".format(e))
        postclean_routes = []
    except Exception as e:
        log.error("An exception has occurred\n{}".format(e))
        return None

    #if preclean_routes is not None and postclean_routes is not None:
    num_preclean = len(preclean_routes)
    num_postclean = len(postclean_routes)
    log.info("# Preclean routes: {}\n# Postclean routes: {}".format(num_preclean, num_postclean))
    return num_preclean == num_postclean

def verify_ipv6_intf_ip_address(device, interface, address,max_time=30,interval=10):
    """
    Verifies that the address is valid and exists in the interface given

    Args:
        device (): Device used to run commands
        interface ('str'): interface on device
        address ('str'): address to verify
        max_time ('int'): time in seconds for trying verification. Default=30
        interval ('int'): time in seconds how often to retry verification. Default=10

    Returns True if address exists in interface, false otherwise
    """

    log.info("Verifying that interface {} on device {} has address {}".format(interface, device.name, address))

    timeout_obj = Timeout(max_time=max_time, interval=interval)            
    ipv6_addresses=''
    while timeout_obj.iterate():
        try:
            ipv6_addresses = device.api.get_ipv6_intf_valid_ip_addresses(interface)
            if ipv6_addresses:
                if address in ipv6_addresses:
                    log.info("A valid Address: {} is found on interface {}".format(address, interface))
                    return True
                else:
                    timeout_obj.sleep()                              
            else:
                timeout_obj.sleep()                
        except Exception as e:
            log.error("Error: an exception occured\n{}".format(e))
            timeout_obj.sleep()
    log.error("Address: {} was not found on interface {}".format(address, interface))
    return False

def verify_ipv6_intf_ip_address_notexist(device, interface, address,max_time=30,interval=10):
    """
    Verifies that the valid address does not exist in the interface given

    Args:
        device (): Device used to run commands
        interface ('str'): interface on device
        address ('str'): address to verify
        max_time ('int'): time in seconds for trying verification. Default=30
        interval ('int'): time in seconds how often to try verification. Default=10

    Returns True if address does not exist in interface, false otherwise
    """
    timeout_obj = Timeout(max_time=max_time, interval=interval)            
    ipv6_addresses=''   
    while timeout_obj.iterate():     
        try:
            exist=False
            ipv6_addresses = device.api.get_ipv6_intf_valid_ip_addresses(interface)
            if ipv6_addresses:
                if address in ipv6_addresses:
                    exist=True
            if exist==True:
                timeout_obj.sleep()                
            else:
                return True                                
        except Exception as e:
            return True
    return False

def verify_linklocal_from_mac_address(device, linklocal_intf, mac_intf):
    """
    Verifies that the linklocal address in linklocal_intf is based
    on the mac address of mac_intf.

    Args:
        device ('Device'): Device used to run commands
        linklocal_intf ('str'): Interface whose linklocal address is being verified
        mac_intf ('str'): Interface where linklocal_intf derives the MAC address to generate
            linklocal address
    
    Returns True if linklocal address is based on the MAC address, False otherwise
    """
    log.info("Verifying that linklocal address of interface {} is based on the\n\
    MAC address of interface {}".format(linklocal_intf, mac_intf))
    # Get expected linklocal address: produced from function
    #   - Get MAC address
    #   - Compute linklocal address from MAC address
    try:
        expected_ll_addr = device.api.ipv6_build_linklocal(mac_intf)
    except Exception as e:
        log.error("Error: an exception occured\n{}".format(e))
    # Get actual linklocal address: get from device
    actual_ll_addr = device.api.get_ipv6_interface_ip_address(linklocal_intf, True)

    # Compare expected and actual linklocal addresses
    log.info("Expected linklocal address: {}\nActual linklocal address: {}".format(expected_ll_addr, actual_ll_addr))
    if expected_ll_addr == actual_ll_addr:
        return True
    return False

def verify_tunnel_linklocal_based_on_ipv4_addr(device, tunnel_intf, ipv4_intf, isatap=False):
    """
    Verifies that tunnel_intf's ipv6 linklocal address is based on
    the ipv4 address of an ipv4_intf

    Args:
        device ('Device'): Device used to run commands
        tunnel_intf ('str'): Tunnel interface whose linklocal address is being checked
        ipv4_intf ('str'): IPv4 interface
        isatap ('bool'): Checks for ISATAP address or not

    Returns True if tunnel_intf's ipv6 linklocal address is based on ipv4_intf's address, False otherwise
    """
    try:
        # Device Tunnel linklocal address (Actual linklocal)
        actual_ll_addr = device.api.get_ipv6_interface_ip_address(tunnel_intf, True)
        # Device ipv4 interface ip address
        # ipv4_addr = device.api.get_interface_ip_address(ipv4_intf)
        # Generated ipv6 linklocal address from ipv4 (Expected linklocal)
        expected_ll_addr = device.api.get_ipv6_linklocal_addr_from_ipv4(ipv4_intf, isatap)
    except Exception as e:
        log.error("Error: an exception occured\n{}".format(e))
    log.info("Actual linklocal address: {}\nExpected linklocal address: {}"\
        .format(actual_ll_addr, expected_ll_addr))

    if actual_ll_addr == expected_ll_addr:
        log.info("The tunnel interface's linklocal address is based on the ipv4 interface's address.")
        return True
    log.error("The tunnel interface's linklocal address is NOT based on the ipv4 interface's address.")
    return False

def verify_ipv6_linklocal_address(device, interface, expected_linklocal):
    """
    Verifies that the expected_linklocal address is equal to the actual
    linklocal address.

    Args:
        device ('Device'): Device used to run commands
        interface ('str'): Interface to get linklocal address from
        expected_linklocal ('str'): Expected linklocal address

    Returns True if expected_linklocal matches actual linklocal address, False otherwise.
    """
    log.info("Verifying that expected linklocal address {} is True on interface {}\
    on device {}".format(expected_linklocal, interface, device.name))
    try:
        actual_linklocal = device.api.get_ipv6_interface_ip_address(interface, True)
    except Exception as e:
        log.error("Error: an exception occured\n{}".format(e))
    log.info("Expected linklocal address: {}\nActual linklocal address: {}".format(expected_linklocal, actual_linklocal))

    if expected_linklocal == actual_linklocal:
        log.info("Expected linklocal address is equal to the actual linklocal address.")
        return True
    log.error("Expected linklocal address is NOT equal to the actual linklocal address.")
    return False

def verify_ipv6_intf_autocfg_address(device, interface, prefix, subnet):
    """
    Verifies that the address matches an entry in the interface given

    Args:
        device (): Device used to run commands
        interface ('str'): interface on device
        prefix ('str'): address to verify
        subnet ('int):  subnetmask

    Returns True if address matches in interface, false otherwise
    """

    log.info("Verifying address {}/{} matches an auto configured address on device".format(prefix, subnet))
    try:
        auto_cfg = device.api.get_ipv6_intf_autocfg_address(interface)
    except Exception as e:
        log.error("Error: An exception occured\n{}".format(e))
    for addr in auto_cfg:
        pfx, nmask = addr.split('/')
        if prefix in pfx and subnet == int(nmask):
            return True

    log.error("Given address {}/{} does not match any of the autocfg addresses {}".format(prefix, subnet, auto_cfg))
    return False
