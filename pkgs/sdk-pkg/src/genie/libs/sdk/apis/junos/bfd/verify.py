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