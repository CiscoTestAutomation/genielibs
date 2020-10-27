import logging

from .markup import get_variable
from .markup import save_variable

from pyats.async_ import pcall
from pyats.aetest.steps import Steps

log = logging.getLogger()


def parallel(self, steps, testbed, section, name, data):
    # When called run all the actions
    # below the keyword parallel concurrently
    pcall_payloads = []
    pcall_returns = []
    with steps.start('Executing actions in parallel', continue_=True) as steps:

        # If parallel keyword is insdie a condition block.
        # We might want to apply a function if the condition met
        # this if condition does that
        if 'parallel_conditioned' in data[0]:

            run_condition = data[0]['parallel_conditioned']
            if run_condition['if']:
                getattr(
                    steps, run_condition['function']
                )('Condition is met the parallel block step result is set to {f}'
                  .format(run_condition['function']))
            else:
                data.pop(0)

        for action_item in data:
            for action, action_kwargs in action_item.items():

                # for future use - Enhancement needed in pyATS
                # with steps.start("Implementing action '{a}' in parallel".format(a=actions)) as step:
                # on parallel it is not possible to set continue to False and benefit from that feature
                step = Steps()

                # Making sure that if a device is connected just the name of the device gets passed by to dispatcher
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
                    'name': name,
                    'data': [{
                        action: action_kwargs
                    }]
                }
                pcall_payloads.append(kwargs)

        pcall_returns = pcall(self.dispatcher, ikwargs=pcall_payloads)
        return _parallel(self, pcall_returns, steps)

def _parallel(self, pcall_returns, step):

    # Each action return is a dictionary containing the action name, possible saved_variable
    # Action results, and device name that action is being implemented on
    # These value would be lost when the child processor that executes the action end the process.
    # It is being implemented this way in order to add these values to the main processor.
    for each_return in pcall_returns:

        # need to iterate through loop and control outputs to adjust the log accordingly
        if 'loop_output' in each_return:
            pcall_return_trim(self, each_return, step, 'loop_output')
            continue
        if 'control_output' in each_return:
            pcall_return_trim(self, each_return, step, 'control_output')
            continue

        if each_return.get('alias'):
            save_variable(self, each_return['alias'],
                          each_return['step_result'])

        if each_return.get('saved_vars'):
            for saved_var_name, saved_var_data in each_return.get(
                    'saved_vars').items():
                save_variable(self, saved_var_name, saved_var_data)

        if each_return.get('filters'):
            log.info('Applied filter: {} to the action {} output'.format(
                each_return['filters'], each_return['action']))

        if each_return.get('loop_conditioned'):
            getattr(step, each_return['loop_conditioned'])()

        if each_return['device']:
            msg = 'Executed action {action} on {device} in parallel'.format(
                action=each_return['action'], device=each_return['device'])
        else:

            msg = 'Executed action {action} in parallel'.format(
                action=each_return['action'])
            if each_return['action'] == 'loop':
                msg = 'Executed actions in loop with loop_until in parallel'

        with step.start(msg,
                        continue_=True,
                        description=each_return['description']) as report_step:
            log.info('Check above for detailed action report')
            getattr(report_step, str(each_return['step_result']))()

    return {'action': 'parallel', 'step_result': step.result}

def pcall_return_trim(self, ret, steps, trim_value):
    
    # recursively check for actions that are running under condition in parallel
    if trim_value == 'control_output':
        with steps.start('Checking the condition in parallel',
                         continue_=True) as step:
            ret = ret['control_output']
            _parallel(self, ret, step)

    # recursively check for actions that are running under loop in parallel
    elif trim_value == 'loop_output':

            with steps.start('Executing actions in loop in parallel',
                         continue_=True) as step:
                ret = ret['loop_output']
                _parallel(self, ret, step)