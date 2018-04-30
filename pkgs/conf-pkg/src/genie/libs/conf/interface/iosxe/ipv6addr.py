'''
IOSXE specific configurations for IPv6Addr feature object.
'''

# Python
from abc import ABC

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning,\
                                       AttributesHelper


class IPv6Addr(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs, kwargs
        assert not apply
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # ===================================
        # ipv6
        # ipv6_prefix_length
        # ipv6_anycast
        # ipv6_eui_64
        # ===================================

        #  ipv6 address <ipv6prefix> [ anycast | eui-64 ]
        if attributes.value('ipv6') and attributes.value('ipv6_prefix_length'):

            cmd = 'ipv6 address {ipv6}/{ipv6_prefix_length}'.\
                    format(ipv6=attributes.value('ipv6'),
                           ipv6_prefix_length=attributes.value('ipv6_prefix_length'))

            if attributes.value('ipv6_eui_64'):
                cmd += ' eui-64'
            elif attributes.value('ipv6_anycast'):
                cmd += ' anycast'

            configurations.append_line(cmd)

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True)
