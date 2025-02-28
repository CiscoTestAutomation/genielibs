''' 
Service-Acceleration Genie Conf Object Implementation for NXOS:
    - ServiceVrf multi-line configuration implementation for NXOS - CLI
'''

# Python
import re
import warnings
from abc import ABC

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class ServiceVrf(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # service system hypershield
        #   service firewall
        #     vrf vrf1 module-affinity dynamic
        #     vrf vrf2 module-affinity 1
        if attributes.value('service_vrf_name'):
            configurations.append_line(
                attributes.format('vrf {service_vrf_name} module-affinity {module_affinity}'))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)
