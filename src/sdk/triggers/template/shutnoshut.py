'''TriggerShutNoShut template'''

from ats import aetest
from genie.harness.base import Trigger

# Genie Libs
from genie.libs.sdk.libs.abstracted_libs import sleep_processor

@aetest.processors(pre=[sleep_processor])
class TriggerShutNoShut(Trigger):
    ''' Template for all TriggerShutNoShut triggers

        A ShutNoShut trigger is defined in 5 main steps:

          1. Verify if we should execute the trigger. This is known this by
             verifying if certain requirements are satisfied.
          2. Shut a particular feature/interface/configuration.
          3. Verify it has been shut correctly and Operational state is as
             expected.
          4. Unshut the particular feature/interface/configuration.
          5. Verify it has been unshut correctly and operation state is
             back to what it was at the begining.
    '''

    @aetest.setup
    def verify_prerequisite(self):
        raise NotImplementedError

    @aetest.test
    def shut(self):
        raise NotImplementedError

    @aetest.test
    def verify_shut(self):
        raise NotImplementedError

    @aetest.test
    def unshut(self):
        raise NotImplementedError

    @aetest.test
    def verify_initial_state(self):
        raise NotImplementedError

