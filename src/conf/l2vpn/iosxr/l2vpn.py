
from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder


class L2vpn(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: l2vpn (config-l2vpn)
            with configurations.submode_context('l2vpn'):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # iosxr: l2vpn / autodiscovery bgp (config-l2vpn-ad)
                # iosxr: l2vpn / autodiscovery bgp / signaling-protocol bgp (config-l2vpn-ad-sig)
                # iosxr: l2vpn / autodiscovery bgp / signaling-protocol bgp / mtu mismatch ignore

                # iosxr: l2vpn / bridge group someword (config-l2vpn-bg)
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 (config-l2vpn-bg-bd)
                for bd, attributes2 in attributes.sequence_values('bridge_domains'):
                    configurations.append_block(
                        str(bd.build_config(apply=False, attributes=attributes2, unconfig=unconfig,
                                        contained=True)))

                # iosxr: l2vpn / capability high-mode
                # iosxr: l2vpn / capability single-mode
                # iosxr: l2vpn / description someword

                # iosxr: l2vpn / ethernet ring g8032 someword (config-l2vpn)
                for ring, attributes2 in attributes.sequence_values('g8032_rings'):
                    configurations.append_block(
                        str(ring.build_config(apply=False, attributes=attributes2, unconfig=unconfig)))

                # iosxr: l2vpn / flexible-xconnect-service vlan-unaware someword (config-l2vpn)
                # iosxr: l2vpn / flexible-xconnect-service vlan-unaware someword / interface Bundle-Ether1
                # iosxr: l2vpn / flexible-xconnect-service vlan-unaware someword / neighbor evpn evi 1 target 1
                # iosxr: l2vpn / flexible-xconnect-service vlan-unaware someword / neighbor evpn evi 1 target 1 source 1

                # iosxr: l2vpn / ignore-mtu-mismatch
                # iosxr: l2vpn / load-balancing flow src-dst-ip
                # iosxr: l2vpn / load-balancing flow src-dst-mac
                # iosxr: l2vpn / logging (config-l2vpn)
                # iosxr: l2vpn / logging / bridge-domain
                # iosxr: l2vpn / logging / nsr
                # iosxr: l2vpn / logging / pseudowire
                # iosxr: l2vpn / logging / pwhe-replication disable
                # iosxr: l2vpn / logging / vfi
                # iosxr: l2vpn / neighbor all ldp flap

                # iosxr: l2vpn / pbb (config-l2vpn)
                ns, attributes2 = attributes.namespace('pbb')
                if ns is not None:
                    configurations.append_block(
                        str(ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig)))

                # iosxr: l2vpn / pw-class someword (config-l2vpn)
                for pwc, attributes2 in attributes.sequence_values('pseudowire_classes'):
                    configurations.append_block(
                        str(pwc.build_config(apply=False, attributes=attributes2, unconfig=unconfig,
                                         contained=True)))

                # iosxr: l2vpn / pw-grouping
                # iosxr: l2vpn / pw-oam refresh transmit 1
                # iosxr: l2vpn / pw-routing (config-l2vpn)
                # iosxr: l2vpn / pw-routing / bgp (config-l2vpn)
                # iosxr: l2vpn / pw-routing / bgp / rd 100:200000
                # iosxr: l2vpn / pw-routing / bgp / rd 65536:200
                # iosxr: l2vpn / pw-routing / bgp / rd 1.2.3.4:1
                # iosxr: l2vpn / pw-routing / global-id 1
                # iosxr: l2vpn / pw-status disable

                # iosxr: l2vpn / redundancy (config-l2vpn)
                # iosxr: l2vpn / redundancy / iccp group 1 (config-l2vpn)
                # See IccpGroup objects

                # iosxr: l2vpn / router-id 1.2.3.4
                configurations.append_line(attributes.format('router-id {router_id}'))

                # iosxr: l2vpn / snmp mib interface format external
                # iosxr: l2vpn / snmp mib pseudowire statistics
                # iosxr: l2vpn / tcn-propagation

                # iosxr: l2vpn / xconnect group someword (config-l2vpn)
                # iosxr: l2vpn / xconnect group someword / mp2mp someword2 (config-l2vpn)
                # iosxr: l2vpn / xconnect group someword / p2p someword2 (config-l2vpn)
                for xc, attributes2 in attributes.sequence_values('xconnects'):
                    configurations.append_block(
                        str(xc.build_config(apply=False, attributes=attributes2, unconfig=unconfig,
                                        contained=True)))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class PbbAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: l2vpn / pbb (config-l2vpn)
                if attributes.value('enabled', force=True):
                    with configurations.submode_context('pbb'):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # iosxr: l2vpn / pbb / backbone-source-mac aaaa.bbbb.cccc
                        configurations.append_line(attributes.format('backbone-source-mac {backbone_source_mac}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

