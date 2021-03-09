'''
NXOS specific configurations for IPv6Addr feature object.
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
        # ipv6_route_tag
        # ===================================

        cmd = []
        #  ipv6 address <ipv6>/<ipv6_prefix_length> [ anycast | eui64 ] [ tag <ipv6_route_tag> ]
        if attributes.value('ipv6') and attributes.value('ipv6_prefix_length'):
            cmd.append('ipv6 address {ipv6}/{ipv6_prefix_length}'.\
                format(ipv6=attributes.value('ipv6'),
                    ipv6_prefix_length=attributes.value('ipv6_prefix_length')))
            if attributes.value('ipv6_eui_64') and \
                attributes.value('ipv6_anycast') and \
                attributes.value('ipv6_route_tag'):
                cmd.append(' eui64 tag {ipv6_route_tag} anycast'.\
                    format(ipv6_route_tag=attributes.value('ipv6_route_tag')))
            elif attributes.value('ipv6_eui_64') and \
                attributes.value('ipv6_route_tag'):
                cmd.append(' eui64 tag {ipv6_route_tag}'.\
                    format(ipv6_route_tag=attributes.value('ipv6_route_tag')))
            elif attributes.value('ipv6_anycast') and \
                attributes.value('ipv6_route_tag'):
                cmd.append(' tag {ipv6_route_tag} anycast'.\
                    format(ipv6_route_tag=attributes.value('ipv6_route_tag')))
            elif attributes.value('ipv6_eui64'):
                cmd.append(' eui64')
            elif attributes.value('ipv6_anycast'):
                cmd.append(' anycast')
            elif attributes.value('ipv6_route_tag'):
                cmd.append(' tag {ipv6_route_tag}'.\
                    format(ipv6_route_tag=attributes.value('ipv6_route_tag')))
            configurations.append_line(''.join(cmd))
        if not attributes.value('redirect'):
            configurations.append_line('no ipv6 redirects')

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True)
