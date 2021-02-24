'''
NXOS specific configurations for IPv4Addr feature object.
'''

# Python
from abc import ABC

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning,\
                                       AttributesHelper


class IPv4Addr(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs, kwargs
        assert not apply
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # ===================================
        # ipv4
        # prefix_length
        # ipv4_secondary
        # route_tag
        # secondary_vrf
        # ===================================

        if attributes.value('ipv4') and attributes.value('prefix_length'):
            if attributes.value('ipv4_secondary'):
                configurations.append_line('ip address'
                    ' {ipv4}/{prefix_length} secondary'
                    .format(ipv4=attributes.value('ipv4'),
                        prefix_length=attributes.value('prefix_length')))
                if attributes.value('tag'):
                    configurations.append_line('ip address'
                        ' {ipv4}/{prefix_length} secondary'
                        ' tag {route_tag}'
                        .format(ipv4=attributes.value('ipv4'), 
                            prefix_length=attributes.value('prefix_length'),
                            route_tag=attributes.value('route_tag')))
            elif attributes.value('tag'):
                    configurations.append_line('ip address'
                        ' {ipv4}/{prefix_length}'
                        ' tag {route_tag}'
                        .format(ipv4=attributes.value('ipv4'), 
                            prefix_length=attributes.value('prefix_length'),
                            route_tag=attributes.value('route_tag')))
            else:
                configurations.append_line('ip address'
                    ' {ipv4}/{prefix_length}'
                    .format(ipv4=attributes.value('ipv4'), 
                        prefix_length=attributes.value('prefix_length')))
        if not attributes.value('redirect'):
            configurations.append_line('no ip redirects')

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True)
