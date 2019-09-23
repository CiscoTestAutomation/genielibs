''' 
OSPF Genie Ops Object for IOSXE - CLI.
'''
# super class
from genie.libs.ops.ospf.ospf import Ospf as SuperOspf

# iosxe show_ospf
from genie.libs.parser.iosxe.show_protocols import ShowIpProtocols


class Ospf(SuperOspf):
    '''Ospf Ops Object'''

    def learn(self, vrf='', interface='', neighbor=''):
        '''Learn Ospf object'''

        ########################################################################
        #                               info
        ########################################################################

        # vrf
        #   vrf_name
        #     address_family
        #       af_name
        #         instance
        #           instance_name
        if vrf:
            info_src = '[vrf][{vrf}][address_family][(?P<af>.*)][instance][(' \
                       '?P<instance>.*)]'.format(vrf=vrf)

        else:
            info_src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][instance][(?P<instance>.*)]'

        info_dest = 'info' + info_src

        # router_id
        self.add_leaf(cmd='show ip ospf',
                      src=info_src+'[router_id]',
                      dest=info_dest+'[router_id]')
        
        # maximum_interfaces - N/A
        
        # preference
        #   single_value
        #     all
        self.add_leaf(cmd=ShowIpProtocols,
                      src='[protocols][ospf]'+info_src+'[preference][single_value][all]',
                      dest=info_dest+'[preference][single_value][all]', vrf=vrf)

        # preference
        #   multi_values 
        #     granularity
        #       coarse - N/A
        #       detail
        #         intra_area
        #         inter_area
        for key in ['intra_area', 'inter_area']:
            self.add_leaf(cmd=ShowIpProtocols,
                          src='[protocols][ospf]'+info_src+'[preference][multi_values][granularity][detail][{key}]'.format(key=key),
                          dest=info_dest+'[preference][multi_values][granularity][detail][{key}]'.format(key=key), vrf=vrf)

        # preference
        #   multi_values 
        #     external
        self.add_leaf(cmd=ShowIpProtocols,
                      src='[protocols][ospf]'+info_src+'[preference][multi_values][external]',
                      dest=info_dest+'[preference][multi_values][external]', vrf=vrf)

        # redistribution
        #   max_prefix
        #     num_of_prefix
        #     prefix_thld
        #     warn_only
        for key in ['num_of_prefix', 'prefix_thld', 'warn_only']:
            self.add_leaf(cmd='show ip ospf',
                          src=info_src+'[redistribution][max_prefix][{key}]'.format(key=key),
                          dest=info_dest+'[redistribution][max_prefix][{key}]'.format(key=key))

        # redistribution
        #   bgp
        #     bgp_id
        #     metric
        #     metric_type - N/A
        #     nssa_only - N/A
        #     route_map - N/A
        #     subnets - N/A
        #     tag - N/A
        #     lsa_type_summary - N/A
        #     preserve_med - N/A
        for key in ['bgp_id', 'metric']:
            self.add_leaf(cmd='show ip ospf',
                          src=info_src+'[redistribution][bgp][{key}]'.format(key=key),
                          dest=info_dest+'[redistribution][bgp][{key}]'.format(key=key))

        # redistribution
        #   connected
        #     enabled
        #     metric
        #     route_policy - N/A
        for key in ['enabled', 'metric']:
            self.add_leaf(cmd='show ip ospf',
                          src=info_src+'[redistribution][connected][{key}]'.format(key=key),
                          dest=info_dest+'[redistribution][connected][{key}]'.format(key=key))
        
        # redistribution
        #   static
        #     enabled
        #     metric
        #     route_policy - N/A
        for key in ['enabled', 'metric']:
            self.add_leaf(cmd='show ip ospf',
                          src=info_src+'[redistribution][static][{key}]'.format(key=key),
                          dest=info_dest+'[redistribution][static][{key}]'.format(key=key))

        # redistribution
        #   isis
        #     isis_pid
        #     metric
        #     route_policy - N/A
        for key in ['isis_pid', 'metric']:
            self.add_leaf(cmd='show ip ospf',
                          src=info_src+'[redistribution][isis][{key}]'.format(key=key),
                          dest=info_dest+'[redistribution][isis][{key}]'.format(key=key))

        # nsr
        #   enable
        self.add_leaf(cmd='show ip ospf',
                      src=info_src+'[nsr][enable]',
                      dest=info_dest+'[nsr][enable]')

        # graceful_restart
        #   gr_type
        #     enable
        #     type
        #     helper_enable - N/A
        #     restart_interval - N/A
        #     helper_strict_lsa_checking - N/A
        for key in ['enable', 'type']:
            self.add_leaf(cmd='show ip ospf',
                          src=info_src+'[graceful_restart][(?P<type>(.*))][{key}]'.format(key=key),
                          dest=info_dest+'[graceful_restart][(?P<type>(.*))][{key}]'.format(key=key))

        # enable - N/A

        # auto_cost
        #   enable
        #   reference_bandwidth
        for key in ['enable', 'bandwidth']:
            self.add_leaf(cmd='show ip ospf',
                          src=info_src+'[auto_cost][{key}]'.format(key=key),
                          dest=info_dest+'[auto_cost][{key}]'.format(key=key))

        # spf_control
        #   paths
        self.add_leaf(cmd=ShowIpProtocols,
                      src='[protocols][ospf]'+info_src+'[spf_control][paths]',
                      dest=info_dest+'[spf_control][paths]', vrf=vrf)

        # spf_control
        #   throttle
        #     spf / lsa
        #       start
        #       hold
        #       maximum
        for key1 in ['spf', 'lsa']:
            for key2 in ['start', 'hold', 'maximum']:
                self.add_leaf(cmd='show ip ospf',
                              src=info_src+'[spf_control][throttle][{key1}][{key2}]'.format(key1=key1,key2=key2),
                              dest=info_dest+'[spf_control][throttle][{key1}][{key2}]'.format(key1=key1,key2=key2))

        # database_control
        #   max_lsa
        self.add_leaf(cmd='show ip ospf',
                      src=info_src+'[database_control][max_lsa]',
                      dest=info_dest+'[database_control][max_lsa]')

        # stub_router
        #   always
        #     always
        #     include_stub
        #     summary_lsa
        #     external_lsa
        for key in ['always', 'include_stub', 'summary_lsa', 'external_lsa']:
            self.add_leaf(cmd='show ip ospf',
                          src=info_src+'[stub_router][always][{key}]'.format(key=key),
                          dest=info_dest+'[stub_router][always][{key}]'.format(key=key))

        # stub_router
        #   on_startup
        #     on_startup
        #     include_stub
        #     summary_lsa
        #     external_lsa
        for key in ['on_startup', 'include_stub', 'summary_lsa', 'external_lsa']:
            self.add_leaf(cmd='show ip ospf',
                          src=info_src+'[stub_router][on_startup][{key}]'.format(key=key),
                          dest=info_dest+'[stub_router][on_startup][{key}]'.format(key=key))

        # stub_router
        #   on_switchover
        #     on_switchover
        #     include_stub
        #     summary_lsa
        #     external_lsa
        for key in ['on_switchover', 'include_stub', 'summary_lsa', 'external_lsa']:
            self.add_leaf(cmd='show ip ospf',
                          src=info_src+'[stub_router][on_switchover][{key}]'.format(key=key),
                          dest=info_dest+'[stub_router][on_switchover][{key}]'.format(key=key))

        # default_originate - N/A
        #   default_originate
        #   always

        # mpls
        #   te - N/A
        #     router_id - N/A

        # mpls
        #   ldp
        #     autoconfig
        #     autoconfig_area_id
        #     igp_sync
        for key in ['autoconfig', 'autoconfig_area_id', 'igp_sync']:
            self.add_leaf(cmd='show ip ospf mpls ldp interface',
                          src=info_src+'[mpls][ldp][{key}]'.format(key=key),
                          dest=info_dest+'[mpls][ldp][{key}]'.format(key=key),
                          interface=interface)

        # local_rib - N/A
        #   prefix
        #     prefix
        #     next_hops
        #       next_hop
        #         outgoing_interface
        #         next_hop
        #     metric
        #     route_type
        #     route_tag

        # bfd
        #   enable
        #   strict_mode
        for key in ['enable', 'strict_mode']:
            self.add_leaf(cmd='show ip ospf',
                          src=info_src+'[bfd][{key}]'.format(key=key),
                          dest=info_dest+'[bfd][{key}]'.format(key=key))

        # log_adjacency_changes - N/A
        #   enable
        #   detail

        # adjacency_stagger
        #   initial_number
        #   maximum_number
        #   no_initial_limit
        #   disable - N/A
        for key in ['initial_number', 'maximum_number', 'no_initial_limit']:
            self.add_leaf(cmd='show ip ospf',
                          src=info_src+'[adjacency_stagger][{key}]'.format(key=key),
                          dest=info_dest+'[adjacency_stagger][{key}]'.format(key=key))

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
        for key in ['area_id', 'area_type', 'summary', 'default_cost']:
            self.add_leaf(cmd='show ip ospf',
                          src=area_src+'[{key}]'.format(key=key),
                          dest=area_dest+'[{key}]'.format(key=key))

        # bfd - N/A
        #   enable - N/A
        #   minimum_interval - N/A
        #   multiplier - N/A

        # enabled_networks - N/A
        #   en_network - N/A
        #     network - N/A
        #     wildcard - N/A

        # mpls
        #   te
        #     enable
        self.add_leaf(cmd='show ip ospf mpls traffic-eng link',
                      src=area_src+'[mpls][te][enable]',
                      dest=area_dest+'[mpls][te][enable]')

        # mpls
        #   ldp - N/A
        #     auto_config - N/A
        #     sync - N/A
        #     sync_igp_shortcuts - N/A

        # ranges
        #   area_range_prefix
        #     prefix
        #     advertise
        #     cost
        for key in ['prefix', 'advertise', 'cost']:
            self.add_leaf(cmd='show ip ospf',
                          src=area_src+'[ranges][(?P<prefix>.*)][{key}]'.format(key=key),
                          dest=area_dest+'[ranges][(?P<prefix>.*)][{key}]'.format(key=key))

        # statistics
        #   spf_runs_count
        #   abr_count - N/A
        #   asbr_count - N/A
        #   as_nssa_translator_event_count - N/A
        #   area_scope_lsa_count
        #   area_scope_lsa_cksum_sum
        for key in ['spf_runs_count', 'area_scope_lsa_count',
                    'area_scope_lsa_cksum_sum']:
            self.add_leaf(cmd='show ip ospf',
                          src=area_src+'[statistics][{key}]'.format(key=key),
                          dest=area_dest+'[statistics][{key}]'.format(key=key))

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
        for cmd in ['show ip ospf database router',
                    'show ip ospf database network',
                    'show ip ospf database external',
                    'show ip ospf database summary',
                    'show ip ospf database opaque-area']:

            # database
            #   lsa_types
            #     lsa_type_name
            #       lsas
            #         lsa_name
            self.add_leaf(cmd=cmd,
                          src=area_src+'[database][lsa_types][(?P<lsa_type>.*)][lsa_type]',
                          dest=area_dest+'[database][lsa_types][(?P<lsa_type>.*)][lsa_type]')

            # lsa_id
            self.add_leaf(cmd=cmd,
                          src=db_src+'[lsa_id]',
                          dest=db_dest+'[lsa_id]')

            # adv_router
            self.add_leaf(cmd=cmd,
                          src=db_src+'[adv_router]',
                          dest=db_dest+'[adv_router]')
            
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
                              dest=db_dest+'[ospfv2][header][{key}]'.format(key=key))

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
            self.add_leaf(cmd='show ip ospf database router',
                          src=rbody_src+'[{key}]'.format(key=key),
                          dest=rbody_dest+'[{key}]'.format(key=key))

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
            self.add_leaf(cmd='show ip ospf database router',
                          src=rbody_links_src+'[{key}]'.format(key=key),
                          dest=rbody_links_dest+'[{key}]'.format(key=key))

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
            self.add_leaf(cmd='show ip ospf database router',
                          src=rbody_links_topo_src+'[{key}]'.format(key=key),
                          dest=rbody_links_topo_dest+'[{key}]'.format(key=key))

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
            self.add_leaf(cmd='show ip ospf database network',
                          src=nbody_src+'[{key}]'.format(key=key),
                          dest=nbody_dest+'[{key}]'.format(key=key))

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
        self.add_leaf(cmd='show ip ospf database summary',
                          src=sbody_src+'[network_mask]',
                          dest=sbody_dest+'[network_mask]')

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
            self.add_leaf(cmd='show ip ospf database summary',
                          src=sbody_topo_src+'[{key}]'.format(key=key),
                          dest=sbody_topo_dest+'[{key}]'.format(key=key))

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
        self.add_leaf(cmd='show ip ospf database external',
                      src=ebody_src+'[network_mask]',
                      dest=ebody_dest+'[network_mask]')

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
            self.add_leaf(cmd='show ip ospf database external',
                          src=ebody_topo_src+'[{key}]'.format(key=key),
                          dest=ebody_topo_dest+'[{key}]'.format(key=key))

        # ======================================================================
        #                     database opaque-area: body
        # ======================================================================

        # ospfv2
        #   body
        #     opaque
        obody_src = db_src + '[ospfv2][body][opaque]'
        obody_dest = db_dest + '[ospfv2][body][opaque]'

        # ospfv2
        #   body
        #     opaque
        #       unknown_tlvs - N/A
        #           unknown_tls - N/A
        #           type -N/A
        #           length -N/A
        #           value - N/A
        #       node_tag_tlvs - N/A
        #           node_tag_tlv - N/A
        #               node_tag - N/A
        #                   tag - N/A
        #       router_address_tlv -N/A
        #           router_address - N/A
        #       link_tlvs
        #         index
        #           link_type
        #           link_id
        #           link_name
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
        for key in ['link_type', 'link_id', 'link_name', 'local_if_ipv4_addrs', 
                    'remote_if_ipv4_addrs', 'te_metric', 'admin_group', 
                    'max_bandwidth', 'max_reservable_bandwidth',
                    'unreserved_bandwidths', 'unknown_tlvs']:
            self.add_leaf(cmd='show ip ospf database opaque-area',
                          src=obody_src+'[link_tlvs][(?P<index>(.*))][{key}]'.format(key=key),
                          dest=obody_dest+'[link_tlvs][(?P<index>(.*))][{key}]'.format(key=key))

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
        #     demand_circuit
        for key in ['name', 'transit_area_id', 'router_id', 'hello_interval', 
                    'dead_interval', 'retransmit_interval', 'transmit_delay',
                    'demand_circuit']:
            self.add_leaf(cmd='show ip ospf virtual-links',
                          src=vl_src+'[{key}]'.format(key=key),
                          dest=vl_dest+'[{key}]'.format(key=key))

        # virtual_links
        #   vl_link_name
        #     ttl_security
        #       enable
        #       hops
        for key in ['enable', 'hops']:
            self.add_leaf(cmd='show ip ospf virtual-links',
                          src=vl_src+'[ttl_security][{key}]'.format(key=key),
                          dest=vl_dest+'[ttl_security][{key}]'.format(key=key))

        # virtual_links
        #   vl_link_name
        #     authentication
        #       auth_trailer_key_chain - N/A
        #         key_chain - N/A
        #       auth_trailer_key
        #         key - N/A
        #         crypto_algorithm
        self.add_leaf(cmd='show ip ospf interface {interface}'.format(interface=interface),
                      src=vl_src+'[authentication][auth_trailer_key][crypto_algorithm]',
                      dest=vl_dest+'[authentication][auth_trailer_key][crypto_algorithm]',
                      interface=interface)
        # virtual_links
        #   vl_link_name
        #     cost
        #     state
        #     hello_timer
        #     wait_timer
        for key in ['cost', 'state', 'hello_timer', 'wait_timer']:
            self.add_leaf(cmd='show ip ospf virtual-links',
                          src=vl_src+'[{key}]'.format(key=key),
                          dest=vl_dest+'[{key}]'.format(key=key))

        # virtual_links
        #   vl_link_name
        #     dr_router_id
        #     dr_ip_addr
        #     bdr_router_id
        #     bdr_ip_addr
        for key in ['dr_router_id', 'dr_ip_addr', 'bdr_router_id', 
                    'bdr_ip_addr']:
            self.add_leaf(cmd='show ip ospf interface {interface}'.format(interface=interface),
                          src=vl_src+'[{key}]'.format(key=key),
                          dest=vl_dest+'[{key}]'.format(key=key),
                          interface=interface)

        # virtual_links
        #   vl_link_name
        #     statistics - N/A
        #       if_event_count - N/A
        #       link_scope_lsa_count - N/A
        #       link_scope_lsa_cksum_sum - N/A
        #       database - N/A
        #         link_scope_lsa_type - N/A
        #         lsa_type - N/A
        #         lsa_count - N/A
        #         lsa_chksum_sum - N/A

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
            self.add_leaf(cmd='show ip ospf neighbor detail',
                          src=vl_src+'[neighbors][(?P<neighbor>(.*))][{key}]'.format(key=key),
                          dest=vl_dest+'[neighbors][(?P<neighbor>(.*))][{key}]'.format(key=key),
                          neighbor=neighbor)

        # virtual_links
        #   vl_link_name
        #     neighbors
        #       statistics
        #         nbr_event_count
        #         nbr_retrans_qlen
        for key in ['nbr_event_count', 'nbr_retrans_qlen']:
            self.add_leaf(cmd='show ip ospf neighbor detail',
                          src=vl_src+'[neighbors][(?P<neighbor>(.*))][statistics][{key}]'.format(key=key),
                          dest=vl_dest+'[neighbors][(?P<neighbor>(.*))][statistics][{key}]'.format(key=key),
                          neighbor=neighbor)

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
        #     demand_circuit
        for key in ['name', 'local_id', 'remote_id', 'transit_area_id', 
                    'hello_interval', 'dead_interval', 'retransmit_interval',
                    'transmit_delay', 'demand_circuit']:
            self.add_leaf(cmd='show ip ospf sham-links',
                          src=sl_src+'[{key}]'.format(key=key),
                          dest=sl_dest+'[{key}]'.format(key=key))

        # sham_links
        #   sl_link_name
        #     ttl_security
        #       enable
        #       hops
        for key in ['enable', 'hops']:
            self.add_leaf(cmd='show ip ospf sham-links',
                          src=sl_src+'[ttl_security][{key}]'.format(key=key),
                          dest=sl_dest+'[ttl_security][{key}]'.format(key=key))

        # sham_links
        #   sl_link_name
        #     authentication
        #       auth_trailer_key_chain - N/A
        #         key_chain - N/A
        #       auth_trailer_key
        #         key - N/A
        #         crypto_algorithm
        self.add_leaf(cmd='show ip ospf interface {interface}'.format(interface=interface),
                      src=sl_src+'[authentication][auth_trailer_key][crypto_algorithm]',
                      dest=sl_dest+'[authentication][auth_trailer_key][crypto_algorithm]',
                      interface=interface)
        
        # sham_links
        #   sl_link_name
        #     cost
        #     prefix_suppression - N/A
        #     state
        #     hello_timer
        #     wait_timer
        for key in ['cost', 'state', 'hello_timer', 'wait_timer']:
            self.add_leaf(cmd='show ip ospf sham-links',
                          src=sl_src+'[{key}]'.format(key=key),
                          dest=sl_dest+'[{key}]'.format(key=key))

        # sham_links
        #   sl_link_name
        #     dr_router_id
        #     dr_ip_addr
        #     bdr_router_id
        #     bdr_ip_addr
        for key in ['dr_router_id', 'dr_ip_addr', 'bdr_router_id', 'bdr_ip_addr']:
            self.add_leaf(cmd='show ip ospf interface {interface}'.format(interface=interface),
                          src=sl_src+'[{key}]'.format(key=key),
                          dest=sl_dest+'[{key}]'.format(key=key),
                          interface=interface)

        # sham_links
        #   sl_link_name
        #     statistics - N/A
        #       if_event_count - N/A
        #       link_scope_lsa_count - N/A
        #       link_scope_lsa_cksum_sum - N/A
        #       database - N/A
        #         link_scope_lsa_type - N/A
        #         lsa_type - N/A
        #         lsa_count - N/A
        #         lsa_chksum_sum - N/A

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
            self.add_leaf(cmd='show ip ospf neighbor detail',
                          src=sl_src+'[neighbors][(?P<neighbor>(.*))][{key}]'.format(key=key),
                          dest=sl_dest+'[neighbors][(?P<neighbor>(.*))][{key}]'.format(key=key),
                          neighbor=neighbor)

        # sham_links
        #   sl_link_name
        #     neighbors
        #       statistics
        #         nbr_event_count
        #         nbr_retrans_qlen
        for key in ['nbr_event_count', 'nbr_retrans_qlen']:
            self.add_leaf(cmd='show ip ospf neighbor detail',
                          src=sl_src+'[neighbors][(?P<neighbor>(.*))][statistics][{key}]'.format(key=key),
                          dest=sl_dest+'[neighbors][(?P<neighbor>(.*))][statistics][{key}]'.format(key=key),
                          neighbor=neighbor)

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
        #     demand_circuit
        #     priority
        #     transmit_delay
        for key in ['name', 'interface_type', 'passive', 'demand_circuit',
                    'priority', 'transmit_delay']:
            self.add_leaf(cmd='show ip ospf interface {interface}'.format(interface=interface),
                          src=intf_src+'[{key}]'.format(key=key),
                          dest=intf_dest+'[{key}]'.format(key=key),
                          interface=interface)
        
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
        #       interval
        #       min_interval
        #       multiplier
        for key in ['enable', 'interval', 'min_interval', 'multiplier']:
            self.add_leaf(cmd='show ip ospf interface {interface}'.format(interface=interface),
                          src=intf_src+'[bfd][{key}]'.format(key=key),
                          dest=intf_dest+'[bfd][{key}]'.format(key=key),
                          interface=interface)

        # interfaces
        #   interface
        #     hello_interval
        #     dead_interval
        #     retransmit_interval
        #     lls
        #     enable - N/A
        for key in ['hello_interval', 'dead_interval', 'retransmit_interval', 
                    'lls']:
            self.add_leaf(cmd='show ip ospf interface {interface}'.format(interface=interface),
                          src=intf_src+'[{key}]'.format(key=key),
                          dest=intf_dest+'[{key}]'.format(key=key),
                          interface=interface)

        # interfaces
        #   interface
        #     ttl_security
        #       enable
        #       hops
        for key in ['enable', 'hops']:
            self.add_leaf(cmd='show ip ospf interface {interface}'.format(interface=interface),
                          src=intf_src+'[ttl_security][{key}]'.format(key=key),
                          dest=intf_dest+'[ttl_security][{key}]'.format(key=key),
                          interface=interface)

        # interfaces
        #   interface
        #     authentication
        #       auth_trailer_key_chain - N/A
        #         key_chain - N/A
        #     auth_trailer_key
        #       key - N/A
        #       crypto_algorithm
        self.add_leaf(cmd='show ip ospf interface {interface}'.format(interface=interface),
                      src=intf_src+'[authentication][auth_trailer_key][crypto_algorithm]',
                      dest=intf_dest+'[authentication][auth_trailer_key][crypto_algorithm]',
                      interface=interface)

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
            self.add_leaf(cmd='show ip ospf interface {interface}'.format(interface=interface),
                          src=intf_src+'[{key}]'.format(key=key),
                          dest=intf_dest+'[{key}]'.format(key=key),
                          interface=interface)

        # interfaces
        #   interface
        #     statistics - N/A
        #       if_event_count - N/A
        #       link_scope_lsa_count - N/A
        #       link_scope_lsa_cksum_sum - N/A
        #       database - N/A
        #         link_scope_lsa_type - N/A
        #         lsa_type - N/A
        #         lsa_count - N/A
        #         lsa_chksum_sum - N/A

        # interfaces
        #   interface
        #     neighbors
        #       neighbor
        #         neighbor_router_id
        #         address
        #         dr_router_id
        #         dr_ip_addr
        #         bdr_router_id
        #         bdr_ip_addr
        #         state
        #         dead_timer
        for key in ['neighbor_router_id', 'address', 'dr_router_id', 
                    'dr_ip_addr', 'bdr_ip_addr', 'bdr_router_id', 'state',
                    'dead_timer']:
            self.add_leaf(cmd='show ip ospf neighbor detail',
                          src=intf_src+'[neighbors][(?P<neighbor>(.*))][{key}]'.format(key=key),
                          dest=intf_dest+'[neighbors][(?P<neighbor>(.*))][{key}]'.format(key=key),
                          neighbor=neighbor)

        # interfaces
        #   interface
        #     neighbors
        #       statistics
        #         nbr_event_count
        #         nbr_retrans_qlen
        for key in ['nbr_event_count', 'nbr_retrans_qlen']:
            self.add_leaf(cmd='show ip ospf neighbor detail',
                          src=intf_src+'[neighbors][(?P<neighbor>(.*))][statistics][{key}]'.format(key=key),
                          dest=intf_dest+'[neighbors][(?P<neighbor>(.*))][statistics][{key}]'.format(key=key),
                          neighbor=neighbor)

        ########################################################################
        #                           Final Structure
        ########################################################################

        # Make final Ops structure
        self.make(final_call=True)