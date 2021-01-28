"""Common verification functions for OSPF3"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)


def get_ospf3_neighbors_instance_state_count(device, expected_neighbor_state='Full', max_time=60, check_interval=10):
    """ Get ospf3 neighbors instance state count

    Args:
        device (obj): Device object
        expected_neighbor_state (str): Expected neighbor state. Defaults to 'Full'.
        max_time (int, optional): Maximum timeout time. Defaults to 60 seconds.
        check_interval (int, optional): Check interval. Defaults to 10 seconds.
    """
    try:
        out = device.parse('show ospf3 neighbor instance all')
    except SchemaEmptyParserError:
        return None

    state_count = out.q.contains_key_value('ospf-neighbor-state', 
        expected_neighbor_state).count()

    return state_count

def get_ospf3_neighbor_count(device, expected_state=None, output=None, max_time=60, check_interval=10):
    """ Get ospf3 neighbors count

    Args:
        device (`obj`): Device object
        expected_state (`str`): Expected neighbor state. Defaults to None
        output (`str`): output of show ospf neighbor. Default to None
        max_time (`int`, optional): Maximum timeout time. Defaults to 60 seconds.
        check_interval (`int`, optional): Check interval. Defaults to 10 seconds.
    """
    try:
        if output:
            out = device.parse('show ospf3 neighbor', output=output)
        else:
            out = device.parse('show ospf3 neighbor')
    except SchemaEmptyParserError:
        return 0

    # example out out
    # {
    #   "ospf3-neighbor-information": {
    #     "ospf3-neighbor": [
    #       {
    #         "activity-timer": "30",
    #         "interface-name": "ge-0/0/0.0",
    #         "neighbor-address": "fe80::250:56ff:fe8d:c305",
    #         "neighbor-id": "2.2.2.2",
    #         "neighbor-priority": "128",
    #         "ospf-neighbor-state": "Full"
    #       },

    if expected_state:
        return len(out.q.contains_key_value('ospf-neighbor-state', expected_state))
    else:
        return len(out.q.get_values('ospf3-neighbor'))