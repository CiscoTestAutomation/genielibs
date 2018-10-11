''' 
OSPF Genie Conf Object Implementation for IOSXE:
    - AreaNetwork multi-line configuration implementation for IOSXE - CLI
'''

# Python
import warnings
from abc import ABC

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class AreaNetwork(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # Get area information
        area = kwargs['area']

        # router ospf 1
        #   network 192.168.1.0 0.0.0.0 area 2
        #   network 192.168.1.1 1.1.1.1 area 3
        if attributes.value('area_network') and attributes.value('area_network_wildcard'):

            # network 192.168.1.0 0.0.0.0
            an_str = 'network {area_network} {area_network_wildcard}'

            # + area 2
            an_str += ' area {}'.format(area)
            
            configurations.append_line(attributes.format(an_str))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)