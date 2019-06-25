''' 
Interface Genie Ops Object for IOSXE - CLI.
'''

import re

# genie.libs
from ..interface import Interface as CommonInterface

# iosxe show_interface
from genie.libs.parser.iosxe.show_interface import ShowInterfacesSwitchport


class Interface(CommonInterface):
    '''Interface Genie Ops Object'''

    def learn(self, interface='', address_family='', custom=None):
        '''Learn Interface Ops'''
        
        # ======================================================================
        #                           common keys
        # ======================================================================
        super().learn(custom=custom, interface=interface, address_family=address_family)
        if hasattr(self, 'info'):
            for intf in self.info:
                if 'switchport_enable' in self.info[intf] and self.info[intf]['switchport_enable']== False:
                    self.info[intf].pop('switchport_enable')

        # ======================================================================
        #                           switchport related
        # ======================================================================
        # Global source
        src = '[(?P<interface>.*)]'
        dest = 'info[(?P<interface>.*)]'

        # vlan_id
        self.add_leaf(cmd=ShowInterfacesSwitchport,
                      src=src + '[access_vlan]',
                      dest=dest + '[vlan_id]',
                      interface=interface)

        req_keys = ['access_vlan', 'trunk_vlans', 'switchport_mode',
                    'switchport_enable', 'operational_mode']

        for key in req_keys:
            self.add_leaf(cmd=ShowInterfacesSwitchport,
                          src=src + '[{}]'.format(key),
                          dest=dest + '[{}]'.format(key),
                          interface=interface)

        # create overwrite keys for port_channel
        self.add_leaf(cmd=ShowInterfacesSwitchport,
                      src=src + '[port_channel]',
                      dest=dest + '[overwrite_port_channel]',
                      interface=interface)

        # ======================================================================
        #                           encapsulation
        # ======================================================================
        # Global source
        dest = 'info[(?P<interface>.*)][encapsulation]'

        # native_vlan
        self.add_leaf(cmd=ShowInterfacesSwitchport,
                      src='[(?P<interface>.*)][encapsulation][native_vlan]',
                      dest=dest + '[native_vlan]',
                      interface=interface)
        # make
        self.make(final_call=True)

        # calculate the switchport switch_enable
        if hasattr(self, 'info'):
            for intf in self.info:
                # switchport_enable is False if not in the intf dict
                if 'switchport_enable' not in self.info[intf]:
                    self.info[intf]['switchport_enable'] = False

                # switchport_enable is False when intf switchport operational_mode is down
                if 'operational_mode' in self.info[intf]:

                    if self.info[intf]['operational_mode'] == 'down':
                        self.info[intf]['switchport_enable'] = False

                    # delete operational_mode which ops does not need
                    del(self.info[intf]['operational_mode'])
                else:
                    self.info[intf]['switchport_enable'] = False

                # overwrite port_channel from show interface switchport
                if 'overwrite_port_channel' in self.info[intf]:

                    self.info[intf]['port_channel'].update(self.info[intf]['overwrite_port_channel'])

                    # delete overwrite_port_channel which ops does not need
                    del(self.info[intf]['overwrite_port_channel'])