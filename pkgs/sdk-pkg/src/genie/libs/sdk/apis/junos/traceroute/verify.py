"""Common verification functions for traceroute"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# pyATS
from genie.utils import Dq

log = logging.getLogger(__name__)

def verify_traceroute_number_of_hops(device, expected_amount,
                          ip_address,
                          max_time=100,
                          check_interval=30):
    """ Verifies the number of hops is expected_amount via
        traceroute {ip_address} no-resolve

        Args:
            device ('obj'): device to use
            expected_amount ('int'): Expected number of hops in output
            ip_address ('str'): IP address passed in command
            max_time ('int', optional): Maximum time to keep checking. Default to 100
            check_interval ('int', optional): How often to check. Default to 30

        Returns:
            True/False

        Raises:
            N/A   
    """     
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            out = device.parse('traceroute {ip_address} no-resolve'.format(ip_address=ip_address))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # {'traceroute': {'hops': [{'address': '106.187.14.158',
        #                         'hop-number': '1',
        #                         'round-trip-time': '1.265 ms  0.946 ms  0.938 ms'},
        #                         {'address': '11.0.0.1',
        #                         'hop-number': '2',
        #                         'round-trip-time': '1.354 ms  1.554 ms  1.431 ms'}],
        #                 'max-hops': '30',
        #                 'packet-size': '52',
        #                 'to': {'address': '11.0.0.1', 'domain': '11.0.0.1'}}}  

        hops_amount = len(out.q.get_values("hops"))     

        if hops_amount == expected_amount:
            return True 

        timeout.sleep()

    return False 