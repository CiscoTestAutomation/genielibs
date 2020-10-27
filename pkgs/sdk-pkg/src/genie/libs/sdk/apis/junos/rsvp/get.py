"""Common get functions for rsvp"""

# Python
import re
import time
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def get_rsvp_hello_sent(
        device,
        ipv4_address,
        sent_count_flag=False
    ):
    """ Verify lsp state is up for neighbor
    
        Args:
            device ('obj'): device to use
            ipv4_address ('str'): IPv4 address to check neighbor node
            sent_count_flag ('bool'): Flag for getting Hello: sent value
        
        Returns:
            sent_count: Value obtained from the Hello: send value
        
        Raises:
            N/A
    """
    # Parse IPv4 address
    ipv4_address = ipv4_address.split("/")[0]

    try:
        output = device.parse("show rsvp neighbor detail")
    except SchemaEmptyParserError:
        log.info('Parser is empty')
        return None
        
    # Example RSVP Neighbor Detail Dictionary   
    # {
    #     "rsvp-neighbor-information": {
    #         "rsvp-neighbor-count": str,
    #         "rsvp-neighbor": [
    #             {
    #                 "rsvp-neighbor-address": str,
    #                 "hellos-sent": str,
    #                 "last-changed-time": str,
    #                       ...
    #             }
    #         ]
    #     }
    # }
    
    # Get RSVP neighbor list 
    for neighbor in output.q.get_values("rsvp-neighbor"):                
       
        # Match the desired neighbor with the give ipv4 address
        if neighbor.get("rsvp-neighbor-address") == ipv4_address:
            
            # Case when user wants to check Hello: sent value
            if sent_count_flag and neighbor.get("hellos-sent") and \
                neighbor.get("last-changed-time"):
                
                # Convert last_changed_time string ("2:20") to seconds
                if ':' in neighbor.get("last-changed-time"):
                    minutes, seconds = neighbor.get("last-changed-time").split(":")
                    return { 
                        "hello_sent": neighbor.get("hellos-sent"),
                        "last_changed_time": int(minutes) * 60 + int(seconds)
                    }
                else:
                    seconds = neighbor.get("last-changed-time")
                    return { 
                        "hello_sent": neighbor.get("hellos-sent"),
                        "last_changed_time": int(seconds)
                    }
            break    
    return None

def get_rsvp_session_state_count(device, expected_lsp_state='Up', max_time=60, check_interval=10):
    """ Get show ldp session count

    Args:
        device (obj): Device object
        expected_lsp_state (str): Expected session state. Defaults to 'Up'.
        max_time (int, optional): Maximum timeout time. Defaults to 60 seconds.
        check_interval (int, optional): Check interval. Defaults to 10 seconds.
    """
    try:
        out = device.parse('show rsvp session transit')
    except SchemaEmptyParserError:
        return None

    state_count = out.q.contains_key_value('lsp-state', 
        expected_lsp_state).count()

    return state_count
