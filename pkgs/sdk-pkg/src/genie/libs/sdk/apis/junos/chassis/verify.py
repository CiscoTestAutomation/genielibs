"""Common verification functions for class-of-service"""

# Python
import re
import logging
import operator

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)

def verify_chassis_fpc_slot_state(device, expected_state, 
                                  expected_slot=None, 
                                  all_slots=False, 
                                  environment=False,
                                  max_time=60, 
                                  check_interval=10):
    """ Verifies slot state via 
            - show chassis fpc
            - show chassis environment fpc

    Args:
        device (obj): Device object
        expected_state (list): Expected state of that slot. For example: ["Offline", "Online"].
        expected_slot (str, optional): Expected slot to check. For example: "0".
        all_slots(bool, optional): Flag that indicate all slots need to be verified. Defaults to False.
        environment(bool, optional): Flag that indicate different show commands. Defaults to False. 
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:
        True/False
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            if environment:
                out = device.parse("show chassis environment fpc")
            else:
                out = device.parse('show chassis fpc')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        # Sample outputs:
        # 
        # show chassis fpc:
        # 'fpc-information': {
        #       'fpc': [{'slot': '0', 
        #       'state': 'Offline'}]

        # show chassis environment fpc:
        # {'environment-component-information': {
        #     'environment-component-item': [
        #         {
        #             'name': 'FPC 0',
        #             'state': 'Online', <-----------------
        #             ...

        
        fpc_list = out.q.contains('slot|state', regex=True).get_values('fpc')
        
        # Verify all slot have the same expected_state
        if all_slots:
            states_set = set(out.q.get_values('state'))
            if states_set.issubset(set(expected_state)):
                return True
            
        # Verify given slot has the expected_state
        else:
            # show chassis environment fpc
            if environment:
                items = out.q.get_values("environment-component-item", None)

                for i in items:
                    slot_pattern = re.compile(r'FPC +(?P<slot>\d+)')
                    slot_match = slot_pattern.match(i['name'])

                    if slot_match:
                        if slot_match.groupdict()['slot'] == expected_slot and i['state'] in expected_state:
                            return True
                    
            
            # show chassis fpc
            else:
                for fpc in fpc_list:
                    slot = fpc.get('slot')
                    state = fpc.get('state')

                    if slot == expected_slot and state in expected_state:
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
                                 invert=False,
                                 max_time=60,
                                 check_interval=10,):
    """ Verify slots present in 'show chassis routing-engine'

        Args:
            device (`obj`): Device object
            expected_slots (`list`): Given slots
            invert ('bool', 'optional'): Inverts to check if it doesn't exist
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
        
        if not invert:
            # check if 'slots' has all elements in 'expected'
            if all(i in slots for i in expected_slots):
                    return True

            timeout.sleep()
        else:
            for slot in slots:
                if str(slot) == expected_slots:
                    timeout.sleep()
                    continue
            return True

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
                i['mastership-state'].lower() == expected_slots_states_pairs[i['slot']].lower():
                return True

        timeout.sleep()
    return False

def verify_chassis_fan_tray_present(device,
                                    fan_tray_list,
                                    invert=False,
                                    max_time=60,
                                    check_interval=10,):
    """ Verify fan_tray_list is present in 'show chassis hardware'

        Args:
            device (`obj`): Device object
            fan_tray_list (`list`): Given fan tray list
            invert (`bool',optional): Check fan tray not present. Defaults to False
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
            output = device.parse('show chassis hardware')
        except SchemaEmptyParserError:
            return None

        # Sample output
        # {
        #         "chassis-inventory": {
        #             "chassis": {
        #                 "@junos:style": "inventory",
        #                 "chassis-module": [
        #                     {
        #                         "name": "Midplane" <--------------------
        #                     },
        #                     {
        #                         "description": "RE-VMX",
        #                         "name": "Routing Engine 0"

        modules = output.q.get_values('chassis-module', None)
        if modules:
            names = [i['name'] for i in modules]

        # check if all items in fan_tray_list appears in names
        # >>> l1=[1,2]
        # >>> l2=[1,2,3,4]
        # >>> all(i in l2 for i in l1)
        # True
        # >>> all(i in l1 for i in l2)
        # False    

        if invert:
            # verify all items in fan_tray_list are not in names
            if (set(names)-set(fan_tray_list)) == set(names):
                return True
        else:
            if all(i in names for i in fan_tray_list):
                return True
        
        timeout.sleep()
        continue
        
    return False    

def verify_chassis_environment_present(device,
                                       fan_tray_list,
                                       expected_status,
                                       max_time=60,
                                       check_interval=10,):
    """ Verify all item in fan_tray_list have expected_status in 'show chassis environment'

        Args:
            device (`obj`): Device object
            fan_tray_list (`list`): Given fan tray list
            expected_status (`str`): Expected status
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
            output = device.parse('show chassis environment')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue       

        # Sample output:
        # {'environment-information': {'environment-item': [
        #                                          {'class': 'Fans',
        #                                            'comment': '2760 RPM',
        #                                            'name': 'Fan Tray 0 Fan 1', <---------------
        #                                            'status': 'OK'}, <--------------------------
        #                                           {'class': 'Fans',
        #                                            'comment': '2520 RPM',
        #                                            'name': 'Fan Tray 0 Fan 2',
        #                                            'status': 'OK'},]}}
        environment_items_list = output.q.get_values('environment-item', None)

        # Create a {name:status} dictionary
        name_status_dict = {}

        if environment_items_list:
            for item in environment_items_list:
                
                # >>> name
                # 'Fan Tray 0 Fan 2'
                # >>> m=re.search('(.+?) +Fan +\d+',name).group(1)
                # >>> m
                # 'Fan Tray 0'   
                res = re.search(r'(.+?) +Fan +\d+',item['name'])
                if not res:
                    continue
                name = res.group(1)  

                name_status_dict[name] = item['status']


            # fan_tray_list = ['Fan Tray 0', 'Fan Tray 1', 'Fan Tray 2', 'Fan Tray 3']
            # 
            # name_status_dict = {'Fan Tray 0': 'OK',
            #                     'Fan Tray 1': 'OK',
            #                     'Fan Tray 2': 'Not OK',
            #                     'Fan Tray 3': 'OK'
            #                     }

            # Group all names that have expected_status into a list
            names_list = []
            for name, status in name_status_dict.items():
                if status == expected_status:
                    names_list.append(name)

            # names_list = ['Fan Tray 0', 'Fan Tray 1', 'Fan Tray 3']

            # Compare if all fan tray item in fan_tray_list appear in the list
            if all(i in names_list for i in fan_tray_list):
                return True 
        
        timeout.sleep()
        
    return False      

def verify_chassis_no_alarms(device, 
                             max_time=60, 
                             check_interval=10):
    """ Verify there are no alarms via 'show chassis alarms'

        Args:
            device (`obj`): Device object
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
            output = device.parse('show chassis alarms')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # {
        # "alarm-information": {
        #     "alarm-summary": {
        #         "no-active-alarms": True
        #         }
        #     },
        # }
        if output.q.get_values("no-active-alarms",0) == True:
            return True

        timeout.sleep()
    return False


def verify_chassis_routing_engine(device,
                                  expected_item,
                                  invert=False,
                                  max_time=60,
                                  check_interval=10,):
    """ Verify fan_tray_list is present in 'show chassis hardware'

        Args:
            device (`obj`): Device object
            expected_item (`str`): Hardware inventory item expected
            invert ('bool'): Invert function
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
            output = device.parse('show chassis hardware')
        except SchemaEmptyParserError:
            return None

        # Sample output
        # {
        #         "chassis-inventory": {
        #             "chassis": {
        #                 "@junos:style": "inventory",
        #                 "chassis-module": [
        #                     {
        #                         "name": "Midplane" <--------------------
        #                     },
        #                     {
        #                         "description": "RE-VMX",
        #                         "name": "Routing Engine 0"

        modules = output.q.get_values('chassis-module', None)
        if modules:
            names = [i['name'] for i in modules]

        if not invert:
            for name in names:
                if name == expected_item:
                    return True
        else:
            for name in names:
                if name == expected_item:
                    timeout.sleep()
                    continue
            return True
        timeout.sleep()
    return False


def verify_chassis_hardware_item_present(device,
                            expected_item,
                            invert=False,
                            max_time=60,
                            check_interval=10):
    """ Verify fan_tray_list is present in 'show chassis hardware'

        Args:
            device (`obj`): Device object
            expected_item (`list`): Item name
            invert ('bool'): Invert function
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
            output = device.parse('show chassis hardware')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Sample output
        # {
        #         "chassis-inventory": {
        #             "chassis": {
        #                 "@junos:style": "inventory",
        #                 "chassis-module": [
        #                     {
        #                         "name": "Midplane" <--------------------
        #                     },
        #                     {
        #                         "description": "RE-VMX",
        #                         "name": "Routing Engine 0"

        item_list = output.q.contains(expected_item).get_values('name')

        if not invert:
            if expected_item in item_list:
                return True
            
        else:
            if expected_item not in item_list:
                return True
        
        timeout.sleep()

    return False


def verify_chassis_environment_component_present(device,
                                        name,
                                       component_list,
                                       expected_status,
                                       max_time=60,
                                       check_interval=10,):
    """ Verify all item in fan_tray_list have expected_status in 'show chassis environment'

        Args:
            device (`obj`): Device object
            fan_tray_list (`list`): Given fan tray list
            expected_status (`str`): Expected status
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        result = True
        try:
            output = device.parse('show chassis environment {name}'.format(
                name=name
            ))
        except SchemaEmptyParserError:
            result = False
            timeout.sleep()
            continue

        # fan_tray_list:
        #     - Fan Tray 0
        #     - Fan Tray 1
        #     - Fan Tray 2
        #     - Fan Tray 3        

        # Sample output:
        # {'environment-information': {'environment-component-item': [
        #                                          {'class': 'Fans',
        #                                            'comment': '2760 RPM',
        #                                            'name': 'Fan Tray 0 Fan 1', <---------------
        #                                            'status': 'OK'}, <--------------------------
        #                                           {'class': 'Fans',
        #                                            'comment': '2520 RPM',
        #                                            'name': 'Fan Tray 0 Fan 2',
        #                                            'status': 'OK'},]}}
        environment_items_list = output.q.get_values('environment-component-item', None)
        
        if environment_items_list:
            for item in environment_items_list:
                
                name_ = item.get('name', None)
                state_ = item.get('state', None)

                if name_ in component_list and state_ != expected_status:
                    result = False
                    break
        if component_list[0] not in output.q.get_values('name', None):
            timeout.sleep()
            continue
        if result:
            return True
        timeout.sleep()
    return False

def verify_chassis_power_item_present(device,
                                       component_list,
                                       expected_status,
                                       max_time=60,
                                       check_interval=10):
    """ Verify all item in fan_tray_list have expected_status in 'show chassis environment'

        Args:
            device (`obj`): Device object
            fan_tray_list (`list`): Given fan tray list
            expected_status (`str`): Expected status
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        result = True
        try:
            output = device.parse('show chassis power')
        except SchemaEmptyParserError:
            result = False
            timeout.sleep()
            continue

        power_usage_item_list = output.q.contains('{}|name'.format(
            expected_status, 
        ), regex=True).get_values('power-usage-item')
        
        if power_usage_item_list:
            for item in power_usage_item_list:
                
                name_ = item.get('name', None)
                state_ = item.get('state', None)

                if name_ in component_list and state_ != expected_status:
                    result = False
                    break
        if result:
            return True
        timeout.sleep()
    return False


def verify_chassis_environment_status(device,
                                      expected_item,
                                      expected_status,
                                      max_time=60,
                                      check_interval=10,):
    """ Verify specific item in fan_tray_list has expected_status in 'show chassis environment'

        Args:
            device (`obj`): Device object
            expected_item (`str`): Hardware inventory item expected
            expected_status (`str`): Expected status
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

            output = device.parse('show chassis environment')
        except SchemaEmptyParserError:
            return None      

        # Sample output:
        # {'environment-information': {'environment-item': [
        #                                          {'class': 'Fans',
        #                                            'comment': '2760 RPM',
        #                                            'name': 'Fan Tray 0 Fan 1', <---------------
        #                                            'status': 'OK'}, <--------------------------
        #                                           {'class': 'Fans',
        #                                            'comment': '2520 RPM',
        #                                            'name': 'Fan Tray 0 Fan 2',
        #                                            'status': 'OK'},]}}
        environment_items_list = output.q.get_values('environment-item', None)

        if environment_items_list:
            for item in environment_items_list:
                if item['name'] == expected_item and item['status'] == expected_status:
                    return True

        timeout.sleep()
    return True      


def verify_chassis_alarm_output(device,
                                message_topic,
                                invert=False,
                                max_time=60, 
                                check_interval=10):
    """ Verify message_topic is mentioned via 'show chassis alarms'

        Args:
            device (`obj`): Device object
            message_topic ('str'): Message information that should be in output
            invert ('bool'): Invert function
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
            output = device.parse('show chassis alarms')
        except SchemaEmptyParserError:
            if invert:
                return True
            timeout.sleep()
            continue

        #"alarm-detail": {
        #        "alarm-class": "Major",
        #        "alarm-description": "PSM 15 Not OK",
        #        "alarm-short-description": "PSM 15 Not OK",
        #        "alarm-time": {
        #            "#text": "2020-07-16 13:38:21 EST",
        #        },
        #        "alarm-type": "Chassis"
        #    },
        #    "alarm-summary": {
        #        "active-alarm-count": "1"
        #    }
        # ['PSM 15 Not OK']
        alarm_description = output.q.get_values('alarm-description', None)

        no_output = output.q.get_values('no-active-alarms', 0)

        if not invert:
            if no_output:
                timeout.sleep()
                continue
            for single_description in alarm_description:
                if message_topic in single_description:
                    return True
            timeout.sleep()
            continue
        else:
            match_flag = False
            if no_output:
                return True
            for single_description in alarm_description:
                if message_topic in single_description:
                    match_flag=True
            if match_flag:
                timeout.sleep()
                continue
            else:
                return True

    return False

def verify_chassis_usb_flag_exists(device, 
                                   flag,
                                   usb,
                                   invert=False,
                                   max_time=60, 
                                   check_interval=10):
    """ Verify there is/isn't usb flag in given usb in the routing engine via show chassis hardware detail

        Args:
            device (`obj`): Device object
            flag (`str`): USB flag description in output,
            usb (`str`): USB name in output,,
            invert (`bool`, optional): Used to indicate a reverse verification. default: False
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
            out = device.parse('show chassis hardware detail')
        except SchemaEmptyParserError:
            return None

        # usb: USB
        # usb_insert_flag: umass
        # 
        # {
        #     "chassis-inventory": {
        #         "chassis": {
        #             "chassis-module": [
        #                 {
        #                     'chassis-re-usb-module': [{'description': 'umass0', <-----------usb_insert_flag
        #                                                 'name': 'usb0 ' <------------- usb
        #                                                         '(addr '
        #                                                         '1)',
        #                                                 'product': 'EHCI '
        #                                                             'root '
        #                                                             'hub',
        #                                                 'product-number': '0',
        #                                                 'vendor': 'Intel'}]}
        
        chassis_module_list = out.q.get_values("chassis-module", None)


        for module in chassis_module_list:
            if 'chassis-re-usb-module' in module:
                usb_module_list = module['chassis-re-usb-module']

                for usb_module in usb_module_list:
                    # check if current usb_module has name starts with 'usb'
                    # usb_name: 'usb0 (addr 1)'
                    # usb: 'USB'
                    usb_name = usb_module['name']

                    if usb.lower() in usb_name:
                        # check if current usb_module has the usb_insert_flag
                        usb_description = usb_module['description']
                    
                        if flag in usb_description:
                            if invert:
                                return False
                            else:
                                return True
                        
                        timeout.sleep()
                        continue
            timeout.sleep()
    if invert:
        return True
    else:
        return False            


def verify_chassis_alarms_no_error(device, 
                                   target_fpc,
                                   max_time=60, 
                                   check_interval=10):
    """ Verify there are no error about target FPC via 'show chassis alarms'

        Args:
            device (`obj`): Device object
            target_fpc (`str`): Target fpc. 
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
            output = device.parse('show chassis alarms')
        except SchemaEmptyParserError:
            return True

        errored_pattern = re.compile(r'FPC (?P<slot>\d+) offline due to unreachable destinations')

        # Sample output
        #     {
        #     "alarm-information": {
        #         "alarm-detail": [{
        #             "alarm-class": "Major",
        #             "alarm-description": "FPC 15 Not OK", <--------------------------
        #             "alarm-short-description": "FPC 15 Not OK",
        #             "alarm-time": {
        #                 "#text": "2020-07-16 13:38:21 EST",
        #             },
        #             "alarm-type": "Chassis"
        #         }],
        #         "alarm-summary": {
        #             "active-alarm-count": "1"
        #         }
        #     },
        # }

        description = output.q.get_values('alarm-description', None)

        for d in description:
            if errored_pattern.match(d):
                return True

        timeout.sleep()
    return False



def verify_chassis_fpc_pic_status(device, 
                                  expected_state, 
                                  pic,
                                  fpc,
                                  max_time=60, 
                                  check_interval=10):
    """ Verifies slot state via 
            - show chassis fpc pic-status

    Args:
        device (obj): Device object
        expected_state (str): Expected state of that slot. For example: "Online"
        pic (int): PIC number
        fpc (int): FPC number
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:
        True/False
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show chassis fpc pic-status')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue    

        # Sample output 
        # {
        # "fpc-information": {
        #     "fpc": [
        #         {
        #             "description": "DPCE 2x 10GE R",
        #             "pic": [
        #                 {
        #                     "pic-slot": "0",
        #                     "pic-state": "Online",
        #                     "pic-type": "1x 10GE(LAN/WAN)"
        #                 },
        #                 {
        #                     "pic-slot": "1", <----------------------- pic
        #                     "pic-state": "Online", <----------------- expected_state
        #                     "pic-type": "1x 10GE(LAN/WAN)"
        #                 }
        #             ],
        #             "slot": "0", <----------------------------------- fpc
        #             "state": "Online"
        #         },

        fpc_list = out['fpc-information']['fpc']

        for fpc_item in fpc_list:
            if fpc_item['slot'] == str(fpc):
                
                pic_list = fpc_item['pic']
                for pic_item in pic_list:
                    if pic_item['pic-slot'] == str(pic) and pic_item['pic-state'] == expected_state:
                        return True 
        
        timeout.sleep()
    return False


def verify_chassis_fpc_pic_not_exists(device, 
                                      pic,
                                      fpc,
                                      max_time=60, 
                                      check_interval=10):
    """ Verifies PIC slot does not exist via 
            - show chassis fpc pic-status

    Args:
        device (obj): Device object
        pic (int): PIC number
        fpc (int): FPC number
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:
        True/False
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show chassis fpc pic-status')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue  

        # Sample output 
        # {
        # "fpc-information": {
        #     "fpc": [
        #         {
        #             "description": "DPCE 2x 10GE R",
        #             "pic": [
        #                 {
        #                     "pic-slot": "0",
        #                     "pic-state": "Online",
        #                     "pic-type": "1x 10GE(LAN/WAN)"
        #                 },
        #                 {
        #                     "pic-slot": "1", <----------------------- pic
        #                     "pic-state": "Online", <----------------- expected_state
        #                     "pic-type": "1x 10GE(LAN/WAN)"
        #                 }
        #             ],
        #             "slot": "0", <----------------------------------- fpc
        #             "state": "Online"
        #         },        

        fpc_list = out['fpc-information']['fpc']
        result = True 

        for fpc_item in fpc_list:
            if fpc_item['slot'] == str(fpc):
                
                pic_list = fpc_item['pic']
                for pic_item in pic_list:
                    if pic_item['pic-slot'] == str(pic):
                        result = False 
        if result:
            return result
        timeout.sleep()
    return result


def verify_chassis_pic_exists_under_mic(device, 
                                        mic,
                                        fpc,
                                        invert=False,
                                        max_time=60, 
                                        check_interval=10):
    """ Verifies PIC exists under MIC $mic of FPC $fpc via 
            - show chassis hardware

    Args:
        device (obj): Device object
        mic (int): MIC number
        fpc (int): FPC number
        invert (bool, optional): True means verifying PIC does not exist
        max_time (int, optional): Maximum timeout time. Defaults to 60 seconds.
        check_interval (int, optional): Check interval. Defaults to 10 seconds.

    Returns:
        True/False
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show chassis hardware')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue 

        # Sample output
        # {
        #     "chassis-inventory": {
        #         "chassis": {
        #             "@junos:style": "inventory",
        #             "chassis-module": [
        #                 {
        #                     "chassis-sub-module": [
        #                         {
        #                             "chassis-sub-sub-module": [{
        #                                 "description": "Virtual",
        #                                 "name": "PIC 0",   <------------------------------------- PIC exists
        #                                 "part-number": "BUILTIN",
        #                                 "serial-number": "BUILTIN",
        #                             },],
        #                             "description": "Virtual",
        #                             "name": "MIC 0", <-------------------------------------------- mic
        #                         },
        #                     ],
        #                     "description": "Virtual FPC",
        #                     "name": "FPC 0", <---------------------------------------------------- fpc
        #                 },
        #             ],
        #             "description": "VMX",
        #             "name": "Chassis",
        #             "serial-number": "VM5D4C6B3599",
        #         }
        #     }
        # }

        chassis_module_list = out.q.get_values('chassis-module', None)

        for chassis_module in chassis_module_list:
            # "name": "FPC 0"
            if chassis_module['name'] == 'FPC '+str(fpc):
                chassis_sub_module_list = Dq(chassis_module).get_values('chassis-sub-module', None)

                for sub in chassis_sub_module_list:
                    # "name": "MIC 0"
                    if sub['name'] == 'MIC '+str(mic):
                        
                        # "chassis-sub-sub-module": [{
                        #     "description": "Virtual",
                        #     "name": "PIC 0",
                        #     "part-number": "BUILTIN",
                        #     "serial-number": "BUILTIN",
                        # },],                        
                        if 'chassis-sub-sub-module' in sub:

                            # >>> d1={'name':'aa'}
                            # >>> d2={'name':'bb'}
                            # >>> l=[d1,d2]
                            # >>> names=[i['name'] for i in l]
                            # >>> names
                            # ['aa', 'bb']
                            # >>>                            
                            names_list = [i['name'] for i in sub['chassis-sub-sub-module']]
                            
                            # >>> l=['PIC 0', 'ABC']
                            # >>> ['PIC' in i for i in l]
                            # [True, False]
                            # >>>                            
                            if invert:
                                if not(True in ['PIC' in i for i in names_list]):
                                    return True 
                            else:
                                if True in ['PIC' in i for i in names_list]:
                                    return True 
                        else:
                            if invert:
                                return True
        timeout.sleep()
    return False


def verify_chassis_mic_exists_under_fpc(device, 
                                        mic,
                                        fpc,
                                        invert=False,
                                        max_time=60, 
                                        check_interval=10):
    """ Verifies MIC $mic exists under FPC $fpc via 
            - show chassis hardware

    Args:
        device (obj): Device object
        mic (int): MIC number
        fpc (int): FPC number
        invert (bool, optional): True means verifying PIC does not exist
        max_time (int, optional): Maximum timeout time. Defaults to 60 seconds.
        check_interval (int, optional): Check interval. Defaults to 10 seconds.

    Returns:
        True/False
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show chassis hardware')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue 

        # Sample output
        # {
        #     "chassis-inventory": {
        #         "chassis": {
        #             "@junos:style": "inventory",
        #             "chassis-module": [
        #                 {
        #                     "chassis-sub-module": [
        #                         {
        #                             "description": "Virtual",
        #                             "name": "MIC 0", <-------------------------------------------- mic
        #                         },
        #                     ],
        #                     "description": "Virtual FPC",
        #                     "name": "FPC 0", <---------------------------------------------------- fpc
        #                 },
        #             ],
        #             "description": "VMX",
        #             "name": "Chassis",
        #             "serial-number": "VM5D4C6B3599",
        #         }
        #     }
        # }

        chassis_module_list = out.q.get_values('chassis-module', None)

        for chassis_module in chassis_module_list:
            # "name": "FPC 0"
            if chassis_module['name'] == 'FPC '+str(fpc):
                chassis_sub_module_list = Dq(chassis_module).get_values('chassis-sub-module', None)

                if invert and chassis_sub_module_list==[]:
                    return True

                # find all names in chassis-sub-module
                names_list = [sub['name'] for sub in chassis_sub_module_list]

                # "name": "MIC 0"
                current_name = 'MIC '+str(mic)

                if invert:
                    if current_name not in names_list:
                        return True
                else:
                    if current_name in names_list:
                        return True                 
        timeout.sleep()
    return False            


def verify_chassis_no_error_fpc_mic(device, 
                                    mic,
                                    fpc,
                                    max_time=60, 
                                    check_interval=10):
    """ Verifies no errored FPC $fpc MIC $mic
            - show chassis alarms

    Args:
        device (obj): Device object
        mic (int): MIC number
        fpc (int): FPC number
        max_time (int, optional): Maximum timeout time. Defaults to 60 seconds.
        check_interval (int, optional): Check interval. Defaults to 10 seconds.

    Returns:
        True/False
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show chassis alarms')
        except SchemaEmptyParserError:
            return True

        # Sample output
        #     {
        #     "alarm-information": {
        #         "alarm-detail": [{
        #             "alarm-class": "Major",
        #             "alarm-description": "PSM 15 Not OK", <------------------
        #             "alarm-short-description": "PSM 15 Not OK",
        #             "alarm-time": {
        #                 "#text": "2020-07-16 13:38:21 EST",
        #             },
        #             "alarm-type": "Chassis"
        #         }],
        #         "alarm-summary": {
        #             "active-alarm-count": "1"
        #         }
        #     },
        # }

        errored_pattern = re.compile(r'FPC +(?P<fpc>\d+) +PIC +(?P<pic>\d+) +Invalid +port +profile +configuration')

        description = out.q.get_values("alarm-description", None)

        for d in description:
            if errored_pattern.match(d):
                return False 

        timeout.sleep()
    return True


def verify_chassis_environment_multiple_status(device,
                                               expected_item,
                                               expected_status,
                                               max_time=60, 
                                               check_interval=10):
    """ Verify specific items status in 'show chassis environment'

        Args:
            device (`obj`): Device object
            expected_item (`str`): Hardware inventory item expected
            expected_status (`str`): Expected status
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
            output = device.parse('show chassis environment')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue      

        # Sample output:
        # {'environment-information': {'environment-item': [
        #                                          {'class': 'Fans',
        #                                            'comment': '2760 RPM',
        #                                            'name': 'Fan Tray 0 Fan 1', <---------------
        #                                            'status': 'OK'}, <--------------------------
        #                                           {'class': 'Fans',
        #                                            'comment': '2520 RPM',
        #                                            'name': 'Fan Tray 0 Fan 2',
        #                                            'status': 'OK'},]}}
        environment_items_list = output.q.get_values('environment-item', None)

        if environment_items_list:
            for item in environment_items_list:
                if re.search(r"{} +([\S\s]+)".format(expected_item), item['name']) and item['status'] == expected_status:
                    return True
        timeout.sleep()
    return False


def verify_chassis_fabric_summary_status(device,
                                         expected_item,
                                         expected_status,
                                         max_time=60, 
                                         check_interval=10):
    """ Verify specific items status in 'show chassis fabric summary'

        Args:
            device (`obj`): Device object
            expected_item (`list`): chassis fabric item expected
            expected_status (`str`): Expected status
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
            output = device.parse('show chassis fabric summary')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue     

        # Sample output:
        # "fm-state-item": [
        #        {
        #            "plane-slot": "0",
        #            "state": "Online",
        #            "up-time": "34 days, 18 hours, 43 minutes, 48 seconds"
        #        },
        #        {
        #            "plane-slot": "1",
        #            "state": "Online",
        #            "up-time": "34 days, 18 hours, 43 minutes, 47 seconds"
        #        }
        fm_state_item = output.q.get_values('fm-state-item', None)

        if fm_state_item:
            for item in fm_state_item:
                if str(item['plane-slot']) == str(expected_item) and item['state'].lower() == expected_status.lower():
                    return True
        timeout.sleep()

    return False


def verify_chassis_fabric_plane_status(device,
                                       expected_item,
                                       expected_status,
                                       max_time=60, 
                                       check_interval=10):
    """ Verify specific items status in 'show chassis fabric plane'

        Args:
            device (`obj`): Device object
            expected_item (`list`): Chassis fabric items expected
            expected_status (`str`): Expected status
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
            output = device.parse('show chassis fabric plane')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue      

        # Sample output:
        # "fmp-plane": [
        #        {
        #            "fru-name": [
        #                "FPC",
        #                "FPC"
        #            ],
        #            "fru-slot": [
        #                "0",
        #                "1"
        #            ],
        #            "pfe-link-status": [
        #                "Links ok",
        #                "Links ok",
        #                "Links ok",
        #                "Links ok"
        #            ],
        #            "pfe-slot": [
        #                "0",
        #                "1",
        #                "0",
        #                "1"
        #            ],
        #            "slot": "0",
        #            "state": "ACTIVE"
        #        }
        fm_state_item = output.q.get_values('fmp-plane', None)

        if fm_state_item:
            for item in fm_state_item:
                if item and item['slot'] == expected_item and item['state'].lower() == expected_status.lower():
                    return True
        timeout.sleep()
    
    return False


def verify_chassis_environment_item(device,
                                    expected_item,
                                    invert=False,
                                    max_time=60,
                                    check_interval=10):
    """ Verify specific item in show chassis environment exists or doesn't exist

        Args:
            device (`obj`): Device object
            expected_item (`str`): Hardware inventory item expected
            invert ('bool', 'optional'): Inverts to check if it doesn't exist
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
            output = device.parse('show chassis environment')
        except SchemaEmptyParserError:
            if invert:
                return True
            timeout.sleep()
            continue      

        # Sample output:
        # {'environment-information': {'environment-item': [
        #                                          {'class': 'Fans',
        #                                            'comment': '2760 RPM',
        #                                            'name': 'Fan Tray 0 Fan 1', <---------------
        #                                            'status': 'OK'}, <--------------------------
        #                                           {'class': 'Fans',
        #                                            'comment': '2520 RPM',
        #                                            'name': 'Fan Tray 0 Fan 2',
        #                                            'status': 'OK'},]}}
        environment_items_list = output.q.get_values('name', None)

        if environment_items_list:
            if not invert:
                if expected_item in environment_items_list :
                    return True

            else:
                if expected_item not in environment_items_list :
                    return True
        
        timeout.sleep()

    return False


def verify_chassis_fabric_plane_exists(device,
                                       expected_item,
                                       invert=False,
                                       max_time=60,
                                       check_interval=10):
    """ Verify specific items status in 'show chassis fabric summary'

        Args:
            device (`obj`): Device object
            expected_item (`list`): Chassis fabric items expected
            invert ('bool', 'optional'): Inverts to check if it doesn't exist
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
            output = device.parse('show chassis fabric plane')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue     

        # Sample output:
        # "fmp-plane": [
        #        {
        #            "fru-name": [
        #                "FPC",
        #                "FPC"
        #            ],
        #            "fru-slot": [
        #                "0",
        #                "1"
        #            ],
        #            "pfe-link-status": [
        #                "Links ok",
        #                "Links ok",
        #                "Links ok",
        #                "Links ok"
        #            ],
        #            "pfe-slot": [
        #                "0",
        #                "1",
        #                "0",
        #                "1"
        #            ],
        #            "slot": "0",
        #            "state": "ACTIVE"
        #        }
        fm_state_item = output.q.get_values('slot', None)

        if not invert:
            if expected_item in fm_state_item:
                return True
        else:
            if expected_item not in fm_state_item:
                return True
        timeout.sleep()
    return True

def verify_chassis_fpc_slot_port(device, fpc_slot, pic_slot, expected_pic_port, 
                                 invert=False, max_time=60, check_interval=10):
    """Verifies chassis fpc slot exists

    Args:
        device (obj): Device object
        fpc_slot (str/int): FPC slot number
        pic_slot (str/int): PIC slot number
        expected_pic_port (str): Expected PIC port
        invert (bool): Inverts function
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
    """

    op = operator.truth
    if invert:
        op = lambda val: operator.not_(operator.truth(val))

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show chassis pic fpc-slot {fpc_slot} pic-slot {pic_slot}'.format(
                fpc_slot=fpc_slot,
                pic_slot=pic_slot,
            ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue   

        """
        schema = {
        "fpc-information": {
            "fpc": {
                "pic-detail": {
                    "port-information": {
                        "port": [
                            {
                                "port-number": str,
        """  

        if op(str(expected_pic_port) in out.q.get_values('port-number')):
            return True

            
def verify_chassis_environment_item(device,
                                    expected_item,
                                    invert=False,
                                    max_time=60,
                                    check_interval=10):
    """ Verify specific item in show chassis environment exists or doesn't exist
        Args:
            device (`obj`): Device object
            expected_item (`str`): Hardware inventory item expected
            invert ('bool', 'optional'): Inverts to check if it doesn't exist
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
            output = device.parse('show chassis environment')
        except SchemaEmptyParserError:
            if invert:
                return True
            timeout.sleep()
            continue      

        # Sample output:
        # {'environment-information': {'environment-item': [
        #                                          {'class': 'Fans',
        #                                            'comment': '2760 RPM',
        #                                            'name': 'Fan Tray 0 Fan 1', <---------------
        #                                            'status': 'OK'}, <--------------------------
        #                                           {'class': 'Fans',
        #                                            'comment': '2520 RPM',
        #                                            'name': 'Fan Tray 0 Fan 2',
        #                                            'status': 'OK'},]}}
        environment_items_list = output.q.get_values('name', None)

        if environment_items_list:
            if not invert:
                if expected_item in environment_items_list :
                    return True

            else:
                if expected_item not in environment_items_list :
                    return True
        
        timeout.sleep()

    return False


def verify_chassis_fabric_plane_exists(device,
                                       expected_item,
                                       invert=False,
                                       max_time=60,
                                       check_interval=10):
    """ Verify specific items status in 'show chassis fabric summary'

        Args:
            device (`obj`): Device object
            expected_item (`list`): Chassis fabric items expected
            invert ('bool', 'optional'): Inverts to check if it doesn't exist
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
            output = device.parse('show chassis fabric plane')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue     

        # Sample output:
        # "fmp-plane": [
        #        {
        #            "fru-name": [
        #                "FPC",
        #                "FPC"
        #            ],
        #            "fru-slot": [
        #                "0",
        #                "1"
        #            ],
        #            "pfe-link-status": [
        #                "Links ok",
        #                "Links ok",
        #                "Links ok",
        #                "Links ok"
        #            ],
        #            "pfe-slot": [
        #                "0",
        #                "1",
        #                "0",
        #                "1"
        #            ],
        #            "slot": "0",
        #            "state": "ACTIVE"
        #        }
        fm_state_item = output.q.get_values('slot', None)

        if not invert:
            if expected_item in fm_state_item:
                return True
        else:
            if expected_item not in fm_state_item:
                return True
        timeout.sleep()
    return False
