'''
IOSXR specific configurations for Mroute feature object.
'''

# Python
import warnings
from abc import ABC

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning,\
                                       AttributesHelper


class Mroute(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not apply
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # ===================================
        # mroute_address/mroute_prefix_mask
        # mroute_interface_name
        # mroute_neighbor_address
        # ===================================

        if attributes.value('mroute_address') and \
            attributes.value('mroute_prefix_mask') and \
            attributes.value('mroute_interface_name') and \
            attributes.value('mroute_neighbor_address'):

            # Final config string
            configurations.append_line(attributes.format(
                'static-rpf {mroute_address} {mroute_prefix_mask}'
                ' {mroute_interface_name} {mroute_neighbor_address}'))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)
