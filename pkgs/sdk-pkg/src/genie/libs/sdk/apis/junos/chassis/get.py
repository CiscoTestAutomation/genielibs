"""Common get info functions for chassis"""

# Python
import re
import copy
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def get_chassis_memory_util(device):
    """Returns chassis memory utilization

    Args:
        device (obj): Device object

    Returns:
        str: Memory utilization percentage
    """

    # Example dict
    # "route-engine-information": {
    #     "route-engine": {
    #         "memory-buffer-utilization": str
    #     }
    # }

    try:
        out = device.parse('show chassis routing-engine')
    except SchemaEmptyParserError:
        return None

    return out.q.get_values("memory-buffer-utilization", 0)

def get_chassis_cpu_util(device, cpu_idle_section = 'cpu-idle-5sec'):
    """Returns chassis cpu utilization

    Args:
        device (obj): Device object
        cpu_idle_section (str): cpu utilization, defaults to cpu-idle-5sec

    Returns:
        str: CPU utilization percentage
    """

    # Example dict
    # "route-engine-information": {
    #     "route-engine": {
    #         "cpu-idle-5sec": str
    #     }
    # }

    try:
        out = device.parse('show chassis routing-engine')
    except SchemaEmptyParserError:
        return None

    return out.q.get_values(cpu_idle_section, 0)
