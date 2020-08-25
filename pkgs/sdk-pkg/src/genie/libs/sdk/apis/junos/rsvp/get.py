"""Common get functions for rsvp"""

# Python
import re
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
            if sent_count_flag and neighbor.get("hellos-sent"):
                return neighbor.get("hellos-sent")
            break
    
    return None