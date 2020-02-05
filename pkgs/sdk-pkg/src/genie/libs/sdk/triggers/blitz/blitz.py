import logging
import copy
from pyats import aetest
from pyats.log.utils import banner
from pyats.aetest.loop import loopable, get_iterations
from genie.harness.base import Trigger

from genie.harness.discovery import copy_func
from pyats.aetest.base import Source
from pyats.aetest.parameters import ParameterDict

from .actions import actions
from .actions import device_parallel
from .actions import action_parallel


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
                func.parameters['data'] = data
                func.source = Source(self, method.__class__)

                new_method = func.__get__(self, func.__testcls__)

                sections.append(new_method)
                used_uids.append(new_method.uid)
        return sections

    def dispatcher(self, steps, testbed, data):
        if not data:
            log.info('Nothing to execute, ending section')
            return

        for action_item in data:
            if action_item == 'parallel':
                action_parallel(self, steps, testbed, data['parallel'])
                continue
            for action, kwargs in action_item.items():

                # See if action exists in actions
                if not kwargs:
                    raise Exception('No data was provided for {a}'.format(a=action))
                if action not in actions:
                    raise Exception("'{a} is not a valid "
                                    "action".format(a=action))

                step_msg = "Starting action {a}".format(a=action)
                if 'device' in kwargs:
                    device = testbed.devices.get(kwargs['device'])
                    if not device:
                        raise Exception("Could not find the device '{d}' "
                                        "which was provided in the "
                                        "action".format(d=device))
                    step_msg += ' on device {d}'.format(d=device.name)

                    # Provide device object
                    kwargs['device'] = device

                continue_ = kwargs.pop('continue', True)
                with steps.start(step_msg, continue_=continue_) as step:

                    if 'banner' in kwargs:
                        log.info(banner(kwargs['banner']))
                        del kwargs['banner']

                    # The actions were not added as a bounded method
                    # so providing the self
                    kwargs['self'] = self
                    # Updating steps to be newly created step
                    kwargs['steps'] = step

                    # Call the action with all the arguments
                    actions[action](**kwargs)

@aetest.setup
def setup_section(self, steps, testbed, data=None):
    return self.dispatcher(steps, testbed, data)

@aetest.test
def test_section(self, steps, testbed, data=None):
    return self.dispatcher(steps, testbed, data)

@aetest.cleanup
def cleanup_section(self, steps, testbed, data=None):
    return self.dispatcher(steps, testbed,  data)
