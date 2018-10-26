
from abc import ABC
import warnings

from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

import re

class Te(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, links=None, apply=True, attributes=None, unconfig=False, **kwargs):
            '''Device build config'''
            assert not apply
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            
            if attributes.iswildcard:
                # iosxe : mpls traffic-eng tunnels
                configurations.append_line('mpls traffic-eng tunnels', \
                                            unconfig_cmd = 'default mpls traffic-eng tunnels')

            if attributes.value('advertise_expnull'):
                configurations.append_line('mpls traffic-eng signalling advertise explicit-null')
                
            # Add per-interface config
            for sub, attributes2 in attributes.mapping_values('interface_attr', keys=self.interfaces, sort=True):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

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

                with configurations.submode_context(attributes.format('interface {interface_name}', force=True)):

                    if attributes.iswildcard:
                        # iosxe : mpls traffic-eng tunnels
                        configurations.append_line('mpls traffic-eng tunnels', \
                                                    unconfig_cmd = 'default mpls traffic-eng tunnels')
                    
                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

class Srlg(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False):
            assert not apply
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # TODO
            pass

            return CliConfig(device=self.device, unconfig=unconfig,
                             cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True)

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False):
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
        
                # TODO
                pass

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True)

