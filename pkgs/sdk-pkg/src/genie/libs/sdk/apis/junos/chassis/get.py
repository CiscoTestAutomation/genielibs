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

def get_routing_engines_states(device,
                       max_time=30,
                       check_interval=10,):
    """ Get state of routing engines

        Args:
            device (`obj`): Device object
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`list`): list of states of routing engines
        Raises:
            N/A
    """
    routing_engine_states = []
    try:
        output = device.parse('show chassis routing-engine')
    except SchemaEmptyParserError:
        return routing_engine_states

    # Sample output
    # "route-engine-information": {
    #             "route-engine": [{
    #                   "mastership-state": "Master",
    #                    ...
    #              },
    #              {
    #                   "mastership-state": "Backup",
    #              }]

    route_engines = output.q.get_values('route-engine')
    route_engine_states = [route_engine['mastership-state']
                           for route_engine in route_engines if route_engine.get('mastership-state', None)]

    return route_engine_states
