"""Common verify functions for routing"""

# Python
import re
import logging
from prettytable import PrettyTable
import operator

# pyATS
from pyats.utils.objects import find, R
from genie.utils import Dq

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# BGP
from genie.libs.sdk.apis.iosxe.bgp.get import (
    get_ip_bgp_summary,
    get_bgp_route_from_neighbors,
    get_bgp_neighbors_advertised_routes,
)

# ROUTING
from genie.libs.sdk.apis.iosxe.routing.get import get_routing_routes
from genie.libs.sdk.apis.iosxe.routing.get import (
    get_routing_repair_path_information, )

log = logging.getLogger(__name__)


def verify_ip_cef_nexthop_label(device,
                                ip,
                                table=None,
                                expected_label=None,
                                vrf=None,
                                max_time=30,
                                check_interval=10):
    """ Verify nexthop does (not) have expected label

        Args:
            device (`obj`): Device object
            ip (`str`): IP address
            expected_label (`str`): Expected label. None if no label expected
            vrf (`str`): Not used on JuniperOS
            table (`str`): Route table
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            if table:
                out = device.parse('show route table {table} {ip}'.format(
                    table=table, ip=ip))
            else:
                out = device.parse('show route {ip}'.format(ip=ip))
        except SchemaEmptyParserError:
            log.info('Failed to parse. Device output might contain nothing.')
            timeout.sleep()
            continue

        for table_name in out.get('table_name', {}):
            if table and table_name not in table:
                continue

            for route in out['table_name'][table_name].get('routes', {}):
                if ip in route:
                    hop_index_dict = out['table_name'][table_name]['routes'][
                        route]
                    for index in hop_index_dict.get('next_hop', {}).get(
                            'next_hop_list', {}):
                        if '>' in hop_index_dict['next_hop']['next_hop_list'][
                                index].get('best_route', ''):
                            found_label = hop_index_dict['next_hop'][
                                'next_hop_list'][index].get('mpls_label')
                            if expected_label and expected_label in found_label:
                                log.info(
                                    'Found the expected label "{}"'.format(
                                        found_label))
                                return True
                            elif not expected_label and not found_label:
                                log.info(
                                    'No label found. No label is expected')
                                return True

        timeout.sleep()
    return False


def verify_routing_static_routes(device,
                                 destination_address,
                                 to=None,
                                 not_to=None,
                                 known_via=None,
                                 tag=None,
                                 preference=None,
                                 protocol_name=None,
                                 extensive=False,
                                 max_time=60,
                                 check_interval=10):
    """ Verify static route exists

        Args:
            device ('str'): Device str
            destination_address ('str'): destination ip address
            to ('str'): to value
            not_to ('str'): not to value
            known_via ('str'): known via value
            tag ('str'): Tag value
            preference ('str'): Preference value
            protocol_name ('str'): Protocol name
            extensive ('bool'): if command with extensive at the end
            max_time (`int`): Max time, default: 60
            check_interval (`int`): Check interval, default: 10
        Returns:
            True / False
        Raises:
            None

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            if extensive:
                out = device.parse('show route protocol static extensive')
            else:
                out = device.parse('show route protocol static')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dictionary structure:
        #         {
        #             "rt": [
        #                 {
        #                     "rt-destination": "10.169.14.240/32",
        #                     "rt-entry": {
        #                         "nh": [
        #                             {
        #                                 "to": "10.169.14.121",
        #                                 "via": "ge-0/0/1.0"
        #                             }
        #                         ],
        #                         "rt-tag": "100",
        #                         "preference": "5",
        #                         "protocol-name": "Static"
        #                     }
        #                 }
        #             ],
        #             "table-name": "inet.0",
        #             "total-route-count": "240"
        #         },
        rt_list = Dq(out).get_values("rt")
        rt_destination_ = None
        for rt_dict in rt_list:
            current_rt_destination = Dq(rt_dict).get_values(
                "rt-destination", 0)
            if current_rt_destination:
                rt_destination_ = current_rt_destination
            if not rt_destination_:
                continue
            if not rt_destination_.startswith(destination_address):
                continue

            if not_to:
                not_to_ = Dq(rt_dict).get_values("to", 0)
                if not_to_.startswith(not_to):
                    continue
            if to:
                to_ = Dq(rt_dict).get_values("to", 0)
                if not to_.startswith(to):
                    continue
            if known_via:
                via_ = Dq(rt_dict).get_values("via", 0)
                if not via_.startswith(known_via):
                    continue
            if tag:
                tag_ = Dq(rt_dict).get_values("rt-tag", 0)
                if str(tag_) != str(tag):
                    continue
            if preference:
                preference_ = Dq(rt_dict).get_values("preference", 0)
                if str(preference_) != str(preference):
                    continue
            if protocol_name:
                protocol_ = Dq(rt_dict).get_values("protocol-name", 0)
                if protocol_.upper() != protocol_name.upper():
                    continue
            return True
        timeout.sleep()
    return False


def verify_routing_interface_preference(device,
                                        protocol,
                                        interface,
                                        preference,
                                        extensive=None,
                                        max_time=60,
                                        check_interval=10):
    """ Verify routing interface preference

        Args:
            device ('str'): Device str
            protocol ('str'): Protocol name
            interface ('str'): Interface name
            preference ('int'): Preference value
            extensive ('bool'): Check with extensive command
            max_time (`int`): Max time, default: 60
            check_interval (`int`): Check interval, default: 10
        Returns:
            True / False
        Raises:
            None

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            if extensive:
                out = device.parse(
                    'show route protocol {protocol} extensive'.format(
                        protocol=protocol))
            else:
                out = device.parse(
                    'show route protocol {protocol}'.format(protocol=protocol))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dictionary structure:
        #         {
        #             "rt": [
        #                 {
        #                     "rt-destination": "10.169.14.240/32",
        #                     "rt-entry": {
        #                         "nh": [
        #                             {
        #                                 "to": "10.169.14.121",
        #                                 "via": "ge-0/0/1.0"
        #                             }
        #                         ],
        #                         "rt-tag": "100",
        #                         "preference": "5",
        #                         "protocol-name": "Static"
        #                     }
        #                 }
        #             ],
        #             "table-name": "inet.0",
        #             "total-route-count": "240"
        #         },
        rt_list = Dq(out).get_values("rt")
        for rt_dict in rt_list:
            via_ = Dq(rt_dict).get_values("via", 0)
            if not via_ or not via_.startswith(interface):
                continue
            preference_ = Dq(rt_dict).get_values("preference", 0)
            if not preference_ or preference_ != str(preference):
                continue
            return True
        timeout.sleep()
    return False


def verify_routing_ip_exist(device,
                            destination_address,
                            protocol=None,
                            metric=None,
                            max_time=60,
                            check_interval=10,
                            extensive=None,
                            exact=None,
                            known_via=None,
                            ):
    """ Verify routing ip exists

        Args:
            device ('str'): Device str
            destination_address ('str'): Destination address
            protocol ('str'): Protocol name
            max_time (`int`): Max time, default: 60
            metric (`int`): Metric of routing protocol
            check_interval (`int`): Check interval, default: 10
            extensive ('bool'): Is extensive
            exact ('bool'): Is exact
        Returns:
            True / False
        Raises:
            None

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            if extensive:
                if exact:
                    out = device.parse(
                        'show route extensive {destination_address} exact'.
                        format(destination_address=destination_address))
                else:
                    out = device.parse(
                        'show route extensive {destination_address}'.format(
                            destination_address=destination_address))
            elif protocol:
                out = device.parse(
                    'show route protocol {protocol}'.format(protocol=protocol))
            else:
                out = device.parse('show route')

        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        rt_list = Dq(out).get_values("rt")

        for rt_dict in rt_list:
            rt_destination_ = Dq(rt_dict).get_values("rt-destination", 0)
            
            if not rt_destination_.startswith(str(destination_address)):
                continue
            
            if metric:
                destination_metric = Dq(rt_dict).get_values("metric", [0])
                if destination_metric != str(metric):
                    continue

            if known_via:
                via_ = Dq(rt_dict).get_values("via", 0)
                if not via_.startswith(known_via):
                    continue
            
            return True
        timeout.sleep()

    return False


def verify_default_route_protocol(device,
                                  route,
                                  ip_type='ipv4',
                                  inet_type='inet.0',
                                  expect_output=True,
                                  max_time=60,
                                  check_interval=10,
                                  subnet_mask_number=True,
                                  protocol=None):
    """ Verifies if route is displayed in output of show route command

        Args:
            device ('obj'): device to use
            route ('str'): ipv4/ipv6 default route
            ip_type ('str'): Either ipv4/ipv6
            inet_type ('str'): type of ip
            expect_output ('bool'): Flag, either expecting output or no output
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check
            subnet_mask_number ('bool'): Flag, to include/exclude subnet masknumber in comparison
            protocol ('str'): Type of protocol (ex.ospf,ospf3,ect)

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            if protocol:
                output = device.parse(
                    'show route protocol {}'.format(protocol))
            else:
                output = device.parse('show route extensive')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        route_tables = output.q.get_values('route-table')
        
        for routes in route_tables:

            #'table-name': 'inet.0'
            table_name = routes.get('table-name', [])

            if Dq(routes).contains('table-name').contains(inet_type):
                route_values = Dq(routes).contains('rt').get_values(
                    'rt-destination')
                for element in route_values:
                    route_value = element if subnet_mask_number else element.split(
                        '/')[0]
                    if route_value == route:
                        if expect_output:
                            return True
                        else:
                            timeout.sleep()
                            continue

        timeout.sleep()

    return False


def verify_routing_route(device,
                         route,
                         expected_protocol_name=None,
                         expected_community=None,
                         extensive=True,
                         max_time=60,
                         check_interval=10,
                         expected_table_name=None,
                         expected_tag=None):
    """Verify show route exists against critera

    Args:
        route ('str'): Route to check
        expected_protocol_name ('str'): Expected protol in route
        expected_community ('str'): Expected community
        extensive ('bool): Whether to use extensive or not
        expected_table_name ('str'): Table name to check for
        expected_tag ('str'): Route table tag to check for

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None

        try:
            if extensive:
                out = device.parse(
                    "show route {route} extensive".format(route=route))
            else:
                out = device.parse("show route {route}".format(route=route))

        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        for table_entry in out.q.get_values('route-table'):

            if expected_table_name:
                    table_name_ = table_entry.get('table-name')
                    if table_name_ != expected_table_name:
                        timeout.sleep()
                        continue                

            for rt in table_entry.get('rt', []):

                # Check values. If value is wrong then skip

                if expected_protocol_name and rt.get("rt-entry", {}).get(
                        "protocol-name", None) != expected_protocol_name:
                    continue

                if expected_community:
                    regexp = re.compile('Communities: +{community}'.format(
                        community=expected_community))
                    if not regexp.search(rt.get('tsi', {}).get("#text", None)):
                        continue

                if expected_tag:
                    tags_ = Dq(rt).get_values('rt-tag')
                    if str(expected_tag) not in tags_:
                        continue

                return True
            
            timeout.sleep()

    return False

def verify_routing_routes(device,
                          addr_list,
                          protocol,
                          contains,
                          max_time=60,
                          check_interval=10):
    """Verifies address list agianst 'show route protocol {protocol}'

    Args:
        addr_list('list'): List to verify
        protocol ('str'): Protocol type to check in show route
        contains ('boolean'): flag to check if addr_list is contained/excluded
        max_time ('int'): Maximum time to keep checking
        check_interval ('int'): How often to check

    Returns:
        True/False

    Raises:
        N/A
    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse(
                "show route protocol {protocol}".format(protocol=protocol))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        active_list = []

        for table_entry in output.q.get_values('route-table'):
            for route in table_entry.get('rt', []):
                active_list.append(route.get('rt-destination', None))

        timeout.sleep()

        if contains == True:
            if set(active_list).issuperset(set(addr_list)):
                return True
            else:
                continue
        else:
            if len(set(active_list).intersection(set(addr_list))) > 0:
                return False
            else:
                continue

    if contains:
        return False
    else:
        return True

                            
def _search_table_for_metric(op, **kwargs):
    route_tables = Dq(kwargs['output']).get_values('route-table')

    for route_table in route_tables:
        for rt in Dq(route_table).get_values('rt'):

            destination_address_ = Dq(rt).get_values('rt-destination', 0)
            if kwargs['address_exceptions'] and destination_address_ in kwargs['address_exceptions']:
                continue

            metric_ = Dq(rt).get_values('metric', 0)

            if op(int(metric_), int(kwargs['metric'])):
                return False
    return True


def verify_routing_no_ospf_metric_match(device, 
                                        metric, 
                                        address_exceptions=None,
                                        max_time=60, 
                                        check_interval=10):
    """Verify that no OSPF routes have given metric

    Args:
        device (obj): Device object
        metric (int): Metric to check for
        address_exceptions (list, optional): List of addresses to not check. Defaults to None.
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
    """
    

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse(
                "show route protocol ospf")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
    
        if _search_table_for_metric(operator.eq, **locals()):
            return True
        else:
            timeout.sleep()
            continue
    return False


def verify_routing_ospf_metric_match_or_greater(device, 
                                        metric, 
                                        address_exceptions=None,
                                        max_time=60, 
                                        check_interval=10):
    """Verify that all OSPF routes have given metric

    Args:
        device (obj): Device object
        metric (int): Metric to check for
        address_exceptions (list, optional): List of addresses to not check. Defaults to None.
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse(
                "show route protocol ospf")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
    
        if _search_table_for_metric(operator.lt, **locals()):
            return True
        else:
            timeout.sleep()
            continue
    return False


def verify_metric_in_route(device, address, expected_metric, table_name, 
                          max_time=60,
                          check_interval=10):
    """Verify metric in 'show route {address}' when given table_name

        Args:
            device ('obj'): Device to use
            address ('str'): IP address in show command
            expected_metric ('int'): Expected metric number
            table_name ('str'): Table name. E.g. "inet.3".
            max_time ('int', optional): Maximum time to keep checking. Default to 60.
            check_interval ('int', optional): How often to check. Default to 10.

        Returns:
            True/False

        Raises:
            N/A
    """  

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:

            out = device.parse("show route {address}".format(address=address))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        # Sample output  
        #  {'route-information': {'route-table': [{'active-route-count': '8',
        #                                         'destination-count': '8',
        #                                         'hidden-route-count': '0',
        #                                         'holddown-route-count': '0',
        #                                         'rt': [{'rt-destination': '106.187.14.240/32',
        #                                                 'rt-entry': {'active-tag': '*',
        #                                                             'age': {'#text': '00:07:19'},
        #                                                             'metric': '1',  <-------------------------- 
        #                                                             'nh': [{'to': '106.187.14.157',
        #                                                                     'via': 'ge-0/0/0.0'}],
        #                                                             'preference': '10',
        #                                                             'protocol-name': 'OSPF'}}],
        #                                         'table-name': 'inet.0', <--------------------------
        #                                         'total-route-count': '8'},
        #                                     {'active-route-count': '1',
        #                                         'destination-count': '1',
        #                                         'hidden-route-count': '0',
        #                                         'holddown-route-count': '0',
        #                                         'rt': [{'rt-destination': '106.187.14.240/32',
        #                                                 'rt-entry': {'active-tag': '*',
        #                                                             'age': {'#text': '00:07:19'},
        #                                                             'metric': '1',  <--------------------------
        #                                                             'nh': [{'to': '106.187.14.157',
        #                                                                     'via': 'ge-0/0/0.0'}],
        #                                                             'preference': '9',
        #                                                             'protocol-name': 'LDP'}}],
        #                                         'table-name': 'inet.3', <--------------------------
        #                                         'total-route-count': '1'}]}}

        # Filter the outputs:
        # Input:        out.q.contains('metric|inet.3', regex=True).reconstruct()
        # Output:       {'route-information': {'route-table': [{'rt': [{'rt-entry': {'metric': '1'}}]},
        #                                                      {'rt': [{'rt-entry': {'metric': '1'}}],
        #                                                                    'table-name': 'inet.3'}
        #                                                     ]}}
        filtered_output = out.q.contains('metric|{table_name}'.format(table_name=table_name), regex=True).reconstruct()

        rt_list = filtered_output['route-information']['route-table']

        for rt in rt_list:
            if 'table-name' in rt and rt['table-name'] == table_name:
                if expected_metric == int(Dq(rt).get_values('metric', 0)):
                    return True

        timeout.sleep()
    return False 


def verify_specific_route(device,
                          address,
                          learn_protocol,
                          max_time=60,
                          check_interval=10):
    """Verifies address list agianst 'show route protocol {protocol}'

    Args:
        device ('obj'): device to use
        address('str'): address to search for
        learn_protocol('str'): Learned protocol
        max_time ('int'): Maximum time to keep checking
        check_interval ('int'): How often to check

    Returns:
        True/False

    Raises:
        N/A
    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse(
                "show route {address}".format(address=address))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        #   [{'rt-entry': {'active-tag': '*', 'protocol-name': 'OSPF', 
        #   'preference': '10', 'metric': '1', 'age': {'#text': '00:00:01'}, 
        #   'nh': [{'to': '106.187.14.158', 'via': 'ge-0/0/0.0'}]}, 
        #   'rt-destination': '59.128.2.250/32'}]
        rt_destination_ = Dq(output).get_values("rt-destination", 0)

        #   [{'rt-entry': {'active-tag': '*', 'protocol-name': 'OSPF', 
        #   'preference': '10', 'metric': '1', 'age': {'#text': '00:00:01'}
        protocol_name = Dq(output).get_values("protocol-name", 0)

        if protocol_name:
            if rt_destination_.startswith(str(address)) and \
                protocol_name.lower() ==  learn_protocol.lower():
                return True
            else:
                timeout.sleep()
                continue
                
        timeout.sleep()

    return False
