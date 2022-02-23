"""Common get info functions for l2route"""

# Python
import os
import logging

# pyATS
from pyats.easypy import runtime

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_l2route_mac_route_flags(device, mac_address=None):
    """ Gets route flags along with mac in "show l2route evpn default-gateway 
        detail"

        Args:
            device ('obj'): Device object
            mac_address ('str'): mac address (optional)
        Returns:
            dict: Contains mac address as key and flag as value
            Ex: {
              'ac4a.67a4.7154': 'BInt()Dgr'
            }
            or {}
        Raises:
            None

    """
    try:
        default_gw_output = device.parse(
            "show l2route evpn default-gateway detail"
        )
    except SchemaEmptyParserError as e:
        log.error("Command has not returned any results")
        return {}
    mac_route_flag = dict()
    for evi in default_gw_output['evi']:
        for eth_tag in default_gw_output['evi'][evi].get("eth_tag",{}):
            for producer in default_gw_output['evi'][evi]['eth_tag']\
                [eth_tag].get("producer", {}):
                for mac_addr in default_gw_output['evi'][evi]['eth_tag']\
                    [eth_tag]['producer'][producer].get("mac_addr", {}):
                    mac_route_flag[mac_addr] = []
                    for host_ip in default_gw_output['evi'][evi]['eth_tag']\
                       [eth_tag]['producer'][producer]["mac_addr"]\
                       [mac_addr].get("host_ip",{}):
                       # storing mac route flag along with mac address
                       flag = default_gw_output['evi'][evi]['eth_tag'][eth_tag]\
                           ['producer'][producer]["mac_addr"][mac_addr]\
                           ["host_ip"][host_ip].get("mac_rt_flags", "")
                       mac_route_flag[mac_addr].append(flag)

    if mac_address and (mac_address in mac_route_flag.keys()):
        mac_and_flag = dict.fromkeys(mac_address,mac_route_flag[mac_address])
        return mac_and_flag
    elif mac_address and (mac_address not in mac_route_flag.keys()):
        return {}
    else:
        return mac_route_flag 
