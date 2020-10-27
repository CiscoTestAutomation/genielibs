import logging

from .markup import get_variable
from .actions_helper import _condition_validator

log = logging.getLogger()


def control(self, steps, testbed, section, name, action_item):

    ret_list = []
    ret_dict = {}

    # the if statement
    condition = action_item.get('if')

    # function to be applied if condition is met
    function = action_item.get('function')

    # actions to run or not run below run_condition
    actions = action_item.get('actions')

    with steps.start('Checking the run_condition {}'.format(condition),
                     continue_=True) as step:

        for item in actions:
            for action, action_kwargs in item.items():

                condition_bool = blitz_control(self, condition, 'if')

                # if the goal is to check a condition on top of a parallel block
                # the condition output has to be added to parallel input
                # so it would be checked before running the parallel
                if action == 'parallel':
                    action_kwargs.insert(
                        0, {
                            'parallel_conditioned': {
                                'if': condition_bool,
                                'function': function
                            }
                        })
                else:
                    # for all the other scenarios, actions loops etc.
                    action_kwargs.update({
                        'run_condition': {
                            'if': condition_bool,
                            'function': function
                        }
                    })

                # In case of loop we need to check that device is connected
                if 'device' in action_kwargs:
                    if not isinstance(
                            action_kwargs['device'],
                            str) and action_kwargs['device'].connected:
                        action_kwargs['device'] = action_kwargs['device'].name
                    elif action_kwargs['device'] not in testbed.devices:
                        action_kwargs.update({'self': self})
                        action_kwargs = get_variable(**action_kwargs)
                        action_kwargs.pop('self')

                kwargs = {
                    'steps': step,
                    'testbed': testbed,
                    'section': section,
                    'data': [{
                        action: action_kwargs
                    }]
                }
                ret_list.append(self.dispatcher(**kwargs))

    # if actions actually ran the output list of outputs
    # should be added to this dict to return
    # mainly useful to be unpacked in parallel
    ret_dict.update({'control_output': ret_list})
    return ret_dict

def blitz_control(self, condition, key):

    condition_dict = {}
    condition_dict.update({'self': self, key: condition})

    # replace all the %VARIABLES{name}
    condition_dict = get_variable(**condition_dict)
    log.info(condition_dict)
    # function that validates conditions
    return _condition_validator(condition_dict[key])
