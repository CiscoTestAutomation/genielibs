# Python
import re
import logging

import time
from time import strptime
from datetime import datetime

log = logging.getLogger(__name__)


def get_syslog_maximum_ospf_down_time(device, logs, server):
    """ Get maximum OSPF down time from show logging
        Args:
            device ('obj'): Device object
            logs ('str'): Output from Syslog server
            server ('str'): Syslog server address
        Returns:
            Integer: OSPF down time in seconds
            None
        Raises:
            None
    """

    # Get first ospf OSPF message in show logging
    ospf_down_message = get_syslog_first_ospf_down_message(
        device=device, logs=logs, server=server
    )
    if ospf_down_message is None:
        return None
    # Extract time stamp from message
    ospf_down_time = get_syslog_message_time(message=ospf_down_message)

    # Get first ospf UP message in show logging
    ospf_up_message = get_syslog_last_ospf_up_message(
        device=device, logs=logs, server=server
    )
    if ospf_up_message is None:
        return None

    # Extract time stamp from message
    ospf_up_time = get_syslog_message_time(message=ospf_up_message)

    return abs((ospf_down_time - ospf_up_time).total_seconds())


def get_syslog_message_time(
    message,
    regex=r".+\s+(?P<month>\S+) +(?P<day>\d+) "
    r"+(?P<hour>\d+)\:(?P<minute>\d+)\:"
    r"(?P<second>\d+)\.(?P<millisecond>"
    r"\d+).+",
):
    """ Get message time
        Args:
            message ('str'): Line from show logging command
            regex ('str'): Regex to extract time from line
        Returns:
            datetime: Time extracted from message
            None
        Raises:
            None
    """

    r1 = re.compile(regex)
    result = r1.match(message)

    if result:
        group = result.groupdict()
        hour = int(group["hour"])
        minute = int(group["minute"])
        second = int(group["second"])
        milliseconds = int(group["millisecond"])
        month = strptime(group["month"], "%b").tm_mon
        day = int(group["day"])
        year = int(group.get("year", datetime.now().year))

        return datetime(year, month, day, hour, minute, second, milliseconds)

    return None


def get_syslog_last_ospf_down_message(device, server, logs, interface=""):
    """ Get last OSPF down message from Syslog server

        Args:
            device ('obj'): Device object
            logs ('str'): Output from tcpdump
            server ('str'): Syslog server address
            interface ('str'): Interface name if searching for specific interface
        Returns:
            String: Line containing message
            None
        Raises:
            None
    """

    return get_syslog_first_ospf_down_message(
        device=device,
        logs=logs,
        server=server,
        interface=interface,
        reverse=True,
    )


def get_syslog_first_ospf_down_message(
    device, logs, server, interface="", reverse=False
):
    """ Get first OSPF down message from Syslog server

        Args:
            device ('obj'): Device object
            logs ('str'): Output from tcpdump
            server ('str'): Syslog server address
            interface ('str'): Interface name if searching for specific interface
        Returns:
            String: Line containing message
            None
        Raises:
            None
    """

    if reverse:
        logs = reversed(logs)

    # <133>837: Jun 7 02:45:47.289 EST: %OSPF-5-ADJCHG: Process 65109, Nbr 10.169.197.252 on GigabitEthernet2 from FULL to DOWN, Neighbor Down: Interface down or detached
    r1 = re.compile(
        r".+\%OSPF\-\d+\-ADJCHG\:\s+Process\s+\d+\,\s+Nbr\s+\S+\s+"
        r"on\s+(?P<interface>\S+)+\s+from\s+FULL\s+to\s+DOWN\,\s+Neighbor\s+Down.*"
    )

    for packet in logs:
        result = r1.match(packet.load.decode())

        if packet.dst == server and result:
            group = result.groupdict()

            if group["interface"] == interface and interface:
                log.info(packet.show(dump=True))
                return result.string

            elif not interface:
                log.info(packet.show(dump=True))
                return result.string

    return None


def get_syslog_last_bgp_down_message(device, logs, server):
    """ Get last BGP down message in show logging

        Args:
            device ('obj'): Device object
            logs ('str'): Output from tcpdump
            server ('str'): Syslog server address
        Returns:
            String: Line containing message
            None
        Raises:
            None
    """

    return get_syslog_first_bgp_down_message(
        device=device, logs=logs, server=server, reverse=True
    )


def get_syslog_first_bgp_down_message(device, server, logs, reverse=False):
    """ Get first BGP down message in show logging

        Args:
            device ('obj'): Device object
            logs ('str'): Output from tcpdump
            server ('str'): Syslog server address
        Returns:
            String: Line containing message
            None
    """
    if reverse:
        logs = reversed(logs)

    # <133>837: Jun  7 02:49:14.705 EST: %BGP-5-ADJCHANGE: neighbor 192.168.36.220 Down
    r1 = re.compile(r".+\%BGP\-\d+\-ADJCHANGE\:\s+neighbor\s+\S+\s+Down.*")

    for packet in logs:
        result = r1.match(packet.load.decode())

        if packet.dst == server and result:
            log.info(packet.show(dump=True))
            return result.string

    return None


def get_syslog_last_ospf_up_message(device, logs, server, interface=""):
    """ Get last OSPF up message in show logging

        Args:
            device ('obj'): Device object
            logs ('str'): Output from tcpdump
            server ('str'): Syslog server address
            interface ('str'): Interface name if searching for specific interface
        Returns:
            String: Line containing message
            None
    """

    return get_syslog_first_ospf_up_message(
        device=device,
        logs=logs,
        server=server,
        interface=interface,
        reverse=True,
    )


def get_syslog_first_ospf_up_message(
    device, logs, server, interface="", reverse=False
):
    """ Get first OSPF up message in show logging

        Args:
            device ('obj'): Device object
            logs ('str'): Output from tcpdump
            server ('str'): Syslog server address
            interface ('str'): Interface name if searching for specific interface
        Returns:
            String: Line containing message
            None
    """

    if reverse:
        logs = reversed(logs)

    # <133>837: Jul 13 05:45:23.872 EST: %OSPF-5-ADJCHG: Process 65109, Nbr 10.169.197.252 on GigabitEthernet2 from LOADING to FULL, Loading Done
    r1 = re.compile(
        r".+\%OSPF\-\d+\-ADJCHG\:\s+Process\s+\d+\,\s+Nbr\s+\S+\s+"
        r"on\s+(?P<interface>\S+)\s+from\s+LOADING\s+to\s+FULL.+"
    )

    for packet in logs:
        result = r1.match(packet.load.decode())

        if packet.dst == server and result:
            group = result.groupdict()

            if group["interface"] == interface and interface:
                log.info(packet.show(dump=True))
                return result.string

            elif not interface:
                log.info(packet.show(dump=True))
                return result.string
    return None


def get_syslog_last_bgp_up_message(device, server, logs=""):
    """ Get last BGP up message in show logging

        Args:
            device ('obj'): Device object
            logs ('str'): Output from tcpdump
            server ('str'): Syslog server address
        Returns:
            String: Line containing message
            None
    """

    return get_syslog_first_bgp_up_message(
        device=device, server=server, logs=logs, reverse=True
    )


def get_syslog_first_bgp_up_message(device, logs, server, reverse=False):
    """ Get first BGP up message in show logging

        Args:
            device ('obj'): Device object
            logs ('str'): Output from tcpdump
            server ('str'): Syslog server address
        Returns:
            String: Line containing message
            None
    """

    if reverse:
        logs = reversed(logs)

    # <133> 837: Jun  7 02:49:14.705 EST: %BGP-5-ADJCHANGE: neighbor 192.168.36.220 Up
    r1 = re.compile(r".+\%BGP\-\d+\-ADJCHANGE\:\s+neighbor\s+\S+\s+Up")

    for packet in logs:
        result = r1.match(packet.load.decode())

        if packet.dst == server and result:
            log.info(packet.show(dump=True))
            return result.string

    return None


def get_syslog_maximum_bgp_down_time(device, logs, server):
    """ Get maximum BGP down time from show logging
        Args:
            device ('obj'): Device object
            logs ('str'): Output from show logging
        Returns:
            BGP down time in seconds
        Raises:
            ValueError
    """

    # Get first BGP down message in show logging
    bgp_down_message = get_syslog_first_bgp_down_message(
        device=device, logs=logs, server=server
    )
    if bgp_down_message is None:
        return None
    # Extract time stamp from message
    bgp_down_time = get_syslog_message_time(message=bgp_down_message)

    # Get first BGP UP message in show logging
    bgp_up_message = get_syslog_last_bgp_up_message(
        device=device, logs=logs, server=server
    )
    if bgp_up_message is None:
        return None

    # Extract time stamp from message
    bgp_up_time = get_syslog_message_time(message=bgp_up_message)

    return abs((bgp_down_time - bgp_up_time).total_seconds())
