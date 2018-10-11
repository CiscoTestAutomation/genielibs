"""Implement IOS-XR (iosxr) Specific Configurations for Evpn objects.
"""

# Table of contents:
#     class Evpn:
#         class InterfaceAttributes:
#             def build_config/build_unconfig:
#             class EthernetSegmentAttributes:
#                 def build_config/build_unconfig:
#                 class BgpAttributes:
#                     def build_config/build_unconfig:
#         class PseudowireNeighborAttributes:
#             def build_config/build_unconfig:
#             class EthernetSegmentAttributes:
#                 def build_config/build_unconfig:
#                 class BgpAttributes:
#                     def build_config/build_unconfig:
#         class VfiAttributes:
#             def build_config/build_unconfig:
#             class EthernetSegmentAttributes:
#                 def build_config/build_unconfig:
#                 class BgpAttributes:
#                     def build_config/build_unconfig:
#         class DeviceAttributes:
#             def build_config/build_unconfig:
#             class BgpAttributes:
#                 def build_config/build_unconfig:
#             class LoadBalancingAttributes:
#                 def build_config/build_unconfig:

from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning, AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig


class Evpn(ABC):

    class InterfaceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: evpn / interface Bundle-Ether1 (config-evpn-ac)
            with configurations.submode_context(attributes.format('interface {interface_name}', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # iosxr: evpn / interface Bundle-Ether1 / ethernet-segment (config-evpn-ac-es)
                ns, attributes2 = attributes.namespace('ethernet_segment')
                if ns is not None:
                    configurations.append_block(ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

                # iosxr: evpn / interface Bundle-Ether1 / mac-flush mvrp
                configurations.append_line(attributes.format('mac-flush {mac_flush}'))

                # iosxr: evpn / interface Bundle-Ether1 / timers (config-evpn-ac-timers)
                with configurations.submode_context('timers', cancel_empty=True):

                    # iosxr: evpn / interface Bundle-Ether1 / timers / recovery 20
                    configurations.append_line(attributes.format('recovery {recovery_timer}', inherited=False))

                    if attributes.value('peering_timer', inherited=False) is not None:
                        warnings.warn(
                            'evpn interface peering_timer',
                            UnsupportedAttributeWarning)

            return str(configurations)

        def build_unconfig(self, *args, **kwargs):
            return self.build_config(*args, unconfig=True, **kwargs)

        class EthernetSegmentAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: evpn / interface Bundle-Ether1 / ethernet-segment (config-evpn-ac-es)
                with configurations.submode_context('ethernet-segment'):
                    if not attributes.value('enabled', force=True):
                        configurations.submode_cancel()
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: evpn / interface Bundle-Ether1 / ethernet-segment / backbone-source-mac aaaa.bbbb.cccc
                    configurations.append_line(attributes.format('backbone-source-mac {backbone_source_mac}'))

                    # iosxr: evpn / interface Bundle-Ether1 / ethernet-segment / bgp route-target aaaa.bbbb.cccc
                    ns, attributes2 = attributes.namespace('bgp')
                    if ns is not None:
                        configurations.append_block(ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

                    # iosxr: evpn / interface Bundle-Ether1 / ethernet-segment / force single-homed
                    if attributes.value('force_single_homed'):
                        configurations.append_line('force single-homed')

                    # iosxr: evpn / interface Bundle-Ether1 / ethernet-segment / identifier type 0 00.11.22.33.44.55.66.77.88
                    configurations.append_line(attributes.format('identifier type {esi.type} {esi.dotted}'))

                    # iosxr: evpn / interface Bundle-Ether1 / ethernet-segment / load-balancing-mode single-active
                    configurations.append_line(attributes.format('load-balancing-mode {load_balancing_mode}'))

                    # iosxr: evpn / interface Bundle-Ether1 / ethernet-segment / service-carving manual (config-evpn-ac-es-vlan-man)
                    # iosxr: evpn / interface Bundle-Ether1 / ethernet-segment / service-carving manual / primary someword secondary someword2

                return str(configurations)

            def build_unconfig(self, *args, **kwargs):
                return self.build_config(*args, unconfig=True, **kwargs)

            class BgpAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    if attributes.value('enabled', force=True):

                        # iosxr: evpn / interface Bundle-Ether1 / ethernet-segment / bgp route-target aaaa.bbbb.cccc
                        configurations.append_line(attributes.format('bgp route-target {import_route_target}'))

                    return str(configurations)

                def build_unconfig(self, *args, **kwargs):
                    return self.build_config(*args, unconfig=True, **kwargs)

    class PseudowireNeighborAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # virtual neighbor 70.70.70.70 pw-id 17300005
            with configurations.submode_context(attributes.format('virtual neighbor {ip} pw-id {pw_id}', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # iosxr: evpn / virtual neighbor 70.70.70.70 pw-id 17300005 / ethernet-segment (config-evpn-ac-es)
                ns, attributes2 = attributes.namespace('ethernet_segment')
                if ns is not None:
                    configurations.append_block(ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

            return str(configurations)

        def build_unconfig(self, *args, **kwargs):
            return self.build_config(*args, unconfig=True, **kwargs)

        class EthernetSegmentAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: evpn / virtual neighbor 70.70.70.70 pw-id 17300005 / ethernet-segment (config-evpn-ac-es)
                with configurations.submode_context('ethernet-segment'):
                    if not attributes.value('enabled', force=True):
                        configurations.submode_cancel()
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: evpn / virtual neighbor 70.70.70.70 pw-id 17300005 / ethernet-segment / bgp route-target aaaa.bbbb.cccc
                    ns, attributes2 = attributes.namespace('bgp')
                    if ns is not None:
                        configurations.append_block(ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

                    # iosxr: evpn / virtual neighbor 70.70.70.70 pw-id 17300005 / ethernet-segment / identifier type 0 00.11.22.33.44.55.66.77.88
                    configurations.append_line(attributes.format('identifier type {esi.type} {esi.dotted}'))

                return str(configurations)

            def build_unconfig(self, *args, **kwargs):
                return self.build_config(*args, unconfig=True, **kwargs)

            class BgpAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    if attributes.value('enabled', force=True):

                        # iosxr: evpn / interface Bundle-Ether1 / ethernet-segment / bgp route-target aaaa.bbbb.cccc
                        configurations.append_line(attributes.format('bgp route-target {import_route_target}'))

                    return str(configurations)

                def build_unconfig(self, *args, **kwargs):
                    return self.build_config(*args, unconfig=True, **kwargs)

    class VfiAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            #  virtual vfi ac-vfi-5
            with configurations.submode_context(attributes.format('virtual vfi {vfi_name}', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # iosxr: evpn / virtual vfi ac-vfi-5 / ethernet-segment (config-evpn-ac-es)
                ns, attributes2 = attributes.namespace('ethernet_segment')
                if ns is not None:
                    configurations.append_block(ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

            return str(configurations)

        def build_unconfig(self, *args, **kwargs):
            return self.build_config(*args, unconfig=True, **kwargs)

        class EthernetSegmentAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: evpn / virtual vfi ac-vfi-5 / ethernet-segment (config-evpn-ac-es)
                with configurations.submode_context('ethernet-segment'):
                    if not attributes.value('enabled', force=True):
                        configurations.submode_cancel()
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: evpn / virtual vfi ac-vfi-5 / ethernet-segment / bgp route-target aaaa.bbbb.cccc
                    ns, attributes2 = attributes.namespace('bgp')
                    if ns is not None:
                        configurations.append_block(ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

                    # iosxr: evpn / virtual vfi ac-vfi-5 / ethernet-segment / identifier type 0 00.11.22.33.44.55.66.77.88
                    configurations.append_line(attributes.format('identifier type {esi.type} {esi.dotted}'))

                return str(configurations)

            def build_unconfig(self, *args, **kwargs):
                return self.build_config(*args, unconfig=True, **kwargs)

            class BgpAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    if attributes.value('enabled', force=True):

                        # iosxr: evpn / interface Bundle-Ether1 / ethernet-segment / bgp route-target aaaa.bbbb.cccc
                        configurations.append_line(attributes.format('bgp route-target {import_route_target}'))

                    return str(configurations)

                def build_unconfig(self, *args, **kwargs):
                    return self.build_config(*args, unconfig=True, **kwargs)

    class DeviceAttributes(ABC):

        def build_config(self, interfaces=None,
                         apply=True, attributes=None, unconfig=False, **kwargs):
            # assert not apply
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            if interfaces is None:
                interfaces = set(self.interfaces)
            else:
                interfaces = set(self.interfaces).intersection(interfaces)

            # iosxr: evpn (config-evpn)
            with configurations.submode_context('evpn'):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # iosxr: evpn / bgp (config-evpn-bgp)
                ns, attributes2 = attributes.namespace('bgp')
                if ns is not None:
                    configurations.append_block(ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

                # iosxr: evpn / evi 1 (config-evpn-evi)
                for evi, attributes2 in attributes.sequence_values('evis', sort=True):
                    if unconfig:
                        configurations.append_block(evi.build_unconfig(apply=False, attributes=attributes2))
                    else:
                        configurations.append_block(evi.build_config(apply=False, attributes=attributes2))

                # iosxr: evpn / interface Bundle-Ether1 (config-evpn-ac)
                for sub, attributes2 in attributes.mapping_values('interface_attr', keys=interfaces, sort=True):
                    configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

                # iosxr: evpn /  virtual neighbor 70.70.70.70 pw-id 17300005
                for sub, attributes2 in attributes.mapping_values('pw_neighbor_attr', sort=True):
                    configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

                # iosxr: evpn /  virtual vfi ac-vfi-5
                for sub, attributes2 in attributes.mapping_values('vfi_attr', sort=True):
                    configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

                # iosxr: evpn / timers (config-evpn-timers)
                with configurations.submode_context('timers', cancel_empty=True):

                    # iosxr: evpn / timers / recovery 20
                    configurations.append_line(attributes.format('recovery {recovery_timer}'))

                    # iosxr: evpn / timers / peering <0-300>
                    configurations.append_line(attributes.format('peering {peering_timer}'))

                # iosxr: evpn / source interface Loopback0
                configurations.append_line(attributes.format('source interface {source_interface.name}'))

                # iosxr: evpn / load-balancing (config-evpn-lb)
                ns, attributes2 = attributes.namespace('load_balancing')
                if ns is not None:
                    configurations.append_block(ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

                # iosxr: evpn / bgp (config-evpn-bgp)
                ns, attributes2 = attributes.namespace('bgp')
                if ns is not None:
                    configurations.append_block(ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, *args, **kwargs):
            return self.build_config(*args, unconfig=True, **kwargs)

        class BgpAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: evpn / bgp (config-evpn-bgp)
                with configurations.submode_context('bgp'):
                    if not attributes.value('enabled', force=True):
                        configurations.submode_cancel()
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: evpn / bgp / rd 100:200000
                    # iosxr: evpn / bgp / rd 65536:200
                    # iosxr: evpn / bgp / rd 1.2.3.4:1
                    configurations.append_line(attributes.format('rd {rd}'))

                return str(configurations)

            def build_unconfig(self, *args, **kwargs):
                return self.build_config(*args, unconfig=True, **kwargs)

        class LoadBalancingAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: evpn / load-balancing (config-evpn-lb)
                with configurations.submode_context('load-balancing'):
                    if not attributes.value('enabled', force=True):
                        configurations.submode_cancel()
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: evpn / load-balancing / flow-label static
                    if attributes.value('flow_label_static'):
                        configurations.append_line('flow-label static')

                return str(configurations)

            def build_unconfig(self, *args, **kwargs):
                return self.build_config(*args, unconfig=True, **kwargs)

