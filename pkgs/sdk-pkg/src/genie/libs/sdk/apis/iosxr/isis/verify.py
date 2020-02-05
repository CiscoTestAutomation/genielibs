'''Common verify functions for isis'''
# Python
import logging

from genie.utils.timeout import Timeout
from pyats.utils.objects import find, R
from genie.libs.sdk.libs.utils.normalize import GroupKeys

log = logging.getLogger(__name__)


def verify_isis_neighbor_in_state(device, interfaces, state='up', 
                                  max_time=60, check_interval=20):
    ''' Verify ISIS neighbor state

        Args:
            device (`obj`): Device object
            interfaces (`list`): ISIS neighbor interfaces
            state  (`str`): Expected state
            max_time (`int`): Max time
            check_interval (`int`): Check interval
        Returns:
            result (`bool`): Verified result
    '''
    cmd = 'show isis neighbors'
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{}':\n{}".format(cmd, e))
            timeout.sleep()
            continue

        result = True
        intfs = '|'.join(interfaces)
        reqs = R(['isis', '(.*)', 
                  'vrf', '(.*)', 
                  'interfaces', '(?P<interface>' + intfs + ')', 
                  'neighbors', '(?P<neighbor>.*)', 
                  'state', '(?P<state>.*)'])

        found = find([out], reqs, filter_=False, all_keys=True)
        if found and len(found) == len(interfaces):
            keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={}, source=found, all_keys=True)
        else:
            log.error("Failed to find required ISIS neighbor interface: {}".format(interfaces))
            timeout.sleep()
            continue

        for intf_dict in keys:
            log.info("Interface {} status is {}, expected value is {}"
                .format(intf_dict['interface'], intf_dict['state'].lower(), state))
            if intf_dict['state'].lower() != state.lower():
                result = False

        if result:
            return True

        timeout.sleep()

    return False


def verify_no_isis_neighbor(device, max_time=60, check_interval=20):
    ''' Verify ISIS neighbors not found

        Args:
            device (`obj`): Device object
        Returns:
            result (`bool`): Verified result
    '''
    cmd = 'show isis neighbors'
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception:
            return True

        reqs = R(['isis', '(.*)', 
                  'vrf', '(.*)', '(?P<interface>.*)'])

        found = find([out], reqs, filter_=False, all_keys=True)
        if found and not found[0][0]:
            return True
        timeout.sleep()

    return True
