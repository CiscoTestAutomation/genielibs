""" Common get functions for segment-routing """

# Python
import re
import logging

# pyATS
from pyats.utils.objects import find, R

# Genie
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Running-Config
from genie.libs.sdk.apis.iosxe.running_config.get import (
    get_running_config_section_dict,
)

log = logging.getLogger(__name__)


def get_segment_routing_policy_active_path_hop_labels(device, policy,
        policy_dict=None, ignore_first_label=False):
    """ Find a segement-routing policy in expected state

        Args:
            device ('obj'): Device object
            policy ('str'): Policy name
            policy_dict ('dict'): Policy dict from parser output
                IOSXE Parser - ShowSegmentRoutingTrafficEngPolicy
                cmd - show segment-routing traffic-eng policy all
            ignore_first_label (`bool`): flag to ignore first label
        Returns:
            labels ('list'): Hop labels
    """
    labels = []
    cmd = 'show segment-routing traffic-eng policy name {policy}'.format(policy=policy)
    if policy_dict is None:
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
            return labels
    else:
        out = policy_dict

    # Check explicit path
    reqs = R(['(.*{}.*)'.format(policy),'candidate_paths',
              'preference','(?P<preference>.*)',
              'path_type','explicit',
              '(?P<category>.*)','(?P<name>.*)',
              'status','(?P<status>.*)'])
    explicit = find([out], reqs, filter_=False, all_keys=True)
    if explicit:
        keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={},
                                    source=explicit, all_keys=True)
    
        for item in keys:
            if item['status'] == 'active':
                path_index = item['preference']

                reqs2 = R(['(.*{}.*)'.format(policy),'candidate_paths',
                          'preference',path_index,
                          'path_type','explicit',
                          '(?P<category>.*)','(?P<name>.*)',
                          'hops','(?P<hops>.*)'])
                hops = find([out], reqs2, filter_=False, all_keys=True)
                if hops:
                    hop = hops[0][0]
                    for value in hop.values():
                        sid = value.get('sid', '')
                        labels.append(str(sid))

                    if ignore_first_label and len(labels):
                        labels.pop(0)
                    return labels

    # Check dynamic path if no active path in explicit path
    reqs = R(['(.*{}.*)'.format(policy),'candidate_paths',
              'preference','(?P<preference>.*)',
              'path_type','dynamic',
              'status','(?P<status>.*)'])
    dynamic = find([out], reqs, filter_=False, all_keys=True)
    if dynamic:
        keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={},
                                    source=dynamic, all_keys=True)

        for item in keys:
            if item['status'] == 'active':
                path_index = item['preference']

                reqs2 = R(['(.*{}.*)'.format(policy),'candidate_paths',
                          'preference',path_index,
                          'path_type','dynamic',
                          'hops','(?P<hops>.*)'])
                hops = find([out], reqs2, filter_=False, all_keys=True)
                if hops:
                    hop = hops[0][0]
                    for value in hop.values():
                        sid = value.get('sid', '')
                        labels.append(str(sid))

    if ignore_first_label and len(labels):
        labels.pop(0)
    return labels


def get_segment_routing_policy_in_state(device, expected_admin='up', expected_oper='up',\
        expected_color='', expected_endpoint=''):
    """ Find a segement-routing policy in expected state

        Args:
            device ('obj'): Device object
            expected_admin ('str'): Expected admin state
            expected_oper ('str'): Expected operational state
            expected_color (`str`): Expected color
            expected_endpoint (`str`): Expected end-point address
        Returns:
            policy ('str'): Policy name
    """
    cmd = 'show segment-routing traffic-eng policy all'
    try:
        out = device.parse(cmd)
    except Exception as e:
        log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
        return None

    for policy in out.keys():
        admin = out.get(policy, {}).get('status', {}).get('admin', '')
        oper = out.get(policy, {}).get('status', {}).\
                   get('operational', {}).get('state', '')
        color = str(out.get(policy, {}).get('color', ''))
        endpoint = out.get(policy, {}).get('end_point', '')

        if (admin.lower() == expected_admin.lower() and 
            oper.lower() == expected_oper.lower() and 
            color == expected_color and 
            endpoint == expected_endpoint):
            return policy
    else:
        log.info("Failed to find a policy with admin state {admin} "
                 "and oper state {oper}".format(admin=expected_admin,
                    oper=expected_oper))
        return None


def get_segment_routing_sid_map_configuration(device, address_family="ipv4"):
    """ Get Segment routing SID map configuration

        Args:
            device ('str'): Device str
            address_family ('str'): Address family
        Returns:
            Dictionary with ip address as key and sid as value
            ex.)
                {
                    '192.168.1.1': '1',
                    '192.168.1.2': '2'
                }
    """
    out = get_running_config_section_dict(
        device=device, section="segment-routing"
    )

    sid_dict = {}

    if not out:
        return None

    p1 = re.compile(r"^(?P<ip_address>\S+) index (?P<sid>\d+) range \d+$")

    connected_prefix_sid_maps = out["segment-routing mpls"][
        "connected-prefix-sid-map"
    ]["address-family {}".format(address_family)].keys()

    for key in connected_prefix_sid_maps:
        key = key.strip()
        m = p1.match(key)
        if m:
            group = m.groupdict()
            sid_dict.update({group["ip_address"]: group["sid"]})
            continue

    return sid_dict


def get_segment_routing_lb_range(device):
    """ Gets segement-routing local block range

        Args:
            device ('obj'): device to use

        Returns:
            ('int', 'int'): label_min, label_max

        Raises:
            N/A
    """
    try:
        out = device.parse("show segment-routing mpls lb")
    except SchemaEmptyParserError:
        return None, None

    return out.get("label_min"), out.get("label_max")


def get_segment_routing_gb_range(device):
    """ Gets segement-routing global block range

        Args:
            device ('obj'): device to use

        Returns:
            ('int', 'int'): label_min, label_max

        Raises:
            None
    """
    try:
        out = device.parse("show segment-routing mpls gb")
    except SchemaEmptyParserError:
        return None, None

    return out.get("label_min"), out.get("label_max")

def get_segment_routing_accumulated_path_metric(device, preference, policy_name=None):
    """ Get accumulated path metric for a preference path

        Args:
            device ('obj'): Device to use
            policy_name ('str'): Policy name to verify. If not specified will verify all
            preference ('int'): Preference path

        Returns:
            accumulated_metric (None, 'int'): Accumulated path metric

        Raises:
            N/A
    """
    if policy_name:
        cmd = 'show segment-routing traffic-eng policy name {policy}'.format(policy=policy_name)
    else:
        cmd = 'show segment-routing traffic-eng policy all'
    
    try:
        out = device.parse(cmd)
    except SchemaEmptyParserError:
        return None
    
    for policy in out:
        for preference_found in out[policy].get('candidate_paths', {}).get('preference', {}):
            if preference != preference_found:
                continue
            if out[policy]['candidate_paths']['preference'][preference].get('path_type'):
                path_type_dict = out[policy]['candidate_paths']['preference'][preference]['path_type']
                if 'dynamic' in path_type_dict:
                    accumulated_metric = path_type_dict['dynamic'].get('path_accumulated_metric', '')
                    return accumulated_metric
    return None

def get_segment_routing_labels_from_bgp(device, route, vrf, best_path=False):
    """ Gets segement-routing labels from bgp table

        Args:
            device (`obj`): device to use
            route (`str`): route to check
            vrf (`vrf`): VRF name
            best_path (`bool`): only best path returned

        Returns:
            ('list'): list of segment routing labels

        Raises:
            N/A
    """

    # search destination's endpoint and color by 
    #               show ip bgp vpnv4 vrf <vrf> <destination address>

    endpoint_color_list = device.api.get_ip_bgp_route_nexthop_color(
        address_family='vpnv4', route=route, vrf=vrf, best_path=True)
    
    # get policy names based on endpoint and color
    policy_list = []
    label_list = []
    if endpoint_color_list:
        log.info('Found endpoint and color: {}'.format(
            endpoint_color_list))
        for endpoint, color in endpoint_color_list:
            policy = device.api.get_segment_routing_policy_in_state(
                expected_admin='up', expected_oper='up',
                expected_color=color, expected_endpoint=endpoint)
            # don't have redundant policy
            if policy not in policy_list:
                policy_list.append(policy)
    if policy_list:
        log.info('Policy Found: {}'.format(policy_list))
        for policy in policy_list:
            label_list = device.api.\
                get_segment_routing_policy_active_path_hop_labels(
                    policy=policy, ignore_first_label=True)

    return label_list
