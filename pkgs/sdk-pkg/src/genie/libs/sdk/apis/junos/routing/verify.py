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


def verify_ip_cef_nexthop_label(device, ip, table=None, expected_label=None, vrf=None,
                                max_time=30, check_interval=10):
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
                out = device.parse('show route table {table} {ip}'.format(table=table, ip=ip))
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
                    for index in hop_index_dict.get('next_hop', {}).get('next_hop_list', {}):
                        if '>' in hop_index_dict['next_hop']['next_hop_list'][index].get('best_route', ''):
                            found_label = hop_index_dict['next_hop']['next_hop_list'][index].get('mpls_label')
                            if expected_label and expected_label in found_label:
                                log.info('Found the expected label "{}"'.format(found_label))
                                return True
                            elif not expected_label and not found_label:
                                log.info('No label found. No label is expected')
                                return True

        timeout.sleep()
    return False
