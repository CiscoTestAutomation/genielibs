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


def get_segment_routing_policy_active_path_hop_labels(device, policy, policy_dict=None):
    """ Find a segement-routing policy in expected state

        Args:
            device ('obj'): Device object
            policy ('str'): Policy name
            policy_dict ('dict'): Policy dict from parser output
                IOSXE Parser - ShowSegmentRoutingTrafficEngPolicy
                cmd - show segment-routing traffic-eng policy all
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
    reqs = R([policy,'candidate_paths',
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

                reqs2 = R([policy,'candidate_paths',
                          'preference',path_index,
                          'path_type','explicit',
                          '(?P<category>.*)','(?P<name>.*)',
                          'hops','(?P<hops>.*)'])
                hops = find([out], reqs2, filter_=False, all_keys=True)
                if hops:
                    hop = hops[0][0]
                    for value in hop.values():
                        sid = value.get('sid', '')
                        labels.append(sid)

                    return labels

    # Check dynamic path if no active path in explicit path
    reqs = R([policy,'candidate_paths',
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

                reqs2 = R([policy,'candidate_paths',
                          'preference',path_index,
                          'path_type','dynamic',
                          'hops','(?P<hops>.*)'])
                hops = find([out], reqs2, filter_=False, all_keys=True)
                if hops:
                    hop = hops[0][0]
                    for value in hop.values():
                        sid = value.get('sid', '')
                        labels.append(sid)

    return labels


def get_segment_routing_policy_in_state(device, expected_admin='up', expected_oper='up'):
    """ Find a segement-routing policy in expected state

        Args:
            device ('obj'): Device object
            expected_admin ('str'): Expected admin state
            expected_oper ('str'): Expected operational state
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

        if (admin.lower() == expected_admin.lower() and 
            oper.lower() == expected_oper.lower()):
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

