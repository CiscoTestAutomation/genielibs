
__all__ = (
        'IccpGroup',
        )

from pyats.datastructures import WeakList

from genie.utils.cisco_collections import typedset

from genie.decorator import managedattribute
from genie.conf.base import DeviceFeature, Interface
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, SubAttributesDict, AttributesInheriter, AttributesHelper

from genie.libs.conf.base import \
    MAC, \
    IPv4Address, IPv6Address

class IccpGroup(DeviceFeature):

    group_id = managedattribute(
        name='group_id',
        read_only=True,
        doc='Group ID (mandatory)')

    mlacp_node_id = managedattribute(
        name='mlacp_node_id',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    mlacp_system_mac = managedattribute(
        name='mlacp_system_mac',
        default=None,
        type=(None, MAC))

    mlacp_system_priority = managedattribute(
        name='mlacp_system_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    interfaces = managedattribute(
        name='interfaces',
        read_only=True,
        finit=WeakList,
        gettype=frozenset)

    def add_interface(self, interface):
        assert isinstance(interface, genie.conf.base.Interface)
        self._interfaces.append(interface)

    def remove_interface(self, interface):
        assert isinstance(interface, genie.conf.base.Interface)
        self._interfaces.remove(interface)

    backbone_interfaces = managedattribute(
        name='backbone_interfaces',
        finit=typedset(managedattribute.test_isinstance(Interface)).copy,
        type=typedset(managedattribute.test_isinstance(Interface))._from_iterable)

    isolation_recovery_delay = managedattribute(
        name='isolation_recovery_delay',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    mac_flush = managedattribute(
        name='mac_flush',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    mode = managedattribute(
        name='mode',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    primary_vlan = managedattribute(
        name='primary_vlan',
        default=None,
        type=(None,
              managedattribute.test_istype(int),
              managedattribute.test_istype(str)))

    recovery_delay = managedattribute(
        name='recovery_delay',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    secondary_vlan = managedattribute(
        name='secondary_vlan',
        default=None,
        type=(None,
              managedattribute.test_istype(int),
              managedattribute.test_istype(str)))

    multi_homing_node_id = managedattribute(
        name='multi_homing_node_id',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        backbone_interfaces = managedattribute(
            name='backbone_interfaces',
            type=typedset(managedattribute.test_isinstance(Interface))._from_iterable)

        @backbone_interfaces.defaulter
        def backbone_interfaces(self):
            device = self.device
            return frozenset(
                interface
                for interface in self.parent.backbone_interfaces
                if interface.device is device)

        class InterfaceAttributes(genie.conf.base.attributes.InterfaceSubAttributes):

            def __init__(self, parent, key):
                super().__init__(parent, key)

        interface_attr = managedattribute(
            name='interface_attr',
            read_only=True,
            doc=InterfaceAttributes.__doc__)

        @interface_attr.initter
        def interface_attr(self):
            return SubAttributesDict(self.InterfaceAttributes, parent=self)

        # interfaces -- See DeviceSubAttributes

        def __init__(self, parent, key):
            super().__init__(parent, key)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __init__(self, group_id, *args, **kwargs):
        self._group_id = int(group_id)
        self.interfaces  # init!
        super().__init__(*args, **kwargs)

    def build_config(self, devices=None, apply=True,
            attributes=None,
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

    def build_unconfig(self, devices=None, apply=True,
            attributes=None,
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

