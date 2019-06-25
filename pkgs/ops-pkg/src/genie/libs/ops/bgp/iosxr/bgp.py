''' 
BGP Genie Ops Object for IOSXR - CLI.
'''

# Super class
from genie.libs.ops.bgp.bgp import Bgp as SuperBgp

# Parser
from genie.libs.parser.iosxr.show_bgp import ShowPlacementProgramAll,\
                                  ShowBgpInstanceAfGroupConfiguration,\
                                  ShowBgpInstanceSessionGroupConfiguration,\
                                  ShowBgpInstanceProcessDetail,\
                                  ShowBgpInstanceNeighborsDetail,\
                                  ShowBgpInstanceNeighborsAdvertisedRoutes,\
                                  ShowBgpInstanceNeighborsReceivedRoutes,\
                                  ShowBgpInstanceNeighborsRoutes,\
                                  ShowBgpInstanceSummary,\
                                  ShowBgpInstanceAllAll, ShowBgpInstances


class Bgp(SuperBgp):
    '''BGP Genie Ops Object'''

    # Callables
    def get_key(self, item):
        # For the sake of simplicity and in the interest of time, 
        # this has been done to reduce the number of for loops for easier
        # maintenance and readability
        # self.neighbors = item.keys()
        return list(item.keys())

    def learn(self, instance='all', vrf='all', address_family='', neighbor=''):
        '''Learn BGP Ops'''

        ########################################################################
        #                               info
        ########################################################################

        # instance
        #   instance_name

        # bgp_id
        self.add_leaf(cmd=ShowBgpInstances,
                      src='[instance][(?P<instance>.*)][bgp_id][(?P<bgp_id>.*)]',
                      dest='info[instance][(?P<instance>.*)][bgp_id][(?P<bgp_id>.*)]')

        # protocol_state
        self.add_leaf(cmd=ShowPlacementProgramAll,
                      src='[program][bgp][instance][(?P<instance>.*)][active_state][(?P<active_state>.*)]',
                      dest='info[instance][(?P<instance>.*)][protocol_state][(?P<active_state>.*)]')

        # ======================================================================
        #                           peer_session
        # ======================================================================

        # peer_session
        #   ps_name
        ps_source = '[(?P<instance>.*)][peer_session][(?P<session_session>.*)]'
        ps_dest = 'info[instance][(?P<instance>.*)][peer_session][(?P<session_session>.*)]'

        peer_session_keys = ['fall_over_bfd', 'suppress_four_byte_as_capability',\
                'description', 'disable_connected_check', 'ebgp_multihop_enable',\
                'ebgp_multihop_max_hop', 'local_as_as_no', 'local_no_prepend',\
                'local_dual_as', 'local_replace_as', 'password_text', 'remote_as',\
                'shutdown', 'keepalive_interval', 'holdtime', 'update_source',\
                'transport_connection_mode']

        for key in peer_session_keys:

            self.add_leaf(cmd=ShowBgpInstanceSessionGroupConfiguration,
                          src='{ps_source}[{key}]'.format(ps_source=ps_source,key=key),
                          dest='{ps_dest}[{key}]'.format(ps_dest=ps_dest,key=key))


        # ======================================================================
        #                           peer_policy
        # ======================================================================

        # peer_policy
        #   pp_name
        pp_src = '[instance][(?P<instance>.*)][pp_name][(?P<peer_policy>.*)]'
        pp_dest = 'info[instance][(?P<instance>.*)][peer_policy][(?P<peer_policy>.*)]'

        peer_policy_keys = ['allowas_in', 'allowas_in_as_number', 'as_override',\
                            'default_originate', 'default_originate_route_map',\
                            'route_map_name_in', 'route_map_name_out',\
                            'next_hop_self', 'route_reflector_client',\
                            'send_community', 'soft_reconfiguration', 'soo',\
                            'maximum_prefix_max_prefix_no',\
                            'maximum_prefix_threshold', 'maximum_prefix_restart',\
                            'maximum_prefix_warning_only']

        for key in peer_policy_keys:

            self.add_leaf(cmd=ShowBgpInstanceAfGroupConfiguration,
                      src='{pp_src}[{key}]'.format(pp_src=pp_src,key=key),
                      dest='{pp_dest}[{key}]'.format(pp_dest=pp_dest,key=key))


        # ======================================================================
        #                               vrf
        # ======================================================================

        # Init vrf first loop
        vrf_loop1 = False

        for vrf_type in ['all', 'vrf']:
            if vrf != 'all':
                vrf_type = 'vrf'

            for af in ['ipv4 unicast', 'ipv6 unicast']:
                if address_family:
                    af=address_family
                # Set or skip 'all all all' iteration
                if vrf_type == 'all':
                    if vrf_loop1:
                        continue
                    else:
                        af = ''
                        vrf_loop1 = True
                # vrf
                #   vrf_id
                vrf_src = '[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)]'
                vrf_dest = 'info[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)]'

                vrf_keys = ['always_compare_med', 'bestpath_compare_routerid',
                            'bestpath_cost_community_ignore',
                            'bestpath_med_missin_at_worst', 'cluster_id',
                            'log_neighbor_changes', 'router_id',
                            'enforce_first_as', 'fast_external_fallover']
                for key in vrf_keys:

                    # set key values
                    src_key = dest_key = key

                    if key == 'cluster_id':
                        src_key = 'active_cluster_id'

                    self.add_leaf(cmd=ShowBgpInstanceProcessDetail,
                          src='{vrf_src}[{src_key}]'.format(vrf_src=vrf_src,src_key=src_key),
                          dest='{vrf_dest}[{dest_key}]'.format(vrf_dest=vrf_dest,dest_key=dest_key),
                          vrf_type=vrf_type, vrf=vrf, instance=instance,
                                  address_family=af)

                # confederation_identifier - N/A
                # confederation_peer_as - N/A
                # graceful_restart - N/A
                # graceful_restart_restart_time - N/A
                # graceful_restart_stalepath_time - N/A
                # keepalive_interval - ??
                # holdtime - ??
                # default_choice_ipv4_unicast - N/A

                # ==============================================================
                #                     vrf: address_family
                # ==============================================================

                # address_family
                #   af_name
                af_src = vrf_src + '[address_family][(?P<address_family>.*)]'
                af_dest = vrf_dest + '[address_family][(?P<address_family>.*)]'

                vrf_af_keys = ['dampening', 'dampening_route_map',\
                               'dampening_half_life_time', 'dampening_reuse_time',\
                               'dampening_suppress_time', 'dampening_max_suppress_time',\
                               'client_to_client_reflection']

                for key in vrf_af_keys:

                    # set key values
                    src_key = dest_key = key

                    self.add_leaf(cmd=ShowBgpInstanceProcessDetail,
                                  src='{af_src}[{src_key}]'.format(af_src=af_src,src_key=src_key),
                                  dest='{af_dest}[{dest_key}]'.format(af_dest=af_dest,dest_key=dest_key),
                                  vrf_type=vrf_type, vrf=vrf,
                                  instance=instance, address_family=af)

                # nexthop_route_map - N/A
                # nexthop_trigger_enable - N/A
                # nexthop_trigger_delay_critical - N/A
                # nexthop_trigger_delay_non_critical - N/A
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

                # ==============================================================
                #                        vrf: neighbor
                # ==============================================================

                # neighbor
                #   neighbor_id
                nbr_src = '[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)][neighbor][(?P<neighbor>.*)]'
                nbr_dest = 'info[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)][neighbor][(?P<neighbor>.*)]'

                nbr_keys = ['suppress_four_byte_as_capability', 'description',\
                            'ebgp_multihop', 'ebgp_multihop_max_hop',\
                            'local_as_as_no', 'local_as_no_prepend',\
                            'local_as_replace_as', 'local_as_dual_as',\
                            'remote_as', 'remove_private_as', 'shutdown',\
                            'keepalive_interval', 'holdtime', \
                            'transport_connection_mode', 'session_state',\
                            'bgp_negotiated_keepalive_timers',\
                            'minimum_neighbor_hold', 'up_time', ]

                for key in nbr_keys:

                    # set key values
                    src_key = dest_key = key

                    if key == 'minimum_neighbor_hold':
                        src_key = 'min_acceptable_hold_time'

                    self.add_leaf(cmd=ShowBgpInstanceNeighborsDetail,
                                  src='{nbr_src}[{src_key}]'.format(nbr_src=nbr_src,src_key=src_key),
                                  dest='{nbr_dest}[{dest_key}]'.format(nbr_dest=nbr_dest,dest_key=dest_key),
                                  vrf_type=vrf_type, vrf=vrf,
                                  instance=instance, address_family=af,
                                  neighbor=neighbor)

                # fall_over_bfd - N/A
                # disable_connected_check - N/A
                # inherit_peer_session - N/A
                # bgp_version - ??
                # installed_prefixes - ??
                # update_source - N/A
                # password_text - N/A

                # bgp_session_transport
                #   connection
                #     state
                #     mode
                #     last_reset
                #     reset_reason
                self.add_leaf(cmd=ShowBgpInstanceNeighborsDetail,
                              src=nbr_src+'[bgp_session_transport][connection]',
                              dest=nbr_dest+'[bgp_session_transport][connection]',
                              vrf_type=vrf_type, vrf=vrf,
                                  instance=instance, address_family=af,
                                  neighbor=neighbor)

                # bgp_session_transport
                #   transport
                #     local_port
                #     local_host
                #     foreign_port
                #     foreign_host
                #     mss
                self.add_leaf(cmd=ShowBgpInstanceNeighborsDetail,
                              src=nbr_src+'[bgp_session_transport][transport]',
                              dest=nbr_dest+'[bgp_session_transport][transport]',
                              vrf_type=vrf_type, vrf=vrf,
                                  instance=instance, address_family=af,
                                  neighbor=neighbor)

                # bgp_negotiated_capabilities
                #   route_refresh
                self.add_leaf(cmd=ShowBgpInstanceNeighborsDetail,
                              src=nbr_src+'[bgp_negotiated_capabilities][route_refresh]',
                              dest=nbr_dest+'[bgp_negotiated_capabilities][route_refresh]',
                              vrf_type=vrf_type, vrf=vrf,
                                  instance=instance, address_family=af,
                                  neighbor=neighbor)

                # bgp_negotiated_capabilities
                #   four_octets_asn
                self.add_leaf(cmd=ShowBgpInstanceNeighborsDetail,
                              src=nbr_src+'[bgp_negotiated_capabilities][four_octets_asn]',
                              dest=nbr_dest+'[bgp_negotiated_capabilities][four_octets_asn]',
                              vrf_type=vrf_type, vrf=vrf,
                                  instance=instance, address_family=af,
                                  neighbor=neighbor)

                # bgp_negotiated_capabilities
                #   vpnv4_unicast
                self.add_leaf(cmd=ShowBgpInstanceNeighborsDetail,
                              src=nbr_src+'[bgp_negotiated_capabilities][vpnv4_unicast]',
                              dest=nbr_dest+'[bgp_negotiated_capabilities][vpnv4_unicast]',
                              vrf_type=vrf_type, vrf=vrf,
                                  instance=instance, address_family=af,
                                  neighbor=neighbor)

                # bgp_negotiated_capabilities
                #   vpnv6_unicast
                self.add_leaf(cmd=ShowBgpInstanceNeighborsDetail,
                              src=nbr_src+'[bgp_negotiated_capabilities][vpnv6_unicast]',
                              dest=nbr_dest+'[bgp_negotiated_capabilities][vpnv6_unicast]',
                              vrf_type=vrf_type, vrf=vrf,
                                  instance=instance, address_family=af,
                                  neighbor=neighbor)

                # bgp_negotiated_capabilities
                #   graceful_restart - N/A

                # bgp_negotiated_capabilities
                #   enhanced_refresh - N/A

                # bgp_negotiated_capabilities
                #   multisession - N/A

                # bgp_negotiated_capabilities
                #   stateful_switchover - N/A

                # bgp_neighbor_counters
                #   messages
                #     sent
                #       opens
                #       updates
                #       notifications
                #       keepalives
                #       route_refreshes
                self.add_leaf(cmd=ShowBgpInstanceNeighborsDetail,
                              src=nbr_src+'[bgp_neighbor_counters][messages][sent]',
                              dest=nbr_dest+'[bgp_neighbor_counters][messages][sent]',
                              vrf_type=vrf_type, vrf=vrf,
                                  instance=instance, address_family=af,
                                  neighbor=neighbor)

                # bgp_neighbor_counters
                #   messages
                #     received
                #       opens
                #       updates
                #       notifications
                #       keepalives
                #       route_refreshes
                self.add_leaf(cmd=ShowBgpInstanceNeighborsDetail,
                              src=nbr_src+'[bgp_neighbor_counters][messages][received]',
                              dest=nbr_dest+'[bgp_neighbor_counters][messages][received]',
                              vrf_type=vrf_type, vrf=vrf,
                                  instance=instance, address_family=af,
                                  neighbor=neighbor)

                # ==============================================================
                #                  vrf: neighbor - address_family
                # ==============================================================

                # nbr_address_family
                #   nbr_af_name
                nbr_af_src = nbr_src + '[address_family][(?P<address_family>.*)]'
                nbr_af_dest = nbr_dest + '[address_family][(?P<address_family>.*)]'

                nbr_af_keys = ['bgp_table_version', 'allowas_in',\
                               'allowas_in_as_number', 'route_map_name_in',\
                               'route_map_name_out', 'route_reflector_client',\
                               'send_community', 'soft_configuration', 'as_override',\
                               'default_originate', 'default_originate_route_map',\
                               'soo', 'maximum_prefix_max_prefix_no',\
                               'maximum_prefix_threshold', 'maximum_prefix_restart',\
                               'maximum_prefix_warning_only']

                for key in nbr_af_keys:

                    # set key values
                    src_key = dest_key = key

                    if key == 'bgp_table_version':
                        src_key = 'neighbor_version'

                    self.add_leaf(cmd=ShowBgpInstanceNeighborsDetail,
                                  src='{nbr_af_src}[{src_key}]'.format(nbr_af_src=nbr_af_src,src_key=src_key),
                                  dest='{nbr_af_dest}[{dest_key}]'.format(nbr_af_dest=nbr_af_dest,dest_key=dest_key),
                                  vrf_type=vrf_type, vrf=vrf,
                                  instance=instance, address_family=af,
                                  neighbor=neighbor)
                if address_family:
                    break
                # routing_table_version - N/A
                # prefixes - N/A
                #   total_entries - N/A
                #   memory_usage - N/A
                # path - N/A
                #   total_entries - N/A
                #   memory_usage - N/A
                # total_memory - N/A
                # inherit_peer_policy - N/A
                # inherit_peer_seq - N/A
                # next_hop_self - N/A

        ########################################################################
        #                               table
        ########################################################################

        # Init table first loop
        table_loop1 = False

        for vrf_type in ['all', 'vrf']:
            if vrf != 'all':
                vrf_type = 'vrf'

            # Set or skip 'all all all' iteration
            if vrf_type == 'all':
                if table_loop1:
                    continue
                else:

                    table_loop1 = True

            # instance
            #   instance_name
            #     vrf
            #       vrf_id
            #         address_family
            #           af_name
            tbl_src = '[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)][address_family][(?P<address_family>.*)]'
            tbl_dest = 'table[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)][address_family][(?P<address_family>.*)]'

            table_keys = ['route_distinguisher', 'default_vrf',\
                          'route_identifier', 'local_as',\
                          'bgp_table_version', 'prefixes']

            for key in table_keys:

                # set key values
                src_key = dest_key = key

                if key == 'prefixes':
                    src_key = 'prefix'

                self.add_leaf(cmd=ShowBgpInstanceAllAll,
                              src='{tbl_src}[{src_key}]'.format(tbl_src=tbl_src,src_key=src_key),
                              dest='{tbl_dest}[{dest_key}]'.format(tbl_dest=tbl_dest,dest_key=dest_key),
                              vrf_type=vrf_type, vrf=vrf, instance=instance, address_family=address_family)

            # paths - N/A

        # ########################################################################
        # #                           routes_per_peer
        # ########################################################################
        
        # Init routes_per_peer first loop
        rpp_loop1 = False

        for vrf_type in ['all', 'vrf']:
            if vrf != 'all':
                vrf_type = 'vrf'
            for af in ['ipv4 unicast', 'ipv6 unicast']:
                if address_family:
                    af = address_family

                # Set or skip 'all all all' iteration
                if vrf_type == 'all':
                    if rpp_loop1:
                        continue
                    else:
                        af = ''
                        rpp_loop1 = True

                # instance
                #   instance_name
                #     vrf
                #       vrf_name
                #         neighbor
                #           neighbor_id
                rpp_src = '[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)][neighbor][(' \
                          '?P<neighbor_id>.*)]'
                rpp_dest = 'routes_per_peer[instance][(?P<instance>.*)][vrf][(' \
                           '?P<vrf>.*)][neighbor][(?P<neighbor_id>.*)]'

                # remote_as
                self.add_leaf(cmd=ShowBgpInstanceSummary,
                              src=rpp_src + '[remote_as]',
                              dest=rpp_dest + '[remote_as]',
                              vrf_type=vrf_type, address_family=af,
                              vrf=vrf, instance=instance)

                # address_family
                #   af_name
                rpp_af_src = rpp_src + '[address_family][(?P<address_family>.*)]'
                rpp_af_dest = rpp_dest + '[address_family][(?P<address_family>.*)]'

                rpp_af_keys = ['route_distinguisher', 'default_vrf', 'msg_rcvd',
                               'msg_sent', 'tbl_ver', 'input_queue',
                               'output_queue', 'up_down', 'state_pfxrcd']

                for key in rpp_af_keys:
                    # set key values
                    src_key = dest_key = key

                    self.add_leaf(cmd=ShowBgpInstanceSummary,
                                  src='{rpp_af_src}[{src_key}]'.format(
                                      rpp_af_src=rpp_af_src, src_key=src_key),
                                  dest='{rpp_af_dest}[{dest_key}]'.format(
                                      rpp_af_dest=rpp_af_dest, dest_key=dest_key),
                                  vrf_type=vrf_type, address_family=af,
                                  vrf=vrf, instance=instance)
                if address_family:
                    break

        # Get list of neighbors
        
        # Init list
        rpp_nbrs_loop1 = False
        for vrf_type in ['all', 'vrf']:
            if vrf != 'all':
                vrf_type = 'vrf'
            for af in ['ipv4 unicast', 'ipv6 unicast']:
                if address_family:
                    af = address_family
                # Set or skip 'all all all' iteration
                if vrf_type == 'all':
                    if rpp_nbrs_loop1:
                        continue
                    else:
                        af = ''
                        rpp_nbrs_loop1 = True

                self.add_leaf(cmd=ShowBgpInstanceNeighborsDetail,
                              src='[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)][neighbor]',
                              dest='neighbors',
                              vrf_type=vrf_type, address_family=af, vrf=vrf,
                              instance=instance, neighbor=neighbor, action=self.get_key)
                self.make()

                if hasattr(self, 'neighbors'):

                    for nbr in sorted(self.neighbors):
                        # print('\nneighbor is {neighbor}'.format(neighbor=neighbor))

                        # advertised
                        self.add_leaf(cmd=ShowBgpInstanceNeighborsAdvertisedRoutes,
                                      src='[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][advertised]',
                                      dest='routes_per_peer[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)][neighbor][{neighbor}][address_family][(?P<af>.*)][advertised]'.format(
                                          neighbor=nbr),
                                      vrf_type=vrf_type, neighbor=nbr, vrf=vrf, instance=instance,
                                      address_family=af)

                        # received
                        self.add_leaf(cmd=ShowBgpInstanceNeighborsReceivedRoutes,
                                      src='[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][received]',
                                      dest='routes_per_peer[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)][neighbor][{neighbor}][address_family][(?P<af>.*)][received_routes]'.format(
                                          neighbor=nbr),
                                      vrf_type=vrf_type, neighbor=nbr,
                                      address_family=af, vrf=vrf,
                                        instance=instance,)

                        # routes
                        self.add_leaf(cmd=ShowBgpInstanceNeighborsRoutes,
                                      src='[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][routes]',
                                      dest='routes_per_peer[instance][(?P<instance>.*)][vrf][(?P<vrf>.*)][neighbor][{neighbor}][address_family][(?P<af>.*)][routes]'.format(
                                          neighbor=nbr),
                                      vrf_type=vrf_type, neighbor=nbr,
                                      address_family=af, vrf=vrf,
                                        instance=instance,)

                    # Delete neighbors for this iteration
                    del self.neighbors
                if address_family:
                    break

        ########################################################################
        #                           Final Structure
        ########################################################################

        # Make final Ops structure
        self.make(final_call=True)
        
        # Delete unnecessary keys
        try:
            del self.list_of_neighbors
        except:
            pass