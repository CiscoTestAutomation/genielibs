'''
IOSXE specific configurations for Mcast feature object.
'''

# Python
from abc import ABC

# Genie
from genie.decorator import managedattribute
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning, \
                                       AttributesHelper

# Structure Hierarchy:
# Mcast
#   +--DeviceAttributes
#       +--VrfAttributes
#           +-- AddressFamilyAttributes


class Mcast(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
 
            # VrfAttributes
            for sub, attributes2 in attributes.mapping_values('vrf_attr',
                    sort=True, keys=self.vrf_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))            
            
            if apply:
                if configurations:
                    self.device.configure(configurations)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

            
        class VrfAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # AddressFamilyAttributes
                for sub, attributes2 in attributes.mapping_values('address_family_attr',
                        sort=True, keys=self.address_family_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

            
            class AddressFamilyAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False,
                                 **kwargs):
                    assert not apply
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    self.af_name = self.address_family.value
                    self.af_name = self.af_name.replace('ipv4', 'ip')

                    # enable
                    if attributes.value('enable'):
                        if self.vrf_id == 'default':
                            cfg_str = '{af_name} multicast-routing'
                        else:
                            cfg_str = '{af_name} multicast-routing vrf {vrf_id}'

                        if self.af_name == 'ip':
                            cfg_str += ' distributed'

                        configurations.append_line(attributes.format(cfg_str))

                    # multipath
                    if attributes.value('multipath'):
                        configurations.append_line(
                            attributes.format('{af_name} multicast multipath'))


                    # Mroute Attributes under top level config
                    for mroute, attributes2 in attributes.sequence_values(
                            'mroutes', sort=True):
                        kwargs = {'vrf':self.vrf_id, 'af_name':self.af_name}
                        if unconfig:
                            configurations.append_block(mroute.build_unconfig(
                                apply=False, attributes=attributes2, **kwargs))
                        else:
                            configurations.append_block(mroute.build_config(
                                apply=False, attributes=attributes2, **kwargs))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    kwargs = {'vrf':self.vrf_id, 'af_name':self.af_name}
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)
