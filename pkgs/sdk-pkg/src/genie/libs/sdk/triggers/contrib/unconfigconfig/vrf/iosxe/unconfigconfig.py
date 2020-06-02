import logging
import time
log = logging.getLogger(__name__)
from pyats import aetest
from pprint import pprint as pp
from genie.harness.base import Trigger
import pdb
from pyats.utils.objects import Not, NotExists
from genie.libs.sdk.triggers.template.unconfigconfig import \
                       TriggerUnconfigConfig as UnconfigConfigTemplate

# Genie
from genie.harness.exceptions import GenieConfigReplaceWarning

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig

class TriggerUnconfigConfigVrf(Trigger):
    ''' Config and Unconfig of Vrf '''
    @aetest.setup
    def prerequisites(self,uut,vrf_id):
        #To verify vrf 
        output = uut.parse('show vrf detail')
        if vrf_id in output:
            self.skipped('Vrf id is there') 

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
    def Unconfig(self,uut,vrf_id):
        '''unconfigure vrf no vrf definition red '''
        uut.configure('no vrf definition {id}'.format(id=vrf_id))
        time.sleep(220) 

    @aetest.test
    def Verify_unconfig(self,uut,vrf_id):
        # ''' Verify vrf unconfig worked or not '''
        output = uut.parse('show vrf detail')
        if vrf_id not in output:
            self.passed("VRF id {id} is not showing anymore in the "
            "output of the cmd, this is "
            "expected!".format(id=vrf_id))

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
