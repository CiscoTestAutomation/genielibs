'''
NXOS specific configurations for static rp feature object.
'''

# Python
import warnings
from abc import ABC

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning,\
                                       AttributesHelper


class RPAddressGroup(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not apply
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # ===================================
        # static_rp_address
        # static_rp_group_list
        # static_rp_prefix_list
        # static_rp_bidir
        # static_rp_override
        # ===================================
        skip_unconfig = False

        if attributes.value('static_rp_address'):
            # ip/ipv6 pim rp-address <static_rp_address>
            if kwargs['vrf'] == 'default':
                static_str = '{ip} pim rp-address'.format(ip=kwargs['ip_type'])
            else:
                static_str = '{ip} pim vrf {vrf} rp-address'.format(ip=kwargs['ip_type'],
                                                                    vrf=kwargs['vrf'])

            static_str += ' {static_rp_address}'

            # group-list {static_rp_group_list} |
            # route-map {static_rp_route_map} |
            # prefix-list {static_rp_prefix_list}
            if attributes.value('static_rp_group_list'):
                static_str += ' {static_rp_group_list}'

            # override 
            if attributes.value('static_rp_override') and \
               kwargs['ip_type'] == 'ip':
                static_str += ' override'

            # bidir
            if attributes.value('static_rp_bidir'):
                static_str += ' bidir'

            configurations.append_line(
                attributes.format(static_str))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)
