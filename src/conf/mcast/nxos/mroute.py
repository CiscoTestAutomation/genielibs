'''
NXOS specific configurations for Mroute feature object.
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
        # mroute_neighbor_address
        # mroute_interface_name
        # mroute_admin_distance
        # mroute_vrf
        # ===================================

        # Get vrf and address_family info
        vrf = kwargs['vrf']
        af_name = kwargs['af_name']

        if af_name == 'ipv4':
            af_key = 'ip'
        else:
            af_key = 'ipv6'

        if attributes.value('mroute_address') and \
           attributes.value('mroute_prefix_mask') and \
           attributes.value('mroute_neighbor_address') and \
           attributes.value('mroute_admin_distance') and \
           attributes.value('mroute_vrf'):
            configurations.append_line('{af_key} mroute'
                ' {mroute_address}/{mroute_prefix_mask}'
                ' {mroute_neighbor_address} {mroute_admin_distance}'
                ' vrf {mroute_vrf}'.format(af_key=af_key,
                    mroute_address=attributes.value('mroute_address'), 
                    mroute_prefix_mask=attributes.value('mroute_prefix_mask'),
                    mroute_neighbor_address=\
                        attributes.value('mroute_neighbor_address'),
                    mroute_admin_distance=\
                        attributes.value('mroute_admin_distance'),
                    mroute_vrf=attributes.value('mroute_vrf')))

        elif attributes.value('mroute_address') and \
             attributes.value('mroute_prefix_mask') and \
             attributes.value('mroute_neighbor_address') and \
             attributes.value('mroute_admin_distance'):
            configurations.append_line('{af_key} mroute'
                ' {mroute_address}/{mroute_prefix_mask}'
                ' {mroute_neighbor_address}'
                ' {mroute_admin_distance}'.format(af_key=af_key,
                    mroute_address=attributes.value('mroute_address'), 
                    mroute_prefix_mask=attributes.value('mroute_prefix_mask'),
                    mroute_neighbor_address=\
                        attributes.value('mroute_neighbor_address'),
                    mroute_admin_distance=\
                        attributes.value('mroute_admin_distance')))
        
        elif attributes.value('mroute_address') and \
             attributes.value('mroute_prefix_mask') and \
             attributes.value('mroute_neighbor_address'):
            configurations.append_line('{af_key} mroute'
                ' {mroute_address}/{mroute_prefix_mask}'
                ' {mroute_neighbor_address}'.format(af_key=af_key,
                    mroute_address=attributes.value('mroute_address'), 
                    mroute_prefix_mask=\
                        attributes.value('mroute_prefix_mask'),
                    mroute_neighbor_address=\
                        attributes.value('mroute_neighbor_address')))
        
        elif attributes.value('mroute_address') and \
             attributes.value('mroute_prefix_mask') and \
             attributes.value('mroute_interface_name') and \
             attributes.value('mroute_admin_distance') and \
             attributes.value('mroute_vrf'):
            configurations.append_line('{af_key} mroute'
                ' {mroute_address}/{mroute_prefix_mask}'
                ' {mroute_interface_name} {mroute_admin_distance}'
                ' vrf {mroute_vrf}'.format(af_key=af_key,
                    mroute_address=attributes.value('mroute_address'), 
                    mroute_prefix_mask=attributes.value('mroute_prefix_mask'),
                    mroute_interface_name=\
                        attributes.value('mroute_interface_name'),
                    mroute_admin_distance=\
                        attributes.value('mroute_admin_distance'),
                    mroute_vrf=attributes.value('mroute_vrf')))

        elif attributes.value('mroute_address') and \
             attributes.value('mroute_prefix_mask') and \
             attributes.value('mroute_interface_name') and \
             attributes.value('mroute_admin_distance'):
            configurations.append_line('{af_key} mroute'
                ' {mroute_address}/{mroute_prefix_mask}'
                ' {mroute_interface_name} {mroute_admin_distance}'.\
                format(af_key=af_key,
                    mroute_address=attributes.value('mroute_address'), 
                    mroute_prefix_mask=attributes.value('mroute_prefix_mask'),
                    mroute_interface_name=\
                        attributes.value('mroute_interface_name'),
                    mroute_admin_distance=\
                        attributes.value('mroute_admin_distance')))

        elif attributes.value('mroute_address') and \
             attributes.value('mroute_prefix_mask') and \
             attributes.value('mroute_interface_name'):
            configurations.append_line('{af_key} mroute'
                ' {mroute_address}/{mroute_prefix_mask}'
                ' {mroute_interface_name}'.format(af_key=af_key,
                    mroute_address=attributes.value('mroute_address'), 
                    mroute_prefix_mask=\
                        attributes.value('mroute_prefix_mask'),
                    mroute_interface_name=\
                        attributes.value('mroute_interface_name')))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)
