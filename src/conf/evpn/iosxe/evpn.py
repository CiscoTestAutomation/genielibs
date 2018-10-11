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
#             class BgpAttributes:
#                 def build_config/build_unconfig:
#             class LoadBalancingAttributes:
#                 def build_config/build_unconfig:

from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning, AttributesHelper
from genie.conf.base.cli import CliConfigBuilder

class Evpn(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, interfaces=None,
                         apply=True, attributes=None, unconfig=False, **kwargs):
            assert not apply
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            if interfaces is None:
                interfaces = set(self.interfaces)
            else:
                interfaces = set(self.interfaces).intersection(interfaces)

            with configurations.submode_context('l2vpn evpn'):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                if attributes.value('arp_flooding_suppression') is not None:
                    if attributes.value('arp_flooding_suppression') is False:
                        configurations.append('arp flooding-suppression disable')

                configurations.append_line(attributes.format('replication-type {replication_type}'))
                configurations.append_line(attributes.format('mpls label mode {label_mode}'))

            for evi, attributes2 in attributes.sequence_values('evis', sort=True):
                if unconfig:
                    configurations.append_block(evi.build_unconfig(apply=False, attributes=attributes2))
                else:
                    configurations.append_block(evi.build_config(apply=False, attributes=attributes2))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return str(configurations)

        def build_unconfig(self, *args, **kwargs):
            return self.build_config(*args, unconfig=True, **kwargs)

        class BgpAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                return str(configurations)

            def build_unconfig(self, *args, **kwargs):
                return self.build_config(*args, unconfig=True, **kwargs)

        class LoadBalancingAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                return str(configurations)

            def build_unconfig(self, *args, **kwargs):
                return self.build_config(*args, unconfig=True, **kwargs)

    class InterfaceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            return str(configurations)

        def build_unconfig(self, *args, **kwargs):
            return self.build_config(*args, unconfig=True, **kwargs)

        class EthernetSegmentAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                return str(configurations)

            def build_unconfig(self, *args, **kwargs):
                return self.build_config(*args, unconfig=True, **kwargs)

            class BgpAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    return str(configurations)

                def build_unconfig(self, *args, **kwargs):
                    return self.build_config(*args, unconfig=True, **kwargs)

