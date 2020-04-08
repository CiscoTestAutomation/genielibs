'''
NXOS specific configurations for Mcast feature object.
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

                with configurations.submode_context(
                    None if self.vrf_name == 'default' else
                        attributes.format('vrf context {vrf_id}', force=True)):

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

                    # Set decider key af_name from user set address family
                    self.af_name = self.address_family.value

                    # ======
                    # enable
                    # ======
                    if attributes.value('enabled'):
                        if unconfig is False:
                            if self.af_name == 'ipv4':
                                configurations.append_line(
                                    attributes.format('feature pim'))
                            elif self.af_name == 'ipv6':
                                configurations.append_line(
                                    attributes.format('feature pim6'))
                        elif unconfig is True:
                            if self.af_name == 'ipv4':
                                configurations.append_line('no feature pim', raw=True)
                            elif self.af_name == 'ipv6':
                                configurations.append_line('no feature pim6', raw=True)

                    # =========
                    # multipath
                    # =========
                    if attributes.value('multipath'):
                        if unconfig is False:
                            configurations.append_line(
                                    attributes.format('ip multicast multipath'))
                        elif unconfig is True:
                            configurations.append_line(
                                'no ip multicast multipath', raw=True)

                    # Mroute attributes configs
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