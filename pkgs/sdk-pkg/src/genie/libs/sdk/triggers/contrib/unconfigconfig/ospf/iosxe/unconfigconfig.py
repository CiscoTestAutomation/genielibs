import time
import logging
from pyats import aetest
from genie.harness.base import Trigger
from pprint import pprint as pp
from genie.harness.base import Trigger
import pdb
import re

log = logging.getLogger(__name__)

# Genie Libs
from genie.libs.sdk.triggers.template.unconfigconfig import \
                       TriggerUnconfigConfig as UnconfigConfigTemplate

# Genie
from genie.harness.exceptions import GenieConfigReplaceWarning

from pyats.utils.objects import Not, NotExists

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig
from genie.utils import Dq

class TriggerUnconfigConfigOspfInteface(Trigger):
    ''' Unconfiguring  ospf under all interfaces'''
    @aetest.setup
    def prerequisites(self, uut):
        ''' Getting the ospf configured interfaces'''
        local_dict_1 = []
        output_1 = uut.parse('show ip ospf neighbor')
        for intrf in output_1['interfaces']:
            local_dict_1.append(intrf)
            if intrf in output_1:
                print("interface:",intrf)

        print('local dictionary:',local_dict_1)
        self.local_intrf_1 = local_dict_1
        for i in self.local_intrf_1:
            print('Local interface:',i)

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
    def Unconfig(self,uut, ospf_id):
        ''' Unconfiguring ospf from all interfaces'''
        for i in self.local_intrf_1:
            uut.configure('''\
interface {id}
no ip ospf {o_id} area 0'''.format(id=i,o_id=ospf_id))

    @aetest.test
    def verify_Unconfig(self,uut):
        ''' Verifying ospf unconfigured interface exists'''
        try:
             output=uut.parse('show ip ospf neighbor')
        except:
            self.passed('ospf configured interface {} is not showing in the output of the cmd, this is expected'.format(self.local_intrf_1))
        else:
            self.failed('Interfaces are showing for the ospf')

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

class unconfigconfigOspf(Trigger):
    ''' Config and Unconfig of Ospf '''
    @aetest.setup
    def prerequisites(self,uut,ospf_id):
        ''' Verify Ospf configured or nor '''

        #To verify if Ospf is configured
        output = uut.parse('show ip ospf')
        if ospf_id not in Dq(output).get_values('instance'):
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
    def Unconfig(self,uut,ospf_id):
        ''' Configure Ospf '''
        uut.configure('no router ospf {id}'.format(id=ospf_id))

    @aetest.test
    def Verify_unconfig(self,uut,ospf_id):
        # ''' Verify Ospf config worked or not '''
        try:
            output = uut.parse('show ip ospf')
        except Exception as err:
            log.info('Schema parser is empty, this if only 1 OSPF instance is configured.')
            output = ''
        if ospf_id not in Dq(output).get_values('instance'):
            self.passed("Ospf is {id} is not showing anymore in the "
            "output of the cmd, this is "
            "expected!".format(id=ospf_id))
        else:
            self.failed("Ospf instance {id} is still in config".format(id=ospf_id))

    @aetest.test
    def Config(self,uut,ospf_id):
        ''' Configure Ospf '''
        uut.configure('''\
router ospf {id}'''.format(id=ospf_id))

    @aetest.test
    def Verify_config(self,uut,ospf_id):
        # ''' Verify Ospf config worked or not '''
        output = uut.parse('show ip ospf')
        if ospf_id in Dq(output).get_values('instance'):
            self.passed("Ospf is {id} is showing in the "
            "output of the cmd, this is "
            "expected!".format(id=ospf_id))
        else:
            self.failed("No ospf {id} is there".format(id=ospf_id))

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
        if ospf_id in Dq(output).get_values('instance'):
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

