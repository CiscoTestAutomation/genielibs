"""
Implement NXOS Specific Configurations for Msdp objects.
"""

# Table of contents:
#     class Msdp:
#         class DeviceAttributes:
#             class VrfAttributes:
#                 class PeerAttributes:

# Python
from abc import ABC
# Genie package
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder

class Msdp(ABC):

    class DeviceAttributes(ABC):
        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # enabled
            if attributes.value('enabled'):
                if unconfig is False:
                    configurations.append_line(attributes.format(
                        'feature msdp'))
                elif unconfig is True and\
                     attributes.attributes == {'enabled': {True: None}} or \
                        attributes.iswildcard:
                    configurations.append_line('no feature msdp', raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            # VrfAttributes
            if unconfig and attributes.iswildcard:
                configurations.submode_unconfig()

            for sub, attributes2 in attributes.mapping_values('vrf_attr',
                                                               sort=True,
                                                               keys=self.vrf_attr):
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
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                        None if self.vrf_name == 'default' else
                        attributes.format('vrf context {vrf_name}', force=True)):
                    if self.vrf_name != 'default' and unconfig and \
                            attributes.iswildcard:
                        configurations.submode_unconfig()

                    if attributes.value('originating_rp'):
                        configurations.append_line(
                            attributes.format(
                                'ip msdp originator-id {originating_rp}'))

                    if attributes.value('global_connect_retry_interval'):
                        configurations.append_line(
                            attributes.format(
                                'ip msdp reconnect-interval {global_connect_retry_interval}'))
                    # PeerAttributes
                    for sub, attributes2 in attributes.mapping_values('peer_attr',
                                                                      sort=True,
                                                                      keys=self.peer_attr):
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

            class PeerAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False,
                                 **kwargs):
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    if unconfig and attributes.value('address'):
                        configurations.append_line(
                            attributes.format('ip msdp peer {}'.format(self.address)))
                        
                    # only add mst_id in attributes when 
                    # unconfig for specific attributes is enable
                    if unconfig and attributes.attributes:
                        attributes.attributes['address'] = None

                    if attributes.value('connected_source'):
                        if attributes.value('peer_as'):
                            configurations.append_line(
                                attributes.format('ip msdp peer {address} '
                                                  'connect-source {connected_source} remote-as {peer_as}'))
                        else:
                            configurations.append_line(
                                attributes.format('ip msdp peer {address} '
                                                  'connect-source {connected_source}'))

                    enable = attributes.value('enable')
                    if enable is not None:
                        if not enable:
                            config_cmd = 'ip msdp shutdown {address}'
                            unconfig_cmd = 'no ip msdp shutdown {}'.format(self.address)
                        else:
                            config_cmd = 'no ip msdp shutdown {address}'
                            unconfig_cmd = 'ip msdp shutdown {}'.format(self.address)
                        configurations.append_line(
                            attributes.format(config_cmd),
                            unconfig_cmd=unconfig_cmd)


                    if attributes.value('description'):
                        configurations.append_line(
                            attributes.format('ip msdp description {address} {description}'))

                    if attributes.value('mesh_group'):
                        configurations.append_line(
                            attributes.format('ip msdp mesh-group {address} {mesh_group}'))

                    if attributes.value('sa_filter_in'):
                        configurations.append_line(
                            attributes.format('ip msdp sa-policy {address} {sa_filter_in} in'))

                    if attributes.value('sa_filter_out'):
                        configurations.append_line(
                            attributes.format('ip msdp sa-policy {address} {sa_filter_out} out'))

                    if attributes.value('sa_limit'):
                        configurations.append_line(
                            attributes.format('ip msdp sa-limit {address} {sa_limit}'))

                    if attributes.value('keepalive_interval')\
                            and attributes.value('holdtime_interval'):
                        configurations.append_line(
                            attributes.format('ip msdp keepalive {address} {keepalive_interval} {holdtime_interval}'))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)
