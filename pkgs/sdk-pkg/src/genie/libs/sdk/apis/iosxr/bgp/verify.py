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


def verify_bgp_neighbor_exist(device, neighbor, address_family, 
                              max_time=60, check_interval=10):
    """ Verify bgp neighbor exists in 'show bgp {address_family} summary'

        Args:
            device ('obj'): Device object
            neighbor ('str'): Neighbor to check
            address_family ('str'): Address family
            max_time ('int'): Maximum time to wait
            check_interval ('int'): Check interval

        Returns:
            result ('bool'): Verified result
    """
    cmd = 'show bgp {address_family} summary'.format(address_family=address_family)
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
            timeout.sleep()
            continue

        reqs = R(['instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)',
                  'neighbor', neighbor, '(.*)'])
        found = find([out], reqs, filter_=False, all_keys=True)
        if found:
            log.info("BGP neighbor {nbr} is present".format(nbr=neighbor))
            return True

        timeout.sleep()

    return False


def verify_bgp_neighbor_in_state(device, neighbor, vrf='', address_family='',
                                 max_time=60, check_interval=10,
                                 expected_state='established'):
    """ Verify bgp neighbor exists in 'show bgp neighbors {nbr}'

        Args:
            device ('obj'): Device object
            neighbor ('str'): Neighbor to check
            vrf ('str'): Vrf
            address_family ('str'): Address family
            expected_state ('str'): Expected state
            max_time ('int'): Maximum time to wait
            check_interval ('int'): Check interval

        Returns:
            result ('bool'): verified result
    """
    if vrf and address_family:
        cmd = 'show bgp vrf {vrf} {address_family} neighbors {nbr}'.format(
                vrf=vrf, address_family=address_family, nbr=neighbor)
    elif vrf:
        cmd = 'show bgp vrf {vrf} neighbors {nbr}'.format(vrf=vrf, nbr=neighbor)
    elif address_family:
        cmd = 'show bgp {address_family} neighbors {nbr}'.format(
                address_family=address_family, nbr=neighbor)
    else:
        cmd = 'show bgp neighbors {nbr}'.format(nbr=neighbor)

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{cmd}':{e}".format(cmd=cmd, e=e))
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
            log.error("Failed to get neighbor {nbr} BGP state".format(nbr=neighbor))
            timeout.sleep()
            continue

        log.info("Neighbor {nbr} BGP state is {state}, expected value is {exp}"
            .format(nbr=neighbor, state=session_state, exp=expected_state))

        if session_state == expected_state.lower():
            return True

        timeout.sleep()

    return False
