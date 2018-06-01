
# import python
from abc import ABC

# import genie
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class Dot1x(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # dot1x system-auth-control
            if attributes.value('system_auth_control'):
                configurations.append_line('dot1x system-auth-control')

            # dot1x supplicant force-multicast
            if attributes.value('supplicant_force_mcast'):
                configurations.append_line('dot1x supplicant force-multicast')
            
            # credentials attributes
            for sub, attributes2 in attributes.mapping_values('credentials_attr',
                sort=True, keys=self.credentials_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                     attributes=attributes2,
                                     unconfig=unconfig))
            
            # interfaces attributes
            for sub, attributes2 in attributes.mapping_values('interface_attr',
                sort=True, keys=self.interface_attr):
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


        class CredentialsAttributes(ABC):

            def build_config(self, apply=True, attributes=None,
                             unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                    attributes.format('dot1x credential {credential_profile}', force=True)): 
                   
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # username <credential_username>
                    configurations.append_line(
                        attributes.format('username {credential_username}'))

                    # password [<credential_pwd_type>] <credential_secret>
                    if attributes.value('credential_pwd_type'):
                        configurations.append_line(attributes.format(
                                'password {credential_pwd_type} {credential_secret}'))
                    else:
                        configurations.append_line(
                            attributes.format('password {credential_secret}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None,
                               **kwargs):
                return self.build_config(apply=apply,
                                         attributes=attributes,
                                         unconfig=True, **kwargs)


        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None,
                             unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                    attributes.format('interface {interface_id}', force=True)):

                    # dot1x pae {if_pae}
                    configurations.append_line(
                        attributes.format('dot1x pae {if_pae}'))

                    # dot1x authenticator eap profile <if_authen_eap_profile>
                    configurations.append_line(
                        attributes.format(
                            'dot1x authenticator eap profile {if_authen_eap_profile}'))

                    # dot1x supplicant eap profile <if_supplicant_eap_profile>
                    configurations.append_line(
                        attributes.format(
                            'dot1x supplicant eap profile {if_supplicant_eap_profile}'))

                    # dot1x credentials <if_credentials>
                    configurations.append_line(
                        attributes.format('dot1x credentials {if_credentials}'))

                    # access-session port-control <if_port_control>
                    configurations.append_line(
                        attributes.format('access-session port-control {if_port_control}'))

                    # access-session host-mode <if_host_mode>
                    configurations.append_line(
                        attributes.format('access-session host-mode {if_host_mode}'))

                    # access-session closed
                    if attributes.value('if_closed'):
                        configurations.append_line(
                            attributes.format('access-session closed'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None,
                               **kwargs):
                return self.build_config(apply=apply,
                                         attributes=attributes,
                                         unconfig=True, **kwargs)