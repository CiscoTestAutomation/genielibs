""" Common verification functions for logging """

# Python
import re
import logging
from datetime import datetime

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logging
from genie.libs.sdk.apis.iosxe.logging.get import get_logging_logs

log = logging.getLogger(__name__)


def is_logging_string_matching_regex_logged(device, oldest_timestamp, regex):
    """ Verifies string that matches regex is logged - ignoring logs from before passed timestamp

        Args:
           device ('obj'): device to use
           oldest_timestamp ('str'): oldest timestamp to match (format: hh:mm:ss.sss)
           regex ('str'): regex string to match

        Returns:
            timestamp of command if found else False ('str') 
        Raises:
            None
    """
    logs = get_logging_logs(device=device)

    p1 = re.compile(regex)
    FMT = "%b %d %H:%M:%S.%f"
    FMT1 = "%b %d %H:%M:%S"

    for line in reversed(logs):
        line = line.strip()

        m = p1.match(line)
        if m:
            timestamp = m.groupdict()["timestamp"]
            if '.' in timestamp:
                t1 = datetime.strptime(timestamp, FMT)
            else:
                t1 = datetime.strptime(timestamp, FMT1)

            if '.' in oldest_timestamp:
                t2 = datetime.strptime(oldest_timestamp, FMT)
            else:
                t2 = datetime.strptime(oldest_timestamp, FMT1)

            tdelta = t1 - t2
            if tdelta.days < 0:
                return False
            else:
                return timestamp

    return False


def is_logging_bfd_down_logged(*args, **kwargs):
    """ Verifies bfd is logged down within specified time from issued command

        Args:
           device ('obj'): device to use
           oldest_timestamp ('str'): oldest timestamp to match (format: hh:mm:ss.sss)

        Returns:
            ('str') timestamp of command if found else False
        Raises:
            None
    """
    log.info("Checking logs for BFD_SESS_DOWN: ECHO FAILURE")

    # Jan 24 18:13:10.814 EST: %BFDFSM-6-BFD_SESS_DOWN: BFD-SYSLOG: BFD session ld:2039 handle:2,is going Down Reason: ECHO FAILURE
    # *Jan 24 18:13:10.814 EST: %BFDFSM-6-BFD_SESS_DOWN: BFD-SYSLOG: BFD session ld:2039 handle:2,is going Down Reason: ECHO FAILURE
    return is_logging_string_matching_regex_logged(
        regex=r"^\*?(?P<timestamp>\w+ +\d+ +\S+) +\w+: +%BFDFSM-6-BFD_SESS_DOWN.*ECHO FAILURE$",
        *args,
        **kwargs
    )


def is_logging_ospf_neighbor_down_logged(*args, **kwargs):
    """ Verifies ospf neighbor is logged down within specified time from issued command

        Args:
           device ('obj'): device to use
           oldest_timestamp ('str'): oldest timestamp to match (format: hh:mm:ss.sss)

        Returns:
            ('str') timestamp of command if found else False
        Raises:
            None
    """
    log.info("Checking logs for OSPF-5-ADJCHG: Neighbor Down: BFD node down")

    # Jan 24 18:13:10.814 EST: %OSPF-5-ADJCHG: Process 1111, Nbr 10.24.24.24 on GigabitEthernet1 from FULL to DOWN, Neighbor Down: BFD node down
    # *Jan 24 18:13:10.814 EST: %OSPF-5-ADJCHG: Process 1111, Nbr 10.24.24.24 on GigabitEthernet1 from FULL to DOWN, Neighbor Down: BFD node down
    # Jan 24 18:13:10.814: %OSPF-5-ADJCHG: Process 1111, Nbr 10.24.24.24 on GigabitEthernet1 from FULL to DOWN, Neighbor Down: BFD node down
    return is_logging_string_matching_regex_logged(
        regex=r"^\*?(?P<timestamp>\w+ +\d+ +\S+)( +\w+)?: +%OSPF-5-ADJCHG.*FULL +to +DOWN, +Neighbor +Down: +BFD +node +down$",
        *args,
        **kwargs
    )


def is_logging_static_route_down_logged(*args, **kwargs):
    """ Verifies static route is logged down within specified time from issued command

        Args:
           device ('obj'): device to use
           oldest_timestamp ('str'): oldest timestamp to match (format: hh:mm:ss.sss)

        Returns:
            ('str') timestamp of command if found else False
        Raises:
            None
    """
    log.info("Checking logs for IP-ST: not active state")

    # Jan 24 18:13:10.814 EST: IP-ST(default):  10.4.1.1/32 [1], GigabitEthernet2 Path = 4 6, no change, not active state
    # *Jan 24 18:13:10.814 EST: IP-ST(default):  10.4.1.1/32 [1], GigabitEthernet3 Path = 4 6, no change, not active state
    # Oct 24 09:48:52.617: IP-ST(default):  10.4.1.1/32 [1], GigabitEthernet0/2/1 Path = 1 8, no change, not active state
    return is_logging_string_matching_regex_logged(
        regex=r"^\*?(?P<timestamp>\w+ +\d+ +\S+)( +\w+)?: +IP-ST.*not +active +state$",
        *args,
        **kwargs
    )
