'''
Urpf Genie Conf Object Implementation for NXOS - CLI.
'''

# Python
from abc import ABC

# Genie
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

# URPF Hierarchy
# --------------
# URPf
#     +- DeviceAttributes
#       +- InterfaceAttributes


class Urpf(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # feature urpf
            if attributes.value('enabled'):
                if unconfig is False:
                    configurations.append_line(
                        attributes.format('no system urpf disable'))

                # Make sure that only enabled was provided in attributes
                # If wildcard,  then delete everything
                elif unconfig is True and\
                    attributes.attributes == {'enabled': {True: None}} or \
                        attributes.iswildcard:
                    configurations.append_line('system urpf disable', raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            #  +- DeviceAttributes
            #      +- InterfaceAttributes
            for sub, attributes2 in attributes.mapping_values('interface_attr',
                                                              sort=True,
                                                              keys=self.interface_attr):
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
        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # interface Ethernet1/1
                with configurations.submode_context(
                        attributes.format('interface {interface_name}', force=True)):

                    # ipverify attributes config
                    for ip_urpf_key, attributes2 in attributes.sequence_values('ip_urpf_keys', sort=True):
                        if unconfig:
                            configurations.append_block(ip_urpf_key.build_unconfig(
                                apply=False, attributes=attributes2, **kwargs))
                        else:
                            configurations.append_block(ip_urpf_key.build_config(
                                apply=False, attributes=attributes2, **kwargs))
                            
                    # ipv6verify attributes config
                    for ipv6_urpf_key, attributes2 in attributes.sequence_values('ipv6_urpf_keys', sort=True):
                        if unconfig:
                            configurations.append_block(ipv6_urpf_key.build_unconfig(
                                apply=False, attributes=attributes2, **kwargs))
                        else:
                            configurations.append_block(ipv6_urpf_key.build_config(
                                apply=False, attributes=attributes2, **kwargs))


                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                            unconfig=True, **kwargs)