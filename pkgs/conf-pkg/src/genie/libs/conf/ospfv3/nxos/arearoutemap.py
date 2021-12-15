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


class AreaRouteMap(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # router ospfv3 1
        #   address-family ipv6 unicast
        #     area {area-id} filter-list route-map map-name out
        #     area {area-id} filter-list route-map map-name in
        if attributes.value('routemap_area_id') and attributes.value('ar_route_map_in'):
            configurations.append_line(attributes.format(
                'area {routemap_area_id} filter-list route-map {ar_route_map_in} in'))

        if attributes.value('routemap_area_id') and attributes.value('ar_route_map_out'):
            configurations.append_line(attributes.format(
                'area {routemap_area_id} filter-list route-map {ar_route_map_out} out'))
        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)
