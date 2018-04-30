"""Implement IOSXE Specific Configurations for Vrf objects.
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
            assert not kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            with configurations.submode_context(attributes.format('vrf definition {name}', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                if attributes.value('shutdown'):
                    warnings.warn('vrf shutdown', UnsupportedAttributeWarning)

                # iosxe: vrf definition vrf1 / vpn id 0:0
                configurations.append_line(attributes.format('vpn id {vpn_id}'))
                # iosxr: vrf vrf1 / description some line data
                configurations.append_line(attributes.format('description {description}'))
                configurations.append_line(attributes.format('rd {rd}'))

                # iosxr: vrf vrf1 / address-family ipv4 unicast (config-vrf-af)
                for key, sub, attributes2 in attributes.mapping_items(
                        'address_family_attr', keys=self.address_family_attr, sort=True):
                    configurations.append_block(
                        sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                # iosxe: vrf vrf1 / vpn id 0:0
                configurations.append_line(attributes.format('vpn id {vpn_id}'))

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

                with configurations.submode_context(attributes.format(
                    'address-family {address_family.value}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # import_from_global_map
                    if attributes.value('import_from_global_map'):
                        configurations.append_line(
                            attributes.format('import {address_family.value} '
                                              'map {import_from_global_map}', force=True))

                    # export_to_global_map
                    if attributes.value('export_to_global_map'):
                        configurations.append_line(
                            attributes.format('export {address_family.value} '
                                              'map {export_to_global_map}', force=True))

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

                    # keep old handle
                    if self.address_family.value == 'ipv4 unicast':
                        if attributes.value('export_route_targets'):
                            for v, attributes3 in attributes.sequence_values('export_route_targets'):
                                configurations.append_line('route-target export {}'.format(v.route_target))

                        if attributes.value('import_route_targets'):
                            for v, attributes3 in attributes.sequence_values('import_route_targets'):
                                configurations.append_line('route-target import {}'.format(v.route_target))
                    
                    if attributes.value('maximum_routes'):
                        configurations.append(attributes.format('maximum routes {maximum_routes}'))


                    # loop over all route-target
                    for sub, attributes2 in attributes.mapping_values(
                            'route_target_attr', keys=self.route_target_attr.keys(), sort=True):
                        configurations.append_block(sub.build_config(apply=False,
                            attributes=attributes2, unconfig=unconfig, **kwargs))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

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
                                'route-target import {rt}'.format(rt=self.rt))
                            configurations.append_line(
                                'route-target export {rt}'.format(rt=self.rt))
                        else:
                            configurations.append_line(
                                'route-target {type} {rt}'.format(
                                    rt=self.rt,
                                    type=attributes.value('rt_type').value))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)

