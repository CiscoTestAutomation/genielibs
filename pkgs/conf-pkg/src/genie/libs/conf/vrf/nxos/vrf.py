"""Implement Nexus (nxos) Specific Configurations for Vrf objects.
"""

# Table of contents:
#     class Vrf:
#         class DeviceAttributes:
#             def build_config/build_unconfig:
#             class AddressFamilyAttributes:
#                 def build_config/build_unconfig:
#                 Class RouteTargetAttributes:

from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig


class Vrf(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # nxos: vrf context vrf1 (config-vrf)
            with configurations.submode_context(attributes.format('vrf context {name}', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # nxos: vrf context vrf1 / rd 1.2:1
                v = attributes.value('rd')
                if v is not None:
                    # if v != 'auto':
                    #     v = format(v, 'd.d:d')
                    configurations.append_line('rd {}'.format(v))

                # nxos: vrf context vrf1 / vni 1-16777214
                if attributes.value('vni'):
                    configurations.append_line(attributes.format('vni {vni}'))

                # nxos: vrf context vrf1 / vni 1-16777214 l3
                if attributes.value('vni_mode_l3'):
                    configurations.append_line(attributes.format('vni {vni_mode_l3} l3'))

                # nxos: vrf context vrf1 / address-family ipv4 unicast (config-vrf-af-ipv4)
                # nxos: vrf context vrf1 / address-family ipv6 unicast (config-vrf-af-ipv6)
                for key, sub, attributes2 in attributes.mapping_items(
                        'address_family_attr', keys=self.address_family_attr,
                        sort=True):
                    configurations.append_block(
                        sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                # nxos: vrf context vrf1 / amt flush-routes
                if attributes.value('amt_flush_routes'):
                    configurations.append_line('amt flush-routes')

                # nxos: vrf context vrf1 / amt pseudo-interface Ethernet1/1
                configurations.append_line(attributes.format('amt pseudo-interface {amt_pseudo_interface.name}'))

                # nxos: vrf context vrf1 / description some line data
                configurations.append_line(attributes.format('description {description}'))

                # nxos: vrf context vrf1 / ip ... -> StaticRouting/TODO
                # nxos: vrf context vrf1 / ipv6 ... -> StaticRouting/TODO

                # nxos: vrf context vrf1 / shutdown
                if attributes.value('shutdown'):
                    configurations.append_line('shutdown')

                # nxos: vrf context vrf1 / vni 4096 topology 1

                # comment out due to impot issue (this is from old configuration)
                #    --- ImportError: cannot import name 'ESI'
                # for vni, attributes2 in attributes.sequence_values('vnis'):
                #     configurations.append_line('vni {}'.format(vni.vni_id))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class AddressFamilyAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # nxos: vrf context vrf1 / address-family ipv4 unicast (config-vrf-af-ipv4)
                # nxos: vrf context vrf1 / address-family ipv6 unicast (config-vrf-af-ipv6)
                with configurations.submode_context(attributes.format(
                    'address-family {address_family.value}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # nxos: vrf context vrf1 / address-family ipv4 unicast / export map someword
                    configurations.append_line(attributes.format('export map {export_route_policy.name}'))

                    # nxos: vrf context vrf1 / address-family ipv4 unicast / import map someword
                    configurations.append_line(attributes.format('import map {import_route_policy.name}'))

                    # nxos: vrf context vrf1 / address-family ipv4 unicast / import vrf default map someword
                    # nxos: vrf context vrf1 / address-family ipv4 unicast / import vrf default 1 map someword
                    v = attributes.value('import_from_default_vrf_route_policy')
                    if v is not None:
                        cfg = 'import vrf default'
                        cfg += attributes.format(' {import_from_default_vrf_route_policy_maximum_prefixes}', force=True)
                        cfg += ' map {}'.format(v)
                        if attributes.value('import_from_default_vrf_advertise_as_vpn'):
                            warnings.warn('import vrf default map advertise_as_vpn', UnsupportedAttributeWarning)
                        configurations.append_line(cfg)

                    # nxos: vrf context vrf1 / address-family ipv4 unicast / route-target both 1.2.3.4:1
                    # nxos: vrf context vrf1 / address-family ipv4 unicast / route-target both 100:200
                    both_route_targets = set(self.export_route_targets) & set(self.import_route_targets)

                    # nxos: vrf context vrf1 / address-family ipv4 unicast / route-target export 1.2.3.4:1
                    # nxos: vrf context vrf1 / address-family ipv4 unicast / route-target export 100:200
                    for v, attributes2 in attributes.sequence_values('export_route_targets'):
                        if v in both_route_targets:
                            cfg = 'route-target both {}'.format(v.route_target)
                        else:
                            cfg = 'route-target export {}'.format(v.route_target)
                        if v.stitching:
                            cfg += ' auto evpn'
                        configurations.append_line(cfg)

                    # nxos: vrf context vrf1 / address-family ipv4 unicast / route-target import 1.2.3.4:1
                    # nxos: vrf context vrf1 / address-family ipv4 unicast / route-target import 100:200
                    for v, attributes2 in attributes.sequence_values('import_route_targets'):
                        if v in both_route_targets:
                            continue  # done above
                        else:
                            cfg = 'route-target import {}'.format(v.route_target)
                        if v.stitching:
                            cfg += ' auto evpn'
                        configurations.append_line(cfg)

                    # nxos: vrf context vrf1 / address-family ipv4|ipv6 unicast / maximum routes 1
                    # nxos: vrf context vrf1 / address-family ipv4|ipv6 unicast / maximum routes 1 1
                    # nxos: vrf context vrf1 / address-family ipv4|ipv6 unicast / maximum routes 1 1 reinstall 1
                    # nxos: vrf context vrf1 / address-family ipv4|ipv6 unicast / maximum routes 1 warning-only
                    cfg = attributes.format('maximum routes {maximum_prefix}')
                    if cfg:
                        if attributes.value('maximum_prefix_warning_only', force=True):
                            cfg += ' warning-only'
                        else:
                            v = attributes.value('maximum_prefix_threshold', force=True)
                            if v is not None:
                                cfg += ' {}'.format(v)
                                cfg += attributes.format(' reinstall {maximum_prefix_reinstall_threshold}', force=True)
                        configurations.append_line(cfg)

                    # ---------- Genie Team latest Update --------------- #
                    # import_from_global_map
                    if attributes.value('import_from_global_map'):
                        configurations.append_line(
                            attributes.format('import vrf default map'
                                              ' {import_from_global_map}', force=True))

                    # routing_table_limit_number
                    if attributes.value('routing_table_limit_number') and \
                       attributes.value('alert_percent_value'):
                        configurations.append_line(
                            attributes.format('maximum routes {routing_table_limit_number} '
                                              '{alert_percent_value}'))
                    elif attributes.value('routing_table_limit_number') and \
                       attributes.value('simple_alert'):
                        configurations.append_line(
                            attributes.format('maximum routes {routing_table_limit_number} '
                                              'warning-only'))

                    # loop over all route-target
                    for sub, attributes2 in attributes.mapping_values(
                            'route_target_attr', keys=self.route_target_attr.keys(), sort=True):
                        configurations.append_block(sub.build_config(apply=False,
                            attributes=attributes2, unconfig=unconfig, **kwargs))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class RouteTargetAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    if unconfig:
                        if attributes.attributes['rt_type'] == {'both': None} or\
                            attributes.attributes['rt_type'] == {'import': None} or\
                            attributes.attributes['rt_type'] == {'export': None}:
                            for key, value in attributes.attributes['rt_type'].items():
                                self.tmp_rt_type = key
                        else:
                            self.tmp_rt_type = attributes.attributes['rt_type']

                        if not self.tmp_rt_type:
                            configurations.append_line(
                                'route-target import {rt}'.format(rt=self.rt))
                            configurations.append_line(
                                'route-target export {rt}'.format(rt=self.rt))
                        else:
                            if self.tmp_rt_type == 'both' and self.rt != "auto":
                                configurations.append_line(
                                    'route-target import {rt}'.format(rt=self.rt), raw=True)
                                configurations.append_line(
                                    'route-target export {rt}'.format(rt=self.rt), raw=True)
                            else:
                                # route-target <rt_type> <rt>
                                configurations.append_line(
                                    'route-target {type} {rt}'.format(
                                        rt=self.rt,
                                        type=self.tmp_rt_type), raw=True)

                    # route-target <rt_type> <rt>
                    if not unconfig and attributes.value('rt_type'):
                        if attributes.value('rt_type').value == 'both' and self.rt != "auto":
                            configurations.append_line(
                                'route-target import {rt}'.format(rt=self.rt))
                            configurations.append_line(
                                'route-target export {rt}'.format(rt=self.rt))
                        else:
                            # route-target <rt_type> <rt>
                            configurations.append_line(
                                'route-target {type} {rt}'.format(
                                    rt=self.rt,
                                    type=attributes.value('rt_type').value))

                    for sub, attributes2 in attributes.mapping_values('protocol_attr',
                                                                      sort=True,
                                                                      keys=self.protocol_attr):
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
                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)

                class ProtocolAttributes(ABC):

                    def build_config(self, apply=True, attributes=None,
                                     unconfig=False, **kwargs):
                        assert not apply
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # route-target <rt_type> <rt> mvpn
                        if attributes.value('rt_mvpn'):
                            self.protocol = 'mvpn'
                        # route-target <rt_type> <rt> evpn
                        if attributes.value('rt_evpn'):
                            self.protocol = 'evpn'

                        if unconfig:
                            if self.protocol:
                                if self.tmp_rt_type:
                                    configurations.append_line(
                                        'route-target {rt_type} {rt} {protocol}'.format(
                                            rt_type=self.tmp_rt_type,
                                            rt=self.rt,
                                            protocol=self.protocol))

                        if not unconfig and self.protocol:
                            configurations.append_line(
                                'route-target {rt_type} {rt} {protocol}'.format(
                                    rt_type=attributes.value('rt_type').value,
                                    rt=self.rt,
                                    protocol=self.protocol))

                        return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)