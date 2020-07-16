"""Common get info functions for OSPF"""

# Python
import re
import copy
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq
# Pyats
from pyats.utils.objects import find, R

log = logging.getLogger(__name__)

def get_class_of_service_shaping_rate(device, interface):
    """ Get shapping rate based on interface name

        Args:
            device ('obj'): Device object
            interface('str'): Interface to get shaping rate
            
        Returns:
            shaping_rate: Staping rate value

        Raises:
            None
    """
    
    try:
        out = device.parse('show class-of-service interface {interface}'.format(
            interface=interface))
    except SchemaEmptyParserError:
        return None

    # Dict

    shaping_rate = out.q.contains('{interface}|interface-shaping-rate'.format(
        interface=interface
    ), regex=True).get_values('interface-shaping-rate', 0)
    
    if not shaping_rate:
        return None
    return shaping_rate