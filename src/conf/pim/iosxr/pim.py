
from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

from genie.libs.conf.vrf import VrfSubAttributes


class Pim(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: router pim (config-pim)
            with configurations.submode_context('router pim'):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                for sub, attributes2 in attributes.mapping_values('vrf_attr', keys=self.vrf_attr, sort=True):
                    configurations.append_block(
                        sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class VrfAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: router pim / vrf someword (config-pim-<vrf>)
                with configurations.submode_context(
                        None if self.vrf_name == 'default' else attributes.format('vrf {vrf_name}', force=True)):
                    if self.vrf_name != 'default' and unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    for sub, attributes2 in attributes.mapping_values('address_family_attr', keys=self.address_family_attr, sort=True):
                        configurations.append_block(
                            sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class AddressFamilyAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # iosxr: router pim / [vrf someword] / address-family ipv4 (config-pim-<vrf>-ipv4)
                    # iosxr: router pim / [vrf someword] / address-family ipv6 (config-pim-<vrf>-ipv6)
                    with configurations.submode_context(attributes.format('address-family {address_family.name}', force=True)):

                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / accept-register someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / allow-rp
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / allow-rp group-list someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / allow-rp rp-list someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / allow-rp rp-list someword group-list someword2
                        # iosxr: router pim / address-family ipv4 / auto-rp candidate-rp GigabitEthernet0/0/0/0 scope 1
                        # iosxr: router pim / address-family ipv4 / auto-rp candidate-rp GigabitEthernet0/0/0/0 scope 1 bidir
                        # iosxr: router pim / address-family ipv4 / auto-rp candidate-rp GigabitEthernet0/0/0/0 scope 1 group-list someword
                        # iosxr: router pim / address-family ipv4 / auto-rp candidate-rp GigabitEthernet0/0/0/0 scope 1 group-list someword bidir
                        # iosxr: router pim / address-family ipv4 / auto-rp candidate-rp GigabitEthernet0/0/0/0 scope 1 group-list someword interval 1
                        # iosxr: router pim / address-family ipv4 / auto-rp candidate-rp GigabitEthernet0/0/0/0 scope 1 group-list someword interval 1 bidir
                        # iosxr: router pim / address-family ipv4 / auto-rp candidate-rp GigabitEthernet0/0/0/0 scope 1 interval 1
                        # iosxr: router pim / address-family ipv4 / auto-rp candidate-rp GigabitEthernet0/0/0/0 scope 1 interval 1 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / auto-rp listen disable
                        # iosxr: router pim / address-family ipv4 / auto-rp mapping-agent GigabitEthernet0/0/0/0 scope 1
                        # iosxr: router pim / address-family ipv4 / auto-rp mapping-agent GigabitEthernet0/0/0/0 scope 1 interval 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / auto-rp relay vrf someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / auto-rp relay vrf someword listen
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-bsr 1.2.3.4
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-bsr 1.2.3.4 hash-mask-len <0-32>
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-bsr 1.2.3.4 hash-mask-len <0-32> priority 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-bsr 1.2.3.4 priority 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 group-list someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 group-list someword bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 group-list someword interval 30
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 group-list someword interval 30 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 group-list someword interval 30 priority 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 group-list someword interval 30 priority 1 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 group-list someword priority 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 group-list someword priority 1 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 interval 30
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 interval 30 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 interval 30 priority 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 interval 30 priority 1 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 priority 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / bsr candidate-rp 1.2.3.4 priority 1 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-bsr 1:2::3
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-bsr 1:2::3 hash-mask-len <0-128>
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-bsr 1:2::3 hash-mask-len <0-128> priority 1
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-bsr 1:2::3 priority 1
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 group-list someword
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 group-list someword bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 group-list someword interval 30
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 group-list someword interval 30 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 group-list someword interval 30 priority 1
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 group-list someword interval 30 priority 1 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 group-list someword priority 1
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 group-list someword priority 1 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 interval 30
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 interval 30 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 interval 30 priority 1
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 interval 30 priority 1 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 priority 1
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / bsr candidate-rp 1:2::3 priority 1 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / bsr relay vrf someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / bsr relay vrf someword listen
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / convergence link-down-prune-delay <0-60>
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / convergence rpf-conflict-join-delay <0-15>
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / convergence-timeout 1800
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / dr-priority <0-4294967295>
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / embedded-rp 1:2::3 someword
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / embedded-rp disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / explicit-rpf-vector inject 1.2.3.4 masklen <0-32> 1.2.3.4 ...
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / explicit-rpf-vector inject 1:2::3 masklen <0-32> 1.2.3.4 ...
                        # iosxr: router pim / address-family ipv4|ipv6 / global maximum bsr crp-cache 1
                        # iosxr: router pim / address-family ipv4|ipv6 / global maximum bsr crp-cache 1 threshold 1
                        # iosxr: router pim / address-family ipv4 / global maximum group-mappings autorp 1
                        # iosxr: router pim / address-family ipv4 / global maximum group-mappings autorp 1 threshold 1
                        # iosxr: router pim / address-family ipv4|ipv6 / global maximum group-mappings bsr 1
                        # iosxr: router pim / address-family ipv4|ipv6 / global maximum group-mappings bsr 1 threshold 1
                        # iosxr: router pim / address-family ipv4|ipv6 / global maximum packet-queue high-priority <0-2147483648>
                        # iosxr: router pim / address-family ipv4|ipv6 / global maximum packet-queue low-priority <0-2147483648>
                        # iosxr: router pim / address-family ipv4|ipv6 / global maximum register-states <0-75000>
                        # iosxr: router pim / address-family ipv4|ipv6 / global maximum register-states <0-75000> threshold <0-0>
                        # iosxr: router pim / address-family ipv4|ipv6 / global maximum route-interfaces 1
                        # iosxr: router pim / address-family ipv4|ipv6 / global maximum route-interfaces 1 threshold 1
                        # iosxr: router pim / address-family ipv4|ipv6 / global maximum routes 1
                        # iosxr: router pim / address-family ipv4|ipv6 / global maximum routes 1 threshold 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / hello-interval 1

                        for sub, attributes2 in attributes.mapping_values('interface_attr', keys=self.interface_attr, sort=True):
                            configurations.append_block(
                                sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / join-prune-interval 10
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / join-prune-mtu 576
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / log neighbor changes
                        # iosxr: router pim / address-family ipv4 / maximum autorp mapping-agent-cache 1
                        # iosxr: router pim / address-family ipv4 / maximum autorp mapping-agent-cache 1 threshold 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / maximum bsr crp-cache 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / maximum bsr crp-cache 1 threshold 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / maximum group-mappings autorp 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / maximum group-mappings autorp 1 threshold 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / maximum group-mappings bsr 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / maximum group-mappings bsr 1 threshold 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / maximum register-states <0-75000>
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / maximum register-states <0-75000> threshold <0-0>
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / maximum route-interfaces 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / maximum route-interfaces 1 threshold 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / maximum routes 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / maximum routes 1 threshold 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp (config-pim-<vrf>-<af>-mdt-cmcast)
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / announce-pim-join-tlv
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / mdt-hello enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / migration
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / migration route-policy someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / shared-tree-prune-delay <0-1800>
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / source-tree-prune-delay <0-300>
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / suppress-pim-data-signaling
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / suppress-shared-tree-join
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability connector disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability connector disable source-as disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability connector disable source-as disable vrf-route-import disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability connector disable source-as disable vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability connector disable source-as enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability connector disable source-as enable vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability connector disable vrf-route-import disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability connector disable vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability connector enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability connector enable source-as enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability connector enable source-as enable vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability connector enable vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability source-as disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability source-as disable vrf-route-import disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability source-as disable vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability source-as enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability source-as enable vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability vrf-route-import disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing bgp / unicast-reachability vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim (config-pim-<vrf>-<af>-mdt-cmcast)
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / announce-pim-join-tlv
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / migration
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / migration route-policy someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / shared-tree-prune-delay <0-1800>
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / source-tree-prune-delay <0-300>
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / suppress-pim-data-signaling
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / suppress-shared-tree-join
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability connector disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability connector disable source-as disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability connector disable source-as disable vrf-route-import disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability connector disable source-as disable vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability connector disable source-as enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability connector disable source-as enable vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability connector disable vrf-route-import disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability connector disable vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability connector enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability connector enable source-as enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability connector enable source-as enable vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability connector enable vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability source-as disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability source-as disable vrf-route-import disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability source-as disable vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability source-as enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability source-as enable vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability vrf-route-import disable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt c-multicast-routing pim / unicast-reachability vrf-route-import enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt data announce-interval 3
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt data max-aggregation 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt data switchover-interval 3
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / mdt neighbor-filter someword
                        # iosxr: router pim / address-family ipv4|ipv6 / mdt-hello-interval 1
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / mofrr (config-pim-<vrf>-ipv4-mofrr)
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / mofrr / clone join 1.2.3.4 to 1.2.3.4 and 1.2.3.4 masklen <0-32>
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / mofrr / clone source 1.2.3.4 to 1.2.3.4 and 1.2.3.4 masklen <0-32>
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / mofrr / flow someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / mofrr / non-revertive
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / mofrr / rib someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / neighbor-check-on-recv enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / neighbor-check-on-send enable
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / neighbor-filter someword
                        # iosxr: router pim / address-family ipv4|ipv6 / nsf lifetime 10
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / old-register-checksum
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / override-interval 400
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / propagation-delay 100
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / register-source GigabitEthernet0/0/0/0

                        # iosxr: router pim / [vrf someword] / address-family ipv4 / rp-address 1.2.3.4
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / rp-address 1.2.3.4 someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / rp-address 1.2.3.4 someword bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / rp-address 1.2.3.4 someword override
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / rp-address 1.2.3.4 someword override bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / rp-address 1.2.3.4 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / rp-address 1.2.3.4 override
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / rp-address 1.2.3.4 override bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / rp-address 1:2::3
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / rp-address 1:2::3 someword
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / rp-address 1:2::3 someword bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / rp-address 1:2::3 someword override
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / rp-address 1:2::3 someword override bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / rp-address 1:2::3 bidir
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / rp-address 1:2::3 override
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / rp-address 1:2::3 override bidir
                        configurations.append_line(attributes.format('rp-address {rp_address}'))

                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / rp-static-deny someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / rpf topology route-policy someword
                        # iosxr: router pim / address-family ipv4 / rpf-redirect route-policy someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / rpf-vector
                        # iosxr: router pim / [vrf someword] / address-family ipv4 / rpf-vector inject 1.2.3.4 masklen <0-32> 1.2.3.4 ...
                        # iosxr: router pim / [vrf someword] / address-family ipv6 / rpf-vector inject 1:2::3 masklen <0-32> 1.2.3.4 ...
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / sg-expiry-timer 40
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / sg-expiry-timer 40 sg-list someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / spt-threshold infinity
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / spt-threshold infinity group-list someword
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / suppress-data-registers
                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / suppress-rpf-change-prunes

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

                class InterfaceAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                        assert not apply
                        assert not kwargs, kwargs
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 (config-pim-<af>-if)
                        with configurations.submode_context(attributes.format('interface {interface_name}', force=True)):
                            if unconfig and attributes.iswildcard:
                                configurations.submode_unconfig()

                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / bfd fast-detect
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / bfd minimum-interval 3
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / bfd multiplier 2
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / bsr-border
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / disable
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / dr-priority <0-4294967295>
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / enable
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / hello-interval 1
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / join-prune-interval 10
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / join-prune-mtu 576
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / maximum route-interfaces 1
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / maximum route-interfaces 1 someword
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / maximum route-interfaces 1 threshold 1
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / maximum route-interfaces 1 threshold 1 someword
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / neighbor-filter someword
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / override-interval 400
                            # iosxr: router pim / [vrf someword] / address-family ipv4|ipv6 / interface GigabitEthernet0/0/0/0 / propagation-delay 100
                            # iosxr: router pim / address-family ipv4 / interface GigabitEthernet0/0/0/0 / rpf-redirect bundle someword
                            # iosxr: router pim / address-family ipv4 / interface GigabitEthernet0/0/0/0 / rpf-redirect bundle someword bandwidth <0-100000000> threshold <0-100000000>

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

