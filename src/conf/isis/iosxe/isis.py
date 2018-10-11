
from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base import Interface
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig
from ..isis import Isis as _Isis

from genie.libs.conf.address_family import AddressFamily, AddressFamilySubAttributes


class Isis(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
            assert not kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxe: router isis 100 (config-isis)
            context_cli = attributes.format('router isis {pid}', force=True)
            with configurations.submode_context(context_cli,cancel_empty=True):

                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # iosxe: router isis 100 / protocol shutdown
                if attributes.value('shutdown'):
                    configurations.append_line(attributes.format('protocol shutdown'))

                # iosxe: router isis 100 / is-type level-1
                # iosxe: router isis 100 / is-type level-2-only
                # iosxe: router isis 100 / is-type level-1-2
                configurations.append_line(attributes.format('is-type {is_type}', transform={
                    _Isis.IsType.level_1: 'level-1',
                    _Isis.IsType.level_2: 'level-2-only',
                    _Isis.IsType.level_1_2: 'level-1-2',
                }))

                # iosxe: router isis 100 / nsf cisco
                # iosxe: router isis 100 / nsf ietf
                configurations.append_line(attributes.format('nsf {nsf}', transform={
                    _Isis.Nsf.cisco: 'cisco',
                    _Isis.Nsf.ietf: 'ietf',
                }))

                # iosxe: router isis 100 / nsr
                if attributes.value('nsr'):
                    configurations.append_line(attributes.format('nsr'))

                # iosxe: router isis 100 / distribute link-state
                if attributes.value('distribute_link_state'):
                    configurations.append_line(attributes.format('distribute link-state'))

                # iosxe: router isis 100 /  segment-routing mpls
                if attributes.value('segment_routing_mpls'):
                    configurations.append_line(attributes.format('segment-routing mpls'))

                # iosxe: router isis 100 / segment-routing prefix-sid-map advertise-local
                if attributes.value('segment_routing_prefix_sid_map_advertise_local'):
                    configurations.append_line(attributes.format('segment-routing prefix-sid-map advertise-local'))

                # iosxe: router isis 100 /  segment-routing prefix-sid-map receive disable 
                if attributes.value('segment_routing_prefix_sid_map_receive') is True:
                    configurations.append_line(attributes.format('segment-routing prefix-sid-map receive'))
                elif attributes.value('segment_routing_prefix_sid_map_receive') is False:
                    configurations.append_line(attributes.format('segment-routing prefix-sid-map receive disable'))

                # iosxe: router isis 100 / net 11.0000.0000.0000.0000.00
                for net_id, attributes2 in attributes.sequence_values('net_ids', sort=True):
                    configurations.append_line(attributes2.format('net {area_address}.{system_id}.{nsel}'))

                # iosxe: router isis 100 / passive-interface Loopback0
                for sub, attributes2 in attributes.mapping_values('interface_attr', keys=self.interfaces, sort=True):
                    if attributes2.value('passive'):
                        configurations.append_line(attributes2.format('passive-interface {interface.name}',force=True))

                for sub, attributes2 in attributes.mapping_values('address_family_attr', keys=self.address_families, sort=True):
                    configurations.append_block(
                        sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            for sub, attributes2 in attributes.mapping_values('interface_attr', keys=self.interfaces, sort=True):
                configurations.append_block(
                    sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            if apply:
                if configurations:
                    self.device.configure(configurations)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class AddressFamilyAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                assert not kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                if self.address_family.name == 'ipv4_unicast':

                    # iosxe: router isis 100 /  metric-style wide
                    configurations.append_line(attributes.format('metric-style {metric_style.value}'))

                    # iosxe : router isis 100 / ispf level-1
                    # iosxe : router isis 100 / ispf level-2
                    # iosxe : router isis 100 / ispf level-1-2
                    configurations.append_line(attributes.format('ispf {ispf_type}', transform={
                        _Isis.IsType.level_1: 'level-1',
                        _Isis.IsType.level_2: 'level-2',
                        _Isis.IsType.level_1_2: 'level-1-2',
                    }))

                    # iosxe: router isis 100 / mpls traffic-eng level-1
                    # iosxe: router isis 100 / mpls traffic-eng level-2
                    # iosxe: router isis 100 / mpls traffic-eng level-1 ; mpls traffic-eng level-2
                    configurations.append_line(attributes.format('mpls traffic-eng {mpls_te_level}', transform={
                        _Isis.IsType.level_1: 'level-1',
                        _Isis.IsType.level_2: 'level-2',
                        _Isis.IsType.level_1_2: 'level-1\nmpls traffic-eng level-2',
                    }))

                    # iosxe: router isis 100 / mpls traffic-eng router-id <intf>
                    configurations.append_line(attributes.format('mpls traffic-eng router-id {mpls_te_rtrid.name}'))

                    # iosxe : router isis 100 / maximum-paths 32
                    configurations.append_line(attributes.format('maximum-paths {maximum-paths}'))

                    # iosxe : router isis 100 / mpls ldp autoconfig
                    if attributes.value('ldp_auto_config'):
                        configurations.append_line(attributes.format('mpls ldp autoconfig'))

                    # iosxe : router isis 100 / mpls ldp sync
                    if attributes.value('ldp_sync'):
                        configurations.append_line(attributes.format('mpls ldp sync'))

                    # iosxe : router isis 100 / mpls ldp sync-igp-shortcut
                    if attributes.value('ldp_sync_shortcut'):
                        configurations.append_line(attributes.format('mpls ldp sync-igp-shortcut'))

                    # iosxe : router isis 100 / mpls ldp ac-igp-shortcut
                    if attributes.value('ldp_auto_config_shortcut'):
                        configurations.append_line(attributes.format('mpls ldp ac-igp-shortcut'))

                # iosxe: router isis 100 / address-family ipv4|ipv6 unicast|multicast (config-isis-af)
                with configurations.submode_context(attributes.format('address-family {address_family.value}', force=True),\
                                                    cancel_empty=True):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    if self.address_family.name != 'ipv4_unicast':
                        configurations.append_line(attributes.format('metric-style {metric_style.value}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                assert not kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxe: interface <intf> (config-if)
                with configurations.submode_context(attributes.format('interface {interface.name}',force=True),cancel_empty=True):
                    for sub, attributes2 in attributes.mapping_values('address_family_attr',keys=self.address_families, sort=True):
                        if sub.address_family.name.startswith('ipv4'):
                            configurations.append_line(attributes.format('ip router isis {pid}',force=True))
                        if sub.address_family.name.startswith('ipv6'):
                            configurations.append_line(attributes.format('ipv6 router isis {pid}',force=True))

                    # iosxe: interface <intf> / isis network point-to-point
                    if attributes.value('point_to_point'):
                        configurations.append_line(attributes.format('isis network point-to-point'))

                    # iosxe: interface <intf> / isis circuit-type level-1
                    # iosxe: interface <intf> / isis circuit-type level-2-only
                    # iosxe: interface <intf> / isis circuit-type level-1-2
                    configurations.append_line(attributes.format('isis circuit-type {circuit_type}', transform={
                        _Isis.IsType.level_1: 'level-1',
                        _Isis.IsType.level_2: 'level-2-only',
                        _Isis.IsType.level_1_2: 'level-1-2',
                    }))

                    # iosxe: interface <intf> / isis metric 10
                    configurations.append_line(attributes.format('isis metric {metric}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

