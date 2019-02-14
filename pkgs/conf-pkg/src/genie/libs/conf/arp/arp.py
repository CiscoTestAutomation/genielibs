
from enum import Enum


# Genie package
from genie.decorator import managedattribute
from genie.conf.base import Base, \
                            DeviceFeature, \
                            LinkFeature, \
                            Interface
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, \
                                       SubAttributesDict, \
                                       AttributesHelper, \
                                       KeyedSubAttributes
from genie.conf.base.attributes import InterfaceSubAttributes
from genie.libs import parser
from genie.abstract import Lookup
from genie.ops.base import Base as ops_Base
from genie.ops.base import Context
# Genie Xbu_shared

from genie.libs.conf.base.feature import consolidate_feature_args

__all__ = (
        'Arp',
        )
# Structure Hierarchy:
# Arp
#   +--DeviceAttributes
#        +-- InterfaceAttributes
#              +-- StaticArpAttributes

class Arp(DeviceFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # =============================================
    # Device attributes
    # =============================================
    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        # InterfaceAttributes
        class InterfaceAttributes(KeyedSubAttributes):
            def __init__(self, parent,key):
                self.interface = key
                super().__init__(parent)

            # StaticArpAttributes
            class StaticArpAttributes(KeyedSubAttributes):
                def __init__(self, parent,key):
                    self.if_static_ip_address = key
                    super().__init__(parent)

            static_arp_attr = managedattribute(
                name='static_arp_attr',
                read_only=True,
                doc=StaticArpAttributes.__doc__)

            @static_arp_attr.initter
            def static_arp_attr(self):
                return SubAttributesDict(self.StaticArpAttributes, parent=self)

        interface_attr = managedattribute(
            name='interface_attr',
            read_only=True,
            doc=InterfaceAttributes.__doc__)

        @interface_attr.initter
        def interface_attr(self):
            return SubAttributesDict(self.InterfaceAttributes, parent=self)

        interface_attr = managedattribute(
            name='interface_attr',
            read_only=True,
            doc=InterfaceAttributes.__doc__)

        @interface_attr.initter
        def interface_attr(self):
            return SubAttributesDict(self.InterfaceAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ============ managedattributes ============#
    max_entries = managedattribute(
        name='max_entries',
        default=None,
        type=managedattribute.test_istype(int),
        doc='ARP Entry count limit <1-2147483647>')

    interface = managedattribute(
        name='interface',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='interface')

    if_proxy_enable = managedattribute(
        name='if_proxy_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='enabled interface proxy')

    if_local_proxy_enable = managedattribute(
        name='if_local_proxy_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='enabled interface local proxy')

    if_expire_time = managedattribute(
        name='if_expire_time',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='interface expire time')

    if_static_ip_address = managedattribute(
        name='if_static_ip_addrtess',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='static ip address')

    if_static_mac_address = managedattribute(
        name='if_static_mac_addrtess',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='static mac address')

    class staticEncapType(Enum):
        ARPA = 'arpa'

    if_static_encap_type = managedattribute(
        name='if_static_encap_type',
        default=None,
        type=(None, staticEncapType),
        doc='static encap type')

    if_static_alias = managedattribute(
        name='if_static_alias',
        default=None,
        type=managedattribute.test_istype(bool),
        doc='static alias')

    if_static_vrf = managedattribute(
        name='if_static_vrf',
        default=None,
        type=managedattribute.test_istype(str),
        doc='static vrf')

    # =========================================================
    #   build_config
    # =========================================================
    def build_config(self, devices=None, interfaces=None, links=None,
                     apply=True, attributes=None, **kwargs):
        attributes = AttributesHelper(self, attributes)
        cfgs = {}

        devices, interfaces, links = \
            consolidate_feature_args(self, devices, interfaces, links)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)
        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, devices=None, interfaces=None, links=None,
                       apply=True, attributes=None, **kwargs):
        attributes = AttributesHelper(self, attributes)
        cfgs = {}

        devices, interfaces, links = \
            consolidate_feature_args(self, devices, interfaces, links)
        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs
