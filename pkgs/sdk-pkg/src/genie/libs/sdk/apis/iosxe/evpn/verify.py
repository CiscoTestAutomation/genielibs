"""Common verify functions for evpn"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


def verify_nve_evni_peer_ip_state(device, peer_ip, local_vni, evni, state,
                                  max_time=60, check_interval=10):
    '''Issues `show nve peers peer-ip <>` on device and checks for:

       Args:
            device ('obj')      : device to execute on
            peer_ip ('str')     : IP address of peer to be checked
            local_vni('str')    : VNI field in output
            evni('str')         : eVNI field in output
            state('str')        : UP/DOWN
            max_time('int')     : max time for Timeout
            check_interval('int): check interval period for Timeout
       Returns:
            True/False
        '''
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            out = device.parse(f"show nve peers peer-ip {peer_ip}")
        except SchemaEmptyParserError:
            pass
        if out:
            if out.q.contains(local_vni).get_values('peer_ip')[0] == peer_ip and \
              out.q.contains(local_vni).get_values('evni')[0] == evni and \
              out.q.contains(local_vni).get_values('state')[0] == state:
                return True
        timeout.sleep()

    return False
