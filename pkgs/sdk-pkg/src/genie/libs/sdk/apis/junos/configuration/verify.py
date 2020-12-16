"""Common verification functions for configuration"""

# Python
import re
import logging
import operator

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)

def verify_configuration_hostname(device, expected_hostname, max_time=60, check_interval=10):
    """ Verifies slot state via show configuration system host-name

    Args:
        device (obj): Device object
        expected_hostname (str): Expected hostname
        max_time (int, optional): Maximum timeout time. Defaults to 60 seconds.
        check_interval (int, optional): Check interval. Defaults to 10 seconds.

    Returns:
        True/False
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.execute('show configuration system host-name')
        except Exception as e:
            timeout.sleep()
            continue

        # Example output
        # ' \r\nhost-name name_000;'
        p = re.compile(r'host-name +(?P<hostname>\S+);')

        m = p.match(out.strip())
        if m and m.groupdict()['hostname']==expected_hostname:
            return True 

        timeout.sleep()
        
    return False



def verify_configuration_ddos_protection_no_output(device, max_time=60, check_interval=10):
    """ Verifies there is no otuput via show configuration system ddos-protection

    Args:
        device (obj): Device object
        max_time (int, optional): Maximum timeout time. Defaults to 60 seconds.
        check_interval (int, optional): Check interval. Defaults to 10 seconds.

    Returns:
        True/False
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.execute('show configuration system ddos-protection')
        except Exception as e:
            timeout.sleep()
            continue
        
        if out == '' or '{master}':
            return True
        timeout.sleep()

    return False
