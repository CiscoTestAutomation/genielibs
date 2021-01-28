import ast
import json
import time
import logging
import importlib

from datetime import datetime
from collections import OrderedDict
from genie.utils.timeout import Timeout

from .markup import get_variable, save_variable
from .actions_helper import _condition_validator

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed, Errored, Skipped,\
                          Aborted, Passx, Blocked

log = logging.getLogger()


def callback_blitz_dispatcher_gen(self,
                                  steps,
                                  testbed,
                                  section,
                                  data,
                                  loop_until=None,
                                  parallel=None):
    """
    calling back the blitz dispatcher to run actions wrapped
    under advanced actions
    """

    # parsing the actions in loop and passing the action
    # keyword args to the self.dispatcher
    for action_item in data:
        for action, action_kwargs in action_item.items():

            if loop_until or parallel:
                steps = Steps()

            if 'device' in action_kwargs:

                # if the device instance is already connected,
                # put the device.name in the kwargs as device
                if not isinstance(action_kwargs['device'],
                                  str) and action_kwargs['device'].connected:
                    action_kwargs['device'] = action_kwargs['device'].name

                # for possible change of device name in case the device name is %VARIABLES{<var_name>}
                # device name should be replaced
                elif action_kwargs['device'] not in testbed.devices:
                    action_kwargs.update({'self': self})
                    action_kwargs = get_variable(**action_kwargs)
                    action_kwargs.pop('self')

            kwargs = {
                'steps': steps,
                'testbed': testbed,
                'section': section,
                'data': [{
                    action: action_kwargs
                }]
            }

            if parallel:
                yield kwargs
            else:
                # getting the output of the action
                yield self.dispatcher(**kwargs)

def _loop_dispatcher(self, steps, testbed, section, action_item, ret_list, name):
    """checks if blitz loop or maple loop and update the keyword arguments
       to these function"""

    actions = action_item.pop('actions')

    # determine whether it is a range or an iterator value(list/dict) as input
    iterator_item = _loop_iterator_item_update(action_item)

    # values needs to be popped so markup vars wont get
    # replaced by get_variable()
    until = action_item.pop('until', None)
    do_until = action_item.pop('do_until', None)

    # Sending to get_variable to replace saved items.
    action_item.update({'self': self})
    action_item = get_variable(**action_item)
    section_ = action_item.pop('section', None)

    # update the kwargs
    action_item.update({'steps': steps,
                        'testbed': testbed,
                        'section': section,
                        'name': name,
                        'actions': actions})

    if not action_item.get('maple'):
        action_item.update({'ret_list': ret_list,
                            'iterator_item':iterator_item,
                            'until': until,
                            'do_until': do_until})

        func = _loop_iterator
    else:
        action_item.update({'section_': section_})
        func = _maple_loop_iterator

    return func, action_item

def _loop_iterator_item_update(action_item):

    if 'range' in action_item:

        range_ = action_item.pop('range')
        tree = ast.parse("f({})".format(range_))
        funccall = tree.body[0].value
        args = [ast.literal_eval(arg) for arg in funccall.args]
        return range(*args)

    iterator_item = action_item.pop('value', None)
    return iterator_item

def _loop_iterator(self,
                 steps,
                 testbed,
                 section,
                 name,
                 ret_list,
                 loop_variable_name=None,
                 loop_until=False,
                 max_time=None,
                 check_interval=None,
                 until=None,
                 do_until=None,
                 actions=None,
                 iterator_item=None,
                 every_seconds=None,
                 **kwargs):
    """actually iterate over the actions under loop and call them"""

    # TODO cant save vars in loop, enhancement needed

    # timeout if until or do_until or loop_until are looping through infinity
    timeout = Timeout(max_time, check_interval)

    iterator_len = None
    iterator_index = 0
    iterator_len = len(iterator_item) if iterator_item else None

    # until condition would be sent to blitz_control
    # in order to evaluate and see if the condition is true or not
    # loop wont start if the condition is true with step as passed
    until_condition = False
    if until and blitz_control(self, until, 'until'):
        until_condition = True
        log.info(
                'Until condition is met. Loop terminated')

    while not until_condition:

        # capturing the start time of the action to calculate
        # the duration of the action
        loop_start_time =  datetime.now()
        log.debug('loop start time: {}'.format(str(loop_start_time)))

        if _check_pre_iteration(iterator_len,
                                iterator_index,
                                max_time,
                                timeout):
            break

        # assign each item in an iterable_item to a variable
        # to be used later on within the actions
        # the loop_variable_name should exist in the testcase
        _save_iterator_items(self, loop_variable_name, iterator_item, iterator_index)

        # running all the actions and adding the outputs of those actions to return list
        if actions:
            kwargs = {'self': self,
                      'steps': steps,
                      'testbed': testbed,
                      'section': section,
                      'data': actions,
                      'loop_until': loop_until
                     }

            ret_list.extend(list(callback_blitz_dispatcher_gen(**kwargs)))

        # check if loop_until is true and get the item that meet the loop_until value
        loop_until_last_index = _check_loop_until(self, ret_list, loop_until)
        if loop_until_last_index is not None:
            ret_list = ret_list[loop_until_last_index: loop_until_last_index+1]

        # increase the iterator_index until it hits the iterator_len
        # it terminates the iteration when reaches the end of iterator
        if iterator_len:
            iterator_index += 1

        until_condition = _check_post_iteration(self,
                                                until,
                                                do_until,
                                                loop_until_last_index)

        _report_every_seconds(loop_start_time, every_seconds)

    return ret_list

def _save_iterator_items(self, loop_variable_name, iterator_item, iterator_index):
    """ Save each item of a loop into a variable before running the actions
        E.g: value: [get_logger, get_mtu_size]
             loop_variable_name: func_name
             action:
                - api:
                    function: %VARIABLES{func_name}
    """

    if loop_variable_name and iterator_item:

        # parse through dictionary
        if isinstance(iterator_item, dict):
            item_dict_key = list(iterator_item.keys())[iterator_index]
            value_ = {item_dict_key: iterator_item[item_dict_key]}

        # parse through list
        else:
            value_ = iterator_item[iterator_index]
        save_variable(self, loop_variable_name, value_)

def _check_pre_iteration(iterator_len, iterator_index, max_time, timeout):
    """
        check pre each iteration, if timeout is reached or
        or the iterator item (list/dict) reached its end
    """
    # keys to check if loop is timing out or it stopped iterating
    keys = [(iterator_len and iterator_index == iterator_len,
            'The loop finished because the iterable item is parsed to the end'),
            (max_time and not timeout.iterate(),
            'Timeout is reached, going out of this loop')]

    for key in keys:
        if key[0]:
            log.info(key[1])
            return True

    return False

def _check_post_iteration(self, until, do_until, loop_until_last_index):
    """check post each iteration if, until, do_until
       or loop_until condition is met"""

    until_condition = False
    if loop_until_last_index is not None:
        return True
    # if terminating condition is set with key do_until/until
    # if condition met update the flag to terminate the loop
    if until:
        until_condition = blitz_control(self, until, 'until')
        until_stmnt = until
    elif do_until:
        until_condition = blitz_control(self, do_until, 'do_until')
        until_stmnt = do_until

    if until_condition:
        log.info(
                'Until condition "{u}" equal True. Loop terminated'.format(u=until_stmnt))
        return True

    return False

def _report_every_seconds(loop_start_time, every_seconds):
    """reporting every_seconds"""
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
            log.info('every_seconds is {}, remaining time is {}. Sleeping ... '
                     .format(every_seconds, wait_time))
        else:
            log.warning('Loop execution time exceeded every_seconds {}'
                        .format(every_seconds))

# Check the name
def _check_loop_until(self, ret_list, loop_until=None):
    """
        checks if loop until and returns the index of the action
        that its results matches the loop_until values (passed/failed)
    """

    if not loop_until:
        return None
    # Considering that multiple actions might be looped over this
    # looks for the first pass/fail of the actions and check if it
    # equals loop_until then breaks the loop
    for index_, action_output in enumerate(ret_list):
        if str(ret_list[index_]['step_result']) == loop_until.lower():
            return index_

def _check_user_input_error(step, action_item, loop_return_items):
    """
    possible user input errors:
    1 - cannot have range and a list/dict together (only one iterable item)
    2 - cannot have until and do_until
    3 - must have actions
    4 - needs at least one iterable or terminating condition
    """

    keys = [(not 'actions' in action_item,
            "No actions was provided to be looped over."),
            ('range' in action_item and 'value' in action_item,
            'Only one iterable item per each loop is allowed.'),
            ('until' in action_item and 'do_until' in action_item,
            'You only can have one terminating condition per loop.'),
            ((not 'range' in action_item and not 'value' in action_item) and
              not 'until' in action_item and not 'do_until' in action_item and
              not 'loop_until' in action_item and not 'maple' in action_item,
            'At least one iterable item or terminating condition should be in the loop')]

    for key in keys:
        if key[0]:
            loop_return_items.append({'action': 'loop',
                                      'step_result': 'errored',
                                      'device': None})
            step.errored(key[1])


def blitz_control(self, condition, key):
    """
        check if the condition provided is True or false
    """
    condition_dict = {}
    condition_dict.update({'self': self, key: condition})

    # replace all the %VARIABLES{name}
    condition_dict = get_variable(**condition_dict)
    # function that validates conditions
    return _condition_validator(condition_dict[key])

def _parallel(self, pcall_returns, step):
    """
    Each action return is a dictionary containing the following:
        * Action name, possible saved_variable, action results,
        * Device name that action was running on
    These value would be lost when the child processor that executes
    the action end the process. This function grabs all the actions outputs
    and returns them to the main processor.
    """

    for each_return in pcall_returns:

        # need to iterate through loop and control outputs
        # to adjust the log accordingly
        if 'advanced_action' in each_return and each_return['substeps']:
            _pcall_return_trim(self, each_return, step, each_return['action'])
            continue

        # save action alias
        if each_return.get('alias'):
            save_variable(self, each_return['alias'],
                          str(each_return['step_result']))

        if each_return.get('saved_vars'):
            for saved_var_name, saved_var_data in each_return.get(
                    'saved_vars').items():
                save_variable(self, saved_var_name, saved_var_data)

        # log the filters that are applied
        if each_return.get('filters'):
            log.info('Applied filter: {} to the action {} output'.format(
                each_return['filters'], each_return['action']))

        msg = _check_parallel_msg(self, each_return)

        with step.start(msg,
                        continue_=True,
                        description=each_return.get('description')) as report_step:
            log.info('Check above for detailed action report')
            getattr(report_step, str(each_return['step_result']))()

    return {'action': 'parallel', 'step_result': step.result}

def _pcall_return_trim(self, each_return, steps, trim_value):
    """
       recursively check for actions that are ran under run_condition/loop
       in parallel
    """

    if trim_value == 'run_condition':
        msg = 'Condition {c} is not met. Running actions in parallel'\
                .format(c=each_return['condition'])
    elif trim_value == 'loop':
        msg = 'Executing actions in loop in parallel'

    with steps.start(msg, continue_=True) as step:
        each_return = each_return['substeps']
        _parallel(self, each_return, step)

def _check_parallel_msg(self, each_return):
    """Set the proper message for actions ran under parallel"""

    if each_return.get('device'):

        msg = 'Executed action {a} on {d} in parallel'.format(
            a=each_return['action'], d=each_return['device'])
    elif each_return.get('run_condition_skipped'):

        msg = "Condition {c} is met and the step result is {r}"\
                .format(c=each_return['condition'],
                        r=str(each_return['step_result']))
    elif each_return.get('loop_until'):

        msg = "Executed actions in loop with loop_until in parallel"
    else:

        msg = 'Executed action {a} in parallel'.format(
                                a=each_return['action'])
    return msg


def _maple_loop_iterator(self,
                         steps,
                         testbed,
                         section,
                         name,
                         actions=None,
                         section_=None,
                         **kwargs):
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
            list(callback_blitz_dispatcher_gen(self, steps, testbed, section, actions))
        else:
            break

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
