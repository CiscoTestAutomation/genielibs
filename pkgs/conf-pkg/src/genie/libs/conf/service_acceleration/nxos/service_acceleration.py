'''
Service Acceleration Genie Conf Object Implementation for NXOS - CLI.
'''

# Python
from abc import ABC
from enum import Enum

# Genie
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

# service-acceleration Hierarchy
# --------------
# ServiceAcceleration
#     +- DeviceAttributes
#       +- ServiceAttributes


class ServiceAcceleration(ABC):

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
                        attributes.format('feature service-acceleration'))

                # Make sure that only enabled was provided in attributes
                # If wildcard,  then delete everything
                elif unconfig is True and\
                    attributes.attributes == {'enabled': {True: None}} or \
                        attributes.iswildcard:
                    configurations.append_line('no feature service-acceleration', raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            # service system <service_vendor> subconfig block
            with configurations.submode_context(
                    attributes.format('service system {service_vendor.value}',force=True)):

                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # service system hypershield
                #   source-interface loopback0
                if attributes.value('source_interface'):
                    configurations.append_line(
                        attributes.format('source-interface {source_interface}'))

                # service system hypershield
                #   service peer ip address <ip> [interface <interface>]
                if attributes.value('peer_ip'):
                    type_str = 'service peer ip address {peer_ip}'

                    if attributes.value('peer_interface'):
                        type_str += ' interface {peer_interface}'
                    configurations.append_line(
                        attributes.format(type_str))

                # service system hypershield
                #  controller connection-token <token>
                if attributes.value('controller_token'):
                    configurations.append_line(
                        attributes.format(
                            "controller connection-token {controller_token}"
                        )
                    )

                # service system hypershield
                #   https-proxy username <username> password <password>
                if attributes.value('https_proxy_username') and attributes.value('https_proxy_password'):
                    configurations.append_line(
                        attributes.format('https-proxy username {https_proxy_username} password {https_proxy_password}'))

                #  +- DeviceAttributes
                #      +- ServiceAttributes
                for sub, attributes2 in attributes.mapping_values('service_attr',
                                                                sort=True,
                                                                keys=self.service_attr):
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

        class ServiceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                    attributes.format('service {service_type}', force=True)):

                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # service system hypershield
                    #   service firewall
                    #     in-service
                    if attributes.value('in_service'):
                        configurations.append_line('in-service')

                    # ServiceVrf attributes config
                    for servicevrf_key, attributes2 in attributes.sequence_values('servicevrf_keys', sort=True):
                        if unconfig:
                            configurations.append_block(servicevrf_key.build_unconfig(
                                apply=False, attributes=attributes2, **kwargs))
                        else:
                            configurations.append_block(servicevrf_key.build_config(
                                apply=False, attributes=attributes2, **kwargs))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)
