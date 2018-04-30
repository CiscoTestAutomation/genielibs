
from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig


class Evi(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs, kwargs
        assert not apply
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        with configurations.submode_context(
                attributes.format('evi {evi_id}', force=True)):

            # iosxr: evpn / evi 1 / advertise-mac
            if attributes.value('advertise_mac'):
                configurations.append_line('advertise-mac')

            # iosxr: evpn / evi 1 / control-word-disable
            if attributes.value('control_word_disable'):
                configurations.append_line('control-word-disable')

            sub, attributes2 = attributes.namespace('bgp')
            if sub is not None:
                configurations.append_block(
                    sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            sub, attributes2 = attributes.namespace('load_balancing')
            if sub is not None:
                configurations.append_block(
                    sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

        return CliConfig(device=self.device, unconfig=unconfig,
                         cli_config=configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes, unconfig=True)

    class BgpAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not apply
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: evpn / evi 1 / bgp (config-evpn-evi-bgp)
            if attributes.value('enabled', force=True):
                with configurations.submode_context('bgp'):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: evpn / evi 1 / bgp / rd 100:200000
                    # iosxr: evpn / evi 1 / bgp / rd 65536:200
                    # iosxr: evpn / evi 1 / bgp / rd 1.2.3.4:1
                    configurations.append_line(
                        attributes.format('rd {rd}'))

                    # iosxr: evpn / evi 1 / bgp / route-target 100:200000
                    # iosxr: evpn / evi 1 / bgp / route-target 100:200000 stitching
                    # iosxr: evpn / evi 1 / bgp / route-target 65536:200
                    # iosxr: evpn / evi 1 / bgp / route-target 65536:200 stitching
                    # iosxr: evpn / evi 1 / bgp / route-target 1.2.3.4:1
                    # iosxr: evpn / evi 1 / bgp / route-target 1.2.3.4:1 stitching
                    both_route_targets = set(self.export_route_targets) & set(self.import_route_targets)

                    # iosxr: evpn / evi 1 / bgp / route-target export 100:200000
                    # iosxr: evpn / evi 1 / bgp / route-target export 100:200000 stitching
                    # iosxr: evpn / evi 1 / bgp / route-target export 65536:200
                    # iosxr: evpn / evi 1 / bgp / route-target export 65536:200 stitching
                    # iosxr: evpn / evi 1 / bgp / route-target export 1.2.3.4:1
                    # iosxr: evpn / evi 1 / bgp / route-target export 1.2.3.4:1 stitching
                    for v, attributes2 in attributes.sequence_values('export_route_targets', sort=True):
                        if v in both_route_targets:
                            cfg = 'route-target {}'.format(v.route_target)
                        else:
                            cfg = 'route-target export {}'.format(v.route_target)
                        if v.stitching:
                            cfg += ' stitching'
                        configurations.append_line(cfg)

                    # iosxr: evpn / evi 1 / bgp / route-target import 100:200000
                    # iosxr: evpn / evi 1 / bgp / route-target import 100:200000 stitching
                    # iosxr: evpn / evi 1 / bgp / route-target import 65536:200
                    # iosxr: evpn / evi 1 / bgp / route-target import 65536:200 stitching
                    # iosxr: evpn / evi 1 / bgp / route-target import 1.2.3.4:1
                    # iosxr: evpn / evi 1 / bgp / route-target import 1.2.3.4:1 stitching
                    for v, attributes2 in attributes.sequence_values('import_route_targets', sort=True):
                        if v in both_route_targets:
                            continue  # Already done above
                        cfg = 'route-target import {}'.format(v.route_target)
                        if v.stitching:
                            cfg += ' stitching'
                        configurations.append_line(cfg)

                    # iosxr: evpn / evi 1 / bgp / route-target export none
                    if attributes.value('export_route_target_none'):
                        if attributes.value('import_route_target_none', force=True):
                            configurations.append_line('route-target none')
                        else:
                            configurations.append_line('route-target export none')

                    # iosxr: evpn / evi 1 / bgp / route-target import none
                    if attributes.value('import_route_target_none'):
                        if attributes.value('export_route_target_none', force=True):
                            pass  # Already done above
                        else:
                            configurations.append_line('route-target import none')

                    # iosxr: evpn / evi 1 / bgp / table-policy <rtepol>

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

            # iosxr: evpn / evi 1 / load-balancing (config-evpn-evi-lb)
            if attributes.value('enabled', force=True):
                with configurations.submode_context('load-balancing'):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: evpn / evi 1 / load-balancing / flow-label static
                    if attributes.value('flow_label_static'):
                        configurations.append_line('flow-label static')

            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True)

