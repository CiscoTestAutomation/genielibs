import json
import time
import logging
import importlib

from datetime import datetime
from collections import OrderedDict
from genie.utils.timeout import Timeout


from .blitz_control import blitz_control
from .markup import get_variable, save_variable

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed, Errored, Skipped,\
                          Aborted, Passx, Blocked

log = logging.getLogger()


def loop(self, steps, testbed, section, name, action_item):

    ret_list = []

    loop_until = action_item.get('loop_until')

    if loop_until:
        msg = "Executing actions in a loop with loop_until: '{l}'".format(l=loop_until)
    else:
        msg = 'Executing actions in a loop'

    # Since loop shows up in action level, it has to be treated as an action and step
    with steps.start(msg, continue_=True) as step:
        # _loop function actually as a dispatcher between blitz loop and
        loop_return_items = _loop(self, step, testbed, section, action_item, ret_list,
                                  name)

        # Each loop is treated as one action.
        # Actions within a loop are considered as substep.
        if loop_return_items: 

            # As a result if a condition is met. The function will be applied on
            # The loop action itself, which in turns applies to all the substeps.
            if 'loop_conditioned' in loop_return_items[0]:
                getattr(step, loop_return_items[0]['loop_conditioned'])(
                    'condition is met, the loop step result is set to {f}'.format(
                        f=loop_return_items[0]['loop_conditioned']))

            # if loop_until is set to passed/failed, then the goal is to
            # loop until pass/fail
            elif loop_until:

                prev_loop_result  = loop_return_items[-1]['step_result']

                if loop_until.lower() == str(prev_loop_result):
                    loop_return_items = [{'step_result': 'passed', 'device': None,
                                          'description': 'loop with loop_until', 'action': 'loop'}]

                    getattr(step, 'passed')(
                        "The loop_until was set to '{a}' and last attempted action in the loop"
                        " had the same result. Hence the loop_output is set to passed".\
                        format(a=loop_until))
                else:
                    loop_return_items = [{'step_result': 'failed', 'device': None, 
                                          'description': 'loop with loop_until', 'action': 'loop'}]

                    getattr(step, 'failed')(
                        "The loop_until was set to '{a}' and last attempted action in the loop did "
                        " not have the same result. Hence the loop_output is set to failed".\
                        format(a=loop_until))

    return {'loop_output': loop_return_items}

def _loop(self, steps, testbed, section, action_item, ret_list, name):

    # actions that would be looped over
    # why Popping this one instead of only using get?
    # Because of saved variables, for actions it will be replaced 
    # below, before calling the action
    try:
        actions = action_item.pop('actions')
    except KeyError:
        raise Exception ("There has to be at least one action to loop over.")

    # Sending to get_variable to replace saved items.
    action_item.update({'self': self})
    action_item = get_variable(**action_item)
    action_item.pop('self')

    # The name of the iterable that carries, list item, or range number
    # that could be reused within the loop
    iterable_name = action_item.get('loop_variable_name')

    # range of number just like loop to range in python
    range_ = action_item.get('range')

    # a list or a dictionary to loop over
    iterator_ = action_item.get('value')

    # if it is maple
    maple = action_item.get('maple')

    # the section in maple loop
    section_ = action_item.get('section')

    # this item would be added to kwargs of the loop (loop is behaving as an action)
    control = action_item.get('run_condition')

    # until keyword that works just like while
    # It allows user to loop while a certain condition is met
    until = action_item.get('until')

    # do_until keyword that works just like do-while
    # It allows user to run the loop once and then for
    # every run after that the condition will be checked for each loop run
    # the first run would happen no matter if condition is met or not
    do_until = action_item.get('do_until')

    # every_seconds to synchronize the run so each action within a loop
    # run within a bracket of time, so if action ended before this value
    # next action would run after waiting for action_duration - every_seconds
    every_seconds = action_item.get('every_seconds')

    # maximum time of iteration that loop would stop after
    max_time = action_item.get('max_time')

    # the interval is entirely optional, number of pauses for rerunning the same loop
    check_interval = action_item.get('check_interval', 0) if max_time else None

    # If provided, (passed/failed) , check if last iteration is passed/failed
    # and come out of the loop
    loop_until = action_item.get('loop_until')

    # Checking if the loop is of type blitz or it is a maple loop
    if maple:
        _maple_loop_helper(self,
                           steps,
                           testbed,
                           section,
                           name,
                           actions=actions,
                           section_=section_)
    else:
        return _loop_helper(self,
                            steps,
                            testbed,
                            section,
                            name,
                            iterable_name,
                            ret_list,
                            loop_until=loop_until,
                            max_time=max_time,
                            check_interval=check_interval,
                            until=until,
                            do_until=do_until,
                            actions=actions,
                            range_=range_,
                            iterator_=iterator_,
                            control=control,
                            every_seconds=every_seconds)

def _loop_helper(self,
                 steps,
                 testbed,
                 section,
                 name,
                 iterable_name,
                 ret_list,
                 loop_until=False,
                 max_time=None,
                 check_interval=None,
                 until=None,
                 do_until=None,
                 actions=None,
                 range_=None,
                 iterator_=None,
                 control=None,
                 every_seconds=None):
    conditioned = False

    # if condition is true, need to add the condition result to the return list
    # since the ret_list is empty at first it would surely go to the start of the list
    # conditioned keyword is set True so no looping would happens.
    if control and control['if']:
        ret_list.append({
            'loop_conditioned': control['function'],
            'device': None
        })
        conditioned = True

    # not possible to do until and do_until at once
    # until functionality is to loop until a condition is met
    # if condition is met before running the loop, the loop wont start
    # do_until is to also check a condition, but if the condition is met
    # before the start at least run the loop once
    if until and do_until:
        raise Exception('You only can have one terminating condition ')

    # cant have a range and value at once
    # range is like looping a range in python,
    # if range_ then the loop is happening over a range of values
    # a list of numbers from 0 to range [0, range)
    # if iterator_, then a list or a dictionary is defined
    # then the loop happens over that iterator_
    # A loop cant happen over both at the same time
    if (range_ and iterator_):
        raise Exception('You can only have one iterable item per each loop')

    # need to at least have
    if (not range_ and not iterator_) and not until and not do_until and not loop_until:
        raise Exception('At least on iterable item or terminating condition')

    # timeout if until or do_until or loop_until are looping through infinity
    timeout = Timeout(max_time, check_interval)

    loop_list = None
    iterator_len = None
    iterator_index = 0

    # loop_list and iterator_len would be assigned value if there is list to loop over
    # Or a range to loop over
    if range_:
        loop_list = range(range_)
        iterator_len = len(loop_list)

    if iterator_:
        loop_list = iterator_
        iterator_len = len(loop_list)

    # until condition would be sent to blitz_control
    # in order to evaluate and see if the condition is true or not
    if until:
        until = blitz_control(self, until, 'until')

    while not conditioned:

        # capturing the start time of the action to calculate 
        # the duration of the action
        loop_start_time =  datetime.now()
        log.debug('loop start time: {}'.format(str(loop_start_time)))

        if (iterator_len and iterator_index == iterator_len):
            log.info(
                'The loop finished because the iterable item is parsed to the end'
            )
            break
        if until:
            log.info(
                'Loop terminating condition is met, going out of this loop.')
            break
        if (max_time and not timeout.iterate()):
            log.info('Timeout is reached, going out of this loop')
            break

        # assign each item in an iterable_item to a variable to be used later on within the actions
        # the iterable_name should exist in the testcase
        if iterable_name and loop_list:

            # parse through dictionary
            if isinstance(loop_list, dict):
                item_dict_key = list(loop_list.keys())[iterator_index]
                value = {item_dict_key: loop_list[item_dict_key]}

            # parse through list
            else:
                value = loop_list[iterator_index]
            save_variable(self, iterable_name, value)

        # running all the actions and adding the outputs of those actions to return list
        if actions:

            ret_list.extend(list(_loop_action_parser(self, steps, testbed, section, actions, loop_until=loop_until)))

        if loop_until:
            # Considering that multiple actions might be looped over this
            # looks for the first pass/fail of the actions and check if it
            # equals loop_until then break the loop
            loop_until_met = False
            for index_ in range(len(ret_list)):
                if str(ret_list[index_]['step_result']) == loop_until.lower():
                    loop_until_met = True
                    break

            if loop_until_met:
                ret_list = ret_list[index_:index_+1]
                break

        # if terminating condition is set with key do_until run the actions at least once then check for the condition
        if do_until:
            until = blitz_control(self, do_until, 'do_until')

        # increase the iterator_index until it hits the iterator_len it would break then
        if iterator_len:
            iterator_index += 1

        # Calculating the loop finishing time in seconds
        loop_end_time = datetime.now()
        log.debug('Action end time: {}'.format(str(loop_end_time)))
        loop_duration = loop_end_time - loop_start_time
        loop_duration_in_seconds = loop_duration.total_seconds()

        # if every_seconds specified, calculate the waiting time
        if every_seconds:
            if every_seconds > loop_duration_in_seconds:
                wait_time = every_seconds - loop_duration_in_seconds
                time.sleep(wait_time)
                log.info('every_seconds is {}, remaining time is {}. Sleeping ... '.format(every_seconds, wait_time))
            else:
                log.warning('Loop execution time exceeded every_seconds {}'.format(every_seconds))

    return ret_list

def _maple_loop_helper(self,
                       steps,
                       testbed,
                       section,
                       name,
                       actions=None,
                       section_=None):
    """ Maple loop
        helloworld_loop_simple:
        teststep_control: continue-on-failure    
        test-steps:       
            step-1:
                loop: |
                    {
                        "package":"maple.plugins.user.LoopPlugins",
                        "method":"simpleloop",
                        "options":[
                            {"total_iterations": "2"}
                        ]
                    }
                confirm:
                    devices:
                        N93_3:
                            rule-1:
                                type: cli
                                commands: |
                                    show XX(vrf_name)XX 
                                match: | 
                                    a
    ==========================================================
    # blitz loop

    helloworld_loop_simple:
    source:
      pkg: genie.libs.sdk
      class: triggers.blitz.blitz.Blitz
        test_sections:
        - step-1:
          - loop:
              maple: true
              section: "{\n    \"package\":\"maple.plugins.user.LoopPlugins\",\n    \"method\"\
                :\"simpleloop\",\n    \"options\":[\n        {\"total_iterations\": \"2\"\
                }\n    ]\n}"
              actions:
              - execute:
                  device: N93_3
                  command: show %VARIABLES{vrf_name}
                  save:
                  - variable_name: rule-1_match_unmatch
                maple_search:
                  search_string: '%VARIABLES{rule-1_match_unmatch}'
                  device: N93_3
                  include:
                  - a
    """

    # looping using maple codes over actions
    while True:

        returned_val = _maple_loop_configure(self, testbed, section_)

        # if false would not loop
        loop_continue = returned_val['loop_continue']
        if loop_continue:
            list(_loop_action_parser(self, steps, testbed, section, actions))
        else:
            break

def _loop_action_parser(self, steps, testbed, section, actions, loop_until=None):

    # parsing the actions in loop and passing the action keyword args to the self.dispatcher
    for action_item in actions:
        for action, action_kwargs in action_item.items():

            if 'device' in action_kwargs:

                # if the device instance is already connected, put the device.name in the kwargs as device
                if not isinstance(action_kwargs['device'],
                                  str) and action_kwargs['device'].connected:
                    action_kwargs['device'] = action_kwargs['device'].name

                # for possible change of device name in case the device name is %VARIABLES{<var_name>}
                # device name should be replaced
                elif action_kwargs['device'] not in testbed.devices:
                    action_kwargs.update({'self': self})
                    action_kwargs = get_variable(**action_kwargs)
                    action_kwargs.pop('self')

            if loop_until:
                steps = Steps()

            kwargs = {
                'steps': steps,
                'testbed': testbed,
                'section': section,
                'data': [{
                    action: action_kwargs
                }]
            }

            # getting the output of the action
            yield self.dispatcher(**kwargs)



def _maple_loop_configure(self, testbed, section_):

    objects = {}
    saved_vars = self.parameters.get('save_variable_name', {})

    # section content that be used in maple code
    section_ = json.loads(section_, object_pairs_hook=OrderedDict)

    # package to call in section code
    package = section_.pop('package', None)

    # method to call in maple code
    method = section_.pop('method', None)

    # other inputs to the maple plugins method
    objects.update({
        'testbed': testbed,
        'matchObjs': saved_vars,
        'section': section_
    })
    for option in section_['options']:
        objects.update(option)

    # if no method specified, raise exception
    if not method:
        raise Exception('No method was provided to call')

    # Import the package
    if package:
        package = importlib.import_module(package.replace('maple.', ''))
    else:
        package = importlib.import_module('plugins.user.LoopPlugins')

    if not hasattr(package, method):
        raise Exception('No valid method or plugin package was provided.')

    # calling the method
    ret_value = getattr(package, method)(objects)

    # saving the variables that had been saved in the maple code
    if 'matchObjs' in ret_value:
        for key, val in ret_value['matchObjs'].items():
            save_variable(self, key, val)

    return ret_value