import re
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
class unconfigconfigOspfmaxpath(Trigger):
    ''' Config and Unconfig of Ospf max paths '''
    @aetest.setup
    def prerequisites(self,uut,prefix):
        ''' Verify Ospf max paths configured or nor '''
        output = uut.execute('show ip cef {}'.format(prefix))
        pre_id=re.findall(r'nexthop',output)
        self.id_count=len(pre_id)
        if len(pre_id) > 1:
            self.skipped('Next hop is greaterthan 1')

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
    def config(self,uut,id_ospf):
        uut.configure('''\
router ospf {id}
maximum-paths 1'''.format(id=id_ospf))

    @aetest.test
    def Verify_config(self,uut,prefix):
        # ''' Verify config worked or not '''
        output = uut.execute('show ip cef {}'.format(prefix))
        pre_id=re.findall(r'nexthop',output)
        if len(pre_id) == 1:
            self.passed("Next hop count is 1 "
            "form the output. This is expected!")

    @aetest.test
    def unconfig(self,uut,id_ospf):
        uut.configure('''\
router ospf {id}
no maximum-paths 1'''.format(id=id_ospf))
        

    @aetest.test
    def Verify_unconfig(self,uut,prefix):
        # ''' Verify config worked or not '''
        output = uut.execute('show ip cef {}'.format(prefix))
        pre_id=re.findall(r'nexthop',output)
        if len(pre_id) == (self.id_count):
            self.passed("Nexthop count is same after unconfig "
            "This is expected!")

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

class Triggeruserconfigentry(Trigger):
    @aetest.setup
    def prerequisites(self,uut,ospf_id):
        output = uut.parse('show ip ospf')
        if ospf_id in output:
            self.skipped("Ospf id {id} is not showing in the "
            "output of the cmd, this is "
            "unexpected!".format(id=ospf_id))

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
    def add_config(self,uut,user_config,testbed):
        uut.configure(user_config)
        ixia_device = testbed.devices['IXIA']
        ixia_device.check_traffic_loss(loss_tolerance = 100, check_interval= 30, check_iteration = 2)


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



