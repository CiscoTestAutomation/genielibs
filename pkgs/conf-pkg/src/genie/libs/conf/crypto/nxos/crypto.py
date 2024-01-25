'''
    Macsec Genie Conf Object Implementation for NXOS - CLI.
'''

# Python
from abc import ABC

#Genie
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig


# Macsec
# +- DeviceAttributes
#   +- MacsecPolicyAttributes

class Crypto(ABC):
    class DeviceAttributes(ABC):
        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            #self.interface_config = CliConfigBuilder(unconfig=unconfig)

            # feature cryptopqc
            if attributes.value('enabled'):
                if unconfig is False:
                    configurations.append_line(
                        attributes.format('feature cryptopqc'))

                # Make sure that only enabled was provided in attributes
                # If wildcard,  then delete everything
                elif unconfig is True and\
                     attributes.attributes == {'enabled': {True: None}} or \
                        attributes.iswildcard:
                    configurations.append_line('no feature cryptopqc', raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            #  +- DeviceAttributes
            #      +- CryptoQkdAttributes
            for sub, attributes2 in attributes.mapping_values('crypto_qkd_attr',
                                                            sort=True,
                                                            keys=self.crypto_qkd_attr):
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

        # +- DeviceAttributes
        #   +- CryptoQkdAttributes
        class CryptoQkdAttributes(ABC):
            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                
                # crypto qkd <test-qkd>
                with configurations.submode_context(
                    attributes.format('crypto qkd profile {crypto_qkd_name}', force=True)):

                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # crypto qkd <test-qkd>
                    #  kme server 10.10.20.1
                    #  OR 
                    #  kme server ipv4 10.10.20.1 port 6000
                    #  OR 
                    #  kme server 10.10.20.1 port 6000
                    
                    if attributes.value('kme_server_ip'):
                        server_ip = attributes.value('kme_server_ip')
                        cmd = f'kme server {server_ip} '
                        if attributes.value('kme_server_ip_version'):
                            server_ip_version = attributes.value('kme_server_ip_version')
                            cmd += server_ip_version.value
                        if attributes.value('kme_server_http_port'):
                            http_port = attributes.value('kme_server_http_port')
                            cmd += f' port {http_port}'
                        
                        configurations.append_line(attributes.format(cmd))
                    
                    #crypto qkd <test-qkd>
                    # transport tls authentication-type trustpoint tp1
                    # OR
                    # transport tls authentication-type trustpoint tp1 ignore-certificate
                    # OR 
                    # transport tls authentication-type psk key-id 20 key test1
                    # transport tls authentication-type trustpoint tp1
                    if attributes.value('tls_auth_type'):
                        tls_type = attributes.value('tls_auth_type')
                        if tls_type.value == 'trustpoint' and attributes.value('tls_trustpoint_name'):
                            trustpoint_name = attributes.value('tls_trustpoint_name')
                            if attributes.value('tls_trustpoint_ignore_certificate'):
                                configurations.append_line(attributes.format(f'transport tls authentication-type {tls_type.value} {trustpoint_name} ignore-certificate'))
                            else: 
                                configurations.append_line(attributes.format(f'transport tls authentication-type {tls_type.value} {trustpoint_name}'))

                        if tls_type.value == 'psk':
                            if attributes.value('tls_pks_key_id') and attributes.value('tls_pks_key_string'):
                                key_id = attributes.value('tls_pks_key_id') 
                                key_string = attributes.value('tls_pks_key_string')
                                configurations.append_line(attributes.format(
                                    f'transport tls authentication-type {tls_type.value} key_id {key_id} key {key_string}'
                                    )
                                )
                            
                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

