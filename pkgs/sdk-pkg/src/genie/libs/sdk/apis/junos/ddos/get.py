"""Common verify functions for ddos"""

# Python
import re
import logging
import operator

# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def get_ddos_protection_arrival_rate(device, protocol, expected_protocol_states_local):
    """ Get arrival rate for expected-protocol-states-local

    Args:
        device (object): Device object
        protocol (str): Protocol value 
        expected_protocol_states_local (str): Expected protocol states local

    Returns:
        bool: True/False
    """
    
    try:
        out = device.parse('show ddos-protection protocols {protocol}'.format(
            protocol=protocol
        ))
    except SchemaEmptyParserError:
        return None
    
    arrival_rate = out.q.contains(expected_protocol_states_local, 
        level=-1).get_values('packet-arrival-rate', 0)
    return arrival_rate or None