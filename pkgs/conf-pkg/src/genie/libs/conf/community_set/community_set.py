
__all__ = (
    'CommunitySet',
)

import operator

from genie.decorator import managedattribute
from genie.conf.base import DeviceFeature
from genie.conf.base.attributes import SubAttributes, SubAttributesDict,\
    AttributesInheriter, AttributesHelper, DeviceSubAttributes

from genie.libs.conf.base import ip_address, ip_network


class CommunitySet(DeviceFeature):

    name = managedattribute(
        name='name',
        type=managedattribute.test_istype(str))

    communities = managedattribute(
        name='communities',
        finit=list)

    class DeviceAttributes(DeviceSubAttributes):

        pass

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __init__(self, name, *args, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)

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

        cfgs = {key: value for key, value in cfgs.items() if value}
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

        cfgs = {key: value for key, value in cfgs.items() if value}
        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

