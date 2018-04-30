''' triggerSleep template'''

# import ats
from ats import aetest

# import genie infra
from genie.harness.base import Trigger


class TriggerSleep(Trigger):
    ''' Template for all Sleep triggers

        TriggerSleep will sleep with no action.
    '''

    @aetest.test
    def sleep(self):
        raise NotImplementedError
