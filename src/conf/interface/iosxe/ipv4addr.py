'''
IOSXE specific configurations for IPv4Addr feature object.
'''

# Python
from abc import ABC
from ipaddress import IPv4Network

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
        # secondary_vrf
        # ===================================

        if attributes.value('ipv4') and attributes.value('prefix_length'):
            # convert prefix_length to netmask
            ret = IPv4Network('1.1.1.1/{}'.format(
                attributes.value('prefix_length')), strict=False)
            mask = ret.with_netmask.split('/')[1]

            if attributes.value('ipv4_secondary'):
                configurations.append_line('ip address'
                    ' {ipv4} {prefix_length} secondary'
                    .format(ipv4=attributes.value('ipv4'),
                        prefix_length=mask))
                if attributes.value('secondary_vrf'):
                    configurations.append_line('ip address'
                        ' {ipv4} {prefix_length} secondary'
                        ' vrf {secondary_vrf}'
                        .format(ipv4=attributes.value('ipv4'), 
                            prefix_length=mask,
                            secondary_vrf=attributes.value('secondary_vrf')))
            else:
                configurations.append_line('ip address'
                    ' {ipv4} {prefix_length}'
                    .format(ipv4=attributes.value('ipv4'), 
                        prefix_length=mask))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True)
