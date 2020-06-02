#import statements
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

class Triggerunconfigconfigcdp(Trigger):
    ''' Config and Unconfig of cdp '''
    @aetest.setup
    def prerequisites(self,uut):
        output = uut.execute('show cdp')
        cdp_status=re.search(r'(Global\s+CDP)',output)
        print(cdp_status.group(1))
        if cdp_status.group(1) == 'Global CDP':
            self.skipped("CDP is enabled globally")
        else:
            self.failed("CDP is not enabled globally")

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
    def unconfig(self,uut):
        uut.configure('no cdp run')

    @aetest.test
    def Verify_unconfig(self,uut):
        # ''' Verify unconfig  for cdp worked or not '''
        output = uut.execute('show cdp')
        if 'Global CDP' not in output:
            self.passed("CDP is not enabled globally")
        else:
            self.failed("CDP is enabled globally")

    @aetest.test
    def config(self,uut):
        uut.configure('cdp run')

    @aetest.test
    def Verify_config(self,uut):
        # ''' Verify config for cdp worked or not '''
        output = uut.execute('show cdp')
        cdp_status=re.search(r'(Global\s+CDP)',output)
        if cdp_status.group(1) == 'Global CDP':
            self.passed("CDP is enabled globally")
        else:
            self.failed("CDP is not enabled globally")


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







