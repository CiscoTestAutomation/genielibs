"""Common verification functions for ARP"""

# Python
import logging
import operator

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)


def verify_arp_interface_exists(device, expected_interface, invert=False, max_time=60, check_interval=10):
    """Verify interface exists in arp table

    Args:
        device (obj): Device object
        expected_interface (str): Interface to check for
        invert (bool, optional): Inverts to ensure interface doesn't exist. Defaults to False.
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
    """

    op = operator.truth
    if invert:
        op = lambda val: operator.not_(operator.truth(val))

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show arp')
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue

        # "arp-table-information": {
        #     "arp-entry-count": str,
        #     "arp-table-entry": [
        #         {
        #             "interface-name": str,

        if op(expected_interface in out.q.get_values('interface-name')):
            return True

        timeout.sleep()

    return False
