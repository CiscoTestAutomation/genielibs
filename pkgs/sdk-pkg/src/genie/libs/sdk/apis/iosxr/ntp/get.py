"""Common get info functions for NTP"""

# Python
import logging
import re

# pyATS
from pyats.utils.objects import find, R
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# utils
# Running-Config
from genie.libs.sdk.apis.iosxe.running_config.get import search_running_config

# interface
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_ip_address

log = logging.getLogger(__name__)


def get_ntp_servers(device):
    """ Get configured ntp servers

        Args:
            device (`obj`): Device object
        Returns:
            peer_dict (`dict`): Peer dictionary
    """
    try:
        out = device.parse("show ntp associations")
        return out.get("peer", None)
    except SchemaEmptyParserError as e:
        log.error("Command 'show ntp associations' " "did not return any results")
    return None


def get_ntp_source_interface_ip(device):
    """ Get source interface IP address used for NTP synchronization 

        Args:
            device (`obj`): Device object
        Returns:
            ip (`str`): IP address of the interface
            interface (`str`): Interface name
    """
    interface = search_running_config(device, "ntp source")
    log.info("Found ntp source interface {}".format(interface))

    ip = get_interface_ip_address(device, interface)
    return ip, interface


def get_ntp_outgoing_interface(device, system_peer):
    """ Get the interface which is used to communicate with NTP system peer

        Args:
            device (`obj`): Device object
            system_peer (`str`): System peer ip
        Returns:
            interface (`str`): Interface name
    """
    try:
        out = device.parse("show ip cef {}".format(system_peer))
    except SchemaEmptyParserError as e:
        log.error(
            "Command 'show ip cef {}' " "did not return any results".format(system_peer)
        )
        return None

    reqs = R(
        [
            "vrf",
            "(?P<vrf>.*)",
            "address_family",
            "(?P<af>.*)",
            "prefix",
            "(?P<ip>.*)",
            "nexthop",
            "(?P<nexthop>.*)",
            "outgoing_interface",
            "(?P<intf>.*)",
            "(?:.*)",
        ]
    )

    found = find([out], reqs, filter_=False, all_keys=True)
    if found:
        keys = GroupKeys.group_keys(
            reqs=reqs.args, ret_num={}, source=found, all_keys=True
        )
    else:
        log.error("No interface was found")
        return None

    interface = keys[0]["intf"]
    return interface


def get_ntp_md5_peer(device, vrf="default", mode="client"):
    """ Get a ntp peer that has established session using MD5

        Args:
            device (`obj`): Device object
            vrf (`str`): Default vrf name
            mode (`str`): Default mode
        Returns:
            peer (`str`): Peer ip
    """
    try:
        out = device.parse("show ntp associations detail")
    except SchemaEmptyParserError as e:
        log.error(
            "Command 'show ntp associations detail' "
            "did not return any results, Error: {}".format(str(e))
        )
        return None

    try:
        peer_dict = out["vrf"][vrf]["associations"]["address"]
    except KeyError as ke:
        log.error("Cannot find key, Error: {}".format(str(ke)))
        return None

    for peer, data in peer_dict.items():
        sub_dict = (
            data.get("local_mode", {}).get(mode, {}).get("isconfigured", {}).get("True")
        )
        if (
            sub_dict
            and sub_dict["isconfigured"] == True
            and sub_dict["authenticated"] == True
            and sub_dict["sane"] == True
            and sub_dict["valid"] == True
        ):
            return peer

    return None


def get_ntp_system_peer(device, peer_list, max_time=90, check_interval=15):
    """ Get a ntp system peer from the given peer list

        Args:
            device (`obj`): Device object
            peer_list (`list`): Peer list
            max_time (`int`): Max time
            check_interval (`int`): Check interval
        Returns:
            sys_peer (`str`): System peer ip
    """
    sys_peer = None
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse("show ntp associations")
        except SchemaEmptyParserError as e:
            log.error(
                "Command 'show ntp associations' "
                "did not return any results, Error: {}".format(str(e))
            )
            pass
        try:
            sys_peer = out["clock_state"]["system_status"]["associations_address"]
            if sys_peer in peer_list:
                return sys_peer
        except KeyError as ke:
            log.error("Cannot find key, Error: {}".format(str(ke)))
            pass

        timeout.sleep()

    return None


def get_ntp_packet(packets, ip_address_source, ip_address_destination):
    """ Find ntp packet with src ip and dest ip in pcap file

        Args:
            packets (`obj`): pcap object
            ip_address_source (`str`): source ip
            ip_address_destination (`str`): destination ip
        Returns:
            pkt (`obj`): verified ntp packet
    """
    for pkt in packets:
        if (
            pkt.haslayer("IP")
            and pkt["IP"].src == ip_address_source
            and pkt["IP"].dst == ip_address_destination
        ):
            log.info("Found NTP packet:\n{pkt}".format(pkt=pkt.show(dump=True)))
            return pkt
    return None
