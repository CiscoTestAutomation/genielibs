"""Common verify functions for syslog"""

import re
import logging

log = logging.getLogger(__name__)


def verify_syslog_interface_shut(interface, server, output):
    """ Verify log for interface shut message

        Args:
            interface ('str'): Interface to be verified
            output ('obj'): Tcpdump output
            server ('str'): Syslog server address
        Returns:
            True
            False
        Raises:
            None
    """

    # <133>2143: Jun  7 02:45:48.206 EST: %LINK-5-CHANGED: Interface GigabitEthernet5, changed state to administratively down
    r1 = re.compile(
        r".+\%LINK\-\d+\-CHANGED\:\s+Interface\s+(?P<interface>\S+)"
        "\,\s+changed\s+state\s+to\s+(administratively\s+down)"
    )
    for line in output:
        result = r1.match(line.load.decode())

        if line.dst == server and result:
            group = result.groupdict()

            if group["interface"] == interface:
                log.info(line.show(dump=True))
                return True
    else:
        log.error(
            "Interface shutdown information not received "
            "on server {srv} for interface {intf}".format(
                intf=interface, srv=server
            )
        )

    return False


def verify_syslog_interface_up(interface, server, output):
    """ Verify log for interface up message

        Args:
            interface ('str'): Interface to be verified
            output ('obj'): Tcpdump output
            server ('str'): Syslog server address
        Returns:
            True
            False
        Raises:
            None
    """

    # <133>2143: Jun  7 02:53:26.222 EST: %LINK-3-UPDOWN: Interface GigabitEthernet4, changed state to up
    r1 = re.compile(
        ".+\%LINK\-3\-UPDOWN\:\s+Interface\s+(?P<interface>\S+)\,\s"
        "+changed\s+state\s+to\s+(up)"
    )

    for line in output:
        result = r1.match(line.load.decode())

        if line.dst == server and result:
            group = result.groupdict()

            if group["interface"] == interface:
                log.info(line.show(dump=True))
                return True

    log.error(
        "Interface no shutdown information not received "
        "on server {srv} for interface {intf}".format(
            intf=interface, srv=server
        )
    )

    return False


def verify_syslog_ospf_neighbor_up(interface, server, output):
    """ Verify log for ospf neighbor up message

        Args:
            interface ('str'): Interface to be verified
            output ('obj'): Tcpdump output
            server ('str'): Syslog server address
        Returns:
            True
            False
        Raises:
            None

    """

    # <133>2143: Jun  7 02:49:10.999 EST: %OSPF-5-ADJCHG: Process 65109, Nbr 10.169.197.252 on GigabitEthernet2 from LOADING to FULL, Loading Done
    r1 = re.compile(
        r".+\%OSPF\-\d+\-ADJCHG\:\s+Process\s+\d+\,\s+Nbr\s+\S+\s+"
        "on\s+(?P<interface>\S+)\s+from\s+LOADING\s+to\s+FULL\,\s"
        "+Loading\s+Done"
    )

    for line in output:
        result = r1.match(line.load.decode())

        if line.dst == server and result:
            group = result.groupdict()

            if group["interface"] == interface:
                log.info(line.show(dump=True))
                return True
    log.error(
        "Interface no shutdown information not received "
        "on server {srv} for interface {intf}".format(
            intf=interface, srv=server
        )
    )

    return False


def verify_syslog_ospf_neighbor_down(interface, server, output):
    """ Verify log for ospf neighbor down message

        Args:
            interface ('str'): Interface to be verified
            output ('obj'): Tcpdump output
            server ('str'): Syslog server address
        Returns:
            True
            False
        Raises:
            None
    """

    # <133>2143: Jun  7 02:45:47.289 EST: %OSPF-5-ADJCHG: Process 65109, Nbr 10.169.197.252 on GigabitEthernet2 from FULL to DOWN, Neighbor Down: Interface down or detached
    r1 = re.compile(
        r".+\%OSPF\-\d+\-ADJCHG\:\s+Process\s+\d+\,\s+Nbr\s+\S+\s+"
        "on\s+(?P<interface>\S+)\s+from\s+FULL\s+to\s+DOWN\,\s+"
        "Neighbor\s+Down\:\s+Interface\s+down\s+or\s+detached"
    )

    for line in output:
        result = r1.match(line.load.decode())

        if line.dst == server and result:
            group = result.groupdict()

            if group["interface"] == interface:
                log.info(line.show(dump=True))
                return True
    log.error(
        "OSPF neighbor state information not received "
        "on server {srv} for interface {intf}".format(
            intf=interface, srv=server
        )
    )

    return False


def verify_syslog_bgp_peer_up(server, output):
    """ Verify log for bgp peer up message

        Args:
            output ('obj'): Tcpdump output
            server ('str'): Syslog server address
        Returns:
            True
            False
        Raises:
            None

    """

    # <133>2143: Jun  7 02:49:14.705 EST: %BGP-5-ADJCHANGE: neighbor 192.168.36.220 Up
    r1 = re.compile(r".+\%BGP\-\d+\-ADJCHANGE\:\s+neighbor\s+\S+\s+Up")

    for line in output:
        result = r1.match(line.load.decode())

        if line.dst == server and result:
            log.info(line.show(dump=True))
            return True
    else:
        log.error(
            "BGP peer state information not received "
            "on server {srv}".format(srv=server)
        )

    return False


def verify_syslog_bgp_peer_down(server, output):
    """ Verify log for bgp peer down message

        Args:
            output ('obj'): Tcpdump output
            server ('str'): Syslog server address
        Returns:
            True
            False
        Raises:
            None

    """

    # <133>2143: Jun  7 02:49:14.705 EST: %BGP-5-ADJCHANGE: neighbor 192.168.36.220 Down
    r1 = re.compile(r".+\%BGP\-\d+\-ADJCHANGE\:\s+neighbor\s+\S+\s+Down.*")

    for line in output:

        result = r1.match(line.load.decode())

        if line.dst == server and result:
            log.info(line.load.decode())
            return True
    log.error(
        "BGP peer state information not received "
        "on server {srv}".format(srv=server)
    )

    return False


def verify_syslog_interface_link_up(device, interface, server, output):
    """ Verify link up message in syslog server

        Args:
            device ('obj'): Device object
            interface ('str'): Interface to be verified
            output ('obj'): Tcpdump output
            server ('str'): Syslog server address
        Returns:
            True
            False
        Raises:
            None
    """

    # Jun  7 02:53:26.222 EST: %LINK-3-UPDOWN: Interface GigabitEthernet4, changed state to up
    r1 = re.compile(
        ".+\%LINK\-3\-UPDOWN\:\s+Interface\s+(?P<interface>\S+)\,\s"
        "+changed\s+state\s+to\s+up"
    )

    for line in output:

        result = r1.match(line.load.decode())

        if line.dst == server and result:

            group = result.groupdict()

            if group["interface"] == interface:
                log.info(line.show(dump=True))
                return True

    log.error(
        "Link state information not received "
        "on server {srv} for device {uut}".format(uut=device.name, srv=server)
    )

    return False


def verify_syslog_interface_link_down(device, interface, server, output):
    """ Verify link down message in syslog server

        Args:
            device ('obj'): Device object
            interface ('str'): Interface to be verified
            output ('obj'): Tcpdump output
            server ('str'): Syslog server address
        Returns:
            True
            False
        Raises:
            None

    """
    # Jun  7 02:53:26.222 EST: %LINK-3-UPDOWN: Interface GigabitEthernet4, changed state to down
    r1 = re.compile(
        ".+\%LINK\-3\-UPDOWN\:\s+Interface\s+(?P<interface>\S+)\,\s"
        "+changed\s+state\s+to\s+down"
    )

    for line in output:
        result = r1.match(line.load.decode())

        if line.dst == server and result:
            group = result.groupdict()

            if group["interface"] == interface:
                log.info(line.show(dump=True))
                return True
    log.error(
        "Link state information not received "
        "on server {srv} for device {uut}".format(uut=device.name, srv=server)
    )

    return False


def is_syslog_message_received(message, server, output):
    """ Verify if a message was received in Syslog server.
        It needs a output from a tcpdump command

        Args:                        
            device ('obj'): Device object
            output ('obj'): Tcpdump output
            server ('str'): Syslog server address
            message ('str'): Message to be verified in Syslog server
        Returns:
            True
            False
        Raises:
            None
    """

    for packet in output:
        try:
            if packet.dst == server and message in packet.load.decode():
                log.info(packet.show(dump=True))
                log.info(
                    "Message '{message}' has been found in Syslog "
                    "server {ip}".format(message=message, ip=server)
                )
                return True

        # Some packets raise UnicodeDecodeError
        # It will continue to next packet
        except UnicodeDecodeError:
            continue

    log.info(
        "Message '{message}' has not been found in Syslog "
        "server {ip}".format(message=message, ip=server)
    )

    return False
