"""Common verify functions for arp"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


def verify_static_arp(
    device, ip_address, mac_address, max_time=15, check_interval=5
):
    """ Verify static arp entry is present in ARP table

        Args:
            device (`obj`): Device object
            ip_address (`str`): IP address
            mac_address (`str`): MAC address
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
        Returns:
            True
            False
    """
    log.info(
        'Verifying ARP table contains static entry with "IP '
        'Address:{}" and "MAC Address:{}"'.format(ip_address, mac_address)
    )

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            out = device.parse("show arp")
        except SchemaEmptyParserError:
            pass
        if out:
            static_table = out.get("global_static_table")
            if static_table and static_table.get(ip_address, None):
                if (
                    static_table[ip_address].get("mac_address", None)
                    == mac_address
                ):
                    return True
        timeout.sleep()
    return False


def verify_arp_packets(pkts, timeout, tolerance):
    """ Verify arp packets sent interval

        Args:
            pkts (`obj`): Pcap object
            timeout (`str`): ARP timeout interval
            tolerance (`int`): Delay tolerance
        Returns:
            True
            False
    """
    prev_pkt = ""
    count = 0
    for pkt in pkts:
        if pkt.haslayer("ARP"):
            count += 1
            log.info(
                "ARP packet {} sent time {}:\n{} ".format(
                    count, pkt.time, pkt.show(dump=True)
                )
            )
            # filter op = is-at ?
            if prev_pkt and count > 1:
                interval = pkt.time - prev_pkt.time
                if (timeout - tolerance) < interval < (timeout + tolerance):
                    log.info(
                        "interval: {} - {} = {}\n ".format(
                            pkt.time, prev_pkt.time, interval
                        )
                    )
                    prev_pkt = pkt
                else:
                    log.error(
                        "Found ARP packet {count} "
                        "With timestamp {time}:\n{pkt}\n"
                        "And ARP packet {pre_c} "
                        "With timestamp {prev_time}:\n{prev_pkt}\n"
                        "interval: {interval}\n".format(
                            count=count,
                            pre_c=count - 1,
                            time=pkt.time,
                            prev_time=prev_pkt.time,
                            interval=interval,
                            pkt=pkt.show(dump=True),
                            prev_pkt=prev_pkt.show(dump=True),
                        )
                    )
                    return False
            else:
                prev_pkt = pkt

    return True
