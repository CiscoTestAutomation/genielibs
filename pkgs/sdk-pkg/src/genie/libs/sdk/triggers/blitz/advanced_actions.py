
import logging

from .markup import get_variable
from .markup import save_variable

from pyats.async_ import pcall
from .advanced_actions_helper import callback_blitz_dispatcher_gen,\
                                     blitz_control, \
                                     _run_condition_with_optional_func, \
                                     _check_user_input_error, \
                                     _loop_dispatcher, \
                                     _parallel

log = logging.getLogger()



def loop(self, steps, testbed, section, name, action_item):
    """
    Running actions in loop
    """
    ret_list = []
    loop_return_items = []

    if action_item.get('custom_substep_message'):
        msg = action_item.pop('custom_substep_message')

    elif action_item.get('loop_until'):
        msg = "Executing actions in a loop with loop_until: '{l}'"\
              .format(l=action_item['loop_until'])

    elif action_item.get('parallel'):
        msg = "Executing actions in the loop concurrently"
    else:
        msg = 'Executing actions in a loop'

    # Since loop shows up in action level, it has to be treated as an action and step
    with steps.start(msg, continue_=True) as step:

        # check if user has made any input error and error out the step
        _check_user_input_error(step, action_item, loop_return_items)

        # check if loop is blitz or maple loop and then dispatch
        # to proper function
        func, action_item = _loop_dispatcher(self,
                                             step,
                                             testbed,
                                             section,
                                             action_item,
                                             ret_list,
                                             name)

        loop_return_items = func(**action_item)

        # Each loop is treated as one action.
        # Actions within a loop are considered as substep.
        # except for loop_until that are one action
        # with no substep
        # if loop_until is set to passed/failed, then the goal is to
        # loop until pass/fail
        if action_item.get('loop_until'):

            prev_loop_result  = loop_return_items[-1]['step_result']

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

    return {'action': 'loop',
            'step_result': step.result,
            'substeps': loop_return_items if not action_item.get('loop_until') else [],
            'advanced_action': True,
            'loop_until': action_item.get('loop_until')}

def parallel(self, steps, testbed, section, name, data):
    """
    When called run all the actions
    below the keyword parallel concurrently
    """
    pcall_payloads = []
    pcall_returns = []
    with steps.start('Executing actions in parallel', continue_=True) as steps:

        kwargs = {'self': self,
          'steps': steps,
          'testbed': testbed,
          'section': section,
          'data': data,
          'parallel': True
         }

        # call generator and store all action kwargs into pcall_payload
        for action_kwargs in callback_blitz_dispatcher_gen(**kwargs):
            pcall_payloads.append(action_kwargs)

        pcall_returns = pcall(self.dispatcher, ikwargs=pcall_payloads)
        return _parallel(self, section, pcall_returns, steps)

def run_condition(self, steps, testbed, section, name, action_item):
    """
    Running actions with regards to a condition
    """
    ret_list = []
    # the if statement
    condition = action_item.get('if')
    # function to be applied if condition is met
    function = action_item.get('function')
    # actions to run or not run below run_condition
    actions = action_item.get('actions')

    # customized description of the conditional statement
    desc = action_item.get('description', '')

    condition_bool = blitz_control(self, section, condition, 'if')
    kwargs = {'self': self,
              'steps': steps,
              'testbed': testbed,
              'section': section,
              'data': actions,
            }

    if not function:
        return _run_condition_with_optional_func(condition_bool,
                                                 condition,
                                                 kwargs,
                                                 description=desc)

    msg = action_item.pop('custom_substep_message',
                          'Checking the condition {}'.format(condition))

    with steps.start(msg, continue_=True) as step:

        if condition_bool:

            getattr(step, function)("{c} is equal True. The run_condition "
                                    "step result is set to {f}"
                                    .format(c=condition, f=function))

        kwargs.update({'steps': step})
        ret_list = list(callback_blitz_dispatcher_gen(**kwargs))[0]
    # if actions actually ran the output list of outputs
    # should be added to this dict to return
    # mainly useful to be unpacked in parallel

    return {'action': 'run_condition',
            'step_result': step.result,
            'substeps': ret_list,
            'advanced_action': True,
            'run_condition_skipped': condition_bool,
            'condition': condition
           }

advanced_actions = {
    'parallel': parallel,
    'loop': loop,
    'run_condition': run_condition
}
