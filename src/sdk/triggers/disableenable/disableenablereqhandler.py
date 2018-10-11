'''Common implementation for disable enable triggers for
   extra handling when disable the features'''

# import python
import time
import logging

# import ats
from ats import aetest
from ats.utils.objects import find, R

# Genie Libs trigger clear template
from genie.libs.sdk.triggers.template.disableenable import \
                       TriggerDisableEnableReqHandler
from genie.libs.sdk.libs.utils.triggeractions import CheckFeatureStatus

log = logging.getLogger(__name__)


class TriggerDisableEnableReqHandler(TriggerDisableEnableReqHandler):
    '''Trigger class for DisableEnable extra handling
       before/after disable/enable action'''

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
        try:
            self.lib.save_configuration(uut, method, abstract)
        except Exception as e:
            self.failed('Saving the configuration failed', from_exception=e,
                        goto=['next_tc'])

    @aetest.test
    def pre_handle_dependency(self, uut):
        ''' Handle the required steps before can disable the feature
            Ex. LACP feature needs remove the port-channel interfaces
                before disable the feaure

            Args:
                uut (`obj`): Device object.

            Returns:
                None

            Raises:
                None
        '''
        log.info('Handle feature dependencies *before* disabling feature')
        if hasattr(self, 'handler'):
            if 'pre' in self.handler:
                try:
                    self.handler['pre'](uut)
                except Exception as e:
                    self.failed('Failed to do pre handle due to',
                                from_exception=e)

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
            self.failed('{n} is not disabled'
                        .format(n=self.feature_name), from_exception=e)

    @aetest.test
    def post_handle_dependency(self, uut):
        ''' Handle the lost configurations which not in the running-config
            after enable the feature.
            Ex. Fabricpath feature needs delete profiles
                after enable the feaure

            Args:
                uut (`obj`): Device object.

            Returns:
                None

            Raises:
                None
        '''
        log.info('Handle feature dependencies after disabling feature')
        if hasattr(self, 'handler') and 'post' in self.handler:
            try:
                self.handler['post'](uut)
            except Exception as e:
                self.failed('Failed to do post handle due to',
                            from_exception=e)

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
        except Exception as e:
            self.failed('Failed to restore the configuration', from_exception=e)

    @aetest.test
    def verify_initial_state(self, uut, abstract, steps):
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
                                                   steps=steps)
        except Exception as e:
            self.failed("Failed to restore", from_exception=e)
