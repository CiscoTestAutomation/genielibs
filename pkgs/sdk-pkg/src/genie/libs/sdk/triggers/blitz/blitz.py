import logging
from copy import deepcopy
from datetime import datetime

# from genie
from genie.harness.base import Trigger
from genie.harness.discovery import copy_func

#ats
from pyats.easypy import runtime

# from pyats
from pyats import aetest
from pyats.log.utils import banner
from pyats.aetest.base import Source
from pyats.aetest.parameters import ParameterDict
from pyats.aetest.loop import loopable, get_iterations
from pyats.results import Passed, Failed, Errored, Skipped,\
                          Aborted, Passx, Blocked

from .actions import actions
from .blitz_loop import loop
from .blitz_parallel import parallel
from .blitz_control import blitz_control, control
from .markup import get_variable, apply_dictionary_filter, apply_regex_filter, save_variable

log = logging.getLogger(__name__)


class Blitz(Trigger):
    '''Apply some configuration, validate some keys and remove configuration'''
    def __iter__(self, *args, **kwargs):

        for section in self._discover():
            if loopable(section):
                for iteration in get_iterations(section):
                    new_section = section.__testcls__(
                        section,
                        uid=iteration.uid,
                        parameters=iteration.parameters,
                        parent=self)
                    yield new_section
            else:
                new_section = section.__testcls__(section, parent=self)
                yield new_section

    def _discover(self):
        # filter decorated aetest methods from helper methods
        aetest_methods = {}
        for item in dir(self):
            if hasattr(getattr(self, item), '__testcls__'):
                aetest_methods.update({item: getattr(self, item)})

        used_uids = []
        loaded_sections = []
        for sections in self.parameters.get('test_sections', {}):
            for section_name, section_values in sections.items():
                # Attempt to find existing method with same name as section_name
                method = aetest_methods.get(section_name)
                if not method:
                    # The function doesn't exist
                    # Generate the test automatically
                    if section_name.startswith('setup_'):
                        # Load the setup one
                        method = setup_section
                    elif section_name.startswith('cleanup_'):
                        # Load the cleanup one
                        method = cleanup_section
                    else:
                        # Default is test
                        method = test_section

                func = copy_func(method)
                func.uid = section_name
                iteration = 1
                while func.uid in used_uids:
                    func.uid = '{}.{}'.format(func.uid, iteration)
                    iteration += 1

                func.parameters = ParameterDict()
                func.parameters['data'] = deepcopy(section_values)
                func.source = Source(self, method.__class__)

                new_method = func.__get__(self, func.__testcls__)
                loaded_sections.append(new_method)
                used_uids.append(new_method.uid)

        return loaded_sections

    def dispatcher(self, steps, testbed, section, data, name='', **kwargs):

        ret_dict = {}
        section_continue = True
        data = deepcopy(data)
        if not data:
            log.info('Nothing to execute, ending section')
            return

        for action_item in data:

            if not action_item or not isinstance(action_item, dict):
                raise Exception("{} is an invalid input".format(str(action_item)))

            if 'run_condition' in action_item:
                ret_dict = control(self, steps, testbed, section, name,
                                   action_item['run_condition'])
                continue

            if 'loop' in action_item:
                ret_dict = loop(self, steps, testbed, section, name,
                                action_item['loop'])
                continue

            if 'parallel' in action_item:
                ret_dict = parallel(self, steps, testbed, section, name,
                                    action_item['parallel'])
                continue
            for action, kwargs in action_item.items():

                if not kwargs and not isinstance(kwargs, bool):
                    raise Exception(
                        'No data was provided for {a}'.format(a=action))

                # Checking the section continue to see if section should not continue upon not passing
                if 'continue' in action:
                    if isinstance(kwargs, bool):
                        section_continue = kwargs
                    else:
                        raise Exception(
                            'continue keyword can only be of type of boolean (True/False)'
                        )
                    continue

                # adding the section description
                if 'description' in action:
                    section.description = kwargs
                    continue

                # This is the run condition for maple
                # checks if the condition provided by maple is met
                # if so apply the function whether, pass, fail, abort etc
                if 'section_control' in action:
                    if blitz_control(self, kwargs['if'],
                                     'if') and kwargs['function'] != 'run':
                        getattr(section,
                                kwargs['function'])('Section condition result')
                    continue

                # Giving action aliases
                action_alias = kwargs.get('alias')
                # Giving user ability to change step message
                custom_msg = kwargs.pop('custom_start_step_message', None)

                if custom_msg:
                    step_msg= custom_msg
                    log.info('The action is: {a}'.format(a=action))
                else:
                    step_msg = "Starting action {a}".format(
                        a=action_alias if action_alias else action)

                if 'device' in kwargs:
                    try:
                        # check if device object, or not
                        if hasattr(kwargs['device'], 'name'):
                            kwargs['device'] = kwargs['device'].name
                        device = testbed.devices[kwargs['device']]
                    except KeyError:
                        raise Exception("Could not find the device '{d}' "
                                        "which was provided in the "
                                        "action".format(d=kwargs['device']))
                    if not custom_msg:
                        step_msg += " on device '{d}'".format(d=device.name)
                    else:
                        log.info('Device: {d}'.format(d=device.name))

                    # Provide device object
                    kwargs['device'] = device
                    # adding the device name to return dictionary
                    ret_dict['device'] = device.name
                    # saving the device.name for the cycle that action exist
                    save_variable(self, 'device.name', device.name)

                else:
                    # in cases that no device is defined
                    ret_dict['device'] = None

                # adding the step description
                description = kwargs.pop('description', '')
                # check if user wants the testcase to stop after a failure or to continue
                continue_ = kwargs.pop('continue', True)
                ret_dict['continue_'] = continue_

                save_variable(self, 'section', section)
                save_variable(self, 'runtime', runtime)
                save_variable(self, 'testscript.name', self.uid.split('.')[0])
                save_variable(self, 'task.id', runtime.tasks._tasks[len(runtime.tasks._tasks) -1].taskid)

                with steps.start(step_msg,
                                 continue_=continue_,
                                 description=description) as step:

                    # Checking a condition before running an action and applying proper function if necessary
                    if 'run_condition' in kwargs:
                        run_condition = kwargs.pop('run_condition')
                        if run_condition['if']:
                            if action_alias:
                                save_variable(self, action_alias,
                                              run_condition['function'])

                            ret_dict.update({
                                'description':
                                description,
                                'action':
                                action,
                                'alias':
                                action_alias,
                                'step_result':
                                run_condition['function']
                            })
                            getattr(step, run_condition['function'])(
                                '{f} the action because of the condition is met'
                                .format(f=run_condition['function']))

                    if 'banner' in kwargs:
                        log.info(banner(kwargs['banner']))
                        del kwargs['banner']

                    # By default the testcase would continue after a failure
                    # if user sets continue to false though it would stop
                    kwargs['continue_'] = continue_

                    # The actions were not added as a bounded method
                    # so providing the self
                    kwargs['self'] = self

                    # Checking to replace variables and get those arguments
                    kwargs = get_variable(**kwargs)
                    save = kwargs.pop('save', [])

                    # Updating steps to be newly created step
                    kwargs['steps'] = step

                    # section/name is added to kwargs for extra decorator
                    kwargs['section'] = section
                    kwargs['name'] = name

                    if action in actions:
                        # Call the action with all the arguments
                        action_output = actions[action](**kwargs)
                    else:
                        # Call custom action
                        _self = kwargs.pop('self')

                        try:
                            action_output = getattr(self, action)(**kwargs)
                        except AttributeError:
                            raise Exception(
                                "'{action}' is not a valid action. Actions should be one of {actions} "
                                "or it should be a custom action.".format(action=action, actions=list(actions.keys())))

                        kwargs['self'] = _self

                    # step.result will be stored in action_alias for future use
                    if action_alias:
                        save_variable(self, action_alias, step.result)


                    # saving actions and outputs and their results in vars
                    # storing all the necessary return values in a dict to be saved later in reporting parallel actions
                    ret_dict.update({'action': action,
                                     'description': description,
                                     'step_result': step.result,
                                     'alias': action_alias,
                                     'saved_vars': {}})

                    # filtering and saving process, ability of saving multiple vars
                    for item in save:

                        # Filtering the action output and saving the output
                        # Saving the variable in self.parameters
                        filters = item.get('filter')
                        save_dict = {}

                        # specify regex true if want to apply regex to an action execute output and extract values
                        if item.get('regex'):
                            output = apply_regex_filter(self,
                                                        action_output,
                                                        filters=filters)
                            save_dict = output

                        # saving non regex variables, using usual save_variable
                        else:
                            save_variable_name = item.get('variable_name')
                            output = apply_dictionary_filter(self,
                                                             action_output,
                                                             filters=filters)
                            save_dict.update({save_variable_name: output})

                        for save_variable_name, output in save_dict.items():
                            save_variable(self, save_variable_name, output,
                                          item.get('append'),
                                          item.get('append_in_list'))

                        if filters:
                            log.info(
                                'Applied filter: {} to the action {} output'.
                                format(filters, action))
                            ret_dict.update({'filters': filters})
                            # updating the return dictionary with the saved value
                        ret_dict['saved_vars'].update(save_dict)

        # Storing section results
        save_variable(self, section.uid, str(section.result))
        # strictly because of use in maple
        save_variable(self,
                      self.uid.split('.')[0] + '.' + section.uid,
                      str(section.result))
            

        # if continue == false ...
        if not section_continue and section.result != Passed:
            section.failed(
                'Section results is NOT passed, Stopping the testcase',
                goto=['exit'])

        return ret_dict


@aetest.setup
def setup_section(self, steps, testbed, section=None, data=None):
    return self.dispatcher(steps, testbed, section, data)


@aetest.test
def test_section(self, steps, testbed, section=None, data=None):
    return self.dispatcher(steps, testbed, section, data)


@aetest.cleanup
def cleanup_section(self, steps, testbed, section=None, data=None):
    return self.dispatcher(steps, testbed, section, data)