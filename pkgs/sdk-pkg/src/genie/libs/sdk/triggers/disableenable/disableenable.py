'''Common implementation for disable enable triggers'''

# import python
import time
import logging

# import pyats
from pyats import aetest
from pyats.utils.objects import find, R

# Genie Libs
from genie.libs.sdk.triggers.template.disableenable import \
                       TriggerDisableEnable as DisableEnableTemplate
from genie.libs.sdk.libs.utils.triggeractions import CheckFeatureStatus

# Genie
from genie.harness.exceptions import GenieConfigReplaceWarning

log = logging.getLogger(__name__)


class TriggerDisableEnable(DisableEnableTemplate):
    '''Trigger class for DisableEnable action'''

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
                                                   timeout=timeout)
        except Exception as e:
            self.errored("Section failed due to: '{e}'".format(e=e))

        for stp in steps.details:
            if stp.result.name == 'skipped':
                self.skipped('Cannot learn the feature', goto=['next_tc'])

        self.print_local_verifications()

    @aetest.test
    def save_configuration(self, uut, method, abstract):
        '''Save current configuration

           Can be either done via TFTP or checkpoint feature (If exists for OS)

            Args:
                uut (`obj`): Device object.
                method (`str`): Save method to save the configuration.
                                For now accpet "local" and "checkpoint"

            Returns:
                None

            Raises:
               pyATS Results
        '''
        self.lib = abstract.sdk.libs.abstracted_libs.restore.Restore()
        default_dir = getattr(self.parent, 'default_file_system', {})
        try:
            self.lib.save_configuration(uut, method, abstract, default_dir)
        except Exception as e:
            self.failed('Saving the configuration failed', from_exception=e,
                        goto=['next_tc'])

    @aetest.test
    def disable(self, uut, abstract, steps):
        ''' Disable the feature on the uut device

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
            self.mapping.unconfigure(device=uut, abstract=abstract, steps=steps)
        except Exception as e:
            self.failed('Failed to disable the feature', from_exception=e)

    @aetest.test
    def verify_disable(self, uut, abstract):
        ''' Verify if the feature is disabled

            Args:
                uut (`obj`): Device object.
                abstract (`obj`): Abstract object.

            Returns:
                None

            Raises:
               Failed: The feature is not disabled as expected
        '''
        # check if the feature is disabled
        # Not using Ops but parsers because two reason
        # 1) disable/enable feature and 'show feature' only support by NXOS
        # 2) 'show feature' is more accurate command to check the feature
        #     status rather then Ops commands.
        try:
            CheckFeatureStatus.check_feature_status(device=uut, expect='disabled',
                                 feature_name=self.feature_name,
                                 abstract=abstract)
        except Exception as e:
            self.failed('{n} is not Disabled'\
                        .format(n=self.feature_name), from_exception=e)

    @aetest.test
    def restore_configuration(self, uut, method, abstract):
        '''Rollback the configuration

           Can be either done via TFTP or checkpoint feature (If exists for OS)

           Args:
               uut (`obj`): Device object.
               method (`str`): Save method from trigger datafile.
                                Only accpet "local" and "checkpoint"

           Returns:
               None

           Raises:
               pyATS Results
        '''
        try:
            self.lib.restore_configuration(uut, method, abstract)
        except GenieConfigReplaceWarning as e:
            self.passx('Configure replace requires device reload')
        except Exception as e:
            self.failed('Failed to restore the configuration', from_exception=e)

    @aetest.test
    def verify_initial_state(self, uut, abstract, steps, timeout_recovery=None):
        '''Verify if the feature is enabled And
           Verify the configuration and device state is back to what
           it was at the begining of the trigger

           Args:
               uut (`obj`): Device object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        try:
            CheckFeatureStatus.check_feature_status(device=uut, expect='enabled',
                                                    feature_name=self.feature_name,
                                                    abstract=abstract)
        except Exception as e:
            self.failed('{n} is not enabled'
                        .format(n=self.feature_name), from_exception=e)

        try:
            self.post_snap = self.mapping.verify_with_initial(\
                                                   device=uut,
                                                   abstract=abstract,
                                                   steps=steps,
                                                   timeout_recovery=timeout_recovery)
        except Exception as e:
            self.failed("Failed to restore", from_exception=e)
