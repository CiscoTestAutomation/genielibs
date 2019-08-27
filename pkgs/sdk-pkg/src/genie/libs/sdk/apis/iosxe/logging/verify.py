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

    for line in reversed(logs):
        line = line.strip()

        m = p1.match(line)
        if m:
            tdelta = datetime.strptime(
                m.groupdict()["timestamp"], FMT
            ) - datetime.strptime(oldest_timestamp, FMT)
            if tdelta.days < 0:
                return False
            else:
                return m.groupdict()["timestamp"]

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
        regex="^\*?(?P<timestamp>\w+ +\d+ +\S+) +\w+: +%BFDFSM-6-BFD_SESS_DOWN.*ECHO FAILURE$",
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

    # Jan 24 18:13:10.814 EST: %OSPF-5-ADJCHG: Process 1111, Nbr 524.524.524.524 on GigabitEthernet1 from FULL to DOWN, Neighbor Down: BFD node down
    # *Jan 24 18:13:10.814 EST: %OSPF-5-ADJCHG: Process 1111, Nbr 524.524.524.524 on GigabitEthernet1 from FULL to DOWN, Neighbor Down: BFD node down
    return is_logging_string_matching_regex_logged(
        regex="^\*?(?P<timestamp>\w+ +\d+ +\S+) +\w+: +%OSPF-5-ADJCHG.*FULL +to +DOWN, +Neighbor +Down: +BFD +node +down$",
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
    return is_logging_string_matching_regex_logged(
        regex="^\*?(?P<timestamp>\w+ +\d+ +\S+) +\w+: +IP-ST.*not +active +state$",
        *args,
        **kwargs
    )
