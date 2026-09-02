""" Common verification functions for logging """

# Python
import re
import logging
from datetime import datetime
from genie.utils.timeout import Timeout

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


def _check_logging(device, log_list, check_count=False, expect_exist=True):
    """Check whether expected log message(s) exist in device `show logging`.

        Args:
            device (`obj`): Device object
            log_list (`str` or `list`): Expected log message(s) in
                "show logging". All top-level logs in the list are checked.
                If any of them is not found, return False. A nested list is
                treated as an OR condition, for example:
                log_list = [['log1', 'log2'], 'log3'] means check log1 OR
                log2 AND log3.
            check_count (`bool`, optional): Whether to check the log count in
                "show logging". Defaults to False.
            expect_exist (`bool`, optional): Whether the log is expected to
                exist. Defaults to True.

        Returns:
            list: [True, message] if check passes, [False, message] otherwise
    """
    logging_list = device.api.get_platform_logging(command='show logging')
    if not isinstance(logging_list, list):
        raise TypeError(f'Get logging failed, '
                        f'expect list but got {type(logging_list)}')
    logging = '\r\n'.join(logging_list)
    if isinstance(log_list, str):
        log_list = [log_list]
    for log_group in log_list:
        if isinstance(log_group, str):
            if expect_exist is True and check_count is True:
                if logging.count(log_group) != 1:
                    msg = 'Check logging failed: Expect only one of ' + \
                            f'"{log_group}" in "show logging"'
                    return [False, msg]
            elif expect_exist is True and check_count is False:
                if logging.count(log_group) < 1:
                    msg = 'Check logging failed: Expect ' + \
                            f'"{log_group}" in "show logging"'
                    return [False, msg]
            else:    # expect_exist is False
                if logging.count(log_group) > 0:
                    msg = 'Check logging failed: Expect ' + \
                            f'"{log_group}" not in "show logging"'
                    return [False, msg]
        elif isinstance(log_group, list):
            if expect_exist is True:
                if check_count is True:
                    count = 0
                    for or_log in log_group:
                        if or_log in logging:
                            count = count + logging.count(or_log)
                    if count != 1:
                        msg = 'Check logging failed: Expect only one of ' + \
                                f'"{log_group}" in "show logging"'
                        return [False, msg]
                else:
                    or_group_matched = False
                    for or_log in log_group:
                        if or_log in logging:
                            or_group_matched = True
                            break
                    if not or_group_matched:
                        msg = 'Check logging failed: Expect at least one' + \
                            f' of "{log_group}" in "show logging"'
                        return [False, msg]
            else:    # expect_exist is False
                for or_log in log_group:
                    if or_log in logging:
                        msg = 'Check logging failed: Expect none of ' + \
                                f'"{log_group}" in "show logging"'
                        return [False, msg]
        else:
            return [False, f'Unknown {log_group} type {type(log_group)}']
    return [True, 'Check logging passed']


def verify_logging(device, log_list, max_time=20, interval_time=2,
                   check_count=False, clear_log=True, expect_exist=True):
    '''
    Verify logging with Aetest step
    Args:
        device (`obj`): Device object
        log_list (`str` or `list`): Expected log message(s) in "show logging".
            All top-level logs in the list are checked. If any of them is not
            found, return False. A nested list is treated as an OR condition,
            for example: log_list = [['log1', 'log2'], 'log3'] means check
            log1 OR log2 AND log3.
        max_time (`int`, optional): Polling max time in seconds. Defaults to 20.
        interval_time (`int`, optional): Polling interval in seconds.
            Defaults to 2.
        check_count (`bool`, optional): Whether to check the log count in
            "show logging". Defaults to False.
        clear_log (`bool`, optional): Whether to clear logging after
            verification. Defaults to True.
        expect_exist (`bool`, optional): Whether the log is expected to exist.
            Defaults to True.
    Returns:
        bool: True if check passes, False otherwise
    '''
    timeout1 = Timeout(max_time, interval_time)
    while timeout1.iterate():
        res, msg = _check_logging(device, log_list, check_count, expect_exist)
        if expect_exist is True:
            if res is True:
                break
            else:
                log.debug(msg)
                timeout1.sleep()
        else:
            if res is True:
                timeout1.sleep()
            else:
                log.debug(msg)
                return False
    else:
        if expect_exist is True:
            log.debug(msg)
            return False
    if clear_log is True:
        device.api.clear_logging()
    return True
