"""Implement Nexus (nxos) Specific Configurations for Evpn objects.
"""

# Table of contents:
#     class Evpn:
#         class InterfaceAttributes:
#             def build_config/build_unconfig:
#             class EthernetSegmentAttributes:
#                 def build_config/build_unconfig:
#                 class BgpAttributes:
#                     def build_config/build_unconfig:
#         class DeviceAttributes:
#             def build_config/build_unconfig:

from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning, AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
import genie.conf.base.interface
from genie.conf.base.config import CliConfig


class Evpn(ABC):

    class VniAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False):
            assert not apply
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # nxos: evpn / vni 4096 l2 (config-evpn-evi)
            with configurations.submode_context(attributes.format('vni {vni.vni_id} l2', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                ns, attributes2 = attributes.namespace('ethernet_segment')
                if ns is not None:
                    configurations.append_block(ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True)

        class EthernetSegmentAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                ns, attributes2 = attributes.namespace('bgp')
                if ns is not None:
                    configurations.append_block(ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True)

            class BgpAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    if attributes.value('enabled', force=True):

                        # nxos: evpn / vni 4096 l2 / bgp
                        if attributes.value('enabled'):
                            configurations.append_line('bgp')

                        # nxos: evpn / vni 4096 l2 / rd auto
                        # nxos: evpn / vni 4096 l2 / rd 100:200000
                        # nxos: evpn / vni 4096 l2 / rd 100000:200
                        # nxos: evpn / vni 4096 l2 / rd 1.2.3.4:1
                        configurations.append_line(attributes.format('rd {rd}'))

                        # nxos: evpn / vni 4096 l2 / route-target both auto
                        # nxos: evpn / vni 4096 l2 / route-target both 100:200000
                        # nxos: evpn / vni 4096 l2 / route-target both 100000:200
                        # nxos: evpn / vni 4096 l2 / route-target both 1.2.3.4:1
                        both_route_targets = set(self.export_route_targets) & set(self.import_route_targets)

                        # nxos: evpn / vni 4096 l2 / route-target export auto  # XXXJST how does this match none in IOS-XR?
                        # nxos: evpn / vni 4096 l2 / route-target export 100:200000
                        # nxos: evpn / vni 4096 l2 / route-target export 100000:200
                        # nxos: evpn / vni 4096 l2 / route-target export 1.2.3.4:1
                        for v, attributes2 in attributes.sequence_values('export_route_targets'):
                            if v == 'auto':
                                cfg = 'route-target {} {}'.format(
                                    'both' if v in both_route_targets else 'export',
                                    v)
                            else:
                                cfg = 'route-target {} {}'.format(
                                    'both' if v in both_route_targets else 'export',
                                    v.route_target)
                                if v.stitching:
                                    warnings.warn(
                                        'export bgp route-target stitching',
                                        UnsupportedAttributeWarning)
                            configurations.append_line(cfg)

                        # nxos: evpn / vni 4096 l2 / route-target import auto
                        # nxos: evpn / vni 4096 l2 / route-target import 100:200000
                        # nxos: evpn / vni 4096 l2 / route-target import 100000:200
                        # nxos: evpn / vni 4096 l2 / route-target import 1.2.3.4:1
                        for v, attributes2 in attributes.sequence_values('import_route_targets'):
                            if v == 'auto':
                                cfg = 'route-target import {}'.format(v)
                            else:
                                cfg = 'route-target import {}'.format(v.route_target)
                                if v.stitching:
                                    warnings.warn(
                                        'import bgp route-target stitching',
                                        UnsupportedAttributeWarning)
                            configurations.append_line(cfg)

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True)

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False):
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # nxos: evpn esi multihoming

            # nxos: evpn (config-evpn)
            with configurations.submode_context('evpn'):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # nxos: evpn / vni 4096 l2 (config-evpn-evi)
                for sub, attributes2 in attributes.mapping_values('vni_attr', keys=self.vnis, sort=True):
                    configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True)

