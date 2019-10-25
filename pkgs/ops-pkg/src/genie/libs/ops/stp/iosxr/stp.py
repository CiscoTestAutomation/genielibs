''' 
Stp Genie Ops Object for IOSXR - CLI.
'''
# Genie
from genie.libs.ops.stp.stp import Stp as SuperStp
from genie.ops.base import Context

# Parser
from genie.libs.parser.iosxr.show_spanning_tree import ShowSpanningTreeMst, \
                                        ShowSpanningTreeMstag, \
                                        ShowSpanningTreePvrst, \
                                        ShowSpanningTreePvrsTag, \
                                        ShowSpanningTreePvsTag

class Stp(SuperStp):
    '''STP Genie Ops Object'''

    def learn(self, mst_domain=None, mstag_domain=None, pvst_id=None, pvrstag_domain=None, pvstag_domain=None):
        '''Learn stp Ops'''

        ########################################################################
        #                               info
        ########################################################################
        #      global - N/A
        #         bridge_assurance - N/A
        #         etherchannel_misconfig_guard - N/A
        #         bpduguard_timeout_recovery - N/A
        #         loop_guard - N/A
        #         bpdu_guard - N/A
        #         bpdu_filter - N/A
        #      mstp
        #         mst_domain
        #             domain - N/A
        #             name - N/A
        #             revision - N/A
        #             max_hop - N/A
        #             hello_time - N/A
        #             max_age - N/A
        #             forwarding_delay - N/A
        #             hold_count - N/A
        #             mst_instances
        #                 mst_id
        #                     mst_id
        #                     vlan
        #                     bridge_priority
        #                     bridge_address
        #                     designated_root_priority
        #                     designated_root_address
        #                     root_port - N/A
        #                     root_cost
        #                     hold_time - N/A
        #                     topology_changes - N/A
        #                     time_since_topology_change - N/A
        #                     interfaces
        #                         m_interface
        #                             name
        #                             cost
        #                             port_priority
        #                             port_num
        #                             role
        #                             port_state
        #                             designated_root_priority - N/A
        #                             designated_root_address - N/A
        #                             designated_cost - N/A
        #                             designated_bridge_priority
        #                             designated_bridge_address
        #                             designated_port_priority
        #                             designated_port_num
        #                             forward_transitions - N/A
        #                             counters - N/A
        #                                 bpdu_sent - N/A
        #                                 bpdu_received - N/A
        #             interfaces - N/A
        #                 m_interface - N/A
        #                     name - N/A
        #                     edge_port - N/A
        #                     link_type - N/A
        #                     guard - N/A
        #                     bpdu_guard - N/A
        #                     bpdu_filter - N/A
        #     mstag
        #         mag_domain
        #             domain
        #             interfaces
        #                 mag_interface
        #                     interface
        #                     name
        #                     revision
        #                     bridge_id
        #                     preempt_delay
        #                     preempt_delay_state - N/A
        #                     max_age
        #                     provider_bridge
        #                     port_id
        #                     external_cost
        #                     hello_time
        #                     active
        #                     counters - N/A
        #                         bpdu_sent - N/A
        #                 instances
        #                     mag_id
        #                         instance
        #                         root_id
        #                         vlans
        #                         priority
        #                         root_priority
        #                         port_priority
        #                         cost
        #                         counters
        #                             topology_changes
        #     pvst
        #         pvst_id
        #             pvst_id
        #             max_age - N/A
        #             hold_count - N/A
        #             forwarding_delay - N/A
        #             hello_time - N/A
        #             vlans
        #                 vlan_id
        #                     vlan_id
        #                     hello_time - N/A
        #                     max_age - N/A
        #                     forwarding_delay - N/A
        #                     bridge_priority
        #                     configured_bridge_priority - N/A
        #                     sys_id_ext
        #                     bridge_address
        #                     designated_root_priority
        #                     designated_root_address
        #                     root_port - N/A
        #                     root_cost - N/A
        #                     hold_time - N/A
        #                     topology_changes - N/A
        #                     time_since_topology_change - N/A
        #                     interface
        #                         v_interface
        #                             name
        #                             cost
        #                             port_priority
        #                             port_num
        #                             role
        #                             port_state
        #                             designated_root_priority - N/A
        #                             designated_root_address - N/A
        #                             designated_cost - N/A
        #                             designated_bridge_priority
        #                             designated_bridge_address
        #                             designated_port_priority
        #                             designated_port_num
        #                             forward_transitions - N/A
        #                             counters - N/A
        #                                 bpdu_sent - N/A
        #                                 bpdu_received - N/A
        #             interfaces - N/A
        #                 p_interface - N/A
        #                     name - N/A
        #                     edge_port - N/A
        #                     link_type - N/A
        #                     guard - N/A
        #                     bpdu_guard - N/A
        #                     bpdu_filter - N/A
        #                     hello_time - N/A
        #     rapid_pvst - N/A
        #         pvst_id - N/A
        #             pvst_id - N/A
        #             max_age - N/A
        #             hold_count - N/A
        #             forwarding_delay - N/A
        #             hello_time - N/A
        #             vlans - N/A
        #                 vlan_id - N/A
        #                     vlan_id - N/A
        #                     hello_time - N/A
        #                     max_age - N/A
        #                     forwarding_delay - N/A
        #                     bridge_priority - N/A
        #                     configured_bridge_priority - N/A
        #                     sys_id_ext - N/A
        #                     bridge_address - N/A
        #                     designated_root_priority - N/A
        #                     designated_root_address - N/A
        #                     root_port - N/A
        #                     root_cost - N/A
        #                     hold_time - N/A
        #                     topology_changes - N/A
        #                     time_since_topology_change - N/A
        #                     interface - N/A
        #                         v_interface - N/A
        #                             name - N/A
        #                             cost - N/A
        #                             port_priority - N/A
        #                             port_num - N/A
        #                             role - N/A
        #                             port_state - N/A
        #                             designated_root_priority - N/A
        #                             designated_root_address - N/A
        #                             designated_cost - N/A
        #                             designated_bridge_priority - N/A
        #                             designated_bridge_address - N/A
        #                             designated_port_priority - N/A
        #                             designated_port_num - N/A
        #                             forward_transitions - N/A
        #                             counters - N/A
        #                                 bpdu_sent - N/A
        #                                 bpdu_received - N/A
        #             interfaces - N/A
        #                 p_interface - N/A
        #                     name - N/A
        #                     edge_port - N/A
        #                     link_type - N/A
        #                     guard - N/A
        #                     bpdu_guard - N/A
        #                     bpdu_filter - N/A
        #                     hello_time - N/A
        #     pvrstag
        #         prag_domain
        #             domain
        #             interfaces
        #                 prag_interface
        #                     interface
        #                     vlans
        #                         prag_vlan
        #                             root_priority
        #                             root_id - N/A
        #                             root_cost
        #                             priority - N/A
        #                             bridge_id
        #                             port_priority
        #                             max_age
        #                             hello_time
        #                             preempt_delay
        #                             preempt_delay_state
        #                             sub_interface
        #                             sub_interface_state
        #                             port_id
        #                             active
        #                             counters
        #                                 bpdu_sent - N/A
        #                                 topology_changes
        #     pvstag
        #         pag_domain
        #             domain
        #             interfaces
        #                 pag_interface
        #                     interface
        #                     vlans
        #                         pag_vlan
        #                             root_priority
        #                             root_id - N/A
        #                             root_cost
        #                             priority - N/A
        #                             bridge_id
        #                             port_priority
        #                             max_age
        #                             hello_time
        #                             preempt_delay
        #                             preempt_delay_state
        #                             sub_interface
        #                             sub_interface_state
        #                             port_id
        #                             active
        #                             counters
        #                                 bpdu_sent - N/A
        #                                 topology_changes

        mstp_domain_instances_src = '[mstp][(?P<mstp_domain>.*)][mst_instances][(?P<mst_id>.*)]'
        mstp_domain_instances_des = 'info[mstp][(?P<mstp_domain>.*)][mst_instances][(?P<mst_id>.*)]'

        if mst_domain:
            for key in ['mst_id', 'vlan', 'bridge_priority',
                'bridge_address' ,
                'designated_root_priority', 'designated_root_address', 'root_cost', 
                ]:

                self.add_leaf(cmd=ShowSpanningTreeMst,
                                src=mstp_domain_instances_src + '[%s]' % key,
                                dest=mstp_domain_instances_des + '[%s]' % key,
                                mst=mst_domain)

        mstp_domain_interfaces_src = mstp_domain_instances_src + '[interfaces][(?P<m_interface>.*)]'
        mstp_domain_interfaces_des = mstp_domain_instances_des + '[interfaces][(?P<m_interface>.*)]'

        if mst_domain:
            for key in ['name', 'cost', 'port_priority', 'port_num', 'role', 
                'port_state', 'designated_cost', 'designated_bridge_priority',
                'designated_bridge_address', 'designated_port_priority', 
                'designated_port_num']:

                self.add_leaf(cmd=ShowSpanningTreeMst,
                            src=mstp_domain_interfaces_src + '[%s]' % key,
                            dest=mstp_domain_interfaces_des + '[%s]' % key,
                            mst=mst_domain)

        mstag_src = '[mstag][(?P<mstag>.*)]'
        mstag_des = 'info[mstag][(?P<mstag>.*)]'

        if mstag_domain:
            self.add_leaf(cmd=ShowSpanningTreeMstag,
                        src=mstag_src + '[domain]',
                        dest=mstag_des + '[domain]',
                        mag_domain=mstag_domain)

        mstag_interfaces_src = mstag_src + '[interfaces][(?P<m_interface>.*)]'
        mstag_interfaces_des = mstag_des + '[interfaces][(?P<m_interface>.*)]'
        
        if mstag_domain:
            for key in ['interface', 'preempt_delay', 'name', 'revision' , 'max_age', 
                'provider_bridge', 'bridge_id', 'port_id', 'external_cost', 'hello_time',
                'active']:
                self.add_leaf(cmd=ShowSpanningTreeMstag,
                        src=mstag_interfaces_src + '[%s]' % key,
                        dest=mstag_interfaces_des + '[%s]' % key,
                        mag_domain=mstag_domain)

        mstag_instances_src = mstag_src + '[interfaces][instances][(?P<m_instance>.*)]'
        mstag_instances_des = mstag_des + '[interfaces][instances][(?P<m_instance>.*)]'
        
        if mstag_domain:
            for key in ['instance', 'vlans', 'priority', 'port_priority', 'cost',
                'root_priority']:
                self.add_leaf(cmd=ShowSpanningTreeMstag,
                        src=mstag_instances_src + '[%s]' % key,
                        dest=mstag_instances_des + '[%s]' % key,
                        mag_domain=mstag_domain)

            self.add_leaf(cmd=ShowSpanningTreeMstag,
                        src= mstag_instances_src + '[counters][topology_changes]',
                        dest=mstag_instances_des + '[counters][topology_changes]',
                        mag_domain=mstag_domain)
        
        pvst_src = '[pvst][(?P<pvst>.*)]'
        pvst_des = 'info[pvst][(?P<pvst>.*)]'

        if pvst_id:
            self.add_leaf(cmd=ShowSpanningTreePvrst,
                        src= pvst_src + '[pvst_id]',
                        dest=pvst_des + '[pvst_id]',
                        pvst_id=pvst_id)

        pvst_vlans_src = pvst_src + '[vlans][(?P<vlans>.*)]'
        pvst_vlans_des = pvst_des + '[vlans][(?P<vlans>.*)]'
        if pvst_id:
            for key in ['vlan_id', 'designated_root_priority', 'designated_root_address',
                'bridge_priority', 'sys_id_ext', 'bridge_address']:
                self.add_leaf(cmd=ShowSpanningTreePvrst,
                        src=pvst_vlans_src + '[%s]' % key,
                        dest=pvst_vlans_des + '[%s]' % key,
                        pvst_id=pvst_id)

        pvst_vlans_interface_src = pvst_vlans_src + '[interface][(?P<m_interface>.*)]'
        pvst_vlans_interface_des = pvst_vlans_des + '[interface][(?P<m_interface>.*)]'
        if pvst_id:
            for key in ['name', 'cost', 'role', 'port_priority', 'port_num', 'port_state',
                'designated_bridge_priority', 'designated_bridge_address', 
                'designated_port_priority', 'designated_port_num']:
                self.add_leaf(cmd=ShowSpanningTreePvrst,
                        src=pvst_vlans_interface_src + '[%s]' % key,
                        dest=pvst_vlans_interface_des + '[%s]' % key,
                        pvst_id=pvst_id)

        pvrstag_src = '[pvrstag][(?P<pvrstag>.*)]'
        pvrstag_des = 'info[pvrstag][(?P<pvrstag>.*)]'
        if pvrstag_domain:
            self.add_leaf(cmd=ShowSpanningTreePvrsTag,
                        src=pvrstag_src + '[domain]',
                        dest=pvrstag_des + '[domain]',
                        pvrstag_domain=pvrstag_domain)

        pvrstag_interfaces_src = pvrstag_src + '[interfaces][(?P<m_interface>.*)]'
        pvrstag_interfaces_des = pvrstag_des + '[interfaces][(?P<m_interface>.*)]'
        if pvrstag_domain:
            self.add_leaf(cmd=ShowSpanningTreePvrsTag,
                        src=pvrstag_interfaces_src + '[interface]',
                        dest=pvrstag_interfaces_des + '[interface]',
                        pvrstag_domain=pvrstag_domain)

        pvrstag_vlans_src = pvrstag_interfaces_src + '[vlans][(?P<vlans>.*)]'
        pvrstag_vlans_des = pvrstag_interfaces_des  + '[vlans][(?P<vlans>.*)]'
        if pvrstag_domain:
            for key in ['preempt_delay', 'preempt_delay_state', 'sub_interface', 
                'sub_interface_state', 'max_age', 'root_priority', 
                'root_cost', 'bridge_id', 'port_priority', 
                'port_id', 'hello_time', 'active']:
                self.add_leaf(cmd=ShowSpanningTreePvrsTag,
                        src=pvrstag_vlans_src + '[%s]' % key,
                        dest=pvrstag_vlans_des + '[%s]' % key,
                        pvrstag_domain=pvrstag_domain)

            self.add_leaf(cmd=ShowSpanningTreePvrsTag,
                        src= pvrstag_vlans_src + '[counters][topology_changes]',
                        dest=pvrstag_vlans_des + '[counters][topology_changes]',
                        pvrstag_domain=pvrstag_domain)

        pvstag_src = '[pvstag][(?P<pvrstag>.*)]'
        pvstag_des = 'info[pvstag][(?P<pvrstag>.*)]'
        if pvstag_domain:
            self.add_leaf(cmd=ShowSpanningTreePvsTag,
                        src=pvstag_src + '[domain]',
                        dest=pvstag_des + '[domain]',
                        pvstag_domain=pvstag_domain)

        pvstag_interfaces_src = pvstag_src + '[interfaces][(?P<m_interface>.*)]'
        pvstag_interfaces_des = pvstag_des + '[interfaces][(?P<m_interface>.*)]'

        if pvstag_domain:
            self.add_leaf(cmd=ShowSpanningTreePvsTag,
                        src=pvstag_interfaces_src + '[interface]',
                        dest=pvstag_interfaces_des + '[interface]',
                        pvstag_domain=pvstag_domain)

        pvstag_vlans_src = pvstag_interfaces_src + '[vlans][(?P<vlans>.*)]'
        pvstag_vlans_des = pvstag_interfaces_des  + '[vlans][(?P<vlans>.*)]'
        if pvstag_domain:
            for key in ['preempt_delay', 'preempt_delay_state', 'sub_interface', 
                'sub_interface_state', 'max_age', 'root_priority',
                'root_cost', 'bridge_id', 'port_priority', 
                'port_id', 'hello_time', 'active']:
                self.add_leaf(cmd=ShowSpanningTreePvsTag,
                        src=pvstag_vlans_src + '[%s]' % key,
                        dest=pvstag_vlans_des + '[%s]' % key,
                        pvstag_domain=pvstag_domain)

            self.add_leaf(cmd=ShowSpanningTreePvsTag,
                        src= pvstag_vlans_src + '[counters][topology_changes]',
                        dest=pvstag_vlans_des + '[counters][topology_changes]',
                        pvstag_domain=pvstag_domain)

        # make to write in cache
        self.make(final_call=True)