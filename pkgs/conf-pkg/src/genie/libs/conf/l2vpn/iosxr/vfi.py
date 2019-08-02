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

        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 (config-l2vpn-bg-bd-vfi)
        if attributes.value('virtual',force=True):
            title = attributes.format('access-vfi {name}', force=True)
        else:
            title = attributes.format('vfi {name}', force=True)

        with configurations.submode_context(title):
            if unconfig and attributes.iswildcard:
                configurations.submode_unconfig()

            sub, attributes2 = attributes.namespace('autodiscovery_bgp')
            if sub is not None:
                configurations.append_block(
                    sub.build_config(apply=False, attributes=attributes2,
                                     unconfig=unconfig))

            sub, attributes2 = attributes.namespace('multicast_p2mp')
            if sub is not None:
                configurations.append_block(
                    sub.build_config(apply=False, attributes=attributes2,
                                     unconfig=unconfig))

            # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / neighbor 1.2.3.4 pw-id 1 (config-l2vpn-bg-bd-vfi-pw)
            for sub, attributes2 in attributes.mapping_values('neighbor_attr', keys=self.pseudowire_neighbors, sort=True):
                configurations.append_block(
                        sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / shutdown
            if attributes.value('shutdown'):
                configurations.append_line('shutdown')

            # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / vpn-id 1
            configurations.append_line(attributes.format('vpn-id {vpn_id}'))

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

            # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp (config-l2vpn-bg-bd-vfi-ad)
            with configurations.submode_context('autodiscovery bgp'):
                if not attributes.value('enabled', force=True):
                    configurations.submode_cancel()

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / control-word
                if attributes.value('control_word'):
                    configurations.append_line('control-word')

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / rd 1.2.3.4:1
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / rd 100000:200
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / rd 100:200000
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / rd auto
                configurations.append_line(attributes.format('rd {rd}'))

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / route-policy export <rtepol>
                configurations.append_line(attributes.format('route-policy {export_route_policy}'))

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / route-target 1.2.3.4:1
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / route-target 100000:200
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / route-target 100:200000
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / route-target export 1.2.3.4:1
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / route-target export 100000:200
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / route-target export 100:200000
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / route-target export import 1.2.3.4:1 (bug)
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / route-target export import 100000:200 (bug)
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / route-target export import 100:200000 (bug)
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

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / route-target import 1.2.3.4:1
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / route-target import 100000:200
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / route-target import 100:200000
                for v, attributes2 in attributes.sequence_values('import_route_targets', sort=True):
                    if v not in both_route_targets:
                        cfg = 'route-target import {}'.format(v.route_target)
                        if v.stitching:
                            warnings.warn(UnsupportedAttributeWarning,
                                         'route-target export/import stitching')
                        configurations.append_line(cfg)

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol bgp (config-l2vpn-bg-bd-vfi-ad-sig)
                sub, attributes2 = attributes.namespace('signaling_protocol_bgp')
                if sub is not None:
                    configurations.append_block(
                        sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol ldp (config-l2vpn-bg-bd-vfi-ad-sig)
                sub, attributes2 = attributes.namespace('signaling_protocol_ldp')
                if sub is not None:
                    configurations.append_block(
                        sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / table-policy <rtepol>
                configurations.append_line(attributes.format('table-policy {table_policy}'))

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

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol bgp (config-l2vpn-bg-bd-vfi-ad-sig)
                with configurations.submode_context('signaling-protocol bgp'):
                    if not attributes.value('enabled', force=True):
                        configurations.submode_cancel()

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label both
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label both static
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label receive
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label receive static
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label transmit
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol bgp / load-balancing flow-label transmit static

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol bgp / ve-id 1
                    configurations.append_line(attributes.format('ve-id {ve_id}'))

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol bgp / ve-range 11
                    configurations.append_line(attributes.format('ve-range {ve_range}'))

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

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol ldp (config-l2vpn-bg-bd-vfi-ad-sig)
                with configurations.submode_context('signaling-protocol ldp'):
                    if not attributes.value('enabled', force=True):
                        configurations.submode_cancel()

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol ldp / load-balancing flow-label both
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol ldp / load-balancing flow-label both static
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol ldp / load-balancing flow-label receive
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol ldp / load-balancing flow-label receive static
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol ldp / load-balancing flow-label transmit
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol ldp / load-balancing flow-label transmit static

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol ldp / vpls-id 1.2.3.4:1
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / autodiscovery bgp / signaling-protocol ldp / vpls-id 100:200000
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

            # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / multicast p2mp (config-l2vpn-bg-bd-vfi-p2mp)
            with configurations.submode_context('multicast p2mp'):
                if not attributes.value('enabled', force=True):
                    configurations.submode_cancel()

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / multicast p2mp / signaling-protocol bgp (config-l2vpn-bg-bd-vfi-p2mp-bgp)
                #sub, attributes2 = attributes.namespace('signaling_protocol_bgp')
                #if sub is not None:
                #    configurations.append_block(
                #        sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / multicast p2mp / transport rsvp-te (config-l2vpn-bg-bd-vfi-p2mp-te)
                sub, attributes2 = attributes.namespace('transport_rsvp_te')
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

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / multicast p2mp / signaling-protocol bgp (config-l2vpn-bg-bd-vfi-ad-sig)
                with configurations.submode_context('signaling-protocol bgp'):
                    if not attributes.value('enabled', force=True):
                        configurations.submode_cancel()

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

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / multicast p2mp / transport rsvp-te (config-l2vpn-bg-bd-vfi-p2mp-te)
                with configurations.submode_context('transport rsvp-te'):
                    if not attributes.value('enabled', force=True):
                        configurations.submode_cancel()

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / multicast p2mp / transport rsvp-te / attribute-set p2mp-te someword4
                    configurations.append_line(attributes.format('attribute-set p2mp-te {attribute_set_p2mp_te}'))

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
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / neighbor 1.2.3.4 pw-id 1 (config-l2vpn-bg-bd-vfi-pw)
                assert self.ip is not None
                assert self.pw_id is not None
                nbr_ctx = attributes.format('neighbor {ip} pw-id {pw_id}', force=True)
            else:
                raise ValueError(self.neighbor)
            assert nbr_ctx
            with configurations.submode_context(nbr_ctx):

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / neighbor 1.2.3.4 pw-id 1 / dhcp ipv4 none
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / neighbor 1.2.3.4 pw-id 1 / dhcp ipv4 snoop profile someword4
                v = attributes.value('dhcp_ipv4_snooping_profile')
                if v is not None:
                    if v is False:
                        configurations.append_line('dhcp ipv4 none')
                    else:
                        configurations.append_line('dhcp ipv4 snoop profile {}'.format(v))

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / neighbor 1.2.3.4 pw-id 1 / igmp snooping profile someword4
                v = attributes.value('igmp_snooping_profile')
                if v is not None:
                    if v is False:
                        pass
                    else:
                        configurations.append_line('igmp snooping profile {}'.format(v))

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / neighbor 1.2.3.4 pw-id 1 / mld snooping profile someword4
                v = attributes.value('mld_snooping_profile')
                if v is not None:
                    if v is False:
                        pass
                    else:
                        configurations.append_line('mld snooping profile {}'.format(v))

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / neighbor 1.2.3.4 pw-id 1 / mpls static label local 16 remote 16
                remote_label = attributes.value('mpls_static_label')
                if remote_label is not None:
                    local_label = self.neighbor_attr[self.local_neighbor].mpls_static_label
                    if local_label is None:
                        warnings.warn(
                            'neighbor {!r} mpls_static_label missing'.format(self.local_neighbor),
                            UnsupportedAttributeWarning)
                    else:
                        configurations.append_line('mpls static label local {} remote {}'.\
                                              format(local_label, remote_label))

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / neighbor 1.2.3.4 pw-id 1 / pw-class someword4
                v = attributes.value('pw_class')
                if v is not None:
                    configurations.append_line('pw-class {}'.\
                                          format(v.device_attr[self.device].name))

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 / neighbor 1.2.3.4 pw-id 1 / static-mac-address aaaa.bbbb.cccc
                configurations.append_line(attributes.format('static-mac-address {static_mac_address}'))

            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)


