
# import python
from abc import ABC

# import genie
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning, \
                                       AttributesHelper


class Pim(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            cfg_line = []
            unconfig_line = []

            # enabled
            if attributes.value('enabled'):
                if unconfig is False:
                    configurations.append_line(attributes.format('feature pim'))
                    configurations.append_line(attributes.format('feature pim6'))

                # Make sure that only enabled was provided in attributes
                # If wildcard,  then delete everything
                elif unconfig is True and\
                     attributes.attributes == {'enabled': {True: None}} or \
                        attributes.iswildcard:
                    configurations.append_line('no feature pim', raw=True)
                    configurations.append_line('no feature pim6', raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            # enable_pim
            elif attributes.value('enabled_pim'):
                cfg_line.append('feature pim')
                unconfig_line.append('no feature pim')

            # enable_pim6
            elif attributes.value('enabled_pim6'):
                cfg_line.append('feature pim6')
                unconfig_line.append('no feature pim6')

            if cfg_line:
                if unconfig is False:
                    configurations.append_line('\n'.join(cfg_line))
                elif unconfig is True:
                    configurations.append_line('\n'.join(unconfig_line), raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            # VrfAttributes
            for sub, attributes2 in attributes.mapping_values('vrf_attr',
                sort=True, keys=self.vrf_attr):
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

        class VrfAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # address_family
                for address_family_sub, address_family_attributes in \
                    attributes.mapping_values(
                        'address_family_attr', sort=True,
                        keys = self.address_family_attr):
                    configurations.append_block(
                        address_family_sub.build_config(apply=False,
                            attributes=address_family_attributes,
                            unconfig=unconfig))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

            class AddressFamilyAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    assert not apply
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)
                    # assign ip version according to the address_family_attr
                    if hasattr(self, 'address_family'):
                        if 'ipv4' in self.address_family.value:
                            self.ip = 'ip'
                        if 'ipv6' in self.address_family.value:
                            self.ip = 'ipv6'

                    if unconfig:
                        attributes.attributes['ip'] = self.ip
                        
                    with configurations.submode_context(
                            None if self.vrf_name == 'default' else
                                attributes.format(
                                    'vrf context {vrf_name}', force=True)):
                        # no configuration append if vrf is default
                        if self.vrf_name != 'default' and unconfig and \
                            attributes.iswildcard:
                            configurations.submode_unconfig()

                        # ==== PIM Auto-RP =======
                        if attributes.value('auto_rp') or \
                           attributes.value('send_rp'):

                            # auto-rp rp-candidate | send-rp-announce
                            if attributes.value('auto_rp'):
                               auto_rp_str = 'ip pim auto-rp rp-candidate'
                            elif attributes.value('send_rp'):
                                auto_rp_str = 'ip pim send-rp-announce'

                            # + {send_rp_announce_rp_group} |
                            # + {send_rp_announce_intf}
                            if attributes.value('send_rp_announce_rp_group'):
                               auto_rp_str += ' {send_rp_announce_rp_group}'
                            elif attributes.value('send_rp_announce_intf'):
                                auto_rp_str += ' {send_rp_announce_intf}'
                            else:
                                auto_rp_str = ''

                            # + group-list {send_rp_announce_group_list} |
                            # + route-map {send_rp_announce_route_map} |
                            # + prefix-list {send_rp_announce_prefix_list}
                            if auto_rp_str:
                                if attributes.value('send_rp_announce_group_list'):
                                    auto_rp_str += ' group-list'\
                                                   ' {send_rp_announce_group_list}'
                                elif attributes.value('send_rp_announce_route_map'):
                                    auto_rp_str += ' route-map'\
                                                   ' {send_rp_announce_route_map}'
                                elif attributes.value('send_rp_announce_prefix_list'):
                                    auto_rp_str += ' prefix-list'\
                                                   ' {send_rp_announce_prefix_list}'
                                else:
                                    auto_rp_str = ''

                            if auto_rp_str:
                                # + interval {send_rp_announce_interval}
                                if attributes.value('send_rp_announce_interval'):
                                    auto_rp_str += ' interval'\
                                                   ' {send_rp_announce_interval}'

                                # + scope {send_rp_announce_scope}
                                if attributes.value('send_rp_announce_scope'):
                                    auto_rp_str += ' scope {send_rp_announce_scope}'

                                # + bidir
                                if attributes.value('send_rp_announce_bidir'):
                                    auto_rp_str += ' bidir'

                            configurations.append_line(
                                attributes.format(auto_rp_str))

                        # === PIM Send-RP-Discovery ===
                        # ip pim auto-rp mapping-agent|send-rp-discovery
                        #  <send_rp_discovery_intf>
                        #  [scope ,send_rp_discovery_scope>]
                        if attributes.value('auto_rp_discovery') or \
                           attributes.value('send_rp_discovery'):

                            # set auto-rp method
                            if attributes.value('auto_rp_discovery'):
                                pre_str = 'ip pim auto-rp mapping-agent'
                            if attributes.value('send_rp_discovery'):
                                pre_str = 'ip pim send-rp-discovery'

                            #  <send_rp_discovery_intf>
                            #  [scope ,send_rp_discovery_scope>]
                            if attributes.value('send_rp_discovery_intf') and \
                               attributes.value('send_rp_discovery_scope'):
                                pre_str +=' {send_rp_discovery_intf}'\
                                          ' scope {send_rp_discovery_scope}'

                            elif attributes.value('send_rp_discovery_intf') and \
                               not attributes.value('send_rp_discovery_scope'):
                                pre_str +=' {send_rp_discovery_intf}'

                            configurations.append_line(
                                attributes.format(pre_str))
                            # initial it back
                            pre_str = ''

                        # ip pim auto-rp forward listen
                        if attributes.value('autorp_listener'):
                            configurations.append_line(
                                attributes.format('ip pim auto-rp forward listen'))

                        # ==== PIM BSR =======
                        # == bsr bsr-candidate ==
                        # ip/ipv6 pim auto-rp forward listen
                        # ip/ipv6 pim [bsr] bsr-candidate <bsr_candidate_interface>
                        if attributes.value('bsr_candidate_interface'):
                            # ip/ipv6 pim bsr forward listen
                            configurations.append_line(
                                attributes.format('{ip} pim bsr forward listen'))

                            # ip/ipv6 pim bsr-candidate {bsr_candidate_interface}
                            bsr_str = '{ip} pim bsr-candidate '\
                                      '{bsr_candidate_interface}'

                            # + hash-len <bsr_candidate_hash_mask_length>
                            if attributes.value('bsr_candidate_hash_mask_length'):
                                bsr_str += ' hash-len '\
                                           '{bsr_candidate_hash_mask_length}'

                            # + interval <bsr_candidate_interval>
                            if attributes.value('bsr_candidate_interval'):
                                bsr_str += ' interval {bsr_candidate_interval}'

                            # + priority <bsr_candidate_priority>
                            if attributes.value('bsr_candidate_priority'):
                                bsr_str += ' priority {bsr_candidate_priority}'

                            configurations.append_line(
                                attributes.format(bsr_str))

                        # == bsr rp-candidate ==
                        # ip/ipv6 pim auto-rp forward listen
                        # ip/ipv6 pim [bsr] rp-candidate <bsr_rp_candidate_interface>
                        if attributes.value('bsr_rp_candidate_interface'):
                            # ip/ipv6 pim bsr forward listen
                            configurations.append_line(
                                attributes.format('{ip} pim bsr forward listen'))

                            # ip/ipv6 pim rp-candidate {bsr_rp_candidate_interface}
                            bsr_rp_str = '{ip} pim rp-candidate '\
                                      '{bsr_rp_candidate_interface}'

                            # + group-list {bsr_rp_candidate_group_list} |
                            # + route-map {bsr_rp_candidate_route_map} |
                            # + prefix-list {bsr_rp_candidate_prefix_list}
                            if attributes.value('bsr_rp_candidate_group_list'):
                                bsr_rp_str += ' group-list'\
                                               ' {bsr_rp_candidate_group_list}'
                            elif attributes.value('bsr_rp_candidate_route_map'):
                                bsr_rp_str += ' route-map'\
                                               ' {bsr_rp_candidate_route_map}'
                            elif attributes.value('bsr_rp_candidate_prefix_list'):
                                bsr_rp_str += ' prefix-list'\
                                               ' {bsr_rp_candidate_prefix_list}'
                            else:
                                bsr_rp_str = ''

                            if bsr_rp_str:
                                # +priority <bsr_rp_candidate_priority>
                                if attributes.value('bsr_rp_candidate_priority'):
                                    bsr_rp_str += ' priority '\
                                               '{bsr_rp_candidate_priority}'

                                # +interval <bsr_rp_candidate_interval>
                                if attributes.value('bsr_rp_candidate_interval'):
                                    bsr_rp_str += ' interval {bsr_rp_candidate_interval}'

                                # +bidir
                                if attributes.value('bsr_rp_candidate_bidir'):
                                    bsr_rp_str += ' bidir'

                            configurations.append_line(
                                attributes.format(bsr_rp_str))
                            
                        # ip/ipv6 pim register-policy <accept_register>
                        if attributes.value('accept_register'):
                            configurations.append_line(
                                attributes.format(
                                    '{ip} pim register-policy '
                                    '{accept_register}'))

                        # ip pim register-policy prefix-list
                        #   <accept_register_prefix_list>
                        if attributes.value('accept_register_prefix_list') \
                           and self.ip == 'ip':
                            configurations.append_line(
                                attributes.format(
                                    'ip pim register-policy prefix-list '
                                    '{accept_register_prefix_list}'))

                        # ip/ipv6 pim log-neighbor-changes
                        if attributes.value('log_neighbor_changes'):
                            configurations.append_line(
                                attributes.format(
                                    '{ip} pim log-neighbor-changes'))

                        # ip pim register-source <register_source>
                        if attributes.value('register_source') and \
                           self.ip == 'ip':
                            configurations.append_line(
                                attributes.format(
                                    'ip pim register-source {register_source}'))
                            
                        # ip pim sg-expiry-timer infinity
                        if attributes.value('sg_expiry_timer_infinity') and \
                           not attributes.value('sg_expiry_timer_prefix_list') \
                           and not attributes.value('sg_expiry_timer_sg_list'):
                            configurations.append_line(
                                attributes.format(
                                    'ip pim sg-expiry-timer infinity'))
                            
                        # ip pim sg-expiry-timer <sg_expiry_timer>
                        if attributes.value('sg_expiry_timer') and \
                           not attributes.value('sg_expiry_timer_prefix_list') \
                           and not attributes.value('sg_expiry_timer_sg_list'):
                            configurations.append_line(
                                attributes.format(
                                    'ip pim sg-expiry-timer {sg_expiry_timer}'))

                        # ip pim sg-expiry-timer <sg_expiry_timer>
                        #   prefix-list <sg_expiry_timer_prefix_list>
                        if attributes.value('sg_expiry_timer') and \
                           attributes.value('sg_expiry_timer_prefix_list'):
                            configurations.append_line(
                                attributes.format(
                                    'ip pim sg-expiry-timer {sg_expiry_timer} '
                                    'prefix-list {sg_expiry_timer_prefix_list}'))

                        # ip pim sg-expiry-timer <sg_expiry_timer>
                        #   sg-list <sg_expiry_timer_sg_list>
                        if attributes.value('sg_expiry_timer') and \
                           attributes.value('sg_expiry_timer_sg_list'):
                            configurations.append_line(
                                attributes.format(
                                    'ip pim sg-expiry-timer {sg_expiry_timer} '
                                    'sg-list {sg_expiry_timer_sg_list}'))

                        # ip pim sg-expiry-timer infinity
                        #   prefix-list <sg_expiry_timer_prefix_list>
                        if attributes.value('sg_expiry_timer_infinity') and \
                           attributes.value('sg_expiry_timer_prefix_list'):
                            configurations.append_line(
                                attributes.format(
                                    'ip pim sg-expiry-timer infinity '
                                    'prefix-list {sg_expiry_timer_prefix_list}'))
                            
                        # ip pim sg-expiry-timer infinity
                        #   sg-list <sg_expiry_timer_sg_list>
                        if attributes.value('sg_expiry_timer_infinity') and \
                           attributes.value('sg_expiry_timer_sg_list'):
                            configurations.append_line(
                                attributes.format(
                                    'ip pim sg-expiry-timer infinity '
                                    'sg-list {sg_expiry_timer_sg_list}'))

                        # ip/ipv6 pim spt-threshold infinity group-list
                        #   <spt_switch_policy>
                        if attributes.value('spt_switch_infinity') and \
                           attributes.value('spt_switch_policy'):
                            configurations.append_line(
                                attributes.format(
                                    '{ip} pim spt-threshold {spt_switch_infinity.value} '
                                    'group-list {spt_switch_policy}'))

                        # ip/ipv6 pim use-shared-tree-only group-list <spt_switch_policy>
                        if not attributes.value('spt_switch_infinity') and \
                           attributes.value('spt_switch_policy'):
                            configurations.append_line(
                                attributes.format(
                                    '{ip} pim use-shared-tree-only group-list'
                                    ' {spt_switch_policy}'))

                        # Static RP address Attributes under top level config
                        for groups, attributes2 in attributes.sequence_values(
                                'rp_addresses', sort=True):
                            kwargs = {'ip_type': self.ip}
                            if unconfig:
                                configurations.append_block(groups.build_unconfig(
                                    apply=False, attributes=attributes2, **kwargs))
                            else:
                                configurations.append_block(groups.build_config(
                                    apply=False, attributes=attributes2, **kwargs))

                    # InterfaceAttributes
                    for sub, attributes2 in attributes.mapping_values(
                        'interface_attr', keys=self.interface_attr,
                        sort=True):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))
                    
                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None,
                                   **kwargs):
                    return self.build_config(apply=apply,
                                             attributes=attributes,
                                             unconfig=True, **kwargs)

                class InterfaceAttributes(ABC):

                    def build_config(self, apply=True, attributes=None,
                                     unconfig=False, **kwargs):
                        assert not apply
                        assert not kwargs, kwargs
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # if self.vrf_name != 'default':
                        #     configurations.append_line('exit')

                        # the interface should have vrf(name = vrf_name) attached
                        with configurations.submode_context(
                            attributes.format('interface {interface_name}',
                                              force=True)):
                            if unconfig and attributes.iswildcard:
                                configurations.submode_unconfig()
                            if unconfig:
                                attributes.attributes['ip'] = self.ip

                            # interface <intf_name>
                            # ip/ipv6 pim sparse-mode
                            if attributes.value('mode'):
                                configurations.append_line(
                                    attributes.format('{ip} pim sparse-mode'))

                            # interface <intf_name>
                            # ip/ipv6 pim jp-policy <boundary> [in|out]
                            if attributes.value('boundary') and \
                               attributes.value('boundary_in') and \
                               attributes.value('boundary_out'):
                                configurations.append_line(
                                    attributes.format(
                                        '{ip} pim jp-policy {boundary} in'))
                                configurations.append_line(
                                    attributes.format(
                                         '{ip} pim jp-policy {boundary} out'))
                            elif attributes.value('boundary') and \
                               attributes.value('boundary_in') and \
                               not attributes.value('boundary_out'):
                                configurations.append_line(
                                    attributes.format(
                                        '{ip} pim jp-policy {boundary} in'))
                            elif attributes.value('boundary') and \
                               not attributes.value('boundary_in') and \
                               attributes.value('boundary_out'):
                                configurations.append_line(
                                    attributes.format(
                                        '{ip} pim jp-policy {boundary} out'))
                            elif attributes.value('boundary') and \
                               not attributes.value('boundary_in') and \
                               not attributes.value('boundary_out'):
                                configurations.append_line(
                                    attributes.format(
                                        '{ip} pim jp-policy {boundary}'))

                            # interface <intf_name>
                            # ip/ipv6 pim border
                            if attributes.value('bsr_border'):
                                configurations.append_line(
                                    attributes.format('{ip} pim border'))

                            # interface <intf_name>
                            # ip/ipv6 pim hello-interval {hello_interval}
                            if attributes.value('hello_interval'):
                                configurations.append_line(
                                    attributes.format(
                                        '{ip} pim hello-interval '
                                        '{hello_interval}'))

                            # interface <intf_name>
                            # ip/ipv6 pim dr-priority {dr_priority}
                            if attributes.value('dr_priority'):
                                configurations.append_line(
                                    attributes.format(
                                        '{ip} pim dr-priority '
                                        '{dr_priority}'))

                            # interface <intf_name>
                            # ip/ipv6 pim neighbor-policy {neighbor_filter}
                            if attributes.value('neighbor_filter'):
                                configurations.append_line(
                                    attributes.format(
                                        '{ip} pim neighbor-policy '
                                        '{neighbor_filter}'))

                            # interface <intf_name>
                            # ip/ipv6 pim neighbor-policy prefix-list
                            #   <neighbor_filter_prefix_list>
                            if attributes.value('neighbor_filter_prefix_list') \
                               and self.ip == 'ip':
                                configurations.append_line(
                                    attributes.format(
                                        'ip pim neighbor-policy prefix-list '
                                        '{neighbor_filter_prefix_list}'))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None,
                                       **kwargs):
                        return self.build_config(apply=apply,
                                                 attributes=attributes,
                                                 unconfig=True, **kwargs)

