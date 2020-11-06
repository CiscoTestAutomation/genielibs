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
from genie.libs.sdk.apis.iosxe.routing.get import (
    get_routing_routes,
    get_routing_repair_path_information)

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
                                        preference,
                                        ip_address=None,
                                        interface=None,
                                        extensive=None,
                                        max_time=60,
                                        check_interval=10):
    """ Verify routing interface preference

        Args:
            device ('str'): Device str
            protocol ('str'): Protocol name
            ip_address ('str'): IP address , default: None
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
                if ip_address:
                    out = device.parse(
                        'show route protocol {protocol} {ip_address}'.format(protocol=protocol,
                            ip_address=ip_address))
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
            if ip_address:
                rt_destination_ = Dq(rt_dict).get_values("rt-destination", 0)
                if not rt_destination_ or not rt_destination_.startswith(ip_address):
                    continue
            if interface:
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
                            extensive_protocol=None,
                            metric=None,
                            max_time=60,
                            check_interval=10,
                            extensive=None,
                            exact=None,
                            known_via=None,
                            protocol_type=None,
                            command_address=None
                            ):
    """ Verify routing ip exists

        Args:
            device ('str'): Device str
            destination_address ('str'): Destination address to check existence
            protocol ('str'): Protocol name
            extensive_protocol ('bool'): If show command includes extensive
            max_time (`int`): Max time, default: 60
            metric (`int`): Metric of routing protocol
            check_interval (`int`): Check interval, default: 10
            extensive ('bool'): Is extensive
            exact ('bool'): Is exact
            protocol_type ('str'): Protocol type 
            command_address ('str'): Address to run command with
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
            elif extensive_protocol:
                out = device.parse(
                    'show route protocol {protocol} extensive'.format(protocol=protocol))

            elif protocol:
                if protocol_type and command_address:
                    out = device.parse(
                        'show route {protocol_type}-protocol {protocol} {command_address}'.
                        format(protocol_type=protocol_type,
                               protocol=protocol,
                               command_address=command_address))
                else:
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

def verify_route_advertised_protocol_community(device,
                                               route,
                                               community_list,
                                               ip_address,
                                               protocol,
                                               protocol_type,
                                               invert=False,
                                               max_time=60,
                                               check_interval=10                      
                                              ):
    """Verify community has the given community_list against criteria

        Args:
            device ('obj'): Device object
            route ('str'): Target route to check
            community_list ('list(str)'): List of communities to verify
            ip_address ('str'): IP address to check
            protocol ('str'): Protocol name that passed in command
            protocol_type ('str'): Protocol type in show command, e.g., advertising-protocol or receive-protocol
            invert(bool, optional): Inverts from equals to not equals. Defaults to False.
            max_time ('int', optional): Maximum time to keep checking, default 60 seconds
            check_interval ('int', optional): How often to check, default 10 seconds

        Returns:
            True/False

        Raises:
            N/A 
    """
    op = operator.eq
    if invert:
        op = operator.ne
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse(
                "show route {protocol_type}-protocol {protocol} {ip_address} {route} detail".format(
                    protocol=protocol,
                    protocol_type=protocol_type,
                    ip_address=ip_address,
                    route=route
                ))
        
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        for rt_table_entry in output.q.get_values('route-table'):
            
            rt_entry = rt_table_entry.get('rt-entry')
            
            if rt_entry:
                
                # Check communities
                if op(rt_entry.get('communities').split(), community_list):
                    return True
            
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
                         expected_active_tag='*',
                         expected_tag=None,
                         expected_protocol_nexthop=None,
                         expected_load_balance_label=None,
                         invert=False,
                         single_community=False):
    """Verify show route exists against critera

    Args:
        route ('str'): Route to check
        expected_protocol_name ('str'): Expected protol in route
        expected_community ('str'): Expected community in route
        extensive ('bool): Whether to use extensive or not
        expected_table_name ('str'): Table name to check for
        expected_active_tag ('str'): Route table active tag to check, default: '*'
        expected_tag ('str'): Route table tag to check for
        invert (bool, optional): Inverts from equals to not equals. Defaults to False.

    Raise: None

    Returns: Boolean

    """
    op = operator.eq
    if invert:
        op = operator.ne
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
                
                if expected_active_tag:
                    a_tags_ = Dq(rt).get_values('active-tag')
                    if str(expected_active_tag) not in a_tags_:
                        continue
                
                if expected_community:
                    # Put all communities into a string for regex to match
                    if not single_community:
                        community_str = " ".join(expected_community)
                    else:
                        community_str=expected_community
                    
                    regexp = re.compile('Communities: +{community}'.format(
                        community=community_str))
                    if op(not regexp.search(rt.get('tsi', {}).get("#text", None)), True):
                        continue
    
                if expected_tag:
                    tags_ = Dq(rt).get_values('rt-tag')
                    if str(expected_tag) not in tags_:
                        continue
                
                if expected_protocol_nexthop:
                    result = False
                    for protocol_nh_dict in Dq(rt).get_values('protocol-nh'):
                        protocol_nexthop_ = protocol_nh_dict.get('to', None)
                        if protocol_nexthop_ == expected_protocol_nexthop:
                            result = True
                            break
                    if not result:
                        continue
                
                if expected_load_balance_label:
                    load_balance_label_ = Dq(rt).get_values('load-balance-label', 0)
                    if expected_load_balance_label not in load_balance_label_:
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


def is_push_present_in_route(device, address, table_name,
                           max_time=60,
                           check_interval=10):
    """Check if Push is presnt in 'show route {address}' when given table_name

        Args:
            device ('obj'): Device to use
            address ('str'): IP address in show command
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

        # Example output
        # {
        #     "route-information": {
        #         "route-table": [{
        #                 "rt": [{
        #                         "rt-entry": {
        #                             "nh": [{
        #                                     "mpls-label": "Push 118420",
        #                                 }]}}],
        #                 "table-name": "inet.3",
        #             }]}}

        rt_list = out.q.contains('nh|{table_name}'.format(
            table_name=table_name), regex=True).get_values('route-table')

        for rt in rt_list:
            if rt.get('table-name') == table_name and Dq(rt).get_values(
                    'mpls-label', None):
                    return True

        timeout.sleep()
    return False


def verify_route_is_advertised_or_received(
        device,
        protocol_type,
        address,
        expected_route,
        target_address=None,
        protocol='bgp',
        max_time=60,
        check_interval=10,
        extensive=False,
        invert=False,
):
    """ Verify the route is advertised

        Args:
            device ('obj'): Device object
            protocol_type ('str'): Protocol type in show command, e.g., advertising-protocol or receive-protocol
            expected_route ('str'): Expected route
            address ('str'): IP address
            target_address ('str'): Address used in show command
            protocol ('str', optional): Protocol name that passed in command. Defaults to 'bgp'
            extensive ('bool', optional): True means the show command contains 'extensive'. Defaults to False. 
            invert ('bool', optional): True means to verify not advertised or received. Defaults to False.
            max_time ('int', optional): Maximum time to keep checking. Default to 60
            check_interval ('int', optional): How often to check. Default to 10.     

        Returns:
            True/False
        Raises:
            None

    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            if extensive:
                out = device.parse(
                "show route {protocol_type}-protocol {protocol} {address} extensive".format(
                    protocol_type=protocol_type,
                    protocol=protocol,
                    address=address)) 
            else:
                if target_address:
                    out = device.parse(
                    "show route {protocol_type}-protocol {protocol} {address} {target_address}".format(
                        protocol_type=protocol_type,
                        protocol=protocol,
                        address=address,
                        target_address=target_address))

                else:
                    out = device.parse(
                        "show route {protocol_type}-protocol {protocol} {address}".format(
                            protocol_type=protocol_type,
                            protocol=protocol,
                            address=address)) 
                
        except SchemaEmptyParserError:
            if invert:
                return True
            timeout.sleep()
            continue                    
        
        # Example 1
        # expected_route = '0.0.0.0/0'
        # {
        #         'route-information': {
        #             'route-table': {
        #                 '0',
        #                 'rt': [{
        #                     'rt-destination': '0.0.0.0/0', <-----------
        #                     'rt-entry': { ...

        # Example 2
        # expected_route = '20.0.0.0'
        # ...
        #  {'rt-announced-count': '1',
        #   'rt-destination': '20.0.0.0', <-------------
        #   'rt-prefix-length': '24'}, <-------------
        # ...

        # Example 3
        # expected_route = '0.0.0.0'
        # 'rt-destination': '0.0.0.0/0',

        rt_list = out.q.get_values('rt')
        destinations = []

        for i in rt_list:
            # support Example 2
            if i.get('rt-prefix-length'):
                destinations.append(i.get('rt-destination')+'/'+i.get('rt-prefix-length'))
            else:
                destinations.append(i.get('rt-destination'))

        else:
            # support Example 1 and Example 3
            for item in destinations:
                if not(invert) and expected_route in item:
                    return True 
        
        timeout.sleep()
    if invert:
        return True 

    return False                       

def verify_route_forwarding_type(device, label, expected_type, max_time=60, check_interval=10):
    """ Verifies route-forwarding type given a label

    Args:
        device (obj): Device object
        label (str): Label to check
        expected_type (str): Expected type
        max_time (int, optional): Maximum sleep time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:
        str or None: mpls out label
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show route forwarding-table label {label}'.format(
                label=label
            ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dictionary
        # {
        #     "forwarding-table-information":{
        #         "route-table": [{
        #                 "rt-entry": [{
        #                         "nh":{
        #                             "nh-type": str,
        #                         }
        #                     }]
        #             }]
        #     }
        # }

        types_ = out.q.get_values('nh-type')
        for type_ in types_:
            if expected_type in type_:
                return True
        
        timeout.sleep()

    return False

def verify_source_of_best_path(device,
                         target_route,
                         expected_best_path,
                         max_time=60,
                         check_interval=10):
    """Verify the source of the best path

    Args:
        target_route ('str'): Route to check
        expected_best_path ('str'): Best path address
        max_time ('int', optional): Maximum time to keep checking. Default to 60.
        check_interval ('int', optional): How often to check. Default to 10.

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None

        try:
            out = device.parse(
                "show route {route} extensive".format(route=target_route))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Sample output
        # "route-information": {
        #     "route-table": [
        #         {"rt": [
        #                 {"rt-entry": [{
        #                     "active-tag": "*",
        #                     "gateway": "4.4.4.4",
        #                 }]

        for rt in out.q.get_values('rt'):
            if isinstance(rt.get("rt-entry"), list):
                for rt_entry_elem in rt.get("rt-entry", []):
                    if rt_entry_elem.get('active-tag') and rt_entry_elem.get(
                            'gateway') == expected_best_path:
                            return True

            elif rt.get("rt-entry", {}).get(
                    "gateway", None) == expected_best_path:
                return True

            timeout.sleep()

    return False

def verify_cluster_list_length_of_path(device,
                         target_route,
                         cluster_list_length,
                         best_route=True,
                         max_time=60,
                         check_interval=10):
    """Verify length of cluster list of path (best or non-best)

    Args:
        target_route ('str'): Route to check
        cluster_list_length ('int'): Length of cluster list
        best_route ('bool'): Whether to use best or non-best path
        max_time ('int', optional): Maximum time to keep checking. Default to 60.
        check_interval ('int', optional): How often to check. Default to 10.

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None

        try:
            out = device.parse(
                "show route {route} extensive".format(route=target_route))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Sample output
        # "route-information": {
        #     "route-table": [
        #         {"rt": [
        #                 {"rt-entry": [{
        #                     "active-tag": "*",
        #                     "cluster-list": "4.4.4.4",
        #                 },
        #                 {
        #                     "inactive-reason": "IGP metric",
        #                     "cluster-list": "2.2.2.2 4.4.4.4",
        #                 }]

        for rt in out.q.get_values('rt'):
            if isinstance(rt.get("rt-entry"), list):
                for rt_entry_elem in rt.get("rt-entry", []):
                    if best_route:
                        if rt_entry_elem.get('active-tag'):
                            if len(rt_entry_elem.get('cluster-list', '').split()) == \
                                    cluster_list_length:
                                return True
                    else:
                        if rt_entry_elem.get('inactive-reason'):
                            if len(rt_entry_elem.get('cluster-list', '').split()) == \
                                    cluster_list_length:
                                return True
            elif len(rt.get("rt-entry", {}).get("cluster-list", '').split()) == \
                    cluster_list_length:
                return True

            timeout.sleep()

    return False


def verify_route_table_label(device,
                             label=None,
                             php_label=None,
                             max_time=60,
                             check_interval=10):
    """ Verify the out label

        Args:
            device (`obj`): Device object
            label (`str`): show route label. Defaults to None.
            php_label (`str`): php label. Defaults to None.
            max_time ('int', optional): Maximum time to keep checking. Default to 60 seconds.
            check_interval ('int', optional): How often to check. Default to 10 seconds.
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show route table mpls.0 label {label}'.format(
                label=label))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        # "next_hop_list": {
        #                     1: {
        #                         "to": "10.19.198.66",
        #                         "via": "ge-0/0/3.0",
        #                         "best_route": ">",
        #                         "mpls_label": "Swap 78",
        #                     }
        mpls_value = Dq(out).contains(label).get_values('mpls_label',0)
        if mpls_value == php_label:
            return True

        timeout.sleep()


    return False


def verify_learned_protocol(device,
                            address,
                            next_hop=None,
                            learn_protocol=None,
                            cluster_value=None,
                            max_time=60,
                            check_interval=10):
    """Verifies learned protocol and next hop agianst 'show route {address} extensive'

    Args:
        device ('obj'): device to use
        address ('str'): IP address for show command
        next_hop ('str'): next hop ip address
        learn_protocol('str'): Learned protocol
        cluster_value('str'): Cluster value in show route
        max_time ('int', optional): Maximum time to keep checking. Default to 60 seconds.
        check_interval ('int', optional): How often to check. Default to 10 seconds.

    Returns:
        True/False

    Raises:
        N/A
    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse(
                "show route {address} extensive".format(address=address))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        #   [{'rt-entry': {'active-tag': '*', 'protocol-name': 'OSPF', 
        #   'preference': '10', 'metric': '1', 'age': {'#text': '00:00:01'}, 
        #   'nh': [{'to': '106.187.14.158', 'via': 'ge-0/0/0.0'}]}, 
        #   'rt-destination': '59.128.2.250/32'}]
        if next_hop:
            protocol_next_hop = Dq(output).contains("protocol-nh").get_values("to")
            if next_hop in protocol_next_hop:
                return True
            else:
                timeout.sleep()
                continue

        #   [{'rt-entry': {'active-tag': '*', 'protocol-name': 'OSPF', 
        #   'preference': '10', 'metric': '1', 'age': {'#text': '00:00:01'}
        if learn_protocol:
            protocol_name = Dq(output).get_values("protocol-name", 0)
            if protocol_name.lower() ==  learn_protocol.lower():
                return True
            else:
                timeout.sleep()
                continue

        #[{"rt-entry-state": "Active Int Ext",
        #"validation-state": "unverified",
        #"task-name": "BGP_2.2.2.2.2",
        #"announce-bits": "2",
        #"announce-tasks": "0-KRT 5-Resolve tree 1",
        #"cluster-list": "2.2.2.2 4.4.4.4"}]
        if cluster_value:
            cluster_item = Dq(output).get_values("cluster-list", 0)
            if cluster_value in str(cluster_item):
                return True
            else:
                timeout.sleep()
                continue
                
        timeout.sleep()

    return False


def verify_push_present_in_show_route(device, 
                                      address, 
                                      push_value,
                                      max_time=60,
                                      check_interval=10):
    """Verify if Push value is present in 'show route {address} extensive'

        Args:
            device ('obj'): Device to use
            address ('str'): IP address for show command
            push_value ('str'): Push value in show route {address} extensive command
            max_time ('int', optional): Maximum time to keep checking. Default to 60 seconds.
            check_interval ('int', optional): How often to check. Default to 10 seconds.

        Returns:
            True/False

        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse("show route {address} extensive".format(address=address))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example output
        # {
        #     "route-information": {
        #         "route-table": [{
        #                 "rt": [{
        #                         "rt-entry": {
        #                             "nh": [{
        #                                     "mpls-label": "Push 118420",
        #                                 }]}}],
        #                 "table-name": "inet.3",
        #             }]}}

        rt_list = Dq(out).get_values("route-table")

        for rt in rt_list:
            if str(push_value) == str(Dq(rt).get_values('mpls-label', 0).split()[1]):
                return True
            
        timeout.sleep()
    return False


def verify_route_best_path(device,
                         target_route,
                         ip_address=None,
                         preference=None,
                         active_tag='*',
                         interface=None,
                         extensive=False,
                         expected_to=None,
                         expected_med=None,
                         max_time=60, 
                         check_interval=10
                        ):
    """ Verify Best path is toward $ip_address or with preference $preference

        Args:
            device (`obj`): Device object
            target_route (`str`): Target route to check
            ip_address (`str`): IP Address to verify is best path, default: None
            preference (`int`): Preference of best path, default: None
            active_tag (`str`, optional): Active tag to check, default: '*' (best path)
            interface (`str`, optional): IP address in show command. Defaults to None. 
            extensive (`bool`, optional): 'extensive' added in the show command. Defaults to None.
            expected_to (`str`, optional): Expected address that be towarded to. Defaults to None.
            expected_med (`str`, optional): Expected med that be towarded to. Defaults to None.
            max_time (`int`, optional): Max time, default: 60 seconds
            check_interval (`int`, optional): Check interval, default: 10 seconds
        
        Returns:
            result (`bool`): Verified result
        
        Raises:
            N/A 
    """    
    timeout = Timeout(max_time, check_interval)
    
    preference = str(preference)
    
    while timeout.iterate():
        try:
            if interface and extensive:
                output = device.parse('show route protocol bgp {interface} extensive'.format(interface=interface))
            else:
                output = device.parse('show route protocol bgp')
            
        except SchemaEmptyParserError:
            log.info('Failed to parse. Device output might contain nothing.')
            timeout.sleep()
            continue
        
        # schema = {
        #     "route-information": {
        #         "route-table": [
        #             {
        #                   ...
        #                 "rt": [
        #                     {
        #                         "rt-destination": str,
        #                         "rt-entry": {
        #                             "active-tag": str,
        #                             "age": {
        #                                 "#text": str,
        #                             },
        #                                   ...
        #                             "preference": str,
        #                              ...
        #                         }
        #                     }
        #                 ],
        #                 ...
        #             }
        #         ]
        #     }
        # }
        route_tables = output.q.get_values('route-table')
        
        for routes in route_tables:
            rt_list = routes.get('rt')
            
            if rt_list:
                for rt in rt_list:
                    rt_entry = rt.get('rt-entry')

                    # show route protocol bgp {interface} extensive

                    #  'rt-entry': {'active-tag': '*',
                    #     'announce-bits': '2',
                    #     'announce-tasks': '0-KRT 5-Resolve tree 1',
                    #     'gateway': '2.2.2.2',
                    #     'nh': [{'nh-string': 'Next hop',
                    #             'session': '45a',
                    #             'to': '20.0.0.2',
                    #             'via': 'ge-0/0/0.0'}],
                    if interface and extensive:
                        if type(rt_entry) == dict:
                            nh_list = rt_entry.get('nh')
                            for nh in nh_list:
                                if nh.get('via') == target_route:
                                    return True 
                        elif type(rt_entry) == list:
                            for r in rt_entry:
                                nh_list = r.get('nh')
                                for nh in nh_list:
                                    if nh.get('via') == target_route:
                                        return True 

                    # Check route and make sure is a best path ('*')
                    if (
                        rt.get('rt-destination') == target_route     
                        and rt_entry.get('active-tag') == active_tag
                    ):  
                        # Verify the best path towards to {expected_to}
                        if expected_to:
                            if type(rt_entry) == dict:
                                nh_list = rt_entry.get('nh')
                                for nh in nh_list:
                                    if nh.get('to') == expected_to.split('/')[0]:
                                        return True 
                            elif type(rt_entry) == list:
                                for r in rt_entry:
                                    nh_list = r.get('nh')
                                    for nh in nh_list:
                                        if nh.get('to') == expected_to.split('/')[0]:
                                            return True 

                        # Verify best path IP address or Preference to best path
                        if (
                            rt_entry.get('learned-from') == ip_address
                            or rt_entry.get('local-preference') == preference
                            or rt_entry.get('med') == expected_med
                        ):
                            return True
                    
        timeout.sleep()
    return False 


def verify_route_best_path_metric(device,
                         expected_metric,
                         ip_address,
                         metric2=False,
                         max_time=60, 
                         check_interval=10,
                         protocol='bgp'
                        ):
    """ Verify the metric of best path

        Args:
            device (`obj`): Device object
            expected_metric (`int`): Expected metric number 
            ip_address (`str`): IP address in show command. 
            metric2(`bool`, optional): Flag used to distinguish 'metric' and 'metric2', default: False
            max_time (`int`, optional): Max time, default: 60 seconds
            check_interval (`int`, optional): Check interval, default: 10 seconds
        
        Returns:
            result (`bool`): Verified result
        
        Raises:
            N/A 
    """    
    timeout = Timeout(max_time, check_interval)
        
    while timeout.iterate():
        try:
            output = device.parse('show route protocol {protocol} {ip_address} extensive'.format(
                ip_address=ip_address,
                protocol=protocol))

        except SchemaEmptyParserError:
            log.info('Failed to parse. Device output might contain nothing.')
            timeout.sleep()
            continue
        
        # schema = {
        #     "route-information": {
        #         "route-table": [
        #             {
        #                   ...
        #                 "rt": [
        #                     {
        #                         "rt-destination": str,
        #                         "rt-entry": {
        #                             "protocol-nh": [
        #                              {'metric': int}
        #                              ]
        #                                   ...
        #                             "preference": str,
        #                             "metric":1,
        #                             "metric2":11,
        #                              ...
        #                         }
        #                     }
        #                 ],
        #                 ...
        #             }
        #         ]
        #     }
        # }
        
        route_tables = output.q.get_values('route-table')
        metric_key = 'metric2' if metric2 else 'metric'
        for routes in route_tables:
            rt_list = routes.get('rt')
            
            if rt_list:
                for rt in rt_list:
                    rt_entry = rt.get('rt-entry')

                    if type(rt_entry) == dict:
                        metric = Dq(rt_entry).get_values(metric_key, 0)

                        if int(metric) == expected_metric:
                            return True 

                    elif type(rt_entry) == list:
                        for r in rt_entry:
                            metric = Dq(r).get_values(metric_key, 0)

                            if int(metric) == expected_metric:
                                return True

                    
        timeout.sleep()
    return False     


def verify_route_non_best_path_metric(device,
                         non_expected_metric,
                         ip_address,
                         metric2=False,
                         max_time=60, 
                         check_interval=10,
                         protocol='bgp'
                        ):
    """ Verify the metric of non best path

        Args:
            device (`obj`): Device object
            non_expected_metric (`int`): Not expected metric number 
            ip_address (`str`): IP address in show command. 
            metric2(`bool`, optional): Flag used to distinguish 'metric' and 'metric2', default: False
            max_time (`int`, optional): Max time, default: 60 seconds
            check_interval (`int`, optional): Check interval, default: 10 seconds
        
        Returns:
            result (`bool`): Verified result
        
        Raises:
            N/A 
    """    
    timeout = Timeout(max_time, check_interval)
        
    while timeout.iterate():
        try:
            output = device.parse('show route protocol {protocol} {ip_address} extensive'.format(
                ip_address=ip_address,
                protocol=protocol))

        except SchemaEmptyParserError:
            log.info('Failed to parse. Device output might contain nothing.')
            timeout.sleep()
            continue
        
        # schema = {
        #     "route-information": {
        #         "route-table": [
        #             {
        #                   ...
        #                 "rt": [
        #                     {
        #                         "rt-destination": str,
        #                         "rt-entry": {
        #                             "protocol-nh": [
        #                              {'metric': int}
        #                              ]
        #                                   ...
        #                             "preference": str,
        #                              ...
        #                         }
        #                     }
        #                 ],
        #                 ...
        #             }
        #         ]
        #     }
        # }
        
        route_tables = output.q.get_values('route-table')
        metric_key = 'metric2' if metric2 else 'metric'

        for routes in route_tables:
            rt_list = routes.get('rt')
            
            if rt_list:
                for rt in rt_list:
                    rt_entry = rt.get('rt-entry')

                    if type(rt_entry) == dict:
                        metric = Dq(rt_entry).get_values(metric_key, 0)

                        if int(metric) != non_expected_metric:
                            return True 

                    elif type(rt_entry) == list:
                        for r in rt_entry:
                            metric = Dq(r).get_values(metric_key, 0)

                            if int(metric) != non_expected_metric:
                                return True
                    
        timeout.sleep()
    return False 


def verify_route_has_no_output(device,
                         target_route,
                         max_time=60,
                         check_interval=10,
                         protocol=None,
                         invert=False,
                         protocol_type=None,
                         peer_address=None,
                         target_address=None,
                         ):
    """Verify route has no output

    Args:
        target_route ('str'): Route to check
        max_time ('int', optional): Maximum time to keep checking. Default to 60.
        check_interval ('int', optional): How often to check. Default to 10.
        protocol ('str', optional): Protocol to check. Defaults to None.
        invert ('bool', optional): Invert the operation. Defaults to False
        protocol_type ('str', optional): Protocol type in show command, e.g., advertising-protocol
                                         or receive-protocol. Default to None.
        peer_address ('str', optional): Address used in command. Defaults to None. 
        target_address ('str', optional): Address used in command. Defaults to None. 

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            if peer_address and target_address:
                device.parse("show route receive-protocol {protocol} {peer_address} {target_address} extensive".format(
                    protocol=protocol,
                    peer_address=peer_address,
                    target_address=target_address
                ))
            
            elif protocol and protocol_type:
                device.parse("show route {protocol_type}-protocol {protocol} {address}".format(
                        protocol_type=protocol_type,
                        protocol=protocol,
                        address=target_route))
            elif protocol:
                device.parse(
                    "show route protocol {protocol} {route}".format(
                        protocol=protocol,
                        route=target_route
                    )
                )
            else:
                device.parse(
                    "show route {route} extensive".format(route=target_route))
        except SchemaEmptyParserError:
            if invert:
                timeout.sleep()
                continue
            return True

        if invert:
            return True
        timeout.sleep()
    return False


def verify_next_hop_in_route(device, route,
                           expected_next_hop,
                           protocol=None,
                           protocol_type=None,
                           active_tag=False,
                           max_time=60,
                           check_interval=10):
    """Verify next hop in route

        Args:
            device ('obj'): Device to use
            route ('str'): IP address in show command
            expected_next_hop ('str'): Next Hop address
            protocol ('str', optional): Protocol name that passed in command. Default to None.
            protocol_type ('str', optional): Protocol type in show command, e.g., advertising-protocol
                                             or receive-protocol. Default to None.
            active_tag (bool, optional): True if needs to verify next hop of best path. Default to False.
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
            if protocol and protocol_type:
                out = device.parse(
                    "show route {protocol_type}-protocol {protocol} {address}".format(
                        protocol_type=protocol_type,
                        protocol=protocol,
                        address=route))
            else:
                out = device.parse("show route {address} extensive".format(address=route))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example output
        # {
        #     "route-information": {
        #         "route-table": [{
        #                 "rt": [{
        #                         "rt-entry": {
        #                             "active-tag": "*",
        #                             "nh": [{
        #                                     "to": "30.0.0.2",
        #                                 }]}}],
        #                 "table-name": "inet.3",
        #             }]}}

        rt_list = Dq(out).get_values("rt")
        if '/' in expected_next_hop:
            expected_next_hop = expected_next_hop.split('/')[0]

        for rt in rt_list:
            rt_entry = rt.get('rt-entry', {})
            if isinstance(rt_entry, list):
                for elem in rt_entry:
                    if active_tag:
                        # Verify next hop of best path
                        if elem.get('active-tag', None) == '*' and \
                                expected_next_hop in Dq(elem).get_values('to'):
                            return True
                    elif expected_next_hop in Dq(elem).get_values('to'):
                        return True

            elif isinstance(rt_entry, dict):
                if active_tag:
                    # Verify next hop of best path
                    if rt_entry.get('active-tag', None) == '*' and \
                            expected_next_hop in Dq(rt_entry).get_values('to'):
                        return True
                elif expected_next_hop in Dq(rt_entry).get_values('to'):
                    return True

        timeout.sleep()
    return False


def verify_protocol_next_hop_in_route(device, route,
                           expected_protocol_next_hop,
                           max_time=60,
                           check_interval=10):
    """Verify protocol next hop in route

        Args:
            device ('obj'): Device to use
            route ('str'): IP address in show command
            expected_protocol_next_hop ('str'): Protocol next Hop address
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
            out = device.parse("show route {address} extensive".format(address=route))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        # Example output
        # {
        #     "route-information": {
        #         "route-table": [{
        #                 "rt": [{
        #                         "rt-entry": [{
        #                                     "protocol-nh": [
        #                                         {
        #                                             "to": "1.1.1.1",
        #                                             "indirect-nh": "0xc298604 1048574 INH Session ID: 0x3c1"
        #                                         },
        #                                         {
        #                                             "to": "1.1.1.1",
        #                                             "metric": "5",
        #                                         }
        #                                     ]}

        rt_list = Dq(out).get_values("rt")

        for rt in rt_list:
            protocol_nh_list = Dq(rt).get_values('protocol-nh')
            for nh_dict in protocol_nh_list:
                if nh_dict.get('to') == expected_protocol_next_hop:
                    return True

        timeout.sleep()
    return False


def verify_route_flag(device,
                      target_route,
                      expected_flag,
                      active_tag='*',
                      max_time=60,
                      check_interval=10
                      ):
    """ Verify the IGP/EGP flag

        Args:
            device (`obj`): Device object
            target_route ('str'): Route to check
            expected_flag (`str`): Expected IGP flag
            active_tag (`str`): Flag for 'best path'. Defaults to '*'.
            max_time (`int`, optional): Max time, default: 60 seconds
            check_interval (`int`, optional): Check interval, default: 10 seconds

        Returns:
            result (`bool`): Verified result

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse('show route protocol bgp')

        except SchemaEmptyParserError:
            log.info('Failed to parse. Device output might contain nothing.')
            timeout.sleep()
            continue

        # schema = {
        #     "route-information": {
        #         "route-table": [
        #             {
        #                   ...
        #                 "rt": [
        #                     {
        #                         "rt-destination": str,
        #                         "rt-entry": {
        #                                   ...
        #                                   "as-path" : " (12345) I"
        #                              ...
        #                         }
        #                     }
        #                 ],
        #                 ...
        #             }
        #         ]
        #     }
        # }

        route_tables = output.q.get_values('route-table')
        as_path_with_flag = re.compile(r'.*{expected_flag}.*'.format(expected_flag=expected_flag))
        rt_destination = ''

        for routes in route_tables:
            rt_list = routes.get('rt')

            if rt_list:
                for rt in rt_list:
                    if rt.get('rt-destination'):
                        rt_destination = rt.get('rt-destination')

                    # Verify there is {target_route}
                    if rt_destination == target_route:

                        rt_entry = rt.get('rt-entry')

                        # Verify this is best path
                        if rt_entry.get('active-tag') == active_tag:
                            if type(rt_entry) == dict:

                                # Obtain the value of key 'as-path'
                                as_path = Dq(rt_entry).get_values('as-path', 0)

                                # Sample output: AS path: 3 4 I, validation-state: unverified
                                # where flag is 'I'
                                if type(as_path) == str and as_path_with_flag.match(as_path):
                                    return True

                            elif type(rt_entry) == list:
                                for r in rt_entry:

                                    as_path = Dq(r).get_values('as-path', 0)

                                    if type(as_path) == str and as_path_with_flag.match(as_path):
                                        return True

                        # Verify flags in other paths
                        elif (not active_tag):
                            if type(rt_entry) == dict:

                                # Obtain the value of key 'as-path'
                                as_path = Dq(rt_entry).get_values('as-path', 0)

                                # Sample output: AS path: 3 4 E, validation-state: unverified
                                # where flag is 'E'
                                if type(as_path) == str and as_path_with_flag.match(as_path):
                                    return True

                            elif type(rt_entry) == list:
                                for r in rt_entry:

                                    as_path = Dq(r).get_values('as-path', 0)

                                    if type(as_path) == str and  as_path_with_flag.match(as_path):
                                        return True

        timeout.sleep()
    return False


def verify_route_table_mpls_label(device,
                                  table,
                                  label,
                                  expected_mpls_label,
                                  max_time=60,
                                  check_interval=10):
    """Verifies mpls label based on table name

    Args:
        device ('str'): Device object
        table ('str'): Table name
        label ('bool'): label for show command
        expected_mpls_label('str'): Expected MPLS label
        max_time ('int', optional): Maximum time to keep checking. Default to 60 seconds.
        check_interval ('int', optional): How often to check. Default to 10 seconds.

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)
    # Dictionary
    # 'table_name': {
    #         'inet.3': {
    #             'active_route_count': 3,
    #             'destination_count': 3,
    #             'hidden_route_count': 0,
    #             'holddown_route_count': 0,
    #             'routes': {
    #                 '10.169.197.254/32': {
    #                     'active_tag': '*',
    #                     'age': '02:14:05',
    #                     'metric': '1001',
    #                     'next_hop': {
    #                         'next_hop_list': {
    #                             1: {
    #                                 'best_route': '>',
    #                                 'to': '10.49.0.1',
    #                                 'via': 'ge-0/0/2.0'
    #                             }
    #                         }
    #                     },
    #                     'preference': '9',
    #                     'protocol_name': 'LDP'
    #                 },
    #                 '192.168.36.220/32': {
    #                     'active_tag': '*',
    #                     'age': '02:03:22',
    #                     'metric': '1111',
    #                     'next_hop': {
    #                         'next_hop_list': {
    #                             1: {
    #                                 'best_route': '>',
    #                                 'mpls_label': 'Push 307742',
    #                                 'to': '192.168.220.6',
    #                                 'via': 'ge-0/0/1.0'
    #                             }
    #                         }
    #                     },
    while timeout.iterate():
        out = None

        try:
            out = device.parse(
                "show route table {table} label {label}".format(
                    table=table,
                    label=label))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        mpls_label = out.q.contains(table).get_values('mpls_label', 0)
        if expected_mpls_label in mpls_label:
            return True

        timeout.sleep()

    return False


def verify_route_has_as_path(
        device: object,
        target_route: str,
        expected_as_path: str,
        max_time: int = 60,
        check_interval: int = 10,
        protocol_type: str = None,
        invert: bool = False,
        extensive: bool = False,
        peer_address: str = None
) -> bool:
    """Verifies a BGP route has an AS path

    Args:
        device (object): Device object
        target_route (str): Target route to check
        expected_as_path (str): Expected AS path
        max_time (int, optional): Maximum time to keep checking. Default to 60 seconds.
        check_interval (int, optional): How often to check. Default to 10 seconds.
        invert (bool, optional): Inverts to check if AS path doesn't exist. Defaults to False.
        extensive (bool, optional): True if show command ends with 'extensive'. Defaults to False.
        protocol_type ('str', optional): Protocol type in show command, e.g., advertising-protocol
                                             or receive-protocol. Default to None.
        peer_addrress ('str', optional): Address used in show command. Defaults to None. 
    Returns:
        bool: True/False
    """

    op = operator.contains
    if invert:
        op = lambda data, check: operator.not_(operator.contains(data, check))

    op1 = operator.eq
    if invert:
        op1 = operator.ne

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None

        try:
            if extensive:
                if protocol_type:
                    out = device.parse(
                        "show route {protocol_type}-protocol bgp {peer_address} extensive".format(
                                                peer_address=peer_address.split('/')[0],
                                                protocol_type=protocol_type)) 
                else:
                    out = device.parse("show route protocol bgp {route} extensive".format(route=target_route))
            else:
                out = device.parse("show route protocol bgp {route}".format(route=target_route))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dict
        # "route-information": {
        #         "route-table": [
        #             {
        #                 "rt": [
        #                     {
        #                         "rt-entry": {
        #                             "as-path": str,
        
        for route_table in out.q.get_values('route-table'):

            for rt in Dq(route_table).get_values('rt'):
                
                if protocol_type:
                    compared_text = Dq(rt).get_values('rt-destination', 0)+'/'+Dq(rt).get_values('rt-prefix-length',0)
                    if target_route == compared_text:
                        if expected_as_path in Dq(rt).get_values('attr-value', 0):
                            return True

                as_paths_ = rt.get('rt-entry', {}).get('as-path').split()

                # '(65001)'
                p = re.compile(r'\((?P<as>\d+)\)')
                for as_path in as_paths_:
                    m = p.match(as_path)
                    if m and m.groupdict()['as'] == str(expected_as_path):
                        return True

                if op(as_paths_, str(expected_as_path)):
                    return True

                expected_as_path_list = "AS path: {}".format(str(expected_as_path)).split()
                if op1(as_paths_, expected_as_path_list):
                    return True

        timeout.sleep()
    return False

def verify_route_has_as_path_length(
        device: object,
        expected_as_path_length: int,
        protocol_type: str = 'receive',
        peer_address: str = None,
        target_address: str = None,
        max_time: int = 60,
        check_interval: int = 10,
) -> bool:
    """Verifies a BGP route has an AS path

    Args:
        device (object): Device object
        expected_as_path_length (int): Expected AS path length
        protocol_type (str, optional): Protocol type in show command, e.g., advertising-protocol
                                        or receive-protocol. Defaults to 'receive'.
        peer_address (str, optional): Peer address used in show command. Defaults to None.
        target_address (str, optional): Target address used in show command. Defaults to None.
        max_time (int, optional): Maximum time to keep checking. Default to 60 seconds.
        check_interval (int, optional): How often to check. Default to 10 seconds.
    Returns:
        bool: True/False
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show route {protocol_type}-protocol bgp {peer_address} {target_address} extensive".format(
                    protocol_type=protocol_type,
                    peer_address=peer_address,
                    target_address=target_address,
                ))

        except SchemaEmptyParserError:
            timeout.sleep()
            continue    

        # show route {protocol_type}-protocol bgp {peer_address} {route} extensive
        # {
        #     "route-information": {
        #         "route-table": [
        #             {
        #                 "active-route-count": "18",
        #                 "destination-count": "18",
        #                 "hidden-route-count": "0",
        #                 "holddown-route-count": "0",
        #                 "rt": {
        #                     "rt-announced-count": "2",
        #                     "rt-destination": "4.4.4.4",
        #                     "rt-entry": {
        #                         "as-path": "AS path: I",
        #                         "bgp-path-attributes": {
        #                             "attr-as-path-effective": {
        #                                 "aspath-effective-string": "AS path:",
        #                                 "attr-value": "I" <---------------------------
        #                             }

        # '1 {123} {456} I' <------ only '1 {123} {456}' needed
        attr_value = out.q.get_values('attr-value', 0)
        attr_value_pattern = re.compile(r'(?P<attr_value>[\d{}\s]+)\w+')

        m = attr_value_pattern.match(attr_value)
        if m:
            sub_attr_value = m.groupdict()['attr_value']

            as_path_len = len(sub_attr_value.split())
            if expected_as_path_length == as_path_len:
                    return True

        timeout.sleep()
    return False

def verify_routing_accepted_message(
    device: object,
    route: str,
    expected_message: str,
    max_time: int = 60,
    check_interval: int = 10,
) -> bool:
    """Verify accepted message of route

    Args:
        device (object): Device object
        route (str): Route to check
        expected_message (str): Expected message to verify against
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:
        bool: True/False
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse(
                "show route {route} extensive".format(route=route))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dict
        # "route-information": {
        #         "route-table": [
        #             {
        #                 "rt": [
        #                     {
        #                         "rt-entry": {
        #                             "accepted": str,

        if expected_message in out.q.get_values('accepted'):
            return True
        
        timeout.sleep()

    return False

def verify_communities_in_route(device,
                                route,
                                expected_community,
                                max_time=60,
                                check_interval=10,):
    """Verify communities exist in show route

    Args:
        route ('str'): Route to check
        expected_community ('str'): Expected community in route

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None

        try:
            out = device.parse("show route {route} extensive".format(route=route))

        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        regexp = re.compile('Communities: +{community}'.format(
                 community=expected_community))
        for table_entry in out.q.get_values('route-table'):           

            for rt in table_entry.get('rt', []):
                               
                #"tsi": {
                #            "#text": "KRT in-kernel 10.220.0.0/16 -> 
                #                     {indirect(1048574)}\nPage 0 idx 1, (group hktGCS002 type Internal) Type 1 val 0x10c0b9b0 
                #                     (adv_entry)\nAdvertised metrics:\nFlags: Nexthop Change\nNexthop: Self\nMED: 12003\n
                #                      Localpref: 120\nAS path: [65171] (65151 65000) I\nCommunities: 65001:10 65151:244\nPath 10.220.0.0
                #                      \nfrom 10.169.14.240\nVector len 4.  Val: 1\nAS path: (65151 65000) I\nCommunities: 65001:10 65151:244\n
                #                      Localpref: 120\nAS path: (65151 65000) I\nCommunities: 65001:10 65151:244\nLocalpref: 120"
                #        }

                if rt.get('tsi', {}):

                    if not regexp.search(rt.get('tsi', {}).get("#text", None)):
                        continue
                else:
                    continue

                return True
            
            timeout.sleep()

    return False


def _checkAsPath(rt_entry, expected_as_length):
        if isinstance(rt_entry, dict):
            as_path = Dq(rt_entry).get_values('as-path')
            if as_path and int(len(as_path[0].split())) - 1 == expected_as_length:
                return True

        elif isinstance(rt_entry, list):
            for elem in rt_entry:
                as_path = Dq(elem).get_values('as-path')
                if as_path and int(len(as_path[0].split())) == expected_as_length:
                    return True
        return False


def verify_route_as_length(device,
                          route,
                          expected_bestpath_as_length,
                          expected_nonbestpath_as_length=None,
                          max_time=60,
                          check_interval=10
                          ):
    """ Verify the length as-path of best path and non best path

        Args:
            device (`obj`): Device object
            route('str'): Target route address
            expected_bestpath_as_length (`int`): Expected best path as length
            expected_nonbestpath_as_length (`int`): Expected non best path as length, default: None
            max_time (`int`, optional): Max time, default: 60 seconds
            check_interval (`int`, optional): Check interval, default: 10 seconds

        Returns:
            result (`bool`): Verified result

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    is_as_path_matched = False

    while timeout.iterate():
        try:
            output = device.parse('show route protocol bgp')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        
        # schema = {
        #     "route-information": {
        #         "route-table": [
        #             {
        #                   ...
        #                 "rt": [
        #                     {
        #                         "rt-destination": str,
        #                         "rt-entry": {
        #                             "as-path": "4 2 I"
        #                              ...

        for rt in output.q.get_values('rt'):
            rt_entry = rt.get('rt-entry', {})
            rt_destination = rt.get('rt-destination', '')

            # Check as length of best path only
            if not expected_nonbestpath_as_length:
                if rt_destination == route:
                    return _checkAsPath(rt_entry, expected_bestpath_as_length)

            # Check as length of best path and non best path
            else:
                if rt_destination == route:
                    if not _checkAsPath(rt_entry, expected_bestpath_as_length):
                        is_as_path_matched = False
                        break
                    else:
                        is_as_path_matched = True
                elif not rt_destination:
                    if not _checkAsPath(rt_entry, expected_nonbestpath_as_length):
                        is_as_path_matched = False
                        break
                    else:
                        is_as_path_matched = True

        if is_as_path_matched:
            return True

        timeout.sleep()
    return False


def verify_best_path_is_towards_to_interface(device,
                           route=None,
                           protocol=None,
                           expected_ip_address=None,
                           expected_target_route=None,
                           expected_via=None,
                           max_time=60,
                           check_interval=10,
                           extensive=False):
    """Verify best path towards to given interface

        Args:
            device ('obj'): Device to use
            route ('str'): Route name. Default to None.
            protocol ('str'): Protocol name. Default to None.
            expected_ip_address ('str'): Expected IP address. Default to None.
            expected_target_route ('str'): Expected target route. Default to None.
            expected_via ('str'): Expected via interface. Default to None.
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
            if extensive:
                if protocol and route:
                    out = device.parse("show route protocol {protocol} {route} extensive".format(
                        protocol=protocol,
                        route=route
                    ))
                elif protocol:
                    out = device.parse("show route protocol {protocol} extensive".format(
                        protocol=protocol
                    ))
            else:
                out = device.parse("show route protocol {protocol}".format(
                    protocol=protocol
                ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example output
        # {
        #     "route-information": {
        #         "route-table": [{
        #                 "rt": [{
        #                         "rt-entry": {
        #                             "nh": [{
        #                                     "to": "30.0.0.2",
        #                                 }]}}],
        #                 "table-name": "inet.3",
        #             }]}}

        rt_list = Dq(out).get_values("rt")
        for rt in rt_list:
            if isinstance(rt.get('rt-entry'), dict):
                rt_entry_list = [rt.get('rt-entry')]
            else:
                rt_entry_list = Dq(rt).get_values('rt-entry')
            
            for rt_entry in rt_entry_list:
                best_path = rt_entry.get('active-tag', None)
                if not best_path:
                    continue

                rt_destination = rt.get('rt-destination', '')
                
                if expected_target_route:
                    if rt_destination != expected_target_route:
                        continue
                
                if expected_ip_address:
                    expected_ip_address = expected_ip_address.split('/')[0]
                    if expected_ip_address not in Dq(rt).get_values('to'):
                        continue
                
                if expected_via and expected_via not in Dq(rt).get_values('via'):
                    continue

                return True

        timeout.sleep()
    return False
    
def _getMetricInroute(output):
    metric_dict = {}
    rt_list = Dq(output).get_values("rt")
    for rt in rt_list:
        rt_entry = rt.get('rt-entry', {})
        if isinstance(rt_entry, list):
            for elem in rt_entry:
                if elem.get('active-tag', None) == '*':
                    # Verify next hop of best path
                    metric = elem.get('metric', None)
                    metric_dict['best_path'] = int(metric) if metric else None
                else:
                    # Verify next hop of non best path
                    metric = elem.get('metric', None)
                    metric_dict['non_best_path'] = int(metric) if metric else None

        elif isinstance(rt_entry, dict):
            if rt_entry.get('active-tag', None) == '*':
                # Verify next hop of best path
                metric = rt_entry.get('metric', None)
                metric_dict['best_path'] = int(metric) if metric else None
            else:
                # Verify next hop of non best path
                metric = rt_entry.get('metric', None)
                metric_dict['non_best_path'] = int(metric) if metric else None

        return metric_dict

def verify_metric_of_route(device,
                              expected_metric,
                              ip_address,
                              active_tag=False,
                              max_time=60,
                              check_interval=10
                              ):
    """ Verify the metric of best path and non best path

        Args:
            device ('obj'): Device object
            expected_metric ('int'): Expected metric number
            ip_address ('str'): IP address in show command.
            active_tag (bool, optional): True if needs to verify metric of best path. Default to False.
            max_time ('int', optional): Max time, default: 60 seconds
            check_interval ('int', optional): Check interval, default: 10 seconds

        Returns:
            result (`bool`): Verified result

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse('show route {ip_address} extensive'.format(ip_address=ip_address))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # schema = {
        #     "route-information": {
        #         "route-table": [
        #             {
        #                   ...
        #                 "rt": [
        #                     {
        #                         "rt-destination": str,
        #                         "rt-entry":
        #                             "active-tag": "*",
        #                             "metric":1,
        #                              ...

        metric_result = _getMetricInroute(output)
        if active_tag and metric_result.get('best_path', None) == expected_metric:
            return True
        elif not active_tag and metric_result.get('non_best_path', None) == expected_metric:
            return True

        timeout.sleep()
    return False

def compare_metric_of_route(device,
                            ip_address,
                            max_time=60,
                            invert=False,
                            check_interval=10
                            ):
    """ Compare the metric of best path and non best path

        Args:
            device ('obj'): Device object
            ip_address ('str'): IP address in show command.
            invert(bool, optional): Inverts from equals to not equals. Defaults to False.
            max_time ('int', optional): Max time, default: 60 seconds
            check_interval ('int', optional): Check interval, default: 10 seconds

        Returns:
            result (`bool`): Verified result

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    op = operator.ge
    if invert:
        op = operator.le

    while timeout.iterate():
        try:
            output = device.parse('show route {ip_address} extensive'.format(ip_address=ip_address))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        
        # schema = {
        #     "route-information": {
        #         "route-table": [
        #             {
        #                   ...
        #                 "rt": [
        #                     {
        #                         "rt-destination": str,
        #                         "rt-entry":
        #                             "active-tag": "*",
        #                             "metric":1,
        #                              ...

        metric_result = _getMetricInroute(output)
        if metric_result.get('best_path') and metric_result.get('non_best_path') and \
                op(metric_result.get('best_path'), metric_result.get('non_best_path')):
            return True

        timeout.sleep()
    return False

def verify_rt_destination(device,
                          target_route,
                          invert=False,
                          max_time=60,
                          check_interval=10,
                          interface=None,
                          extensive=False,
                          protocol=None,
                          protocol_type=None):
    """Verify rt destination

        Args:
            device ('obj'): Device to use
            target_route ('str'): target route address
            invert(bool, optional): Inverts from equals to not equals. Defaults to False.
            max_time ('int', optional): Maximum time to keep checking. Default to 60 seconds.
            check_interval ('int', optional): How often to check. Default to 10 seconds.
            interface ('str', optional): expected interface address. Default to None.
            extensive(bool, optional): True if show command has extensive. Defaults to False.
            protocol ('str', optional): Protocol name that passed in command. Default to None.
            protocol_type ('str', optional): Protocol type in show command, e.g., advertising-protocol
                                             or receive-protocol. Default to None.

        Returns:
            True/False

        Raises:
            N/A
    """
    op = operator.eq
    if invert:
        op = operator.ne

    if interface:
        interface = interface.split('/')[0]

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            if protocol and protocol_type and interface:
                out = device.parse("show route {protocol_type}-protocol {protocol} {address}".format(
                        protocol_type=protocol_type,
                        protocol=protocol,
                        address=interface))
            elif extensive:
                out = device.parse("show route {route} extensive".format(route=target_route))
            else:
                out = device.parse("show route protocol bgp")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example output
        # {
        #     "route-information": {
        #         "route-table": [{
        #                 "rt": [{
        #                         "rt-destination": '0.0.0.0/0',

        rt_list = Dq(out).get_values("rt")
        if not rt_list and invert:
            return True

        for rt in rt_list:
            rt_destination = rt.get('rt-destination', '')
            if op(rt_destination, target_route):
                return True

        timeout.sleep()
    return False


def verify_route_as_path_count(
    device: object,
    route: str,
    expected_count: int,
    excluded_paths: list = list(),
    best_path: bool = True,
    max_time: int = 60,
    check_internval: int = 10
) -> bool:
    """Verify route as path count

    Args:
        device (object): Device object
        route (str): Route to check
        expected_count (int): Expected count to check against
        excluded_paths (list, optional): Paths to exclude. Defaults to [].
        best_path (bool, optional): Check the best path or the next, non-best path. Defaults to True.
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_internval (int, optional): Check interval. Defaults to 10.

    Returns:
        bool: True/False
    """

    timeout = Timeout(max_time, check_internval)
    while timeout.iterate():
        try:
            out = device.parse('show route protocol bgp {route} extensive'.format(
                route=route
            ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # schema = {
        #     "route-information": {
        #         "route-table": [
        #             {
        #                   ...
        #                 "rt": [
        #                     {
        #                         "rt-destination": str,
        #                         "rt-entry": {
        #                             "as-path": "4 2 I"
        #                              ...

        excluded_paths = [str(path) for path in excluded_paths] + ['AS', 'path:']
        break_loop = False

        as_path = list()

        for rt in out.q.get_values('rt'):
            rt_entry_ = rt.get('rt-entry', {})
            if not isinstance(rt_entry_, list):
                rt_entry_ = [rt_entry_]
            for rt_entry in rt_entry_:
                if best_path and rt_entry.get('active-tag') == "*":
                    as_path_ = rt_entry.get('as-path')
                    as_path = [path for path in as_path_.split() if path.translate(
                        {ord('('):None,ord(')'):None}) not in excluded_paths]
                    break_loop = True
                    break
                elif not best_path and not rt_entry.get('active-tag'):
                    as_path_ = rt_entry.get('as-path')
                    as_path = [path for path in as_path_.split() if path.translate(
                        {ord('('):None,ord(')'):None}) not in excluded_paths]
                    break_loop = True
                    break
            if break_loop:
                break

        if len(as_path)-1 == expected_count:
            return True

        timeout.sleep()
    return False


def verify_route_all_as_length(
    device: object,
    route: str,
    expected_path_as_length: str,
    excluded_paths: list = [],
    max_time: int = 60,
    check_interval: int = 10
    ) -> bool:
    """Verifies the as path length of all paths

    Args:
        device (object): Device object
        route (str): Route to check path lengths of
        expected_path_as_length (str): Expected AS path length
        excluded_paths (list, optional): Paths to exclude from the count. Defaults to [].
        max_time (int, optional): Max timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:
        bool: True/False
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show route {route} extensive'.format(
                route = route
            ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # schema = {
        #     "route-information": {
        #         "route-table": [
        #             {
        #                   ...
        #                 "rt": [
        #                     {
        #                         "rt-destination": str,
        #                         "rt-entry": {
        #                             "as-path": "4 2 I"
        #                              ...
        excluded_paths = [str(path) for path in excluded_paths]
        failed = False

        for as_path in output.q.get_values('as-path'):
            as_path = as_path.replace('AS path: ', '')
            if len(
                [path for path in as_path.split(' ') if path.translate(
                    {ord('('):None,ord(')'):None}) not in excluded_paths]
                ) - 1 != expected_path_as_length:
                failed = True
                break

        if failed:
            timeout.sleep()
            continue

        return True
        
    return False


def verify_route_same_as_peer_local(
    device: object,
    target_route: str,
    best_path: bool = True,
    invert: bool = False,
    max_time: int = 60,
    check_interval: int = 10,
) -> bool:
    """Verifies a route's Peer AS and Local AS are the same

    Args:
        device (object): Device object
        target_route (str): Target route to check
        best_path (bool): Whether to check the best path or not
        invert (bool, optional): Invert to check if they're different. Defaults to False.
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:
        bool: True/False
    """
    bp_op = operator.eq
    if not best_path:
        bp_op = operator.ne

    invert_op = operator.eq
    if invert:
        invert_op = operator.ne

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show route {route} extensive'.format(
                route = target_route
            ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dict
        # Optional("@xmlns:junos"): str,
        #     "route-information": {
        #         "route-table": [
        #             {
        #                 "rt": [
        #                     {
        #                         "rt-entry": {
        #                             "local-as": str,
        #                             "peer-as": str,

        for rt in output.q.get_values('rt'):
            for rt_entry in Dq(rt).get_values('rt-entry'):
                rt_entry_ = Dq(rt_entry)
                if bp_op(rt_entry_.get_values('active-tag', 0), '*'):
                    if invert_op(rt_entry_.get_values('peer-as', 0), rt_entry_.get_values('local-as', 0)):
                        return True
        
        timeout.sleep()

    return False


def verify_route_table_output_interface(device,
                             label,
                             table='mpls.0',
                             output_interface=None,
                             max_time=60,
                             check_interval=10):
    """ Verify the route table output interface

        Args:
            device (`obj`): Device object
            label (`str`): show route label
            table (`str`): Table name, Default mpls.0
            output_interface (`str`): Output interface. Defaults to None.
            max_time ('int', optional): Maximum time to keep checking. Default to 60 seconds.
            check_interval ('int', optional): How often to check. Default to 10 seconds.
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show route table {table} label {label}'.format(
                table=table,
                label=label))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        # "next_hop_list": {
        #                     1: {
        #                         "to": "10.19.198.66",
        #                         "via": "ge-0/0/3.0",
        #                         "best_route": ">",
        #                         "mpls_label": "Swap 78",
        #                     }
        output_interface_ = Dq(out).contains(label).get_values('via',0)
        if output_interface_ == output_interface:
            return True

        timeout.sleep()


    return False

def verify_route_forwarding_table(device, label, expected_type, expected_nh_index=None, 
    expected_netif=None, max_time=60, check_interval=10):
    """ Verifies route-forwarding type given a label

    Args:
        device (obj): Device object
        label (str): Label to check
        expected_type (str): Expected type
        expected_nh_index (str): Expected nh-index. Defaults to None
        expected_netif (str): Expected netif. Defaults to None
        max_time (int, optional): Maximum sleep time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:
        str or None: mpls out label
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            
            out = device.parse('show route forwarding-table label {label}'.format(
                label=label
            ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        

        # Example dictionary
        # {
        #     "forwarding-table-information":{
        #         "route-table": [{
        #                 "rt-entry": [{
        #                         "nh":{
        #                             "nh-type": str,
        #                         }
        #                     }]
        #             }]
        #     }
        # }

        for rt_dict in out.q.get_values('rt-entry'):
            
            rt_dict_dq = Dq(rt_dict)
            nh_type_ = rt_dict_dq.get_values('nh-type', 0)
            if nh_type_ != expected_type:
                continue

            if expected_nh_index:
                nh_index_ = rt_dict_dq.get_values('nh-index', 0)
                if nh_index_ != expected_nh_index:
                    continue
            
            if expected_netif:
                netif_ = rt_dict_dq.get_values('via', 0)
                if netif_ != expected_netif:
                    log.info(netif_)
                    log.info(expected_netif)
                    continue
            
            return True
        
        timeout.sleep()

    return False


def verify_route_peer_as(
    device: object,
    route: str,
    expected_peer_as: str,
    best_path: bool = True,
    max_time: int = 60,
    check_interval: int = 10,
) -> bool:
    """Verify a BGP route's peer as

    Args:
        device (object): Device object
        route (str): Route to check
        expected_peer_as (str): Expected peer as to check for
        best_path (bool, optional): Whether to check the best route or not. Defaults to True.
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Checkout interval. Defaults to 10.

    Returns:
        bool: True/False
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show route {route} extensive".format(
                route=route
            ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dict
        # Optional("@xmlns:junos"): str,
        #     "route-information": {
        #         "route-table": [
        #             {
        #                 "rt": [
        #                     {
        #                         "rt-entry": {
        #                             "peer-as": str,

        for rt in out.q.get_values('rt-entry'):
            if best_path and rt.get('active-tag') == "*":
                peer_as_ = rt.get('peer-as')
                break
            elif not best_path and not rt.get('active-tag'):
                peer_as_ = rt.get('peer-as')
                break

        if str(peer_as_) == str(expected_peer_as):
            return True

        timeout.sleep()
    return False


def verify_route_push_label(device, table_name, expected_label, ip_address,
    max_time=60, check_interval=10):
    """ Verifies there is Push expected_label in the table_name via show route ip_address

    Args:
        device (obj): Device object
        table_name (str): Given table name
        expected_label (str): Expected label
        ip_address (str): IP address used in show command
        max_time (int, optional): Maximum sleep time. Defaults to 60 seconds.
        check_interval (int, optional): Check interval. Defaults to 10 seconds.

    Returns:
        bool
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            
            out = device.parse('show route {ip_address}'.format(
                ip_address=ip_address
            ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue    

        # {'route-information': {'route-table': [{'active-route-count': '1',
        #                                 'table-name': 'inet.3', <-----------------------------
        #                                 'rt': [{'rt-destination': '3.3.3.3/32',
        #                                         'rt-entry': {'active-tag': '*',
        #                                                      'age': {'#text': '00:01:13'},
        #                                                      'as-path': ' 1 I',
        #                                                      'local-preference': '100',
        #                                                      'med': '1',
        #                                                      'nh': [{'mpls-label': 'Push '
        #                                                                            '38', <-----------------------------
        #                                                              'to': '20.0.0.1',
        #                                                              'via': 'ge-0/0/0.0'}],

        filtered_out = out.q.contains('{table_name}|nh'.format(table_name=table_name),regex=True).reconstruct()
        mpls_label = Dq(filtered_out).get_values('mpls-label', 0)
        # mple_label:
        # 'Push 38' or [] 

        if type(mpls_label) == str:
            if int(mpls_label.split(' ')[1]) == expected_label:
                return True 
        timeout.sleep()

    return False   


def verify_route_table_label_output(device,  
                                    label_name,
                                    table_name='mpls.0',
                                    max_time=60, 
                                    check_interval=10):
    """ Verifies there is path via show route table table_name label label_name

    Args:
        device (obj): Device object
        table_name (str): Table name used in show command. Defaults to 'mpls.0'
        label_name (str): Given label used in show command
        max_time (int, optional): Maximum sleep time. Defaults to 60 seconds.
        check_interval (int, optional): Check interval. Defaults to 10 seconds.

    Returns:
        bool
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show route table {table_name} label {label_name}'.format(
                table_name=table_name,
                label_name=label_name
            ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue    

        # {'table_name': {'mpls.0': {'active_route_count': 10,
        #                         'destination_count': 10,
        #                         'hidden_route_count': 0,
        #                         'holddown_route_count': 0,
        #                         'routes': {'46': {'active_tag': '*',  <------------------------ '46' is a label
        #                                             'age': '00:07:53',
        #                                             'next_hop': {'next_hop_list': {1: {'best_route': '>',
        #                                                                                 'mpls_label': 'Pop',
        #                                                                                 'to': '30.0.0.2',
        #                                                                                 'via': 'ge-0/0/1.0'}}},
        #                                             'preference': '170',
        #                                             'protocol_name': 'VPN'},
        #                                     '46(S=0)': {'active_tag': '*', <------------------------ '46(S=0)' is a label
        
        labels = out.q.get_values('routes')
        # labels:
        # ['46', '46(S=0)'] or [] 

        if label_name in labels:
            return True 
        timeout.sleep()

    return False        


def verify_route_exists(device, expected_route, invert=False, max_time=60, check_interval=10):
    """ Verifies route exists via show route protocol bgp

    Args:
        device (obj): Device object
        expected_route (str): Expected route
        invert (bool): Default to False. Set to True if verify route doesn't exist.
        max_time (int, optional): Maximum sleep time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.    
    Returns:
        bool
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:       
            out = device.parse('show route protocol bgp')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue  

        # {'route-information': {'route-table': [{'active-route-count': '14',
        #                                 'destination-count': '14',
        #                                 'hidden-route-count': '0',
        #                                 'holddown-route-count': '0',
        #                                 'rt': [{'rt-destination': '1.0.0.0/24', <----------------------
        #                                         'rt-entry': {'age': {'#text': '00:00:48'},
        #                                                      'as-path': ' 2 I',
        #                                                      'local-preference': '100',
        #                                                      'nh': [{'to': '20.0.0.2',

        routes = out.q.get_values('rt-destination')

        if invert:
            if expected_route not in routes:
                return True 
        
        if expected_route in routes:
            return True      
        timeout.sleep()

    return False                     

def verify_preference_show_route(device,
                                 address,
                                 preference,
                                 max_time=60,
                                 check_interval=10):
    """ Verify routing interface preference

        Args:
            device ('str'): Device str
            address ('str'): address to be ued in show command
            preference ('int'): Preference name
            max_time (`int`): Max time, defaults to 60 seconds
            check_interval (`int`): Check interval, defaults to 10 seconds
        Returns:
            True / False
        Raises:
            None

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse(
                'show route protocol bgp extensive {address}'.format(
                    address=address))

        except SchemaEmptyParserError:
            timeout.sleep()
            continue


        # Example dictionary structure:
        #"rt": {
        #            "rt-announced-count": "1",
        #            "rt-destination": "100.0.0.0",
        #            "rt-entry": {
        #                "active-tag": "*",
        #                "age": {
        #                    "#text": "4:32"
        #                },
        #                "bgp-rt-flag": "Accepted",
        #                "gateway": "60.0.0.2",
        #                "local-as": "1",
        #                "local-preference": "100",
        #                "peer-as": "2",
        #                "peer-id": "206.26.0.1",
        #                "preference": "170",
        #                "preference2": "101",
        #                "protocol-name": "BGP",
        #            },
        #}

        rt_destination = out.q.get_values("rt-destination",0)
        
        if str(rt_destination) == str(address) and out.q.get_values("preference", 0) == str(preference):
            return True

        timeout.sleep()

    return False


def verify_cluster_exists_in_route(device,
                                   protocol,
                                   address,
                                   cluster_value,
                                   max_time=60,
                                   check_interval=10):
    """Verifies cluster exists in route

    Args:
        device ('obj'): device to use
        address ('str'): IP address for show command
        protocol ('str'): Protocol to use in show command
        cluster_value('str'): Cluster value in show route
        max_time ('int', optional): Maximum time to keep checking. Default to 60 seconds.
        check_interval ('int', optional): How often to check. Default to 10 seconds.

    Returns:
        True/False

    Raises:
        N/A
    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse(
                "show route protocol {protocol} {address} extensive".format(protocol=protocol, address=address))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        #[{"rt-entry-state": "Active Int Ext",
        #"validation-state": "unverified",
        #"task-name": "BGP_2.2.2.2.2",
        #"announce-bits": "2",
        #"announce-tasks": "0-KRT 5-Resolve tree 1",
        #"cluster-list": "2.2.2.2 4.4.4.4"}]
        if cluster_value:
            cluster_item = Dq(output).get_values("cluster-list", 0)
            if cluster_value in str(cluster_item):
                return True
            else:
                timeout.sleep()
                continue
                
        timeout.sleep()

    return False

    
def verify_route_best_path_counter(device, expected_count, protocol=None, ip_address=None,
    max_time=60, check_interval=10):
    """ Verify best path counter

        Args:
            device ('str'): Device str
            expected_count ('int'): Expected best path count
            protocol ('str'): Protocol name. Default to None
            ip_address ('str'): IP address. Default to None.
            max_time (`int`, optional): Max time, defaults to 60 seconds
            check_interval (`int`, optional): Check interval, defaults to 10 seconds
        Returns:
            True / False
        Raises:
            None

    """

    timeout = Timeout(max_time, check_interval)
    
    while timeout.iterate():
        try:
            out = device.parse('show route protocol {protocol} {ip_address}'.format(
                protocol=protocol,
                ip_address=ip_address
            ))
        except Exception as e:
            timeout.sleep()
            continue
        
        # Example dictionary structure:
        #"rt": {
        #            "rt-announced-count": "1",
        #            "rt-destination": "100.0.0.0",
        #            "rt-entry": {
        #                "active-tag": "*",

        rt_list = out.q.contains('active-tag|nh', regex=True).get_values('rt')

        best_path_counter = 0

        for rt in rt_list:
            rt_entry = rt.get('rt-entry', {})
            if not rt_entry.get('active-tag', None):
                continue
            nh_list = Dq(rt_entry).get_values('nh')
            best_path_counter = best_path_counter + len(nh_list)
        
        if expected_count == best_path_counter:
            return True
        
    return False

def verify_route_logical_system_has_no_output(device,
                         logical_name,
                         max_time=60,
                         check_interval=10,
                         invert=False
                         ):
    """Verify route logical system has no output

    Args:
        logical_name ('str'): Logical system name
        max_time ('int', optional): Maximum time to keep checking. Default to 60.
        check_interval ('int', optional): How often to check. Default to 10.
        invert ('bool', optional): Invert the operation. Defaults to False

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            device.parse(
                "show route logical-system {logical_name}".format(logical_name=logical_name))
        except SchemaEmptyParserError:
            if invert:
                timeout.sleep()
                continue
            return True

        if invert:
            return True
        timeout.sleep()
    return False