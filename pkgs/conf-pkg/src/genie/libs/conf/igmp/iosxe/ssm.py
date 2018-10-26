'''
IOSXE specific configurations for Ssm feature object.
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
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # ===================================
        # ssm_group_policy
        # ssm_source_addr
        # ===================================

        # get vrf info
        vrf = kwargs['vrf']

        if vrf == 'default':
            cmd_str = 'ip igmp'
        else:
            cmd_str = 'ip igmp vrf {}'.format(vrf)

        if attributes.value('ssm_group_policy') and \
           attributes.value('ssm_source_addr'):

            cmd_str += ' ssm-map static {ssm_group_policy} {ssm_source_addr}'
            configurations.append_line(attributes.format(cmd_str))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)
