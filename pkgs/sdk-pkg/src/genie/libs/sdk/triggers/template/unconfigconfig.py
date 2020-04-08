'''TriggerUnconfigConfig template'''

from pyats import aetest
from genie.harness.base import Trigger

class TriggerUnconfigConfig(Trigger):
    ''' Template for all TriggerUnconfigConfig triggers

        A UnconfigConfig trigger is defined in 6 main steps:

          1. Verify if we should execute the trigger. This is known by
             verifying if certain requirements are satisfied.
          2. Prepare mechanism to revert configuration for the end step.
          3. Unconfigure certain configuration.
          4. Verify it has been unconfigured correctly and Operational state is
             as expected.
          5. Revert the configuration.
          6. Verify it has been reverted correctly and operation state is
             back to what it was at the begining.
    '''

    @aetest.setup
    def verify_prerequisite(self):
        raise NotImplementedError

    @aetest.test
    def save_configuration(self):
        raise NotImplementedError

    @aetest.test
    def unconfigure(self):
        raise NotImplementedError

    @aetest.test
    def verify_unconfigure(self):
        raise NotImplementedError

    @aetest.test
    def restore_configuration(self):
        raise NotImplementedError

    @aetest.test
    def verify_initial_state(self):
        raise NotImplementedError
