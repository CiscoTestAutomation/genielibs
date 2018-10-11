from enum import Enum

# Genie
from genie.decorator import managedattribute
from genie.conf.base.config import CliConfig
from genie.conf.base.base import DeviceFeature
from genie.conf.base.attributes import DeviceSubAttributes,\
                                       SubAttributesDict,\
                                       AttributesHelper, \
                                       KeyedSubAttributes


# Prefix_list
#   +-- DeviceAttributes
#     +-- PrefixAttributes
#       +-- MaxLengthRangeAttributes


class PrefixList(DeviceFeature):

    def __init__(self, prefix_set_name, *args, **kwargs):
        self.name = prefix_set_name
        super().__init__(*args, **kwargs)


    class DeviceAttributes(DeviceSubAttributes):


        class PrefixAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.prefix = key
                super().__init__(parent)


            class MaxLengthRangeAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.maxlength_range = key
                    super().__init__(parent)

            maxlength_range_attr = managedattribute(
                name='maxlength_range_attr',
                read_only=True,
                doc=MaxLengthRangeAttributes.__doc__)

            @maxlength_range_attr.initter
            def maxlength_range_attr(self):
                return SubAttributesDict(self.MaxLengthRangeAttributes, parent=self)

        prefix_attr = managedattribute(
            name='prefix_attr',
            read_only=True,
            doc=PrefixAttributes.__doc__)

        @prefix_attr.initter
        def prefix_attr(self):
            return SubAttributesDict(self.PrefixAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ==================== Prefix-list attributes ====================   

    # protocol
    class PROTOCOL(Enum):
        ipv4 = 'ipv4'
        ipv6 = 'ipv6'

    protocol = managedattribute(
        name='protocol',
        default=None,
        type=(None, PROTOCOL),
        doc='ipv4 or ipv6')

    def build_config(self, devices=None, apply=True, attributes=None,
                     unconfig=False):
        cfgs = {}
        attributes = AttributesHelper(self, attributes)
        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr', sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)
        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, devices=None, apply=True, attributes=None):
        cfgs = {}
        attributes = AttributesHelper(self, attributes)
        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr', sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs

