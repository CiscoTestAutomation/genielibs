'''Common verify functions for BGP'''
# Python
import logging

from genie.utils.timeout import Timeout
from pyats.utils.objects import find, R
from genie.libs.sdk.libs.utils.normalize import GroupKeys

log = logging.getLogger(__name__)


def verify_bgp_l2vpn_evpn_neighbor_in_state(device, neighbor, state='established', 
                                            max_time=60, check_interval=20):
    ''' Verify BGP l2vpn evpn neighbor state

        Args:
            device (`obj`): Device object
            neighbor (`str`): Neighbor IP
            state  (`str`): Expected state
            max_time (`int`): Max time
            check_interval (`int`): Check interval
        Returns:
            result (`bool`): Verified result
    '''
    cmd = 'show bgp l2vpn evpn neighbors {}'.format(neighbor)
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{}':\n{}".format(cmd, e))
            timeout.sleep()
            continue

        reqs = R(['instance', '(.*)', 
                  'vrf', '(.*)', 
                  'neighbor', neighbor, 
                  'session_state', '(?P<state>.*)'])
        found = find([out], reqs, filter_=False, all_keys=True)
        if found:
            session_state = found[0][0].lower()
        else:
            log.error("Failed to get neighbor {} BGP state".format(neighbor))
            timeout.sleep()
            continue

        log.info("Neighbor {} BGP state is {}, expected value is {}"
            .format(neighbor, session_state, state))

        if session_state == state.lower():
            return True
        
        timeout.sleep()

    return False
