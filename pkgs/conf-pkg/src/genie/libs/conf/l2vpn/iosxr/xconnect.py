# Xconnect
#   DeviceAttributes (device_attr)
#     AutodiscoveryBgpAttributes (autodiscovery_bgp)
#         parent = xconnect.autodiscovery_bgp
#       SignalingProtocolBgpAttributes (signaling_protocol_bgp)
#           parent = xconnect.autodiscovery_bgp.signaling_protocol_bgp
#         CeAttributes (ce_attr)
#           InterfaceAttributes (interface_attr)
#
#   DeviceAutodiscoveryBgpAttributesDefaults (autodiscovery_bgp) (no config)
#     DeviceSignalingProtocolBgpAttributesDefaults (signaling_protocol_bgp) (no config)


from abc import ABC
import warnings
import contextlib

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

from genie.libs.conf.l2vpn.pseudowire import PseudowireNeighbor,\
    PseudowireIPv4Neighbor, PseudowireIPv6Neighbor, PseudowireEviNeighbor

from ..xconnect import Xconnect as _Xconnect


class Xconnect(ABC):

    class DeviceAttributes(ABC):

        class NeighborAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                nbr_ctx = None
                nbr_is_submode = True
                if isinstance(self.neighbor, PseudowireIPv4Neighbor):
                    # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 (config-l2vpn)
                    assert self.ip is not None
                    assert self.pw_id is not None
                    nbr_ctx = attributes.format('neighbor ipv4 {ip} pw-id {pw_id}', force=True)
                elif isinstance(self.neighbor, PseudowireIPv6Neighbor):
                    # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 (config-l2vpn)
                    assert self.ip is not None
                    assert self.pw_id is not None
                    nbr_ctx = attributes.format('neighbor ipv6 {ip} pw-id {pw_id}', force=True)
                elif isinstance(self.neighbor, PseudowireEviNeighbor):
                    # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor evpn evi 1 target 1 source 1
                    assert self.evi is not None
                    assert self.ac_id is not None
                    assert self.source_ac_id is not None
                    nbr_ctx = attributes.format('neighbor evpn evi {evi.evi_id} target {ac_id} source {source_ac_id}', force=True)
                    nbr_is_submode = False
                else:
                    raise ValueError(self.neighbor)
                assert nbr_ctx
                if not nbr_is_submode:
                    configurations.append_line(nbr_ctx)
                else:
                    with configurations.submode_context(nbr_ctx):

                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / backup neighbor 1.2.3.4 pw-id 1 (config-l2vpn)
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / backup neighbor 1.2.3.4 pw-id 1 / mpls static label local 16 remote 16
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / backup neighbor 1.2.3.4 pw-id 1 / pw-class someword3
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / backup neighbor 1.2.3.4 pw-id 1 (config-l2vpn)
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / backup neighbor 1.2.3.4 pw-id 1 / mpls static label local 16 remote 16
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / backup neighbor 1.2.3.4 pw-id 1 / pw-class someword3

                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / bandwidth <0-4294967295>
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / bandwidth <0-4294967295>

                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / l2tp static (config-l2vpn)
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / l2tp static / local cookie size 0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / l2tp static / local cookie size 4 value 0x0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / l2tp static / local cookie size 8 value 0x0 0x0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / l2tp static / local session 1
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / l2tp static / remote cookie size 0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / l2tp static / remote cookie size 4 value 0x0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / l2tp static / remote cookie size 8 value 0x0 0x0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / l2tp static / remote session 1
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / l2tp static (config-l2vpn)
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / l2tp static / local cookie secondary size 0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / l2tp static / local cookie secondary size 4 value 0x0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / l2tp static / local cookie secondary size 8 value 0x0 0x0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / l2tp static / local cookie size 0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / l2tp static / local cookie size 4 value 0x0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / l2tp static / local cookie size 8 value 0x0 0x0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / l2tp static / local session 1
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / l2tp static / remote cookie size 0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / l2tp static / remote cookie size 4 value 0x0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / l2tp static / remote cookie size 8 value 0x0 0x0
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / l2tp static / remote session 1

                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / mpls static label local 16 remote 16
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / mpls static label local 16 remote 16
                        remote_label = attributes.value('mpls_static_label')
                        if remote_label is not None:
                            local_label = self.parent.neighbor_attr[self.remote_neighbor].mpls_static_label
                            if local_label is None:
                                warnings.warn(
                                    'neighbor {!r} mpls_static_label missing'.format(self.remote_neighbor),
                                    UnsupportedAttributeWarning)
                            else:
                                configurations.append_line('mpls static label local {} remote {}'.\
                                                      format(local_label, remote_label))

                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / pw-class someword3
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / pw-class someword3
                        v = attributes.value('pw_class')
                        if v is not None:
                            configurations.append_line('pw-class {}'.\
                                                  format(v.device_attr[self.device].name))

                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / source 1:2::3
                        elif isinstance(self.neighbor, PseudowireIPv6Neighbor):
                            configurations.append_line(attributes.format('ipv6 source {ipv6_source}'))

                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor [ipv4] 1.2.3.4 pw-id 1 / tag-impose vlan 1
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 / tag-impose vlan 1

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class AutodiscoveryBgpAttributes(ABC):

            class SignalingProtocolBgpAttributes(ABC):

                class CeAttributes(ABC):

                    class InterfaceAttributes(ABC):

                        def build_config(self, apply=True, attributes=None, unconfig=False,
                                         **kwargs):
                            assert not apply
                            assert not kwargs, kwargs
                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / ce-id 1 / interface Bundle-Ether1 remote-ce-id 1
                            configurations.append_line(attributes.format('interface {interface_name} remote-ce-id {remote_ce_id}', force=True))

                            return str(configurations)

                        def build_unconfig(self, apply=True, attributes=None, **kwargs):
                            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

                    #CeAttributes
                    def build_config(self, apply=True, attributes=None, unconfig=False,
                                     **kwargs):
                        assert not apply
                        assert not kwargs, kwargs
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / ce-id 1 (config-l2vpn)
                        with configurations.submode_context(attributes.format('ce-id {ce_id}', force=True)):
                            if unconfig and attributes.iswildcard:
                                configurations.submode_unconfig()

                            # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / ce-id 1 / interface Bundle-Ether1 remote-ce-id 1
                            for ns, attributes2 in attributes.mapping_values('interface_attr', keys=self.interfaces, sort=True):
                                configurations.append_block(ns.build_config(apply=False, unconfig=unconfig, attributes=attributes2))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

                #SignalingProtocolBgpAttributes
                def build_config(self, apply=True, attributes=None, unconfig=False,
                                 **kwargs):
                    assert not apply
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp (config-l2vpn)
                    with configurations.submode_context('signaling-protocol bgp'):
                        if not attributes.value('enabled', force=True):
                            configurations.submode_cancel()

                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / ce-range 11
                        configurations.append_line(attributes.format('ce-range {ce_range}'))

                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / ce-id 1 (config-l2vpn)
                        for ns, attributes2 in attributes.mapping_values('ce_attr', keys=self.ce_ids, sort=True):
                            configurations.append_block(ns.build_config(apply=False, unconfig=unconfig, attributes=attributes2))

                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label both
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label both static
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label receive
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label receive static
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label transmit
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label transmit static

                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label both
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label both static
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label receive
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label receive static
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label transmit
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label transmit static

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            #AutodiscoveryBgpAttributes
            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp (config-l2vpn)
                with configurations.submode_context('autodiscovery bgp'):
                    if not attributes.value('enabled', force=True):
                        configurations.submode_cancel()

                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / rd 100000:200
                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / rd 100:200000
                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / rd 1.2.3.4:1
                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / rd auto
                    configurations.append_line(attributes.format('rd {rd}'))

                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / route-policy export <rtepol>

                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / route-target 100000:200
                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / route-target 100:200000
                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / route-target 1.2.3.4:1
                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / route-target export 100000:200
                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / route-target export 100:200000
                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / route-target export 1.2.3.4:1
                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / route-target export import 100000:200 (bug)
                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / route-target export import 100:200000 (bug)
                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / route-target export import 1.2.3.4:1 (bug)
                    both_route_targets = set(self.export_route_targets) & set(self.import_route_targets)
                    for v, attributes2 in attributes.sequence_values('export_route_targets', sort=True):
                        if v in both_route_targets:
                            cfg = 'route-target {}'.format(v.route_target)
                        else:
                            cfg = 'route-target export {}'.format(v.route_target)
                        if v.stitching:
                            warnings.warn(UnsupportedAttributeWarning,
                                         'route-target export/import stitching')
                        configurations.append_line(cfg)

                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / route-target import 100000:200
                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / route-target import 100:200000
                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / route-target import 1.2.3.4:1
                    for v, attributes2 in attributes.sequence_values('import_route_targets', sort=True):
                        if v not in both_route_targets:
                            cfg = 'route-target import {}'.format(v.route_target)
                            if v.stitching:
                                warnings.warn(UnsupportedAttributeWarning,
                                             'route-target export/import stitching')
                            configurations.append_line(cfg)

                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp (config-l2vpn)
                    ns, attributes2 = attributes.namespace('signaling_protocol_bgp')
                    if ns:
                        configurations.append_block(ns.build_config(apply=False, unconfig=unconfig, attributes=attributes2))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         contained=False, **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: l2vpn (config-l2vpn)
            submode_stack = contextlib.ExitStack()
            if not contained:
                submode_stack.enter_context(
                    configurations.submode_context('l2vpn'))

            # iosxr: l2vpn / xconnect group someword (config-l2vpn)
            with configurations.submode_context(attributes.format('xconnect group {group_name}', force=True, cancel_empty=True)):

                if self.xconnect_type is _Xconnect.Type.mp2mp:
                    # iosxr: l2vpn / xconnect group someword / mp2mp someword2 (config-l2vpn)
                    with configurations.submode_context(attributes.format('mp2mp {name}', force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / control-word disable
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / interworking ethernet
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / l2-encapsulation ethernet
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / l2-encapsulation vlan
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / mtu 64
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / shutdown
                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / vpn-id 1
                        configurations.append_line(attributes.format('vpn-id {vpn_id}'))

                        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp (config-l2vpn)
                        ns, attributes2 = attributes.namespace('autodiscovery_bgp')
                        if ns:
                            configurations.append_block(ns.build_config(apply=False, unconfig=unconfig, attributes=attributes2))

                elif self.xconnect_type is _Xconnect.Type.p2p:
                    # iosxr: l2vpn / xconnect group someword / p2p someword2 (config-l2vpn)
                    with configurations.submode_context(attributes.format('p2p {name}', force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / backup interface Bundle-Ether1

                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / description someword3
                        configurations.append_line(attributes.format('description {description}'))

                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / interface Bundle-Ether1
                        for interface, attributes2 in attributes.sequence_values('interfaces', sort=True):
                            configurations.append_line('interface {}'.\
                                                  format(interface.name))

                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / interworking ethernet
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / interworking ipv4
                        configurations.append_line(attributes.format('interworking {interworking}'))

                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / monitor-session someword3

                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor 1.2.3.4 pw-id 1 (config-l2vpn)
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv4 1.2.3.4 pw-id 1 (config-l2vpn)
                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor ipv6 1:2::3 pw-id 1 (config-l2vpn)
                        for sub, attributes2 in attributes.mapping_values('neighbor_attr', keys=self.pseudowire_neighbors, sort=True):
                            configurations.append_block(
                                sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                        # iosxr: l2vpn / xconnect group someword / p2p someword2 / neighbor evpn evi 1 target 1 source 1

                else:
                    warnings.warn(
                        'xconnect type mode {}'.format(self.xconnect_type),
                        UnsupportedAttributeWarning)

            submode_stack.close()
            if apply:
                if configurations:
                    self.device.configure(str(configurations), fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

