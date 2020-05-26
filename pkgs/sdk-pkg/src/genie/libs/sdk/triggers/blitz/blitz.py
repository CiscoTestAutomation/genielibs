import logging
from copy import deepcopy

from genie.harness.base import Trigger
from genie.harness.discovery import copy_func

from pyats import aetest
from pyats.log.utils import banner
from pyats.aetest.base import Source
from pyats.aetest.parameters import ParameterDict
from pyats.aetest.loop import loopable, get_iterations

from .actions import actions
from .actions import action_parallel
from .markup import get_variable, filter_variable, save_variable

log = logging.getLogger()


class Blitz(Trigger):
    '''Apply some configuration, validate some keys and remove configuration'''
    def __iter__(self, *args, **kwargs):

        for section in self._discover():
            if loopable(section):
                for iteration in get_iterations(section):
                    new_section = section.__testcls__(section,
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
        sections = []
        for component in self.parameters.get('test_sections', {}):
            for action, data in component.items():
                # Attempt to find existing method with same name as action
                method = aetest_methods.get(action)
                if not method:
                    # The function doesn't exist
                    # Generate the test automatically
                    if 'setup' in data:
                        # Load the setup one
                        method = setup_section
                    elif 'cleanup' in data:
                        # Load the cleanup one
                        method = cleanup_section
                    else:
                        # Default is test
                        method = test_section

                func = copy_func(method)
                func.uid = action
                iteration = 1
                while func.uid in used_uids:
                    func.uid = '{}.{}'.format(func.uid, iteration)
                    iteration += 1

                func.parameters = ParameterDict()
                func.parameters['data'] = deepcopy(data)
                func.source = Source(self, method.__class__)

                new_method = func.__get__(self, func.__testcls__)

                sections.append(new_method)
                used_uids.append(new_method.uid)
        return sections

    def dispatcher(self, steps, testbed, section, data):
        ret_dict = {} 
        if not data:
            log.info('Nothing to execute, ending section')
            return
        
        for action_item in data:
            if 'parallel' in action_item:

                action_parallel(self, steps, testbed, section, action_item['parallel'])
                continue
                
            for action, kwargs in action_item.items():
                if not kwargs:
                    raise Exception('No data was provided for {a}'.format(a=action))

                # adding the section description
                if 'description' in action:
                    section.description = kwargs
                    continue

                step_msg = "Starting action {a}".format(a=action)
                if 'device' in kwargs:
                    try:
                        device = testbed.devices[kwargs['device']]
                    except KeyError:
                        raise Exception("Could not find the device '{d}' "
                                        "which was provided in the "
                                        "action".format(d=kwargs['device']))
                    step_msg += " on device '{d}'".format(d=device.name)

                    # Provide device object
                    kwargs['device'] = device
                    # adding the device name to return dictionary
                    ret_dict['device'] = device.name
                else:
                    # in cases that no device is defined
                    ret_dict['device'] = None

                # adding the step description
                description = kwargs.pop('description', '')
                # check if user wants the testcase to stop after a failure or to continue
                continue_ = kwargs.pop('continue', True)
                ret_dict['continue_'] = continue_
                with steps.start(step_msg, continue_=continue_, description=description) as step:

                    if 'banner' in kwargs:
                        log.info(banner(kwargs['banner']))
                        del kwargs['banner']

                    # By default the testcase would continue after a failure
                    # if user sets continue to false though it would stop
                    kwargs['continue_'] = continue_

                    # The actions were not added as a bounded method
                    # so providing the self
                    kwargs['self'] = self
                    save = kwargs.pop('save', [])

                    # Checking to replace variables and get those arguments
                    kwargs = get_variable(**kwargs)

                    # Updating steps to be newly created step
                    kwargs['steps'] = step

                    if action in actions:
                        # Call the action with all the arguments

                        action_output = actions[action](**kwargs)
                    else:
                        # Call custom action
                        _self = kwargs.pop('self')

                        try:
                            action_output = getattr(self, action)(**kwargs)
                        except AttributeError:
                            raise Exception("'{action}' is not a valid action "
                                            "or custom action"
                                            .format(action=action))

                        kwargs['self'] = _self

                    # saving actions and outputs and their results in vars
                    # storing all the necessary return values in a dict to be saved later in reporting parallel actions
                    ret_dict.update({'action': action,
                                     'description': description,
                                     'step_result': step.result,
                                     'saved_vars': {}})

                    # filtering and saving process, ablity of saving multiple vars
                    for item in save:
                        # Filtering the action output and saving the output
                        # Saving the variable in self.parameters
                        save_variable_name = item.get('variable_name')
                        filters = item.get('filter')
                        output = filter_variable(self, action_output, filters=filters)

                        if filters:
                            log.info('Applied filter: {} to the action {} output'.format(filters, action))
                            ret_dict.update({'filters': filters})

                        save_variable(self, output, save_variable_name)

                        # updating the return dictionary with the saved value
                        ret_dict['saved_vars'].update({save_variable_name:output})

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