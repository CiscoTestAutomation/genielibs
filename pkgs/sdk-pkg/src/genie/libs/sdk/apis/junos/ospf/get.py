"""Common get info functions for OSPF"""

# Python
import logging
import datetime
import re

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


def get_ospf_interface_and_area(device):
    """ Retrieve interface for ospf on junos device

        Args:
            device ('obj'): Device object

        Returns:
            interface and area value dictionary
    """
    try:
        out = device.parse("show ospf interface brief")
    except SchemaEmptyParserError as spe:
        raise SchemaEmptyParserError(
            "Could not parse output for"
            " command 'show ospf interface brief'") from spe

    key_val = {}

    try:
        interface_dict = out["instance"]["master"]["areas"]
        for k, v in interface_dict.items():
            for interface in v["interfaces"].keys():
                key_val.update({interface: k})
    except KeyError as ke:
        raise KeyError("Key issue with exception: {}".format(str(ke))) from ke
    return key_val

def get_ospf_spf_scheduled_time(log):
    """
    Get OSPF spf scheduled time in log 'Jun 12 03:32:19.068983 OSPF SPF scheduled for topology default in 8s' 

    Args:
        log ('str'): log string

    Returns:
        date time ('str')  
    """  
    # Jun 12 03:32:19.068983 OSPF SPF scheduled for topology default in 8s
    p_scheduled = ('(?P<date>\S+\s+\d+) (?P<scheduled_time>\d+\:\d+\:\d+\.\d+) '\
        'OSPF SPF scheduled for topology default in (?P<spf_change>\d+)s')    
    m = re.match(p_scheduled, log)

    try:
        if m:
            group = m.groupdict()
            scheduled_time = group['scheduled_time']
            return scheduled_time
    except KeyError as e:
        raise KeyError(f"Key issue with exception: {str(e)}") from e
    
    

def get_ospf_spf_start_time(log):
    """
    Get OSPF spf start time in log 'Jun 12 03:40:19.068983 Starting full SPF for topology default' 

    Args:
        log ('str'): log string

    Returns:
        date time ('str')  
    """
    # Jun 12 03:40:19.068983 Starting full SPF for topology default
    p_start = (
        '(?P<date>\S+\s+\d+) (?P<start_time>\d+\:\d+\:\d+\.\d+) Starting full SPF for topology default'
    )     
    m = re.match(p_start, log)
    
    try:
        if m:
            group = m.groupdict()
            start_time = group['start_time']
            return start_time
    except KeyError as e:
        raise KeyError(f"Key issue with exception: {str(e)}") from e
    
    return None

def get_ospf_database_checksum(device, lsa_type=None):
    """ Get ospf data base checksum data in a list

    Args:
        device (obj): Device object
        lsa_type (str, optional): LSA type to check for. Defaults to None.

    Returns:
        list: List of checksums
    """

    try:
        out = device.parse('show ospf database')
    except SchemaEmptyParserError:
        return list()
    
    ret_list = []

    # Example dict
    # {
    #     'ospf-database-information': {
    #         'ospf-database': [{
    #             'lsa-type': 'Router',
    #             'checksum': '0xa9b6',
    #         }]
    #     }
    # }

    for entry_ in out.q.get_values('ospf-database'):
        if lsa_type and entry_.get('lsa-type') != lsa_type:
            continue

        if entry_.get('checksum'):
            ret_list.append(entry_.get('checksum'))

    return ret_list

def get_ospf_router_id(device):
    """ Retrieve ospf router id

    Args:
        device (obj): Device object
    """
    try:
        output = device.parse('show ospf overview')
    except SchemaEmptyParserError:
            return None
    
    try:
        return output.q.get_values('ospf-router-id', 0)
    except Exception as e:
        log.info("Error retrieving router ID: {e}".format(e=e))    
    return None
    
def get_ospf_neighbors_instance_state_count(device, expected_neighbor_state='Full', max_time=60, check_interval=10):
    """ Get ospf neighbors instance state count

    Args:
        device (obj): Device object
        expected_neighbor_state (str): Expected neighbor state. Defaults to 'Full'. 
        max_time (int, optional): Maximum timeout time. Defaults to 60 seconds.
        check_interval (int, optional): Check interval. Defaults to 10 seconds.
    """
    try:
        out = device.parse('show ospf neighbor instance all')
    except SchemaEmptyParserError:
        return None

    state_count = out.q.contains_key_value('ospf-neighbor-state', 
        expected_neighbor_state).count()

    return state_count

def get_ospf_neighbor_count(device, expected_state=None, output=None, max_time=60, check_interval=10):
    """ Get ospf neighbors count

    Args:
        device (`obj`): Device object
        expected_state (`str`): Expected neighbor state. Defaults to None
        output (`str`): output of show ospf neighbor. Default to None
        max_time (`int`, optional): Maximum timeout time. Defaults to 60 seconds.
        check_interval (`int`, optional): Check interval. Defaults to 10 seconds.
    """
    try:
        if output:
            out = device.parse('show ospf neighbor', output=output)
        else:
            out = device.parse('show ospf neighbor')
    except SchemaEmptyParserError:
        return 0

    # example out out
    # {
    #   "ospf-neighbor-information": {
    #     "ospf-neighbor": [
    #       {
    #         "activity-timer": "32",
    #         "interface-name": "ge-0/0/0.0",
    #         "neighbor-address": "12.0.0.2",
    #         "neighbor-id": "2.2.2.2",
    #         "neighbor-priority": "128",
    #         "ospf-neighbor-state": "Full"
    #       },

    if expected_state:
        return len(out.q.contains_key_value('ospf-neighbor-state', expected_state))
    else:
        return len(out.q.get_values('ospf-neighbor'))

