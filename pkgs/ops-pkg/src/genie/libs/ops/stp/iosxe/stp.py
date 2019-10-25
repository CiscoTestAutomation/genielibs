''' 
Spanning-tree Genie Ops Object for IOSXE - CLI.
'''
# Genie
from genie.libs.ops.stp.stp import Stp as SuperStp
from genie.ops.base import Context


class Stp(SuperStp):
    '''Spanning-tree Genie Ops Object'''

    def choose_one_max_hop(self, item):
        '''return max_hops value from one of the mst_instances'''
        for inst, i_dict in item.items():
            if 'configured' in i_dict:
                return i_dict['configured'].get('max_hops')

    def learn(self):
        '''Learn Spanning-tree Ops'''
        
        ########################################################################
        #                               info
        ########################################################################
        # bridge_assurance is from show run

        # etherchannel_misconfig_guard
        # loop_guard, bpdu_guard, bpdu_filter
        for key in ['etherchannel_misconfig_guard',
                    'loop_guard', 'bpdu_guard', 'bpdu_filter']:
            self.add_leaf(cmd='show spanning-tree summary',
                          src='[%s]' % key,
                          dest='info[global][%s]' % key)

        # bpduguard_timeout_recovery
        self.add_leaf(cmd='show errdisable recovery',
                      src='[bpduguard_timeout_recovery]',
                      dest='info[global][bpduguard_timeout_recovery]')

        # ----------------- Mode Attributes --------------------------
        # # max_hop  --- only for mode mstp
        self.add_leaf(cmd='show spanning-tree mst detail',
                      src='[mst_instances]',
                      dest='info[mstp][default][max_hop]',
                      action=self.choose_one_max_hop)

        # name, revision
        for key in ['name', 'revision']:
            self.add_leaf(cmd='show spanning-tree mst configuration',
                          src='[(?P<mode>.*)][%s]' % key,
                          dest='info[(?P<mode>.*)][default][%s]' % key)

        # hello_time, max_age, forwarding_delay, hold_count
        for key in ['hello_time', 'max_age', 'forwarding_delay', 'hold_count']:
            self.add_leaf(cmd='show spanning-tree detail',
                          src='[(?P<mode>.*)][%s]' % key,
                          dest='info[(?P<mode>.*)][default][%s]' % key)
            self.add_leaf(cmd='show spanning-tree detail',
                          src='[(?P<mode_vlan>(pvst|rapid_pvst))][vlans][(?P<vlans>.*)][%s]' % key,
                          dest='info[(?P<mode_vlan>(pvst|rapid_pvst))][default][vlans][(?P<vlans>.*)][%s]' % key)

        # ----------------- Instance/Vlans Attributes -----------------
        # mst_id, vlan, bridge_priority, bridge_address, topology_changes,
        # time_since_topology_change, hold_time
        src = '[(?P<mode>.*)][(?P<mode_inst_type>.*)][(?P<inst>.*)]'
        dest = 'info[(?P<mode>.*)][default][(?P<mode_inst_type>.*)][(?P<inst>.*)]'
        for key in ['mst_id', 'vlan', 'vlan_id', 'bridge_priority', 'bridge_address',
                    'topology_changes', 'time_since_topology_change', 'hold_time']:
            self.add_leaf(cmd='show spanning-tree detail',
                          src=src + '[%s]' % key,
                          dest=dest + '[%s]' % key)
        # mstp vlan
        self.add_leaf(cmd='show spanning-tree mst detail',
                      src='[mst_instances][(?P<inst>.*)][vlan]',
                      dest='info[mstp][default][mst_instances][(?P<inst>.*)][vlan]')


        # designated_root_priority, designated_root_address,root_port, root_cost,
        root_map_dict = {"cost": 'root_cost', 'port': 'root_port',
                         'priority': 'designated_root_priority',
                         'address': 'designated_root_address'}
        for key_src, key_dest in root_map_dict.items():
            self.add_leaf(cmd='show spanning-tree',
                          src=src + '[root][%s]' % key_src,
                          dest=dest + '[%s]' % key_dest)

        for key in ['configured_bridge_priority', 'sys_id_ext']:
            self.add_leaf(cmd='show spanning-tree',
                          src=src + '[bridge][%s]' % key,
                          dest=dest + '[%s]' % key)


        # ----------------- Instance/Vlans Interfaces Attributes ------
        # name, cost, port_priority, port_num, designated_root_priority, 
        # designated_root_address, designated_cost, designated_bridge_priority,
        # designated_bridge_address, forward_transitions, counters

        src = '[(?P<mode>.*)][(?P<mode_inst_type>.*)][(?P<inst>.*)][interfaces][(?P<intf>.*)]'
        dest = 'info[(?P<mode>.*)][default][(?P<mode_inst_type>.*)][(?P<inst>.*)][interfaces][(?P<intf>.*)]'

        intf_Keys = ['name', 'cost', 'port_priority', 'port_num', 'designated_root_priority',
                     'designated_root_address', 'designated_bridge_priority',
                     'designated_bridge_address', 'counters']

        for key in intf_Keys:
            self.add_leaf(cmd='show spanning-tree detail',
                          src=src + '[%s]' % key,
                          dest=dest + '[%s]' % key)

        for src_key, dest_key in {'number_of_forward_transitions':'forward_transitions',
                                  'designated_path_cost': 'designated_cost'}.items():
            self.add_leaf(cmd='show spanning-tree detail',
                          src=src + '[%s]' % src_key,
                          dest=dest + '[%s]' % dest_key)

        # role, port_state, designated_port_priority, designated_port_num
        for key in ['role', 'port_state']:
            self.add_leaf(cmd='show spanning-tree',
                          src=src + '[{}]'.format(key),
                          dest=dest + '[{}]'.format(key))

        for src_key, dest_key in {'port_priority': 'designated_port_priority',
                                  'port_num': 'designated_port_num'}.items():
            self.add_leaf(cmd='show spanning-tree',
                          src=src + '[{}]'.format(src_key),
                          dest=dest + '[{}]'.format(dest_key))

        # make to write in cache
        self.make(final_call=True)

        # pvst_id  domain
        if hasattr(self, 'info'):
            self.info['mstp']['default'].setdefault('domain', 'default') \
                if 'mstp' in self.info else None
            self.info['pvst']['default'].setdefault('pvst_id', 'default') \
                if 'pvst' in self.info else None
            self.info['rapid_pvst']['default'].setdefault('pvst_id', 'default') \
                if 'rapid_pvst' in self.info else None