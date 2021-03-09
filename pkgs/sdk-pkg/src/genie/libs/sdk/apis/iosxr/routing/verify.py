"""Common verification functions for bfd"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError


def verify_route_known_via(device, route, address_family, known_via, max_time=90, check_interval=10):
    """ Verify route known via

        Args:
            device ('obj'): Device object
            route ('str'): Route address
            known_via ('str'): Known via value
            max_time ('int'): Max time in seconds checking output
            check_interval ('int'): Interval in seconds of each checking 
        Return:
            True/False
        Raises:
            None
    """
    
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            out = device.parse('show route {} {}'.format(
                address_family, route))
        except Exception:
            timeout.sleep()
            continue
        
        know_via_ = out.q.get_values('known_via')
        if known_via in know_via_:
            return True
        timeout.sleep()
    return False