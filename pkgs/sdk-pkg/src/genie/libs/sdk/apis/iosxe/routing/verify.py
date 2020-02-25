"""Common verify functions for routing"""

# Python
import re
import logging
from prettytable import PrettyTable

# pyATS
from pyats.utils.objects import find, R

# Genie
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

def verify_route_known_via(device, route, known_via, max_time=90, check_interval=10):
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
            out = device.parse('show ip route {}'.format(route))
        except SchemaEmptyParserError:
            out = None
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