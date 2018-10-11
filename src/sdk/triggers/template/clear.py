''' triggerClear template'''

# import ats
from ats import aetest

# import genie infra
from genie.harness.base import Trigger


class TriggerClear(Trigger):
    ''' Template for all Clear triggers

        TriggerClear will follow the following steps:
          1. Take pre snapshot for ops before clear action.
          2. Execute clear command.
          3. Verify the clear command to see if it works.
    '''

    @aetest.test
    def verify_prerequisite(self):
        raise NotImplementedError

    @aetest.test
    def clear(self):
        raise NotImplementedError

    @aetest.test
    def verify_clear(self):
        raise NotImplementedError
