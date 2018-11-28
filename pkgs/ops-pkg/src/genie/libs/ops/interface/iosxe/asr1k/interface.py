''' 
Interface Genie Ops Object for IOSXE - CLI.
'''

import re

# genie.libs
from ..interface import Interface as CommonInterface

# iosxe show_interface
from genie.libs.parser.iosxe.show_lag import ShowEtherchannelSummary


class Interface(CommonInterface):
    '''Interface Genie Ops Object'''

    def learn(self, custom=None):
        '''Learn Interface Ops'''
        
        # ======================================================================
        #                           common keys
        # ======================================================================
        super().learn(custom)

        # switchport_enable   -- default values
        if hasattr(self, 'info'):
            for intf in self.info:
                self.info[intf]['switchport_enable'] = False


        # ======================================================================
        #                           switchport related
        # ======================================================================
        # Global source
        # port-channel interfaces
        src = '[interfaces][(?P<interface>.*)][port_channel]'
        dest = 'info[(?P<interface>.*)][port_channel]'

        # vlan_id
        for key in ['port_channel_member_intfs', 'port_channel_member']:
            self.add_leaf(cmd=ShowEtherchannelSummary,
                          src=src + '[{}]'.format(key),
                          dest=dest + '[{}]'.format(key))

        # Ethernet interfaces
        src = '[interfaces][(?P<port_intf>.*)][members][(?P<interface>.*)][port_channel]'
        dest = 'info[(?P<interface>.*)][port_channel]'

        # vlan_id
        for key in ['port_channel_int', 'port_channel_member']:
            self.add_leaf(cmd=ShowEtherchannelSummary,
                          src=src + '[{}]'.format(key),
                          dest=dest + '[{}]'.format(key))

        self.make(final_call=True)
