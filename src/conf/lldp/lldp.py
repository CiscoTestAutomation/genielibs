
__all__ = (
    'Lldp',
)

# import genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase
from genie.conf.base.config import CliConfig
from genie.conf.base.base import DeviceFeature, InterfaceFeature
from genie.conf.base.attributes import DeviceSubAttributes,\
                                       SubAttributesDict,\
                                       AttributesHelper, \
                                       KeyedSubAttributes, SubAttributes
# import genie.libs
from genie.conf.base.attributes import InterfaceSubAttributes


# Structure
# Lldp
#  +- Device
#      +- TlvSelectAttributes
#      +- InterfaceAttributes


class ConfigurableTlvNamespace(ConfigurableBase):

    def __init__(self, tlv):
        self._tlv = tlv

    _tlv = None

    @property
    def tlv(self):
        return self._tlv

    @property
    def testbed(self):
        return self.tlv.testbed

    @property
    def device(self):
        return self.tlv.device


class Lldp(DeviceFeature, InterfaceFeature):

    # device attributes
    enabled = managedattribute(
        name='enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    hello_timer = managedattribute(
        name='hello_timer',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    hold_timer = managedattribute(
        name='hold_timer',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    reinit_timer = managedattribute(
        name='reinit_timer',
        default=None,
        type=(None, managedattribute.test_istype(int)))


    # interface attributes
    interface = managedattribute(
        name='interface',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    if_enabled = managedattribute(
        name='if_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    class DeviceAttributes(DeviceSubAttributes):

        
        class InterfaceAttributes(InterfaceSubAttributes):

            def __init__(self, parent, key):
                self.intf = key
                super().__init__(parent, key)
            
           
        interface_attr = managedattribute(
            name='interface_attr',
            read_only=True,
            doc=InterfaceAttributes.__doc__)

        @interface_attr.initter
        def interface_attr(self):
            return SubAttributesDict(
                self.InterfaceAttributes, parent=self)

        class TlvSelectAttributes(ConfigurableTlvNamespace):            
            # tlvSelect attributes
            suppress_tlv_chassis_id = managedattribute(
                name='suppress_tlv_chassis_id',
                default=None,
                type=(None, managedattribute.test_istype(bool)))

            suppress_tlv_port_id = managedattribute(
                name='suppress_tlv_port_id',
                default=None,
                type=(None, managedattribute.test_istype(bool)))

            suppress_tlv_port_description = managedattribute(
                name='suppress_tlv_port_description',
                default=None,
                type=(None, managedattribute.test_istype(bool)))

            suppress_tlv_system_name = managedattribute(
                name='suppress_tlv_system_name',
                default=None,
                type=(None, managedattribute.test_istype(bool)))

            suppress_tlv_system_description = managedattribute(
                name='suppress_tlv_system_description',
                default=None,
                type=(None, managedattribute.test_istype(bool)))
            
            suppress_tlv_system_capabilities = managedattribute(
                name='suppress_tlv_system_capabilities',
                default=None,
                type=(None, managedattribute.test_istype(bool)))

            
            suppress_tlv_management_address = managedattribute(
                name='suppress_tlv_management_address',
                default=None,
                type=(None, managedattribute.test_istype(bool)))

        tlv_select_attr = managedattribute(
            name='tlv_select_attr',
            read_only=True,
            doc=TlvSelectAttributes.__doc__)

        @tlv_select_attr.initter
        def tlv_select_attr(self):
            return self.TlvSelectAttributes(tlv=self)

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
