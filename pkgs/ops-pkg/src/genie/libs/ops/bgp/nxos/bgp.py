''' 
BGP Genie Ops Object for NXOS - CLI.
'''

import re

# Genie
from genie.ops.base import Base
from genie.ops.base import Context

# nxos show_bgp
from genie.libs.parser.nxos.show_bgp import ShowBgpProcessVrfAll, ShowBgpPeerSession,\
                                 ShowBgpPeerPolicy, ShowBgpPeerTemplate,\
                                 ShowBgpVrfAllAll,\
                                 ShowBgpVrfAllNeighbors,\
                                 ShowBgpVrfAllAllNextHopDatabase,\
                                 ShowBgpVrfAllAllSummary,\
                                 ShowBgpVrfAllAllDampeningParameters,\
                                 ShowBgpVrfAllNeighborsAdvertisedRoutes,\
                                 ShowBgpVrfAllNeighborsRoutes,\
                                 ShowBgpVrfAllNeighborsReceivedRoutes

# nxos show_vrf
from genie.libs.parser.nxos.show_vrf import ShowVrf

# nxos show_routing
from genie.libs.parser.nxos.show_routing import ShowRoutingVrfAll


class Bgp(Base):
    '''BGP Genie Ops Object'''

    # Callables
    def get_af_key(self, item):
        return {key: {} for key in item.keys()}
    
    def get_af_name(self,item):
        p = re.compile(r'(?P<afname>.*) RD')
        m = p.match(item)
        if m:
            item = m.groupdict()['afname']
        return item

    def convert_to_int(self, item):
        return int(item)

    def learn(self):
        '''Learn BGP Ops'''
        
        ########################################################################
        #                               info
        ########################################################################
        
        # Global callable
        self.callables = {'get_af_name': self.get_af_name}

        # bgp_id
        self.add_leaf(cmd=ShowBgpProcessVrfAll,
                      src='[bgp_tag]',
                      dest='info[instance][default][bgp_id]',
                      action=self.convert_to_int)

        # protocol_state
        self.add_leaf(cmd=ShowBgpProcessVrfAll,
                      src='[bgp_protocol_state]',
                      dest='info[instance][default][protocol_state]')

        # ======================================================================
        #                           peer_session
        # ======================================================================
        
        # ps_name
        ps_source = '[peer_session][(?P<peer_session>.*)]'
        ps_dest = 'info[instance][default][peer_session][(?P<peer_session>.*)]'
        
        # fall_over_bfd
        self.add_leaf(cmd=ShowBgpPeerSession,
                      src=ps_source+'[bfd]',
                      dest=ps_dest+'[fall_over_bfd]')

        # suppress_four_byte_as_capability
        self.add_leaf(cmd=ShowBgpPeerSession,
                      src=ps_source+'[suppress_capabilities]',
                      dest=ps_dest+'[suppress_four_byte_as_capability]')

        # description
        self.add_leaf(cmd=ShowBgpPeerSession,
                      src=ps_source+'[description]',
                      dest=ps_dest+'[description]')

        # disable_connected_check
        self.add_leaf(cmd=ShowBgpPeerSession,
                      src=ps_source+'[disable_connectivity_check]',
                      dest=ps_dest+'[disable_connected_check]')

        # ebgp_multihop_enable
        self.add_leaf(cmd=ShowBgpPeerSession,
                      src=ps_source+'[ebgp_multihop_enable]',
                      dest=ps_dest+'[ebgp_multihop_enable]')

        # ebgp_multihop_max_hop
        self.add_leaf(cmd=ShowBgpPeerSession,
                      src=ps_source+'[ebgp_multihop_limit]',
                      dest=ps_dest+'[ebgp_multihop_max_hop]')

        # local_as_as_no
        self.add_leaf(cmd=ShowBgpPeerSession,
                      src=ps_source+'[local_as]',
                      dest=ps_dest+'[local_as_as_no]')

        # local_no_prepend - N/A
        # local_dual_as - N/A
        # local_replace_as - N/A

        # password_text
        self.add_leaf(cmd=ShowBgpPeerSession,
                      src=ps_source+'[password]',
                      dest=ps_dest+'[password_text]')

        # remote_as
        self.add_leaf(cmd=ShowBgpPeerSession,
                      src=ps_source+'[remote_as]',
                      dest=ps_dest+'[remote_as]')

        # shutdown
        self.add_leaf(cmd=ShowBgpPeerSession,
                      src=ps_source+'[shutdown]',
                      dest=ps_dest+'[shutdown]')

        # keepalive_interval
        self.add_leaf(cmd=ShowBgpPeerSession,
                      src=ps_source+'[keepalive]',
                      dest=ps_dest+'[keepalive_interval]')

        # holdtime
        self.add_leaf(cmd=ShowBgpPeerSession,
                      src=ps_source+'[holdtime]',
                      dest=ps_dest+'[holdtime]')

        # transport_connection_mode
        self.add_leaf(cmd=ShowBgpPeerSession,
                      src=ps_source+'[transport_connection_mode]',
                      dest=ps_dest+'[transport_connection_mode]')

        # update_source
        self.add_leaf(cmd=ShowBgpPeerSession,
                      src=ps_source+'[update_source]',
                      dest=ps_dest+'[update_source]')

        # ======================================================================
        #                           peer_policy
        # ======================================================================
        
        # pp_name
        pp_src = '[peer_policy][(?P<peer_policy>.*)]'
        pp_dest = 'info[instance][default][peer_policy][(?P<peer_policy>.*)]'

        # allowas_in
        self.add_leaf(cmd=ShowBgpPeerPolicy,
                      src=pp_src+'[allowas_in]',
                      dest=pp_dest+'[allowas_in]')

        # allowas_in_as_number - N/A

        # as_override
        self.add_leaf(cmd=ShowBgpPeerPolicy,
                      src=pp_src+'[as_override]',
                      dest=pp_dest+'[as_override]')

        # default_originate
        self.add_leaf(cmd=ShowBgpPeerPolicy,
                      src=pp_src+'[default_originate]',
                      dest=pp_dest+'[default_originate]')

        # default_originate_route_map
        self.add_leaf(cmd=ShowBgpPeerPolicy,
                      src=pp_src+'[default_originate_route_map]',
                      dest=pp_dest+'[default_originate_route_map]')

        # route_map_name_in
        self.add_leaf(cmd=ShowBgpPeerPolicy,
                      src=pp_src+'[route_map_name_in]',
                      dest=pp_dest+'[route_map_name_in]')

        # route_map_name_out
        self.add_leaf(cmd=ShowBgpPeerPolicy,
                      src=pp_src+'[route_map_name_out]',
                      dest=pp_dest+'[route_map_name_out]')

        # maximum_prefix_max_prefix_no
        self.add_leaf(cmd=ShowBgpPeerPolicy,
                      src=pp_src+'[maximum_prefix_max_prefix_no]',
                      dest=pp_dest+'[maximum_prefix_max_prefix_no]')

        # maximum_prefix_threshold - N/A
        # maximum_prefix_restart - N/A
        # maximum_prefix_warning_only - N/A
        
        # next_hop_self
        self.add_leaf(cmd=ShowBgpPeerPolicy,
                      src=pp_src+'[next_hop_self]',
                      dest=pp_dest+'[next_hop_self]')

        # route_reflector_client
        self.add_leaf(cmd=ShowBgpPeerPolicy,
                      src=pp_src+'[route_reflector_client]',
                      dest=pp_dest+'[route_reflector_client]')

        # send_community
        self.add_leaf(cmd=ShowBgpPeerPolicy,
                      src=pp_src+'[send_community]',
                      dest=pp_dest+'[send_community]')

        # soft_reconfiguration
        self.add_leaf(cmd=ShowBgpPeerPolicy,
                      src=pp_src+'[soft_reconfiguration]',
                      dest=pp_dest+'[soft_reconfiguration]')

        # soo
        self.add_leaf(cmd=ShowBgpPeerPolicy,
                      src=pp_src+'[site_of_origin]',
                      dest=pp_dest+'[soo]')

        # ======================================================================
        #                               vrf
        # ======================================================================
        
        #   vrf_id
        vrf_src = '[vrf][(?P<vrf>.*)]'
        vrf_dest = 'info[instance][default][vrf][(?P<vrf>.*)]'

        # always_compare_med - N/A
        # bestpath_compare_routerid - N/A
        # bestpath_cost_community_ignore - N/A
        # bestpath_med_missin_at_worst - N/A

        # cluster_id
        self.add_leaf(cmd=ShowBgpProcessVrfAll,
                      src=vrf_src+'[cluster_id]',
                      dest=vrf_dest+'[cluster_id]')

        # confederation_identifier
        self.add_leaf(cmd=ShowBgpProcessVrfAll,
                      src=vrf_src+'[confed_id]',
                      dest=vrf_dest+'[confederation_identifier]')

        # confederation_peer_as - N/A

        # graceful_restart
        self.add_leaf(cmd=ShowBgpProcessVrfAll,
                      src=vrf_src+'[graceful_restart]',
                      dest=vrf_dest+'[graceful_restart]')

        # graceful_restart_restart_time
        self.add_leaf(cmd=ShowBgpProcessVrfAll,
                      src=vrf_src+'[graceful_restart_restart_time]',
                      dest=vrf_dest+'[graceful_restart_restart_time]')

        # graceful_restart_stalepath_time
        self.add_leaf(cmd=ShowBgpProcessVrfAll,
                      src=vrf_src+'[graceful_restart_stalepath_time]',
                      dest=vrf_dest+'[graceful_restart_stalepath_time]')

        # log_neighbor_changes - N/A

        # router_id
        self.add_leaf(cmd=ShowBgpProcessVrfAll,
                      src=vrf_src+'[router_id]',
                      dest=vrf_dest+'[router_id]')

        # keepalive_interval - N/A
        # holdtime - N/A
        # enforce_first_as - N/A
        # fast_external_fallover - N/A
        # default_choice_ipv4_unicast - N/A

        # ======================================================================
        #                           vrf: address_family
        # ======================================================================

        # address_family
        #   addr_family
        af_src = '[address_family][(?P<afname>{get_af_name})]'
        af_dest = '[address_family][(?P<afname>{get_af_name})]'

        # Add empty address family
        self.add_leaf(cmd=ShowBgpProcessVrfAll,
                      src=vrf_src+'[address_family]',
                      dest=vrf_dest+'[address_family]',
                      action=self.get_af_key)

        # dampening
        self.add_leaf(cmd=ShowBgpVrfAllAllDampeningParameters,
                      src=vrf_src+af_src+'[dampening]',
                      dest=vrf_dest+af_dest+'[dampening]')

        # dampening_route_map
        self.add_leaf(cmd=ShowBgpVrfAllAllDampeningParameters,
                      src=vrf_src+af_src+'[dampening_route_map]',
                      dest=vrf_dest+af_dest+'[dampening_route_map]')

        # dampening_half_life_time
        self.add_leaf(cmd=ShowBgpVrfAllAllDampeningParameters,
                      src=vrf_src+af_src+'[dampening_half_life_time]',
                      dest=vrf_dest+af_dest+'[dampening_half_life_time]')

        # dampening_reuse_time
        self.add_leaf(cmd=ShowBgpVrfAllAllDampeningParameters,
                      src=vrf_src+af_src+'[dampening_reuse_time]',
                      dest=vrf_dest+af_dest+'[dampening_reuse_time]')

        # dampening_suppress_time
        self.add_leaf(cmd=ShowBgpVrfAllAllDampeningParameters,
                      src=vrf_src+af_src+'[dampening_suppress_time]',
                      dest=vrf_dest+af_dest+'[dampening_suppress_time]')

        # dampening_max_suppress_time
        self.add_leaf(cmd=ShowBgpVrfAllAllDampeningParameters,
                      src=vrf_src+af_src+'[dampening_max_suppress_time]',
                      dest=vrf_dest+af_dest+'[dampening_max_suppress_time]')

        # nexthop_route_map - N/A

        # nexthop_trigger_enable
        self.add_leaf(cmd=ShowBgpVrfAllAllNextHopDatabase,
                      src=vrf_src+af_src+'[af_nexthop_trigger_enable]',
                      dest=vrf_dest+af_dest+'[nexthop_trigger_enable]')

        # nexthop_trigger_delay_critical
        self.add_leaf(cmd=ShowBgpVrfAllAllNextHopDatabase,
                      src=vrf_src+af_src+'[nexthop_trigger_delay_critical]',
                      dest=vrf_dest+af_dest+'[nexthop_trigger_delay_critical]')

        # nexthop_trigger_delay_non_critical
        self.add_leaf(cmd=ShowBgpVrfAllAllNextHopDatabase,
                      src=vrf_src+af_src+'[nexthop_trigger_delay_non_critical]',
                      dest=vrf_dest+af_dest+'[nexthop_trigger_delay_non_critical]')

        # client_to_client_reflection - N/A

        # distance_extern_as
        self.add_leaf(cmd=ShowRoutingVrfAll,
                      src=vrf_src+af_src+'[bgp_distance_extern_as]',
                      dest=vrf_dest+af_dest+'[distance_extern_as]')

        # distance_internal_as
        self.add_leaf(cmd=ShowRoutingVrfAll,
                      src=vrf_src+af_src+'[bgp_distance_internal_as]',
                      dest=vrf_dest+af_dest+'[distance_internal_as]')

        # distance_local
        self.add_leaf(cmd=ShowRoutingVrfAll,
                      src=vrf_src+af_src+'[bgp_distance_local]',
                      dest=vrf_dest+af_dest+'[distance_local]')

        # maximum_paths_ebgp
        self.add_leaf(cmd=ShowBgpProcessVrfAll,
                      src=vrf_src+af_src+'[ebgp_max_paths]',
                      dest=vrf_dest+af_dest+'[maximum_paths_ebgp]')

        # maximum_paths_ibgp
        self.add_leaf(cmd=ShowBgpProcessVrfAll,
                      src=vrf_src+af_src+'[ibgp_max_paths]',
                      dest=vrf_dest+af_dest+'[maximum_paths_ibgp]')

        # maximum_paths_eibgp - N/A

        # aggregate_address_ipv4_address
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=vrf_src+af_src+'[aggregate_address_ipv4_address]',
                      dest=vrf_dest+af_dest+'[aggregate_address_ipv4_address]')

        # aggregate_address_ipv4_mask
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=vrf_src+af_src+'[aggregate_address_ipv4_mask]',
                      dest=vrf_dest+af_dest+'[aggregate_address_ipv4_mask]')

        # aggregate_address_as_set
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=vrf_src+af_src+'[aggregate_address_as_set]',
                      dest=vrf_dest+af_dest+'[aggregate_address_as_set]')

        # aggregate_address_summary_only
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=vrf_src+af_src+'[aggregate_address_summary_only]',
                      dest=vrf_dest+af_dest+'[aggregate_address_summary_only]')

        # network_number - N/A
        # network_mask - N/A
        # network_route_map - N/A
        # redist_isis - N/A
        # redist_isis_metric - N/A
        # redist_isis_route_policy - N/A
        # redist_ospf - N/A
        # redist_ospf_metric - N/A
        # redist_ospf_route_policy - N/A
        # redist_rip - N/A
        # redist_rip_metric - N/A
        # redist_rip_route_policy - N/A
        # redist_static - N/A
        # redist_static_metric - N/A
        # redist_static_route_policy - N/A
        # redist_connected - N/A
        # redist_connected_metric - N/A
        # redist_connected_route_policy - N/A

        # v6_aggregate_address_ipv6_address
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=vrf_src+af_src+'[v6_aggregate_address_ipv6_address]',
                      dest=vrf_dest+af_dest+'[v6_aggregate_address_ipv6_address]')

        # v6_aggregate_address_as_set
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=vrf_src+af_src+'[v6_aggregate_address_as_set]',
                      dest=vrf_dest+af_dest+'[v6_aggregate_address_as_set]')

        # v6_aggregate_address_summary_only
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=vrf_src+af_src+'[v6_aggregate_address_summary_only]',
                      dest=vrf_dest+af_dest+'[v6_aggregate_address_summary_only]')

        # v6_network_number - N/A
        # v6_network_route_map - N/A
        # v6_allocate_label_all - N/A
        # retain_rt_all - N/A
        
        # label_allocation_mode
        self.add_leaf(cmd=ShowBgpProcessVrfAll,
                      src=vrf_src+af_src+'[label_mode]',
                      dest=vrf_dest+af_dest+'[label_allocation_mode]')

        # ======================================================================
        #                             vrf: neighbor
        # ======================================================================

        # Get vrfs for input to 'show bgp vrf <vrf_name> all neighbors'
        self.add_leaf(cmd=ShowVrf,
                      src='[vrfs]',
                      dest='info[list_of_vrfs]')
        self.make()

        # Creating a list of all vrfs configured on the device. Looping through
        # each vrf to execute "show bgp vrf <vrf_name> all neighbors"
        if hasattr(self, 'info') and 'list_of_vrfs' in self.info:

            for vrf_name in sorted(self.info['list_of_vrfs']):

                # neighbor_id
                nbr_src = '[neighbor][(?P<neighbor_id>.*)]'
                nbr_dest = 'info[instance][default][vrf][{vrf_name}][neighbor][(?P<neighbor_id>.*)]'.format(vrf_name=vrf_name)

                # fall_over_bfd
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bfd_live_detection]',
                              dest=nbr_dest+'[fall_over_bfd]',
                              vrf=vrf_name)

                # suppress_four_byte_as_capability
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[suppress_four_byte_as_capability]',
                              dest=nbr_dest+'[suppress_four_byte_as_capability]',
                              vrf=vrf_name)

                # description
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[description]',
                              dest=nbr_dest+'[description]',
                              vrf=vrf_name)

                # disable_connected_check
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[disable_connected_check]',
                              dest=nbr_dest+'[disable_connected_check]',
                              vrf=vrf_name)

                # ebgp_multihop
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[ebgp_multihop]',
                              dest=nbr_dest+'[ebgp_multihop]',
                              vrf=vrf_name)

                # ebgp_multihop_max_hop
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[ebgp_multihop_max_hop]',
                              dest=nbr_dest+'[ebgp_multihop_max_hop]',
                              vrf=vrf_name)

                # inherit_peer_session
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[inherit_peer_session]',
                              dest=nbr_dest+'[inherit_peer_session]',
                              vrf=vrf_name)

                # local_as_as_no
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[local_as]',
                              dest=nbr_dest+'[local_as_as_no]',
                              vrf=vrf_name)

                # local_as_no_prepend - N/A
                # local_as_replace_as - N/A
                # local_as_dual_as - N/A
                
                # remote_as
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[remote_as]',
                              dest=nbr_dest+'[remote_as]',
                              vrf=vrf_name)

                # remove_private_as
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[remove_private_as]',
                              dest=nbr_dest+'[remove_private_as]',
                              vrf=vrf_name)

                # shutdown
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[shutdown]',
                              dest=nbr_dest+'[shutdown]',
                              vrf=vrf_name)

                # keepalive_interval
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bgp_negotiated_keepalive_timers][keepalive_interval]',
                              dest=nbr_dest+'[keepalive_interval]',
                              vrf=vrf_name)

                # holdtime
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bgp_negotiated_keepalive_timers][hold_time]',
                              dest=nbr_dest+'[holdtime]',
                              vrf=vrf_name)

                # bgp_version
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bgp_version]',
                              dest=nbr_dest+'[bgp_version]',
                              vrf=vrf_name)
                
                # installed_prefixes - N/A

                # session_state
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[session_state]',
                              dest=nbr_dest+'[session_state]',
                              vrf=vrf_name)
                
                # bgp_negotiated_keepalive_timers
                #   keepalive_interval
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bgp_negotiated_keepalive_timers][keepalive_interval]',
                              dest=nbr_dest+'[bgp_negotiated_keepalive_timers][keepalive_interval]',
                              vrf=vrf_name)
                
                # bgp_negotiated_keepalive_timers
                #   hold_time
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bgp_negotiated_keepalive_timers][hold_time]',
                              dest=nbr_dest+'[bgp_negotiated_keepalive_timers][hold_time]',
                              vrf=vrf_name)

                # bgp_session_transport
                #   connection
                #     state
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[session_state]',
                              dest=nbr_dest+'[bgp_session_transport][connection][state]',
                              vrf=vrf_name)

                # bgp_session_transport
                #   connection
                #     mode
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bgp_session_transport][connection][mode]',
                              dest=nbr_dest+'[bgp_session_transport][connection][mode]',
                              vrf=vrf_name)

                # bgp_session_transport
                #   connection
                #     last_reset
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bgp_session_transport][connection][last_reset]',
                              dest=nbr_dest+'[bgp_session_transport][connection][last_reset]',
                              vrf=vrf_name)

                # bgp_session_transport
                #   connection
                #     reset_reason
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bgp_session_transport][connection][reset_reason]',
                              dest=nbr_dest+'[bgp_session_transport][connection][reset_reason]',
                              vrf=vrf_name)
                
                # bgp_session_transport
                #   transport
                #     local_port
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bgp_session_transport][transport][local_port]',
                              dest=nbr_dest+'[bgp_session_transport][transport][local_port]',
                              vrf=vrf_name)

                # bgp_session_transport
                #   transport
                #     local_host
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bgp_session_transport][transport][local_host]',
                              dest=nbr_dest+'[bgp_session_transport][transport][local_host]',
                              vrf=vrf_name)

                # bgp_session_transport
                #   transport
                #     foreign_port
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bgp_session_transport][transport][foreign_port]',
                              dest=nbr_dest+'[bgp_session_transport][transport][foreign_port]',
                              vrf=vrf_name)

                # bgp_session_transport
                #   transport
                #     foreign_host
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bgp_session_transport][transport][foreign_host]',
                              dest=nbr_dest+'[bgp_session_transport][transport][foreign_host]',
                              vrf=vrf_name)
                
                # bgp_session_transport
                #   transport
                #     mss - N/A

                # minimum_neighbor_hold - N/A
                
                # up_time
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[up_time]',
                              dest=nbr_dest+'[up_time]',
                              vrf=vrf_name)

                # update_source
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[update_source]',
                              dest=nbr_dest+'[update_source]',
                              vrf=vrf_name)

                # password_text
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[tcp_md5_auth]',
                              dest=nbr_dest+'[password_text]',
                              vrf=vrf_name)

                # bgp_negotiated_capabilities
                #   route_refresh
                #   four_octets_asn
                #   vpnv4_unicast
                #   vpnv6_unicast
                #   graceful_restart
                #   enhanced_refresh
                #   multisession
                #   stateful_switchover
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bgp_negotiated_capabilities]',
                              dest=nbr_dest+'[bgp_negotiated_capabilities]',
                              vrf=vrf_name)

                # bgp_neighbor_counters
                #   messages
                #     sent/received
                #       opens
                #       updates
                #       notifications
                #       keepalives
                #       route_refreshes
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[bgp_neighbor_counters]',
                              dest=nbr_dest+'[bgp_neighbor_counters]',
                              vrf=vrf_name)

                # ==============================================================
                #                  vrf: neighbor - address_family
                # ==============================================================

                # address_family
                #   nbr_af_name
                #     bgp_table_version
                #     session_state
                req_keys = ['bgp_table_version','session_state']
                for key in req_keys:
                    self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                                  src=nbr_src+'[address_family][(?P<address_family>.*)][{}]'.format(key),
                                  dest=nbr_dest+'[address_family][(?P<address_family>.*)][{}]'.format(key),
                                  vrf=vrf_name)
                # address_family
                #   nbr_af_name
                #     routing_table_version - N/A

                # address_family
                #   nbr_af_name
                #     prefixes
                #       total_entries
                #       memory_usage
                self.add_leaf(cmd=ShowBgpVrfAllAllSummary,
                              src='[vrf][?P<vrf>.*)][neighbor][(?P<neighbor>.*)][address_family][(?P<address_family>.*)][prefixes]',
                              dest='info[instance][default][vrf][(?P<vrf>.*)][neighbor][(?P<neighbor>.*)][address_family][(?P<address_family>.*)][prefixes]')

                # address_family
                #   nbr_af_name
                #     path
                #       total_entries
                #       memory_usage
                self.add_leaf(cmd=ShowBgpVrfAllAllSummary,
                              src='[vrf][?P<vrf>.*)][neighbor][(?P<neighbor>.*)][address_family][(?P<address_family>.*)][path]',
                              dest='info[instance][default][vrf][(?P<vrf>.*)][neighbor][(?P<neighbor>.*)][address_family][(?P<address_family>.*)][path]')

                # total_memory - N/A
                # allowas_in - N/A
                # allowas_in_as_number - N/A

                # inherit_peer_policy
                #   inherit_peer_seq
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[address_family][(?P<address_family>.*)][inherit_peer_policy]',
                              dest=nbr_dest+'[address_family][(?P<address_family>.*)][inherit_peer_policy]',
                              vrf=vrf_name)

                # maximum_prefix_max_prefix_no
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[address_family][(?P<address_family>.*)][maximum_prefix_max_prefix_no]',
                              dest=nbr_dest+'[address_family][(?P<address_family>.*)][maximum_prefix_max_prefix_no]',
                              vrf=vrf_name)

                # maximum_prefix_threshold - N/A
                # maximum_prefix_restart - N/A
                # maximum_prefix_warning_only - N/A

                # address_family
                #   nbr_af_name
                #     route_map_name_in
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[address_family][(?P<address_family>.*)][route_map_name_in]',
                              dest=nbr_dest+'[address_family][(?P<address_family>.*)][route_map_name_in]',
                              vrf=vrf_name)

                # address_family
                #   nbr_af_name
                #     route_map_name_out
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[address_family][(?P<address_family>.*)][route_map_name_out]',
                              dest=nbr_dest+'[address_family][(?P<address_family>.*)][route_map_name_out]',
                              vrf=vrf_name)

                # route_reflector_client
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[address_family][(?P<address_family>.*)][route_reflector_client]',
                              dest=nbr_dest+'[address_family][(?P<address_family>.*)][route_reflector_client]',
                              vrf=vrf_name)
                
                # address_family
                #   nbr_af_name
                #     send_community
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[address_family][(?P<address_family>.*)][send_community]',
                              dest=nbr_dest+'[address_family][(?P<address_family>.*)][send_community]',
                              vrf=vrf_name)
                
                # address_family
                #   nbr_af_name
                #     soft_configuration
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[address_family][(?P<address_family>.*)][soft_configuration]',
                              dest=nbr_dest+'[address_family][(?P<address_family>.*)][soft_configuration]',
                              vrf=vrf_name)
                
                # next_hop_self
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[address_family][(?P<address_family>.*)][next_hop_self]',
                              dest=nbr_dest+'[address_family][(?P<address_family>.*)][next_hop_self]',
                              vrf=vrf_name)

                # as_override
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[address_family][(?P<address_family>.*)][as_override]',
                              dest=nbr_dest+'[address_family][(?P<address_family>.*)][as_override]',
                              vrf=vrf_name)

                # default_originate
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[address_family][(?P<address_family>.*)][default_originate]',
                              dest=nbr_dest+'[address_family][(?P<address_family>.*)][default_originate]',
                              vrf=vrf_name)

                # default_originate_route_map
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[address_family][(?P<address_family>.*)][default_originate_route_map]',
                              dest=nbr_dest+'[address_family][(?P<address_family>.*)][default_originate_route_map]',
                              vrf=vrf_name)

                # soo
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src=nbr_src+'[address_family][(?P<address_family>.*)][soo]',
                              dest=nbr_dest+'[address_family][(?P<address_family>.*)][soo]',
                              vrf=vrf_name)

        ########################################################################
        #                               table
        ########################################################################

        # vrf
        #   vrf_id
        #     address_family
        #       af_name
        table_src = '[vrf][(?P<vrf_name>.*)][address_family][(?P<address_family>.*)]'
        table_dest = 'table[instance][default]'+ table_src

        # route_identifier
        self.add_leaf(cmd=ShowBgpVrfAllAllSummary,
                      src='[vrf][(?P<vrf_name>.*)][neighbor][?P<neighbor>.*][address_family][(?P<address_family>.*)][route_identifier]',
                      dest=table_dest+'[route_identifier]')

        # local_as
        self.add_leaf(cmd=ShowBgpVrfAllAllSummary,
                      src='[vrf][(?P<vrf_name>.*)][neighbor][?P<neighbor>.*][address_family][(?P<address_family>.*)][local_as][(?P<local_as>.*)]',
                      dest=table_dest+'[local_as][(?P<local_as>.*)]')
        
        # bgp_table_version
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=table_src+'[bgp_table_version]',
                      dest=table_dest+'[bgp_table_version]')

        # routing_table_version - N/A

        # route_distinguisher
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=table_src+'[route_distinguisher]',
                      dest=table_dest+'[route_distinguisher]')

        # default_vrf
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=table_src+'[default_vrf]',
                      dest=table_dest+'[default_vrf]')

        # paths - N/A

        # prefixes
        #   prefix
        prefix_src = '[prefixes][(?P<prefix>.*)]'
        prefix_dest = '[prefixes][(?P<prefix>.*)]'

        # table_version - N/A

        # index
        #   index
        idx_src = prefix_src+'[index][(?P<index>.*)]'
        idx_dest = prefix_dest+'[index][(?P<index>.*)]'

        # next_hop_igp_metric - N/A
        # gateway - N/A
        # cluster_id - N/A
        # update_group - N/A

        # next_hop
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=table_src+idx_src+'[next_hop]',
                      dest=table_dest+idx_dest+'[next_hop]')

        # status_codes
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=table_src+idx_src+'[status_codes]',
                      dest=table_dest+idx_dest+'[status_codes]')

        # origin_codes
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=table_src+idx_src+'[origin_codes]',
                      dest=table_dest+idx_dest+'[origin_codes]')

        # metric
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=table_src+idx_src+'[metric]',
                      dest=table_dest+idx_dest+'[metric]')

        # localpref
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=table_src+idx_src+'[localprf]',
                      dest=table_dest+idx_dest+'[localpref]')

        # weight
        self.add_leaf(cmd=ShowBgpVrfAllAll,
                      src=table_src+idx_src+'[weight]',
                      dest=table_dest+idx_dest+'[weight]')

        # ext_community - N/A
        # mpls_labels_inout - N/A
        # originator - N/A
        # cluster_list - N/A

        ########################################################################
        #                           routes_per_peer
        ########################################################################

        # Routes per peer top level key
        rpp_src = '[vrf][(?P<vrf>.*)][neighbor][(?P<neighbor>.*)][address_family][(?P<address_family>.*)]'
        rpp_dest = 'routes_per_peer[instance][default][vrf][(?P<vrf>.*)][neighbor][(?P<neighbor>.*)][address_family][(?P<address_family>.*)]'

        # msg_rcvd
        self.add_leaf(cmd=ShowBgpVrfAllAllSummary,
                      src=rpp_src+'[msg_rcvd]',
                      dest=rpp_dest+'[msg_rcvd]')

        # msg_sent
        self.add_leaf(cmd=ShowBgpVrfAllAllSummary,
                      src=rpp_src+'[msg_sent]',
                      dest=rpp_dest+'[msg_sent]')

        # tbl_ver
        self.add_leaf(cmd=ShowBgpVrfAllAllSummary,
                      src=rpp_src+'[tbl_ver]',
                      dest=rpp_dest+'[tbl_ver]')

        # input_queue
        self.add_leaf(cmd=ShowBgpVrfAllAllSummary,
                      src=rpp_src+'[inq]',
                      dest=rpp_dest+'[input_queue]')

        # output_queue
        self.add_leaf(cmd=ShowBgpVrfAllAllSummary,
                      src=rpp_src+'[outq]',
                      dest=rpp_dest+'[output_queue]')

        # up_down
        self.add_leaf(cmd=ShowBgpVrfAllAllSummary,
                      src=rpp_src+'[up_down]',
                      dest=rpp_dest+'[up_down]')

        # state_pfxrcd
        self.add_leaf(cmd=ShowBgpVrfAllAllSummary,
                      src=rpp_src+'[state_pfxrcd]',
                      dest=rpp_dest+'[state_pfxrcd]')

        if hasattr(self, 'info') and 'list_of_vrfs' in self.info:
            
            # Got vrfs from "vrf: neighbor" section for below commands
            for vrf_name in sorted(self.info['list_of_vrfs']):

                # remote_as
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src='[neighbor][(?P<neighbor_id>.*)][remote_as][(?P<remote_as>.*)]',
                              dest='routes_per_peer[instance][default][vrf][{vrf_name}][neighbor][(?P<neighbor_id>.*)][remote_as][(?P<remote_as>.*)]'.format(vrf_name=vrf_name),
                              vrf=vrf_name)
                
                # Get neighbors for input to:
                #  * 'show bgp vrf <vrf_name> all neighbors <neighbor> advertised-routes'
                #  * 'show bgp vrf <vrf_name> all neighbors <neighbor> routes'
                #  * 'show bgp vrf <vrf_name> all neighbors <neighbor> receieved-routes'
                self.add_leaf(cmd=ShowBgpVrfAllNeighbors,
                              src='[neighbor]',
                              dest='routes_per_peer[list_of_neighbors]',
                              vrf=vrf_name)
                self.make()

                if hasattr (self, 'routes_per_peer') and\
                   'list_of_neighbors' in self.routes_per_peer:

                    for neighbor in sorted(self.routes_per_peer['list_of_neighbors']):

                        # advertised
                        self.add_leaf(cmd=ShowBgpVrfAllNeighborsAdvertisedRoutes,
                                      src='[vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][advertised]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      dest='routes_per_peer[instance][default][vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][advertised]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      vrf=vrf_name, neighbor=neighbor)

                        # advertised - route_distinguisher
                        self.add_leaf(cmd=ShowBgpVrfAllNeighborsAdvertisedRoutes,
                                      src='[vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][route_distinguisher]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      dest='routes_per_peer[instance][default][vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][route_distinguisher]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      vrf=vrf_name, neighbor=neighbor)

                        # advertised - default_vrf
                        self.add_leaf(cmd=ShowBgpVrfAllNeighborsAdvertisedRoutes,
                                      src='[vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][default_vrf]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      dest='routes_per_peer[instance][default][vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][default_vrf]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      vrf=vrf_name, neighbor=neighbor)

                        # routes
                        self.add_leaf(cmd=ShowBgpVrfAllNeighborsRoutes,
                                      src='[vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][routes]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      dest='routes_per_peer[instance][default][vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][routes]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      vrf=vrf_name, neighbor=neighbor)

                        # routes - route_distinguisher
                        self.add_leaf(cmd=ShowBgpVrfAllNeighborsRoutes,
                                      src='[vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][route_distinguisher]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      dest='routes_per_peer[instance][default][vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][route_distinguisher]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      vrf=vrf_name, neighbor=neighbor)

                        # routes - default_vrf
                        self.add_leaf(cmd=ShowBgpVrfAllNeighborsRoutes,
                                      src='[vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][default_vrf]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      dest='routes_per_peer[instance][default][vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][default_vrf]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      vrf=vrf_name, neighbor=neighbor)

                        # received_routes
                        self.add_leaf(cmd=ShowBgpVrfAllNeighborsReceivedRoutes,
                                      src='[vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][received_routes]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      dest='routes_per_peer[instance][default][vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][received_routes]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      vrf=vrf_name, neighbor=neighbor)

                        # received_routes - route_distinguisher
                        self.add_leaf(cmd=ShowBgpVrfAllNeighborsReceivedRoutes,
                                      src='[vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][route_distinguisher]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      dest='routes_per_peer[instance][default][vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][route_distinguisher]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      vrf=vrf_name, neighbor=neighbor)

                        # received_routes - default_vrf
                        self.add_leaf(cmd=ShowBgpVrfAllNeighborsReceivedRoutes,
                                      src='[vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][default_vrf]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      dest='routes_per_peer[instance][default][vrf][{vrf_name}][neighbor][{neighbor}][address_family][(?P<address_family>.*)][default_vrf]'.format(vrf_name=vrf_name, neighbor=neighbor),
                                      vrf=vrf_name, neighbor=neighbor)

                    # clear list of neighbors for next vrf
                    del self.routes_per_peer['list_of_neighbors']

        ########################################################################
        #                           Final Structure
        ########################################################################

        # Make final Ops structure
        self.make()

        # Delete unnecessary keys
        try:
            del self.info['list_of_vrfs']
        except:
            pass

