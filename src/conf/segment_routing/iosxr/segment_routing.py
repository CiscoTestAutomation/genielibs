
from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

from genie.libs.conf.route_policy import RoutePolicy


class SegmentRouting(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: segment-routing (config-sr)
            with configurations.submode_context('segment-routing'):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # iosxr: segment-routing / global-block 16000 16001
                v = attributes.value('global_block')
                if v is not None:
                    configurations.append_line('global-block {first} {last}'.format(
                        first=v.start,
                        last=v[-1]))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

    # TODO
    # iosxr: segment-routing / mapping-server (config-sr-ms)
    # iosxr: segment-routing / mapping-server / prefix-sid-map (config-sr-ms-map)
    # iosxr: segment-routing / mapping-server / prefix-sid-map / address-family ipv4 (config-sr-ms-map-af)
    # iosxr: segment-routing / mapping-server / prefix-sid-map / address-family ipv4 / 1.2.3.0/24 <0-1048575>
    # iosxr: segment-routing / mapping-server / prefix-sid-map / address-family ipv4 / 1.2.3.0/24 <0-1048575> attached
    # iosxr: segment-routing / mapping-server / prefix-sid-map / address-family ipv4 / 1.2.3.0/24 <0-1048575> range <0-1048575>
    # iosxr: segment-routing / mapping-server / prefix-sid-map / address-family ipv4 / 1.2.3.0/24 <0-1048575> range <0-1048575> attached
    # iosxr: segment-routing / mapping-server / prefix-sid-map / address-family ipv6 (config-sr-ms-map-af)
    # iosxr: segment-routing / mapping-server / prefix-sid-map / address-family ipv6 / 1:2::3/128 <0-1048575>
    # iosxr: segment-routing / mapping-server / prefix-sid-map / address-family ipv6 / 1:2::3/128 <0-1048575> attached
    # iosxr: segment-routing / mapping-server / prefix-sid-map / address-family ipv6 / 1:2::3/128 <0-1048575> range <0-1048575>
    # iosxr: segment-routing / mapping-server / prefix-sid-map / address-family ipv6 / 1:2::3/128 <0-1048575> range <0-1048575> attached

