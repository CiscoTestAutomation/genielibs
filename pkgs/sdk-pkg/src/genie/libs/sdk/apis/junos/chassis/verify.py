"""Common verification functions for class-of-service"""

# Python
import logging
import operator

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)

def verify_chassis_fpc_slot_state(device, expected_slot, expected_state, max_time=60, check_interval=10):
    """ Verifies slot state via show chassis fpc

    Args:
        device (obj): Device object
        expected_slot (bool): Expected slot to check.
        expected_state (str): Expected state of that slot.
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:
        True/False
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show chassis fpc')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dict
        # 'fpc-information': {
        #       'fpc': [{'slot': '0', 
        #       'state': 'Offline'}]

        # object_types_ = out.q.get_values("cos-object-type")
        
        fpc_list = out.q.contains('slot|state', regex=True).get_values('fpc')
        
        for fpc in fpc_list:
            slot = fpc.get('slot')
            state = fpc.get('state')
            if slot == expected_slot and state == expected_state:
                return True

        timeout.sleep()
        
    return False

def verify_chassis_re_state(device,
                       expected_re_state,
                       max_time=60,
                       check_interval=10,):
    """ Verify output of show chassis routing-engine ends as expected state

        Args:
            device (`obj`): Device object
            expected_re_state (`str`): Expected end of output state
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show chassis routing-engine')
        except SchemaEmptyParserError:
            return None

        # Sample output
        # "route-engine-information": {
        #             "route-engine": [{
        #                   "mastership-state": "Master",
        #                    ...
        #              },
        #              {
        #                   "mastership-state": "Backup",
        #              }]
        #              "re-state": {master}

        re_state = output.q.get_values('re-state')
        if expected_re_state in re_state:
            return True

        timeout.sleep()
    return False


def verify_chassis_slots_present(device,
                                 expected_slots,
                                 max_time=60,
                                 check_interval=10,):
    """ Verify slots present in 'show chassis routing-engine'

        Args:
            device (`obj`): Device object
            expected_slots (`list`): Given slots
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show chassis routing-engine')
        except SchemaEmptyParserError:
            return None

        # Sample output
        # {
        # "route-engine-information": {
        #     "route-engine": [{
        #         ...
        #         "model": "RE-VMX",
        #         "slot": "0", <------------------
        #         "start-time": {
        #             "#text": "2019-08-29 09:02:22 UTC"
        #         },

        slots = output.q.get_values('slot')
        
        # check if 'slots' has all elements in 'expected'
        if all(i in slots for i in expected_slots):
                return True

        timeout.sleep()
    return False


def verify_chassis_slot_state(device,
                              expected_slots_states_pairs,
                              max_time=60,
                              check_interval=10,):
    """ Verify slot's state in 'show chassis routing-engine'

        Args:
            device (`obj`): Device object
            expected_slots_states_pairs (`dict`): Expected states with given slots. E.g.,{'slot1':'state1', 'slot2':'state2'}
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show chassis routing-engine')
        except SchemaEmptyParserError:
            return None

        # Sample output
        # {
        # "route-engine-information": {
        #     "route-engine": [{
        #         ...
        #         "model": "RE-VMX",
        #         "mastership-state": "Master",   <------------------    
        #         "slot": "0", <-----------------
        #         "start-time": {
        #             "#text": "2019-08-29 09:02:22 UTC"
        #         },

        rout=Dq(out).contains('slot|mastership-state',regex=True).reconstruct()
        # rout example:
        # {'route-engine-information': {'route-engine': 
        #                                   [{'mastership-state': 'Master',
        #                                         'slot': '0'},
        #                                    {'mastership-state': 'Backup',
        #                                         'slot': '1'}]}}

        route_engines = Dq(rout).get_values('route-engine')
        # 'route_engines' example:
        # [{'mastership-state': 'Master', 'slot': '0'}, 
        # {'mastership-state': 'Backup', 'slot': '1'}]

        # 'expected_slots_states_pairs' example:
        # {'0':'master', '1':'backup'} 
        for i in route_engines:
            if i['slot'] in expected_slots_states_pairs and \
                i['mastership-state'].lower() == expected_slots_states_pairs[i['slot']]:
                return True

        timeout.sleep()
    return False