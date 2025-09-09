''' 
Service-Acceleration Genie Conf Object Implementation for NXOS:
    - ServiceVlan multi-line configuration implementation for NXOS - CLI
'''

# Python
import re
import warnings
from abc import ABC

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class ServiceVlan(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # service system hypershield
        #   service firewall
        #     vlan id 2 bridged-traffic module-affinity 1
        #     vlan id 3 bridged-traffic module-affinity dynamic
        if attributes.value('service_vlan_name'):
            configurations.append_line(
                attributes.format('vlan id {service_vlan_name} bridged-traffic module-affinity {module_affinity}'))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)
