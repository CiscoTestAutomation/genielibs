"""Common verification functions for ipv6"""

# Python
import logging
import operator

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)


def verify_ipv6_neighbor_state(device, expected_interface, expected_state, max_time=60, check_interval=10):
    """Verify interface exists with expected state

    Args:
        device (obj): Device object
        expected_interface (str): Interface to check for
        expected_state (str): Expected interface state
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show ipv6 neighbor')
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue

        # "ipv6-nd-information": {
        #   "ipv6-nd-entry": [
        #     {
        #         "ipv6-nd-state": str

        for entry in out.q.get_values("ipv6-nd-entry"):
            if expected_interface.lower() == entry.get("ipv6-nd-neighbor-address").lower():
                if expected_state.lower() == entry.get("ipv6-nd-state").lower():
                    return True

        timeout.sleep()

    return False
