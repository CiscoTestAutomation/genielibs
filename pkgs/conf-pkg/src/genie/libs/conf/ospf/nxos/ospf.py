''' 
OSPF Genie Conf Object Implementation for NXOS - CLI.
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

            # feature ospf
            if attributes.value('enabled'):
                if unconfig is False:
                    configurations.append_line(
                        attributes.format('feature ospf'))

                # Make sure that only enabled was provided in attributes
                # If wildcard,  then delete everything
                elif unconfig is True and\
                     attributes.attributes == {'enabled': {True: None}} or \
                        attributes.iswildcard:
                    configurations.append_line('no feature ospf', raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

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

                # router ospf 1
                with configurations.submode_context(
                    attributes.format('router ospf {instance}', force=True)):

                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # router ospf 1
                    #   vrf VRF1
                    if self.vrf_name != 'default':
                        with configurations.submode_context(
                            attributes.format('vrf {vrf_name}', force=True) ):

                            if unconfig and attributes.iswildcard:
                                configurations.submode_unconfig()

                            # router ospf 1
                            #   vrf VRF1
                            #     shutdown/no shutdown
                            if attributes.value('enable') is False:
                                configurations.append_line(attributes.format('shutdown'))
                            elif attributes.value('enable'):
                                configurations.append_line(attributes.format('no shutdown'))

                            # router ospf 1
                            #   vrf VRF1
                            #     router-id 1.1.1.1
                            if attributes.value('router_id'):
                                configurations.append_line(attributes.format('router-id {router_id}'))

                            # router ospf 1
                            #   distance 110
                            if attributes.value('pref_all'):
                                configurations.append_line(attributes.format('distance {pref_all}'))

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
                            if attributes.value('ldp_autoconfig') and \
                                attributes.value('ldp_auto_config_area_id'):
                                configurations.append_line(attributes.format(
                                    'mpls ldp autoconfig area {ldp_auto_config_area_id}'))

                            # router ospf 1
                            #   mpls ldp sync
                            if attributes.value('ldp_igp_sync'):
                                configurations.append_line(attributes.format('mpls ldp sync'))

                            # router ospf 1
                            #   redistribute bgp 100 route-map ottawa
                            if attributes.value('redist_bgp_id') and \
                                attributes.value('redist_bgp_route_map'):
                                configurations.append_line(attributes.format(
                                    'redistribute bgp {redist_bgp_id} route-map {redist_bgp_route_map}'))

                            # router ospf 1
                            #   redistribute direct route-map toronto
                            if attributes.value('redist_connected') and \
                                attributes.value('redist_connected_route_policy'):
                                configurations.append_line(attributes.format(
                                    'redistribute direct route-map {redist_connected_route_policy}'))

                            # router ospf 1
                            #   redistribute static route-map montreal
                            if attributes.value('redist_static') and \
                                attributes.value('redist_static_route_policy'):
                                configurations.append_line(attributes.format(
                                    'redistribute static route-map {redist_static_route_policy}'))

                            # router ospf 1
                            #   redistribute isis ABC route-map nowhere
                            if attributes.value('redist_isis') and \
                                attributes.value('redist_isis_route_policy'):
                                configurations.append_line(attributes.format(
                                    'redistribute isis {redist_isis} route-map {redist_isis_route_policy}'))

                            # router ospf 1
                            #   redistribute maximum-prefix 123 10 warning-only
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
                            #   bfd
                            if attributes.value('bfd_enable'):
                                configurations.append_line(attributes.format('bfd'))

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
                            #   auto-cost reference-bandwidth 60000
                            #   auto-cost reference-bandwidth 60000 mbps
                            #   auto-cost reference-bandwidth 60000 gbps
                            if attributes.value('auto_cost_enable') is False:
                                configurations.append_line(attributes.format('no auto-cost reference-bandwidth'))
                            elif attributes.value('auto_cost_enable') is True and \
                                attributes.value('auto_cost_reference_bandwidth'):

                                # auto-cost reference-bandwidth {auto_cost_reference_bandwidth}
                                auto_cost_str = 'auto-cost reference-bandwidth {auto_cost_reference_bandwidth}'

                                # + {auto_cost_bandwidth_unit}
                                if attributes.value('auto_cost_bandwidth_unit'):
                                    unit = attributes.value('auto_cost_bandwidth_unit').value
                                    auto_cost_str += ' {}'.format(unit)

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
                    else:
                        # router ospf 1
                        #   shutdown/no shutdown
                        if attributes.value('enable') is False:
                            configurations.append_line(attributes.format('shutdown'))
                        elif attributes.value('enable'):
                            configurations.append_line(attributes.format('no shutdown'))

                        # router ospf 1
                        #   router-id 1.1.1.1
                        if attributes.value('router_id'):
                            configurations.append_line(attributes.format('router-id {router_id}'))

                        # router ospf 1
                        #   distance 110
                        if attributes.value('pref_all'):
                            configurations.append_line(attributes.format('distance {pref_all}'))

                        # GracefulRestart attributes config
                        for gr_key, attributes2 in attributes.sequence_values('gr_keys', sort=True):
                            if attributes.value('gr_key').value == 'cisco':
                                continue
                            if unconfig:
                                configurations.append_block(gr_key.build_unconfig(
                                    apply=False, attributes=attributes2, **kwargs))
                            else:
                                configurations.append_block(gr_key.build_config(
                                    apply=False, attributes=attributes2, **kwargs))
                        
                        # router ospf 1
                        #   mpls ldp autoconfig area 0.0.0.0
                        if attributes.value('ldp_autoconfig') and \
                            attributes.value('ldp_auto_config_area_id'):
                            configurations.append_line(attributes.format(
                                'mpls ldp autoconfig area {ldp_auto_config_area_id}'))

                        # router ospf 1
                        #   mpls ldp sync
                        if attributes.value('ldp_igp_sync'):
                            configurations.append_line(attributes.format('mpls ldp sync'))

                        # router ospf 1
                        #   redistribute bgp 100 route-map ottawa
                        if attributes.value('redist_bgp_id') and \
                            attributes.value('redist_bgp_route_map'):
                            configurations.append_line(attributes.format(
                                'redistribute bgp {redist_bgp_id} route-map {redist_bgp_route_map}'))

                        # router ospf 1
                        #   redistribute direct route-map toronto
                        if attributes.value('redist_connected') and \
                            attributes.value('redist_connected_route_policy'):
                            configurations.append_line(attributes.format(
                                'redistribute direct route-map {redist_connected_route_policy}'))

                        # router ospf 1
                        #   redistribute static route-map montreal
                        if attributes.value('redist_static') and \
                            attributes.value('redist_static_route_policy'):
                            configurations.append_line(attributes.format(
                                'redistribute static route-map {redist_static_route_policy}'))

                        # router ospf 1
                        #   redistribute isis ABC route-map nowhere
                        if attributes.value('redist_isis') and \
                            attributes.value('redist_isis_route_policy'):
                            configurations.append_line(attributes.format(
                                'redistribute isis {redist_isis} route-map {redist_isis_route_policy}'))

                        # router ospf 1
                        #   redistribute maximum-prefix 123 10 warning-only
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
                        #   bfd
                        if attributes.value('bfd_enable'):
                            configurations.append_line(attributes.format('bfd'))

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
                        #   auto-cost reference-bandwidth 60000
                        #   auto-cost reference-bandwidth 60000 mbps
                        #   auto-cost reference-bandwidth 60000 gbps
                        if attributes.value('auto_cost_enable') is False:
                            configurations.append_line(attributes.format('no auto-cost reference-bandwidth'))
                        elif attributes.value('auto_cost_enable') is True and \
                            attributes.value('auto_cost_reference_bandwidth'):

                            # auto-cost reference-bandwidth {auto_cost_reference_bandwidth}
                            auto_cost_str = 'auto-cost reference-bandwidth {auto_cost_reference_bandwidth}'

                            # + {auto_cost_bandwidth_unit}
                            if attributes.value('auto_cost_bandwidth_unit'):
                                unit = attributes.value('auto_cost_bandwidth_unit').value
                                auto_cost_str += ' {}'.format(unit)

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
                    #   mpls traffic-eng area 2
                    if attributes.value('area_te_enable') and self.vrf_name == 'default':
                        configurations.append_line(attributes.format('mpls traffic-eng area {area}'))

                    # router ospf 1
                    #   area 2 stub
                    #   area 2 nssa
                    #   area 2 stub no-summary
                    #   area 2 nssa no-summary
                    if attributes.value('area_type').value != 'normal':
                        # area 2 stub
                        # area 2 nssa
                        type_str = 'area {area}'
                        atype = attributes.value('area_type').value
                        type_str += ' {}'.format(atype)

                        # + no-summary
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
                        #  area 2 virtual-link 7.7.7.7
                        if attributes.value('vl_router_id') and \
                            attributes.value('area_type') != 'stub' and \
                            attributes.value('area_type') != 'nssa':
                            with configurations.submode_context(
                                attributes.format('area {area} virtual-link {vl_router_id}', force=True)):

                                if unconfig and attributes.iswildcard:
                                    configurations.submode_unconfig()

                                # router ospf 1
                                #  area 2 virtual-link 7.7.7.7
                                #    hello-interval 55
                                if attributes.value('vl_hello_interval'):
                                    configurations.append_line(attributes.format('hello-interval {vl_hello_interval}'))

                                # router ospf 1
                                #  area 2 virtual-link 7.7.7.7
                                #    dead-interval 55
                                if attributes.value('vl_dead_interval'):
                                    configurations.append_line(attributes.format('dead-interval {vl_dead_interval}'))

                                # router ospf 1
                                #  area 2 virtual-link 7.7.7.7
                                #   retransmit-interval 55
                                if attributes.value('vl_retransmit_interval'):
                                    configurations.append_line(attributes.format('retransmit-interval {vl_retransmit_interval}'))

                                # router ospf 1
                                #  area 2 virtual-link 7.7.7.7
                                #   transmit-delay 55
                                if attributes.value('vl_transmit_delay'):
                                    configurations.append_line(attributes.format('transmit-delay {vl_transmit_delay}'))

                                # router ospf 1
                                #  area 2 virtual-link 7.7.7.7
                                #   authentication key-chain "ottawa"
                                if attributes.value('vl_auth_trailer_key_chain'):
                                    configurations.append_line(attributes.format('authentication key-chain {vl_auth_trailer_key_chain}'))

                                # router ospf 1
                                #  area 2 virtual-link 7.7.7.7
                                #   authentication
                                #   authentication-key anything
                                #   authentication message-digest
                                #   message-digest-key 1 md5 anything
                                if attributes.value('vl_auth_trailer_key_crypto_algorithm'):

                                    auth_type = attributes.value('vl_auth_trailer_key_crypto_algorithm').value

                                    # area 2 virtual-link 7.7.7.7 authentication
                                    if auth_type == 'simple':
                                        configurations.append_line(attributes.format('authentication'))

                                        # area 2 virtual-link 7.7.7.7 authentication-key anything
                                        if attributes.value('vl_auth_trailer_key'):
                                            configurations.append_line(attributes.format('authentication-key {vl_auth_trailer_key}'))

                                    # area 2 virtual-link 7.7.7.7 authentication message-digest
                                    elif auth_type == 'md5':
                                        configurations.append_line(attributes.format('authentication message-digest'))

                                        # area 2 virtual-link 7.7.7.7 message-digest-key 1 md5 anything
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
                        #  area 2 sham-link 1.1.1.1 2.2.2.2
                        if self.vrf_name != 'default' and attributes.value('sl_local_id') and attributes.value('sl_remote_id'):
                            with configurations.submode_context(
                                attributes.format('area {area} sham-link {sl_local_id} {sl_remote_id}', force=True)):

                                if unconfig and attributes.iswildcard:
                                    configurations.submode_unconfig()

                                # router ospf 1
                                #  area 2 sham-link 1.1.1.1 2.2.2.2
                                #    hello-interval 55
                                if attributes.value('sl_hello_interval'):
                                    configurations.append_line(attributes.format('hello-interval {sl_hello_interval}'))

                                # router ospf 1
                                #  area 2 sham-link 1.1.1.1 2.2.2.2
                                #    dead-interval 55
                                if attributes.value('sl_dead_interval'):
                                    configurations.append_line(attributes.format('dead-interval {sl_dead_interval}'))

                                # router ospf 1
                                #  area 2 sham-link 1.1.1.1 2.2.2.2
                                #   retransmit-interval 55
                                if attributes.value('sl_retransmit_interval'):
                                    configurations.append_line(attributes.format('retransmit-interval {sl_retransmit_interval}'))

                                # router ospf 1
                                #  area 2 sham-link 1.1.1.1 2.2.2.2
                                #   transmit-delay 55
                                if attributes.value('sl_transmit_delay'):
                                    configurations.append_line(attributes.format('transmit-delay {sl_transmit_delay}'))

                                # router ospf 1
                                #  area 2 sham-link 1.1.1.1 2.2.2.2
                                #   authentication key-chain "ottawa"
                                if attributes.value('sl_auth_trailer_key_chain'):
                                    configurations.append_line(attributes.format('authentication key-chain {sl_auth_trailer_key_chain}'))

                                # router ospf 1
                                #  area 2 sham-link 1.1.1.1 2.2.2.2
                                #   authentication
                                #   authentication-key anything
                                #   authentication message-digest
                                #   message-digest-key 1 md5 anything
                                if attributes.value('sl_auth_trailer_key_crypto_algorithm'):

                                    auth_type = attributes.value('sl_auth_trailer_key_crypto_algorithm').value

                                    # area 2 sham-link 7.7.7.7 authentication
                                    if auth_type == 'simple':
                                        configurations.append_line(attributes.format('authentication'))

                                        # area 2 sham-link 7.7.7.7 authentication-key anything
                                        if attributes.value('sl_auth_trailer_key'):
                                            configurations.append_line(attributes.format('authentication-key {sl_auth_trailer_key}'))

                                    # area 2 sham-link 7.7.7.7 authentication message-digest
                                    elif auth_type == 'md5':
                                        configurations.append_line(attributes.format('authentication message-digest'))

                                        # area 2 sham-link 7.7.7.7 message-digest-key 1 md5 anything
                                        if attributes.value('sl_auth_trailer_key'):
                                            configurations.append_line(attributes.format('message-digest-key 1 md5 {sl_auth_trailer_key}'))

                                # router ospf 1
                                #  area 2 sham-link 1.1.1.1 2.2.2.2
                                #   cost 10
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

                        # interface GigabitEthernet1
                        with configurations.submode_context(
                            attributes.format('interface {interface_name}', force=True)):

                            # interface GigabitEthernet1
                            #   ip ospf 1 area 2
                            if attributes.value('if_admin_control'):
                                configurations.append_line(attributes.format('ip router ospf {instance} area {area}'))

                            # interface GigabitEthernet1
                            #   ip ospf cost 100
                            if attributes.value('if_cost'):
                                configurations.append_line(attributes.format('ip ospf cost {if_cost}'))

                            # interface GigabitEthernet1
                            #   ip ospf network point-to-point
                            if attributes.value('if_type'):
                                iftype = attributes.value('if_type').value
                                # Configure acceptable interface types
                                if iftype == 'broadcast' or iftype == 'point-to-point':
                                    configurations.append_line(attributes.format('ip ospf network {}'.format(iftype)))

                            # passive-interface GigabitEthernet1
                            if attributes.value('if_passive'):
                                configurations.append_line(attributes.format('ip ospf passive-interface'))

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

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)

