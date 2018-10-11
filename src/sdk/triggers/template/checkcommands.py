'''TriggerCheckCommands template'''

from ats import aetest
from genie.harness.base import Trigger


class TriggerCheckCommands(Trigger):
    ''' Template for all TriggerCheckCommands triggers
    '''

    @aetest.setup
    def stack_show_switch(self):
        raise NotImplementedError

    @aetest.test
    def verify_show_inventory(self):
        raise NotImplementedError
        
    @aetest.test
    def verify_show_version(self):
        raise NotImplementedError

    @aetest.test
    def stack_ha_redundancy_state(self):
        raise NotImplementedError
        
    @aetest.test
    def verify_show_module(self):
        raise NotImplementedError
        
    @aetest.test
    def verify_show_environment(self):
        raise NotImplementedError        
        
    @aetest.test
    def verify_show_platform(self):
        raise NotImplementedError

    @aetest.test
    def verify_show_power_inline(self):
        raise NotImplementedError

