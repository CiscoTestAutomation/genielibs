"""Implement IOS-XR (iosxr) Specific Configurations for Vrf objects.
"""

# Table of contents:
#     class Vrf:
#         class DeviceAttributes:
#             def build_config/build_unconfig:
#             class AddressFamilyAttributes:
#                 def build_config/build_unconfig:
#                 class RouteTargetAttributes:
#                     def build_config/build_unconfig:

from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder


class Vrf(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            with configurations.submode_context(attributes.format('vrf {name}', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                if attributes.value('shutdown'):
                    warnings.warn('vrf shutdown', UnsupportedAttributeWarning)

                # iosxr: vrf vrf1 / description some line data
                configurations.append_line(attributes.format('description {description}'))

                # iosxr: vrf vrf1 / address-family ipv4 unicast (config-vrf-af)
                for key, sub, attributes2 in attributes.mapping_items(
                        'address_family_attr', keys=self.address_family_attr, sort=True):
                    configurations.append_block(
                        sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                # iosxr: vrf vrf1 / fallback-vrf vrf2
                configurations.append_line(attributes.format('fallback-vrf {fallback_vrf.name}'))

                # iosxr: vrf vrf1 / mhost ipv4 default-interface GigabitEthernet0/0/0/0
                configurations.append_line(attributes.format('mhost ipv4 default-interface {mhost_ipv4_default_interface.name}'))

                # iosxr: vrf vrf1 / mhost ipv6 default-interface GigabitEthernet0/0/0/0
                configurations.append_line(attributes.format('mhost ipv6 default-interface {mhost_ipv6_default_interface.name}'))

                # iosxr: vrf vrf1 / mode big
                configurations.append_line(attributes.format('mode {scale_mode}'))

                # iosxr: vrf vrf1 / remote-route-filtering disable
                if attributes.value('remote_route_filtering') is False:
                    configurations.append_line('remote-route-filtering disable')

                # iosxr: vrf vrf1 / vpn id 0:0
                configurations.append_line(attributes.format('vpn id {vpn_id}'))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class AddressFamilyAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(attributes.format('address-family {address_family.value}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    if attributes.value('export_vrf') or attributes.value('import_vrf'):
                        warnings.warn('vrf export/import vrf', UnsupportedAttributeWarning)

                    # iosxr: vrf vrf1 / address-family ipv4 unicast / export route-policy <rtepol>
                    configurations.append_line(attributes.format('export route-policy {export_route_policy}'))

                    # iosxr: vrf vrf1 / address-family ipv4 unicast / export route-target 100:200
                    # iosxr: vrf vrf1 / address-family ipv4 unicast / export route-target 100:20 stitching
                    for v, attributes2 in attributes.sequence_values('export_route_targets'):
                        cfg = 'export route-target {}'.format(v.route_target)
                        if v.stitching:
                            cfg += ' stitching'
                        configurations.append_line(cfg)

                    # iosxr: vrf vrf1 / address-family ipv4 unicast / export to default-vrf route-policy <rtepol>
                    configurations.append_line(attributes.format('export to default-vrf route-policy {export_to_default_vrf_route_policy.name}'))

                    # iosxr: vrf vrf1 / address-family ipv4 unicast / export to vrf allow-imported-vpn
                    # iosxr: vrf vrf1 / address-family ipv4 unicast / export to vrf allow-imported-vpn import stitching-rt
                    # iosxr: vrf vrf1 / address-family ipv4 unicast / export to vrf import stitching-rt
                    if attributes.value('export_to_vrf_allow_imported_vpn') or \
                            attributes.value('export_to_vrf_import_stitching_rt'):
                        cfg = 'export to vrf'
                        if attributes.value('export_to_vrf_allow_imported_vpn', force=True):
                            cfg += ' allow-imported-vpn'
                        if attributes.value('export_to_vrf_import_stitching_rt', force=True):
                            cfg += ' import stitching-rt'
                        configurations.append_line(cfg)

                    # iosxr: vrf vrf1 / address-family ipv4 unicast / import from default-vrf route-policy <rtepol>
                    # iosxr: vrf vrf1 / address-family ipv4 unicast / import from default-vrf route-policy <rtepol> advertise-as-vpn
                    v = attributes.value('import_from_default_vrf_route_policy')
                    if v is not None:
                        cfg = 'import from default-vrf route-policy {}'.format(v)
                        if attributes.value('import_from_default_vrf_advertise_as_vpn', force=True):
                            cfg += ' advertise-as-vpn'
                        configurations.append_line(cfg)

                    # iosxr: vrf vrf1 / address-family ipv4 unicast / import route-policy <rtepol>
                    configurations.append_line(attributes.format('import route-policy {import_route_policy}'))

                    # iosxr: vrf vrf1 / address-family ipv4 unicast / import route-target 100:200
                    # iosxr: vrf vrf1 / address-family ipv4 unicast / import route-target 100:20 stitching
                    for v, attributes2 in attributes.sequence_values('import_route_targets'):
                        cfg = 'import route-target {}'.format(v.route_target)
                        if v.stitching:
                            cfg += ' stitching'
                        configurations.append_line(cfg)

                    # iosxr: vrf vrf1 / address-family ipv4 unicast / maximum prefix 32
                    # iosxr: vrf vrf1 / address-family ipv4 unicast / maximum prefix 32 1
                    cfg = attributes.format('maximum prefix {maximum_prefix}')
                    if cfg:
                        if attributes.value('maximum_prefix_warning_only', force=True):
                            warnings.warn('vrf maximum prefix warning-only', UnsupportedAttributeWarning)
                        v = attributes.value('maximum_prefix_threshold', force=True)
                        if v is not None:
                            cfg += ' {}'.format(v)
                            if attributes.value('maximum_prefix_reinstall_threshold', force=True):
                                warnings.warn('vrf maximum prefix reinstall threshold', UnsupportedAttributeWarning)
                        configurations.append_line(cfg)

                    # loop over all route-target
                    for sub, attributes2 in attributes.mapping_values(
                            'route_target_attr', keys=self.route_target_attr, sort=True):
                        configurations.append_block(sub.build_config(apply=False,
                            attributes=attributes2, unconfig=unconfig, **kwargs))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=False, **kwargs)


            class RouteTargetAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # route-target <rt_type> <rt>
                    if attributes.value('rt_type'):
                        if attributes.value('rt_type').value == 'both':
                            configurations.append_line(
                                'import route-target {rt}'.format(rt=self.rt))
                            configurations.append_line(
                                'export route-target {rt}'.format(rt=self.rt))
                        else:
                            configurations.append_line(
                                '{type} route-target {rt}'.format(
                                    rt=self.rt,
                                    type=attributes.value('rt_type').value))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)

