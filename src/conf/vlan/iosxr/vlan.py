"""Implement IOSXR (iosxr) Specific Configurations for Vlan objects.
"""

# Table of contents:
#     class Vlan:
#         class DeviceAttributes:
#             class AccessMapAttributes:
#             class VlanConfigurationAttributes:
#             class InterfaceAttributes:

# Python
from abc import ABC

# Genie package
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base import Interface
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder


class Vlan(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            for sub, attributes2 in attributes.mapping_values(
                    'access_map_attr',
                    keys=self.access_map_attr):
                configurations.append_block(
                    sub.build_config(apply=False, attributes=attributes2,
                                     unconfig=unconfig, **kwargs))

            for sub, attributes2 in attributes.mapping_values(
                        'vlan_configuration_attr',
                        keys=self.vlan_configuration_attr):
                configurations.append_block(
                    sub.build_config(apply=False, attributes=attributes2,
                                     unconfig=unconfig, **kwargs))

            for sub, attributes2 in attributes.mapping_values(
                    'interface_attr',
                    keys=self.interface_attr.keys()):
                configurations.append_block(
                    sub.build_config(apply=False, attributes=attributes2,
                                     unconfig=unconfig, **kwargs))

            if apply:
                if configurations:
                    self.device.configure(str(configurations),
                                          fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        class AccessMapAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

        class VlanConfigurationAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)

                if attributes.value('eth_encap_type1'):
                    self.interface.eth_encap_type1 = \
                        attributes.value('eth_encap_type1')

                if attributes.value('eth_encap_val1'):
                    self.interface.eth_encap_val1 = \
                        attributes.value('eth_encap_val1')

                if attributes.value('eth_encap_type2'):
                    self.interface.eth_encap_type2 = \
                        attributes.value('eth_encap_type2')

                if attributes.value('eth_encap_val2'):
                    self.interface.eth_encap_val2 = \
                        attributes.value('eth_encap_val2')

                if unconfig:
                    if attributes.attributes is not None:
                        configurations = \
                            self.interface.build_unconfig(
                                apply=False,
                                attributes=attributes.attributes)
                    else:
                        configurations = \
                            self.interface.build_unconfig(
                                apply=False,
                                attributes={'eth_encap_type1': None,
                                            'eth_encap_val1': None,
                                            'eth_encap_type2': None,
                                            'eth_encap_val2': None})
                else:
                    # self.interface.build_config always calls cliconfig method
                    # A fix is needed in Genie infrastructure to fix that
                    # context abstraction issue.
                    configurations = self.interface.build_config(apply=False)

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)
