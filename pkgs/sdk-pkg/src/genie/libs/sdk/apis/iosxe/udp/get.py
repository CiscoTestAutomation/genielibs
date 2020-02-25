"""Common get info functions for UDP"""

# Python
import logging


log = logging.getLogger(__name__)


def analyze_udp_in_mpls_packets(
    packets, ip_address, ttl, packet_count, destination_port
):
    """ Analyze passed packets

        Args:
            packets('str'): Packets to analyze
            ip_address ('str'): Destination IP address
            ttl (`int`): Time to live
            packet_count (`int`): Packet count to check during
                packet analysis
            destination_port (`int`): Destination port start "traceroute"
        Returns:
            pkt count
        Raises:
            None 
    """
    try:
        from scapy.all import load_contrib, UDP
        from scapy.contrib.mpls import MPLS
    except ImportError:
        raise ImportError('scapy is not installed, please install it by running: '
                          'pip install scapy') from None
    count = 0

    for pkt in packets:
        # Analyze MPLS packets
        if pkt.type == 34887:
            load_contrib("mpls")
            mpls_pkt = MPLS(pkt["Raw"])

            if (
                mpls_pkt.haslayer("IP")
                and mpls_pkt["IP"].dst == ip_address
                and mpls_pkt["IP"].ttl == ttl
                and mpls_pkt.haslayer("UDP")
            ):

                # Catch the start of source and destination ports
                if count == 0:
                    sport_count = mpls_pkt["UDP"].sport
                    dport_count = destination_port
                    log.info(
                        "Found a packet that meets the requirement:\nDestination:\t{"
                        "ip_pkt_dst}\nDestination Port:\t{dst_port}\nSource:\t\t{"
                        "ip_pkt_src}\nSource Port:\t{src_port}\nUDP Packet:\t{"
                        "mpls_pkt}\n".format(
                            ip_pkt_dst=mpls_pkt["IP"].dst,
                            dst_port=dport_count,
                            ip_pkt_src=mpls_pkt["IP"].src,
                            src_port=sport_count,
                            mpls_pkt="True" if mpls_pkt["UDP"] else "False",
                        )
                    )
                    count += 1
                    continue

                # Verify source and destination ports are incrementing
                if mpls_pkt["UDP"].sport != sport_count + 1:
                    log.info(
                        "Source port didn't increment to "
                        "{source_port} as expected; instead it is {sp}".format(
                            source_port=sport_count + 1,
                            destination_port=dport_count + 1,
                            sp=mpls_pkt["UDP"].sport,
                        )
                    )
                    return None, 0
                elif mpls_pkt["UDP"].dport != dport_count + 1:
                    log.info(
                        "destination port didn't increment to "
                        "{destination_port} as expected; instead "
                        "it is {dp}".format(
                            source_port=sport_count + 1,
                            destination_port=dport_count + 1,
                            dp=mpls_pkt["UDP"].dport,
                        )
                    )
                    return None, 0
                else:
                    count += 1
                    sport_count += 1
                    dport_count += 1
                    log.info(
                        'Found a packet that "meets" the requirement:\nDestination:\t{'
                        "ip_pkt_dst}\nDestination Port:\t{dst_port}\nSource:\t\t{"
                        "ip_pkt_src}\nSource Port:\t{src_port}\nUDP Packet:\t{"
                        "mpls_pkt}\n".format(
                            ip_pkt_dst=mpls_pkt["IP"].dst,
                            dst_port=dport_count,
                            ip_pkt_src=mpls_pkt["IP"].src,
                            src_port=sport_count,
                            mpls_pkt="True" if mpls_pkt["UDP"] else "False",
                        )
                    )

                if count == packet_count:
                    return pkt, count

    return None, count
