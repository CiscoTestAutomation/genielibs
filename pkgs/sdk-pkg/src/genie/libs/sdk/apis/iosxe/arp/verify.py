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


def verify_arp_vrf_interface_mac_entry(
    device, ip_address, expected_interface, vrf=None, expected_mac=None, 
    max_time=30, check_interval=10
):
    """ Verify that interface and mac (optional) passed in are the 
        outgoing interface and mac for host in ARP table 
        'show arp vrf {vrf} {ip}' / 'show arp {ip}'

        Args:
            device (`obj`): Device object
            ip_address (`str`): Ip address
            expected_interface ('str'): interface
            vrf ('str', optional): vrf interface, default None
            expected_mac ('str', optional): mac address, default None
            max_time ('int', optional): maximum time to wait in seconds, 
                default 30
            check_interval ('int', optional): how often to check in seconds, 
                default 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        received_intf_mac = device.api.get_arp_interface_mac_from_ip(
            device=device,
            ip_address=ip_address,
            vrf=vrf,
        )

        if received_intf_mac:

            if expected_mac:
                if (expected_interface and expected_mac) in received_intf_mac:
                    return True
            else:
                if expected_interface in received_intf_mac:
                    return True

        timeout.sleep()

    if not received_intf_mac:
        log.error(
            'Unable to get entry {} related interface and mac from'
            'show arp vrf {} {}'.format(ip_address, vrf, ip_address)
        )
    elif expected_mac:
        log.error(
            'Unable to find entry for interface {} and Mac {} in arp host'
            '{} table {}'.format(expected_interface, expected_mac, ip_address,
                received_intf_mac)
        )
    else:
        log.error(
            "Unable to find entry for interface {} in arp host {} "
            "table {}".format(expected_interface, ip_address, received_intf_mac)
        )
 
    return False
