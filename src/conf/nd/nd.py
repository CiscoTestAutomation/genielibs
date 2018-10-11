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
        'Nd',
        )
# Table of contents:
#   class Nd:
#      class DeviceAttributes:
#         class InterfaceAttributes:
#            class NeighborAttributes:

class Nd(DeviceFeature, LinkFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # =============================================
    # Device attributes
    # =============================================
    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        # InterfaceAttributes
        class InterfaceAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.interface = key
                super().__init__(parent=parent)

            # NeighborAttribute
            class NeighborAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.ip = key
                    super().__init__(parent)

            neighbor_attr = managedattribute(
                name='neighbor_attr',
                read_only=True,
                doc=NeighborAttributes.__doc__)

            @neighbor_attr.initter
            def neighbor_attr(self):
                return SubAttributesDict(self.NeighborAttributes, parent=self)

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

    # ============       managedattributes ============#
    interface = managedattribute(
        name='interface',
        default=None,
        type=managedattribute.test_istype(str),
        doc='Interface')

    if_ra_interval = managedattribute(
        name='if_ra_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='set interface periodic interval')

    if_ra_lifetime = managedattribute(
        name='if_ra_lifetime',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='set router lifetime')

    if_ra_suppress = managedattribute(
        name='if_ra_suppress',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable suppress RA')

    ip = managedattribute(
        name='ip',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='neighbor ip')

    link_layer_address = managedattribute(
        name='link_layer_address',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='set Mac address')

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
