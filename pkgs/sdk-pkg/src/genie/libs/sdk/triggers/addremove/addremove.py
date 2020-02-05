'''Common implementation for addremove triggers'''

# import python
import logging

# import pyats
from pyats import aetest

# Genie Libs
from genie.libs.sdk.triggers.template.addremove import \
                       TriggerAddRemove as AddRemoveTemplate

# Genie
from genie.harness.exceptions import GenieConfigReplaceWarning

log = logging.getLogger(__name__)


class TriggerAddRemove(AddRemoveTemplate):
    '''Trigger class for AddRemove action'''

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
    def add_configuration(self, uut, abstract, steps):
        '''Add configuration on the uut device

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
            self.mapping.configure(device=uut, abstract=abstract, steps=steps)
        except Exception as e:
            self.failed('Failed to configure', from_exception=e)

    @aetest.test
    def verify_configuration(self, uut, abstract, steps):
        '''Verify configuration has been added correctly and Operational
           state is as expected.

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
            self.mapping.verify_ops(device=uut, abstract=abstract, steps=steps)
        except Exception as e:
            self.failed('Failed to verify the '
                        'added feature', from_exception=e)

    @aetest.test
    def remove_configuration(self, uut, abstract, steps):
        '''Remove configuration from the uut device

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
        '''Verify configuration has been removed correctly and Operational
           state is as expected.

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
            self.mapping.verify_with_initial(device=uut, abstract=abstract,
                                            steps=steps, timeout_recovery=timeout_recovery)
        except Exception as e:
            self.failed('Failed to verify the '
                        'unconfigure feature', from_exception=e)
