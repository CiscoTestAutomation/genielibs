"""Common get info functions for acl"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def get_acl_hit_counts(device,
                       name,
                       source_network='',
                       destination_network='',
                       output='',
                       parsed_output=''):
    """ Get ACL(access-list) hit counts

        Args:
            device(`obj`): Device object
            name(`str`): Access-list name
            source_network(`str`): source network
            destination_network(`str`): destination network
            output(`str`): output of show access-lists
            parsed_output(`str`): parsed_output from show access-lists
        Returns:
            List:
            [[str, int]]

            Example:
            [['acl1', 100]]
        Raises:
            None
    """

    ret_list = []

    if not source_network and not destination_network:
        return ret_list

    if parsed_output:
        out = parsed_output
    else:
        if output:
            try:
                out = device.parse("show access-lists {name}".format(name=name),
                               output=output)
            except SchemaEmptyParserError:
                return ret_list
        else:
            try:
                out = device.parse("show access-lists {name}".format(name=name))
            except SchemaEmptyParserError:
                return ret_list
        if not out:
            return ret_list

    src_aces = Dq(out).contains_key_value('source_network',
                                          source_network).get_values('aces')
    dest_aces = Dq(out).contains_key_value(
        'destination_network', destination_network).get_values('aces')

    if source_network and destination_network:
        aces = set(src_aces) & set(dest_aces)
    elif source_network and not destination_network:
        aces = src_aces
    else:
        aces = dest_aces

    for ace in aces:
        hit_count = Dq(out).contains_key_value(
            'aces', ace).get_values('matched_packets')
        if hit_count:
            ret_list.append([ace, hit_count[0]])

    return ret_list
