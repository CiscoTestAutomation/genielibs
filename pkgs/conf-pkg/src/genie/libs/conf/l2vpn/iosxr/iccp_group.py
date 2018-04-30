
from abc import ABC
import warnings
import contextlib

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder


class IccpGroup(ABC):

    class DeviceAttributes(ABC):

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: l2vpn / redundancy / iccp group 1 / interface Bundle-Ether1 (config-l2vpn)
                with configurations.submode_context(attributes.format('interface {interface_name}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: l2vpn / redundancy / iccp group 1 / interface Bundle-Ether1 / mac-flush stp-tcn
                    configurations.append_line(attributes.format('mac-flush {mac_flush}'))

                    # iosxr: l2vpn / redundancy / iccp group 1 / interface Bundle-Ether1 / primary vlan someword
                    configurations.append_line(attributes.format('primary vlan {primary_vlan}'))

                    # iosxr: l2vpn / redundancy / iccp group 1 / interface Bundle-Ether1 / recovery delay 30
                    configurations.append_line(attributes.format('recovery delay {recovery_delay}'))

                    # iosxr: l2vpn / redundancy / iccp group 1 / interface Bundle-Ether1 / secondary vlan someword
                    configurations.append_line(attributes.format('secondary vlan {secondary_vlan}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: l2vpn (config-l2vpn)
            # iosxr: l2vpn / redundancy (config-l2vpn)
            # iosxr: redundancy (config-redundancy)
            # NOTE:
            #   Starting in release 6.2.1, redundancy is not under l2vpn
            #   submode anymore; Enter l2vpn+redundancy but exit back root in
            #   case parser automatically went up one level.
            #with configurations.submode_context('l2vpn', cancel_empty=True, exit_cmd=None), \
            #        configurations.submode_context('redundancy', cancel_empty=True, exit_cmd='root'):
            with configurations.submode_context('redundancy', cancel_empty=True):

                # iosxr: l2vpn / redundancy / iccp group 1 (config-l2vpn)
                with configurations.submode_context(attributes.format('iccp group {group_id}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: l2vpn / redundancy / iccp group 1 / backbone (config-redundancy-group-iccp-backbone)
                    with configurations.submode_context('backbone', cancel_empty=True):

                        # iosxr: l2vpn / redundancy / iccp group 1 / backbone / interface <intf>
                        for sub, attributes2 in attributes.sequence_values('backbone_interfaces', sort=True):
                            configurations.append_line('interface {sub.name}'.format(sub=sub))

                    # iosxr: l2vpn / redundancy / iccp group 1 / interface Bundle-Ether1 (config-l2vpn)
                    for sub, attributes2 in attributes.mapping_values('interface_attr', keys=self.interfaces, sort=True):
                        configurations.append_block(
                            sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                    # iosxr: l2vpn / redundancy / iccp group 1 / isolation recovery-delay 30
                    configurations.append_line(attributes.format('isolation recovery-delay {isolation_recovery_delay}'))

                    # iosxr: l2vpn / redundancy / iccp group 1 / member (config-redundancy-group-iccp-member)
                    # iosxr: l2vpn / redundancy / iccp group 1 / member / neighbor 1.2.3.4

                    # iosxr: l2vpn / redundancy / iccp group 1 / mlacp connect timeout 0

                    # iosxr: l2vpn / redundancy / iccp group 1 / mlacp node 0
                    configurations.append_line(attributes.format('mlacp node {mlacp_node_id}'))

                    # iosxr: l2vpn / redundancy / iccp group 1 / mlacp system mac aaaa.bbbb.cccc
                    configurations.append_line(attributes.format('mlacp system mac {mlacp_system_mac}'))

                    # iosxr: l2vpn / redundancy / iccp group 1 / mlacp system priority 1
                    configurations.append_line(attributes.format('mlacp system priority {mlacp_system_priority}'))

                    # iosxr: l2vpn / redundancy / iccp group 1 / mode singleton
                    configurations.append_line(attributes.format('mode {mode}'))

                    # iosxr: l2vpn / redundancy / iccp group 1 / multi-homing node-id <0-254>
                    configurations.append_line(attributes.format('multi-homing node-id {multi_homing_node_id}'))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

