"""Common verification functions for BFD"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)


def get_bfd_session_state_count(device, expected_session_state='Up', max_time=60, check_interval=10):
    """ Get bfd session state count

    Args:
        device (obj): Device object
        expected_session_state (str): Expected session state. Defaults to 'Up'.
        max_time (int, optional): Maximum timeout time. Defaults to 60 seconds.
        check_interval (int, optional): Check interval. Defaults to 10 seconds.
    """
    try:
        out = device.parse('show bfd session')
    except SchemaEmptyParserError:
        return None

    session_count = out.q.contains_key_value('session-state', 
        expected_session_state).count()
    return session_count