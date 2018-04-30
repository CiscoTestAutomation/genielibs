__all__ = (
        'Mcast',
        )

# Genie
from genie.utils.cisco_collections import typedset
from genie.decorator import managedattribute
from genie.conf.base.config import CliConfig
from genie.conf.base.base import DeviceFeature, InterfaceFeature

from .mroute import Mroute
from genie.libs.conf.base import Routing
from genie.libs.conf.vrf import Vrf, VrfSubAttributes
from genie.libs.conf.address_family import AddressFamily,\
                                            AddressFamilySubAttributes
from genie.conf.base.attributes import DeviceSubAttributes, SubAttributesDict,\
                                       InterfaceSubAttributes, AttributesHelper,\
                                       KeyedSubAttributes

# Structure Hierarchy:
# Mcast
#   +--DeviceAttributes
#      +--VrfAttributes


class Mcast(Routing, DeviceFeature, InterfaceFeature):

    # ==================== MCAST attributes ====================

    # feature pim/pim6
    enabled = managedattribute(
        name='enabled',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="Enable or disable both feature pim and pim6 on the device.")

    # multipath
    multipath = managedattribute(
        name='multipath',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="Configure 'ip multicast multipath' on the device.")

    # if_enable
    if_enable = managedattribute(
        name='if_enable',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="Configure 'enable' on the device interface.")

    # ===========================================================

    # Compatibility
    address_families = managedattribute(
        name='address_families',
        finit=typedset(AddressFamily, {AddressFamily.ipv4}).copy,
        type=typedset(AddressFamily)._from_iterable)

    # Compatibility
    @property
    def vrfs(self):
        return \
            self.force_vrfs | \
            {intf.vrf for intf in self.interfaces}

    # Compatibility
    force_vrfs = managedattribute(
        name='force_vrfs',
        read_only=True,
        finit=set,
        gettype=frozenset)
        # XXXJST TODO force_vrfs needs to also be accessible per-device. Being read_only, that can't happen

    # Compatibility
    def add_force_vrf(self, vrf):
        assert vrf is None or isinstance(vrf, Vrf)
        self.force_vrfs  # init!
        self._force_vrfs.add(vrf)

    # Compatibility
    def remove_force_vrf(self, vrf):
        assert vrf is None or isinstance(vrf, Vrf)
        self.force_vrfs  # init!
        self._force_vrfs.remove(vrf)

    # ===========================================================

    class DeviceAttributes(DeviceSubAttributes):

        mroutes = managedattribute(
            name='mroutes',
            finit=typedset(managedattribute.test_isinstance(Mroute)).copy,
            type=typedset(managedattribute.test_isinstance(Mroute))._from_iterable,
            doc='A `set` of Mroute associated objects')

        def add_mroute(self, mroute):
            self.mroutes.add(mroute)

        def remove_mroute(self, mroute):
            mroute._device = None
            try:
                self.mroutes.remove(mroute)
            except:
                pass

        # Compatibility
        address_families = managedattribute(
            name='address_families',
            type=typedset(AddressFamily)._from_iterable)

        # Compatibility
        @property
        def vrfs(self):
            return \
                self.force_vrfs | \
                {intf.vrf for intf in self.interfaces}

        # Compatibility
        @address_families.defaulter
        def address_families(self):
            return frozenset(self.parent.address_families)


        class VrfAttributes(VrfSubAttributes):

            def __init__(self, parent, key):
                self.vrf_id = key
                super().__init__(parent, key)

            mroutes = managedattribute(
                name='mroutes',
                finit=typedset(managedattribute.test_isinstance(Mroute)).copy,
                type=typedset(managedattribute.test_isinstance(Mroute))._from_iterable,
                doc='A `set` of Mroute associated objects')

            def add_mroute(self, mroute):
                self.mroutes.add(mroute)

            def remove_mroute(self, mroute):
                mroute._device = None
                try:
                    self.mroutes.remove(mroute)
                except:
                    pass

            # Compatibility
            address_families = managedattribute(
                name='address_families',
                type=typedset(AddressFamily)._from_iterable)

            # Compatibility
            @address_families.defaulter
            def address_families(self):
                return frozenset(self.parent.address_families)

            class AddressFamilyAttributes(AddressFamilySubAttributes):

                mroutes = managedattribute(
                    name='mroutes',
                    finit=typedset(managedattribute.test_isinstance(Mroute)).copy,
                    type=typedset(managedattribute.test_isinstance(Mroute))._from_iterable,
                    doc='A `set` of Mroute associated objects')

                def add_mroute(self, mroute):
                    self.mroutes.add(mroute)

                def remove_mroute(self, mroute):
                    mroute._device = None
                    try:
                        self.mroutes.remove(mroute)
                    except:
                        pass

                # Compatibility
                class InterfaceAttributes(InterfaceSubAttributes):
                    pass

                interface_attr = managedattribute(
                    name='interface_attr',
                    read_only=True,
                    doc=InterfaceAttributes.__doc__)

                @interface_attr.initter
                def interface_attr(self):
                    return SubAttributesDict(
                        self.InterfaceAttributes, parent=self)

            address_family_attr = managedattribute(
                name='address_family_attr',
                read_only=True,
                doc=AddressFamilySubAttributes.__doc__)

            @address_family_attr.initter
            def address_family_attr(self):
                return SubAttributesDict(self.AddressFamilyAttributes,
                                         parent=self)

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

    # ===========================================================

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
