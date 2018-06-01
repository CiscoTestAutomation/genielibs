
__all__ = (
    'Fdb',
)
# import genie
from genie.decorator import managedattribute
from genie.conf.base.base import DeviceFeature, InterfaceFeature
from genie.conf.base.attributes import DeviceSubAttributes,\
                                       SubAttributesDict,\
                                       AttributesHelper, \
                                       KeyedSubAttributes ,\
                                       InterfaceSubAttributes


# Structure
# Fdb
#  +- DeviceAttributes
#      +- VlanAttributes
#          +- MacAddressAttributes
#              +- InterfaceAttributes

class Fdb(DeviceFeature, InterfaceFeature):

    # device attributes
    mac_learning = managedattribute(
        name='mac_learning',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    mac_aging_time = managedattribute(
        name='mac_aging_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    maximum_entries = managedattribute(
        name='maximum_entries',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # VlanAttributes
    vlan_mac_learning = managedattribute(
        name='vlan_mac_learning',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    vlan_mac_aging_time = managedattribute(
        name='vlan_mac_aging_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    vlan_maximum_entries = managedattribute(
        name='vlan_maximum_entries',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # MacAddressAttributes
    mac_address = managedattribute(
        name='mac_address',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # InterfaceAttributes
    drop = managedattribute(
        name='drop',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    interface = managedattribute(
        name='interface',
        default=None,
        type=(None, managedattribute.test_istype(list)))

    class DeviceAttributes(DeviceSubAttributes):

        class VlanAttributes(KeyedSubAttributes):

            def __init__(self, parent, key):
                self.vlan_id = key
                super().__init__(parent)


            class MacAddressAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.mac_address = key
                    super().__init__(parent)

            mac_address_attr = managedattribute(
                name='mac_address_attr',
                read_only=True,
                doc=MacAddressAttributes.__doc__)

            @mac_address_attr.initter
            def mac_address_attr(self):
                return SubAttributesDict(self.MacAddressAttributes, parent=self)


        vlan_attr = managedattribute(
            name='vlan_attr',
            read_only=True,
            doc=VlanAttributes.__doc__)

        @vlan_attr.initter
        def vlan_attr(self):
            return SubAttributesDict(self.VlanAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __init__(self, *args, **kwargs):
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
