
__all__ = (
    'Routing',
)

# Python
from enum import Enum

# Genie
from genie.decorator import managedattribute
from genie.conf.base.config import CliConfig
from genie.conf.base.base import DeviceFeature, LinkFeature
from genie.conf.base.attributes import DeviceSubAttributes, SubAttributesDict,\
                                       AttributesHelper

# Routing Heirarchy
# -----------------
# Routing
#  +- DeviceAttributes


class Routing(DeviceFeature, LinkFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ==========================================================================
    #                           CONF CLASS STRUCTURE
    # ==========================================================================

    # +- DeviceAttributes
    class DeviceAttributes(DeviceSubAttributes):
        pass

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================
    
    # enabled
    enabled = managedattribute(
        name='enabled',
        default=None,
        type=managedattribute.test_istype(bool),
        doc='Enable both ip routing and ipv6 unicast routing')

    # enabled_ipv6_unicast_routing
    enabled_ipv6_unicast_routing = managedattribute(
        name='enabled_ipv6_unicast_routing',
        default=None,
        type=managedattribute.test_istype(bool),
        doc='Enable ipv6 unicast routing')

    # enabled_ip_routing
    enabled_ip_routing = managedattribute(
        name='enabled_ip_routing',
        default=None,
        type=managedattribute.test_istype(bool),
        doc='Enable ip routing')

    # ==========================================================================
    #                       BUILD_CONFIG & BUILD_UNCONFIG
    # ==========================================================================

    def build_config(self, devices=None, apply=True, attributes=None,
                     **kwargs):
        cfgs = {}
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs


    def build_unconfig(self, devices=None, apply=True, attributes=None,
                       **kwargs):
        cfgs = {}
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

