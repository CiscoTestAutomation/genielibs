'''Common implementation for shutnoshut triggers'''

# Python
import time
import logging

# ATS
from ats import aetest

# Genie Libs Triggers
from genie.libs.sdk.triggers.template.ha import TriggerSwitchover as\
                                                SwitchoverTemplate
from genie.libs.sdk.triggers.template.ha import TriggerReload as ReloadTemplate
from genie.libs.sdk.triggers.template.ha import TriggerIssu as IssuTemplate

# Genie Libs Utils
from genie.libs.sdk.libs.utils.common import UpdateLearntDatabase

log = logging.getLogger(__name__)


class TriggerSwitchover(SwitchoverTemplate):
    '''Trigger class for Switchover action'''

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
        self.timeout = timeout
        try:
            self.pre_snap = self.mapping.learn_ops(device=uut,
                                                   abstract=abstract,
                                                   steps=steps,
                                                   timeout=self.timeout)
        except Exception as e:
            self.errored("Section failed due to: '{e}'".format(e=e))

        for stp in steps.details:
            if stp.result.name == 'skipped':
                self.skipped('Cannot learn the feature', goto=['next_tc'])

    @aetest.test
    def switchover(self, uut, abstract, steps):
        '''Switchover and reconnect to device

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        self.ha = abstract.sdk.libs.abstracted_libs.ha.HA(device=uut)
        try:
            self.ha.switchover(timeout=self.timeout, steps=steps)
        except Exception as e:
            self.failed('Failed to switchover', from_exception=e,
                         goto=['next_tc'])

    @aetest.test
    def verify_switchover(self, uut, abstract, steps):
        '''Verify if the switchover taken place

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        try:
            self.mapping.verify_ops(device=uut, abstract=abstract,
                                    steps=steps)
        except Exception as e:
            self.failed('Failed to verify the '
                        "platform", from_exception=e)

    @aetest.test
    def update_platform(self, uut, abstract, steps,
                        update_verifications=None, update_pts_features=None):
        '''Learn the verifications from the given list and
        overwrite it into local and global verifications.

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object
               update_verifications (`list`): Verifications that want to be updatd
               update_pts_features (`list`): Features of the PTSs that want to be updatd

           Returns:
               None

           Raises:
               pyATS Results
        '''
        # initial UpdateLearntDatabase object to update the database
        update_obj = UpdateLearntDatabase(obj=self, device=uut)

        # update global/local verification
        if update_verifications:
            with steps.start("Update global and local verifications for {}"
              .format(update_verifications)) as step:
                update_obj.update_verification(abstract=abstract,
                                               update_ver_list=update_verifications)

        # update platform pts
        # update chassis_sn and slot info
        if update_pts_features:
            with steps.start("Update PTS for features {}"
              .format(update_pts_features)) as step:
                update_obj.update_pts(abstract=abstract,
                                      update_feature_list=update_pts_features,
                                      update_attributes={'platform': ['chassis_sn', 'slot', 'virtual_device']})


class TriggerReload(ReloadTemplate):
    '''Trigger class for Reload action'''

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
        self.timeout = timeout
        try:
            self.pre_snap = self.mapping.learn_ops(device=uut,
                                                   abstract=abstract,
                                                   steps=steps,
                                                   timeout=self.timeout)
        except Exception as e:
            self.skipped('Cannot learn the feature', from_exception=e,
                         goto=['next_tc'])

    @aetest.test
    def reload(self, uut, abstract, steps):
        '''Reload and reconnect to device

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        self.ha = abstract.sdk.libs.abstracted_libs.ha.HA(device=uut)
        try:
            self.ha.reload(timeout=self.timeout, steps=steps)
        except Exception as e:
            self.failed('Failed to reload', from_exception=e,
                         goto=['next_tc'])

    @aetest.test
    def verify_reload(self, uut, abstract, steps):
        '''Verify if the reload taken place

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''        
        try:
            self.mapping.verify_ops(device=uut, abstract=abstract,
                                    steps=steps)
        except Exception as e:
            self.failed('Failed to verify the '
                        "platform", from_exception=e)

        # Verify uptime
        with steps.start("Verify if system uptime is reset") as step:
            used_time = self.timeout.max_time - (self.timeout.timeout - time.time())
            if hasattr(self.mapping, 'verify_ops_object') and \
               hasattr(self.mapping.verify_ops_object, 'rp_uptime'):
                if self.mapping.verify_ops_object.rp_uptime >= used_time:
                    self.failed('System uptime is not reset, uptime: {u} >= waitTime: {w}'
                                .format(u=self.mapping.verify_ops_object.rp_uptime,
                                        w=used_time))
                else:
                    log.info('System uptime is reset, uptime: {u} < waitTime: {w}'
                                .format(u=self.mapping.verify_ops_object.rp_uptime,
                                        w=used_time))

    @aetest.test
    def update_platform(self, uut, abstract, steps,
                        update_verifications=None, update_pts_features=None):
        '''Learn the verifications from the given list and
        overwrite it into local and global verifications.

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object
               update_verifications (`list`): Verifications that want to be updatd
               update_pts_features (`list`): Features of the PTSs that want to be updatd

           Returns:
               None

           Raises:
               pyATS Results
        '''
        # initial UpdateLearntDatabase object to update the database
        update_obj = UpdateLearntDatabase(obj=self, device=uut)

        # update global/local verification
        if update_verifications:
            with steps.start("Update global and local verifications for {}"
              .format(update_verifications)) as step:
                update_obj.update_verification(abstract=abstract,
                                               update_ver_list=update_verifications)

        # update platform pts
        # update chassis_sn and slot info
        if update_pts_features:
            with steps.start("Update PTS for features {}"
              .format(update_pts_features)) as step:
                update_obj.update_pts(abstract=abstract,
                                      update_feature_list=update_pts_features,
                                      update_attributes={'platform': ['chassis_sn', 'slot', 'virtual_device']})


class TriggerReloadLc(TriggerReload):
    '''Trigger class for Reload LCs action'''

    @aetest.test
    def reload(self, uut, abstract, steps, lcRole=None):
        '''Reload LC and reconnect to device if needed

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        self.ha = abstract.sdk.libs.abstracted_libs.ha.HA(device=uut)

        # get the LC number
        for lc in self.mapping.keys:
            for key, value in lc.items():
                if lcRole and lcRole not in key:
                    continue
                try:
                    self.ha.reloadLc(timeout=self.timeout, steps=steps, lc=value)
                except Exception as e:
                    self.failed('Failed to reload LC {}'
                                 .format(value), from_exception=e,
                                goto=['next_tc'])

    @aetest.test
    def verify_reload(self, uut, abstract, steps):
        '''Verify if the reload taken palce

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''        
        try:
            self.mapping.verify_ops(device=uut, abstract=abstract,
                                    steps=steps)
        except Exception as e:
            self.failed('Failed to verify the '
                        "platform", from_exception=e)


class TriggerIssu(IssuTemplate):
    '''Trigger class for ISSU action'''

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
        self.timeout = timeout
        try:
            self.pre_snap = self.mapping.learn_ops(device=uut,
                                                   abstract=abstract,
                                                   steps=steps,
                                                   timeout=self.timeout)
        except Exception as e:
            self.skipped('Cannot learn the feature', from_exception=e,
                         goto=['next_tc'])

    @aetest.test
    def prepare_issu(self, uut, abstract, steps):
        '''Perform the steps necessary to prepare the device for ISSU

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        # Check if user has provided ISSU upgrade image successfully
        if not self.parameters['upgrade_image']:
            self.skipped("ISSU upgrade image not provided - skipping trigger",
                         goto=['next_tc'])
        self.ha = abstract.sdk.libs.abstracted_libs.ha.HA(device=uut)
        try:
            self.ha.prepare_issu(steps=steps,
                                 upgrade_image=self.parameters['upgrade_image'])
        except Exception as e:
            self.failed('Failed to successfully prepare the device for ISSU',
                        from_exception=e, goto=['next_tc'])

    @aetest.test
    def perform_issu(self, uut, abstract, steps):
        '''Perform ISSU and reconnect to switched RP

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        self.ha = abstract.sdk.libs.abstracted_libs.ha.HA(device=uut)
        try:
            self.ha.perform_issu(steps=steps,
                                 upgrade_image=self.parameters['upgrade_image'])
        except Exception as e:
            self.failed('Failed to successfully perform ISSU', from_exception=e,
                         goto=['next_tc'])

    @aetest.test
    def verify_issu(self, uut, abstract, steps):
        '''Verify if the ISSU has taken place

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        try:
            self.mapping.verify_ops(device=uut, abstract=abstract,
                                    steps=steps)
        except Exception as e:
            self.failed('Failed to verify the '
                        "platform", from_exception=e)

        # Verify uptime
        with steps.start("Verify if system uptime is reset") as step:
            used_time = self.timeout.max_time - (self.timeout.timeout - time.time())
            if hasattr(self.mapping, 'verify_ops_object') and \
               hasattr(self.mapping.verify_ops_object, 'rp_uptime'):
                if self.mapping.verify_ops_object.rp_uptime >= used_time:
                    self.failed("System uptime has not reset - rp_uptime '{u}' "
                                "is greater than the elapsed time for this "
                                " trigger '{w}'".format(
                                u=self.mapping.verify_ops_object.rp_uptime,
                                w=used_time))
                else:
                    log.info('System uptime is reset, uptime: {u} < waitTime: {w}'
                                .format(u=self.mapping.verify_ops_object.rp_uptime,
                                        w=used_time))

    @aetest.test
    def update_platform(self, uut, abstract, steps,
                        update_verifications=None, update_pts_features=None):
        '''Learn the verifications from the given list and
        overwrite it into local and global verifications.

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object
               update_verifications (`list`): Verifications that want to be updatd
               update_pts_features (`list`): Features of the PTSs that want to be updatd

           Returns:
               None

           Raises:
               pyATS Results
        '''
        # initial UpdateLearntDatabase object to update the database
        update_obj = UpdateLearntDatabase(obj=self, device=uut)

        # update global/local verification
        if update_verifications:
            with steps.start("Update global and local verifications for {}"
              .format(update_verifications)) as step:
                update_obj.update_verification(abstract=abstract,
                                               update_ver_list=update_verifications)

        # update platform pts
        # update chassis_sn and slot info
        if update_pts_features:
            with steps.start("Update PTS for features {}"
              .format(update_pts_features)) as step:
                update_obj.update_pts(abstract=abstract,
                                      update_feature_list=update_pts_features,
                                      update_attributes={'platform': ['chassis_sn', 'slot', 'virtual_device']})
