'''
IOSXR specific configurations for Mcast feature object.
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

            # multicast-routing
            with configurations.submode_context('multicast-routing'):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

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
                        None if self.vrf_name == 'default' \
                             else attributes.format('vrf {vrf_name}', force=True)):
                    if self.vrf_name != 'default' and unconfig \
                       and attributes.iswildcard:
                        configurations.submode_unconfig()

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

                    # # Set decider key af_name from user set address family
                    # self.af_name = self.address_family.value

                    with configurations.submode_context(attributes.format(
                        'address-family {address_family.name}', force=True)):

                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # ======
                        # enable
                        # ======
                        if attributes.value('enable'):
                            configurations.append_line(attributes.format(
                                'interface all enable'))

                        # =========
                        # multipath
                        # =========
                        if attributes.value('multipath'):
                            configurations.append_line(
                                    attributes.format('multipath'))

                        # Mroute attributes configs
                        for mroute, attributes2 in attributes.sequence_values(
                                'mroutes', sort=True):
                            if unconfig:
                                configurations.append_block(mroute.build_unconfig(
                                    apply=False, attributes=attributes2, **kwargs))
                            else:
                                configurations.append_block(mroute.build_config(
                                    apply=False, attributes=attributes2, **kwargs))

                        # InterfaceAttribute
                        for sub, attributes2 in attributes.mapping_values('interface_attr',
                            sort=True, keys=self.interface_attr):
                                configurations.append_block(
                                    sub.build_config(apply=False,
                                                     attributes=attributes2,
                                                     unconfig=unconfig))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)


                class InterfaceAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False,
                                     **kwargs):
                        assert not apply
                        assert not kwargs, kwargs
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        with configurations.submode_context(attributes.format(
                            'interface {interface.name}', force=True)):

                            if unconfig and attributes.iswildcard:
                                configurations.submode_unconfig()

                            # ======
                            # if_enable
                            # ======
                            if attributes.value('if_enable'):
                                configurations.append_line(attributes.format(
                                    'enable'))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)