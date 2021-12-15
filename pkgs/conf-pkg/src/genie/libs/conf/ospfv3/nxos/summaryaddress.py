''' 
OSPFv3 Genie Conf Object Implementation for NXOS:
    - summary address multi-line configuration implementation for NXOS - CLI
'''

# Python
import re
import warnings
from abc import ABC
from netaddr import IPNetwork

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class SummaryAddress(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # router ospfv3 1
        #   address-family ipv6 unicast
        #     summary-address 2001:1::1:1/112
        #     summary-address 2001:1::1:1/112 tag 10
        #     summary-address 2001:1::1:1/112 not-advertise
        if attributes.value('summary_address_prefix'):

            sum_str = 'summary-address'
            # + range {area_range_prefix}
            if re.search(r"\/", attributes.value('summary_address_prefix')):
                sum_str += ' {summary_address_prefix}'

            # + not-advertise
            if attributes.value('summary_address_not_advertise'):
                sum_str += ' not-advertise'
            # + tag {summary_address_tag}
            elif attributes.value('summary_address_tag'):
                sum_str += ' tag {summary_address_tag}'

            configurations.append_line(attributes.format(sum_str))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)
