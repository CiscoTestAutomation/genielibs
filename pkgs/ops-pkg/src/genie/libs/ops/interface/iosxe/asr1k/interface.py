''' 
Interface Genie Ops Object for IOSXE - CLI.
'''

import re

# genie.libs
from ..interface import Interface as CommonInterface

# iosxe show_interface
from genie.libs.parser.iosxe.show_interface import ShowEtherchannelSummary


class Interface(CommonInterface):
    '''Interface Genie Ops Object'''

    def learn(self):
        '''Learn Interface Ops'''
        
        # ======================================================================
        #                           common keys
        # ======================================================================
        super().learn()  

        # switchport_enable   -- default values
        if hasattr(self, 'info'):
            for intf in self.info:
                self.info[intf]['switchport_enable'] = False


        # ======================================================================
        #                           switchport related
        # ======================================================================
        # Global source
        src = '[interfaces][(?P<interface>.*)][port_channel]'
        dest = 'info[(?P<interface>.*)][port_channel]'

        # vlan_id
        for key in ['port_channel_member_intfs', 'port_channel_int']:
            self.add_leaf(cmd=ShowEtherchannelSummary,
                          src=src + '[{}]'.format(key),
                          dest=dest + '[{}]'.format(key))

        self.make()

        # overwrite the port_channel_member
        if hasattr(self, 'info'):
            for intf in self.info:
                if 'port_channel' not in self.info[intf]:
                    continue
                if ('port_channel_int' in self.info[intf]['port_channel'] and \
                    self.info[intf]['port_channel']['port_channel_int']) or \
                   ('port_channel_member_intfs' in self.info[intf]['port_channel'] and \
                    self.info[intf]['port_channel']['port_channel_member_intfs']):
                    self.info[intf]['port_channel']['port_channel_member'] = True
