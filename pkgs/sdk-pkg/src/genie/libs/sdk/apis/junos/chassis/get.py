"""Common get info functions for chassis"""

# Python
import re
import copy
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def get_chassis_memory_util(device, expected_slot=None):
    """Returns chassis memory utilization

    Args:
        device (obj): Device object
        expected_slot (int): Expected slot number

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

    if expected_slot:
        route_engine = out.q.contains('slot', level=-1).get_values('route-engine')

        for route in route_engine:
            if route.get('slot') != expected_slot:
                continue
            return route.get('memory-buffer-utilization', None)
    
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

def get_chassis_cpu_util_alternative(device, cpu_idle_section = 'cpu-idle', expected_state='Master', 
    expected_slot=None):
    """Returns chassis cpu utilization. When show chassis routing-engine
       has the alternative output

    Args:
        device (obj): Device object
        cpu_idle_section ('str', optional): cpu utilization, defaults to cpu-idle
        expected_state ('str'): cpu state, defaults to Master
        expected_slot (int, optional): Expected slot number. default to None. 

    Returns:
        str: CPU utilization percentage
    """

    # Example dict
    #"route-engine": [
    #            {
    #                "cpu-background": "0",
    #                "cpu-idle": "82",
    #                "cpu-interrupt": "4",
    #                "cpu-system": "11",
    #                "cpu-user": "3",
    #                "last-reboot-reason": "Router rebooted after a normal shutdown.",
    #                "load-average-fifteen": "0.23",
    #                "load-average-five": "0.26",
    #                "load-average-one": "0.22",
    #                "mastership-priority": "Master (default)",

    try:
        out = device.parse('show chassis routing-engine')
    except SchemaEmptyParserError:
        return None
    
    if expected_slot:
        route_engine = out.q.contains('slot', level=-1).get_values('route-engine')
    else:
        route_engine = out.q.get_values('route-engine')

    for route in route_engine:
        if expected_slot:
            if route.get('slot') != expected_slot:
                continue
        if route.get('mastership-state') == expected_state:
            return route.get(cpu_idle_section)
    return None

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

def get_chassis_zone_actual_usage(device,
                       expected_zone):
    """ Get capacity actual usage of a zone

        Args:
            device (`obj`): Device object
            expected_zone (`str`): Expected zone
        Returns:
            result (`list`): list of states of routing engines
        Raises:
            N/A
    """
    routing_engine_states = []
    try:
        output = device.parse('show chassis power')
    except SchemaEmptyParserError:
        return routing_engine_states

    actual_usage = output.q.contains('power-usage-zone-information').contains(
        expected_zone, level=-1).get_values('capacity-actual-usage', 0)
    return actual_usage or None

def get_chassis_fpc_slot_numbers(device, expected_state=None):
    """Returns slot numbers
    Args:
        device (obj): Device object
        expected_state (str): Expected state. Default to None.
    Returns:
        list: List of slot numbers 
    """

    # Example dict
    # "route-engine-information": {
    #     "route-engine": {
    #         "memory-buffer-utilization": str
    #     }
    # }

    try:
        out = device.parse('show chassis fpc')
    except SchemaEmptyParserError:
        return None

    if expected_state:
        return out.q.contains(expected_state, level=-1).get_values('slot') or None
    return out.q.get_values('slot') or None

def get_chassis_fpc_cpu_util(device, cpu_total = 'cpu-total', expected_slot='0', all_slots=False):
    """Returns chassis fpc cpu utilization

    Args:
        device (obj): Device object
        cpu_total ('str', optional): cpu utilization, defaults to cpu-total
        expected_state ('str'): cpu state, defaults to Master
        Returns:
        str: CPU utilization percentage
    """

    # Example dict
    #"fpc": [
    #        {
    #            "cpu-15min-avg": "2",
    #            "cpu-1min-avg": "2",
    #            "cpu-5min-avg": "2",
    #            "cpu-interrupt": "0",
    #            "cpu-total": "3",
    #            "memory-buffer-utilization": "0",
    #            "memory-dram-size": "511",
    #            "memory-heap-utilization": "31",
    #            "slot": "0",
    #            "state": "Online",
    #            "temperature": {"#text": "Testing"},
    #        },

    try:
        out = device.parse('show chassis fpc')
    except SchemaEmptyParserError:
        return None

    if all_slots:
        return(out.q.get_values(cpu_total))

    if expected_slot is not None:
        slot_dict = out.q.get_values('fpc', int(expected_slot))
        slot_ = slot_dict.get('slot')
        if slot_ == str(expected_slot):
            cpu_total_val = slot_dict.get(cpu_total, None)
            return int(cpu_total_val) if cpu_total_val else None

    return None


def get_chassis_slot_idle_value(device, slot='0'):
    """Returns chassis cpu utilization for specific slot.

    Args:
        device (obj): Device object
        cpu_idle_section ('str', optional): cpu utilization, defaults to cpu-idle
        slot ('str'): cpu slot, defaults to 0

    Returns:
        str: CPU utilization percentage
    """

    # Example dict
    #"route-engine": [
    #            {
    #                "cpu-background": "0",
    #                "cpu-idle": "82",
    #                "cpu-interrupt": "4",
    #                "cpu-system": "11",
    #                "cpu-user": "3",
    #                "last-reboot-reason": "Router rebooted after a normal shutdown.",
    #                "load-average-fifteen": "0.23",
    #                "load-average-five": "0.26",
    #                "load-average-one": "0.22",
    #                "mastership-priority": "Master (default)",

    try:
        out = device.parse('show chassis routing-engine')
    except SchemaEmptyParserError:
        return None

    route_engine = out.q.get_values('route-engine')

    for route in route_engine:
        if route.get('slot') == slot:
            return route.get('cpu-idle')

    return None
