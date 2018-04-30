'''TriggerModify template'''

from ats import aetest
from genie.harness.base import Trigger

# Genie Libs
from genie.libs.sdk.libs.abstracted_libs import sleep_processor

@aetest.processors(pre=[sleep_processor])
class TriggerModify(Trigger):
    ''' Template for all TriggerModify triggers

        A Modify trigger is defined in 6 main steps:

          1. Verify if we should execute the trigger. This is known this by
             verifying if certain requirements are satisfied.
          2. Prepare mechanism to revert configuration (see step 5).
          3. Modify the configuration.
          4. Verify it has been modified correctly and operational state is as
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
    def modify_configuration(self):
        raise NotImplementedError

    @aetest.test
    def verify_modification(self):
        raise NotImplementedError

    @aetest.test
    def restore_configuration(self):
        raise NotImplementedError

    @aetest.test
    def verify_initial_state(self):
        raise NotImplementedError
