from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

from ..rsvp import Rsvp as _Rsvp


class Rsvp(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, links=None, apply=True, attributes=None, unconfig=False, **kwargs):
            '''Device build config'''
            assert not apply
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            if attributes.value('sig_gr',force=True):
                configurations.append(attributes.format('ip rsvp signalling hello graceful-restart mode {sig_gr_mode}')) 

            configurations.append_line(attributes.format('ip rsvp signalling hello graceful-restart refresh interval {sig_hello_gr_refresh_interval}'))

            configurations.append_line(attributes.format('ip rsvp signalling hello graceful-restart refresh misses {sig_hello_gr_refresh_misses}'))

            # Add per-interface config
            for sub, attributes2 in attributes.mapping_values('interface_attr', keys=self.interfaces, sort=True):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

            # # Add per-neighbor config
            # for sub, attributes2 in attributes.mapping_values('neighbor_attr', keys=self.neighbors, sort=True):
            #     configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

            # # Add per-controller config
            # for sub, attributes2 in attributes.mapping_values('controller_attr', keys=self.controllers, sort=True):
            #     configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

            return CliConfig(device=self.device, unconfig=unconfig,
                             cli_config=configurations)

        def build_unconfig(self, links=None, apply=True, attributes=None, **kwargs):
            return self.build_config(links=links, apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                '''Interface build config'''
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxe: interface <name> (config-if)
                with configurations.submode_context(attributes.format('interface {interface_name}', force=True)):

                    if attributes.value('enable_default_bw'):
                        configurations.append_line('ip rsvp bandwidth')

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

