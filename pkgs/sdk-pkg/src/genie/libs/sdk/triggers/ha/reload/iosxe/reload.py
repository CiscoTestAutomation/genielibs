'''IOSXE implementation for Reload triggers'''

# import pyats
from pyats import aetest
from genie.harness.base import Trigger
from genie.utils.timeout import Timeout
from unicon.eal.dialogs import Dialog

# Genie Libs
from genie.libs.sdk.triggers.ha.ha import \
                       TriggerReload as CommonReload, \
                       TriggerReloadLc


class TriggerReload(Trigger):

    @aetest.setup
    def verify_prerequisite(self, uut, timeout, save_config=False):
        '''Reload device

           Trigger to reload device

           Args:
               uut (`obj`): Device object.
               save_config (`Bool`): Boolean to determine whether or not to save running config before reload
               timeout (`timeout obj`): Timeout Object

           Returns:
               None
        '''
    @aetest.test
    def reload_node(self, uut, timeout, save_config=False):

        if save_config:
            dialog = Dialog([[r'Destination filename \[startup-config]\?\s*$', 'sendline()', None, True, False]])
            uut.execute('copy run start', timeout=120, reply=dialog)
        uut.settings.RELOAD_WAIT = float(timeout.interval)
        uut.settings.RELOAD_RECONNECT_ATTEMPTS = int(round(timeout.max_time/timeout.interval))
        result = uut.reload()
        if not result:
            self.failed('{uut} failed to reload.'.format(uut=uut.name))


class TriggerReloadActiveRP(CommonReload):

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
        self.skipped('No implementation for generic iosxe HA reload',
                     goto=['next_tc'])


class TriggerReloadStandbyRP(CommonReload):

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
        self.skipped('No implementation for generic iosxe HA reload',
                     goto=['next_tc'])


class TriggerReloadMember(TriggerReloadLc):

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
        self.skipped('No implementation for generic iosxe HA reload',
                     goto=['next_tc'])


class TriggerReloadActiveFP(TriggerReloadLc):

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
        self.skipped('No implementation for generic iosxe HA reload',
                     goto=['next_tc'])
        