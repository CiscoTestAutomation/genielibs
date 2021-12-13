''' 
OSPFv3 Genie Conf Object Implementation for NXOS:
    - Area Default Cost multi-line configuration implementation for NXOS - CLI
'''

# Python
import re
import warnings
from abc import ABC
from netaddr import IPNetwork

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class AreaDefaultCost(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # router ospf 1
        #   area 2 default-cost 10
        #   area 3 default-cost 20
        if attributes.value('af_area_id') and attributes.value('area_def_cost'):
            configurations.append_line(attributes.format(
                'area {af_area_id} default-cost {area_def_cost}'))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)
