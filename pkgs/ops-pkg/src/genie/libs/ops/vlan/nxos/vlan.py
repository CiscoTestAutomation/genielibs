# Genie package
from genie.libs.ops.vlan.vlan import Vlan as SuperVlan

# genie.libs
#from genie.libs.parser.nxos import show_vlan, \
#                                   show_interface
from genie.libs.parser.nxos import show_vlan,\
                        show_feature,\
                        show_igmp,\
                        show_interface


class Vlan(SuperVlan):
    '''Vlan Ops Object'''
    
    def set_enable(self, item):
        try:
            for inst in item:
                if item[inst]['state'] == 'enabled':
                    ret_val = True
                    break
                else:
                    ret_val = False
                    continue
        except:
            ret_val = False
        return ret_val

    def transfer_to_bool(self, item):
        if 'active' not in item:
            return True
        else:
            return False

    def learn(self):
        '''Learn Vlan object'''

        # new vlan structure
        # Place holder to make it more readable
        src_vlan = '[feature]'
        dest_vlan = 'info[vlans]'

        self.add_leaf(cmd=show_feature.ShowFeature,
                      src=src_vlan + '[interface-vlan][instance]',
                      dest=dest_vlan + '[interface_vlan_enabled]',
                      action=self.set_enable)

        self.add_leaf(cmd=show_feature.ShowFeature,
                      src=src_vlan + '[vnseg_vlan][instance]',
                      dest=dest_vlan + '[vn_segment_vlan_based_enabled]',
                      action=self.set_enable)

        src_vlan = '[vlans][(?P<vlan_id>.*)]'
        dest_vlan = 'info[vlans][(?P<vlan_id>.*)]'

        req_keys = ['vlan_id','name','state','interfaces','mode']
        for key in req_keys:
            self.add_leaf(cmd=show_vlan.ShowVlan,
                          src=src_vlan + '[{}]'.format(key),
                          dest=dest_vlan + '[{}]'.format(key))

        # shutdown
        self.add_leaf(cmd=show_vlan.ShowVlan,
                      src=src_vlan + '[state]',
                      dest=dest_vlan + '[shutdown]',
                      action=self.transfer_to_bool)

        self.add_leaf(cmd=show_vlan.ShowVlanIdVnSegment,
                      src=src_vlan + '[vn_segment_id]',
                      dest=dest_vlan + '[vn_segment_id]')

        src_igmp = '[vlans]'
        dest_igmp = 'info[vlans]'
        self.add_leaf(cmd=show_igmp.ShowIpIgmpSnooping,
                      src=src_igmp + '[(?P<configuration_vlan_id>.*)][ip_igmp_snooping]',
                      dest=dest_igmp + '[configuration][(?P<configuration_vlan_id>.*)][ip_igmp_snooping]')

        self.make(final_call=True)
