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

class TriggerUnconfigConfigMplsStaticBindings(Trigger):
    ''' Unconfigure Configure mpls static bindings'''
    @aetest.setup
    def prerequisites(self, uut):
        ''' Getting the bindings config and local labels'''
        output = uut.execute('show run')
        self.mpls_bind=re.findall(r'.*(mpls\sstatic\sbinding\sipv4\s\d+\.\d+\.\d+\.\d+\s\d+\.\d+\.\d+\.\d+\s\d+)',output)
        local_dict_1 = []
        output1 = uut.parse('show mpls forwarding-table')
        for vrf_id in output1['vrf']:
            for local_id in output1['vrf'][vrf_id]['local_label']:
                local_dict_1.append(local_id)
                if local_id in output1:
                     print("local id:",local_id)

        self.local_1 = local_dict_1
        print('self local label:',self.local_1)

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
    def Unconfig(self,uut, testbed):
        ''' unconfiguring all the mpls static bindings'''
        for i in self.mpls_bind:
            status = 'no '
            val= status + i
            print('mpls static bind:',val)
            uut.configure(val)

    @aetest.test
    def verify_Unconfig(self, uut, l_id):
        ''' verifying the unconfigured labels are getting or not '''
        local_dict_2 = []
        output2 = uut.parse('show mpls forwarding-table detail')
        for vrf_id in output2['vrf']:
            for local_id in output2['vrf'][vrf_id]['local_label']:
                local_dict_2.append(local_id)
                if local_id not in output2:
                    print("local id:",local_id)

        self.local_2 = local_dict_2
        print('self local label:',self.local_2)

        if l_id not in self.local_2:
            self.passed("local label {local_lbl} is not showing in the "
            "output of the cmd, this is expected"
            "expected!".format(local_lbl=l_id))
        else:
            self.failed("local label {local_lbl} is showing in the "
            "output of the cmd, this is unexpected"
            "un expected!".format(local_lbl=l_id))

    @aetest.test
    def Config(self,uut, testbed):
        ''' re-configuring all the mpls static bindings '''    
        for i in self.mpls_bind:
            val= i
            print('mpls static bind:',val)
            uut.configure(val)

    @aetest.test
    def verify_Config(self, uut, l_id):
        ''' verifying the unconfigured labels are getting or not '''
        local_dict_3 = []
        output3 = uut.parse('show mpls forwarding-table')
        for vrf_id in output3['vrf']:
            for local_id in output3['vrf'][vrf_id]['local_label']:
                local_dict_3.append(local_id)
                if local_id in output3:
                    print("local id:",local_id)

        self.local_3 = local_dict_3
        print('self local label:',self.local_3)

        if l_id in self.local_3:
            self.passed("local label {local_lbl} is showing in the "
            "output of the cmd, this is "
            "expected!".format(local_lbl=l_id))
        else:
            self.failed("local label {local_lbl} is not showing in the "
            "output of the cmd, this is "
            "unexpected!".format(local_lbl=l_id))

    @aetest.test
    def restore_configuration(self, uut, method, abstract, steps, testbed):
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

