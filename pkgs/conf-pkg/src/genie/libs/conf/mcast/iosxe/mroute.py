'''
IOSXE specific configurations for Mroute feature object.
'''

# Python
import warnings
from abc import ABC
from ipaddress import IPv4Network

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning,\
                                       AttributesHelper


class Mroute(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        # assert not kwargs, kwargs
        assert not apply
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # ===================================
        # mroute_address
        # mroute_prefix_mask
        # mroute_neighbor_address
        # mroute_interface_name
        # mroute_admin_distance
        # ===================================

        # get vrf and address_family info
        vrf = kwargs['vrf']
        af = kwargs['af_name']

        begin_with = {'ip': 'ip mroute', 'ipv6': 'ipv6 route'}

        if vrf == 'default':
            cmd_str = begin_with[af]
        else:
            cmd_str = begin_with[af] + ' vrf {}'.format(vrf)

        if attributes.value('mroute_address') and \
           attributes.value('mroute_prefix_mask'):

            if af == 'ip':
                # convert prefix_length to netmask
                ret = IPv4Network('1.1.1.1/{}'.format(
                    attributes.value('mroute_prefix_mask')), strict=False)
                mask = ret.with_netmask.split('/')[1]
                address = '{addr} {mask}'.format(addr=attributes.value('mroute_address'),
                                                 mask=mask)
            else:
                address = '{addr}/{mask}'.format(
                    addr=attributes.value('mroute_address'),
                    mask=attributes.value('mroute_prefix_mask'))

            # build up configuration string                
            if attributes.value('mroute_neighbor_address'):
                cmd_str += ' {address} {nei}'.format(
                            address=address,
                            nei=attributes.value('mroute_neighbor_address'))

            elif attributes.value('mroute_interface_name'):
                cmd_str += ' {address} {int}'.format(
                            address=address,
                            int=attributes.value('mroute_interface_name'))
            else:
                cmd_str = ''
      
            if attributes.value('mroute_admin_distance') and cmd_str:
                cmd_str += ' ' + str(attributes.value('mroute_admin_distance'))

            configurations.append_line(cmd_str)

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)
