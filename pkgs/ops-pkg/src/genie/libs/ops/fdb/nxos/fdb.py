''' 
Fdb Genie Ops Object for IOSXE - CLI.
'''
# Genie
from genie.libs.ops.fdb.fdb import Fdb as SuperFdb
from genie.libs.parser.nxos.show_fdb import (ShowMacAddressTable,
                                             ShowMacAddressTableAgingTime)
from genie.libs.parser.nxos.show_system import ShowSystemInternalL2fwderMac


class Fdb(SuperFdb):
    '''Fdb Genie Ops Object'''

    def learn(self, address=None, interface=None, vlan=None):
        '''Learn Fdb Ops'''
        
        ########################################################################
        #                               info
        ########################################################################
        # mac_learning                              N/A
        # mac_aging_time
        # maximum_entries                           N/A
        # mac_table
        #     vlans
        #         vlan
        #             vlan
        #             mac_learning                  N/A
        #             mac_aging_time                N/A
        #             mac_addresses
        #                 mac_address
        #                     mac_address
        #                     drop
        #                         drop
        #                         age
        #                         entry_type
        #                     interfaces
        #                         interface
        #                             interface
        #                             age
        #                             entry_type
        #     total_mac_addresses                   N/A

        self.add_leaf(cmd=ShowMacAddressTableAgingTime,
                      src='[mac_aging_time]',
                      dest='info[mac_aging_time]')

        vlan_src = '[mac_table][vlans][(?P<vlan>^\d+$)]'
        vlan_dst = 'info[mac_table][vlans][(?P<vlan>^\d+$)]'
        self.add_leaf(cmd=ShowMacAddressTable,
                      src=vlan_src + '[vlan]',
                      dest=vlan_dst + '[vlan]',
                      address=address,
                      interface=interface,
                      vlan=vlan)
        self.add_leaf(cmd=ShowSystemInternalL2fwderMac,
                      src=vlan_src + '[vlan]',
                      dest=vlan_dst + '[vlan]')

        #             mac_addresses
        #                 mac_address
        #                     mac_address
        mac_address_src = vlan_src + '[mac_addresses][(?P<mac_address>.*)]'
        mac_address_dst = vlan_dst + '[mac_addresses][(?P<mac_address>.*)]'
        self.add_leaf(cmd=ShowMacAddressTable,
                      src=mac_address_src + '[mac_address]',
                      dest=mac_address_dst + '[mac_address]',
                      address=address,
                      interface=interface,
                      vlan=vlan)
        self.add_leaf(cmd=ShowSystemInternalL2fwderMac,
                      src=mac_address_src + '[mac_address]',
                      dest=mac_address_dst + '[mac_address]')

        #                     drop
        #                         drop
        #                         age
        #                         entry_type
        drop_src = mac_address_src + '[drop]'
        drop_dst = mac_address_dst + '[drop]'
        for key in ['[drop]', '[age]', '[mac_type]']:
            if key == '[mac_type]':
                dst_key = '[entry_type]'
            else:
                dst_key = key

            self.add_leaf(cmd=ShowMacAddressTable,
                          src=drop_src + key,
                          dest=drop_dst + dst_key,
                          address=address,
                          interface=interface,
                          vlan=vlan)
            self.add_leaf(cmd=ShowSystemInternalL2fwderMac,
                          src=drop_src + key,
                          dest=drop_dst + dst_key)

        #                     interfaces
        #                         interface
        #                             interface
        #                             age
        #                             entry_type
        interface_src = mac_address_src + '[interfaces][(?P<interface>.*)]'
        interface_dst = mac_address_dst + '[interfaces][(?P<interface>.*)]'
        for key in ['[interface]', '[age]', '[mac_type]']:
            if key == '[mac_type]':
                dst_key = '[entry_type]'
            else:
                dst_key = key

            self.add_leaf(cmd=ShowMacAddressTable,
                          src=interface_src + key,
                          dest=interface_dst + dst_key,
                          address=address,
                          interface=interface,
                          vlan=vlan)
            self.add_leaf(cmd=ShowSystemInternalL2fwderMac,
                          src=interface_src + key,
                          dest=interface_dst + dst_key)




        # make to write in cache
        self.make(final_call=True)
