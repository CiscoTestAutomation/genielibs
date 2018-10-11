''' 
OSPF Genie Conf Object Implementation for IOSXE - CLI.
'''

# Pyhon
from abc import ABC

# Genie
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

# Ospf
# +- DeviceAttributes
#   +- VrfAttributes
#     +- AreaAttributes
#       +- VirtualLinkAttributes
#       +- ShamLinkAttributes
#       +- InterfaceAttributes


class Ospf(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            # Seperate CliConfigBuilder for InterfaceAttribute configuration
            self.interface_config = CliConfigBuilder(unconfig=unconfig)

            #  +- DeviceAttributes
            #      +- VrfAttributes
            for sub, attributes2 in attributes.mapping_values('vrf_attr', 
                                                              sort=True, 
                                                              keys=self.vrf_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                     attributes=attributes2,
                                     unconfig=unconfig))

            # Add InterfaceAttribute configuration
            configurations.append_block(self.interface_config)

            if apply:
                if configurations:
                    self.device.configure(configurations)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        # +- DeviceAttributes
        #   +- VrfAttributes
        class VrfAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                self.interface_router_configurations = CliConfigBuilder(unconfig=unconfig)

                # router ospf 1
                # router ospf 1 vrf VRF1
                with configurations.submode_context(
                    attributes.format('router ospf {instance} vrf {vrf_name}', force=True) if self.vrf_name != 'default' else \
                    attributes.format('router ospf {instance}', force=True)):

                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # router ospf 1
                    #   shutdown/no shutdown
                    if attributes.value('enable') is True:
                        configurations.append_line(attributes.format('no shutdown'))
                    elif attributes.value('enable'):
                        configurations.append_line(attributes.format('shutdown'))

                    # router ospf 1
                    #   router-id 1.1.1.1
                    if attributes.value('router_id'):
                        configurations.append_line(attributes.format('router-id {router_id}'))

                    # router ospf 1
                    #   distance 110
                    if attributes.value('pref_all'):
                        configurations.append_line(attributes.format('distance {pref_all}'))

                    # router ospf 1
                    #   distance ospf inter-area 30 intra-area 40 external 50
                    if attributes.value('pref_intra_area') or \
                        attributes.value('pref_inter_area') or \
                        attributes.value('pref_external'):

                        # distance ospf
                        dist_cfg_str = 'distance ospf'

                        # If internal, overwrite intra with inter
                        if attributes.value('pref_internal'):
                            attributes.value('pref_intra_area').value = attributes.value('pref_inter_area').value

                        # + intra-area {pref_intra_area}
                        if attributes.value('pref_intra_area'):
                            dist_cfg_str += ' intra-area {pref_intra_area}'
                        
                        # + inter-area {pref_inter_area}
                        if attributes.value('pref_inter_area'):
                            dist_cfg_str += ' inter-area {pref_inter_area}'
                        
                        # + external {pref_external}
                        if attributes.value('pref_external'):
                            dist_cfg_str += ' external {pref_external}'

                        configurations.append_line(attributes.format(dist_cfg_str))

                    # router ospf 1
                    #   nsr
                    if attributes.value('nsr_enable'):
                        configurations.append_line(attributes.format('nsr'))

                    # GracefulRestart attributes config
                    for gr_key, attributes2 in attributes.sequence_values('gr_keys', sort=True):
                        if unconfig:
                            configurations.append_block(gr_key.build_unconfig(
                                apply=False, attributes=attributes2, **kwargs))
                        else:
                            configurations.append_block(gr_key.build_config(
                                apply=False, attributes=attributes2, **kwargs))
                    
                    # router ospf 1
                    #   mpls ldp autoconfig area 0.0.0.0
                    if attributes.value('ldp_autoconfig'):
                        
                        # mpls ldp autoconfig
                        ldp_str = 'mpls ldp autoconfig'

                        # + area {ldp_auto_config_area_id}
                        if attributes.value('ldp_auto_config_area_id'):
                            ldp_str += ' area {ldp_auto_config_area_id}'

                        configurations.append_line(attributes.format(ldp_str))

                    # router ospf 1
                    #   mpls ldp sync
                    if attributes.value('ldp_igp_sync'):
                        configurations.append_line(attributes.format('mpls ldp sync'))

                    # router ospf 1
                    #   redistribute bgp 100 metric 10 metric-type 1 subnets nssa-only tag 5 route-map ottawa
                    if attributes.value('redist_bgp_id'):

                        # redistribute bgp {redist_bgp_id}
                        redist_bgp_str = 'redistribute bgp {redist_bgp_id}'

                        # + metric {redist_bgp_metric}
                        if attributes.value('redist_bgp_metric'):
                            redist_bgp_str += ' metric {redist_bgp_metric}'

                        # + metric-type {redist_bgp_metric_type}
                        if attributes.value('redist_bgp_metric_type'):
                            redist_type = attributes.value('redist_bgp_metric_type').value
                            redist_bgp_str += ' metric-type {}'.format(redist_type)

                        # + subnets
                        if attributes.value('redist_bgp_subnets'):
                            redist_bgp_str += ' subnets'

                        # + nssa-only
                        if attributes.value('redist_bgp_nssa_only'):
                            redist_bgp_str += ' nssa-only'

                        # + tag {redist_bgp_tag}
                        if attributes.value('redist_bgp_tag'):
                            redist_bgp_str += ' tag {redist_bgp_tag}'

                        # + route-map {redist_bgp_route_map}
                        if attributes.value('redist_bgp_route_map'):
                            redist_bgp_str += ' route-map {redist_bgp_route_map}'

                        configurations.append_line(attributes.format(redist_bgp_str))

                    # router ospf 1
                    #   redistribute connected metric 10 route-map toronto
                    if attributes.value('redist_connected'):

                        # redistribute connected
                        redist_connected_str = 'redistribute connected'

                        # + metric {redist_connected_metric}
                        if attributes.value('redist_connected_metric'):
                            redist_connected_str += ' metric {redist_connected_metric}'

                        # + route-map {redist_connected_route_policy}
                        if attributes.value('redist_connected_route_policy'):
                            redist_connected_str += ' route-map {redist_connected_route_policy}'

                        configurations.append_line(attributes.format(redist_connected_str))

                    # router ospf 1
                    #   redistribute static metric 10 route-map montreal
                    if attributes.value('redist_static'):

                        # redistribute static
                        redist_static_str = 'redistribute static'

                        # + metric {redist_static_metric}
                        if attributes.value('redist_static_metric'):
                            redist_static_str += ' metric {redist_static_metric}'

                        # + route-map {redist_static_route_policy}
                        if attributes.value('redist_static_route_policy'):
                            redist_static_str += ' route-map {redist_static_route_policy}'

                        configurations.append_line(attributes.format(redist_static_str))

                    # router ospf 1
                    #   redistribute isis metric 10 route-map test
                    if attributes.value('redist_isis'):

                        # redistribute isis {redist_isis}
                        redist_isis_str = 'redistribute isis {redist_isis}'

                        # + metric {redist_isis_metric}
                        if attributes.value('redist_isis_metric'):
                            redist_isis_str += ' metric {redist_isis_metric}'

                        # + route-map {redist_isis_route_policy}
                        if attributes.value('redist_isis_route_policy'):
                            redist_isis_str += ' route-map {redist_isis_route_policy}'

                        configurations.append_line(attributes.format(redist_isis_str))

                    # router ospf 1
                    #   redistribute maximum-prefix 10 50 warning-only
                    if attributes.value('redist_max_prefix'):

                        # redistribute maximum-prefix {redist_max_prefix}
                        redist_maxpfx_str = 'redistribute maximum-prefix {redist_max_prefix}'

                        # + {redist_max_prefix_thld}
                        if attributes.value('redist_max_prefix_thld'):
                            redist_maxpfx_str += ' {redist_max_prefix_thld}'

                        # + warning-only
                        if attributes.value('redist_max_prefix_warn_only'):
                            redist_maxpfx_str += ' warning-only'

                        configurations.append_line(attributes.format(redist_maxpfx_str))

                    # router ospf 1
                    #   bfd all-interfaces strict-mode
                    if attributes.value('bfd_enable'):

                        # bfd all-interfaces
                        bfd_str = 'bfd all-interfaces'

                        if attributes.value('bfd_strict_mode'):
                            bfd_str += ' strict-mode'

                        configurations.append_line(attributes.format(bfd_str))

                    # router ospf 1
                    #   mpls traffic-eng router-id Loopback0
                    if attributes.value('te_router_id'):
                        configurations.append_line(attributes.format('mpls traffic-eng router-id {te_router_id}'))

                    # router ospf 1
                    #   log-adjacency-changes
                    #   log-adjacency-changes detail
                    if attributes.value('log_adjacency_changes'):

                        # log-adjacency-changes
                        log_str = 'log-adjacency-changes'

                        # + detail
                        if attributes.value('log_adjacency_changes_detail'):
                            log_str += ' detail'
                        
                        configurations.append_line(attributes.format(log_str))

                    # router ospf 1
                    #   adjacency stagger 563 1625
                    if attributes.value('adjacency_stagger_initial_number'):
                        
                        # adjacency stagger {adjacency_stagger_initial_number}
                        stagger_str = 'adjacency stagger {adjacency_stagger_initial_number}'

                        # + {adjacency_stagger_maximum_number}
                        if attributes.value('adjacency_stagger_maximum_number'):
                            stagger_str += ' {adjacency_stagger_maximum_number}'

                        configurations.append_line(attributes.format(stagger_str))

                    # router ospf 1
                    #   auto-cost
                    #   auto-cost reference-bandwidth 60000
                    if attributes.value('auto_cost_enable') is False:
                        configurations.append_line(attributes.format('no auto-cost'))
                    elif attributes.value('auto_cost_enable') is True:

                        # auto-cost
                        auto_cost_str = 'auto-cost'

                        # + reference-bandwidth
                        if attributes.value('auto_cost_reference_bandwidth'):
                            auto_cost_str += ' reference-bandwidth'
                            # Calculate bandwidth based on unit type
                            if attributes.value('auto_cost_bandwidth_unit').value == 'gbps':
                                bandwidth = str(attributes.value('auto_cost_reference_bandwidth') * 1000)
                            else:
                                bandwidth = attributes.value('auto_cost_reference_bandwidth')
                            auto_cost_str += ' {}'.format(bandwidth)

                        configurations.append_line(attributes.format(auto_cost_str))

                    # router ospf 1
                    #   maximum-paths 15
                    if attributes.value('spf_paths'):
                        configurations.append_line(attributes.format('maximum-paths {spf_paths}'))

                    # router ospf 1
                    #   timers throttle spf 5000 10000 20000
                    if attributes.value('spf_start'):

                        # timers throttle spf {spf_start}
                        throttle_str = 'timers throttle spf {spf_start}'

                        # + {spf_hold}
                        if attributes.value('spf_hold'):
                            throttle_str += ' {spf_hold}'

                        # + {spf_maximum}
                        if attributes.value('spf_maximum'):
                            throttle_str += ' {spf_maximum}'

                        configurations.append_line(attributes.format(throttle_str))

                    # router ospf 1
                    #   timers throttle lsa 5000 10000 20000
                    if attributes.value('spf_lsa_start'):

                        # timers throttle {spf_lsa_start}
                        throttle_lsa = 'timers throttle lsa {spf_lsa_start}'

                        # + {spf_lsa_hold}
                        if attributes.value('spf_lsa_hold'):
                            throttle_lsa += ' {spf_lsa_hold}'

                        # + {spf_lsa_maximum}
                        if attributes.value('spf_lsa_maximum'):
                            throttle_lsa += ' {spf_lsa_maximum}'

                        configurations.append_line(attributes.format(throttle_lsa))

                    # router ospf 1
                    #   max-lsa 56666666
                    if attributes.value('db_ctrl_max_lsa'):
                        configurations.append_line(attributes.format('max-lsa {db_ctrl_max_lsa}'))

                    # StubRouter attributes config
                    for sr_key, attributes2 in attributes.sequence_values('sr_keys', sort=True):
                        if unconfig:
                            configurations.append_block(sr_key.build_unconfig(
                                apply=False, attributes=attributes2, **kwargs))
                        else:
                            configurations.append_block(sr_key.build_config(
                                apply=False, attributes=attributes2, **kwargs))

                    # router ospf 1
                    #   default-information originate always
                    if attributes.value('default_originate'):
                        
                        # + default-information originate
                        default_originate_str = 'default-information originate'

                        # + always
                        if attributes.value('default_originate_always'):
                            default_originate_str += ' always'

                        configurations.append_line(attributes.format(default_originate_str))

                    # +- DeviceAttributes
                    #   +- VrfAttributes
                    #     +- AreaAttributes
                    for sub, attributes2 in attributes.mapping_values('area_attr', 
                                                                      sort=True, 
                                                                      keys=self.area_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))
                
                    # Add interface configurations under router submode
                    configurations.append_block(self.interface_router_configurations)

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

            # +- DeviceAttributes
            #   +- VrfAttributes
            #     +- AreaAttributes
            class AreaAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # AreaNetwork attributes config
                    for areanetwork_key, attributes2 in attributes.sequence_values('areanetwork_keys', sort=True):
                        kwargs = {'area':self.area}
                        if unconfig:
                            configurations.append_block(areanetwork_key.build_unconfig(
                                apply=False, attributes=attributes2, **kwargs))
                        else:
                            configurations.append_block(areanetwork_key.build_config(
                                apply=False, attributes=attributes2, **kwargs))

                    # router ospf 1
                    #   mpls traffic-eng area 2
                    if attributes.value('area_te_enable'):
                        configurations.append_line(attributes.format('mpls traffic-eng area {area}'))

                    # router ospf 1
                    #   area 2 stub
                    #   area 2 nssa
                    #   area 2 stub no-summary
                    #   area 2 nssa no-summary
                    if attributes.value('area_type').value != 'normal':
                        #   area 2 stub
                        #   area 2 nssa
                        type_str = 'area {area}'
                        atype = attributes.value('area_type').value
                        type_str += ' {}'.format(atype)

                        # + summary
                        if attributes.value('summary') is False:
                            type_str += ' no-summary'

                        configurations.append_line(attributes.format(type_str))

                    # router ospf 1
                    #   area 2 default-cost 100
                    if attributes.value('default_cost'):
                        configurations.append_line(attributes.format('area {area} default-cost {default_cost}'))

                    # AreaRange attributes config
                    for arearange_key, attributes2 in attributes.sequence_values('arearange_keys', sort=True):
                        kwargs = {'area':self.area}
                        if unconfig:
                            configurations.append_block(arearange_key.build_unconfig(
                                apply=False, attributes=attributes2, **kwargs))
                        else:
                            configurations.append_block(arearange_key.build_config(
                                apply=False, attributes=attributes2, **kwargs))

                    # +- DeviceAttributes
                    #   +- VrfAttributes
                    #     +- AreaAttributes
                    #       +- VirtualLinkAttributes
                    for sub, attributes2 in attributes.mapping_values('virtual_link_attr', 
                                                                      sort=True, 
                                                                      keys=self.virtual_link_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                    # +- DeviceAttributes
                    #   +- VrfAttributes
                    #     +- AreaAttributes
                    #       +- ShamLinkAttributes
                    for sub, attributes2 in attributes.mapping_values('sham_link_attr', 
                                                                      sort=True, 
                                                                      keys=self.sham_link_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                    # +- DeviceAttributes
                    #   +- VrfAttributes
                    #     +- AreaAttributes
                    #       +- InterfaceAttributes
                    interface_config = CliConfigBuilder(unconfig=unconfig)
                    for sub, attributes2 in attributes.mapping_values('interface_attr', 
                                                                      sort=True, 
                                                                      keys=self.interface_attr):
                        interface_config.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                    self.parent.parent.interface_config.append_block(interface_config)
                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)

                # +- DeviceAttributes
                #   +- VrfAttributes
                #     +- AreaAttributes
                #       +- VirtualLinkAttributes
                class VirtualLinkAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                        assert not apply
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # router ospf 1
                        #   area 2 virtual-link 7.7.7.7
                        if attributes.value('vl_router_id'):
                            configurations.append_line(attributes.format('area {area} virtual-link {vl_router_id}'))

                            # router ospf 1
                            #   area 2 virtual-link 7.7.7.7 hello-interval 55
                            if attributes.value('vl_hello_interval'):
                                configurations.append_line(attributes.format('area {area} virtual-link {vl_router_id} hello-interval {vl_hello_interval}'))

                            # router ospf 1
                            #   area 2 virtual-link 7.7.7.7 dead-interval 55
                            if attributes.value('vl_dead_interval'):
                                configurations.append_line(attributes.format('area {area} virtual-link {vl_router_id} dead-interval {vl_dead_interval}'))

                            # router ospf 1
                            #   area 2 virtual-link 7.7.7.7 retransmit-interval 55
                            if attributes.value('vl_retransmit_interval'):
                                configurations.append_line(attributes.format('area {area} virtual-link {vl_router_id} retransmit-interval {vl_retransmit_interval}'))

                            # router ospf 1
                            #   area 2 virtual-link 7.7.7.7 transmit-delay 55
                            if attributes.value('vl_transmit_delay'):
                                configurations.append_line(attributes.format('area {area} virtual-link {vl_router_id} transmit-delay {vl_transmit_delay}'))

                            # router ospf 1
                            #   area 2 virtual-link 7.7.7.7 ttl-security hops 163
                            if attributes.value('vl_ttl_sec_hops'):
                                configurations.append_line(attributes.format('area {area} virtual-link {vl_router_id} ttl-security hops {vl_ttl_sec_hops}'))

                            # router ospf 1
                            #   area 2 virtual_link 7.7.7.7 authentication key-chain ottawa
                            if attributes.value('vl_auth_trailer_key_chain'):
                                configurations.append_line(attributes.format('area {area} virtual-link {vl_router_id} authentication key-chain {vl_auth_trailer_key_chain}'))

                            # router ospf 1
                            #   area 2 virtual-link 7.7.7.7 authentication
                            #   area 2 virtual-link 7.7.7.7 authentication-key anything
                            #   area 2 virtual_link 7.7.7.7 authentication message-digest
                            #   area 2 virtual_link 7.7.7.7 message-digest-key 1 md5 anything
                            if attributes.value('vl_auth_trailer_key_crypto_algorithm'):

                                auth_type = attributes.value('vl_auth_trailer_key_crypto_algorithm').value

                                # area 2 virtual-link 7.7.7.7 authentication
                                if auth_type == 'simple':
                                    configurations.append_line(attributes.format('area {area} virtual-link {vl_router_id} authentication'))

                                    # area 2 virtual-link 7.7.7.7 authentication-key anything
                                    if attributes.value('vl_auth_trailer_key'):
                                        configurations.append_line(attributes.format('area {area} virtual-link {vl_router_id} authentication-key {vl_auth_trailer_key}'))

                                # area 2 virtual_link 7.7.7.7 authentication message-digest
                                elif auth_type == 'md5':
                                    configurations.append_line(attributes.format('area {area} virtual-link {vl_router_id} authentication message-digest'))

                                    # area 2 virtual_link 7.7.7.7 message-digest-key 1 md5 anything
                                    if attributes.value('vl_auth_trailer_key'):
                                        configurations.append_line(attributes.format('area {area} virtual-link {vl_router_id} message-digest-key 1 md5 {vl_auth_trailer_key}'))


                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)

                # +- DeviceAttributes
                #   +- VrfAttributes
                #     +- AreaAttributes
                #       +- ShamLinkAttributes
                class ShamLinkAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                        assert not apply
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # router ospf 1
                        #   area 2 sham-link 1.1.1.1 2.2.2.2
                        if attributes.value('sl_local_id') and attributes.value('sl_remote_id'):
                            configurations.append_line(attributes.format('area {area} sham-link {sl_local_id} {sl_remote_id}'))

                            # router ospf 1
                            #   area 2 sham-link 1.1.1.1 2.2.2.2 ttl-security hops 163
                            if attributes.value('sl_ttl_sec_hops'):
                                configurations.append_line(attributes.format('area {area} sham-link {sl_local_id} {sl_remote_id} ttl-security hops {sl_ttl_sec_hops}'))

                            # router ospf 1
                            #   area 2 sham-link 1.1.1.1 2.2.2.2 cost 10
                            if attributes.value('sl_cost'):
                                configurations.append_line(attributes.format('area {area} sham-link {sl_local_id} {sl_remote_id} cost {sl_cost}'))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)

                # +- DeviceAttributes
                #   +- VrfAttributes
                #     +- AreaAttributes
                #       +- InterfaceAttributes
                class InterfaceAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                        assert not apply
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)
                        intf_rtr_cfgs = CliConfigBuilder(unconfig=unconfig)

                        # passive-interface GigabitEthernet1
                        if attributes.value('if_passive'):
                            intf_rtr_cfgs.append_line(attributes.format('passive-interface {interface_name}'))

                        # InterfaceStaticNeighbor attributes config
                        for intf_staticnbr_key, attributes2 in attributes.sequence_values('intf_staticnbr_keys', sort=True):
                            if unconfig:
                                intf_rtr_cfgs.append_block(intf_staticnbr_key.build_unconfig(
                                    apply=False, attributes=attributes2, **kwargs))
                            else:
                                intf_rtr_cfgs.append_block(intf_staticnbr_key.build_config(
                                    apply=False, attributes=attributes2, **kwargs))

                        # Add intf_rtr_cfgs to VrfAttributes
                        self.parent.parent.interface_router_configurations.append_block(intf_rtr_cfgs)

                        # interface GigabitEthernet1
                        with configurations.submode_context(
                            attributes.format('interface {interface_name}', force=True)):

                            # interface GigabitEthernet1
                            #   ip ospf 1 area 2
                            if attributes.value('if_admin_control'):
                                configurations.append_line(attributes.format('ip ospf {instance} area {area}'))

                            # interface GigabitEthernet1
                            #   ip ospf cost 100
                            if attributes.value('if_cost'):
                                configurations.append_line(attributes.format('ip ospf cost {if_cost}'))

                            # interface GigabitEthernet1
                            #   ip ospf network point-to-point
                            if attributes.value('if_type'):
                                iftype = attributes.value('if_type').value
                                configurations.append_line(attributes.format('ip ospf network {}'.format(iftype)))

                            # interface GigabitEthernet1
                            #   ip ospf demand-circuit
                            if attributes.value('if_demand_circuit'):
                                configurations.append_line(attributes.format('ip ospf demand-circuit'))

                            # interface GigabitEthernet1
                            #   ip ospf priority 100
                            if attributes.value('if_priority'):
                                configurations.append_line(attributes.format('ip ospf priority {if_priority}'))

                            # interface GigabitEthernet1
                            #   ip ospf bfd
                            if attributes.value('if_bfd_enable'):
                                configurations.append_line(attributes.format('ip ospf bfd'))

                            # interface GigabitEthernet1
                            #   bfd interval 50 min_rx 60 multiplier 2
                            if attributes.value('if_bfd_interval'):

                                # bfd interval [if_bfd_interval]
                                bfd_str = 'bfd interval {if_bfd_interval}'

                                # + min_rx {if_bfd_min_interval}
                                if attributes.value('if_bfd_min_interval'):
                                    bfd_str += ' min_rx {if_bfd_min_interval}'

                                # + multiplier {if_bfd_multiplier}
                                if attributes.value('if_bfd_multiplier'):
                                    bfd_str += ' multiplier {if_bfd_multiplier}'

                                configurations.append_line(attributes.format(bfd_str))

                            # interface GigabitEthernet1
                            #   ip ospf hello-interval 10
                            if attributes.value('if_hello_interval'):
                                configurations.append_line(attributes.format('ip ospf hello-interval {if_hello_interval}'))

                            # interface GigabitEthernet1
                            #   ip ospf dead-interval 10
                            if attributes.value('if_dead_interval'):
                                configurations.append_line(attributes.format('ip ospf dead-interval {if_dead_interval}'))

                            # interface GigabitEthernet1
                            #   ip ospf retransmit-interval 10
                            if attributes.value('if_retransmit_interval'):
                                configurations.append_line(attributes.format('ip ospf retransmit-interval {if_retransmit_interval}'))

                            # interface GigabitEthernet1
                            #   ip ospf lls
                            #   ip ospf lls disable
                            if attributes.value('if_lls') is True:
                                configurations.append_line(attributes.format('ip ospf lls'))
                            elif attributes.value('if_lls') is False:
                                configurations.append_line(attributes.format('ip ospf lls disable'))

                            # interface GigabitEthernet1
                            #   ip ospf ttl-security hops 50
                            if attributes.value('if_ttl_sec_enable'):

                                # ip ospf ttl-security
                                ttl_str = 'ip ospf ttl-security'

                                # + hops 50
                                if attributes.value('if_ttl_sec_hops'):
                                    ttl_str += ' hops {if_ttl_sec_hops}'

                                configurations.append_line(attributes.format(ttl_str))

                            # interface GigabitEthernet1
                            #   ip ospf authentication key-chain ottawa
                            if attributes.value('if_auth_trailer_key_chain'):
                                configurations.append_line(attributes.format('ip ospf authentication key-chain {if_auth_trailer_key_chain}'))

                            # interface GigabitEthernet1
                            #   ip ospf authentication
                            #   ip ospf authentication-key anything
                            #   ip ospf authentication message-digest
                            #   ip ospf message-digest-key 1 md5 anything
                            if attributes.value('if_auth_trailer_key_crypto_algorithm'):

                                auth_type = attributes.value('if_auth_trailer_key_crypto_algorithm').value

                                # ip ospf authentication
                                if auth_type == 'simple':
                                    configurations.append_line(attributes.format('ip ospf authentication'))

                                    # ip ospf authentication-key anything
                                    if attributes.value('if_auth_trailer_key'):
                                        configurations.append_line(attributes.format('ip ospf authentication-key {if_auth_trailer_key}'))

                                # ip ospf authentication message-digest
                                elif auth_type == 'md5':
                                    configurations.append_line(attributes.format('ip ospf authentication message-digest'))

                                    # ip ospf message-digest-key 1 md5 anything
                                    if attributes.value('if_auth_trailer_key'):
                                        configurations.append_line(attributes.format('ip ospf message-digest-key 1 md5 {if_auth_trailer_key}'))

                            # interface GigabitEthernet1
                            #   ip ospf mtu-ignore
                            if attributes.value('if_mtu_ignore'):
                                configurations.append_line(attributes.format('ip ospf mtu-ignore'))

                            # interface GigabitEthernet1
                            #   ip ospf prefix-suppression
                            if attributes.value('if_prefix_suppression'):
                                configurations.append_line(attributes.format('ip ospf prefix-suppression'))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)

