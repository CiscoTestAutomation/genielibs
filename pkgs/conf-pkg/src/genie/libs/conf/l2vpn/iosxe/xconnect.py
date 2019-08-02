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

from genie.libs.conf.l2vpn.pseudowire import PseudowireNeighbor,\
    PseudowireIPv4Neighbor, PseudowireIPv6Neighbor
from genie.libs.conf.interface.iosxe.interface import EFPInterface, EthernetInterface

from ..xconnect import Xconnect as _Xconnect

class Xconnect(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         contained=False, **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            with configurations.submode_context(attributes.format('l2vpn xconnect context {name}', force=True, cancel_empty=True)):
                if attributes.value('redundancy_predictive'):
                    configurations.append_line('redundancy predictive enable')

                for interface, attributes2 in attributes.sequence_values('interfaces', sort=True):
                    if isinstance(interface, EFPInterface):
                        configurations.append_line('member {parent_interface} service-instance {service_instance}'.format\
                                                   (parent_interface = interface.parent_interface.name,\
                                                    service_instance = interface.service_instance))
                    elif isinstance(interface,EthernetInterface):
                        configurations.append_line('member {interface} '.format\
                                                   (interface = interface.name))

                for neighbor, neighbor_sub, neighbor_attributes in attributes.mapping_items('neighbor_attr', keys=self.pseudowire_neighbors, sort=True):
                    if getattr(neighbor,'pseudowire_interface',None) is not None:
                        if neighbor_attributes.value('redundancy_group') is None and neighbor_attributes.value('redundancy_priority') is None:
                            configurations.append_line('member %s' % neighbor.pseudowire_interface.name)
                        elif neighbor_attributes.value('redundancy_group') is not None and neighbor_attributes.value('redundancy_priority') is None:
                            configurations.append_line(neighbor_attributes.format('member %s group {redundancy_group}' % neighbor.pseudowire_interface.name,force=True))
                        elif neighbor_attributes.value('redundancy_group') is not None and neighbor_attributes.value('redundancy_priority') is not None:
                            configurations.append_line(neighbor_attributes.format('member %s group {redundancy_group} priority {redundancy_priority}' \
                                                                                   % neighbor.pseudowire_interface.name,force=True))

            if apply:
                if configurations:
                    self.device.configure(str(configurations), fail_invalid=True)
            else:
                return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class NeighborAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class AutodiscoveryBgpAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

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

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

                class CeAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False,
                                     **kwargs):
                        assert not apply
                        assert not kwargs, kwargs
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)


                    class InterfaceAttributes(ABC):

                        def build_config(self, apply=True, attributes=None, unconfig=False,
                                         **kwargs):
                            assert not apply
                            assert not kwargs, kwargs
                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            return str(configurations)

                        def build_unconfig(self, apply=True, attributes=None, **kwargs):
                            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

