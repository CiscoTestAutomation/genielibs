''' 
OSPF Genie Conf Object Implementation for IOSXR - CLI.
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

            #  +- DeviceAttributes
            #      +- VrfAttributes
            for sub, attributes2 in attributes.mapping_values('vrf_attr', 
                                                              sort=True, 
                                                              keys=self.vrf_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                     attributes=attributes2,
                                     unconfig=unconfig))

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

                # router ospf 1
                # router ospf 1 vrf VRF1
                with configurations.submode_context(
                    attributes.format('router ospf {instance} vrf {vrf_name}', force=True) if self.vrf_name != 'default' else \
                    attributes.format('router ospf {instance}', force=True)):

                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # router ospf 1
                    #   router-id 1.1.1.1
                    if attributes.value('router_id'):
                        configurations.append_line(attributes.format('router-id {router_id}'))

                    # router ospf 1
                    #   distance 110
                    if attributes.value('pref_all'):
                        configurations.append_line(attributes.format('distance {pref_all}'))

                    # router ospf 1
                    #   distance ospf inter-area 30
                    #   distance ospf intra-area 40
                    #   distance ospf external 50
                    #   distance ospf inter-area 30 intra-area 40
                    #   distance ospf intra-area 40 external 50
                    #   distance ospf inter-area 30 external 50
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
                    #   nsr disable
                    if attributes.value('nsr_enable') is True and self.vrf_name == 'default':
                        configurations.append_line(attributes.format('nsr'))
                    elif attributes.value('nsr_enable') is False and self.vrf_name == 'default':
                        configurations.append_line(attributes.format('nsr disable'))

                    # GracefulRestart attributes config
                    for gr_key, attributes2 in attributes.sequence_values('gr_keys', sort=True):
                        if unconfig:
                            configurations.append_block(gr_key.build_unconfig(
                                apply=False, attributes=attributes2, **kwargs))
                        else:
                            configurations.append_block(gr_key.build_config(
                                apply=False, attributes=attributes2, **kwargs))

                    # router ospf 1
                    #   mpls ldp auto-config
                    if attributes.value('ldp_autoconfig') and self.vrf_name == 'default':
                        configurations.append_line(attributes.format('mpls ldp auto-config'))

                    # router ospf 1
                    #   mpls ldp sync
                    if attributes.value('ldp_igp_sync'):
                        configurations.append_line(attributes.format('mpls ldp sync'))

                    # router ospf 1
                    #   redistribute bgp 100
                    #   redistribute bgp 100 lsa-type summary
                    #   redistribute bgp 100 lsa-type summary metric 10
                    #   redistribute bgp 100 lsa-type summary metric 10 metric-type 2
                    #   redistribute bgp 100 lsa-type summary metric 10 metric-type 2 nssa-only
                    #   redistribute bgp 100 lsa-type summary metric 10 metric-type 2 nssa-only preserve-med
                    #   redistribute bgp 100 lsa-type summary metric 10 metric-type 2 nssa-only preserve-med tag 24
                    #   redistribute bgp 100 lsa-type summary metric 10 metric-type 2 nssa-only preserve-med tag 24 route-policy BGP_TO_OSPF
                    if attributes.value('redist_bgp_id'):

                        # redistribute bgp {redist_bgp_id}
                        redist_bgp_str = 'redistribute bgp {redist_bgp_id}'

                        # + lsa-type summary
                        if attributes.value('redist_bgp_lsa_type_summary '):
                            redist_bgp_str += ' lsa-type summary'

                        # + metric {redist_bgp_metric}
                        if attributes.value('redist_bgp_metric'):
                            redist_bgp_str += ' metric {redist_bgp_metric}'

                        # + metric-type {redist_bgp_metric_type}
                        if attributes.value('redist_bgp_metric_type'):
                            redist_type = attributes.value('redist_bgp_metric_type').value
                            redist_bgp_str += ' metric-type {}'.format(redist_type)

                        # + nssa-only
                        if attributes.value('redist_bgp_nssa_only'):
                            redist_bgp_str += ' nssa-only'

                        # + preserve-med
                        if attributes.value('redist_bgp_preserve_med'):
                            redist_bgp_str += ' preserve-med'

                        # + tag {redist_bgp_tag}
                        if attributes.value('redist_bgp_tag'):
                            redist_bgp_str += ' tag {redist_bgp_tag}'

                        # + route-policy {redist_bgp_route_map}
                        if attributes.value('redist_bgp_route_map'):
                            redist_bgp_str += ' route-policy {redist_bgp_route_map}'

                        configurations.append_line(attributes.format(redist_bgp_str))

                    # router ospf 1
                    #   redistribute connected
                    #   redistribute connected metric 10
                    #   redistribute connected metric 10 route-policy BGP_TO_OSPF
                    if attributes.value('redist_connected'):

                        # redistribute connected
                        redist_connected_str = 'redistribute connected'

                        # + metric {redist_connected_metric}
                        if attributes.value('redist_connected_metric'):
                            redist_connected_str += ' metric {redist_connected_metric}'

                        # + route-map {redist_connected_route_policy}
                        if attributes.value('redist_connected_route_policy'):
                            redist_connected_str += ' route-policy {redist_connected_route_policy}'

                        configurations.append_line(attributes.format(redist_connected_str))

                    # router ospf 1
                    #   redistribute static
                    #   redistribute static metric 10
                    #   redistribute static metric 10 route-policy BGP_TO_OSPF
                    if attributes.value('redist_static'):

                        # redistribute static
                        redist_static_str = 'redistribute static'

                        # + metric {redist_static_metric}
                        if attributes.value('redist_static_metric'):
                            redist_static_str += ' metric {redist_static_metric}'

                        # + route-policy {redist_static_route_policy}
                        if attributes.value('redist_static_route_policy'):
                            redist_static_str += ' route-policy {redist_static_route_policy}'

                        configurations.append_line(attributes.format(redist_static_str))

                    # router ospf 1
                    #   redistribute isis ABC
                    #   redistribute isis ABC metric 10
                    #   redistribute isis ABC metric 10 route-policy test
                    if attributes.value('redist_isis'):

                        # redistribute isis {redist_isis}
                        redist_isis_str = 'redistribute isis {redist_isis}'

                        # + metric {redist_isis_metric}
                        if attributes.value('redist_isis_metric'):
                            redist_isis_str += ' metric {redist_isis_metric}'

                        # + route-policy {redist_isis_route_policy}
                        if attributes.value('redist_isis_route_policy'):
                            redist_isis_str += ' route-policy {redist_isis_route_policy}'

                        configurations.append_line(attributes.format(redist_isis_str))

                    # router ospf 1
                    #   maximum redistributed-prefixes 10
                    #   maximum redistributed-prefixes 10 50
                    #   maximum redistributed-prefixes 10 50 warning-only
                    if attributes.value('redist_max_prefix'):

                        # maximum redistributed-prefixes {redist_max_prefix}
                        redist_maxpfx_str = 'maximum redistributed-prefixes {redist_max_prefix}'

                        # + {redist_max_prefix_thld}
                        if attributes.value('redist_max_prefix_thld'):
                            redist_maxpfx_str += ' {redist_max_prefix_thld}'

                        # + warning-only
                        if attributes.value('redist_max_prefix_warn_only'):
                            redist_maxpfx_str += ' warning-only'

                        configurations.append_line(attributes.format(redist_maxpfx_str))

                    # router ospf 1
                    #   bfd fast-detect
                    #   bfd fast-detect strict-mode
                    if attributes.value('bfd_enable'):

                        # bfd all-interfaces
                        bfd_str = 'bfd fast-detect'

                        if attributes.value('bfd_strict_mode'):
                            bfd_str += ' strict-mode'

                        configurations.append_line(attributes.format(bfd_str))

                    # router ospf 1
                    #   mpls traffic-eng router-id Loopback0
                    if attributes.value('te_router_id') and self.vrf_name == 'default':
                        configurations.append_line(attributes.format('mpls traffic-eng router-id {te_router_id}'))

                    # router ospf 1
                    #   log adjacency changes
                    #   log adjacency changes detail
                    if attributes.value('log_adjacency_changes'):

                        # log adjacency changes
                        log_str = 'log adjacency changes'

                        # + detail
                        if attributes.value('log_adjacency_changes_detail'):
                            log_str += ' detail'
                        
                        configurations.append_line(attributes.format(log_str))

                    # router ospf 1
                    #   adjacency stagger 563 1625
                    if attributes.value('adjacency_stagger_initial_number') and\
                        attributes.value('adjacency_stagger_maximum_number'):
                        configurations.append_line(attributes.format(
                            'adjacency stagger {adjacency_stagger_initial_number} {adjacency_stagger_maximum_number}'))

                    # router ospf 1
                    #   no auto-cost disable
                    #   auto-cost reference-bandwidth 60000
                    if attributes.value('auto_cost_enable') is False:
                        configurations.append_line(attributes.format('auto-cost disable'))
                    elif attributes.value('auto_cost_enable') is True and \
                        attributes.value('auto_cost_reference_bandwidth'):

                        # auto-cost
                        auto_cost_str = 'auto-cost reference-bandwidth'

                        # Calculate bandwidth based on unit type
                        if attributes.value('auto_cost_bandwidth_unit') and \
                            attributes.value('auto_cost_bandwidth_unit').value == 'gbps':
                            bandwidth = str(attributes.value('auto_cost_reference_bandwidth') * 1000)
                        else:
                            bandwidth = attributes.value('auto_cost_reference_bandwidth')
                        auto_cost_str += ' {}'.format(bandwidth)

                        configurations.append_line(attributes.format(auto_cost_str))

                    # router ospf 1
                    #   maximum paths 30
                    if attributes.value('spf_paths'):
                        configurations.append_line(attributes.format('maximum paths {spf_paths}'))

                    # router ospf 1
                    #   maximum interfaces 123
                    if attributes.value('maximum_interfaces'):
                        configurations.append_line(attributes.format('maximum interfaces {maximum_interfaces}'))

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
                    #   timers throttle lsa all 5000 10000 20000
                    if attributes.value('spf_lsa_start'):

                        # timers throttle {spf_lsa_start}
                        throttle_lsa = 'timers throttle lsa all {spf_lsa_start}'

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

                    # router ospf 1
                    #   area 0.0.0.0
                    with configurations.submode_context(attributes.format('area {area_id}', force=True)):

                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # router ospf 1
                        #   area 0.0.0.0
                        #     mpls traffic-eng
                        if attributes.value('area_te_enable') and self.vrf_name == 'default':
                            configurations.append_line(attributes.format('mpls traffic-eng'))

                        # router ospf 1
                        #   area 0.0.0.0
                        #     bfd fast-detect
                        #     bfd fast-detect disable
                        if attributes.value('area_bfd_enable') is True:
                            configurations.append_line(attributes.format('bfd fast-detect'))
                        elif attributes.value('area_bfd_enable') is False:
                            configurations.append_line(attributes.format('bfd fast-detect disable'))

                        # router ospf 1
                        #   area 0.0.0.0
                        #     bfd minimum-interval {area_bfd_min_interval}
                        if attributes.value('area_bfd_min_interval'):
                            configurations.append_line(attributes.format('bfd minimum-interval {area_bfd_min_interval}'))

                        # router ospf 1
                        #   area 0.0.0.0
                        #     bfd multiplier {area_bfd_multiplier}
                        if attributes.value('area_bfd_multiplier'):
                            configurations.append_line(attributes.format('bfd multiplier {area_bfd_multiplier}'))

                        # router ospf 1
                        #   area 0.0.0.0
                        #     passive enable
                        #     passive disable
                        if attributes.value('area_passive') is True:
                            configurations.append_line(attributes.format('passive enable'))
                        elif attributes.value('area_passive') is False:
                            configurations.append_line(attributes.format('passive disable'))

                        # router ospf 1
                        #   area 0.0.0.0
                        #     mtu-ignore enable
                        #     mtu-ignore disable
                        if attributes.value('area_mtu_ignore') is True:
                            configurations.append_line(attributes.format('mtu-ignore enable'))
                        elif attributes.value('area_mtu_ignore') is False:
                            configurations.append_line(attributes.format('mtu-ignore disable'))

                        # router ospf 1
                        #   area 0.0.0.0
                        #     demand-circuit enable
                        #     demand-circuit disable
                        if attributes.value('area_demand_cirtuit') is True:
                            configurations.append_line(attributes.format('demand-circuit enable'))
                        elif attributes.value('area_demand_cirtuit') is False:
                            configurations.append_line(attributes.format('demand-circuit disable'))

                        # router ospf 1
                        #   area 0.0.0.0
                        #     external-out enable
                        #     external-out disable
                        if attributes.value('area_external_out') is True:
                            configurations.append_line(attributes.format('external-out enable'))
                        elif attributes.value('area_external_out') is False:
                            configurations.append_line(attributes.format('external-out disable'))

                        # router ospf 1
                        #   area 0.0.0.0
                        #     flood-reduction enable
                        #     flood-reduction disable
                        if attributes.value('area_flood_reduction') is True:
                            configurations.append_line(attributes.format('flood-reduction enable'))
                        elif attributes.value('area_flood_reduction') is False:
                            configurations.append_line(attributes.format('flood-reduction disable'))

                        # router ospf 1
                        #   area 0.0.0.0
                        #     link-down fast-detect
                        #     link-down fast-detect disable
                        if attributes.value('area_link_down_fast_detect') is True:
                            configurations.append_line(attributes.format('link-down fast-detect'))
                        elif attributes.value('area_link_down_fast_detect') is False:
                            configurations.append_line(attributes.format('link-down fast-detect disable'))

                        # router ospf 1
                        #   area 0.0.0.0
                        #     mpls ldp auto-config
                        if attributes.value('area_ldp_auto_config') and self.vrf == 'default':
                            configurations.append_line(attributes.format('mpls ldp auto-config'))

                        # router ospf 1
                        #   area 0.0.0.0
                        #     mpls ldp sync
                        #     mpls ldp sync disable
                        if attributes.value('area_ldp_sync') is True:
                            configurations.append_line(attributes.format('mpls ldp sync'))
                        elif attributes.value('area_ldp_sync') is False:
                            configurations.append_line(attributes.format('mpls ldp sync disable'))

                        # router ospf 1
                        #   area 0.0.0.0
                        #     mpls ldp sync-igp-shortcuts
                        if attributes.value('area_ldp_sync_igp_shortcuts') and self.vrf == 'default':
                            configurations.append_line(attributes.format('mpls ldp sync-igp-shortcuts'))

                        # router ospf 1
                        #   area 0.0.0.0
                        #     stub
                        #     nssa
                        #     stub no-summary
                        #     nssa no-summary
                        if attributes.value('area_type').value != 'normal':
                            # stub
                            # nssa
                            atype = attributes.value('area_type').value
                            type_str = ' {}'.format(atype)

                            # + no-summary
                            if attributes.value('summary') is False:
                                type_str += ' no-summary'

                            configurations.append_line(attributes.format(type_str))

                        # router ospf 1
                        #   area 0.0.0.0
                        #     default-cost 100
                        if attributes.value('default_cost'):
                            configurations.append_line(attributes.format('default-cost {default_cost}'))

                        # AreaRange attributes config
                        for arearange_key, attributes2 in attributes.sequence_values('arearange_keys', sort=True):
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
                        #configurations = CliConfigBuilder(unconfig=unconfig)
                        for sub, attributes2 in attributes.mapping_values('interface_attr', 
                                                                          sort=True, 
                                                                          keys=self.interface_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))

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
                        #   area 0.0.0.0
                        #     virtual-link 7.7.7.7
                        with configurations.submode_context(
                            attributes.format('virtual-link {vl_router_id}', force=True)):

                            if unconfig and attributes.iswildcard:
                                configurations.submode_unconfig()

                            # router ospf 1
                            #   area 0.0.0.0
                            #     virtual-link 7.7.7.7
                            #       hello-interval 55
                            if attributes.value('vl_hello_interval'):
                                configurations.append_line(attributes.format('hello-interval {vl_hello_interval}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     virtual-link 7.7.7.7
                            #       dead-interval 55
                            if attributes.value('vl_dead_interval'):
                                configurations.append_line(attributes.format('dead-interval {vl_dead_interval}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     virtual-link 7.7.7.7
                            #       retransmit-interval 55
                            if attributes.value('vl_retransmit_interval'):
                                configurations.append_line(attributes.format('retransmit-interval {vl_retransmit_interval}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     virtual-link 7.7.7.7
                            #       transmit-delay 55
                            if attributes.value('vl_transmit_delay'):
                                configurations.append_line(attributes.format('transmit-delay {vl_transmit_delay}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     virtual-link 7.7.7.7
                            #       authentication message-digest keychain HAHA
                            if attributes.value('vl_auth_trailer_key_chain'):
                                configurations.append_line(attributes.format('authentication message-digest keychain {vl_auth_trailer_key_chain}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     virtual-link 7.7.7.7
                            #       authentication
                            #       authentication-key ABC
                            #       authentication message-digest
                            #       message-digest-key 1 md5 XYZ
                            if attributes.value('vl_auth_trailer_key_crypto_algorithm'):

                                auth_type = attributes.value('vl_auth_trailer_key_crypto_algorithm').value

                                # authentication
                                if auth_type == 'simple':
                                    configurations.append_line(attributes.format('authentication'))

                                    # authentication-key ABC
                                    if attributes.value('vl_auth_trailer_key'):
                                        configurations.append_line(attributes.format('authentication-key {vl_auth_trailer_key}'))

                                # authentication message-digest
                                elif auth_type == 'md5':
                                    configurations.append_line(attributes.format('authentication message-digest'))

                                    # message-digest-key 1 md5 XYZ
                                    if attributes.value('vl_auth_trailer_key'):
                                        configurations.append_line(attributes.format('message-digest-key 1 md5 {vl_auth_trailer_key}'))

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
                        #   area 0.0.0.0
                        #     sham-link 7.7.7.7 8.8.8.8
                        with configurations.submode_context(
                            attributes.format('sham-link {sl_local_id} {sl_remote_id}', force=True)):

                            if unconfig and attributes.iswildcard:
                                configurations.submode_unconfig()

                            # router ospf 1
                            #   area 0.0.0.0
                            #     sham-link 7.7.7.7 8.8.8.8
                            #       hello-interval 55
                            if attributes.value('sl_hello_interval'):
                                configurations.append_line(attributes.format('hello-interval {sl_hello_interval}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     sham-link 7.7.7.7 8.8.8.8
                            #       dead-interval 55
                            if attributes.value('sl_dead_interval'):
                                configurations.append_line(attributes.format('dead-interval {sl_dead_interval}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     sham-link 7.7.7.7 8.8.8.8
                            #       retransmit-interval 55
                            if attributes.value('sl_retransmit_interval'):
                                configurations.append_line(attributes.format('retransmit-interval {sl_retransmit_interval}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     sham-link 7.7.7.7 8.8.8.8
                            #       transmit-delay 55
                            if attributes.value('sl_transmit_delay'):
                                configurations.append_line(attributes.format('transmit-delay {sl_transmit_delay}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     sham-link 7.7.7.7 8.8.8.8
                            #       authentication message-digest keychain "ottawa"
                            if attributes.value('sl_auth_trailer_key_chain'):
                                configurations.append_line(attributes.format('authentication message-digest keychain {sl_auth_trailer_key_chain}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     sham-link 7.7.7.7 8.8.8.8
                            #       authentication
                            #       authentication-key ABC
                            #       authentication message-digest
                            #       message-digest-key 1 md5 XYZ
                            if attributes.value('sl_auth_trailer_key_crypto_algorithm'):

                                auth_type = attributes.value('sl_auth_trailer_key_crypto_algorithm').value

                                # authentication
                                if auth_type == 'simple':
                                    configurations.append_line(attributes.format('authentication'))

                                    # authentication-key ABC
                                    if attributes.value('sl_auth_trailer_key'):
                                        configurations.append_line(attributes.format('authentication-key {sl_auth_trailer_key}'))

                                # authentication message-digest
                                elif auth_type == 'md5':
                                    configurations.append_line(attributes.format('authentication message-digest'))

                                    # message-digest-key 1 md5 XYZ
                                    if attributes.value('sl_auth_trailer_key'):
                                        configurations.append_line(attributes.format('message-digest-key 1 md5 {sl_auth_trailer_key}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     sham-link 7.7.7.7 8.8.8.8
                            #       cost 10
                            if attributes.value('sl_cost'):
                                configurations.append_line(attributes.format('cost {sl_cost}'))

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

                        # router ospf 1
                        #   area 0.0.0.0
                        #     interface GigabitEthernet1
                        with configurations.submode_context(
                            attributes.format('interface {interface_name}', force=True)):

                            if unconfig and attributes.iswildcard:
                                configurations.submode_unconfig()

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       cost 100
                            if attributes.value('if_cost'):
                                configurations.append_line(attributes.format('cost {if_cost}'))

                            # InterfaceStaticNeighbor attributes config
                            for intf_staticnbr_key, attributes2 in attributes.sequence_values('intf_staticnbr_keys', sort=True):
                                if unconfig:
                                    configurations.append_block(intf_staticnbr_key.build_unconfig(
                                        apply=False, attributes=attributes2, **kwargs))
                                else:
                                    configurations.append_block(intf_staticnbr_key.build_config(
                                        apply=False, attributes=attributes2, **kwargs))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       network point-to-point
                            if attributes.value('if_type'):
                                iftype = attributes.value('if_type').value
                                configurations.append_line(attributes.format('network {}'.format(iftype)))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       passive
                            if attributes.value('if_passive'):
                                configurations.append_line(attributes.format('passive'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       demand-circuit
                            if attributes.value('if_demand_circuit'):
                                configurations.append_line(attributes.format('demand-circuit'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       priority 100
                            if attributes.value('if_priority'):
                                configurations.append_line(attributes.format('priority {if_priority}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       bfd fast-detect
                            if attributes.value('if_bfd_enable'):
                                configurations.append_line(attributes.format('bfd fast-detect'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       bfd minimum-interval 50
                            if attributes.value('if_bfd_interval'):
                                configurations.append_line(attributes.format('bfd minimum-interval {if_bfd_interval}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       bfd multiplier 7
                            if attributes.value('if_bfd_multiplier'):
                                configurations.append_line(attributes.format('bfd multiplier {if_bfd_multiplier}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       hello-interval 10
                            if attributes.value('if_hello_interval'):
                                configurations.append_line(attributes.format('hello-interval {if_hello_interval}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       dead-interval 10
                            if attributes.value('if_dead_interval'):
                                configurations.append_line(attributes.format('dead-interval {if_dead_interval}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       retransmit-interval 10
                            if attributes.value('if_retransmit_interval'):
                                configurations.append_line(attributes.format('retransmit-interval {if_retransmit_interval}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       security ttl
                            #       security ttl hops 50
                            if attributes.value('if_ttl_sec_enable'):

                                # security ttl
                                ttl_str = 'security ttl'

                                # + hops 50
                                if attributes.value('if_ttl_sec_hops'):
                                    ttl_str += ' hops {if_ttl_sec_hops}'

                                configurations.append_line(attributes.format(ttl_str))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       authentication message-digest keychain ottawa
                            if attributes.value('if_auth_trailer_key_chain'):
                                configurations.append_line(attributes.format('authentication message-digest keychain {if_auth_trailer_key_chain}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       authentication
                            #       authentication-key ABC
                            #       authentication message-digest
                            #       message-digest-key 1 md5 XYZ
                            if attributes.value('if_auth_trailer_key_crypto_algorithm'):

                                auth_type = attributes.value('if_auth_trailer_key_crypto_algorithm').value

                                # authentication
                                if auth_type == 'simple':
                                    configurations.append_line(attributes.format('authentication'))

                                    # authentication-key ABC
                                    if attributes.value('if_auth_trailer_key'):
                                        configurations.append_line(attributes.format('authentication-key {if_auth_trailer_key}'))

                                # authentication message-digest
                                elif auth_type == 'md5':
                                    configurations.append_line(attributes.format('authentication message-digest'))

                                    # message-digest-key 1 md5 anything
                                    if attributes.value('if_auth_trailer_key'):
                                        configurations.append_line(attributes.format('message-digest-key 1 md5 {if_auth_trailer_key}'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       mtu-ignore
                            if attributes.value('if_mtu_ignore'):
                                configurations.append_line(attributes.format('mtu-ignore'))

                            # router ospf 1
                            #   area 0.0.0.0
                            #     interface GigabitEthernet1
                            #       prefix-suppression
                            if attributes.value('if_prefix_suppression'):
                                configurations.append_line(attributes.format('prefix-suppression'))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)

