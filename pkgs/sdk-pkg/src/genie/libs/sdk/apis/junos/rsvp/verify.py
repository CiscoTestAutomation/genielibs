"""Common verify functions for rsvp"""

# Python
import re
import logging

# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_lsp_neighbor(
        device,
        ipv4_address,
        expected_status="Up",
        max_time=60,
        check_interval=10,
        lsp_state_flag=False
    ):
    """ Verify lsp state is up for neighbor
    
        Args:
            device ('obj'): device to use
            ipv4_address ('str'): IPv4 address to check neighbor node
            expected_status ('str'): Expected neighbor lsp status
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check
            lsp_state_flag ('bool'): Flag for verifying Lsp state
        
        Returns:
            True/False
        
        Raises:
            N/A
    """
    # Parse IPv4 address
    ipv4_address = ipv4_address.split("/")[0]
    
    timeout = Timeout(max_time, check_interval)
    
    while timeout.iterate():
        try:
            output = device.parse("show rsvp neighbor detail")
        except SchemaEmptyParserError:
            log.info('Parser is empty')
            timeout.sleep()
            continue
    
        # Example RSVP Neighbor Detail Dictionary   
        # {
        #     "rsvp-neighbor-information": {
        #         "rsvp-neighbor-count": str,
        #         "rsvp-neighbor": [
        #             {
        #                 "rsvp-neighbor-address": str,
        #                 "rsvp-neighbor-status": str,
        #                           ...
        #             }
        #         ]
        #     }
       	# }
            
        # Get RSVP neighbor list 
        for neighbor in output.q.get_values("rsvp-neighbor"):    
            if neighbor.get("rsvp-neighbor-address") == ipv4_address:                 
                
                # Case when user wants to check the Lsp status of neighbor
                if (lsp_state_flag and 
                    neighbor.get("rsvp-neighbor-status") == expected_status):
                    return True
                break       
            
        timeout.sleep()
    return False

def verify_rsvp_neighbor(device, expected_ipaddress, max_time=30, check_interval=10):
    """
    Verify there is a neighbor

    Args:
        device (`obj`): Device object
        expected_ipaddress (`str`): The IP address that is expected in the output 
        max_time (`int`): Max time, default: 30
        check_interval (`int`): Check interval, default: 10
    Returns:
        result (`bool`): Verified result 
    """       

    # {'rsvp-neighbor-information': 
    #       {   'rsvp-neighbor-count': '4',
    #           'rsvp-neighbor': [
    #                   {'rsvp-neighbor-address': '59.128.3.252',
    #                    'neighbor-idle': '39:15',
    #                    'neighbor-up-count': '0',
    #                    'neighbor-down-count': '0',
    #                    'last-changed-time': '39:15',
    #                    'hello-interval': '9',
    #                    'hellos-sent': '262',
    #                    'hellos-received': '0',
    #                    'messages-received': '0'},

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show rsvp neighbor")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        if expected_ipaddress in out.q.get_values("rsvp-neighbor-address"):
            return True 
        
        timeout.sleep()
    return False


def verify_rsvp_session_state(device, expected_state, session_name=None,
                              session_type="Transit", max_time=60, check_interval=10):
    """ Verify RSVP session state

    Args:
        device (obj): device object
        expected_state (str): Expected state
        session_name (str, optional): Session name. Defaults to None.
        session_type (str): Session type. Defaults to "Transit"
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
    """

        #'rsvp-session-information': {
            # 'rsvp-session-data': [{
            # 'session-type': 'Transit',
            # 'count': '30',
            # 'rsvp-session': [{
            #     'destination-address': '10.49.194.125',
            #     'source-address': '10.49.194.127',
            #     'lsp-state': 'Up',
            #     'route-count': '0',
            #     'rsb-count': '1',
            #     'resv-style': 'FF',
            #     'label-in': '46',
            #     'label-out': '44',
            #     'name': 'test_lsp_01'
            # }, 

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show rsvp session')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        for session in out.q.get_values('rsvp-session-data'):
            if session.get('session-type') == session_type:
                session_data = Dq(session).get_values('rsvp-session')
                for data in session_data:
                    if session_name and session_name != data.get('name'):
                        continue

                    if data.get('lsp-state').lower() != expected_state.lower():
                        continue

                    return True
        timeout.sleep()    
    return False    

def verify_rsvp_session_state(device, expected_state, session_name=None,
                              session_type="Transit", max_time=60, check_interval=10):
    """ Verify RSVP session state

    Args:
        device (obj): device object
        expected_state (str): Expected state
        session_name (str, optional): Session name. Defaults to None.
        session_type (str): Which session to look into. Defaults to "Transit"
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show rsvp session')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dictionary
        # {
        #     "rsvp-session-information": {
        #         "rsvp-session-data": [{
        #             "session-type": str,
        #             "rsvp-session": [{
        #                 "lsp-state": str,
        #                 "name": str,
        #             }],
        #         }]
        #     }
        # }

        for session in out.q.get_values('rsvp-session-data'):
            if session.get('session-type') == session_type:
                session_data = Dq(session).get_values('rsvp-session')
                for data in session_data:
                    if session_name != data.get('name'):
                        continue

                    if data.get('lsp-state').lower() != expected_state.lower():
                        continue

                    return True
        timeout.sleep()    
    return False