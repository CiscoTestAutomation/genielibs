# Genie package
from genie.libs.ops.vlan.vlan import Vlan as SuperVlan


class Vlan(SuperVlan):
    '''Vlan Ops Object'''

    def learn(self):
        '''Learn Vlan object'''

        # new vlan structure
        # Place holder to make it more readable
        src_vlan = '[vlans][(?P<vlan_id>.*)]'
        dest_vlan = 'info' + src_vlan

        # interface_vlan_enabled N/A
        # vn_segment_vlan_based_enabled N/A
        # ip_igmp_snooping  N/A
        # mode N/A
        # vn_segment_id N/A

        req_key =['vlan_id','name','state','shutdown','interfaces']
        for key in req_key:
            self.add_leaf(cmd='show vlan',
                          src=src_vlan + '[{}]'.format(key),
                          dest=dest_vlan + '[{}]'.format(key))

        self.make(final_call=True)