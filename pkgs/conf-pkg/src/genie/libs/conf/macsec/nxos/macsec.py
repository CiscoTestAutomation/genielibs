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
#   +- InterfaceAttributes

class Macsec(ABC):
    class DeviceAttributes(ABC):
        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            #self.interface_config = CliConfigBuilder(unconfig=unconfig)

            # feature macsec
            if attributes.value('enabled'):
                if unconfig is False:
                    configurations.append_line(
                        attributes.format('feature macsec'))

                # Make sure that only enabled was provided in attributes
                # If wildcard,  then delete everything
                elif unconfig is True and\
                     attributes.attributes == {'enabled': {True: None}} or \
                        attributes.iswildcard:
                    configurations.append_line('no feature macsec', raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            #  +- DeviceAttributes
            #      +- MacsecPolicyAttributes
            for sub, attributes2 in attributes.mapping_values('macsec_policy_attr',
                                                            sort=True,
                                                            keys=self.macsec_policy_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                    attributes=attributes2,
                                    unconfig=unconfig))


            # # Add InterfaceAttribute configuration
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

        # +- DeviceAttributes
        #   +- MacsecPolicyAttributes
        class MacsecPolicyAttributes(ABC):
            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # macsec policy <MP1>
                with configurations.submode_context(
                    attributes.format('macsec policy {macsec_policy_name}', force=True)):

                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    #macsec policy <MP1>
                    #   key-server-priority 30
                    if attributes.value('key_server_priority'):
                       configurations.append_line(attributes.format('key-server-priority {key_server_priority}'))

                    # macsec policy <MP1>
                    #   cipher-suite GCM-AES-128|GCM-AES-256|GCM-AES-XPN-128|GCM-AES-XPN-256
                    if attributes.value('cipher_suite'):
                        cipher_suite = attributes.value('cipher_suite')
                        configurations.append_line(attributes.format('cipher-suite {cipher_suite.value}'))
                    
                     # cipher-suite enforce GCM-AES-128 GCM-AES-256 GCM-AES-XPN-128 GCM-AES-XPN-256 
                    if attributes.value('enforce_cipher_suite'):
                        enforce_cipher_suite = ' '.join(attributes.value('enforce_cipher_suite').split(','))
                        configurations.append_line(attributes.format(f'cipher-suite enforce-peer {enforce_cipher_suite}'))
                    
                    #macsec policy <MP1>
                    #   conf-offset CONF-OFFSET-50|CONF-OFFSET-30|CONF-OFFSET-0
                    if attributes.value('conf_offset'):
                        configurations.append_line(attributes.format('conf-offset {conf_offset.value}'))

                    #macsec policy <MP1>
                    #   security-policy must-secure|should-secure
                    if attributes.value('security_policy'):
                        configurations.append_line(attributes.format('security-policy {security_policy.value}'))

                    #macsec policy <MP1>
                    #   sak-expiry-time 60
                    if attributes.value('sak_expiry_timer'):
                       configurations.append_line(attributes.format('sak-expiry-time {sak_expiry_timer}'))

                    #macsec policy <MP1>
                    #   include-icv-indicator
                    if attributes.value('include_icv_indicator') is True:
                       configurations.append_line(attributes.format('include-icv-indicator'))
                    if attributes.value('include_icv_indicator') is False:
                        configurations.append_line(attributes.format('no include-icv-indicator'))

                    #macsec policy <MP1>
                    #   include-sci
                    if attributes.value('include_sci') is True:
                       configurations.append_line(attributes.format('include-sci'))
                    if attributes.value('include_sci') is False:
                        configurations.append_line(attributes.format('no include-sci'))

                    #macsec policy <MP1>
                    #   window-size 10000
                    if attributes.value('window_size'):
                        configurations.append_line(attributes.format('window-size {window_size}'))
                    
                    #macsec policy <MP1>
                    #   ppk crypto-qkd-profile QKD1
                    if attributes.value('ppk_profile_name'):
                       configurations.append_line(attributes.format('ppk crypto-qkd-profile {ppk_profile_name}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

        class InterfaceAttributes(ABC):
            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # interface Ethernet1/1
                with configurations.submode_context(
                    attributes.format('interface {interface_name}', force=True)):

                    #  macsec keychain KC1 policy MP1
                    if attributes.value('key_chain') and attributes.value('macsec_policy_name'):
                        if not  attributes.value('fallback_key_chain'):
                            configurations.append_line(attributes.format('macsec keychain {key_chain} policy {macsec_policy_name}'))
                        else:
                            #  macsec keychain KC1 policy MP1 fallback-keychain KC2
                            configurations.append_line(attributes.format(
                                'macsec keychain {key_chain} policy {macsec_policy_name} fallback-keychain {fallback_key_chain}'
                                ))
                    
                    if attributes.value('eapol_mac_address'):
                        #eapol mac-address <address> 
                        if not attributes.value('ether_type'):
                            configurations.append_line(attributes.format('eapol mac-address {eapol_mac_address} '))
                        #eapol mac-address <address> ethertype 0x888ef
                        else:
                            configurations.append_line(attributes.format(
                                'eapol mac-address {eapol_mac_address} ethertype 0x{ether_type}')
                            )

                    if attributes.value('eapol_broadcast_mac_address'): 
                        #eapol mac-address broadcast-address
                        if not attributes.value('ether_type'):
                            configurations.append_line(attributes.format('eapol mac-address broadcast-address'))
                        #eapol mac-address broadcast-address ethertype 0x888ef
                        else:
                            configurations.append_line(attributes.format(
                                'eapol mac-address broadcast-address ethertype 0x{ether_type}')
                            )

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                                unconfig=True, **kwargs)