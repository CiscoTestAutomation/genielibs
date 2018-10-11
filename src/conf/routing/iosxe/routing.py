"""
Implement IOSXE (iosxe) Specific Configurations for Route objects.
"""

# Routing Heirarchy
# -----------------
# Routing
#  +- DeviceAttributes

# Python
from abc import ABC

# import genie
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning,\
                                       AttributesHelper


class Routing(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            cfg_line = []
            unconfig_line = []

            # enabled
            if attributes.value('enabled'):
                if unconfig is False:
                    configurations.append_line(attributes.format('ip routing'))
                    configurations.append_line(attributes.format('ipv6 unicast routing'))

                # Make sure that only enabled was provided in attributes
                # If wildcard,  then delete everything
                elif unconfig is True and\
                     attributes.attributes == {'enabled': {True: None}} or \
                        attributes.iswildcard:
                    configurations.append_line('no ip routing', raw=True)
                    configurations.append_line('no ipv6 unicast routing', raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            # enabled_ip_routing
            elif attributes.value('enabled_ip_routing'):
                cfg_line.append('ip routing')
                unconfig_line.append('no ip routing')
            
            # enabled_ipv6_unicast_routing
            elif attributes.value('enabled_ipv6_unicast_routing'):
                cfg_line.append('ipv6 unicast routing')
                unconfig_line.append('no ipv6 unicast routing')

            if cfg_line:
                if unconfig is False:
                    configurations.append_line('\n'.join(cfg_line))
                elif unconfig is True:
                    configurations.append_line('\n'.join(unconfig_line), raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            if apply:
                if configurations:
                    self.device.configure(configurations)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply,
                                     attributes=attributes,
                                     unconfig=True, **kwargs)

