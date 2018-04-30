
from abc import ABC
import warnings
import contextlib

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

from genie.libs.conf.l2vpn.pseudowire import PseudowireNeighbor,\
    PseudowireIPv4Neighbor


class Vfi(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not apply
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # iosxe: l2vpn vfi context {name}
        with configurations.submode_context(attributes.format('l2vpn vfi context {name}', force=True)):
            if unconfig and attributes.iswildcard:
                configurations.submode_unconfig()

            # iosxr: l2vpn vfi context {name} / vpn id {vpn_id}
            assert self.vpn_id is not None
            configurations.append_line(attributes.format('vpn id {vpn_id}'))

            sub, attributes2 = attributes.namespace('autodiscovery_bgp')
            if sub is not None:
                configurations.append_block(
                    sub.build_config(apply=False, attributes=attributes2,
                                     unconfig=unconfig))

            for sub, attributes2 in attributes.mapping_values('neighbor_attr', keys=self.pseudowire_neighbors, sort=True):
                configurations.append_block(
                        str(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig)))

        return CliConfig(device=self.device, unconfig=unconfig,
                         cli_config=configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

    class AutodiscoveryBgpAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not apply
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            if attributes.value('enabled'):

                sub, attributes2 = attributes.namespace('signaling_protocol_ldp')
                if sub is not None:
                    configurations.append_block(
                        sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                sub, attributes2 = attributes.namespace('signaling_protocol_bgp')
                if sub is not None:
                    configurations.append_block(
                        sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class SignalingProtocolBgpAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context('autodiscovery bgp signaling bgp'):
                    if not attributes.value('enabled', force=True):
                        configurations.submode_cancel()

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class SignalingProtocolLdpAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context('autodiscovery bgp signaling ldp'):
                    if not attributes.value('enabled', force=True):
                        configurations.submode_cancel()

                    configurations.append_line(attributes.format('vpls-id {vpls_id}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

    class MulticastP2mpAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not apply
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class TransportRsvpTeAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

    class NeighborAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not apply
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            if isinstance(self.neighbor, PseudowireIPv4Neighbor):
                assert self.ip is not None
                if attributes.value('pw_id'):
                    configurations.append_line(attributes.format('member {ip} {pw_id} encapsulation mpls',force_ip = True))
                else:
                    configurations.append_line(attributes.format('member {ip} encapsulation mpls',force_ip = True))

            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

