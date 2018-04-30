'''IOSXE implementation for Switchover triggers'''

# import ats
from ats import aetest

# Genie Libs
from genie.libs.sdk.triggers.ha.ha import \
                       TriggerSwitchover as CommonSwitchover


class TriggerSwitchover(CommonSwitchover):

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
        self.skipped('No implementation for generic iosxe HA switchover',
                     goto=['next_tc'])
