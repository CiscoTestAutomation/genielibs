'''Common get info functions for bgp'''
# Python
import re
import logging
import datetime

# unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout
from genie.libs.sdk.apis.utils import get_config_dict
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def get_bgp_peer_prefixes(
    device: object,
    peer_address: str,
) -> dict:
    """Return a dictionary of BGP prefix value

    Args:
        device (object): Device object
        peer_address (str): Peer address

    Returns:
        dict: Dictionary of prefix values
    """

    try:
        out = device.parse('show bgp neighbor')
    except SchemaEmptyParserError:
        return dict()

    # Example dict
    # "bgp-information": {
    #     "bgp-peer": [
    #         {
    #             "bgp-rib": [
    #                 {
    #                     "accepted-prefix-count": str,
    #                     "active-prefix-count": str,
    #                     "received-prefix-count": str,
    #                     "advertised-prefix-count": str,
    #                     "suppressed-prefix-count": str,

    for peer in out.q.get_values('bgp-peer'):
        peer_interface_ = peer.get('peer-address')

        # 20.0.0.3+63208
        if '+' in peer_interface_:
            peer_interface_ = peer_interface_.split('+')[0]

        # 20.0.0.2/24
        if '/' in peer_address:
            peer_address = peer_address.split('/')[0]

        if peer_interface_ != peer_address:
            continue

        ret_dict = {
            "accepted-prefix-count": Dq(peer).get_values('accepted-prefix-count', 0),
            "active-prefix-count": Dq(peer).get_values('active-prefix-count', 0),
            "received-prefix-count": Dq(peer).get_values('received-prefix-count', 0),
            "advertised-prefix-count": Dq(peer).get_values('advertised-prefix-count', 0),
            "suppressed-prefix-count": Dq(peer).get_values('suppressed-prefix-count', 0),
            }

        return ret_dict


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


def get_peer_restart_flags_received(device, neighbor_address=None):
    """ Retrieve peer restart flags received

        Args:
            device ('obj'): Device object
            neighbor_address ('str'): Neighbor IP address

        Returns:
            List of peer restart flags received
    """
    
    try:
        if neighbor_address:
            out = device.parse("show bgp neighbor {neighbor_address}".format(
                neighbor_address=neighbor_address
            ))
        else:
            out = device.parse("show bgp neighbor")
    except SchemaEmptyParserError:
        return None

    peer_restart_flags = out.q.get_values('peer-restart-flags-received')
    
    return peer_restart_flags

"""Common verification functions for BFD"""

def get_bgp_summary_neighbor_state_count(device, expected_neighbor_state='Establ', max_time=60, check_interval=10):
    """ Get bgp summary peer-state count

    Args:
        device (obj): Device object
        expected_neighbor_state (str): Expected neighbor state. Defaults to 'Establ'.
        max_time (int, optional): Maximum timeout time. Defaults to 60 seconds.
        check_interval (int, optional): Check interval. Defaults to 10 seconds.
    """
    try:
        out = device.parse('show bgp summary')
    except SchemaEmptyParserError:
        return None

    if expected_neighbor_state=='Establ':
        expected_neighbor_state='Establ|[\d\/ ]+'
    
    state_count = out.q.contains('peer-state').contains(expected_neighbor_state, 
        regex=True).count()

    return state_count