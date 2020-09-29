"""Common verify functions for firewall"""

# Python
import re
import logging
import operator

# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def verify_firewall_filter(
    device: object, 
    expected_filter: str,
    max_time: int = 60,
    check_interval: int = 10,
    invert: bool = False,
    ) -> bool:
    """Verify firewall filter exists

    Args:
        device (object): Device object
        expected_filter (str): Filter to check for
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
        invert (bool, optional): Invert function. Defaults to False.

    Returns:
        bool: True/False
    """

    op = operator.contains
    if invert:
        op = lambda filters, ex_filter : operator.not_(operator.contains(filters, ex_filter))

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show firewall')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dict
        # "firewall-information": {
        #     "filter-information": [
        #         {
        #             "filter-name": str,

        filters_ = out.q.get_values('filter-name')
        if op(filters_, expected_filter):
            return True
        
        timeout.sleep()
    return False

def verify_firewall_packets(
    device: object, 
    expected_packet_count: int,
    filter: str,
    counter_name: str,
    max_time: int = 60,
    check_interval: int = 10,
    invert: bool = False,
    ) -> bool:
    """Verify firewall filter exists

    Args:
        device (object): Device object
        expected_packet_count (int): Expected packets to find
        filter (str): Filter to check
        counter_name (str): Counter name to check
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
        invert (bool, optional): Invert function. Defaults to False.

    Returns:
        bool: True/False
    """

    op = operator.eq
    if invert:
        op = operator.ne

    expected_packet_count = int(expected_packet_count)

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show firewall counter filter {filter} {counter_name}'.format(
                filter=filter,
                counter_name=counter_name,
            ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dict
        # "firewall-information": {
        #     "filter-information": [
        #         {
        #           Optional("counter"): {
        #               "packet-count": str

        packet_count_ = out.q.get_values('packet-count', 0)
        if packet_count_:
            packet_count_ = int(packet_count_)
        if op(expected_packet_count, packet_count_):
            return True
        
        timeout.sleep()
    return False


def verify_firewall_counter(device,
                            filters,
                            counter_name,
                            max_time=60,
                            check_interval=10):
    """ Verify counter is not 0

        Args:
            device (`obj`): Device object
            filters (`str`): Firewall filter argument
            counter_name (`str`): Firewall counter name argument
            max_time (`int`): Max time, defaults to 60 seconds
            check_interval (`int`): Check interval, defaults to 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show firewall counter filter {filters} {counter_name}'.format(
                filters=filters,
                counter_name=counter_name
            ))
        except Exception as e:
            log.info(e)
            timeout.sleep()
            continue

        #"firewall-information": {
        #    "filter-information": {
        #        "counter": {
        #            "byte-count": "1061737740",
        #            "counter-name": "v6_last_policer",
        #            "packet-count": "7860915"
        #        },
        #        "filter-name": "v6_local-access-control"
        #    }
        #}

        byte_count = out.q.get_values('byte-count',0)
        packet_count = out.q.get_values('packet-count',0)

        if byte_count and byte_count != 0 and packet_count and packet_count != 0:
            return True
        
    return False


def verify_firewall_log(device,
                        max_time=60,
                        check_interval=10
                        ):
    """ Verify show firewall log has output

        Args:
            device ('obj'): Device object
            max_time ('int', optional): Max time, default: 60 seconds
            check_interval ('int', optional): Check interval, default: 10 seconds

        Returns:
            result (`bool`): Verified result

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse('show firewall log')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        #"firewall-log-information": {
        #    "log-information": [
        #        {
        #            "action-name": "D",
        #            "destination-address": "40.0.0.1",
        #            "filter-name": "pfe",
        #            "interface-name": "ge-0/0/0.0",
        #            "protocol-name": "TCP",
        #            "source-address": "40.0.0.2",
        #            "time": "10:28:22"
        #        }
        #    ]
        #}

        log_list = output.q.get_values('log-information')

        if log_list:
            return True

        timeout.sleep()
    return False