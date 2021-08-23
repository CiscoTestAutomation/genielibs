"""
Implement NXOS Specific Configurations for Vxlan objects.
"""

# Table of contents:
#  class DeviceAttributes
#     class EvpnMsiteBgwAttributes
#     class EvpnAttributes
#         class VniAttributes
#             class RouteTargetAttributes

# Python
from abc import ABC
# Genie package
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder

class Vxlan(ABC):

    class DeviceAttributes(ABC):
        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # nxos: it enables 3 features once
            # feature nv overlay
            # feature vn-segment-vlan-based
            # feature nv overlay evpn
            if attributes.value('enabled'):
                configurations.append_line(attributes.format('feature nv overlay'))
                configurations.append_line(attributes.format('feature vn-segment-vlan-based'))
                configurations.append_line(attributes.format('nv overlay evpn'))

            # nxos: feature nv overlay
            if attributes.value('enabled_nv_overlay'):
                if not unconfig or not attributes.value('enabled_vn_segment_vlan_based') :
                    configurations.append_line(attributes.format('feature nv overlay'))

            # nxos: feature vn-segment-vlan-based
            if attributes.value('enabled_vn_segment_vlan_based'):
                if unconfig:
                    configurations.append_line(attributes.format('feature nv overlay'))
                configurations.append_line(attributes.format('feature vn-segment-vlan-based'))

            # nxos: nv overlay evpn
            if attributes.value('enabled_nv_overlay_evpn'):
                configurations.append_line('nv overlay evpn')

            # nxos: feature ngmvpn
            if attributes.value('enabled_ngmvpn'):
                configurations.append_line('feature ngmvpn')

            # nxos: advertise evpn multicast
            if attributes.value('advertise_evpn_multicast'):
                configurations.append_line('advertise evpn multicast')

            # nxos: abric forwarding anycast-gateway-mac <str>
            if attributes.value('fabric_fwd_anycast_gw_mac'):
                if not unconfig:
                    configurations.append_line(\
                        attributes.format('fabric forwarding anycast-gateway-mac {fabric_fwd_anycast_gw_mac}'))
                if unconfig and  not attributes.value('enabled_nv_overlay_evpn'):
                    configurations.append_line( \
                        attributes.format('fabric forwarding anycast-gateway-mac {fabric_fwd_anycast_gw_mac}'))

            # EvpnAttributes
            for sub, attributes2 in attributes.mapping_values('evpn_attr',
                                                              sort=True,
                                                              keys=self.evpn_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                     attributes=attributes2,
                                     unconfig=unconfig))

            # EvpnMsiteBgwAttributes
            for sub, attributes2 in attributes.mapping_values('evpn_msite_attr',
                                                              sort=True,
                                                              keys=self.evpn_msite_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                     attributes=attributes2,
                                     unconfig=unconfig))

            if apply:
                if configurations:
                    self.device.configure(configurations)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        # EvpnMsiteBgwAttributes
        class EvpnMsiteBgwAttributes(ABC):
            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                        attributes.format('evpn multisite border-gateway {evpn_msite_bgw}',
                                          force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # nxos : delay-restore time <int 30-1000>
                    if attributes.value('evpn_msite_bgw_delay_restore_time'):
                        configurations.append_line(\
                            attributes.format('delay-restore time {evpn_msite_bgw_delay_restore_time}'))

                    # nxos : dci-advertise-pip
                    if attributes.value('evpn_msite_dci_advertise_pip'):
                        configurations.append_line( \
                            attributes.format('dci-advertise-pip'))

                    # nxos: split-horizon per-site
                    if attributes.value('evpn_msite_split_horizon_per_site'):
                        configurations.append_line( \
                            attributes.format('split-horizon per-site'))


                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply,
                                         attributes=attributes,
                                         unconfig=True, **kwargs)
        # EvpnAttributes
        class EvpnAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                if unconfig and attributes.iswildcard:
                    with configurations.submode_context(
                            attributes.format('evpn',force=True)):

                        configurations.submode_unconfig()
                        for sub, attributes2 in attributes.mapping_values('vni_attr',
                                                                          sort=True,
                                                                          keys=self.vni_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))
                else:
                    with configurations.submode_context(
                            attributes.format('evpn', force=True)):
                        for sub, attributes2 in attributes.mapping_values('vni_attr',
                                                                          sort=True,
                                                                          keys=self.vni_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))

                if apply:
                    if configurations:
                        self.device.configure(configurations)
                else:
                    return CliConfig(device=self.device, unconfig=unconfig,
                                     cli_config=configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)
            # VniAttributes
            class VniAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False,
                                 **kwargs):
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)
                    if unconfig and attributes.iswildcard:
                        with configurations.submode_context(
                                attributes.format('vni {evpn_vni} l2', force=True)):

                            configurations.submode_unconfig()
                            # nxos: rd "auto"
                            if attributes.value('evpn_vni_rd'):
                                configurations.append_line(attributes.format('rd {evpn_vni_rd}'))


                            for sub, attributes2 in attributes.mapping_values('route_target_attr',
                                                                              sort=True,
                                                                              keys=self.route_target_attr):
                                configurations.append_block(
                                    sub.build_config(apply=False,
                                                     attributes=attributes2,
                                                     unconfig=unconfig))
                    else:
                        with configurations.submode_context(
                                attributes.format('vni {evpn_vni} l2', force=True)):
                            # nxos: rd "auto"
                            if attributes.value('evpn_vni_rd'):
                                configurations.append_line(attributes.format('rd {evpn_vni_rd}'))

                            for sub, attributes2 in attributes.mapping_values('route_target_attr',
                                                                              sort=True,
                                                                              keys=self.route_target_attr):
                                configurations.append_block(
                                    sub.build_config(apply=False,
                                                     attributes=attributes2,
                                                     unconfig=unconfig))

                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                     cli_config=configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)
                # RouteTargetAttributes
                class RouteTargetAttributes(ABC):
                    def build_config(self, apply=True, attributes=None, unconfig=False,
                                     **kwargs):
                        assert not apply
                        assert not kwargs, kwargs
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        if attributes.value('evpn_vni_rt') and attributes.value('evpn_vni_rt_type'):
                            configurations.append_line(\
                                attributes.format("route-target {evpn_vni_rt_type.value} {evpn_vni_rt}"))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply,
                                                 attributes=attributes,
                                                 unconfig=True, **kwargs)
