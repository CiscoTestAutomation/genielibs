"""Common verify functions for rsvp"""
#pyATS
from genie.utils import Dq

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError


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