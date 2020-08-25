'''Common get info functions for running-config'''
# Python
import re
import logging
# unicon
from unicon.core.errors import SubCommandFailure
from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.libs.sdk.apis.utils import get_config_dict
from genie.utils import Dq

log = logging.getLogger(__name__)

def get_active_outgoing_interface(device, destination_address, extensive=False):
    """ Get active outgoing interface value

        Args:
            device (`obj`): Device object
            destination_address (`str`): Destination address value
            extensive ('bool'): Try command with extensive 
        Returns:
            Interface name
    """

    try:
        if extensive:
            out = device.parse('show route protocol static extensive')
        else:
            out = device.parse('show route protocol static')
    except SchemaEmptyParserError:
        return None
    
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
        rt_destination_ = Dq(rt_dict).get_values("rt-destination", 0)
        if not rt_destination_.startswith(destination_address):
            continue

        active_tag_ = Dq(rt_dict).get_values("active-tag", None)
        if not active_tag_:
            continue

        via_ = Dq(rt_dict).get_values("via", None)
        if not via_:
            continue

        return via_.pop()
    
    return None

def get_route_destination_address(device, extensive=None, prefix='inet.0', protocol='Direct', 
                                  interface='ge-0/0/0.0'):
    """Get destination address that matches criteria

    Args:
        device (obj): device object
        extensive (bool): Show extensive output. Defaults to None.
        prefix (str, optional): Route prefix. Defaults to None.
        protocol (str, optional): Route protocol. Defaults to None.
        interface (str, optional): Route interface. Defaults to None.

    Returns:
        str: The destination address
    """

    try:
        if extensive:
            out = device.parse('show route extensive')
        else:
            out = device.parse('show route')
    except SchemaEmptyParserError:
        return None
    
    # Example dictionary structure:
    #         {
    #             'rt': [{'rt-destination': '0.0.0.0/0',
    #                    'rt-entry': {'active-tag': '*',
    #                                 'age': {'#text': '02:53:14'},
    #                                 'nh': [{'to': '172.16.1.254',
    #                                         'via': 'ge-0/0/0.0'}],
    #                                 'preference': '12',
    #                                 'protocol-name': 'Access-internal'}},
    #                   {'rt-destination': '12.1.1.0/24',
    #                    'rt-entry': {'active-tag': '*',
    #                                 'age': {'#text': '5w1d '
    #                                                  '19:01:21'},
    #                                 'nh': [{'via': 'ge-0/0/3.0'}],
    #                                 'preference': '0',
    #                                 'protocol-name': 'Direct'}},
    #                   {'rt-destination': '12.1.1.2/32',
    #                    'rt-entry': {'active-tag': '*',
    #                                 'age': {'#text': '5w1d '
    #                                                  '19:01:21'},
    #                                 'nh': [{'nh-local-interface': 'ge-0/0/3.0'}],
    #                                 'preference': '0',
    #                                 'protocol-name': 'Local'}},
    #         },
    route_table_list = Dq(out).get_values("route-table")
    for route in route_table_list:
        if prefix:
            prefix_ = Dq(route).get_values('table-name', 0)
            if not prefix_.lower().startswith(prefix.lower()):
                continue
        
        rt_list = Dq(route).get_values('rt')
        for rt_dict in rt_list:
            if protocol:
                protocol_ = Dq(rt_dict).get_values('protocol-name', 0)
                if not protocol_.lower().startswith(protocol.lower()):
                    continue

            if interface:
                interface_ = Dq(rt_dict).get_values('via', 0) or Dq(rt_dict).get_values('nh-local-interface', 0)
                if not interface_.lower().startswith(interface.lower()):
                    continue

            return Dq(rt_dict).get_values('rt-destination', 0)
    
    return None

def get_route_table_switched_path_destination_address(device, table, name):
    """ Get route table switched path destination address

    Args:
        device (obj): Device object
        table (str): Table name
        name (str): switched path label

    Returns:
        str or None: metric value
    """

    # Example dictionary
    # {
    #     "route-information": {
    #         "route-table": {
    #             "rt": [{
    #                 "rt-destination": str,
    #             }]
    #         }
    #     }
    # }

    try:
        out = device.parse('show route table {table} label-switched-path {name}'.format(
            table=table,
            name=name
        ))
    except SchemaEmptyParserError:
        return None

    

    return out.q.get_values('rt-destination', 0) or None

def get_ospf_metric(device,
                    destination_address):
    """Get OSPF metric

    Args:
        device (obj): Device object
        destination_address (str): Destination address
    """
    out = device.parse('show route')
    

    # Example dictionary

    # "route-table": [
    #             {
    #                 "active-route-count": "0",
    #                 "destination-count": "0",
    #                 "hidden-route-count": "0",
    #                 "holddown-route-count": "0",
    #                 "rt": [
    #                     {
    #                             "metric": "101",
    #                         }
    #                     },

    rt_list = Dq(out).get_values('rt')
    for rt_dict in rt_list:
        rt_destination_ = Dq(rt_dict).get_values("rt-destination", 0)
        if not isinstance(rt_destination_, list):
            if rt_destination_.startswith(str(destination_address)):
                metric_ = Dq(rt_dict).get_values('metric', 0)
                if not metric_:
                    continue
                return metric_
    return None


def get_route_advertising_label(device,
                          protocol,
                          ip_address,
                          route,
                          table_name):
    """Get the label with given table_name via
        'show route advertising-protocol {protocol} {ip_address} {route} detail'

        Args:
            device ('obj'): Device to use
            protocol ('str'): Protocol used in show command
            ip_address ('str'): IP address used in show command
            route ('str'): Route used in show command
            table_name ('str'): Label inet

        Returns:
            str

        Raises:
            N/A
    """
    out = device.parse(
        "show route advertising-protocol {protocol} {ip_address} {route} detail".format(
            protocol=protocol,
            ip_address=ip_address,
            route=route
        )
    )
    # Example output
    # {'route-information': {'route-table': [{'table-name': 'inet.3', <------------------
    #                                         'rt-entry': {'active-tag': '*',
    #                                                     'as-path': '[1] I',
    #                                                     'bgp-group': {'bgp-group-name': 'eBGP_SUT-2',
    #                                                                 'bgp-group-type': 'External'},
    #                                                     'flags': 'Nexthop Change',
    #                                                     'med': '1',
    #                                                     'nh': {'to': 'Self'},
    #                                                     'route-label': '17', <------------------

    filtered_out = out.q.contains('{table_name}|route-label'.format(table_name=table_name),regex=True).reconstruct()
    # filtered_out: 
    # {'route-information': {'route-table': [{'rt-entry': {'route-label': '19'},
    #                                     'table-name': 'inet.3'}]}}
    
    rt_list = Dq(filtered_out).get_values('route-table')
    # rt_list:
    # [{'table-name': 'inet.3', 'rt-entry': {'route-label': '19'}}]

    for rt in rt_list:
        if rt.get('table-name') == table_name:
            label = Dq(rt).get_values('route-label', 0)
            if type(label) == str:
                return int(label)
            
    return None
def get_route_table_output_interface(device,
    table, route):
    """Get route table output interface

    Args:
        device (obj): Device object
        table (str): Table name
        route (str): Route IP address
    
    Returns:
        output_interface (str)
    """

    # Example Dictionary
    # {'table_name': {'inet.3': {'active_route_count': 5001,
    #                        'destination_count': 5001,
    #                        'hidden_route_count': 0,
    #                        'holddown_route_count': 0,
    #                        'routes': {'200.0.0.0/32': {'active_tag': '*',
    #                                                    'age': '00:01:29',
    #                                                    'metric': '1',
    #                                                    'next_hop': {'next_hop_list': {1: {'best_route': '>',
    #                                                                                       'mpls_label': 'Push '
    #                                                                                                     '574',
    #                                                                                       'to': '106.187.14.121',
    #                                                                                       'via': 'ge-0/0/1.0'}}},
    #                                                    'preference': '9',
    #                                                    'protocol_name': 'LDP'}},
    #                        'total_route_count': 5001}}}
    
    out = device.parse('show route table {table} {route}'.format(
        table=table,
        route=route
    ))
    

    output_interface = out.q.contains('.*{route}.*'.format(route=route), 
        regex=True).get_values('via', 0)
    
    if not output_interface:
        return None

    return output_interface


def get_route_table_output_label(device,
    table, route):
    """Get route table output label

    Args:
        device (obj): Device object
        table (str): Table name
        route (str): Route IP address
    
    Returns:
        output_label (str)
    """

    # Example Dictionary
    # {'table_name': {'inet.3': {'active_route_count': 5001,
    #                        'destination_count': 5001,
    #                        'hidden_route_count': 0,
    #                        'holddown_route_count': 0,
    #                        'routes': {'200.0.0.0/32': {'active_tag': '*',
    #                                                    'age': '00:01:29',
    #                                                    'metric': '1',
    #                                                    'next_hop': {'next_hop_list': {1: {'best_route': '>',
    #                                                                                       'mpls_label': 'Push '
    #                                                                                                     '574',
    #                                                                                       'to': '106.187.14.121',
    #                                                                                       'via': 'ge-0/0/1.0'}}},
    #                                                    'preference': '9',
    #                                                    'protocol_name': 'LDP'}},
    #                        'total_route_count': 5001}}}
    
    out = device.parse('show route table {table} {route}'.format(
        table=table,
        route=route
    ))
    

    output_label = out.q.contains('.*{route}.*'.format(route=route), 
        regex=True).get_values('mpls_label', 0)
    
    if not output_label:
        return None

    return output_label
