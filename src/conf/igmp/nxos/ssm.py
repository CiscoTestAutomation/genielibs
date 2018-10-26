'''
NXOS specific configurations for Ssm feature object.
'''

# Python
import warnings
from abc import ABC

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning,\
                                       AttributesHelper


class Ssm(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # ===================================
        # ssm_group_range
        # ssm_source_addr
        # ===================================

        if attributes.value('ssm_group_range') and \
           attributes.value('ssm_source_addr'):
           
            configurations.append_line(
                attributes.format('ip igmp ssm-translate '
                                  '{ssm_group_range} {ssm_source_addr}'))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)
