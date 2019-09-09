""" Common get functions for segment-routing """

# Python
import logging
import re

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Running-Config
from genie.libs.sdk.apis.iosxe.running_config.get import (
    get_running_config_section_dict,
)

log = logging.getLogger(__name__)


def get_segment_routing_sid_map_configuration(device, address_family="ipv4"):
    """ Get Segment routing SID map configuration

        Args:
            device ('str'): Device str
            address_family ('str'): Address family
        Returns:
            Dictionary with ip address as key and sid as value
            ex.)
                {
                    '192.168.1.1': '1',
                    '192.168.1.2': '2'
                }
    """
    out = get_running_config_section_dict(
        device=device, section="segment-routing"
    )

    sid_dict = {}

    if not out:
        return None

    p1 = re.compile(r"^(?P<ip_address>\S+) index (?P<sid>\d+) range \d+$")

    connected_prefix_sid_maps = out["segment-routing mpls"][
        "connected-prefix-sid-map"
    ]["address-family {}".format(address_family)].keys()

    for key in connected_prefix_sid_maps:
        key = key.strip()
        m = p1.match(key)
        if m:
            group = m.groupdict()
            sid_dict.update({group["ip_address"]: group["sid"]})
            continue

    return sid_dict


def get_segment_routing_lb_range(device):
    """ Gets segement-routing local block range

        Args:
            device ('obj'): device to use

        Returns:
            ('int', 'int'): label_min, label_max

        Raises:
            N/A
    """
    try:
        out = device.parse("show segment-routing mpls lb")
    except SchemaEmptyParserError:
        return None, None

    return out.get("label_min"), out.get("label_max")


def get_segment_routing_gb_range(device):
    """ Gets segement-routing global block range

        Args:
            device ('obj'): device to use

        Returns:
            ('int', 'int'): label_min, label_max

        Raises:
            None
    """
    try:
        out = device.parse("show segment-routing mpls gb")
    except SchemaEmptyParserError:
        return None, None

    return out.get("label_min"), out.get("label_max")