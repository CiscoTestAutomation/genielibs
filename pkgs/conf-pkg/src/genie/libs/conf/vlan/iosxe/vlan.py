"""Implement IOSXE (iosxe) Specific Configurations for Vlan objects.
"""

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
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxe: vlan 1000 (config-vlan)
            with configurations.submode_context(
                    attributes.format('vlan {vlan_id}', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # iosxe: vlan 1000 / media enet
                # iosxe: vlan 1000 / media ethernet
                # iosxe: vlan 1000 / media fd-net
                # iosxe: vlan 1000 / media fddi
                # iosxe: vlan 1000 / media tokenring
                configurations.append_line(attributes.format(
                    'media {media.value}'))

                # iosxe: vlan 1000 / name vlan1000
                configurations.append_line(attributes.format('name {name}'))

                # iosxe: vlan 1000 / shutdown
                # iosxe: vlan 1000 / no shutdown
                v = attributes.value('shutdown')
                if v is not None:
                    if v:
                        configurations.append_line('shutdown')
                    else:
                        configurations.append_line('no shutdown')

                # iosxe: vlan 1000 / state active
                # iosxe: vlan 1000 / state suspend
                configurations.append_line(attributes.format(
                    'state {status.value}'))

                # iosxe: vlan 1000 / are <0-13>
                configurations.append_line(attributes.format('are {are}'))

                # iosxe: vlan 1000 / backupcrf enable
                # iosxe: vlan 1000 / backupcrf disable
                configurations.append_line(attributes.format(
                    'backupcrf {backupcrf.value}'))

                # iosxe: vlan 1000 / bridge <0-15>
                configurations.append_line(attributes.format(
                    'bridge {bridge}'))

                # iosxe: vlan 1000 / bridge type srb
                # iosxe: vlan 1000 / bridge type srt
                configurations.append_line(attributes.format(
                    'bridge type {bridge_type}'))

                # iosxe: vlan 1000 / parent <0-1005>
                configurations.append_line(attributes.format(
                    'parent {parent_id}'))

                # iosxe: vlan 1000 / private-vlan community
                # iosxe: vlan 1000 / private-vlan isolated
                # iosxe: vlan 1000 / private-vlan primary
                # iosxe: vlan 1000 / private-vlan association \
                # <private_vlan_association_ids>
                # iosxe: vlan 1000 / private-vlan association add \
                # <private_vlan_association_ids>
                # iosxe: vlan 1000 / private-vlan association remove \
                # <private_vlan_association_ids>
                if attributes.value('private_vlan_type'):
                    cfg = attributes.format('private-vlan {private_vlan_type}',
                                            force=True)
                    v = attributes.value('private_vlan_association_action')
                    if v is not None:
                        cfg += ' {}'.format(v)
                        association_id = \
                            attributes.value(
                                'private_vlan_association_ids', force=True)
                        if association_id is not None:
                            cfg += attributes.format(
                                ' {private_vlan_association_ids}',
                                force=True)

                    configurations.append_line(cfg)

                # iosxe: vlan 1000 / remote-span
                if attributes.value('remote_span'):
                    configurations.append_line(attributes.format(
                        'remote-span'))

                # iosxe: vlan 1000 / ring <1-1005>
                configurations.append_line(attributes.format('ring {ring}'))

                # iosxe: vlan 1000 / said <1-4294967294>
                configurations.append_line(attributes.format('said {said}'))

                # iosxe: vlan 1000 / ste <0-13>
                configurations.append_line(attributes.format('ste {ste}'))

                # iosxe: vlan 1000 / stp type auto
                # iosxe: vlan 1000 / stp type ibm
                # iosxe: vlan 1000 / stp type ieee
                configurations.append_line(attributes.format(
                    'stp type {stp_type}'))

                # iosxe: vlan 1000 / tb-vlan1 <0-1005>
                configurations.append_line(attributes.format(
                    'tb-vlan1 {tb_vlan1}'))

                # iosxe: vlan 1000 / tb-vlan2 <0-1005>
                configurations.append_line(attributes.format(
                    'tb-vlan2 {tb_vlan2}'))

            # iosxe: vlan accounting
            # iosxe: vlan accounting input
            # iosxe: vlan accounting output
            configurations.append_line(
                attributes.format('vlan accounting {accounting_type}'))

            # iosxe: vlan dot1q tag native
            if attributes.value('dot1q_tag_native'):
                configurations.append_line(
                    attributes.format('vlan dot1q tag native'))

            # iosxe: vlan configuration <Vlan id list>
            configurations.append_line(
                attributes.format(
                    'vlan configuration {configuration_id_list}'))

            # iosxe: vlan group <group name> <Vlan id list>
            configurations.append_line(
                attributes.format('vlan group {group_name} {group_id_list}'))

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

            # new vlan structure for vlans
            for sub, attributes2 in attributes.mapping_values(
                    'vlan_attr', keys=self.vlan_attr):
                configurations.append_block(sub.build_config(apply=False,
                                                             attributes=attributes2,
                                                             unconfig=unconfig,
                                                             **kwargs))

            # new vlan structure for  vlan_configs
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

                        # iosxe: vlan access-map <access_map_id> \
                        # <vlan_access_map_sequence>
                        # A workaround that needs to be better handled
                        if attributes.value('access_map_sequence'):
                            configurations.append_line(
                                attributes.format(
                                    'no vlan access-map {access_map_id}'))
                            configurations.append_line(
                                attributes.format(
                                    'vlan access-map {access_map_id}\
                                     {access_map_sequence}'))

                        # iosxe: vlan access-map <access_map_id> / action drop
                        # iosxe: vlan access-map <access_map_id> / \
                        # action forward
                        configurations.append_line(
                            attributes.format('action {access_map_action}'))

                        # iosxe: vlan access-map <access_map_id> / default

                        # iosxe: vlan access-map <access_map_id> / \
                        # match ip address <access-list name>
                        # iosxe: vlan access-map <access_map_id> / \
                        # match ipv6 address <access-list name>
                        # iosxe: vlan access-map <access_map_id> / \
                        # match mac address <access-list name>
                        if attributes.value('access_map_match'):
                            if attributes.value('access_list'):
                                configurations.append_line(
                                    attributes.format('match {access_map_match}\
                                     address {access_list}'))

                        # iosxe: vlan access-map <access_map_id> / no

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
                    # datalink flow monitor
                    if attributes.value('datalink_flow_monitor'):
                        configurations.append_line(
                            attributes.format('datalink flow monitor'))
                    # iosxe: vlan configuration <vlan_configuration_id> / \
                    # device-tracking
                    # iosxe: vlan configuration <vlan_configuration_id> / \
                    # action
                    # iosxe: vlan configuration <vlan_configuration_id> / exit
                    # iosxe: vlan configuration <vlan_configuration_id> / ip
                    # iosxe: vlan configuration <vlan_configuration_id> / ipv6
                    # iosxe: vlan configuration <vlan_configuration_id> / no

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                # "Set the interface to access or trunk mode for VLANs"
                if attributes.value('switchport_mode'):
                    self.interface.switchport_mode = \
                        attributes.value('switchport_mode')

                if attributes.value('sw_trunk_allowed_vlan'):
                    self.interface.sw_trunk_allowed_vlan = \
                        attributes.value('sw_trunk_allowed_vlan')

                if attributes.value('sw_trunk_native_vlan'):
                    self.interface.sw_trunk_allowed_vlan = \
                        attributes.value('sw_trunk_native_vlan')


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
                                            'sw_trunk_allowed_vlan': None,
                                            'sw_trunk_native_vlan': None})
                else:
                    configurations = self.interface.build_config(apply=False)

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

        # ===================================================
        #  new vlan structure
        # ====================================================

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

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

