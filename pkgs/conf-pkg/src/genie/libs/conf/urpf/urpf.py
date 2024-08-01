__all__ = ("Urpf",)

# genie
from genie.decorator import managedattribute
from genie.conf.base.base import DeviceFeature, InterfaceFeature
from genie.utils.cisco_collections import typedset

# genie.libs
from genie.conf.base.attributes import (
    DeviceSubAttributes,
    SubAttributesDict,
    AttributesHelper,
    InterfaceSubAttributes,
)

# Multi-line config classes
from .ipverify import IpVerify
from .ipv6verify import Ipv6Verify

# Structure Hierarchy:
# URPF
# +-- DeviceAttribute
#     +--InterfaceAttribute


class Urpf(DeviceFeature, InterfaceFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ==========================================================================
    #                           CONF CLASS STRUCTURE
    # ==========================================================================

    # +- DeviceAttributes
    class DeviceAttributes(DeviceSubAttributes):

        # +- DeviceAttributes
        #   +- InterfaceAttributes
        class InterfaceAttributes(InterfaceSubAttributes):
            def __init__(self, parent, key):
                super().__init__(parent, key)

            # ip verify source multi-line configs
            ip_urpf_keys = managedattribute(
                name="ip_urpf_keys",
                finit=typedset(managedattribute.test_isinstance(IpVerify)).copy,
                type=typedset(
                    managedattribute.test_isinstance(IpVerify)
                )._from_iterable,
                doc="A `set` of ip verify source keys objects",
            )

            def add_ip_urpf_key(self, ip_urpf_key):
                self.ip_urpf_keys.add(ip_urpf_key)

            def remove_ip_key(self, ip_urpf_key):
                ip_urpf_key._device = None
                try:
                    self.ip_urpf_keys.remove(ip_urpf_key)
                except:
                    pass

            # ipv6 verify source multi-line configs
            ipv6_urpf_keys = managedattribute(
                name="ipv6_urpf_keys",
                finit=typedset(managedattribute.test_isinstance(Ipv6Verify)).copy,
                type=typedset(
                    managedattribute.test_isinstance(Ipv6Verify)
                )._from_iterable,
                doc="A `set` of ipv6 verify source keys objects",
            )

            def add_ipv6_urpf_key(self, ipv6_urpf_key):
                self.ipv6_urpf_keys.add(ipv6_urpf_key)

            def remove_ip_key(self, ipv6_urpf_key):
                ipv6_urpf_key._device = None
                try:
                    self.ipv6_urpf_keys.remove(ipv6_urpf_key)
                except:
                    pass

        interface_attr = managedattribute(
            name="interface_attr", read_only=True, doc=InterfaceAttributes.__doc__
        )

        @interface_attr.initter
        def interface_attr(self):
            return SubAttributesDict(self.InterfaceAttributes, parent=self)

    device_attr = managedattribute(
        name="device_attr", read_only=True, doc=DeviceAttributes.__doc__
    )

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================

    # enabled
    enabled = managedattribute(
        name="enabled", default=None, type=(None, managedattribute.test_istype(bool))
    )

    # ==========================================================================
    # +- DeviceAttributes
    #   +- InterfaceAttributes
    # ==========================================================================

    # if_name - Attribute key

    # ==========================================================================
    #                       BUILD_CONFIG & BUILD_UNCONFIG
    # ==========================================================================

    def build_config(self, devices=None, apply=True, attributes=None, **kwargs):
        cfgs = {}
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
            "device_attr", keys=devices, sort=True
        ):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, devices=None, apply=True, attributes=None, **kwargs):
        cfgs = {}
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
            "device_attr", keys=devices, sort=True
        ):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs
