'''Common implementation for shutnoshut triggers'''

# import python
import logging

# import ats
from ats import aetest

# Genie Libs
from genie.libs.sdk.triggers.template.shutnoshut import \
                       TriggerShutNoShut as ShutNoShutTemplate

log = logging.getLogger(__name__)

class TriggerShutNoShut(ShutNoShutTemplate):
    '''Trigger class for ShutNoShut action'''

    @aetest.setup
    def verify_prerequisite(self, uut, abstract, steps, timeout):
        '''Learn Ops object and verify the requirements.

           If the requirements are not satisfied, then skip to the next
           testcase.

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object
               timeout (`timeout obj`): Timeout Object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        self.timeout = timeout
        try:
            self.pre_snap = self.mapping.learn_ops(device=uut,
                                                   abstract=abstract,
                                                   steps=steps,
                                                   timeout=self.timeout)
        except Exception as e:
            self.errored("Section failed due to: '{e}'".format(e=e))

        for stp in steps.details:
            if stp.result.name == 'skipped':
                self.skipped('Cannot learn the feature', goto=['next_tc'])

    @aetest.test
    def shut(self, uut, abstract, steps):
        '''Send configuration to shut

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        try:
            self.mapping.configure(device=uut, abstract=abstract, steps=steps)
        except Exception as e:
            self.failed('Failed to shut the feature', from_exception=e)

    @aetest.test
    def verify_shut(self, uut, abstract, steps):
        '''Verify if the shut command shut the feature correctly and
           as expected

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        try:
            self.mapping.verify_ops(device=uut, abstract=abstract,
                                    steps=steps)
        except Exception as e:
            self.failed('Failed to verify the '
                        "shut'd feature", from_exception=e)

    @aetest.test
    def unshut(self, uut, abstract, steps):
        '''Send configuration to shut

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        try:
            self.mapping.unconfigure(device=uut, abstract=abstract, steps=steps)
        except Exception as e:
            self.failed('Failed to unshut the feature', from_exception=e)

    @aetest.test
    def verify_initial_state(self, uut, abstract, steps, timeout_recovery=None):
        '''Verify the configuration and device state is back to what
           it was at the begining of the trigger

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        try:
            self.post_snap = self.mapping.verify_with_initial(\
                                                   device=uut,
                                                   abstract=abstract,
                                                   steps=steps,
                                                   timeout_recovery=timeout_recovery)
        except Exception as e:
            self.failed("Failed to restore", from_exception=e)
