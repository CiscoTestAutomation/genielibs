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
from .advanced_actions import advanced_actions
from .advanced_actions_helper import blitz_control
from .markup import get_variable, apply_regex_filter,\
                                  apply_dictionary_filter,\
                                  apply_list_filter, \
                                  save_variable

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

            # advanced actions examples, loop, run_condition, parallel
            ret_dict = self._check_advanced_actions(
                            steps, testbed, section, name, action_item)
            if ret_dict:
                continue

            for action, kwargs in action_item.items():

                # if action value is ['continue', 'description', 'section_control']
                # The value would give the script a certain functionality
                # but it is not an action and it should continue the loop
                if self._check_non_action_keywords(action, kwargs, section):
                    section_continue = section.section_continue
                    continue

                pre_step_removed_kwargs = self._pre_step_start_kwargs_update(action,
                                                                             kwargs,
                                                                             testbed,
                                                                             ret_dict,
                                                                             section)
                # Action starts.
                with steps.start(pre_step_removed_kwargs['step_msg'],
                                 continue_=pre_step_removed_kwargs['continue_'],
                                 description=pre_step_removed_kwargs['description']) as step:

                    kwargs = self._pre_action_call_kwargs_update(step,
                                                                action,
                                                                section,
                                                                name,
                                                                kwargs,
                                                                ret_dict,
                                                                pre_step_removed_kwargs)
                    save = kwargs.pop('save', [])
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
                                "or it should be a custom action.".
                                format(action=action, actions=list(actions.keys())))

                        kwargs['self'] = _self

                    # saving actions and outputs and their results in vars
                    # storing all the necessary return values in a dict to be
                    # saved later in reporting parallel actions
                    ret_dict.update({'action': action,
                                     'description': pre_step_removed_kwargs['description'],
                                     'step_result': step.result,
                                     'alias': pre_step_removed_kwargs['action_alias'],
                                     'saved_vars': {}})

                    # step.result will be stored in action_alias for future use
                    if pre_step_removed_kwargs['action_alias']:
                        save_variable(self, pre_step_removed_kwargs['action_alias'], str(step.result))
                        ret_dict['saved_vars'].update({
                            pre_step_removed_kwargs['action_alias']: str(step.result)
                            })

                    # Apply proper filter (regex filter, dq filter, list filter) on an output
                    # Then save the filtered output in the value
                    self._filter_and_save_action_output(ret_dict, save, action_output)

        # strictly because of use in maple
        save_variable(self,
                      self.uid.split('.')[0] + '.' + section.uid,
                      str(section.result))

        save_variable(self, section.uid, str(section.result))

        # if continue == false ...
        if not section_continue and section.result != Passed:
            section.failed(
                'Section results is NOT passed, Stopping the testcase',
                goto=['exit'])

        return ret_dict

    def _check_advanced_actions(self, steps, testbed, section, name, action_item):
        """Check if any advanced action is used in datafile
           such as(loop, parallel, run_condition)"""

        for func_name, advanced_action in advanced_actions.items():
            if func_name in action_item:
                args = (self, steps, testbed, section, name, action_item[func_name])
                return advanced_action(*args)

        return {}

    def _check_non_action_keywords(self, action, kwargs, section):
        """check if a section contains of description or section continue
           or section_control or anyother keyword that is specified as actions
           but is not actually an action
        """

        setattr(section, 'section_continue', True)
        if kwargs is None:
            raise Exception(
                'No data was provided for {a}'.format(a=action))

        # Checking the section continue to see if section should not continue upon not passing
        if 'continue' in action:
            if isinstance(kwargs, bool):
                section.section_continue = kwargs
            else:
                raise Exception(
                    'continue keyword can only be of type of boolean (True/False)'
                )
            return True

        # adding the section description
        if 'description' in action:
            section.description = kwargs
            return True

        # This is the run condition for maple
        # checks if the condition provided by maple is met
        # if so apply the function whether, pass, fail, abort etc
        if 'section_control' in action:
            if blitz_control(self, kwargs['if'],
                             'if') and kwargs['function'] != 'run':
                getattr(section,
                        kwargs['function'])('Section condition result')
            return True

        return False

    def _pre_step_start_kwargs_update(self,
                                      action,
                                      kwargs,
                                      testbed,
                                      ret_dict,
                                      section):
        """updating the keyword of an action arguments pre starting the step"""

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

        # check if user wants the testcase to stop after a failure or to continue
        continue_ = kwargs.pop('continue', True)
        ret_dict['continue_'] = continue_

        save_variable(self, 'section', section)
        save_variable(self, 'runtime', runtime)
        save_variable(self, 'testscript.name', self.uid.split('.')[0])
        save_variable(self, 'task.id', runtime.tasks._tasks[-1].taskid)

        return {'action_alias': action_alias,
                'step_msg': step_msg,
                'continue_': continue_,
                'description': kwargs.pop('description', '')}

    def _pre_action_call_kwargs_update(self,
                                      step,
                                      action,
                                      section,
                                      name,
                                      kwargs,
                                      ret_dict,
                                      pre_step_removed_kwargs):
        """updating keyword arguments of an action pre calling the action """

        if 'banner' in kwargs:
            log.info(banner(kwargs['banner']))
            del kwargs['banner']

        # The actions were not added as a bounded method
        # so providing the self
        kwargs['self'] = self
        # Checking to replace variables and get those arguments
        kwargs = get_variable(**kwargs)

        # updating step to the newly created step
        # section/name is added to kwargs for extra decorator
        # by default continue after a failure, specify as False if otherwise is desired
        kwargs.update({'steps': step,
                       'continue_': pre_step_removed_kwargs['continue_'],
                       'section': section,
                       'name': name})

        return kwargs

    def _filter_and_save_action_output(self, ret_dict, save, action_output):
        """
            Apply proper filter to the output based on the type of filter
            (regex, list, dictionary)
            and save the filtered output to the variable name provided
        """
        # filtering and saving process, ability of saving multiple vars
        for item in save:
            # Filtering the action output and saving the output
            # Saving the variable in self.parameters
            filter_ = item.get('filter')
            save_dict = {}

            # specify regex true if want to apply regex to an action execute
            # output and extract values
            if item.get('regex'):

                # applying regex_filter to string output
                output = apply_regex_filter(self,
                                            action_output,
                                            filters=filter_)
                save_dict = output

            # saving non regex variables, using usual save_variable
            else:
                save_variable_name = item.get('variable_name')

                # If list
                if isinstance(action_output, (list, tuple)):
                    output = apply_list_filter(self,
                                               action_output,
                                               list_index=item.get('list_index'),
                                               filters=filter_)

                # If dictionary with dq filter
                else:
                    output = apply_dictionary_filter(self,
                                                     action_output,
                                                     filters=filter_)

                save_dict.update({save_variable_name: output})

            for save_variable_name, output in save_dict.items():
                save_variable(self,
                              save_variable_name,
                              output,
                              item.get('append'),
                              item.get('append_in_list'))
            if filter_:
                log.info(
                    'Applied filter: {} to the action {} output'.
                    format(filter_, ret_dict['action']))

                ret_dict.update({'filters': filter_})

            # updating the return dictionary with the saved value
            ret_dict['saved_vars'].update(save_dict)

@aetest.setup
def setup_section(self, steps, testbed, section=None, data=None):
    return self.dispatcher(steps, testbed, section, data)

@aetest.test
def test_section(self, steps, testbed, section=None, data=None):
    return self.dispatcher(steps, testbed, section, data)

@aetest.cleanup
def cleanup_section(self, steps, testbed, section=None, data=None):
    return self.dispatcher(steps, testbed, section, data)