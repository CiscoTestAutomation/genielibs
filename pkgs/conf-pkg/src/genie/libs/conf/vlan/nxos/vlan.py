"""Implement Nexus (nxos) Specific Configurations for Vlan objects."""

# Table of contents:
#     class Vlan:
#         class DeviceAttributes:
#             class AccessMapAttributes:
#             class VlanConfigurationAttributes:
#             class InterfaceAttributes:

# Python
from abc import ABC

# Genie package
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base import Interface
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder


class Vlan(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # enabled
            if attributes.value('enabled'):
                configurations.append_line(attributes.format(
                                            'feature interface-vlan'))
                configurations.append_line(attributes.format(
                                        'feature vn-segment-vlan-based'))

            # enabled_interface_vlan
            elif attributes.value('enabled_interface_vlan'):
                configurations.append_line('feature interface-vlan')
            
            # enabled_vn_segment_vlan_based
            elif attributes.value('enabled_vn_segment_vlan_based'):
                configurations.append_line('feature vn-segment-vlan-based')

            # nxos: vlan 1000 (config-vlan)
            with configurations.submode_context(
                    attributes.format('vlan {vlan_id}', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # nxos: vlan 1000 / media enet
                configurations.append_line(
                    attributes.format('media {media.value}'))

                # nxos: vlan 1000 / name vlan1000
                configurations.append_line(attributes.format('name {name}'))

                # nxos: vlan 1000 / shutdown
                # nxos: vlan 1000 / no shutdown
                v = attributes.value('shutdown')
                if v is not None:
                    if v:
                        configurations.append_line('shutdown', unconfig_cmd='no shutdown')
                    else:
                        configurations.append_line('no shutdown', unconfig_cmd='shutdown')

                # nxos: vlan 1000 / remote-span
                if attributes.value('remote_span'):
                    configurations.append_line(
                        attributes.format('remote-span'))

                # nxos: vlan 1000 / state active
                # nxos: vlan 1000 / state suspend
                configurations.append_line(
                    attributes.format('state {status.value}'))

                # nxos: vlan 1000 / vn-segment 4096
                if attributes.value('vn_segment_id'):
                    configurations.append_line(
                        attributes.format('vn-segment {vn_segment_id}'))

            # nxos: vlan dot1q tag native
            # nxos: vlan dot1q tag native exclude control
            # nxos: vlan dot1q tag native fabricpath
            # nxos: vlan dot1q tag native fabricpath exclude control
            if attributes.value('dot1q_tag_native'):
                configurations.append_line(
                    attributes.format('vlan dot1q tag native'))

            # nxos: vlan configuration <Vlan id list>
            configurations.append_line(
                attributes.format('vlan configuration'
                                  ' {configuration_id_list}'))

            # nxos: vlan filter <list name> <list of vlans>

            for sub, attributes2 in attributes.mapping_values(
                    'access_map_attr',
                    keys=self.access_map_attr):
                configurations.append_block(
                    sub.build_config(apply=False, attributes=attributes2,
                                     unconfig=unconfig, **kwargs))

            for sub, attributes2 in attributes.mapping_values(
                        'vlan_configuration_attr',
                        keys=self.vlan_configuration_attr):
                configurations.append_block(
                    sub.build_config(apply=False, attributes=attributes2,
                                     unconfig=unconfig, **kwargs))

            for sub, attributes2 in attributes.mapping_values(
                    'interface_attr',
                    keys=self.interface_attr):
                configurations.append_block(
                    sub.build_config(apply=False, attributes=attributes2,
                                     unconfig=unconfig, **kwargs))

            # new vlan structure for all vlans
            for sub, attributes2 in attributes.mapping_values(
                    'vlan_attr', keys=self.vlan_attr):
                configurations.append_block(sub.build_config(apply=False,
                                                             attributes=attributes2,
                                                             unconfig=unconfig,
                                                             **kwargs))

            # new vlan structure for vlan_configs
            for sub, attributes2 in attributes.mapping_values(
                    'config_vlan_attr', keys=self.config_vlan_attr.keys()):
                configurations.append_block(sub.build_config(apply=False,
                                                             attributes=attributes2,
                                                             unconfig=unconfig,
                                                             **kwargs))

            if apply:
                if configurations:
                    self.device.configure(str(configurations),
                                          fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        class AccessMapAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)
                    with configurations.submode_context(
                        attributes.format('vlan access-map {access_map_id}',
                                          force=True)):
                        if unconfig and attributes.iswildcard:
                            # Never reached!
                            configurations.submode_unconfig()

                        # No point of configuring access_map_sequence
                        # nxos: vlan access-map <access_map_id> \
                        # <access_map_sequence>
                        # A workaround that needs to be better handled
                        if attributes.value('access_map_sequence'):
                            configurations.append_line(
                                attributes.format(
                                    'no vlan access-map {access_map_id}'))
                            configurations.append_line(
                                attributes.format(
                                    'vlan access-map {access_map_id} '
                                    '{access_map_sequence}'))

                        # nxos: vlan access-map <access_map_id> / action drop
                        # nxos: vlan access-map <access_map_id> /action forward
                        # nxos: vlan access-map <access_map_id> / action \
                        # redirect <redirect_interface>
                        if attributes.value('access_map_action') and \
                           attributes.value('redirect_interface'):
                            configurations.append_line(
                                attributes.format(
                                    'action {access_map_action} '
                                    '{redirect_interface}'))
                        else:
                            configurations.append_line(
                                attributes.format(
                                    'action {access_map_action}'))

                        # nxos: vlan access-map <access_map_id> / statistics
                        # nxos: vlan access-map <access_map_id> / exit
                        # nxos: vlan access-map <access_map_id> / match
                        if attributes.value('access_map_match'):
                            if attributes.value('access_list_name'):
                                configurations.append_line(
                                    attributes.format('match {access_map_match}'
                                                      ' address {access_list}'))

                        # nxos: vlan access-map <access_map_id> / no
                        # nxos: vlan access-map <access_map_id> / this
                        # nxos: vlan access-map <access_map_id> / pop
                        # nxos: vlan access-map <access_map_id> / push
                        # nxos: vlan access-map <access_map_id> / where

                    return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

        class VlanConfigurationAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                with configurations.submode_context(
                    attributes.format(
                        'vlan configuration {vlan_configuration_id}',
                        force=True)):
                    if unconfig and attributes.iswildcard:
                        # Never reached!
                        configurations.submode_unconfig()

                    # iosxe: vlan configuration <vlan_configuration_id> / \
                    # egress port-channel load-balance random
                    if attributes.value('egress_load_balance'):
                        configurations.append_line(
                            attributes.format(
                                'egress port-channel load-balance random'))
                    # nxos: vlan configuration <vlan_configuration_id> / \
                    # device-tracking
                    # nxos: vlan configuration <vlan_configuration_id> / action
                    # nxos: vlan configuration <vlan_configuration_id> / exit
                    # nxos: vlan configuration <vlan_configuration_id> / ip
                    # nxos: vlan configuration <vlan_configuration_id> / ipv6
                    # nxos: vlan configuration <vlan_configuration_id> / no
                    # nxos: vlan configuration <vlan_configuration_id> / egress
                    # nxos: vlan configuration <vlan_configuration_id> /layer-2
                    # nxos: vlan configuration <vlan_configuration_id> / \
                    # service-policy
                    # nxos: vlan configuration <vlan_configuration_id> / this
                    # nxos: vlan configuration <vlan_configuration_id> / pop
                    # nxos: vlan configuration <vlan_configuration_id> / push
                    # nxos: vlan configuration <vlan_configuration_id> / where

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                # "Set the interface to access or trunk mode for VLANs"
                if attributes.value('switchport_mode'):
                    self.interface.switchport_mode = \
                        attributes.value('switchport_mode')

                if attributes.value('sw_trunk_allowed_vlan'):
                    self.interface.sw_trunk_allowed_vlan = \
                        attributes.value('sw_trunk_allowed_vlan')

                if unconfig:
                    if attributes.attributes is not None:
                        configurations = \
                            self.interface.build_unconfig(
                                apply=False,
                                attributes=attributes.attributes)
                    else:
                        configurations = \
                            self.interface.build_unconfig(
                                apply=False,
                                attributes={'switchport_mode': None,
                                            'sw_trunk_allowed_vlan': None})
                else:
                    configurations = self.interface.build_config(apply=False)

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

        # ============== new vlan structure ===========================
        class VlanAttributes(ABC):
            def build_config(self, devices=None, apply=True, attributes=None,
                             unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                        attributes.format('vlan {vlan}', force=True)):
                    if unconfig and attributes.iswildcard:
                        # Never reached!
                        configurations.submode_unconfig()

                    # shutdown
                    if attributes.value('shutdown') == False:
                        configurations.append_line(
                            attributes.format('no shutdown'))
                    elif attributes.value('shutdown') == True:
                        configurations.append_line(
                            attributes.format('shutdown'))

                    # name
                    if attributes.value('name'):
                        configurations.append_line(
                            attributes.format('name {name}'))

                    # state
                    if attributes.value('state'):
                        state_value = attributes.value('state').value
                        configurations.append_line(
                            attributes.format('state {state}'.format(state=state_value)))

                    # mode
                    if attributes.value('mode'):
                        state_value = attributes.value('mode').value
                        configurations.append_line(
                            attributes.format('mode {mode.value}'))
                    # vn_segment_id
                    if attributes.value('vn_segment_id'):
                        configurations.append_line(
                            attributes.format('vn-segment {vn_segment_id}'))

                return str(configurations)

        class VlanConfigAttributes(ABC):
            def build_config(self, devices=None, apply=True, attributes=None,
                             unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                        attributes.format(
                            'vlan configuration {config_vlan_id}', force=True)):
                    if unconfig and attributes.iswildcard:
                        # Never reached!
                        configurations.submode_unconfig()

                    # ip_igmp_snooping
                    if attributes.value('ip_igmp_snooping'):
                        configurations.append_line('ip igmp snooping')

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)


