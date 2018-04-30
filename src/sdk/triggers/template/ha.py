'''HA triggers template'''

from ats import aetest
from genie.harness.base import Trigger

class TriggerSwitchover(Trigger):
    ''' Template for all Switchover triggers

        A Switchover trigger is defined in 4 main steps:

          1. Verify if we can do switchover on the device,
             get RP information.
          2. Do switchover
          3. Verify the active and standby RP are switched
          4. Update the global/local verifications, and PTS if
             the features are enabled.
    '''
    @aetest.setup
    def verify_prerequisite(self, uut, abstract, steps, timeout):
        raise NotImplementedError

    @aetest.test
    def switchover(self, uut, abstract, steps):
        raise NotImplementedError

    @aetest.test
    def verify_switchover(self, uut, abstract, steps):
        raise NotImplementedError

    @aetest.test
    def update_platform(self, uut, abstract, steps):
        raise NotImplementedError


class TriggerReload(Trigger):
    ''' Template for all Reload triggers

        A Switchover Reload is defined in 4 main steps:

          1. Verify if we can do reload on the device,
             get RP information.
          2. Do reload
          3. Verify the device status is back ready.
          4. Update the global/local verifications, and PTS if
             the features are enabled.
    '''
    @aetest.setup
    def verify_prerequisite(self, uut, abstract, steps, timeout):
        raise NotImplementedError

    @aetest.test
    def reload(self, uut, abstract, steps):
        raise NotImplementedError

    @aetest.test
    def verify_reload(self, uut, abstract, steps):
        raise NotImplementedError

    @aetest.test
    def update_platform(self, uut, abstract, steps):
        raise NotImplementedError