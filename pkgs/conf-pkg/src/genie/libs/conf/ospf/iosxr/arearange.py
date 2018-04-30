''' 
OSPF Genie Conf Object Implementation for IOSXR:
    - AreaRange multi-line configuration implementation for IOSXR - CLI
'''

# Python
import re
from abc import ABC
from netaddr import IPNetwork

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class AreaRange(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # router ospf 1
        #   range 192.168.1.0 255.255.255.0
        #   range 192.168.1.0 255.255.255.0 advertise
        #   range 192.168.1.0 255.255.255.0 not-advertise
        if attributes.value('area_range_prefix'):

            # + range {area_range_prefix}
            if re.search("\/", attributes.value('area_range_prefix')):
                range_val = IPNetwork(attributes.value('area_range_prefix'))
                prefix = str(range_val.ip)
                netmask = str(range_val.netmask)
                ar_str = ' range {} {}'.format(prefix, netmask)
            else:
                ar_str = ' range {area_range_prefix}'

            # + advertise
            # + not-advertise
            if attributes.value('area_range_advertise') is True:
                ar_str += ' advertise'
            elif attributes.value('area_range_advertise') is False:
                ar_str += ' not-advertise'

            configurations.append_line(attributes.format(ar_str))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)