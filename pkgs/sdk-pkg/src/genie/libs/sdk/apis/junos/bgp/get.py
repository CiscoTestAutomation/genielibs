"""Common get info functions for BGP"""

# Python
import re
import logging
import datetime

# Genie
from genie.utils.dq import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_peer_bgp_address(device, address_family):
    """ Retrieve peer's ip address for 'show bpg neighbor' command

        Args:
            device ('obj'): Device object
            address_family('str'): Mandatory field (ipv4, ipv6)

        Returns:
            an ip address
    """
    # 20.0.0.3
    ipv4 = re.compile(r'^[\d\.]+$')

    # 2001:30::1
    # 2001:0:3238:DFE1:63::FEFB
    ipv6 = re.compile(r'^[\w\:]+$')

    try:
        out = device.parse("show bgp neighbor")
    except SchemaEmptyParserError:
        return None

    peers_list = out.q.get_values("bgp-peer")

    for peer in peers_list:
        peer_address = peer.get('peer-address')

        # 20.0.0.3+63208
        if '+' in peer_address:
            peer_address = peer_address.split('+')[0]

        if 'ipv4' in address_family:
            if ipv4.match(peer_address):
                return peer_address
            else:
                continue
        
        elif 'ipv6' in address_family:
            if ipv6.match(peer_address):
                return peer_address
            else:
                continue
        else:
            return None

