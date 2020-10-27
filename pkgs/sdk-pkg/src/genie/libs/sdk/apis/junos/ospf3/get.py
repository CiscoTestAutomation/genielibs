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