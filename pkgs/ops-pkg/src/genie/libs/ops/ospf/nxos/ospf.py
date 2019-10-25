''' 
OSPF Genie Ops Object for NXOS - CLI.
'''

# super class
from genie.libs.ops.ospf.ospf import Ospf as SuperOspf

# Parser
from genie.libs.parser.nxos.show_ospf import ShowIpOspf,\
                                  ShowIpOspfMplsLdpInterface,\
                                  ShowIpOspfVirtualLinks,\
                                  ShowIpOspfShamLinks,\
                                  ShowIpOspfInterface,\
                                  ShowIpOspfNeighborDetail,\
                                  ShowIpOspfDatabaseExternalDetail,\
                                  ShowIpOspfDatabaseNetworkDetail,\
                                  ShowIpOspfDatabaseSummaryDetail,\
                                  ShowIpOspfDatabaseRouterDetail,\
                                  ShowIpOspfDatabaseOpaqueAreaDetail

# nxos show_feature
from genie.libs.parser.nxos.show_feature import ShowFeature


class Ospf(SuperOspf):
    '''Ospf Ops Object'''

    def set_enable(self, key):
        for inst in key:
            if 'state' not in key[inst]:
                continue
            if key[inst]['state'] == 'enabled':
                return True
        return False

    def learn(self, vrf='all', interface='', neighbor=''):
        '''Learn Ospf object'''

        # feature_ospf
        self.add_leaf(cmd=ShowFeature,
                      src='[feature][ospf][instance]',
                      dest='info[feature_ospf]',
                      action=self.set_enable)

        ########################################################################
        #                               info
        ########################################################################

        # vrf
        #   vrf_name
        #     address_family
        #       af_name
        #         instance
        #           instance_name
        info_src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][instance][(?P<instance>.*)]'
        info_dest = 'info' + info_src


        # router_id
        self.add_leaf(cmd=ShowIpOspf,
                      src=info_src+'[router_id]',
                      dest=info_dest+'[router_id]',
                      vrf=vrf)

        #  maximum_interfaces - N/A

        # preference
        #   single_value
        #     all
        #   multi_values - N/A
        #     granularity - N/A
        #       detail - N/A
        #         inter_area - N/A
        #         intra_area - N/A
        #     external - N/A
        self.add_leaf(cmd=ShowIpOspf,
                      src=info_src+'[preference][single_value][all]',
                      dest=info_dest+'[preference][single_value][all]',
                      vrf=vrf)
        
        # redistribution
        #   max_prefix - N/A
        #     num_of_prefix - N/A
        #     prefix_thld - N/A
        #     warn_only - N/A
        #   bgp - N/A
        #     bgp_id - N/A
        #     metric - N/A
        #     metric_type - N/A
        #     nssa_only - N/A
        #     route_map - N/A
        #     subnets - N/A
        #     tag - N/A
        #     lsa_type_summary - N/A
        #     preserve_med - N/A
        #   connected - N/A
        #     enabled - N/A
        #     metric - N/A
        #     route_policy - N/A
        #   static - N/A
        #     enabled - N/A
        #     metric - N/A
        #     route_policy - N/A
        #   isis - N/A
        #     isis_pid - N/A
        #     metric - N/A
        #     route_policy - N/A

        # nsr
        #   enable
        self.add_leaf(cmd=ShowIpOspf,
                      src=info_src+'[nsr][enable]',
                      dest=info_dest+'[nsr][enable]',
                      vrf=vrf)

        # graceful_restart
        #   gr_type
        #     enable
        #     type
        #     helper_enable - N/A
        #     restart_interval
        #     helper_strict_lsa_checking - N/A
        for key in ['enable', 'type', 'restart_interval']:
            self.add_leaf(cmd=ShowIpOspf,
                          src=info_src+'[graceful_restart][ietf][{key}]'.format(key=key),
                          dest=info_dest+'[graceful_restart][ietf][{key}]'.format(key=key),
                          vrf=vrf)
        
        # enable
        self.add_leaf(cmd=ShowIpOspf,
                      src=info_src+'[enable]',
                      dest=info_dest+'[enable]',
                      vrf=vrf)

        # auto_cost
        #   enable
        #   reference_bandwith
        for key in ['enable', 'reference_bandwidth']:
            self.add_leaf(cmd=ShowIpOspf,
                          src=info_src+'[auto_cost][{key}]'.format(key=key),
                          dest=info_dest+'[auto_cost][{key}]'.format(key=key),
                          vrf=vrf)

        # spf_control
        #   paths
        self.add_leaf(cmd=ShowIpOspf,
                      src=info_src+'[spf_control][paths]',
                      dest=info_dest+'[spf_control][paths]',
                      vrf=vrf)

        # spf_control
        #   throttle
        #     spf
        #       start
        #       hold
        #       maximum
        #     lsa
        #       start
        #       hold
        #       maximum
        for key1 in ['spf', 'lsa']:
            for key2 in ['start', 'hold', 'maximum']:
                self.add_leaf(cmd=ShowIpOspf,
                              src=info_src+'[spf_control][throttle][{key1}][{key2}]'.format(key1=key1, key2=key2),
                              dest=info_dest+'[spf_control][throttle][{key1}][{key2}]'.format(key1=key1, key2=key2),
                              vrf=vrf)

        # database_control
        #   max_lsa
        self.add_leaf(cmd=ShowIpOspf,
                      src=info_src+'[database_control][max_lsa]',
                      dest=info_dest+'[database_control][max_lsa]',
                      vrf=vrf)

        # stub_router
        #   always
        #     always
        #     include_stub
        #     summary_lsa
        #     external_lsa
        for key in ['always', 'include_stub', 'summary_lsa', 'external_lsa']:
            self.add_leaf(cmd=ShowIpOspf,
                          src=info_src+'[stub_router][always][{key}]'.format(key=key),
                          dest=info_dest+'[stub_router][always][{key}]'.format(key=key),
                          vrf=vrf)
        # stub_router
        #   on_startup
        #     on_startup
        #     include_stub
        #     summary_lsa
        #     external_lsa
        for key in ['on_startup', 'include_stub', 'summary_lsa', 'external_lsa']:
            self.add_leaf(cmd=ShowIpOspf,
                          src=info_src+'[stub_router][on_startup][{key}]'.format(key=key),
                          dest=info_dest+'[stub_router][on_startup][{key}]'.format(key=key),
                          vrf=vrf)

        # stub_router
        #   on_switchover - N/A
        #     on_switchover - N/A
        #     include_stub - N/A
        #     summary_lsa - N/A
        #     external_lsa -N/A
        

        # default_originate - N/A
        #   default_originate - N/A
        #   always - N/A

        # mpls - N/A
        #   te - N/A
        #     router_id - N/A
        #   ldp - N/A
        #     autoconfig - N/A
        #     autoconfig_area_id - N/A
        #     ldp_igp_sync - N/A

        # local_rib - N/A
        #   prefix - N/A
        #     prefix - N/A
        #     next_hops - N/A
        #       next_hop - N/A
        #         outgoing_interface - N/A
        #         next_hop - N/A
        #     metric - N/A
        #     route_type - N/A
        #     route_tag - N/A

        # bfd
        #   enable
        #   strict_mode - N/A
        self.add_leaf(cmd=ShowIpOspf,
                      src=info_src+'[bfd][enable]',
                      dest=info_dest+'[bfd][enable]',
                      vrf=vrf)

        # log_adjacency_changes - N/A
        #   enable - N/A
        #   detail - N/A

        # adjacency_stagger - N/A
        #   initial_number - N/A
        #   maximum_number - N/A
        #   disable - N/A
        #   no_initial_limit - N/A

        # ======================================================================
        #                    areas: miscellaneous keys
        # ======================================================================

        # areas
        #   area_name
        area_src = info_src+'[areas][(?P<area>.*)]'
        area_dest = info_dest+'[areas][(?P<area>.*)]'

        # area_id
        # area_type
        # summary
        # default_cost
        for key in ['area_id', 'area_type', 'summary' 'default_cost']:
            self.add_leaf(cmd=ShowIpOspf,
                          src=area_src+'[{key}]'.format(key=key),
                          dest=area_dest+'[{key}]'.format(key=key),
                          vrf=vrf)

        # bfd - N/A
        #   enable
        #   minimum_interval
        #   multiplier

        # enabled_networks - N/A
        #   en_network -N/A
        #     network - N/A
        #     wildcard - N/A

        # mpls
        #   te - N/A
        #     enable - N/A
        
        # mpls
        #   ldp
        #     auto_config
        #     sync_igp_shortcuts - N/A
        self.add_leaf(cmd=ShowIpOspfMplsLdpInterface,
                      src=area_src+'[mpls][ldp][autoconfig]',
                      dest=area_dest+'[mpls][ldp][auto_config]',
                      vrf=vrf, interface=interface)

        # mpls
        #   ldp
        #     sync
        self.add_leaf(cmd=ShowIpOspfMplsLdpInterface,
                      src=area_src+'[mpls][ldp][igp_sync]',
                      dest=area_dest+'[mpls][ldp][sync]',
                      vrf=vrf, interface=interface)

        # ranges
        #   range_name
        #     prefix
        #     advertise
        #     cost
        for key in ['prefix', 'advertise', 'cost']:
            self.add_leaf(cmd=ShowIpOspf,
                              src=area_src+'[ranges][(?P<range>.*)][{key}]'.format(key=key),
                              dest=area_dest+'[ranges][(?P<range>.*)][{key}]'.format(key=key),
                              vrf=vrf)

        # statistics
        #   spf_runs_count
        #   abr_count - N/A
        #   asbr_count - N/A
        #   as_nssa_translator_event_count - N/A
        #   area_scope_lsa_count
        #   area_scope_lsa_cksum_sum
        for key in ['spf_runs_count', 'area_scope_lsa_count', 'area_scope_lsa_cksum_sum']:
            self.add_leaf(cmd=ShowIpOspf,
                          src=area_src+'[statistics][{key}]'.format(key=key),
                          dest=area_dest+'[statistics][{key}]'.format(key=key),
                          vrf=vrf)

        # passive - N/A
        # mtu_ignore - N/A
        # demand_circuit - N/A
        # external_out - N/A
        # flood_reduction - N/A
        # link_down_fast_detect - N/A

        # ======================================================================
        #                       database <any>: header
        # ======================================================================

        # database
        #   lsa_types
        #     lsa_type_name
        #       lsas
        #         lsa_name
        db_src = area_src + '[database][lsa_types][(?P<lsa_type>.*)][lsas][(?P<lsa>.*)]'
        db_dest = area_dest + '[database][lsa_types][(?P<lsa_type>.*)][lsas][(?P<lsa>.*)]'

        # Loop over all database related show commands to set keys
        for cmd in [ShowIpOspfDatabaseRouterDetail,
                    ShowIpOspfDatabaseNetworkDetail,
                    ShowIpOspfDatabaseSummaryDetail,
                    ShowIpOspfDatabaseExternalDetail,
                    ShowIpOspfDatabaseOpaqueAreaDetail]:

            # database
            #   lsa_types
            #     lsa_type_name
            #       lsas
            #         lsa_name
            self.add_leaf(cmd=cmd,
                          src=area_src+'[database][lsa_types][(?P<lsa_type>.*)][lsa_type]',
                          dest=area_dest+'[database][lsa_types][(?P<lsa_type>.*)][lsa_type]',
                          vrf=vrf)

            # lsa_id
            self.add_leaf(cmd=cmd,
                          src=db_src+'[lsa_id]',
                          dest=db_dest+'[lsa_id]',
                          vrf=vrf)

            # adv_router
            self.add_leaf(cmd=cmd,
                          src=db_src+'[adv_router]',
                          dest=db_dest+'[adv_router]',
                          vrf=vrf)
            
            # decoded_completed - N/A
            # raw_data - N/A

            # ospfv2
            #   header
            #     option
            #     lsa_id
            #     opaque_type
            #     opaque_id
            #     age
            #     type
            #     adv_router
            #     seq_num
            #     checksum
            #     length
            for key in ['option', 'lsa_id', 'opaque_type', 'opaque_id', 'age',
                        'type', 'adv_router', 'seq_num', 'checksum', 'length']:
                self.add_leaf(cmd=cmd,
                              src=db_src+'[ospfv2][header][{key}]'.format(key=key),
                              dest=db_dest+'[ospfv2][header][{key}]'.format(key=key),
                              vrf=vrf)

        # ======================================================================
        #                       database router: body
        # ======================================================================

        # ospfv2
        #   body
        #     router
        rbody_src = db_src + '[ospfv2][body][router]'
        rbody_dest = db_dest + '[ospfv2][body][router]'

        # ospfv2
        #   body
        #     router
        #       flags
        #       num_of_links
        for key in ['flags', 'num_of_links']:
            self.add_leaf(cmd=ShowIpOspfDatabaseRouterDetail,
                          src=rbody_src+'[{key}]'.format(key=key),
                          dest=rbody_dest+'[{key}]'.format(key=key),
                          vrf=vrf)

        # body
        #  router
        #    links
        #      link_id
        rbody_links_src = rbody_src + '[links][(?P<link>.*)]'
        rbody_links_dest = rbody_dest + '[links][(?P<link>.*)]'

        # body
        #  router
        #    links
        #      link_id
        #        link_id
        #        link_data
        #        type
        for key in ['link_id', 'link_data', 'type']:
            self.add_leaf(cmd=ShowIpOspfDatabaseRouterDetail,
                          src=rbody_links_src+'[{key}]'.format(key=key),
                          dest=rbody_links_dest+'[{key}]'.format(key=key),
                          vrf=vrf)

        # body
        #  router
        #    links
        #      link_id
        #        topologies
        #          mt_id
        rbody_links_topo_src = rbody_links_src + '[topologies][(?P<mt_id>.*)]'
        rbody_links_topo_dest = rbody_links_dest + '[topologies][(?P<mt_id>.*)]'

        # body
        #  router
        #    links
        #      link_id
        #        topologies
        #          mt_id
        #            topology - N/A
        #            mt_id
        #            metric
        for key in ['mt_id', 'metric']:
            self.add_leaf(cmd=ShowIpOspfDatabaseRouterDetail,
                          src=rbody_links_topo_src+'[{key}]'.format(key=key),
                          dest=rbody_links_topo_dest+'[{key}]'.format(key=key),
                          vrf=vrf)

        # ======================================================================
        #                       database network: body
        # ======================================================================

        # ospfv2
        #   body
        #     network
        nbody_src = db_src + '[ospfv2][body][network]'
        nbody_dest = db_dest + '[ospfv2][body][network]'

        # ospfv2
        #   body
        #     network
        #       network_mask
        #       attached_routers
        #         attr_router_name
        for key in ['network_mask', 'attached_routers']:
            self.add_leaf(cmd=ShowIpOspfDatabaseNetworkDetail,
                          src=nbody_src+'[{key}]'.format(key=key),
                          dest=nbody_dest+'[{key}]'.format(key=key),
                          vrf=vrf)

        # ======================================================================
        #                       database summary: body
        # ======================================================================

        # ospfv2
        #   body
        #     summary
        sbody_src = db_src + '[ospfv2][body][summary]'
        sbody_dest = db_dest + '[ospfv2][body][summary]'

        # ospfv2
        #   body
        #     summary
        #       network_mask
        self.add_leaf(cmd=ShowIpOspfDatabaseSummaryDetail,
                          src=sbody_src+'[network_mask]',
                          dest=sbody_dest+'[network_mask]',
                          vrf=vrf)

        # ospfv2
        #   body
        #     summary
        #       topologies
        sbody_topo_src = sbody_src + '[topologies][(?P<mt_id>.*)]'
        sbody_topo_dest = sbody_dest + '[topologies][(?P<mt_id>.*)]'

        # ospfv2
        #   body
        #     summary
        #       topologies
        #         mt_id
        #           topology - N/A
        #           mt_id
        #           metric
        for key in ['mt_id', 'metric']:
            self.add_leaf(cmd=ShowIpOspfDatabaseSummaryDetail,
                          src=sbody_topo_src+'[{key}]'.format(key=key),
                          dest=sbody_topo_dest+'[{key}]'.format(key=key),
                          vrf=vrf)

        # ======================================================================
        #                       database external: body
        # ======================================================================

        # ospfv2
        #   body
        #     external
        ebody_src = db_src + '[ospfv2][body][external]'
        ebody_dest = db_dest + '[ospfv2][body][external]'

        # ospfv2
        #   body
        #     external
        #       network_mask
        self.add_leaf(cmd=ShowIpOspfDatabaseExternalDetail,
                      src=ebody_src+'[network_mask]',
                      dest=ebody_dest+'[network_mask]',
                      vrf=vrf)

        # ospfv2
        #   body
        #     external
        #       topologies
        ebody_topo_src = ebody_src + '[topologies][(?P<mt_id>.*)]'
        ebody_topo_dest = ebody_dest + '[topologies][(?P<mt_id>.*)]'

        # ospfv2
        #   body
        #     external
        #       topologies
        #         mt_id
        #           topology - N/A
        #           mt_id
        #           flags
        #           metric
        #           forwarding_address
        #           external_route_tag
        for key in ['mt_id', 'flags', 'metric', 'forwarding_address',
                    'external_route_tag']:
            self.add_leaf(cmd=ShowIpOspfDatabaseExternalDetail,
                          src=ebody_topo_src+'[{key}]'.format(key=key),
                          dest=ebody_topo_dest+'[{key}]'.format(key=key),
                          vrf=vrf)

        # ======================================================================
        #                       database opaque-area: body
        # ======================================================================

        # ospfv2
        #   body
        #     opqaue
        obody_src = db_src + '[ospfv2][body][opaque]'
        obody_dest = db_dest + '[ospfv2][body][opaque]'

        # ospfv2
        #   body
        #     opqaue
        #       unknown_tlvs - N/A
        #         unknown_tlv - N/A
        #           type - N/A
        #           length - N/A
        #           value - N/A
        #       node_tag_tlvs - N/A
        #         node_tag_tlv - N/A
        #           node_tag - N/A
        #             tag - N/A
        #       router_address_tlv - N/A
        #         router_address - N/A
        #       link_tlvs
        #         index
        #           link_type
        #           link_id
        #           local_if_ipv4_addrs
        #             local_if_ipv4_addr: {}
        #           remote_if_ipv4_addrs
        #             remote_if_ipv4_addr: {}
        #           te_metric
        #           admin_group
        #           max_bandwidth
        #           max_reservable_bandwidth
        #           unreserved_bandwidths
        #             ub_key
        #               priority
        #               unreserved_bandwidth
        #           unknown_tlvs
        #             index
        #               type
        #               length
        #               value
        #         extended_prefix_tlvs - N/A
        #           extended_prefix_tlv - N/A
        #             route_type - N/A
        #             flags - N/A
        #             prefix - N/A
        #             unknown_tlvs - N/A
        #               unknonwn_tlv - N/A
        #                 type - N/A
        #                 length - N/A
        #                 value - N/A
        #         extended_link_tlvs - N/A
        #           extended_link_tlv - N/A
        #             link_id - N/A
        #             link_data - N/A
        #             type - N/A
        #             unknown_tlvs - N/A
        #               unknown_tlv - N/A
        #                 type - N/A
        #                 length - N/A
        #                 value - N/A
        self.add_leaf(cmd=ShowIpOspfDatabaseOpaqueAreaDetail,
                      src=obody_src+'[link_tlvs]',
                      dest=obody_dest+'[link_tlvs]',
                      vrf=vrf)

        # ======================================================================
        #                           virtual_links
        # ======================================================================

        # virtual_links
        #   vl_link_name
        vl_src = area_src + '[virtual_links][(?P<vlink>.*)]'
        vl_dest = area_dest + '[virtual_links][(?P<vlink>.*)]'

        # virtual_links
        #   vl_link_name
        #     name
        #     transit_area_id
        #     router_id
        #     hello_interval
        #     dead_interval
        #     retransmit_interval
        #     transmit_delay
        #     demand_circuit - N/A
        for key in ['name', 'transit_area_id', 'router_id', 'hello_interval', 
                    'dead_interval', 'retransmit_interval', 'transmit_delay']:
            self.add_leaf(cmd=ShowIpOspfVirtualLinks,
                          src=vl_src+'[{key}]'.format(key=key),
                          dest=vl_dest+'[{key}]'.format(key=key),
                          vrf=vrf)

        # virtual_links
        #   vl_link_name
        #     ttl_security - N/A
        #       hops - N/A        

        # virtual_links
        #   vl_link_name
        #     authentication
        #       auth_trailer_key_chain
        #         key_chain
        self.add_leaf(cmd=ShowIpOspfInterface,
                      src=vl_src+'[authentication][auth_trailer_key_chain][key_chain]',
                      dest=vl_dest+'[authentication][auth_trailer_key_chain][key_chain]',
                      vrf=vrf, interface=interface)

        # virtual_links
        #   vl_link_name
        #     authentication
        #       key
        #       crypto_algorithm
        for key in ['key', 'crypto_algorithm']:
            self.add_leaf(cmd=ShowIpOspfInterface,
                          src=vl_src+'[authentication][auth_trailer_key][{key}]'.format(key=key),
                          dest=vl_dest+'[authentication][auth_trailer_key][{key}]'.format(key=key),
                          vrf=vrf, interface=interface)

        # virtual_links
        #   vl_link_name
        #     cost
        #     state
        #     hello_timer
        #     wait_timer
        for key in ['cost', 'state', 'hello_timer', 'wait_timer']:
            self.add_leaf(cmd=ShowIpOspfVirtualLinks,
                          src=vl_src+'[{key}]'.format(key=key),
                          dest=vl_dest+'[{key}]'.format(key=key),
                          vrf=vrf)

        # virtual_links
        #   vl_link_name
        #     dr_router_id
        #     dr_ip_addr
        #     bdr_router_id
        #     bdr_ip_addr
        for key in ['dr_router_id', 'dr_ip_addr', 'bdr_router_id', 
                    'bdr_ip_addr']:
            self.add_leaf(cmd=ShowIpOspfInterface,
                          src=vl_src+'[{key}]'.format(key=key),
                          dest=vl_dest+'[{key}]'.format(key=key),
                          vrf=vrf, interface=interface)

        # virtual_links
        #   vl_link_name
        #     statistics - N/A
        #       link_scope_lsa_count
        #       link_scope_lsa_cksum_sum
        #       if_event_count - N/A
        #       database - N/A
        #         link_scope_lsa_type - N/A
        #         lsa_type - N/A
        #         lsa_count - N/A
        #         lsa_chksum_sum - N/A
        for key in ['link_scope_lsa_count', 'link_scope_lsa_cksum_sum']:
            self.add_leaf(cmd=ShowIpOspfInterface,
                          src=vl_src+'[statistics][{key}]'.format(key=key),
                          dest=vl_dest+'[statistics][{key}]'.format(key=key),
                          vrf=vrf, interface=interface)

        # virtual_links
        #   vl_link_name
        #     neighbors
        #       neighbor
        #         neighbor_router_id
        #         address
        #         dr_router_id - N/A
        #         dr_ip_addr
        #         bdr_router_id - N/A
        #         bdr_ip_addr
        #         state
        #         dead_timer
        for key in ['neighbor_router_id', 'address', 'dr_ip_addr', 'bdr_ip_addr',
                    'state', 'dead_timer']:
            self.add_leaf(cmd=ShowIpOspfNeighborDetail,
                          src=vl_src+'[neighbors][(?P<neighbor>(.*))][{key}]'.format(key=key),
                          dest=vl_dest+'[neighbors][(?P<neighbor>(.*))][{key}]'.format(key=key),
                          vrf=vrf, neighbor=neighbor)

        # virtual_links
        #   vl_link_name
        #     neighbors
        #       statistics
        #         nbr_event_count
        #         nbr_retrans_qlen - N/A
        for key in ['nbr_event_count']:
            self.add_leaf(cmd=ShowIpOspfNeighborDetail,
                          src=vl_src+'[neighbors][(?P<neighbor>(.*))][statistics][{key}]'.format(key=key),
                          dest=vl_dest+'[neighbors][(?P<neighbor>(.*))][statistics][{key}]'.format(key=key),
                          vrf=vrf, neighbor=neighbor)

        # ======================================================================
        #                           sham_links
        # ======================================================================

        # sham_links
        #   sl_link_name
        sl_src = area_src + '[sham_links][(?P<slink>.*)]'
        sl_dest = area_dest + '[sham_links][(?P<slink>.*)]'

        # sham_links
        #   sl_link_name
        #     name
        #     local_id
        #     remote_id
        #     transit_area_id
        #     hello_interval
        #     dead_interval
        #     retransmit_interval
        #     transmit_delay
        #     demand_circuit - N/A
        for key in ['name', 'local_id', 'remote_id', 'transit_area_id',
                    'hello_interval', 'dead_interval', 'retransmit_interval',
                    'transmit_delay']:
            self.add_leaf(cmd=ShowIpOspfShamLinks,
                          src=sl_src+'[{key}]'.format(key=key),
                          dest=sl_dest+'[{key}]'.format(key=key),
                          vrf=vrf)

        # sham_links
        #   sl_link_name
        #     ttl_security - N/A
        #       hops - N/A        

        # sham_links
        #   sl_link_name
        #     authentication
        #       auth_trailer_key_chain
        #         key_chain
        self.add_leaf(cmd=ShowIpOspfInterface,
                      src=sl_src+'[authentication][auth_trailer_key_chain][key_chain]',
                      dest=sl_dest+'[authentication][auth_trailer_key_chain][key_chain]',
                      vrf=vrf, interface=interface)
        
        # sham_links
        #   sl_link_name
        #     authentication
        #       key
        #       crypto_algorithm
        for key in ['key', 'crypto_algorithm']:
            self.add_leaf(cmd=ShowIpOspfInterface,
                          src=sl_src+'[authentication][auth_trailer_key][{key}]'.format(key=key),
                          dest=sl_dest+'[authentication][auth_trailer_key][{key}]'.format(key=key),
                          vrf=vrf, interface=interface)

        # sham_links
        #   sl_link_name
        #     cost
        #     prefix_suppression - N/A
        #     state
        #     hello_timer
        #     wait_timer
        for key in ['cost', 'state', 'hello_timer', 'wait_timer']:
            self.add_leaf(cmd=ShowIpOspfShamLinks,
                          src=sl_src+'[{key}]'.format(key=key),
                          dest=sl_dest+'[{key}]'.format(key=key),
                          vrf=vrf)

        # sham_links
        #   sl_link_name
        #     dr_router_id
        #     dr_ip_addr
        #     bdr_router_id
        #     bdr_ip_addr
        for key in ['dr_router_id', 'dr_ip_addr', 'bdr_router_id', 'bdr_ip_addr']:
            self.add_leaf(cmd=ShowIpOspfInterface,
                          src=sl_src+'[{key}]'.format(key=key),
                          dest=sl_dest+'[{key}]'.format(key=key),
                          vrf=vrf, interface=interface)

        # sham_links
        #   sl_link_name
        #     statistics
        #       link_scope_lsa_count
        #       link_scope_lsa_cksum_sum
        #       if_event_count - N/A
        #       database - N/A
        #         link_scope_lsa_type - N/A
        #         lsa_type - N/A
        #         lsa_count - N/A
        #         lsa_chksum_sum - N/A
        for key in ['link_scope_lsa_count', 'link_scope_lsa_cksum_sum']:
            self.add_leaf(cmd=ShowIpOspfInterface,
                          src=sl_src+'[statistics][{key}]'.format(key=key),
                          dest=sl_dest+'[statistics][{key}]'.format(key=key),
                          vrf=vrf, interface=interface)

        # sham_links
        #   sl_link_name
        #     neighbors
        #       neighbor
        #         neighbor_router_id
        #         address
        #         dr_router_id - N/A
        #         dr_ip_addr
        #         bdr_router_id - N/A
        #         bdr_ip_addr
        #         state
        #         dead_timer
        for key in ['neighbor_router_id', 'address', 'dr_ip_addr', 'bdr_ip_addr',
                    'state', 'dead_timer']:
            self.add_leaf(cmd=ShowIpOspfNeighborDetail,
                          src=sl_src+'[neighbors][(?P<neighbor>(.*))][{key}]'.format(key=key),
                          dest=sl_dest+'[neighbors][(?P<neighbor>(.*))][{key}]'.format(key=key),
                          vrf=vrf, neighbor=neighbor)

        # sham_links
        #   sl_link_name
        #     neighbors
        #       statistics
        #         nbr_event_count
        #         nbr_retrans_qlen - N/A
        for key in ['nbr_event_count']:
            self.add_leaf(cmd=ShowIpOspfNeighborDetail,
                          src=sl_src+'[neighbors][(?P<neighbor>(.*))][statistics][{key}]'.format(key=key),
                          dest=sl_dest+'[neighbors][(?P<neighbor>(.*))][statistics][{key}]'.format(key=key),
                          vrf=vrf, neighbor=neighbor)

        # ======================================================================
        #                           interfaces
        # ======================================================================
        
        # interfaces
        #   interface
        if interface:
            intf_src = area_src + '[interfaces][{interface}]'.format(interface=interface)
            intf_dest = area_dest + '[interfaces][{interface}]'.format(interface=interface)
        else:
            intf_src = area_src + '[interfaces][(?P<intf>.*)]'
            intf_dest = area_dest + '[interfaces][(?P<intf>.*)]'

        # interfaces
        #   interface
        #     name
        #     interface_type
        #     passive
        #     demand_circuit - N.A
        #     priority
        #     transmit_delay
        for key in ['name', 'interface_type', 'passive', 'priority', 'transmit_delay']:
            self.add_leaf(cmd=ShowIpOspfInterface,
                          src=intf_src+'[{key}]'.format(key=key),
                          dest=intf_dest+'[{key}]'.format(key=key),
                          vrf=vrf, interface=interface)
        
        # interfaces
        #   interface
        #     static_neigbhors - N/A
        #       if_static_neighbor - N/A
        #         identifier - N/A
        #         cost - N/A
        #         poll_interval - N/A
        #         priority - N/A

        # interfaces
        #   interface
        #     bfd
        #       enable
        #       min_interval
        #       interval - N/A
        #       multiplier - N/A
        for key in ['enable', 'min_interval']:
            self.add_leaf(cmd=ShowIpOspfInterface,
                          src=intf_src+'[bfd][{key}]'.format(key=key),
                          dest=intf_dest+'[bfd][{key}]'.format(key=key),
                          vrf=vrf, interface=interface)

        # interfaces
        #   interface
        #     hello_interval
        #     dead_interval
        #     retransmit_interval
        #     lls - N/A
        #     ttl_security - N/A
        #       enable - N/A
        #       hops - N/A
        #     enable
        for key in ['hello_interval', 'dead_interval', 'retransmit_interval', 
                    'enable']:
            self.add_leaf(cmd=ShowIpOspfInterface,
                          src=intf_src+'[{key}]'.format(key=key),
                          dest=intf_dest+'[{key}]'.format(key=key),
                          vrf=vrf, interface=interface)

        # interfaces
        #   interface
        #     authentication
        #       auth_trailer_key_chain
        #         key_chain
        self.add_leaf(cmd=ShowIpOspfInterface,
                      src=intf_src+'[authentication][auth_trailer_key_chain][key_chain]',
                      dest=intf_dest+'[authentication][auth_trailer_key_chain][key_chain]',
                      vrf=vrf, interface=interface)
        
        # interfaces
        #   interface
        #     authentication
        #       key
        #       crypto_algorithm
        for key in ['key', 'crypto_algorithm']:
            self.add_leaf(cmd=ShowIpOspfInterface,
                          src=intf_src+'[authentication][auth_trailer_key][{key}]'.format(key=key),
                          dest=intf_dest+'[authentication][auth_trailer_key][{key}]'.format(key=key),
                          vrf=vrf, interface=interface)

        # interfaces
        #   interface
        #     cost
        #     mtu_ignore - N/A
        #     prefix_suppression - N/A
        #     state
        #     hello_timer
        #     wait_timer
        #     dr_router_id
        #     dr_ip_addr
        #     bdr_router_id
        #     bdr_ip_addr
        for key in ['enable', 'cost', 'state', 'hello_timer', 'wait_timer',
                    'dr_router_id', 'dr_ip_addr', 'bdr_router_id', 'bdr_ip_addr']:
            self.add_leaf(cmd=ShowIpOspfInterface,
                          src=intf_src+'[{key}]'.format(key=key),
                          dest=intf_dest+'[{key}]'.format(key=key),
                          vrf=vrf, interface=interface)

        # interfaces
        #   interface
        #     statistics - N/A
        #       link_scope_lsa_count
        #       link_scope_lsa_cksum_sum
        #       if_event_count - N/A
        #       database - N/A
        #         link_scope_lsa_type - N/A
        #         lsa_type - N/A
        #         lsa_count - N/A
        #         lsa_chksum_sum - N/A
        for key in ['link_scope_lsa_count', 'link_scope_lsa_cksum_sum']:
            self.add_leaf(cmd=ShowIpOspfInterface,
                          src=intf_src+'[statistics][{key}]'.format(key=key),
                          dest=intf_dest+'[statistics][{key}]'.format(key=key),
                          vrf=vrf, interface=interface)

        # interfaces
        #   interface
        #     neighbors
        #       neighbor
        #         neighbor_router_id
        #         address
        #         dr_router_id - N/A
        #         dr_ip_addr
        #         bdr_router_id - N/A
        #         bdr_ip_addr
        #         state
        #         dead_timer
        #         last_state_change
        for key in ['neighbor_router_id', 'address', 'dr_ip_addr', 'bdr_ip_addr',
                    'state', 'dead_timer','last_state_change']:
            self.add_leaf(cmd=ShowIpOspfNeighborDetail,
                          src=intf_src+'[neighbors][(?P<neighbor>(.*))][{key}]'.format(key=key),
                          dest=intf_dest+'[neighbors][(?P<neighbor>(.*))][{key}]'.format(key=key),
                          vrf=vrf, neighbor=neighbor)

        # interfaces
        #   interface
        #     neighbors
        #       statistics
        #         nbr_event_count
        #         nbr_retrans_qlen - N/A
        for key in ['nbr_event_count']:
            self.add_leaf(cmd=ShowIpOspfNeighborDetail,
                          src=intf_src+'[neighbors][(?P<neighbor>(.*))][statistics][{key}]'.format(key=key),
                          dest=intf_dest+'[neighbors][(?P<neighbor>(.*))][statistics][{key}]'.format(key=key),
                          vrf=vrf, neighbor=neighbor)

        # ======================================================================
        #                          BUILD STRUCTURE
        # ======================================================================

        # Make final Ops structure
        self.make(final_call=True)
