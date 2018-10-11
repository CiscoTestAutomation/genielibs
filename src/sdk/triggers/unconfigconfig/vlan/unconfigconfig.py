'''Implementation for vlan unconfigconfig triggers'''

# import ats
from ats import aetest

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import \
                        TriggerUnconfigConfig as TriggerUnconfigConfigMain


class TriggerUnconfigConfig(TriggerUnconfigConfigMain):
    '''Trigger class for UnconfigConfig action'''

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
        # check if device is with vtp enabled, 
        # if so, will change mode to Conf object
        try:
            vtp_output = abstract.parser.show_vtp.ShowVtpStatus(device=uut).parse()
            if vtp_output['vtp']['enabled']:
                method = 'conf'
        except:
            # will keep the default method
            pass

        self.method = method

        if 'conf' not in self.method:
            self.lib = abstract.sdk.libs.abstrtacted_libs.restore.Restore()
            try:
                self.lib.save_configuration(uut, method, abstract)
            except Exception as e:
                self.failed('Saving the configuration failed', from_exception=e,
                            goto=['next_tc'])
        else:
            pass


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
        if self.method == 'conf':
            try:
                self.mapping.configure(device=uut, abstract=abstract, steps=steps)
            except Exception as e:
                self.failed('Failed to configure the vlan', from_exception=e)
        else:
            try:
                self.lib.restore_configuration(uut, method, abstract)
            except Exception as e:
                self.failed('Failed to restore the configuration', from_exception=e)
