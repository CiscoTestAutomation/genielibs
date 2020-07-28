"""Common verification functions for ping"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# pyATS
from genie.utils import Dq

log = logging.getLogger(__name__)


def verify_ping_loss_rate(device,
                    expected_loss_rate,
                    address,
                    ttl,
                    count,
                    wait,
                    max_time=100,
                    check_interval=10):
    """ Verifies loss rate via ping {address} ttl {ttl} count {count} wait {wait}

        Args:
            device ('obj'): device to use
            expected_loss_rate ('int'): Expected loss rate
            address ('str'): IP address passed in command
            ttl ('int'): ttl value passed in command
            count ('int'): count value passed in command
            wait ('int'): wait value passed in command
            max_time ('int', optional): Maximum time to keep checking. Default to 100
            check_interval ('int', optional): How often to check. Default to 10

        Returns:
            True/False

        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('ping {address} ttl {ttl} count {count} wait {wait}'.format(
                address=address,
                ttl=ttl,
                count=count,
                wait=wait))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        # {'ping': {'address': '11.0.0.1',
        #         'data-bytes': 56,
        #         'source': '11.0.0.1',
        #         'statistics': {'loss-rate': 100, 'received': 0, 'send': 5}}}
        if out.q.get_values("loss-rate", 0)==expected_loss_rate:
            return True

        timeout.sleep()

    return False