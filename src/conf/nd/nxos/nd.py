"""
Implement NXOS Specific Configurations for Nd objects.
"""

# Table of contents:
#     class Nd:
#         class DeviceAttributes:
#             class InterfaceAttributes:
#                 class NeighborAttributes:

# Python
from abc import ABC
# Genie package
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder

class Nd(ABC):

    class DeviceAttributes(ABC):
        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # InterfaceAttributes
            with configurations.submode_context(attributes.format(
                    'interface {interface}', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                for sub, attributes2 in attributes.mapping_values('interface_attr',
                                                                  sort=True,
                                                                  keys=self.interface_attr):
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

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                if attributes.value('if_ra_interval'):
                    configurations.append_line(
                        attributes.format('ipv6 nd ra-interval {if_ra_interval}'))
                if attributes.value('if_ra_lifetime'):
                    configurations.append_line(
                        attributes.format('ipv6 nd ra-lifetime {if_ra_lifetime}'))
                if attributes.value('if_ra_suppress') == True:
                    configurations.append_line(
                        attributes.format('ipv6 nd suppress-ra'))

                # NeighborAttributes
                for sub, attributes2 in attributes.mapping_values('neighbor_attr',
                                                                  sort=True,
                                                                  keys=self.neighbor_attr):
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

            class NeighborAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False,
                                 **kwargs):
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    if attributes.value('ip') and attributes.value('link_layer_address'):
                        configurations.append_line(attributes.format('ipv6 neighbor {ip} {link_layer_address}'))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)
