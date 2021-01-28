"""Common verification functions for BFD"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)


def verify_bfd_session(device, session_address, expected_session_state=None, 
expected_session_multiplier=None, max_time=60, check_interval=10, expected_interface=None):
    """ Verifiy the session state

    Args:
        device (obj): Device object
        session_address (str): Session address
        expected_session_state (str): Expected session state
        expected_session_multiplier (str): Expected session multiplier
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
        expected_interface (str, optional): Expected interface to check

    Returns:  
        Boolean

    Raises:
        N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show bfd session')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        sessions_ = out.q.get_values('bfd-session')

        for session in sessions_:
            if session.get('session-neighbor') == session_address:
                if expected_session_multiplier and \
                    session.get('session-adaptive-multiplier') != str(expected_session_multiplier):
                    continue
                if expected_session_state and \
                    session.get('session-state').lower() != expected_session_state.lower():
                    continue
                if expected_interface and session.get('session-interface') != expected_interface:
                    continue

                return True
        
        timeout.sleep()

    return False


def verify_bfd_session_detail(device, session_address, expected_session_state=None, expected_client=None, 
                              expected_session_multiplier=None, expected_tx_interval=None, expected_rx_interval=None,
                              expected_session_detect_time=None, expected_remote_state=None, max_time=60, 
                              check_interval=10):
    """ Verifiy the session state

    Args:
        device (obj): Device object
        session_address (str): Session address
        expected_session_state (str): Expected session state
        expected_client ('str'): Expected client
        expected_session_multiplier ('str'): Expected session multiplier
        expected_tx_interval ('str'): Expected tx interval
        expected_rx_interval ('str'): Expected rx interval
        expected_session_detect_time ('str'): Expected session detect time
        expected_remote_state ('str'): Expected remote session state
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show bfd session address {address} detail'.format(
                address=session_address))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        #"bfd-session": {
        #    "bfd-client": {
        #        "client-name": "LDP-OAM",
        #        "client-reception-interval": "0.050",
        #        "client-transmission-interval": "0.050",
        #    },
        #    "local-diagnostic": "None",
        #    "remote-diagnostic": "None",
        #    "remote-state": "Up",
        #    "session-adaptive-multiplier": "3",
        #    "session-detection-time": "1.500",
        #    "session-neighbor": "10.34.2.250",
        #    "session-state": "Up",
        #    "session-transmission-interval": "0.500",
        #    "session-up-time": "00:02:46",
        #    "session-version": "1",  

        session_state = out.q.get_values('session-state',0)
        if session_state:
            session_state = session_state.lower()
        
        remote_state = out.q.get_values('session-state',0)
        if remote_state:
            remote_state = remote_state.lower()

        client = out.q.get_values('client-name',0)
        if client:
            client = client.lower()
        
        session_detect_time = out.q.get_values('session-detection-time',0)

        multiplier = out.q.get_values('session-adaptive-multiplier',0)

        tx_interval = out.q.get_values('client-transmission-interval',0)

        rx_interval = out.q.get_values('client-transmission-interval',0)
        
        if expected_session_state and expected_session_state.lower() != session_state:
            timeout.sleep()
            continue

        if expected_client and expected_client.lower() != client:
            timeout.sleep()
            continue
        
        if expected_session_multiplier and multiplier and float(expected_session_multiplier) != float(multiplier):
            timeout.sleep()
            continue

        if expected_tx_interval and tx_interval and float(expected_tx_interval) != float(tx_interval):
            timeout.sleep()
            continue

        if expected_rx_interval and rx_interval and float(expected_rx_interval) != float(rx_interval):
            timeout.sleep()
            continue
        
        if expected_session_detect_time and session_detect_time and float(session_detect_time) != float(expected_session_detect_time):
            timeout.sleep()
            continue

        if expected_remote_state and remote_state and remote_state != expected_client.lower():
            timeout.sleep()
            continue
        
        return True

    return False


def verify_bfd_session_count(device, address, expected_session_count, expected_client_count=None, max_time=60, check_interval=10):
    """ Verify BFD session count
    Args:
        device (`obj`): Device object
        address (`str`): Session address
        expected_session_count (`int`): number of expected session count
        expected_client_count (`int`, optional): number of expected client count
                                                 Default to None
        max_time (`int`, optional): Maximum timeout time. Defaults to 60.
        check_interval (`int`, optional): Check interval. Defaults to 10.
    Returns:  
        Boolean
    Raises:
        N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show bfd session address {address} detail'.format(
                address=address))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # example of out
        # {
        #   "bfd-session-information": {
        #     "bfd-session": {
        #       (snip)
        #     },
        #     "clients": "1", # <-----
        #     "cumulative-reception-rate": "2.0",
        #     "cumulative-transmission-rate": "2.0",
        #     "sessions": "1" # <-----
        #   }
        # }

        sessions = int(out.q.get_values('sessions', 0))
        clients = int(out.q.get_values('clients', 0))

        if expected_client_count is not None:
            if sessions == expected_session_count and clients == expected_client_count:
                return True
        else:
            if sessions == expected_session_count:
                return True

        timeout.sleep()

    return False