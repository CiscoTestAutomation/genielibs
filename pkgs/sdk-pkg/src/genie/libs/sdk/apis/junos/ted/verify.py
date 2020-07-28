"""Common verification functions for ted"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# pyATS
from genie.utils import Dq

log = logging.getLogger(__name__)


def verify_ted_interface(device,
                         interface,
                         expected_interface,
                         max_time=100,
                         check_interval=10):
    """ Verifies ted interface exists

        Args:
            device ('obj'): device to use
            interface ('str'): Interface to use in show command
            expected_interface ('str'): expected interface
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show ted database {interface}'.format(interface=interface))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
            
        #{
        #"ted-link-local-address": "106.187.14.158",
        #"ted-link-local-ifindex": "333",
        #"ted-link-protocol": "OSPF(0.0.0.8)",
        #"ted-link-remote-address": "106.187.14.157",
        #"ted-link-remote-ifindex": "0",
        #"ted-link-to": "106.187.14.240"
        #}
        for address in Dq(out).get_values('ted-link-local-address'):

            if address != expected_interface:
                continue
            return True

        timeout.sleep()

    return False