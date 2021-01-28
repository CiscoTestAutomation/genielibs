"""Common verification functions for PPM"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)


def verify_ppm_transmissions(device, destination, expected_distributed_values=None, max_time=60, check_interval=10, expected_interface=None):
    """ Verifiy the session state

    Args:
        device (obj): Device object
        destination (str): route address
        expected_distributed_values (list): list of boolean values describing transmission distributed
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
        expected_interface (str, optional): Expected interface to check
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show ppm transmissions protocol bfd detail')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        #{'transmission-data': 
        #    [{'protocol': 'BFD',
        #     'transmission-destination': '27.85.194.102',
        #     'transmission-distributed': 'TRUE',
        #     'transmission-interface-index': '783',
        #     'transmission-interval': '300',
        #     'transmission-pfe-addr': 'fpc9',
        #     'transmission-pfe-handle': '6918'
        #     }]
        #}

        transmission_data = out.q.get_values('transmission-data')
        for item in transmission_data:
            if item.get('transmission-destination') == destination:
                if item.get('transmission-distributed').lower() in expected_distributed_values:
                    return True
        timeout.sleep()

    return False