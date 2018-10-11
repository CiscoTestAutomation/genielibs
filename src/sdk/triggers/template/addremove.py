'''TriggerAddRemove template'''

from ats import aetest
from genie.harness.base import Trigger


class TriggerAddRemove(Trigger):
    ''' Template for all TriggerAddRemove triggers

        An AddRemove trigger is defined in 6 main steps:

          1. Verify if we should execute the trigger. This is known by
             verifying if certain requirements are satisfied.
          2. Add configuration on the device.
          3. Verify configuration has been added correctly and Operational
             state is as expected.
          4. Remove previously added configuration.
          5. Verify configuration has been removed correctly and Operational
             state is as expected.
    '''

    @aetest.setup
    def verify_prerequisite(self):
        raise NotImplementedError

    @aetest.test
    def save_configuration(self):
        raise NotImplementedError

    @aetest.test
    def add_configuration(self):
        raise NotImplementedError

    @aetest.test
    def verify_configuration(self):
        raise NotImplementedError

    @aetest.test
    def remove_configuration(self):
        raise NotImplementedError

    @aetest.test
    def restore_configuration(self):
        raise NotImplementedError

    @aetest.test
    def verify_initial_state(self):
        raise NotImplementedError
