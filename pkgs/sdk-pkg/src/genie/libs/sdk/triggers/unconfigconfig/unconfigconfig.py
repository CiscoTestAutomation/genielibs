'''Common implementation for unconfigconfig triggers'''

# import python
import logging

# import ats
from ats import aetest

# Genie Libs
from genie.libs.sdk.triggers.template.unconfigconfig import \
                       TriggerUnconfigConfig as UnconfigConfigTemplate

# Genie Exceptions
from genie.harness.exceptions import GenieConfigReplaceWarning

log = logging.getLogger(__name__)


class TriggerUnconfigConfig(UnconfigConfigTemplate):
    '''Trigger class for UnconfigConfig action'''

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

    @aetest.test
    def save_configuration(self, uut, method, abstract, steps):
        '''Save current configuration

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
        self.lib = abstract.sdk.libs.abstracted_libs.restore.Restore()
        default_dir = getattr(self.parent, 'default_file_system', {})
        try:
            self.lib.save_configuration(uut, method, abstract, default_dir)
        except Exception as e:
            self.failed('Saving the configuration failed', from_exception=e,
                        goto=['next_tc'])

    @aetest.test
    def unconfigure(self, uut, abstract, steps):
        '''Unconfig configuration on the uut device

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
            self.failed('Failed to unconfigure feature', from_exception=e)

    @aetest.test
    def verify_unconfigure(self, uut, abstract, steps):
        '''Verify that the unconfiguration was done correctly and Ops state is 
           as expected.

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
            self.mapping.verify_missing_ops(device=uut, abstract=abstract,
                                            steps=steps)
        except Exception as e:
            self.failed('Failed to verify the '
                        'unconfigure feature', from_exception=e)

    @aetest.test
    def restore_configuration(self, uut, method, abstract, steps):
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
        '''Verify the configuration and device state is back to what
           it was at the begining of the trigger

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
            self.post_snap = self.mapping.verify_with_initial(\
                                                   device=uut,
                                                   abstract=abstract,
                                                   steps=steps,
                                                   timeout_recovery=timeout_recovery)
        except Exception as e:
            self.failed("Failed to restore initial configuration",
                        from_exception=e)
