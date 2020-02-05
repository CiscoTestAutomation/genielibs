'''TriggerProcessRestart template'''

from pyats import aetest
from genie.harness.base import Trigger

class TriggerProcessRestart(Trigger):
    ''' Template for all TriggerRestart triggers

        A ProcessRestart trigger is defined in 3 main steps:

          1. Verify if we can restart the processs and find what to restart
          2. Restart the found process
          3. Verify it has restarted correctly and the state is as expected
    '''
    @aetest.setup
    def verify_prerequisite(self, uut, abstract, steps, timeout):
        raise NotImplementedError

    @aetest.test
    def restart(self, uut, abstract, steps):
        raise NotImplementedError

    @aetest.test
    def verify_restart(self, uut, abstract, steps):
        raise NotImplementedError
