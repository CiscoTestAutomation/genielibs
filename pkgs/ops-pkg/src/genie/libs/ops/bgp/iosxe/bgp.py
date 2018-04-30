''' 
BGP Genie Ops Object for IOSXE - CLI.
'''

import re

# Genie
from genie.ops.base import Base
from genie.ops.base import Context

# iosxe show_bgp
from genie.libs.parser.iosxe.show_bgp import ShowBgpAllSummary, ShowBgpAllClusterIds, \
                                  ShowBgpAllNeighborsAdvertisedRoutes, \
                                  ShowBgpAllNeighborsReceivedRoutes, \
                                  ShowBgpAllNeighborsRoutes, \
                                  ShowIpBgpTemplatePeerPolicy, \
                                  ShowBgpAllNeighbors, \
                                  ShowIpBgpAllDampeningParameters, \
                                  ShowIpBgpTemplatePeerSession, \
                                  ShowBgpAllNeighborsPolicy, \
                                  ShowBgpAllDetail, \
                                  ShowBgpAll


class Bgp(Base):
    '''BGP Genie Ops Object'''

    # Callables
    def get_af_key(self, item):
        return {key: {} for key in item.keys()}

    def get_af_name(self, item):
        p = re.compile(r'(?P<afname>.*) RD')
        m = p.match(item)
        if m:
            item = m.groupdict()['afname']
        return item

    def learn(self):
        '''Learn BGP Ops'''
        
        ########################################################################
        #                               info
        ########################################################################
        
        # Global callable
        self.callables = {'get_af_name': self.get_af_name}

        # bgp_id
        self.add_leaf(cmd=ShowBgpAllSummary,
                      src='[bgp_id]',
                      dest='info[instance][default][bgp_id]')

        # protocol_state - N/A

        # ======================================================================
        #                           peer_session
        # ======================================================================

        # peer_session
        #   ps_name
        ps_source = '[peer_session][(?P<peer_session>.*)]'
        ps_dest = 'info[instance][default][peer_session][(?P<peer_session>.*)]'

        peer_session_keys = ['fall_over_bfd',\
            'suppress_four_byte_as_capability', 'description',\
            'disable_connected_check', 'ebgp_multihop_enable',\
            'ebgp_multihop_max_hop', 'local_as_as_no', 'password_text',\
            'remote_as', 'shutdown', 'keepalive_interval',\
            'holdtime', 'transport_connection_mode', 'update_source']

        for key in peer_session_keys:

            self.add_leaf(cmd=ShowIpBgpTemplatePeerSession,
                          src='{ps_source}[{key}]'.format(ps_source=ps_source,
                                                          key=key),
                          dest='{ps_dest}[{key}]'.format(ps_dest=ps_dest,
                                                         key=key))

        # local_no_prepend - N/A
        # local_dual_as - N/A
        # local_replace_as - N/A

        # ======================================================================
        #                           peer_policy
        # ======================================================================

        # peer_policy
        #   pp_name
        pp_src = '[peer_policy][(?P<peer_policy>.*)]'
        pp_dest = 'info[instance][default][peer_policy][(?P<peer_policy>.*)]'

        peer_policy_keys = ['allowas_in', 'as_override', 'default_originate',\
            'default_originate_route_map', 'route_map_name_in',\
            'route_map_name_out', 'maximum_prefix_max_prefix_no',\
            'next_hop_self', 'route_reflector_client', 'send_community',\
            'soft_reconfiguration', 'soo']

        for key in peer_policy_keys:

            self.add_leaf(cmd=ShowIpBgpTemplatePeerPolicy,
                      src='{pp_src}[{key}]'.format(pp_src=pp_src,key=key),
                      dest='{pp_dest}[{key}]'.format(pp_dest=pp_dest,key=key))

        # allowas_in_as_number - N/A
        # maximum_prefix_threshold - N/A
        # maximum_prefix_restart - N/A
        # maximum_prefix_warning_only - N/A

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
        self.add_leaf(cmd=ShowBgpAllClusterIds,
                      src=vrf_src+'[cluster_id]',
                      dest=vrf_dest+'[cluster_id]')

        # confederation_identifier- N/A
        # confederation_peer_as - N/A
        # graceful_restart - N/A
        # graceful_restart_restart_time - N/A
        # graceful_restart_stalepath_time - N/A
        # log_neighbor_changes - N/A
        # router_id - N/A
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
        self.add_leaf(cmd=ShowIpBgpAllDampeningParameters,
                      src=vrf_src+'[address_family]',
                      dest=vrf_dest+'[address_family]',
                      action=self.get_af_key)

        # vrf: address_family
        vrf_add_src = vrf_src+af_src
        vrf_add_dest = vrf_dest+af_dest

        vrf_add_keys = ['dampening', 'dampening_half_life_time',\
            'dampening_reuse_time', 'dampening_suppress_time',\
            'dampening_max_suppress_time']

        for key in vrf_add_keys:

            self.add_leaf(cmd=ShowIpBgpAllDampeningParameters,
                      src='{vrf_add_src}[{key}]'.format(
                        vrf_add_src=vrf_add_src, key=key),
                      dest='{vrf_add_dest}[{key}]'.format(
                        vrf_add_dest=vrf_add_dest, key=key))

        # nexthop_route_map - N/A
        # nexthop_trigger_enable - N/A
        # nexthop_trigger_delay_critical - N/A
        # nexthop_trigger_delay_non_critical - N/A
        # client_to_client_reflection - N/A
        # distance_extern_as - N/A
        # distance_internal_as - N/A
        # distance_local - N/A
        # maximum_paths_ebgp - N/A
        # maximum_paths_ibgp - N/A
        # maximum_paths_eibgp - N/A
        # aggregate_address_ipv4_address - N/A
        # aggregate_address_ipv4_mask - N/A
        # aggregate_address_as_set - N/A
        # aggregate_address_summary_only - N/A
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
        # v6_aggregate_address_ipv6_address - N/A
        # v6_aggregate_address_as_set - N/A
        # v6_aggregate_address_summary_only - N/A
        # v6_network_number - N/A
        # v6_network_route_map - N/A
        # v6_allocate_label_all - N/A
        # retain_rt_all - N/A
        # label_allocation_mode - N/A

        # ======================================================================
        #                             vrf: neighbor
        # ======================================================================

        # neighbor_id
        nbr_src = '[vrf][(?P<vrf>.*)][neighbor][(?P<neighbor_id>.*)]'
        nbr_dest = 'info[instance][default][vrf][(?P<vrf>.*)][neighbor]'\
                   '[(?P<neighbor_id>.*)]'

        neighbor_keys = ['description', 'remote_as',\
            'shutdown', 'bgp_version',\
            'session_state']

        for key in neighbor_keys:

            self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src='{nbr_src}[{key}]'.format(nbr_src=nbr_src,
                                                   key=key),
                      dest='{nbr_dest}[{key}]'.format(nbr_dest=nbr_dest,
                                                     key=key))
        # fall_over_bfd - N/A
        # suppress_four_byte_as_capability - N/A
        # disable_connected_check - N/A
        # ebgp_multihop - N/A
        # ebgp_multihop_max_hop - N/A
        # inherit_peer_session - N/A
        # local_as_as_no - N/A
        # local_as_no_prepend - N/A
        # local_as_replace_as - N/A
        # local_as_dual_as - N/A
        # remove_private_as - N/A
        # installed_prefixes - N/A

        # bgp_negotiated_keepalive_timers
        #   keepalive_interval
        self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src=nbr_src+'[bgp_negotiated_keepalive_timers]'
                                  '[keepalive_interval]',
                      dest=nbr_dest+'[bgp_negotiated_keepalive_timers]'
                                    '[keepalive_interval]')

        # bgp_negotiated_keepalive_timers
        #   hold_time
        self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src=nbr_src+'[bgp_negotiated_keepalive_timers]'
                                  '[hold_time]',
                      dest=nbr_dest+'[bgp_negotiated_keepalive_timers]'
                                    '[hold_time]')

        # bgp_session_transport
        #   connection
        #     state
        self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src=nbr_src+'[session_state]',
                      dest=nbr_dest+'[bgp_session_transport][connection]'
                                    '[state]')

        # bgp_session_transport
        #   connection
        #     mode - N/A

        # bgp_session_transport
        #   connection
        #     last_reset
        self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src=nbr_src+'[bgp_session_transport][connection]'
                                  '[last_reset]',
                      dest=nbr_dest+'[bgp_session_transport][connection]'
                                    '[last_reset]')

        # bgp_session_transport
        #   connection
        #     reset_reason
        self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src=nbr_src+'[bgp_session_transport][connection]'
                                  '[reset_reason]',
                      dest=nbr_dest+'[bgp_session_transport][connection]'
                                    '[reset_reason]')
        
        # bgp_session_transport
        #   transport
        #     local_port
        self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src=nbr_src+'[bgp_session_transport][transport]'
                                  '[local_port]',
                      dest=nbr_dest+'[bgp_session_transport][transport]'
                                    '[local_port]')

        # bgp_session_transport
        #   transport
        #     local_host
        self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src=nbr_src+'[bgp_session_transport][transport]'
                                  '[local_host]',
                      dest=nbr_dest+'[bgp_session_transport][transport]'
                                    '[local_host]')

        # bgp_session_transport
        #   transport
        #     foreign_port
        self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src=nbr_src+'[bgp_session_transport][transport]'
                                  '[foreign_port]',
                      dest=nbr_dest+'[bgp_session_transport][transport]'
                                    '[foreign_port]')

        # bgp_session_transport
        #   transport
        #     foreign_host
        self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src=nbr_src+'[bgp_session_transport][transport]'
                                  '[foreign_host]',
                      dest=nbr_dest+'[bgp_session_transport][transport]'
                                    '[foreign_host]')
        
        # bgp_session_transport
        #   transport
        #     mss
        self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src=nbr_src+'[bgp_session_transport][transport]'
                                  '[mss]',
                      dest=nbr_dest+'[bgp_session_transport][transport]'
                                    '[mss]')

        # minimum_neighbor_hold - N/A
        # up_time - N/A
        # update_source - N/A
        # password_text - N/A

        # bgp_negotiated_capabilities
        capabilities_src = nbr_src+'[bgp_negotiated_capabilities]'
        capabilities_dest = nbr_dest+'[bgp_negotiated_capabilities]'

        capabilities_keys = ['route_refresh', 'four_octets_asn',\
            'vpnv4_unicast', 'vpnv6_unicast',\
            'graceful_restart', 'enhanced_refresh', 'multisession',\
            'stateful_switchover']

        for key in capabilities_keys:

            self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src='{capabilities_src}[{key}]'.format(
                        capabilities_src=capabilities_src, key=key),
                      dest='{capabilities_dest}[{key}]'.format(
                        capabilities_dest=capabilities_dest, key=key))

        # bgp_neighbor_counters_messages
        counters_src = nbr_src+'[bgp_neighbor_counters][messages]'
        counters_dest = nbr_dest+'[bgp_neighbor_counters][messages]'

        counters_keys = ['opens', 'updates', 'notifications', 'keepalives',\
            'route_refreshes']

        for key in counters_keys:

            self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src='{counters_src}[sent][{key}]'.format(
                        counters_src=counters_src, key=key),
                      dest='{counters_dest}[sent][{key}]'.format(
                        counters_dest=counters_dest, key=key))

            self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src='{counters_src}[received][{key}]'.format(
                        counters_src=counters_src, key=key),
                      dest='{counters_dest}[received][{key}]'.format(
                        counters_dest=counters_dest, key=key))

        # ==============================================================
        #                  vrf: neighbor - address_family
        # ==============================================================

        # address_family
        #   nbr_af_name
        nbr_af_src = '[address_family][(?P<afname>{get_af_name})]'
        nbr_af_dest = '[address_family][(?P<afname>{get_af_name})]'

        # aggregated source and destination
        final_src = nbr_src+nbr_af_src
        final_dest = nbr_dest+nbr_af_dest

        nbr_af_keys = ['bgp_table_version', 'routing_table_version',\
            'prefixes', 'path', 'total_memory', 'session_state']

        for key in nbr_af_keys:

            # address_family
            #   nbr_af_name
            self.add_leaf(cmd=ShowBgpAllSummary,
                      src='{final_src}[{key}]'.format(
                        final_src=final_src, key=key),
                      dest='{final_dest}[{key}]'.format(
                        final_dest=final_dest, key=key))

        # allowas_in - N/A
        # allowas_in_as_number - N/A

        # inherit_peer_policy
        #   inherit_peer_seq - N/A

        # maximum_prefix_max_prefix_no - N/A
        # maximum_prefix_threshold - N/A
        # maximum_prefix_restart - N/A
        # maximum_prefix_warning_only - N/A

        # Get neighbors for input to:
        #  * 'show bgp all neighbors <neighbor> policy'
        #  * 'show bgp all neighbors <WORD> received-routes'
        self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src='[list_of_neighbors]',
                      dest='info[list_of_neighbors]')

        self.make()

        if hasattr (self, 'info') and\
           'list_of_neighbors' in self.info:

            for neighbor in sorted(self.info['list_of_neighbors']):

                # address_family
                #   nbr_af_name
                #     route_map_name_in
                self.add_leaf(cmd=ShowBgpAllNeighborsPolicy,
                              src='[vrf][(?P<vrf>.*)][neighbor]'
                                  '[{neighbor}]'.format(neighbor=neighbor)+
                                  nbr_af_src+'[nbr_af_route_map_name_in]',
                              dest='info[instance][default][vrf][(?P<vrf>.*)]'
                                   '[neighbor][{neighbor}]'.format(
                                    neighbor=neighbor)+nbr_af_dest+
                                   '[route_map_name_in]',
                              neighbor=neighbor)

                # address_family
                #   nbr_af_name
                #     route_map_name_out
                self.add_leaf(cmd=ShowBgpAllNeighborsPolicy,
                              src='[vrf][(?P<vrf>.*)][neighbor][{neighbor}]'.\
                              format(neighbor=neighbor)+nbr_af_src+
                              '[nbr_af_route_map_name_out]',
                              dest='info[instance][default][vrf][(?P<vrf>.*)]'
                                   '[neighbor][{neighbor}]'.format(neighbor=\
                                    neighbor)+nbr_af_dest+'[route_map_name_out]',
                              neighbor=neighbor)

            # clear list of neighbors
            del self.info['list_of_neighbors']

        # route_reflector_client - N/A
        # address_family
        #   nbr_af_name
        #     send_community - N/A
        # address_family
        #   nbr_af_name
        #     soft_configuration - N/A
        # next_hop_self - N/A
        # as_override - N/A
        # default_originate - N/A
        # default_originate_route_map - N/A
        # soo - N/A


        ########################################################################
        #                               table
        ########################################################################

        # vrf
        #   vrf_id
        #     address_family
        #       af_name
        table_src = '[vrf][(?P<vrf_name>.*)][address_family]'\
                    '[(?P<address_family>.*)]'
        table_dest = 'table[instance][default]'+ table_src

        table_keys = ['route_identifier', 'bgp_table_version',\
            'route_distinguisher', 'default_vrf']

        for key in table_keys:

            self.add_leaf(cmd=ShowBgpAll,
                      src='{table_src}[{key}]'.format(
                        table_src=table_src, key=key),
                      dest='{table_dest}[{key}]'.format(
                        table_dest=table_dest, key=key))

        # Building prefix section
        # paths
        self.add_leaf(cmd=ShowBgpAllDetail,
                      src='[instance][default][vrf][(?P<vrf_name>.*)]'\
                          '[address_family][(?P<address_family>.*)][prefixes]'\
                          '[(?P<prefix>.*)][paths]',
                      dest=table_dest+'[paths]')

        # table_version
        self.add_leaf(cmd=ShowBgpAllDetail,
                      src='[instance][default][vrf][(?P<vrf_name>.*)]'\
                          '[address_family][(?P<address_family>.*)][prefixes]'\
                          '[(?P<prefix>.*)][table_version]',
                      dest=table_dest+'[prefixes][(?P<prefix>.*)][table_version]')

        # Building index section
        index_src = '[instance][default][vrf][(?P<vrf_name>.*)]'\
                    '[address_family][(?P<address_family>.*)][prefixes]'\
                    '[(?P<prefix>.*)][index][(?P<index>.*)]'

        index_dest = table_dest+'[prefixes][(?P<prefix>.*)][index]'\
            '[(?P<index>.*)]'

        index_keys = ['next_hop', 'next_hop_igp_metric', 'gateway',\
            'update_group', 'status_codes', 'origin_codes', 'metric',\
            'localpref', 'weight', 'originator']

        for key in index_keys:

            self.add_leaf(cmd=ShowBgpAllDetail,
                      src='{index_src}[{key}]'.format(
                        index_src=index_src, key=key),
                      dest='{index_dest}[{key}]'.format(
                        index_dest=index_dest, key=key))

        # cluster_id - N/A
        # mpls_labels_inout - N/A
        # cluster_list - N/A

        # local_as
        self.add_leaf(cmd=ShowBgpAllSummary,
                      src=table_src+'[local_as]',
                      dest=table_dest+'[local_as]')

        # routing_table_version
        self.add_leaf(cmd=ShowBgpAllSummary,
                      src=table_src+'[routing_table_version]',
                      dest=table_dest+'[routing_table_version]')

        # ext_community
        self.add_leaf(cmd=ShowBgpAllDetail,
                      src='[instance][default][vrf][(?P<vrf_name>.*)]'
                          '[address_family][(?P<address_family>.*)]'
                          '[prefixes][(?P<prefix>.*)][index][(?P<index>.*)]'
                          '[evpn][ext_community]',
                      dest=table_dest+'[prefixes][(?P<prefix>.*)][index]'
                                      '[(?P<index>.*)][ext_community]')

        ########################################################################
        #                           routes_per_peer
        ########################################################################

        # Routes per peer top level key
        rpp_src = '[vrf][(?P<vrf>.*)][neighbor][(?P<neighbor>.*)]'\
                  '[address_family][(?P<address_family>.*)]'
        rpp_dest = 'routes_per_peer[instance][default][vrf][(?P<vrf>.*)]'\
                   '[neighbor][(?P<neighbor>.*)][address_family]'\
                   '[(?P<address_family>.*)]'

        rpp_keys = ['msg_rcvd', 'msg_sent', 'tbl_ver',\
            'input_queue', 'output_queue', 'up_down', 'state_pfxrcd']

        for key in rpp_keys:

            self.add_leaf(cmd=ShowBgpAllSummary,
                      src='{rpp_src}[{key}]'.format(
                        rpp_src=rpp_src, key=key),
                      dest='{rpp_dest}[{key}]'.format(
                        rpp_dest=rpp_dest, key=key))

        # remote_as
        self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src='[vrf][(?P<vrf>.*)][neighbor][(?P<neighbor>.*)]'
                          '[remote_as]',
                      dest='routes_per_peer[instance][default][vrf]'
                           '[(?P<vrf>.*)][neighbor][(?P<neighbor>.*)]'
                           '[remote_as]')

        # Get neighbors for input to:
        #  * 'show bgp all neighbors <WORD> advertised-routes'
        #  * 'show bgp all neighbors <WORD> received-routes'
        #  * 'show bgp all neighbors <WORD> routes'
        self.add_leaf(cmd=ShowBgpAllNeighbors,
                      src='[list_of_neighbors]',
                      dest='routes_per_peer[list_of_neighbors]')

        self.make()

        if hasattr (self, 'routes_per_peer') and\
           'list_of_neighbors' in self.routes_per_peer:

            for neighbor in sorted(self.routes_per_peer['list_of_neighbors']):

                # route_distinguisher
                self.add_leaf(cmd=ShowBgpAllNeighborsAdvertisedRoutes,
                              src='[vrf][(?P<vrf>.*)][neighbor][{neighbor}]'
                                  '[address_family][(?P<address_family>.*)]'
                                  '[route_distinguisher]'.format(
                                    neighbor=neighbor),
                              dest='routes_per_peer[instance][default][vrf]'
                                   '[(?P<vrf>.*)][neighbor][{neighbor}]'
                                   '[address_family][(?P<address_family>.*)]'
                                   '[route_distinguisher]'.format(
                                    neighbor=neighbor),
                              neighbor=neighbor)

                # default_vrf
                self.add_leaf(cmd=ShowBgpAllNeighborsAdvertisedRoutes,
                              src='[vrf][(?P<vrf>.*)][neighbor][{neighbor}]'
                                  '[address_family][(?P<address_family>.*)]'
                                  '[default_vrf]'.format(neighbor=neighbor),
                              dest='routes_per_peer[instance][default][vrf]'
                                   '[(?P<vrf>.*)][neighbor][{neighbor}]'
                                   '[address_family][(?P<address_family>.*)]'
                                   '[default_vrf]'.format(neighbor=neighbor),
                              neighbor=neighbor)

                # advertised
                self.add_leaf(cmd=ShowBgpAllNeighborsAdvertisedRoutes,
                              src='[vrf][(?P<vrf>.*)][neighbor][{neighbor}]'
                                  '[address_family][(?P<address_family>.*)]'
                                  '[advertised]'.format(neighbor=neighbor),
                              dest='routes_per_peer[instance][default][vrf]'
                                   '[(?P<vrf>.*)][neighbor][{neighbor}]'
                                   '[address_family][(?P<address_family>.*)]'
                                   '[advertised]'.format(neighbor=neighbor),
                              neighbor=neighbor)

                # routes
                self.add_leaf(cmd=ShowBgpAllNeighborsRoutes,
                              src='[vrf][(?P<vrf>.*)][neighbor][{neighbor}]'
                                  '[address_family][(?P<address_family>.*)]'
                                  '[routes]'.format(neighbor=neighbor),
                              dest='routes_per_peer[instance][default][vrf]'
                                   '[(?P<vrf>.*)][neighbor][{neighbor}]'
                                   '[address_family][(?P<address_family>.*)]'
                                   '[routes]'.format(neighbor=neighbor),
                              neighbor=neighbor)

                # received_routes
                self.add_leaf(cmd=ShowBgpAllNeighborsReceivedRoutes,
                              src='[vrf][(?P<vrf>.*)][neighbor][{neighbor}]'
                                  '[address_family][(?P<address_family>.*)]'
                                  '[received_routes]'.format(neighbor=neighbor),
                              dest='routes_per_peer[instance][default][vrf]'
                                   '[(?P<vrf>.*)][neighbor][{neighbor}]'
                                   '[address_family][(?P<address_family>.*)]'
                                   '[received_routes]'.format(
                                    neighbor=neighbor),
                              neighbor=neighbor)

            # clear list of neighbors
            del self.routes_per_peer['list_of_neighbors']

        ########################################################################
        #                           Final Structure
        ########################################################################

        # Make final Ops structure
        self.make()

        if hasattr (self, 'routes_per_peer'):
            # Removing 'path_type' from the ops structure
            for vrf in self.routes_per_peer['instance']['default']['vrf']:
                for neighbor in self.routes_per_peer['instance']['default']\
                    ['vrf'][vrf]['neighbor']:
                    if 'address_family' in self.routes_per_peer['instance']\
                        ['default']['vrf'][vrf]['neighbor'][neighbor]:
                        for add_family in self.routes_per_peer['instance']\
                            ['default']['vrf'][vrf]['neighbor'][neighbor]\
                                ['address_family']:
                            if 'advertised' in self.routes_per_peer['instance']\
                                ['default']['vrf'][vrf]['neighbor'][neighbor]\
                                    ['address_family'][add_family]:
                                for route in self.routes_per_peer['instance']\
                                    ['default']['vrf'][vrf]['neighbor'][neighbor]\
                                        ['address_family'][add_family]\
                                            ['advertised']:
                                    for idx in self.routes_per_peer['instance']\
                                        ['default']['vrf'][vrf]['neighbor']\
                                            [neighbor]['address_family']\
                                            [add_family]['advertised'][route]\
                                            ['index']:
                                        if 'path_type' in self.routes_per_peer\
                                            ['instance']['default']['vrf'][vrf]\
                                            ['neighbor'][neighbor]\
                                            ['address_family'][add_family]\
                                            ['advertised'][route]['index'][idx]:
                                            del self.routes_per_peer['instance']\
                                                ['default']['vrf'][vrf]['neighbor']\
                                                    [neighbor]['address_family']\
                                                        [add_family]['advertised']\
                                                        [route]['index'][idx]\
                                                        ['path_type']
                            if 'received_routes' in self.routes_per_peer\
                                ['instance']['default']['vrf'][vrf]['neighbor']\
                                    [neighbor]['address_family'][add_family]:
                                for route in self.routes_per_peer['instance']\
                                    ['default']['vrf'][vrf]['neighbor'][neighbor]\
                                        ['address_family'][add_family]\
                                            ['received_routes']:
                                    for idx in self.routes_per_peer['instance']\
                                        ['default']['vrf'][vrf]['neighbor']\
                                            [neighbor]['address_family']\
                                            [add_family]['received_routes'][route]\
                                            ['index']:
                                        if 'path_type' in self.routes_per_peer\
                                            ['instance']['default']['vrf'][vrf]\
                                            ['neighbor'][neighbor]\
                                            ['address_family'][add_family]\
                                            ['received_routes'][route]['index']\
                                            [idx]:
                                            del self.routes_per_peer['instance']\
                                                ['default']['vrf'][vrf]['neighbor']\
                                                    [neighbor]['address_family']\
                                                        [add_family]\
                                                        ['received_routes'][route]\
                                                        ['index'][idx]['path_type']
                            if 'routes' in self.routes_per_peer\
                                ['instance']['default']['vrf'][vrf]['neighbor']\
                                    [neighbor]['address_family'][add_family]:
                                for route in self.routes_per_peer['instance']\
                                    ['default']['vrf'][vrf]['neighbor'][neighbor]\
                                        ['address_family'][add_family]\
                                            ['routes']:
                                    for idx in self.routes_per_peer['instance']\
                                        ['default']['vrf'][vrf]['neighbor']\
                                            [neighbor]['address_family']\
                                            [add_family]['routes'][route]\
                                            ['index']:
                                        if 'path_type' in self.routes_per_peer\
                                            ['instance']['default']['vrf'][vrf]\
                                            ['neighbor'][neighbor]\
                                            ['address_family'][add_family]\
                                            ['routes'][route]['index']\
                                            [idx]:
                                            del self.routes_per_peer['instance']\
                                                ['default']['vrf'][vrf]['neighbor']\
                                                    [neighbor]['address_family']\
                                                        [add_family]\
                                                        ['routes'][route]\
                                                        ['index'][idx]['path_type']