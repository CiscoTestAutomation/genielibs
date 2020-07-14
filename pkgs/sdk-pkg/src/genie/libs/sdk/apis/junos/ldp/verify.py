"""Common verification functions for LDP"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

# pyATS
from genie.utils import Dq

log = logging.getLogger(__name__)


def verify_ldp_session(
    device,
    address=None,
    expected_session_state=None,
    max_time=60,
    check_interval=10,
):
    """Verifies ldp session exists

    Args:
        device (obj): device object
        address (str): Neighbor address to check for
        expected_address (str): Expected address
        max_time (int): Maximum timeout time
        check_interval (int): Interval to check
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show ldp session")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        sessions = out.q.get_values('ldp-session')

        for session in sessions:
            if address:
                if session['ldp-neighbor-address'] != address:
                    continue

            if expected_session_state:
                if session['ldp-session-state'] != expected_session_state:
                    continue

            return True

        timeout.sleep()
    return False
