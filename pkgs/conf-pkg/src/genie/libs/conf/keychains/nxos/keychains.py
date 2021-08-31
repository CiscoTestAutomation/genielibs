"""
Implement NXOS Specific Configurations for Keychains objects.
"""

# Structure Hierarchy:
# Keychains
#   +--DeviceAttributes
#     +-- KeyChainAttributes
#     | +-- KeyIdAttributes
#     +-- KeyChainMacSecAttributes
#     | +-- KeyIdAttributes
#     +-- KeyChainTunEncAttributes
#       +-- KeyIdAttributes

# Python
from abc import ABC

# Genie
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder


# Keychains
class Keychains(ABC):

    # Keychains
    #   +--DeviceAttributes
    class DeviceAttributes(ABC):
        def build_config(self,
                         apply=True,
                         attributes=None,
                         unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # DeviceAttributes
            # (None)

            # KeyChainAttributes
            for sub, attributes2 in attributes.mapping_values(
                    'keychain_attr', sort=True, keys=self.keychain_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                     attributes=attributes2,
                                     unconfig=unconfig))

            # KeyChainMacSecAttributes
            for sub, attributes2 in attributes.mapping_values(
                    'ms_keychain_attr', sort=True, keys=self.ms_keychain_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                     attributes=attributes2,
                                     unconfig=unconfig))

            # KeyChainTunEncAttributes
            for sub, attributes2 in attributes.mapping_values(
                    'te_keychain_attr', sort=True, keys=self.te_keychain_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                     attributes=attributes2,
                                     unconfig=unconfig))

            if not apply:
                return CliConfig(device=self.device,
                                 unconfig=unconfig,
                                 cli_config=configurations)

            if configurations:
                self.device.configure(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply,
                                     attributes=attributes,
                                     unconfig=True,
                                     **kwargs)

        # Keychains
        #   +--DeviceAttributes
        #     +-- KeyChainAttributes
        class KeyChainAttributes(ABC):
            def build_config(self,
                             apply=True,
                             attributes=None,
                             unconfig=False,
                             **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                        attributes.format('key chain {key_chain}',
                                          force=True)):

                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                        # No attributes

                    for sub, attributes2 in attributes.mapping_values(
                            'key_id_attr', sort=True, keys=self.key_id_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))
                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply,
                                         attributes=attributes,
                                         unconfig=True,
                                         **kwargs)

            # Keychains
            #   +--DeviceAttributes
            #     +-- KeyChainAttributes
            #     | +-- KeyIdAttributes
            class KeyIdAttributes(ABC):
                def build_config(self,
                                 apply=True,
                                 attributes=None,
                                 unconfig=False,
                                 **kwargs):
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    with configurations.submode_context(
                            attributes.format('key {key_id}', force=True)):

                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # key chain <key_chain>
                        #  key <key_id>
                        #   key-string [key_enc_type] <key_string>
                        if attributes.value('key_string'):

                            # + key-string
                            key_string_str = 'key-string'

                            # + [key_enc_type] <key_string>
                            if attributes.value('key_enc_type'):
                                key_string_str += attributes.format(
                                    ' {key_enc_type} {key_string}')
                            else:
                                key_string_str += attributes.format(
                                    ' {key_string}')

                            configurations.append_line(
                                attributes.format(key_string_str))

                    return str(configurations)

                def build_unconfig(self,
                                   apply=True,
                                   attributes=None,
                                   **kwargs):
                    return self.build_config(apply=apply,
                                             attributes=attributes,
                                             unconfig=True,
                                             **kwargs)

        # Keychains
        #   +--DeviceAttributes
        #     +-- KeyChainMacSecAttributes
        class KeyChainMacSecAttributes(ABC):
            def build_config(self,
                             apply=True,
                             attributes=None,
                             unconfig=False,
                             **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                        attributes.format('key chain {ms_key_chain} macsec',
                                          force=True)):

                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                        # No attributes

                    for sub, attributes2 in attributes.mapping_values(
                            'key_id_attr', sort=True, keys=self.key_id_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))
                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply,
                                         attributes=attributes,
                                         unconfig=True,
                                         **kwargs)

            # Keychains
            #   +--DeviceAttributes
            #     +-- KeyChainMacSecAttributes
            #     | +-- KeyIdAttributes
            class KeyIdAttributes(ABC):
                def build_config(self,
                                 apply=True,
                                 attributes=None,
                                 unconfig=False,
                                 **kwargs):

                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    with configurations.submode_context(
                            attributes.format('key {key_id}', force=True)):

                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # key chain <te_key_chain> macsec
                        #  key <key_id>
                        #   key-octet-string [key_enc_type] <key_string> [cryptographic-algorithm <crypto_algo>]
                        if attributes.value('key_string'):

                            # + key-octet-string
                            key_string_str = 'key-octet-string'

                            # + [te_key_enc_type]
                            if attributes.value('key_enc_type'):
                                key_string_str += attributes.format(
                                    ' {key_enc_type}')

                            # + <key_string>
                            key_string_str += attributes.format(
                                ' {key_string}')

                            # + [cryptographic-algorithm <crypto_algo>]
                            if attributes.value('crypto_algo'):
                                if attributes.value(
                                        'crypto_algo').value == 'aes-128-cmac':
                                    key_string_str += ' cryptographic-algorithm AES_128_CMAC'
                                elif attributes.value(
                                        'crypto_algo').value == 'aes-128-cmac':
                                    key_string_str += ' cryptographic-algorithm AES_256_CMAC'

                            configurations.append_line(
                                attributes.format(key_string_str))

                    return str(configurations)

                def build_unconfig(self,
                                   apply=True,
                                   attributes=None,
                                   **kwargs):
                    return self.build_config(apply=apply,
                                             attributes=attributes,
                                             unconfig=True,
                                             **kwargs)

        # Keychains
        #   +--DeviceAttributes
        #     +-- KeyChainMacSecAttributes
        class KeyChainTunEncAttributes(ABC):
            def build_config(self,
                             apply=True,
                             attributes=None,
                             unconfig=False,
                             **kwargs):
                assert not kwargs, kwargs

                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                        attributes.format(
                            'key chain {te_key_chain} tunnel-encryption',
                            force=True)):

                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                        # No attributes

                    for sub, attributes2 in attributes.mapping_values(
                            'key_id_attr', sort=True, keys=self.key_id_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))
                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply,
                                         attributes=attributes,
                                         unconfig=True,
                                         **kwargs)

            # Keychains
            #   +--DeviceAttributes
            #     +-- KeyChainTunEncAttributes
            #     | +-- KeyIdAttributes
            class KeyIdAttributes(ABC):
                def build_config(self,
                                 apply=True,
                                 attributes=None,
                                 unconfig=False,
                                 **kwargs):

                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    with configurations.submode_context(
                            attributes.format('key {key_id}', force=True)):

                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # key chain <key_chain> tunnel-encryption
                        #  key <key_id>
                        #   key-octet-string [key_enc_type] <key_string> [cryptographic-algorithm <crypto_algo>]
                        if attributes.value('key_string'):

                            # + key-octet-string
                            key_string_str = 'key-octet-string'

                            # + [key_enc_type]
                            if attributes.value('key_enc_type'):
                                key_string_str += attributes.format(
                                    ' {key_enc_type}')

                            # + <key_string>
                            key_string_str += attributes.format(
                                ' {key_string}')

                            # + [cryptographic-algorithm <crypto_algo>]
                            if attributes.value('crypto_algo'):
                                if attributes.value(
                                        'crypto_algo').value == 'aes-128-cmac':
                                    key_string_str += ' cryptographic-algorithm AES_128_CMAC'
                                elif attributes.value(
                                        'crypto_algo').value == 'aes-128-cmac':
                                    key_string_str += ' cryptographic-algorithm AES_256_CMAC'

                            configurations.append_line(
                                attributes.format(key_string_str))

                        # key chain <key_chain> tunnel-encryption
                        #  key <key_id>
                        #   send-lifetime <lifetime_start> duration <lifetime_duration>
                        if attributes.value(
                                'lifetime_start') and attributes.value(
                                    'lifetime_duration'):

                            # send-lifetime <lifetime_start> duration <lifetime_duration>
                            lifetime_str = 'send-lifetime {lifetime_start} duration {lifetime_duration}'

                            configurations.append_line(
                                attributes.format(lifetime_str))

                    return str(configurations)

                def build_unconfig(self,
                                   apply=True,
                                   attributes=None,
                                   **kwargs):
                    return self.build_config(apply=apply,
                                             attributes=attributes,
                                             unconfig=True,
                                             **kwargs)
