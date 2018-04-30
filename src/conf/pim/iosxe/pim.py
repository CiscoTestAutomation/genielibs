
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
            
            # ip pim bidir-enable
            if attributes.value('enabled_bidir'):
                configurations.append_line(
                    attributes.format('ip pim bidir-enable'))

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

                    base_cfg = '{ip} pim'.format(ip=self.ip) if self.vrf_name == 'default' else \
                                '{ip} pim vrf {vrf}'.format(ip=self.ip, vrf=self.vrf_name)


                    skip_unconfig = False

                    if self.ip == 'ip':
                        # ==== PIM Auto-RP =======
                        # send-rp-announce { <send_rp_announce_intf> | <send_rp_announce_rp_group> }
                        if attributes.value('send_rp_announce_rp_group'):
                            auto_rp_str = ' send-rp-announce {send_rp_announce_rp_group}'
                        elif attributes.value('send_rp_announce_intf'):
                            auto_rp_str = ' send-rp-announce {send_rp_announce_intf}'
                        else:
                            auto_rp_str = ''

                        # + scope <send_rp_announce_scope>
                        if auto_rp_str and attributes.value('send_rp_announce_scope'):
                            auto_rp_str += ' scope {send_rp_announce_scope}'
                        else:
                            auto_rp_str = ''

                        # + group-list {send_rp_announce_group_list}
                        if auto_rp_str and attributes.value('send_rp_announce_group_list'):
                            if attributes.value('send_rp_announce_group_list'):
                                auto_rp_str += ' group-list'\
                                               ' {send_rp_announce_group_list}'

                        # + interval {send_rp_announce_interval}
                        if auto_rp_str and attributes.value('send_rp_announce_interval'):
                            if attributes.value('send_rp_announce_interval'):
                                auto_rp_str += ' interval'\
                                               ' {send_rp_announce_interval}'

                        # + bidir
                        if auto_rp_str and attributes.value('send_rp_announce_bidir'):
                            if unconfig and attributes.value('enabled_bidir'):
                                skip_unconfig = True
                            else:
                                auto_rp_str += ' bidir'
                                skip_unconfig = False

                        if auto_rp_str and not skip_unconfig:
                            configurations.append_line(
                                attributes.format(base_cfg + auto_rp_str))

                        # === PIM Send-RP-Discovery ===
                        # ip pim [ vrf <vrf_name> ]
                        # send-rp-discovery [ <send_rp_discovery_intf> ]
                        # scope <send_rp_discovery_scope>
                        # [ interval <send_rp_discovery_interval> ]

                        #  <send_rp_discovery_intf>
                        #  [scope ,send_rp_discovery_scope>]
                        if not attributes.value('send_rp_discovery_intf') and \
                           attributes.value('send_rp_discovery_scope'):
                            pre_str = ' send-rp-discovery'\
                                      ' scope {send_rp_discovery_scope}'
                        elif attributes.value('send_rp_discovery_intf') and \
                           attributes.value('send_rp_discovery_scope'):
                            pre_str = ' send-rp-discovery {send_rp_discovery_intf}'\
                                       ' scope {send_rp_discovery_scope}'
                        else:
                            pre_str = ''

                        if pre_str and attributes.value('send_rp_discovery_scope'):
                            pre_str += ' interval {send_rp_discovery_interval}'


                        if pre_str:
                            configurations.append_line(
                                attributes.format(base_cfg + pre_str))

                        # ip pim autorp listener
                        if attributes.value('autorp_listener'):
                            configurations.append_line(
                                attributes.format('ip pim autorp listener'))

                    # ==== PIM BSR =======
                    # == bsr bsr-candidate ==
                    # ip/ipv6 pim [ vrf  <vrf_name>] bsr-candidate <bsr_candidate_interface>
                    if attributes.value('bsr_candidate_interface'):

                        # ip/ipv6 pim bsr-candidate {bsr_candidate_interface}
                        bsr_str = ' bsr-candidate '\
                                  '{bsr_candidate_interface}' if self.ip == 'ip' else \
                                  '  bsr candidate bsr'\
                                  '{bsr_candidate_interface}'

                        # + <bsr_candidate_hash_mask_length>
                        if attributes.value('bsr_candidate_hash_mask_length'):
                            bsr_str += ' {bsr_candidate_hash_mask_length}'

                        # + priority <bsr_candidate_priority> | 
                        # <bsr_candidate_priority>
                        if attributes.value('bsr_candidate_priority'):
                            bsr_str += ' priority {bsr_candidate_priority}' if \
                                       self.ip == 'ipv6' else \
                                       ' {bsr_candidate_priority}'

                        # + [scope]  -- only for ipv6 pim
                        if attributes.value('scope') and self.ip == 'ipv6':
                            bsr_str += ' scope'

                        # + accept-rp-candidate <bsr_candidate_accept_rp_acl>
                        if attributes.value('bsr_candidate_accept_rp_acl'):
                            bsr_str += ' accept-rp-candidate {bsr_candidate_accept_rp_acl}'

                        configurations.append_line(
                            attributes.format(base_cfg + bsr_str))

                    # == bsr rp-candidate ==
                    # ip pim rp-candidate <bsr_rp_candidate_interface>
                    if attributes.value('bsr_rp_candidate_interface') and self.ip == 'ip':
                        # ip pim rp-candidate {bsr_rp_candidate_interface}
                        bsr_rp_str = ' rp-candidate '\
                                  '{bsr_rp_candidate_interface}'

                        # + group-list {bsr_rp_candidate_group_list}
                        if attributes.value('bsr_rp_candidate_group_list'):
                            bsr_rp_str += ' group-list'\
                                           ' {bsr_rp_candidate_group_list}'

                        # +interval <bsr_rp_candidate_interval>
                        if attributes.value('bsr_rp_candidate_interval'):
                            bsr_rp_str += ' interval {bsr_rp_candidate_interval}'

                        # +priority <bsr_rp_candidate_priority>
                        if attributes.value('bsr_rp_candidate_priority'):
                            bsr_rp_str += ' priority '\
                                       '{bsr_rp_candidate_priority}'

                        # +bidir
                        if attributes.value('bsr_rp_candidate_bidir'):
                            if unconfig and attributes.value('enabled_bidir'):
                                skip_unconfig = True
                            else:
                                bsr_rp_str += ' bidir'
                                skip_unconfig = False

                        if not skip_unconfig:
                            configurations.append_line(
                                attributes.format(base_cfg + bsr_rp_str))

                    elif attributes.value('bsr_rp_candidate_address') and self.ip == 'ipv6':
                        # ipv6 pim [ vrf <vrf_name> ]  bsr candidate rp <bsr_rp_candidate_address> 
                        bsr_rp_str = ' bsr candidate rp '\
                                  '{bsr_rp_candidate_address}'

                        # + group-list {bsr_rp_candidate_group_list}
                        if attributes.value('bsr_rp_candidate_group_list'):
                            bsr_rp_str += ' group-list'\
                                           ' {bsr_rp_candidate_group_list}'

                        # +interval <bsr_rp_candidate_interval>
                        if attributes.value('bsr_rp_candidate_interval'):
                            bsr_rp_str += ' interval {bsr_rp_candidate_interval}'

                        # +priority <bsr_rp_candidate_priority>
                        if attributes.value('bsr_rp_candidate_priority'):
                            bsr_rp_str += ' priority '\
                                       '{bsr_rp_candidate_priority}'

                        # +bidir
                        if attributes.value('bsr_rp_candidate_bidir'):
                            if unconfig and attributes.value('enabled_bidir'):
                                skip_unconfig = True
                            else:
                                bsr_rp_str += ' bidir'
                                skip_unconfig = False

                        if not skip_unconfig:
                            configurations.append_line(
                                attributes.format(base_cfg + bsr_rp_str))
                        
                    # ip/ipv6 pim register-policy list <accept_register>
                    if attributes.value('accept_register'):
                        if self.ip == 'ip':
                            configurations.append_line(
                                attributes.format('ip pim accept-register list '
                                    '{accept_register}', force=True))
                        else:
                            configurations.append_line(
                                attributes.format(base_cfg + ' accept-register list '
                                    '{accept_register}', force=True))

                    # ip pim log-neighbor-changes
                    if attributes.value('log_neighbor_changes') and self.ip == 'ip':
                        configurations.append_line(
                            attributes.format(
                                'ip pim log-neighbor-changes'))

                    # ip/ipv6 pim [vrf <vrf_name>] register-source <register_source>
                    if attributes.value('register_source'):
                        configurations.append_line(
                            attributes.format(base_cfg +
                                ' register-source {register_source}'))
                                                
                    # ip pim [ vrf <vrf_name> ] sparse sg-expiry-timer <sg_expiry_timer>
                    if attributes.value('sg_expiry_timer') and self.ip == 'ip':
                        sg_cfg = ' sparse sg-expiry-timer {sg_expiry_timer}'

                        if attributes.value('sg_expiry_timer_sg_list'):
                            sg_cfg += ' sg-list {sg_expiry_timer_sg_list}'
                        configurations.append_line(
                            attributes.format(base_cfg + sg_cfg))

                    # ip/ipv6 pim spt-threshold infinity group-list
                    #   <spt_switch_policy>
                    if attributes.value('spt_switch_infinity') and \
                       attributes.value('spt_switch_policy'):
                        configurations.append_line(
                            attributes.format(base_cfg + 
                                ' spt-threshold {spt_switch_infinity.value} '
                                'group-list {spt_switch_policy}'))
                    elif attributes.value('spt_switch_infinity') and \
                       not attributes.value('spt_switch_policy'):
                        configurations.append_line(
                            attributes.format(base_cfg + 
                                ' spt-threshold {spt_switch_infinity.value}'))

                    # Static RP address Attributes under top level config
                    for groups, attributes2 in attributes.sequence_values(
                            'rp_addresses', sort=True):
                        kwargs = {'ip_type': self.ip,
                                  'vrf': self.vrf_name,
                                  'bidir': attributes.value('enabled_bidir')}
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

                        # the interface should have vrf(name = vrf_name) attached
                        with configurations.submode_context(
                            attributes.format('interface {interface_name}',
                                              force=True)):

                            # avoid the force = True for every config line
                            # assign the 'ip' attribute when unconfig 
                            if unconfig and attributes.attributes:
                                attributes.attributes['ip'] = self.ip

                            # interface <intf_name>
                            # ip/ipv6 pim sparse-mode
                            if attributes.value('mode'):
                                configurations.append_line(
                                    attributes.format('{ip} pim {mode.value}'))

                            # interface <intf_name>
                            # ip multicast <boundary> [filter-autorp] [in|out]
                            if attributes.value('boundary') and self.ip == 'ip':
                                cfg_str = 'ip multicast boundary {boundary}'

                                if attributes.value('boundary_in'):
                                    cfg_str += ' in'
                                elif attributes.value('boundary_out'):
                                    cfg_str += ' out'
                                elif attributes.value('boundary_filter_autorp'):
                                    cfg_str += ' filter-autorp'

                                configurations.append_line(
                                    attributes.format(cfg_str))
                            if attributes.value('boundary') and self.ip == 'ipv6':
                                configurations.append_line(
                                    attributes.format('ipv6 multicast boundary block source'))

                            # interface <intf_name>
                            # ip/ipv6 pim bsr border
                            if attributes.value('bsr_border'):
                                if self.ip == 'ip':
                                    configurations.append_line(
                                        attributes.format('{ip} pim bsr-border'))
                                else:                                    
                                    configurations.append_line(
                                        attributes.format('{ip} pim bsr border'))

                            # interface <intf_name>
                            # ip/ipv6 pim dr-priority {dr_priority}
                            if attributes.value('dr_priority'):
                                configurations.append_line(
                                    attributes.format(
                                        '{ip} pim dr-priority '
                                        '{dr_priority}'))

                            if self.ip == 'ip':
                                # interface <intf_name>
                                # ip pim query-interval <hello_interval> [msec]
                                if attributes.value('hello_interval'):
                                    configurations.append_line(
                                        attributes.format(
                                            'ip pim query-interval '
                                            '{hello_interval}'))
                                elif attributes.value('hello_interval_msec'):
                                    configurations.append_line(
                                        attributes.format(
                                            'ip pim query-interval '
                                            '{hello_interval_msec} msec'))

                                # interface <intf_name>
                                # ip pim neighbor-filter <neighbor_filter>
                                if attributes.value('neighbor_filter'):
                                    configurations.append_line(
                                        attributes.format(
                                            'ip pim neighbor-filter '
                                            '{neighbor_filter}'))
                            else:
                                # interface <intf_name>
                                #  ipv6 pim hello-interval <hello_interval>
                                if attributes.value('hello_interval'):
                                    configurations.append_line(
                                        attributes.format(
                                            'ipv6 pim hello-interval '
                                            '{hello_interval}'))

                        # interface <intf_name>
                        # ipv6 pim [ vrf <vrf_name> ]  neighbor-filter list <neighbor_filter>
                        # this is done in config)# mode, not under interface for IPV6
                        if attributes.value('neighbor_filter') and self.ip == 'ipv6':
                            cfg_str = 'ipv6 pim' if self.vrf_name == 'default' else \
                                      'ipv6 pim vrf {vrf}'.format(vrf=self.vrf_name)
                            configurations.append_line(
                                attributes.format(cfg_str + 
                                    ' neighbor-filter list '
                                    '{neighbor_filter}'))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None,
                                       **kwargs):
                        return self.build_config(apply=apply,
                                                 attributes=attributes,
                                                 unconfig=True, **kwargs)

