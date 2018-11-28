''' 
Fdb Genie Ops Object for IOSXE - CLI.
'''
# Genie
from genie.ops.base import Base
from genie.ops.base import Context

# Parser
from genie.libs.parser.iosxe.show_fdb import ShowMacAddressTable, \
                                             ShowMacAddressTableAgingTime, \
                                             ShowMacAddressTableLearning


class Fdb(Base):
    '''Fdb Genie Ops Object'''

    def learn(self):
        '''Learn Fdb Ops'''
        
        ########################################################################
        #                               info
        ########################################################################

        # unsupported keys
        # maximum_entries, mac_learning (global), age

        # mac_aging_time        
        self.add_leaf(cmd=ShowMacAddressTableAgingTime,
                      src='[mac_aging_time]',
                      dest='info[mac_aging_time]')

        vlan_src = '[vlans][(?P<vlan>^\d+$)]'
        vlan_dst = 'info[mac_table][vlans][(?P<vlan>^\d+$)]'

        self.add_leaf(cmd=ShowMacAddressTableAgingTime,
                      src=vlan_src + '[mac_aging_time]',
                      dest=vlan_dst + '[mac_aging_time]')

        # mac_learning
        self.add_leaf(cmd=ShowMacAddressTableLearning,
                      src=vlan_src + '[mac_learning]',
                      dest=vlan_dst + '[mac_learning]')

        # vlan, mac_address, drop, interfaces
        self.add_leaf(cmd=ShowMacAddressTable,
                      src='[mac_table]' + vlan_src,
                      dest='info[mac_table][vlans][(?P<vlan>^\d+$)]')
        # total_mac_addresses
        self.add_leaf(cmd=ShowMacAddressTable,
                      src='[total_mac_addresses]',
                      dest='info[total_mac_addresses]')

        # make to write in cache
        self.make(final_call=True)
