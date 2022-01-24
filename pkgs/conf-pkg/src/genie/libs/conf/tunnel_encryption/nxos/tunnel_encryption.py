
'''
NXOS specific configurations for tunnel encryption feature object.
'''

# Python
from abc import ABC

# Genie
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


# Structure Hierarchy:
# TunnelEncryption
# +-- DeviceAttributes
#     +-- TunnelPolicyAttributes
#     +-- TunnelPeeripAttributes


class TunnelEncryption(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # feature tunnel encryption
            if attributes.value('enabled'):
                if unconfig is False:
                    configurations.append_line(
                        attributes.format('feature tunnel-encryption'))

            # Make sure that only enabled was provided in attributes
                # If wildcard,  then delete everything
                elif unconfig and\
                    attributes.attributes == {'enabled': {True: None}} or \
                        attributes.iswildcard:
                    configurations.append_line('no feature tunnel-encryption', raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            # nxos: tunnel-encryption must-secure-policy
            if attributes.value('enabled_must_secure_policy'):
                configurations.append_line('tunnel-encryption must-secure-policy')

            # nxos: tunnel-encryption source-interface
            if attributes.value('tunnel_source_interface'):
                configurations.append_line(\
                    attributes.format('tunnel-encryption source-interface {tunnel_source_interface}'))

            # tunnelpolicy Attribute
            for sub, attributes2 in attributes.mapping_values('tunnelpolicy_attr',
                                                              sort=True, keys=self.tunnelpolicy_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                     attributes=attributes2,
                                     unconfig=unconfig))
            # tunnelpeerip Attribute
            for sub, attributes2 in attributes.mapping_values('tunnelpeerip_attr',
                                                              sort=True, keys=self.tunnelpeerip_attr):
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
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class TunnelPolicyAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                with configurations.submode_context(attributes.format(
                        'tunnel-encryption policy {policy_name}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # nxos:
                    if attributes.value('cipher_suite'):
                        if attributes.value(
                                'cipher_suite').value == 'gcm-aes-xpn-128':
                            configurations.append_line(
                                attributes.format('cipher-suite GCM-AES-XPN-128'))
                        elif attributes.value(
                                'cipher_suite').value == 'gcm-aes-xpn-256':
                            configurations.append_line(
                                attributes.format('cipher-suite GCM-AES-XPN-257'))

                    # nxos: auto-recovery reload-delay <value>
                    if attributes.value('sak_rekey_time'):
                        configurations.append_line(
                            attributes.format('sak-rekey-time {sak_rekey_time}'))
                return str(configurations)

        class TunnelPeerIpAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                with configurations.submode_context(attributes.format(
                        'tunnel-encryption peer-ip {peer_ip}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # nxos: keychain and policy
                    if attributes.value('keychain_name'):
                        peerip_cfg = 'keychain {keychain_name} '

                        if attributes.value('tunnelpolicy_name'):
                            peerip_cfg += 'policy {tunnelpolicy_name}'

                    configurations.append_line(
                        attributes.format(peerip_cfg))

                return str(configurations)

