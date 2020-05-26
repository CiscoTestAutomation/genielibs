"""Common verify functions for routing"""

# Python
import re
import logging
from prettytable import PrettyTable

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
    get_routing_repair_path_information,
)

log = logging.getLogger(__name__)


def verify_ip_cef_nexthop_label(
        device,
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
                out = device.parse(
                    'show route table {table} {ip}'.format(
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
                    hop_index_dict = out['table_name'][table_name]['routes'][route]
                    for index in hop_index_dict.get(
                            'next_hop',
                            {}).get(
                            'next_hop_list',
                            {}):
                        if '>' in hop_index_dict['next_hop']['next_hop_list'][index].get(
                                'best_route', ''):
                            found_label = hop_index_dict['next_hop']['next_hop_list'][index].get(
                                'mpls_label')
                            if expected_label and expected_label in found_label:
                                log.info(
                                    'Found the expected label "{}"'.format(found_label))
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
                                 known_via=None,
                                 tag=None,
                                 preference=None,
                                 protocol_name=None,
                                 extensive=False):
    """ Verify static route exists

        Args:
            device ('str'): Device str
            destination_address ('str'): destination ip address
            to ('str'): to value
            known_via ('str'): known via value
            tag ('str'): Tag value
            preference ('str'): Preference value
            protocol_name ('str'): Protocol name
            extensive ('bool'): if command with extensive at the end
        Returns:
            True / False
        Raises:
            None

    """
    try:
        if extensive:
            out = device.parse('show route protocol static extensive')
        else:
            out = device.parse('show route protocol static')
    except SchemaEmptyParserError:
        return False

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

    return False
