import logging

from .markup import get_variable

from pyats.async_ import pcall
from .advanced_actions_helper import callback_blitz_dispatcher_gen,\
                                     blitz_control, \
                                     _run_condition_with_optional_func, \
                                     _check_user_input_error, \
                                     _loop_dispatcher, \
                                     _parallel

from pyats.results import Passed, Failed, Errored, Skipped,\
                          Aborted, Passx, Blocked                                

log = logging.getLogger()


def loop(self, steps, testbed, section, name, action_item):
    """
    Running actions in loop
    """
    ret_list = []
    loop_return_items = []

    if action_item.get('custom_substep_message'):
        msg = action_item.pop('custom_substep_message')

        kwargs = {'msg': msg, 'self': self, 'section': section}

        replaced_kwargs = get_variable(**kwargs)
        msg = replaced_kwargs['msg']

    elif action_item.get('loop_until'):
        msg = "Executing actions in a loop with loop_until: '{l}'"\
              .format(l=action_item['loop_until'])

    elif action_item.get('parallel'):
        msg = "Executing actions in the loop concurrently"
    else:
        msg = 'Executing actions in a loop'

    # check if the step logs needs to be suppressed
    suppress_logs = bool(self.parameters.get('suppress_logs'))

    # Since loop shows up in action level, it has to be treated as an action and step
    with steps.start(msg, continue_=True, suppress_logs=suppress_logs) as step:

        # check if user has made any input error and error out the step
        _check_user_input_error(step, action_item, loop_return_items)

        # check if loop is blitz or maple loop and then dispatch
        # to proper function
        func, action_item = _loop_dispatcher(self, step, testbed, section,
                                             action_item, ret_list, name)

        loop_return_items = func(**action_item)

        # Each loop is treated as one action.
        # Actions within a loop are considered as substep.
        # except for loop_until that are one action
        # with no substep
        # if loop_until is set to passed/failed, then the goal is to
        # loop until pass/fail
        if action_item.get('loop_until'):

            prev_loop_result = loop_return_items[-1]['step_result']

            loop_until_msg = "The loop_until was set to '{0}'"\
                             " and last attempted action in the"\
                             " loop did not have the same result."\
                             " Hence the loop_output is set to {1}"

            if action_item.get('loop_until').lower() == str(prev_loop_result):
                loop_until_step_result = 'passed'
            else:
                loop_until_step_result = 'failed'

            getattr(step, loop_until_step_result)(
                    loop_until_msg.\
                    format(action_item.get('loop_until'), loop_until_step_result))

    return {
        'action': 'loop',
        'step_result': step.result,
        'substeps':
        loop_return_items if not action_item.get('loop_until') else [],
        'advanced_action': True,
        'loop_until': action_item.get('loop_until')
    }


def parallel(self, steps, testbed, section, name, data):
    """
    When called run all the actions
    below the keyword parallel concurrently
    """
    pcall_payloads = []
    pcall_returns = []

    # check if the step logs needs to be suppressed
    suppress_logs = bool(self.parameters.get('suppress_logs'))

    with steps.start('Executing actions in parallel', continue_=True, suppress_logs=suppress_logs) as steps:

        kwargs = {
            'self': self,
            'steps': steps,
            'testbed': testbed,
            'section': section,
            'data': data,
            'parallel': True
        }

        # call generator and store all action kwargs into pcall_payload
        for action_kwargs in callback_blitz_dispatcher_gen(**kwargs):
            pcall_payloads.append(action_kwargs)

        # Run actions in parallel
        pcall_returns = pcall(self.dispatcher, ikwargs=pcall_payloads)

        _parallel_results = _parallel(self, section, pcall_returns, steps)

        # Check for `continue: False` and go to exit if a section doesn't pass
        continues = [entry.get('continue_') for entry in pcall_returns]
        if not all(continues) and section.result != Passed:
                section.failed(
                    'Parallel section results is NOT passed, Stopping the testcase',
                    goto=['exit'])

        return _parallel_results


def run_condition(self, steps, testbed, section, name, action_item):
    """
    Running actions with regards to a condition
    """
    ret_list = []

    # check if the logs needs to be suppressed
    suppress_logs = bool(self.parameters.get('suppress_logs', False))

    # Legacy implementation
    if isinstance(action_item, dict):

        # the if statement
        condition = action_item.get('if')
        # function to be applied if condition is met
        function = action_item.get('function')
        # actions to run or not run below run_condition
        actions = action_item.get('actions')

        # customized description of the conditional statement
        desc = action_item.get('description', '')

        condition_bool = blitz_control(self, section, condition, 'if')
        kwargs = {
            'self': self,
            'steps': steps,
            'testbed': testbed,
            'section': section,
            'name': name,
            'data': actions,
        }

        if not function:
            return _run_condition_with_optional_func(condition_bool,
                                                    condition,
                                                    kwargs,
                                                    description=desc,
                                                    suppress_logs=suppress_logs)

        msg = action_item.pop('custom_substep_message',
                            'Checking the condition {}'.format(condition))

        with steps.start(msg, continue_=True) as step:

            if condition_bool:

                getattr(step,
                        function)("{c} is equal True. The run_condition "
                                "step result is set to {f}".format(c=condition,
                                                                    f=function))

            kwargs.update({'steps': step})
            ret_list = list(callback_blitz_dispatcher_gen(**kwargs))[0]
        # if actions actually ran the output list of outputs
        # should be added to this dict to return
        # mainly useful to be unpacked in parallel

        return {
            'action': 'run_condition',
            'step_result': step.result,
            'substeps': ret_list,
            'advanced_action': True,
            'run_condition_skipped': condition_bool,
            'condition': condition
        }

    # Implementation that supports if, elif and else
    else:
        step_result = steps.result
        run_condition_skipped = False
        if_flag=False
        else_flag=False

        # Check multiple conditions have been passed
        for item in action_item:
            # To check multiple if
            if 'if' in item.keys():
                if not if_flag:
                    if_flag = True
                    continue
                else:
                    log.info(action_item)
                    raise Exception("Multple if conditions have been passed, please provide only one"\
                    " if condition")

            # To check multiple else
            if 'else' in item.keys():
                if not else_flag:
                    else_flag = True
                    continue
                else:
                    log.info(action_item)
                    raise Exception("Multiple else conditions have been passed, please provide only one"\
                    " else condition")

        # To check if atleast one if condition is passed
        if not if_flag:
            log.info(action_item)
            raise Exception("At least one if condition should be passed")

        # Implementation of if, elif, else
        for item in action_item:
            # the condition
            if 'if' in item:
                condition = item.get('if')
            elif 'elif' in item:
                condition = item.get('elif')
            else:
                condition = None

            # function to be applied if condition is met
            function = item.get('function')

            # actions to run or not run below run_condition
            actions = item.get('actions')

            # customized description of the conditional statement
            desc = item.get('description', '')

            # To check the given condition
            if condition:
                condition_bool = blitz_control(self, section, condition, 'if')
                if not condition_bool:
                    run_condition_skipped = True
                    continue

            kwargs = {
                'self': self,
                'steps': steps,
                'testbed': testbed,
                'section': section,
                'name': name,
                'data': actions,
            }

            # Only executes when condition is True
            if not function and condition_bool:
                return _run_condition_with_optional_func(condition_bool,
                                                        condition,
                                                        kwargs,
                                                        description=desc,
                                                        suppress_logs=suppress_logs,)

            # When condition is True and function
            if function and condition_bool:
                msg = item.pop('custom_substep_message',
                            'Checking the condition {}'.format(condition))

                with steps.start(msg, continue_=True) as step:
                    if condition_bool:
                        getattr(step,
                                function)("{c} is equal True. The run_condition "
                                        "step result is set to {f}".format(c=condition,
                                                                            f=function))
                    kwargs.update({'steps': step})
                    ret_list = list(callback_blitz_dispatcher_gen(**kwargs))[0]
                step_result = step.result

            # To execute actions under else condition
            if 'else' in item.keys():
                ret_list = list(callback_blitz_dispatcher_gen(**kwargs))[0]

            # To break when condition passes
            if condition_bool:
                break

        # if actions actually ran the output list of outputs
        # should be added to this dict to return
        # mainly useful to be unpacked in parallel
        return {
            'action': 'run_condition',
            'step_result': step_result,
            'substeps': ret_list,
            'advanced_action': True,
            'run_condition_skipped': run_condition_skipped,
            'condition': condition
        }

advanced_actions = {
    'parallel': parallel,
    'loop': loop,
    'run_condition': run_condition
}
