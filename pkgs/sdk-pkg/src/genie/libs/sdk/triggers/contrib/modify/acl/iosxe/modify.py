
#acl modify trigger
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

import re
# Genie
from genie.harness.exceptions import GenieConfigReplaceWarning
import pprint
# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig

class Triggermodifyacl(Trigger):
    @aetest.setup
    def prerequisites(self,uut,aclname):
        #To verify acl
        output = uut.parse('show access-lists '+aclname)
        pprint.pprint(output)
#        self.passed('acl parsing',pprint.pprint(output))
        if output:
            self.skipped('ACL configs are there')

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
    def modify_acl(self,uut,aclname):
        uut.configure('''\
ip access-list extended {acl_n}
no 1022 permit tcp any eq 18000 any eq ftp-data'''.format(acl_n=aclname))

    @aetest.test
    def Verify_modify_acl(self,uut,aclname):
        output = uut.parse('show access-lists '+aclname)
#        if output:
#            self.passed("mpls ldp neighbors are there")

    @aetest.test
    def remove_acl_modify(self,uut,aclname):
        uut.configure('''\
ip access-list extended {acl_n}
1022 deny tcp any eq 18000 any eq ftp-data'''.format(acl_n=aclname))
#        uut.configure('''\
#ip access-list extended {acl_n}
#1022 permit tcp any eq 18000 any eq ftp-data'''.format(acl_n=aclname))

    @aetest.test
    def Verify_remove_acl_modify(self,uut,aclname):
        output = uut.execute('show access-lists '+aclname)
#        if not output:
#            self.passed("No neighbors for mpls and ldp")

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






