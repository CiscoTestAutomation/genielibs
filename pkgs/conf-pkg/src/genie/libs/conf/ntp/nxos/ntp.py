'''
NXOS specific configurations for Ntp feature object.
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
# Ntp
# +-- DeviceAttribute
#     +-- VrfAttributes
#     |   +-- ServerAttributes
#     |   +-- PeerAttributes
#     +-- AuthKeyAttribute

class Ntp(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # enabled
            if attributes.value('enabled'):
                if unconfig is False:
                    configurations.append_line(
                        attributes.format('feature ntp'))

                # Make sure that only enabled was provided in attributes
                # If wildcard,  then delete everything
                elif unconfig is True and\
                     attributes.attributes == {'enabled': {True: None}} or \
                        attributes.iswildcard:
                    configurations.append_line('no feature ntp', raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            # master_stratum
            if attributes.value('master_stratum'):
                configurations.append_line(
                    attributes.format('ntp master {master_stratum}'))

            # auth_enabled
            if attributes.value('auth_enabled'):
                configurations.append_line('ntp authenticate')
 
            # VrfAttributes
            for sub, attributes1 in attributes.mapping_values('vrf_attr',
                    sort=True, keys=self.vrf_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes1,
                                             unconfig=unconfig))
 
            # AuthKeyAttribute
            for sub, attributes2 in attributes.mapping_values('auth_key_attr',
                    sort=True, keys=self.auth_key_attr):
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

                # source_interface
                if attributes.value('source_interface') and \
                   self.vrf_name == 'default':
                    configurations.append_line(
                        attributes.format('ntp source-interface {source_interface}'))

                # ServerAttributes
                for sub, attributes1 in attributes.mapping_values('server_attr',
                        sort=True, keys=self.server_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes1,
                                                 unconfig=unconfig))

                # PeerAttributes
                for sub, attributes2 in attributes.mapping_values('peer_attr',
                        sort=True, keys=self.peer_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

            
            class ServerAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False,
                                 **kwargs):
                    # assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # server_address
                    if not attributes.value('server_address') and not unconfig:
                        return str()

                    conf_line = 'ntp server {server_address}'

                    # server_key_id
                    if attributes.value('server_key_id'):
                        conf_line += ' key {server_key_id}'

                    # server_maxpoll
                    if attributes.value('server_maxpoll'):
                        conf_line += ' maxpoll {server_maxpoll}'

                    # server_minpoll
                    if attributes.value('server_minpoll'):
                        conf_line += ' minpoll {server_minpoll}'

                    # server_prefer
                    if attributes.value('server_prefer'):
                        conf_line += ' prefer'

                    if self.vrf_name and self.vrf_name != 'default':
                        conf_line += ' use-vrf {vrf_name}'

                    # append the line
                    configurations.append_line(attributes.format(conf_line, force=True))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)

            
            class PeerAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False,
                                 **kwargs):
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # peer_address
                    if not attributes.value('peer_address') and not unconfig:
                        return str()

                    conf_line = 'ntp peer {peer_address}'

                    # peer_key_id
                    if attributes.value('peer_key_id'):
                        conf_line += ' key {peer_key_id}'

                    # peer_maxpoll
                    if attributes.value('peer_maxpoll'):
                        conf_line += ' maxpoll {peer_maxpoll}'

                    # peer_minpoll
                    if attributes.value('peer_minpoll'):
                        conf_line += ' minpoll {peer_minpoll}'

                    # peer_prefer
                    if attributes.value('peer_prefer'):
                        conf_line += ' prefer'

                    if self.vrf_name and self.vrf_name != 'default':
                        conf_line += ' use-vrf {vrf_name}'

                    # append the line
                    configurations.append_line(attributes.format(conf_line, force=True))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)


        class AuthKeyAttribute(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # auth_key_id, auth_algorithm, auth_key
                if attributes.value('auth_algorithm') and \
                   attributes.value('auth_key'):
                    configurations.append_line(
                        attributes.format('ntp authentication-key '
                            '{auth_key_id} {auth_algorithm.value} {auth_key}', force=True))

                # auth_trusted_key
                if attributes.value('auth_trusted_key'):
                    configurations.append_line(
                        attributes.format('ntp trusted-key {auth_key_id}', force=True))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)