# Python
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

# Genie Xbu_shared
from genie.libs.conf.base.feature import consolidate_feature_args

__all__ = (
        'StaticRouting',
        )
# Table of contents:
#     class StaticRouting:
#         class DeviceAttributes:
#             class VrfAttributes:
#                 class AddressFamilyAttributes:
#                     class RouteAttributes:
#                         class InterfaceAttributes:
#                         class NextHopAttributes:

class StaticRouting(DeviceFeature, LinkFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # =============================================
    # Device attributes
    # =============================================
    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        # VrfAttributes
        class VrfAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.vrf = key
                super().__init__(parent=parent)

            # AddressFamilyAttribute
            class AddressFamilyAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.af = key
                    super().__init__(parent)

                # RouteAttributes
                class RouteAttributes(KeyedSubAttributes):
                    def __init__(self, parent, key):
                        self.route = key
                        super().__init__(parent)

                    # InterfaceAttributes
                    class InterfaceAttributes(KeyedSubAttributes):
                        def __init__(self, parent, key):
                            self.interface = key
                            super().__init__(parent)

                    interface_attr = managedattribute(
                        name='interface_attr',
                        read_only=True,
                        doc=InterfaceAttributes.__doc__)

                    @interface_attr.initter
                    def interface_attr(self):
                        return SubAttributesDict(self.InterfaceAttributes, parent=self)

                    # NextHopAttributes
                    class NextHopAttributes(KeyedSubAttributes):
                        def __init__(self, parent, key):
                            self.nexthop = key
                            super().__init__(parent)

                    next_hop_attr = managedattribute(
                        name='next_hop_attr',
                        read_only=True,
                        doc=NextHopAttributes.__doc__)

                    @next_hop_attr.initter
                    def next_hop_attr(self):
                        return SubAttributesDict(self.NextHopAttributes, parent=self)


                route_attr = managedattribute(
                    name='route_attr',
                    read_only=True,
                    doc=RouteAttributes.__doc__)

                @route_attr.initter
                def route_attr(self):
                    return SubAttributesDict(self.RouteAttributes, parent=self)


            address_family_attr = managedattribute(
                name='address_family_attr',
                read_only=True,
                doc=AddressFamilyAttributes.__doc__)

            @address_family_attr.initter
            def address_family_attr(self):
                return SubAttributesDict(self.AddressFamilyAttributes, parent=self)

        vrf_attr = managedattribute(
            name='vrf_attr',
            read_only=True,
            doc=VrfAttributes.__doc__)

        @vrf_attr.initter
        def vrf_attr(self):
            return SubAttributesDict(self.VrfAttributes, parent=self)


    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ============       managedattributes ============#
    vrf = managedattribute(
        name='vrf',
        default=None,
        type=managedattribute.test_istype(str),
        doc='Vrf Name')

    # address_family
    class ADDRESS_FAMILY(Enum):
        ipv4 = 'ipv4'
        ipv6 = 'ipv6'

    af = managedattribute(
        name='address_family',
        default='ipv4',
        type=(None, ADDRESS_FAMILY),
        doc='Configure static routing address family')

    route = managedattribute(
        name='route',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='route name')

    interface = managedattribute(
        name='interface',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Interface name')

    if_nexthop = managedattribute(
        name='if_nexthop',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Next hop')

    if_preference = managedattribute(
        name='if_preference',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Preference')

    if_tag = managedattribute(
        name='if_tag',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Tag')

    if_track = managedattribute(
        name='if_track',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Track')

    if_nh_vrf = managedattribute(
        name='if_nh_vrf',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='vrf for next hop')

    nexthop = managedattribute(
        name='nexthop',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Next hop')

    preference = managedattribute(
        name='preference',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Preference')

    tag = managedattribute(
        name='tag',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Tag')

    track = managedattribute(
        name='track',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Track')

    nh_vrf = managedattribute(
        name='nh_vrf',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='vrf for next hop')

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
