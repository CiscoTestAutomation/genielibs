'''
OSPFv3 Genie Conf Object Implementation for NXOS - CLI.
'''

# Python
from abc import ABC

# Genie
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig
from genie.libs.conf.address_family import AddressFamily

# OSPFv3 Hierarchy
# --------------
# Ospfv3
#     +- DeviceAttributes
#         +- VrfAttributes
#             +- AddressFamilyAttributes
#             +- AreaAttributes
#                 +- InterfaceAttributes
#                 +- VirtualLinkAttributes


class Ospfv3(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            # Seperate CliConfigBuilder for InterfaceAttribute configuration
            self.interface_config = CliConfigBuilder(unconfig=unconfig)

            # feature ospfv3
            if attributes.value('enabled'):
                if unconfig is False:
                    configurations.append_line(
                        attributes.format('feature ospfv3'))

                # Make sure that only enabled was provided in attributes
                # If wildcard,  then delete everything
                elif unconfig is True and\
                    attributes.attributes == {'enabled': {True: None}} or \
                        attributes.iswildcard:
                    configurations.append_line('no feature ospfv3', raw=True)
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

        class VrfAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                        attributes.format('router ospfv3 {instance}', force=True)):

                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    with configurations.submode_context(
                        None if self.vrf_name == 'default' else
                            attributes.format('vrf {vrf_name}', force=True)):
                        if self.vrf_name != 'default' and unconfig and \
                                attributes.iswildcard:
                            configurations.submode_unconfig()
                        # router ospfv3 1
                        #   vrf <default/someword>
                        #     router-id 1.1.1.1
                        if attributes.value('router_id'):
                            configurations.append_line(
                                attributes.format('router-id {router_id}'))

                        # router ospfv3 1
                        #   vrf <default/someword>
                        #     shutdown
                        if attributes.value('inst_shutdown'):
                            configurations.append_line(
                                attributes.format('shutdown'))

                        # router ospfv3 1
                        #   vrf <default/someword>
                        #     passive-interface default
                        if attributes.value('passive_interface'):
                            configurations.append_line(
                                attributes.format('passive-interface default'))

                        # router ospfv3 1
                        #   log-adjacency-changes
                        #   log-adjacency-changes detail
                        if attributes.value('log_adjacency_changes'):

                            # log-adjacency-changes
                            log_str = 'log-adjacency-changes'

                            # + detail
                            if attributes.value('log_adjacency_changes_detail'):
                                log_str += ' detail'

                            configurations.append_line(
                                attributes.format(log_str))

                        # router ospfv3 1
                        #   bfd
                        if attributes.value('bfd_enable'):
                            configurations.append_line(
                                attributes.format('bfd'))

                        # timers lsa-arrival msec
                        if attributes.value('lsa_arrival'):
                            configurations.append_line(attributes.format(
                                'timers lsa-arrival {lsa_arrival}'))

                        # timers lsa-group-pacing seconds
                        if attributes.value('lsa_group_pacing'):
                            configurations.append_line(attributes.format(
                                'timers lsa-group-pacing {lsa_group_pacing}'))

                        # timers throttle lsa start-time hold-interval max-time
                        if attributes.value('lsa_start_time') and attributes.value('lsa_hold_time') and attributes.value('lsa_max_time'):
                            configurations.append_line(attributes.format(
                                'timers throttle lsa {lsa_start_time} {lsa_hold_time} {lsa_max_time}'))

                        # GracefulRestart attributes config
                        for gr_key, attributes2 in attributes.sequence_values('gr_keys'):
                            if unconfig:
                                configurations.append_block(gr_key.build_unconfig(
                                    apply=False, attributes=attributes2, **kwargs))
                            else:
                                configurations.append_block(gr_key.build_config(
                                    apply=False, attributes=attributes2, **kwargs))

                        # +- DeviceAttributes
                        #   +- VrfAttributes
                        #     +- AddressFamilyAttributes
                        for sub, attributes2 in attributes.mapping_values('address_family_attr',
                                                                          sort=True,
                                                                          keys=self.address_family_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))

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

            class AddressFamilyAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    if attributes.value('address_family') is AddressFamily.ipv6_unicast:

                        with configurations.submode_context(
                            attributes.format('address-family '
                                              '{address_family.value}',
                                              force=True)):
                            if unconfig and attributes.iswildcard:
                                # Never reached!
                                configurations.submode_unconfig()

                            # router ospfv3 1
                            #   address-family ipv6 unicast
                            #     default-information originate [ always ] [ route-map map-name ]
                            if attributes.value('default_originate'):
                                cfg_str = 'default-information originate {default_originate}'

                                if attributes.value('default_originate_always'):
                                    cfg_str += ' always'
                                if attributes.value('default_originate_routemap'):
                                    cfg_str += ' route-map {default_originate_routemap}'

                                configurations.append_line(
                                    attributes.format(cfg_str))

                            # router ospfv3 1
                            #   address-family ipv6 unicast
                            #     default-metric <>
                            if attributes.value('default_metric'):
                                configurations.append_line(
                                    attributes.format('default-metric {default_metric}'))

                            #   redistribute bgp 100 route-map <str>
                            if attributes.value('redist_bgp_id') and \
                                    attributes.value('redist_bgp_route_map'):
                                configurations.append_line(attributes.format(
                                    'redistribute bgp {redist_bgp_id} route-map {redist_bgp_route_map}'))

                            #   redistribute direct route-map <str>
                            if attributes.value('redist_direct') and \
                                    attributes.value('redist_direct_route_map'):
                                configurations.append_line(attributes.format(
                                    'redistribute direct route-map {redist_direct_route_map}'))

                            #   redistribute static route-map <str>
                            if attributes.value('redist_static') and \
                                    attributes.value('redist_static_route_map'):
                                configurations.append_line(attributes.format(
                                    'redistribute static route-map {redist_static_route_map}'))

                            #   redistribute isis ABC route-map <str>
                            if attributes.value('redist_isis_id') and \
                                    attributes.value('redist_isis_route_map'):
                                configurations.append_line(attributes.format(
                                    'redistribute isis {redist_isis_id} route-map {redist_isis_route_map}'))

                            #   redistribute rip ABC route-map <str>
                            if attributes.value('redist_rip_id') and \
                                    attributes.value('redist_rip_route_map'):
                                configurations.append_line(attributes.format(
                                    'redistribute rip {redist_rip_id} route-map {redist_rip_route_map}'))

                            # router ospfv3 1
                            #   address-family ipv6 unicast
                            #     redistribute maximum-prefix <> [ threshold ] [ warning-only | withdraw [ num-retries timeout ]]--
                            if attributes.value('redist_max_prefix'):
                                cfg_str = 'redistribute maximum-prefix {redist_max_prefix}'

                                if attributes.value('redist_max_prefix_thld'):
                                    cfg_str += ' {redist_max_prefix_thld}'

                                if attributes.value('redist_max_prefix_warn_only'):
                                    cfg_str += ' warning-only'
                                elif attributes.value('redist_max_prefix_withdraw'):
                                    cfg_str += ' withdraw'
                                    if attributes.value('redist_max_prefix_retries') and \
                                            attributes.value('redist_max_prefix_retries_timeout'):
                                        cfg_str += ' {redist_max_prefix_retries} {redist_max_prefix_retries_timeout}'

                                configurations.append_line(
                                    attributes.format(cfg_str))

                            # router ospfv3 1
                            #   address-family ipv6 unicast
                            #     table-map <>
                            if attributes.value('table_map'):
                                configurations.append_line(
                                    attributes.format('table-map {table_map}'))

                            # timers throttle spf start-time hold-interval max-time
                            if attributes.value('spf_start_time') and \
                                attributes.value('spf_hold_time') and \
                                    attributes.value('spf_max_time'):
                                configurations.append_line(attributes.format(
                                    'timers throttle lsa {spf_start_time} {spf_hold_time} {spf_max_time}'))

                            # Area default cost attributes config
                            for areacost_key, attributes2 in attributes.sequence_values('areacost_keys', sort=True):
                                if unconfig:
                                    configurations.append_block(areacost_key.build_unconfig(
                                        apply=False, attributes=attributes2, **kwargs))
                                else:
                                    configurations.append_block(areacost_key.build_config(
                                        apply=False, attributes=attributes2, **kwargs))

                            # Area route map attributes config
                            for arearoutemap_key, attributes2 in attributes.sequence_values('arearoutemap_keys', sort=True):
                                if unconfig:
                                    configurations.append_block(arearoutemap_key.build_unconfig(
                                        apply=False, attributes=attributes2, **kwargs))
                                else:
                                    configurations.append_block(arearoutemap_key.build_config(
                                        apply=False, attributes=attributes2, **kwargs))

                            # SummaryAddress attributes config
                            for sumadd_key, attributes2 in attributes.sequence_values('sumadd_keys', sort=True):
                                if unconfig:
                                    configurations.append_block(sumadd_key.build_unconfig(
                                        apply=False, attributes=attributes2, **kwargs))
                                else:
                                    configurations.append_block(sumadd_key.build_config(
                                        apply=False, attributes=attributes2, **kwargs))

                            # AreaRange attributes config
                            for arearange_key, attributes2 in attributes.sequence_values('arearange_keys', sort=True):
                                if unconfig:
                                    configurations.append_block(arearange_key.build_unconfig(
                                        apply=False, attributes=attributes2, **kwargs))
                                else:
                                    configurations.append_block(arearange_key.build_config(
                                        apply=False, attributes=attributes2, **kwargs))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None,
                                   **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class AreaAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)
                    # router ospfv3 1
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
                        if attributes.value('nosummary'):
                            type_str += ' no-summary'

                        if atype == 'nssa':
                            # + no-redistribution
                            if attributes.value('nssa_no_redistribution'):
                                type_str += ' no-redistribution'

                            # + default-information-originate
                            if attributes.value('nssa_default_info_originate'):
                                type_str += ' default-information-originate'

                                # + route-map {map}
                                if attributes.value('nssa_route_map'):
                                    type_str += ' route-map {nssa_route_map}'

                        configurations.append_line(attributes.format(type_str))

                    if attributes.value('area_type').value == 'nssa' and \
                        (attributes.value('nssa_translate_always') or
                         attributes.value('nssa_translate_never') or
                         attributes.value('nssa_translate_suppressfa')):
                        # area 2 nssa [ translate type7 { always | never } [ suppress-fa ]]
                        type_str = 'area {area} nssa translate type7'

                        # + always
                        if attributes.value('nssa_translate_always'):
                            type_str += ' always'
                        # + never
                        elif attributes.value('nssa_translate_never'):
                            type_str += ' never'

                        # + suppress-fa
                        if attributes.value('nssa_translate_supressfa'):
                            type_str += ' suppress-fa'

                        configurations.append_line(attributes.format(type_str))

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
                    #       +- InterfaceAttributes
                    for sub, attributes2 in attributes.mapping_values('interface_attr',
                                                                      sort=True,
                                                                      keys=self.interface_attr):
                        self.interface_config.append_block(
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

                        # router ospfv3 1
                        #  area 2 virtual-link 7.7.7.7
                        if attributes.value('vl_router_id') and \
                                attributes.value('area_type').value != 'stub' and \
                                attributes.value('area_type').value != 'nssa':
                            with configurations.submode_context(
                                    attributes.format('area {area} virtual-link {vl_router_id}', force=True)):

                                if unconfig and attributes.iswildcard:
                                    configurations.submode_unconfig()

                                # router ospfv3 1
                                #  area 2 virtual-link 7.7.7.7
                                #    hello-interval 55
                                if attributes.value('vl_hello_interval'):
                                    configurations.append_line(attributes.format(
                                        'hello-interval {vl_hello_interval}'))

                                # router ospfv3 1
                                #  area 2 virtual-link 7.7.7.7
                                #    dead-interval 55
                                if attributes.value('vl_dead_interval'):
                                    configurations.append_line(attributes.format(
                                        'dead-interval {vl_dead_interval}'))

                                # router ospfv3 1
                                #  area 2 virtual-link 7.7.7.7
                                #   retransmit-interval 55
                                if attributes.value('vl_retransmit_interval'):
                                    configurations.append_line(attributes.format(
                                        'retransmit-interval {vl_retransmit_interval}'))

                                # router ospfv3 1
                                #  area 2 virtual-link 7.7.7.7
                                #   transmit-delay 55
                                if attributes.value('vl_transmit_delay'):
                                    configurations.append_line(attributes.format(
                                        'transmit-delay {vl_transmit_delay}'))
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

                        # interface Ethernet1/1
                        with configurations.submode_context(
                                attributes.format('interface {interface_name}', force=True)):

                            # interface Ethernet1/1
                            #   ipv6 router ospfv3 1 area 2 [secondaries none]
                            if attributes.value('if_admin_control'):
                                ospfv3_str = 'ipv6 router ospfv3 {instance} area {area}'

                                # + secondaries none
                                if attributes.value('if_secondaries_none'):
                                    ospfv3_str = ' secondaries none'
                                configurations.append_line(
                                    attributes.format(ospfv3_str))

                            # interface Ethernet1/1
                            #   ospfv3 cost 100
                            if attributes.value('if_cost'):
                                configurations.append_line(
                                    attributes.format('ospfv3 cost {if_cost}'))

                            # interface Ethernet1/1
                            #   ospfv3 network point-to-point
                            if attributes.value('if_type'):
                                iftype = attributes.value('if_type').value
                                # Configure acceptable interface types
                                if iftype == 'broadcast' or iftype == 'point-to-point':
                                    configurations.append_line(attributes.format(
                                        'ospfv3 network {}'.format(iftype)))

                            # interface Ethernet1/1
                            #   ospfv3 bfd
                            if attributes.value('if_bfd_enable'):
                                configurations.append_line(
                                    attributes.format('ospfv3 bfd'))

                            # pospfv3 passive-interface
                            if attributes.value('if_passive'):
                                configurations.append_line(
                                    attributes.format('ospfv3 passive-interface'))

                            # interface Ethernet1/1
                            #   ospfv3 priority100
                            if attributes.value('if_priority'):
                                configurations.append_line(attributes.format(
                                    'ospfv3 priority {if_priority}'))

                            # interface Ethernet1/1
                            #   ospfv3 hello-interval 10
                            if attributes.value('if_hello_interval'):
                                configurations.append_line(attributes.format(
                                    'ospfv3 hello-interval {if_hello_interval}'))

                            # interface Ethernet1/1
                            #   ospfv3 dead-interval 10
                            if attributes.value('if_dead_interval'):
                                configurations.append_line(attributes.format(
                                    'ospfv3 dead-interval {if_dead_interval}'))

                            # interface Ethernet1/1
                            #   ospfv3 retransmit-interval seconds
                            if attributes.value('if_retransmit_interval'):
                                configurations.append_line(attributes.format(
                                    'ospfv3 retransmit-interval {if_retransmit_interval}'))

                            # interface Ethernet1/1
                            #   ospfv3 mtu-ignore
                            if attributes.value('if_mtu_ignore'):
                                configurations.append_line(
                                    attributes.format('ospfv3 mtu-ignore'))

                            # interface Ethernet1/1
                            #   ospfv3 instance instance
                            if attributes.value('if_instance'):
                                configurations.append_line(
                                    attributes.format('ospfv3 instance {if_instance}'))

                            # interface Ethernet1/1
                            #   ospfv3 shutdown
                            if attributes.value('if_protocol_shutdown'):
                                configurations.append_line(
                                    attributes.format('ospfv3 shutdown'))

                            # interface Ethernet1/1
                            #   ospfv3 transmit-delay 10
                            if attributes.value('if_transmit_delay'):
                                configurations.append_line(attributes.format(
                                    'ospfv3 transmit-delay {if_transmit_delay}'))

                            # interface Ethernet1/1
                            #   ipv6 router ospfv3 instance-tag multi-area area-id
                            if attributes.value('if_multi_area'):
                                configurations.append_line(attributes.format(
                                    'ipv6 router ospfv3 {instance} multi-area {if_multi_area}'))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)
