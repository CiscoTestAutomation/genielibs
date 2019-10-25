''' 
Fdb Genie Ops Object for IOSXE - CLI.
'''
# Genie
from genie.libs.ops.fdb.fdb import Fdb as SuperFdb
from genie.ops.base import Context


class Fdb(SuperFdb):
    '''Fdb Genie Ops Object'''

    def learn(self):
        '''Learn Fdb Ops'''
        
        ########################################################################
        #                               info
        ########################################################################

        # unsupported keys
        # maximum_entries, mac_learning (global), age

        # mac_aging_time        
        self.add_leaf(cmd='show mac address-table aging-time',
                      src='[mac_aging_time]',
                      dest='info[mac_aging_time]')

        vlan_src = '[vlans][(?P<vlan>^\d+$)]'
        vlan_dst = 'info[mac_table][vlans][(?P<vlan>^\d+$)]'

        self.add_leaf(cmd='show mac address-table aging-time',
                      src=vlan_src + '[mac_aging_time]',
                      dest=vlan_dst + '[mac_aging_time]')

        # mac_learning
        self.add_leaf(cmd='show mac address-table learning',
                      src=vlan_src + '[mac_learning]',
                      dest=vlan_dst + '[mac_learning]')

        # vlan, mac_address, drop, interfaces
        self.add_leaf(cmd='show mac address-table',
                      src='[mac_table]' + vlan_src,
                      dest='info[mac_table][vlans][(?P<vlan>^\d+$)]')
        # total_mac_addresses
        self.add_leaf(cmd='show mac address-table',
                      src='[total_mac_addresses]',
                      dest='info[total_mac_addresses]')

        # make to write in cache
        self.make(final_call=True)
