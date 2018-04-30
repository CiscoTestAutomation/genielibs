
from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder


class Evi(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs, kwargs
        assert not apply
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        with configurations.submode_context(
                attributes.format('l2vpn evpn instance {evi_id} {evi_mode}', force=True)):

            sub, attributes2 = attributes.namespace('bgp')
            if sub is not None:
                configurations.append_block(
                    sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes, unconfig=True)

    class BgpAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not apply
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            if attributes.value('enabled', force=True):

                configurations.append_line(
                    attributes.format('rd {rd}'))

                both_route_targets = set(self.export_route_targets) & set(self.import_route_targets)

                for v, attributes2 in attributes.sequence_values('export_route_targets', sort=True):
                    if v in both_route_targets:
                        cfg = 'route-target {}'.format(v.route_target)
                    else:
                        cfg = 'route-target export {}'.format(v.route_target)
                    configurations.append_line(cfg)

                for v, attributes2 in attributes.sequence_values('import_route_targets', sort=True):
                    if v in both_route_targets:
                        continue  # Already done above
                    cfg = 'route-target import {}'.format(v.route_target)
                    configurations.append_line(cfg)

                if attributes.value('auto_route_target') is not None:
                    if attributes.value('auto_route_target'):
                        configurations.append_line('auto-route-target')
                    else:
                        configurations.append_line('no auto-route-target', unconfig_cmd = 'auto-route-target')

            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True)

    class LoadBalancingAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not apply
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True)

