"""Common get info functions for DNS"""

# Python
import os
import logging
import re

log = logging.getLogger(__name__)


def verify_dns_packets(packets, ip_address):
    """ Analyze the DNS packets

        Args:
            packets('str'): Packets to analyze
            ip_address('str'): The captured IP address

        Returns:
            True
            False
    """

    for pkt in packets:
        if (
            pkt.haslayer("IP")
            and pkt.haslayer("DNS")
            and pkt["DNS"].haslayer("DNS Resource Record")
        ):
            if (
                pkt["DNS"]["DNS Resource Record"].rdata
                and ip_address == pkt["DNS"]["DNS Resource Record"].rdata
            ):
                log.info(
                    "Here is the packet meeting "
                    "the requirements:\n{pkt}".format(pkt=pkt.show(dump=True))
                )
                return True

    return False
