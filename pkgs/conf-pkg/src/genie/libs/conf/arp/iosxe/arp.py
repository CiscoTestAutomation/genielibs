"""
Implement Iosxe Specific Configurations for Arp objects.
"""

# Table of contents:
#  class DeviceAttributes
#     class InterfaceAttributes
#         class StaticArpAttributes

# Python
from abc import ABC
# Genie package
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder

class Arp(ABC):

    class DeviceAttributes(ABC):
        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # arp entries interface-limit <max_entries>
            if attributes.value('max_entries'):
                configurations.append_line(attributes.format('arp entries interface-limit {max_entries}'))

            # InterfaceAttributes
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

        # InterfaceAttributes
        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)


                if attributes.value('if_proxy_enable') or \
                        attributes.value('if_local_proxy_enable') or\
                        attributes.value('if_expire_time'):
                    with configurations.submode_context(
                            attributes.format('interface {interface}',force=True)):

                        if attributes.value('if_proxy_enable'):
                            configurations.append_line(attributes.format('ip proxy-arp'))

                        if attributes.value('if_local_proxy_enable'):
                            configurations.append_line(attributes.format('ip local-proxy-arp'))

                        if attributes.value('if_expire_time'):
                            configurations.append_line(attributes.format('arp timeout {if_expire_time}'))


                for sub, attributes2 in attributes.mapping_values('static_arp_attr',
                                                                  sort=True,
                                                                  keys=self.static_arp_attr):
                    configurations.append_block(
                        sub.build_config(apply=False,
                                         attributes=attributes2,
                                         unconfig=unconfig))
                return str(configurations)


            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

            # StaticArpAttributes
            class StaticArpAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False,
                                 **kwargs):

                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    vrf = ""
                    if attributes.value('if_static_vrf'):
                        vrf = 'vrf {}'.format(attributes.value('if_static_vrf'))

                    static_alias = ""
                    if attributes.value('if_static_alias')==True:
                        static_alias = 'alias'

                    cli_cmd = ['arp {vrf} {if_static_ip_address} {if_static_mac_address} {if_static_encap_type.value} {static_alias}',
                           'arp {if_static_ip_address} {if_static_mac_address} {if_static_encap_type.value} {static_alias}',
                           'arp {vrf} {if_static_ip_address} {if_static_mac_address} {if_static_encap_type.value}',
                           'arp {if_static_ip_address} {if_static_mac_address} {if_static_encap_type.value}']

                    if attributes.value('if_static_ip_address') and \
                            attributes.value('if_static_mac_address') and \
                            attributes.value('if_static_encap_type'):
                        if vrf and static_alias:
                            cmd = cli_cmd[0]. \
                                format(vrf=vrf,
                                   if_static_ip_address=attributes.value('if_static_ip_address'),
                                   if_static_mac_address=attributes.value('if_static_mac_address'),
                                   if_static_encap_type=attributes.value('if_static_encap_type'),
                                   static_alias=static_alias)
                        if vrf and not static_alias:
                            cmd = cli_cmd[1]. \
                                format(vrf=vrf,
                                   if_static_ip_address=attributes.value('if_static_ip_address'),
                                   if_static_mac_address=attributes.value('if_static_mac_address'),
                                   if_static_encap_type=attributes.value('if_static_encap_type'))
                        if not vrf and static_alias:
                            cmd = cli_cmd[2]. \
                                format(if_static_ip_address=attributes.value('if_static_ip_address'),
                                       if_static_mac_address=attributes.value('if_static_mac_address'),
                                       if_static_encap_type=attributes.value('if_static_encap_type'),
                                       static_alias=static_alias)
                        if not vrf and not static_alias:
                            cmd = cli_cmd[3]. \
                                format(if_static_ip_address=attributes.value('if_static_ip_address'),
                                       if_static_mac_address=attributes.value('if_static_mac_address'),
                                       if_static_encap_type=attributes.value('if_static_encap_type'))

                        configurations.append_line(cmd)


                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                     cli_config=configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)

