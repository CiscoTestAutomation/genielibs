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
from enum import Enum

from genie.conf.base.attributes import UnsupportedAttributeWarning, AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
import genie.conf.base.interface
from genie.conf.base.config import CliConfig
from genie.decorator import managedattribute

class Evpn(ABC):

    class InterfaceAttributes(ABC):

        evpn_multihoming_core_tracking = managedattribute(
            name='evpn_multihoming_core_tracking',
            type=bool,
            read_only=False,
            doc="EVPN multihoming core tracking for the interface."
        )
        
        ethernet_segment_intf = managedattribute(
            name='ethernet_segment_intf',
            type=bool,
            read_only=False,
            doc="EVPN ethernet-segment multihoming access facing interface."
        )

        system_mac = managedattribute(
            name='system_mac',
            type=str,
            read_only=False,
            doc="System MAC address for the ESI."
        )

        local_discriminator = managedattribute(
            name='local_discriminator',
            type=int,
            read_only=False,
            doc="Local discriminator for the ESI."
        )

        esi_tag = managedattribute(
            name='esi_tag',
            type=int,
            read_only=False,
            doc="Tag for the ESI."
        )        

        def build_config(self, apply=True, attributes=None,
                            unconfig=False, **kwargs):
            assert not apply
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            with configurations.submode_context(
                attributes.format('interface {interface_name}',
                                    force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # interface Ethernet1/1 / evpn multihoming core-tracking
                if attributes.value('evpn_multihoming_core_tracking'):
                    configurations.append_line(
                        attributes.format('evpn multihoming core-tracking'), unconfig_cmd='no evpn multihoming core-tracking')
                
                if attributes.value('ethernet_segment_intf'):

                    # interface port-channel1 / switchport
                    configurations.append_line(
                        attributes.format('switchport'))    
                      
                    # interface port-channel1 / ethernet-segment
                    with configurations.submode_context('ethernet-segment'):
                        if attributes.value('local_discriminator'):
                            if attributes.value('system_mac'):

                                # interface port-channel1 / ethernet-segment / esi system-mac <system-mac> <local-discriminator>
                                configurations.append_line(attributes.format('esi system-mac {system_mac} {local_discriminator}'))

                            else:
                                # interface port-channel1 / ethernet-segment / esi system-mac <local-discriminator>                                
                                configurations.append_line(attributes.format('esi system-mac {local_discriminator}'))      

                        elif attributes.value('esi_tag'):
                            # interface port-channel1 / ethernet-segment / esi <esi_tag>
                            configurations.append_line(attributes.format('esi {esi_tag}'))       
            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None,
                            **kwargs):
            return self.build_config(apply=apply,
                                        attributes=attributes,
                                        unconfig=True, **kwargs)

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

        # evpn_mode # node01(config)# evpn multihoming 

        multi_homing_enabled = managedattribute(
            name='multi_homing_enabled',
            default=None,
            type=(None, managedattribute.test_istype(bool)),
            doc="Enable Evpn Multihoming feature.")
        
        class DfElectionMode(Enum):
            mode1 = 'modulo'
            mode2 = 'per-flow'
            
        evpn_mutihoming_df_election = managedattribute(
            name = 'evpn_mutihoming_df_election',
            type = (None, DfElectionMode),
            default = None,
            doc = "DF election mode for EVPN multihoming"
        )

        evpn_multihoming_es_delay_restore_time = managedattribute(
            name = 'evpn_multihoming_es_delay_restore_time',
            type = int,
            default = None,
            doc = 'Delay restore time for EVPN multihoming ethernet segment'
        )

        evpn_multihoming_global_system_mac = managedattribute(
            name = 'evpn_multihoming_global_system_mac',
            type = str,
            default = None,
            doc = 'EVPN Multi homing system mac configured at global level'
        )

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # nxos: evpn multihoming
            if attributes.value('multi_homing_enabled'):
                with configurations.submode_context(attributes.format(
                        'evpn multihoming', force=True)):
                    
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()
                    if attributes.value('evpn_mutihoming_df_election') == 'modulo':
                        # nxos: evpn multihoming / df-election mode modulo
                        configurations.append_line('df-election mode modulo', unconfig_cmd='no df-election mode modulo')

                    if attributes.value('evpn_mutihoming_df_election') == 'per-flow':
                        # nxos: evpn multihoming / df-election mode per-flow
                        configurations.append_line('df-election mode per-flow', unconfig_cmd='no df-election mode per-flow')

                    if attributes.value('evpn_multihoming_es_delay_restore_time'):
                        # nxos: evpn multihoming / ethernet-segment delay-restore time 45
                        configurations.append_line(attributes.format('ethernet-segment delay-restore time {evpn_multihoming_es_delay_restore_time}'), unconfig_cmd=attributes.format('no ethernet-segment delay-restore time {evpn_multihoming_es_delay_restore_time}'))

                    if attributes.value('evpn_multihoming_global_system_mac'):
                        # nxos: evpn multihoming / system-mac aaaa.deaf.beef
                        configurations.append_line(attributes.format('system-mac {evpn_multihoming_global_system_mac}'), unconfig_cmd=attributes.format('no system-mac {evpn_multihoming_global_system_mac}'))
                
                for sub, attributes2 in attributes.mapping_values('interface_attr',
                    sort=True, keys=self.interface_attr):
                    configurations.append_block(
                        sub.build_config(apply=False,
                                        attributes=attributes2,
                                        unconfig=unconfig))

            # nxos: evpn (config-evpn)
            else:
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
        

