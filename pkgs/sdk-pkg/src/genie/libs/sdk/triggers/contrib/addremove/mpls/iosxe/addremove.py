import time
import logging
from pyats import aetest
from genie.harness.base import Trigger
from pprint import pprint as pp
from genie.harness.base import Trigger
import pdb

log = logging.getLogger(__name__)

# Genie Libs
from genie.libs.sdk.triggers.template.addremove import \
                       TriggerAddRemove as AddRemoveTemplate

# Genie
from genie.harness.exceptions import GenieConfigReplaceWarning

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove

import re
from genie.libs.sdk.triggers.template.unconfigconfig import \
                       TriggerUnconfigConfig as UnconfigConfigTemplate

class TriggerAddRemoveMplsLdpAutoConfig(Trigger):
    '''Add Remove mpls ldp Auto config in ospf'''

    @aetest.setup
    def prerequisites(self, uut):
        '''Figure out if ospf is configured'''
        output = uut.parse('show ip ospf')
        for vrf_id in output['vrf']:
            for addr_id in output['vrf'][vrf_id]['address_family']:
                for instance in output['vrf'][vrf_id]['address_family'][addr_id]['instance']:
                    if instance not in output:
                        print("ospf instances:",instance)
                        print("No ospf is configured for "\
                         "device '{d}'".format(d=uut.name))                 
        print(instance)
        self.ospf_id = instance
        print(self.ospf_id)

        #Getting the mpls peer id 
        output1 = uut.parse('show mpls ldp neighbor')
        for vrf_id in output1['vrf']:
            for peers in output1['vrf'][vrf_id]['peers']:
                if peers not in output1:
                    print("mpls peer:",peers)
                    print("No mpls peers are configured for "\
                     "device '{d}'".format(d=uut.name))

        print(peers)
        self.peers_id = peers
        print(self.peers_id)

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
    def remove(self, uut):
        '''Remove auto config under ospf'''
        uut.configure('''\
router ospf {id}
no mpls ldp autoconfig'''.format(id=self.ospf_id))

    @aetest.test
    def verify_remove(self, uut):
        ''' verifying the peer-id exists in the mpls neighbor list'''
        output1 = uut.parse('show mpls ldp neighbor')
        for vrf_id in output1['vrf']:
            for peers in output1['vrf'][vrf_id]['peers']:
                print("peers after removing:",peers)
                if (self.peers_id) not in peers:
                    self.passed("peers id {peers_id} is not showing anymore in the "
                    "output of the cmd, this is "
                    "unexpected!".format(peers_id=self.peers_id))

    @aetest.test
    def add(self, uut):
        '''Configuring auto config under ospf'''
        uut.configure('''\
router ospf {id}
mpls ldp autoconfig'''.format(id=self.ospf_id))

    @aetest.test
    def verify_add(self, uut):
        ''' verifying the peer-id exists in the mpls neighbor list'''
        output1 = uut.parse('show mpls ldp neighbor')
        for vrf_id in output1['vrf']:
            for peers in output1['vrf'][vrf_id]['peers']:
                print("mpls peers after reconfigure:",peers)
                if (self.peers_id) in peers:
                    self.passed("peers id {peers_id} is showing in the "
                    "output of the cmd, this is "
                    "expected!".format(peers_id=self.peers_id))

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

class Triggermplsaddremove(Trigger):
    ''' Config and Unconfig of mpls '''
    @aetest.setup
    def prerequisites(self,uut):
        #To verify mpls 
        output = uut.execute('show mpls ldp neighbor')
        if output:
            self.skipped('mpls ldp neighbors are there')

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
    def add_mpls(self,uut,ospf_id,isis_name):
        ''' add mpls with ospf and isis '''
        uut.configure('''\
router ospf {id}
mpls ldp autoconfig'''.format(id=ospf_id))

        uut.configure('''\
router isis {is_name}
mpls ldp autoconfig'''.format(is_name=isis_name))

    @aetest.test
    def Verify_addmpls(self,uut):
        # ''' Verify mpls '''
        output = uut.execute('show mpls ldp neighbor')
        if output:
            self.passed("mpls ldp neighbors are there")

    @aetest.test
    def remove_mpls(self,uut,ospf_id,isis_name):
        '''remove  mpls with ospf and isis '''
        uut.configure('''\
router ospf {id}
no mpls ldp autoconfig'''.format(id=ospf_id))

        uut.configure('''\
router isis {is_name}
no mpls ldp autoconfig'''.format(is_name=isis_name))

    @aetest.test
    def Verify_removempls(self,uut):
        # ''' Verify mpls '''
        output = uut.execute('show mpls ldp neighbor')
        if not output:
            self.passed("No neighbors for mpls and ldp")

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

class Triggermplsexplicitnull(Trigger):
    ''' mpls explict null'''
    @aetest.setup
    def prerequisites(self,uut):
        #To verify mpls
        output = uut.execute('show mpls ldp neighbor')
        id=re.search(r'.*(Msgs\s+sent)\/(rcvd)\:\s+(\d+)\/(\d+).*',output)
        msgs=id.group(1)
        msgs_recvd=id.group(3)
        rcevid=id.group(2)
        msgs_rcivd=id.group(4)
        print(msgs)
        print(msgs_recvd)
        print(rcevid)
        print(msgs_rcivd)
        self.sent_msgs=msgs_recvd
        print(self.sent_msgs)
        self.recvd_msgs=msgs_rcivd
        print(self.recvd_msgs)
#        if output:
#            self.skipped('mpls ldp neighbors are there')

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
    def explictmplsnull(self,uut):
        ''' explicit mpls '''
        uut.configure('mpls ldp explicit-null')

    @aetest.test
    def Verify_explictmplsnull(self,uut):
        # ''' Verify mpls '''
        output = uut.execute('show mpls ldp neighbor')
        id=re.search(r'.*(Msgs\s+sent)\/(rcvd)\:\s+(\d+)\/(\d+).*',output)
        beforeexp=id.group(3)
        print(beforeexp)
        beforeexprec=id.group(4)
        print(beforeexprec)
        if self.sent_msgs == beforeexp and self.recvd_msgs== beforeexprec:
            self.passed('Packets are same before and after mpls lsp explicit null')
        else:
            self.failed('Packets are not same')
           



    @aetest.test
    def noexplicit_mpls(self,uut):
        '''no explicit mpls '''
        uut.configure('no mpls ldp explicit-null')

    @aetest.test
    def Verify_noexplicit_mpls(self,uut):
        # ''' Verify mpls '''
        output = uut.execute('show mpls ldp neighbor')

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
