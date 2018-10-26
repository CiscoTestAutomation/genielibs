'''
IOSXE specific configurations for MldGroup feature object.
'''

# Python
import warnings
from abc import ABC

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning,\
                                       AttributesHelper


class MldGroup(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # ===================================
        # join_group
        # join_group_source_addr
        # static_group
        # static_group_source_addr
        # ===================================

        if attributes.value('join_group'):

            cmd_str = 'ipv6 mld join-group {join_group}'

            # build up configuration string
            if attributes.value('join_group_source_addr'):
                cmd_str += ' {join_group_source_addr}'

            configurations.append_line(attributes.format(cmd_str))

        elif attributes.value('static_group'):

            cmd_str = 'ipv6 mld static-group {static_group}'
            
            # build up configuration string
            if attributes.value('static_group_source_addr'):
                cmd_str += ' {static_group_source_addr}'

            configurations.append_line(attributes.format(cmd_str))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)
