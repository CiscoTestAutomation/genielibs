''' 
OSPFv3 Genie Conf Object Implementation for NXOS:
    - AreaRange multi-line configuration implementation for NXOS - CLI
'''

# Python
import re
import warnings
from abc import ABC
from netaddr import IPNetwork

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class AreaRange(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # router ospf 1
        #   area 2 range 2001:1::1:1/112 cost 10
        #   area 2 range 2001:1::1:1/112 advertise cost 10
        #   area 2 range 2001:1::1:1/112 not-advertise cost 10
        if attributes.value('range_area_id') and attributes.value('area_range_prefix'):

            # area {area}
            ar_str = 'area {range_area_id}'

            # + range {area_range_prefix}
            if re.search(r"\/", attributes.value('area_range_prefix')):
                ar_str += ' range {area_range_prefix}'

            # + not-advertise
            if attributes.value('area_range_not_advertise'):
                ar_str += ' not-advertise'

            # + cost {area_range_cost}
            if attributes.value('area_range_cost'):
                ar_str += ' cost {area_range_cost}'

            configurations.append_line(attributes.format(ar_str))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)
