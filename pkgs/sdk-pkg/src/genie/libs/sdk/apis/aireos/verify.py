"""
    Utility type functions that do not fit into another category
"""

# Python
import re
import time
import logging
import subprocess

# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout

# unicon
from ats.log.utils import banner
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def verify_ping(device, ip_addr, max_time=30, check_interval=10):
    """ Verify ping

    Args:
        device ('obj'): Device object
        ip_addr ('str'): An ip address
        max_time ('int'): Max time to execute; default is 30
        check_interval ('int'): An interval to check again; default is 10
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('ping {}'.format(ip_addr))
        except SubCommandFailure as e:
            timeout.sleep()
            continue

        rate = Dq(out).contains('statistics').get_values('received')
        
        if rate:
            if rate[0] > 0:
                return True
            else:
                timeout.sleep()
                continue
    
    return False

