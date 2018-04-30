
from abc import ABC
import warnings
import contextlib

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

from ..bridge_domain import BridgeDomain
from ..xconnect import Xconnect
from ..vfi import Vfi
from ..pseudowire import Pseudowire as _Pseudowire, \
    PseudowireIPv4Neighbor, PseudowireIPv6Neighbor


class PseudowireClass(ABC):

    class DeviceAttributes(ABC):

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

            # iosxr: l2vpn / pw-class someword (config-l2vpn)
            with configurations.submode_context(attributes.format('pw-class {name}', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # iosxr: l2vpn / pw-class someword / backup disable delay <0-180>
                # iosxr: l2vpn / pw-class someword / backup disable never

                # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 (config-l2vpn)
                # iosxr: l2vpn / pw-class someword / encapsulation mpls (config-l2vpn)
                ns, attributes2 = attributes.namespace('encapsulation')
                if ns is not None:
                    configurations.append_block(
                        str(ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig)))

                # iosxr: l2vpn / pw-class someword / mac-withdraw
                if attributes.value('mac_withdraw'):
                    configurations.append_line('mac-withdraw')

            submode_stack.close()
            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class EncapsulationAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                if self.type is None:
                    pass
                elif self.type is _Pseudowire.EncapsulationType.l2tpv3:
                    # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 (config-l2vpn)
                    with configurations.submode_context('encapsulation l2tpv3'):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / cookie size 0
                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / cookie size 4
                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / cookie size 8
                        configurations.append_line(attributes.format('cookie size {cookie_size}'))

                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / dfbit set
                        if attributes.value('dfbit_set'):
                            configurations.append_line('dfbit set')

                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / ipv4 source 1.2.3.4
                        configurations.append_line(attributes.format('ipv4 source {ipv4_source}'))

                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / pmtu max 65535
                        configurations.append_line(attributes.format('pmtu max {pmtu_max}'))

                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / protocol l2tpv3
                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / protocol l2tpv3 class someword2
                        cfg = attributes.format('protocol {protocol.value}')
                        if cfg:
                            cfg += attributes.format('class {protocol_class}', force=True)
                            configurations.append_line(cfg)

                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / sequencing both
                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / sequencing both resync 5
                        cfg = attributes.format('sequencing {sequencing_direction}')
                        if cfg:
                            cfg += attributes.format('resync {sequencing_resync}', force=True)
                            configurations.append_line(cfg)

                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / tos reflect
                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / tos reflect value <0-255>
                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / tos value <0-255>
                        if (attributes.value('tos') is not None or
                                attributes.value('tos_reflect')):
                            cfg = ' tos'
                            if attributes.value('tos_reflect', force=True):
                                cfg += ' reflect'
                            cfg += attributes.format(' value {tos}', force=True)
                            configurations.append_line(cfg)

                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / transport-mode ethernet
                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / transport-mode vlan
                        configurations.append_line(
                            attributes.format('transport-mode {transport_mode}', transform={
                                _Pseudowire.TransportMode.ethernet: 'ethernet',
                                _Pseudowire.TransportMode.vlan: 'vlan',
                            }))

                        # iosxr: l2vpn / pw-class someword / encapsulation l2tpv3 / ttl 1
                        configurations.append_line(attributes.format('ttl {ttl}'))

                elif self.type is _Pseudowire.EncapsulationType.mpls:
                    # iosxr: l2vpn / pw-class someword / encapsulation mpls (config-l2vpn)
                    with configurations.submode_context('encapsulation mpls'):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / control-word
                        if attributes.value('control_word'):
                            configurations.append_line('control-word')

                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / ipv4 source 1.2.3.4
                        configurations.append_line(attributes.format('ipv4 source {ipv4_source}'))

                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / load-balancing (config-l2vpn)
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / load-balancing / flow-label both
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / load-balancing / flow-label both static
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / load-balancing / flow-label code 17
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / load-balancing / flow-label code 17 disable
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / load-balancing / flow-label receive
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / load-balancing / flow-label receive static
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / load-balancing / flow-label transmit
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / load-balancing / flow-label transmit static
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / load-balancing / pw-label

                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / protocol ldp
                        configurations.append_line(attributes.format('protocol {protocol.value}'))

                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / redundancy (config-l2vpn)
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / redundancy / initial-delay <0-120>
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / redundancy / one-way

                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / sequencing both
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / sequencing both resync 5
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / sequencing receive
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / sequencing receive resync 5
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / sequencing transmit
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / sequencing transmit resync 5
                        cfg = attributes.format('sequencing {sequencing_direction}')
                        if cfg:
                            cfg += attributes.format('resync {sequencing_resync}', force=True)
                            configurations.append_line(cfg)

                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / switching-tlv hide

                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / tag-rewrite ingress vlan 1
                        configurations.append_line(attributes.format('tag-rewrite ingress vlan {tag_rewrite_ingress_vlan}'))

                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / transport-mode ethernet
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / transport-mode vlan
                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / transport-mode vlan passthrough
                        configurations.append_line(
                            attributes.format('transport-mode {transport_mode}', transform={
                                _Pseudowire.TransportMode.ethernet: 'ethernet',
                                _Pseudowire.TransportMode.vlan: 'vlan',
                                _Pseudowire.TransportMode.vlan_passthrough: 'vlan passthrough',
                            }))

                        # iosxr: l2vpn / pw-class someword / encapsulation mpls / vccv verification-type none
                        configurations.append_line(attributes.format('vccv verification-type {vccv_verification_type}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

