
__all__ = (
        'Isis',
        )

from enum import Enum
import ipaddress
import binascii
from ipaddress import IPv4Address, IPv4Interface, IPv6Address, IPv6Interface

from genie.utils.cisco_collections import typedset

from genie.decorator import managedattribute
from genie.conf.base import Base, DeviceFeature, InterfaceFeature, LinkFeature, Interface
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, SubAttributesDict, AttributesHelper

from genie.libs.conf.base import Routing
from genie.libs.conf.address_family import AddressFamily, AddressFamilySubAttributes
from .isis_net import IsisAreaAddress, IsisSystemID, IsisNET


class Isis(Routing, DeviceFeature, InterfaceFeature, LinkFeature):

    pid = managedattribute(
        name='pid',
        type=str,
        doc='Process ID (mandatory)')

    address_families = managedattribute(
        name='address_families',
        finit=typedset(AddressFamily, {AddressFamily.ipv4_unicast}).copy,
        type=typedset(AddressFamily)._from_iterable)

    class MetricStyle(Enum):
        narrow = 'narrow'
        wide = 'wide'
        transition = 'transition'
        narrow_transition = 'narrow transition'
        wide_transition = 'wide transition'

    metric_style = managedattribute(
        name='metric_style',
        default=None,
        type=(None, MetricStyle))

    metric = managedattribute(
        name='metric',
        default=None,
        type=(None, int, str))

    class IsType(Enum):
        level_1 = 'level 1'
        level_1_2 = 'level 1 and 2'
        level_2 = 'level 2'

    is_type = managedattribute(
        name='is_type',
        default=None,
        type=(None, IsType))

    ispf_type = managedattribute(
        name='ispf_type',
        default=None,
        type=(None, IsType))

    circuit_type = managedattribute(
        name='circuit_type',
        default=None,
        type=(None, IsType))

    maximum_paths = managedattribute(
        name='maximum_paths',
        default=None,
        type=(None, int))

    ldp_auto_config = managedattribute(
        name='ldp_auto_config',
        default=None,
        type=(None, bool))

    ldp_sync = managedattribute(
        name='ldp_sync',
        default=None,
        type=(None, bool))

    ldp_sync_shortcut = managedattribute(
        name='ldp_sync_shortcut',
        default=None,
        type=(None, bool))

    ldp_auto_config_shortcut = managedattribute(
        name='ldp_auto_config_shortcut',
        default=None,
        type=(None, bool))

    distribute_link_state = managedattribute(
        name='distribute_link_state',
        default=None,
        type=(None, bool))

    mpls_te_level = managedattribute(
        name='mpls_te_level',
        default=None,
        type=(None, IsType))

    mpls_te_rtrid = managedattribute(
        name='mpls_te_rtrid',
        default=None,
        type=(None, managedattribute.test_isinstance(Interface)))

    net_id = managedattribute(
        name='net_id',
        read_only=True,
        doc='''Single Network Entity Title (NET). Only meaningful per device.''')

    net_ids = managedattribute(
        name='net_ids',
        read_only=True,
        doc='''Set of Network Entity Title (NET). Only meaningful per device.''')

    area_addresses = managedattribute(
        name='area_addresses',
        type=(None, managedattribute.test_set_of(IsisAreaAddress)),
        doc='''Set of area address part of Network Entity Title (NET).

        Default value is a single area address unique value based on ISIS process ID.

        Set to None to trigger each device to have a unique value based on individual device name.
        ''')

    @area_addresses.defaulter
    def area_addresses(self):
        unique_int = binascii.crc32(self.pid.encode())
        return frozenset([
            IsisAreaAddress(
                '47.{:04X}.{:04X}'.format(
                    (unique_int >> 16) & 0xFFFF,
                    unique_int & 0xFFFF,
                ))])

    @property
    def area_address(self):
        '''The area address part of the Network Entity Title (NET).

        `area_address` can be assigned to and will set `area_addresses` to a
        single item.

        `area_address`'s value is a single area address, or None. Use
        `area_addresses` to retrieve all the area addresses. Assign
        `area_addresses` to support multiple area addresses.
        '''
        area_addresses = self.area_addresses
        if area_addresses:
            for area_address in sorted(self.area_addresses):
                return area_address
        return None

    @area_address.setter
    def area_address(self, value):
        if value is None:
            self.area_addresses = None
        else:
            self.area_addresses = {value}

    @area_address.deleter
    def area_address(self):
        del self.area_addresses

    system_id = managedattribute(
        name='system_id',
        default=None,
        type=(None, IsisSystemID),
        doc='''System ID. Assign to make all devices use the same System ID for level 1 operation.''')

    class Nsf(Enum):
        cisco = 'cisco'
        ietf = 'ietf'

    nsf = managedattribute(
        name='nsf',
        default=None,
        type=(None, Nsf))

    nsf_lifetime = managedattribute(
        name='nsf_lifetime',
        default=None,
        type=(None, int))

    nsr = managedattribute(
        name='nsr',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    redistribute_connected = managedattribute(
        name='redistribute_connected',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    passive = managedattribute(
        name='passive',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    point_to_point = managedattribute(
        name='point_to_point',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    shutdown = managedattribute(
        name='shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nsf_lifetime = managedattribute(
        name='lsp_mtu',
        default=None,
        type=(None, int))

    segment_routing_mpls = managedattribute(
        name='segment_routing_mpls',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    segment_routing_mpls_sr_prefer = managedattribute(
        name='segment_routing_mpls_sr_prefer',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    segment_routing_prefix_sid_map_advertise_local = managedattribute(
        name='segment_routing_prefix_sid_map_advertise_local',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    segment_routing_prefix_sid_map_receive = managedattribute(
        name='segment_routing_prefix_sid_map_receive',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # NOTE: prefix_sid and prefix_sid_index are mutually exclusive
    prefix_sid = managedattribute(
        name='prefix_sid',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # NOTE: prefix_sid and prefix_sid_index are mutually exclusive
    prefix_sid_index = managedattribute(
        name='prefix_sid_index',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    prefix_sid_explicit_null = managedattribute(
        name='prefix_sid_explicit_null',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    prefix_sid_n_flag_clear = managedattribute(
        name='prefix_sid_n_flag_clear',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        address_families = managedattribute(
            name='address_families',
            type=typedset(AddressFamily)._from_iterable)

        @address_families.defaulter
        def address_families(self):
            return frozenset(self.parent.address_families)

        area_addresses = managedattribute(
            name='area_addresses',
            type=managedattribute.test_set_of(IsisAreaAddress),
            doc='''Set of area address part of Network Entity Title (NET).

            Default value is taken from parent Isis object or, if None, a single area address unique value based on device name.
            ''')

        @area_addresses.defaulter
        def area_addresses(self):
            area_addresses = self.parent.area_addresses
            if area_addresses is None:
                unique_int = binascii.crc32(self.device_name.encode())
                area_addresses = [
                    IsisAreaAddress(
                        '47.{:04X}.{:04X}'.format(
                            (unique_int >> 16) & 0xFFFF,
                            unique_int & 0xFFFF,
                        ))]
            return frozenset(area_addresses)

        @property
        def area_address(self):
            '''The area address part of the Network Entity Title (NET).

            `area_address` can be assigned to and will set `area_addresses` to a
            single item.

            `area_address`'s value is a single area address, or None. Use
            `area_addresses` to retrieve all the area addresses. Assign
            `area_addresses` to support multiple area addresses.
            '''
            for area_address in sorted(self.area_addresses):
                return area_address
            return None

        @area_address.setter
        def area_address(self, value):
            self.area_addresses = {value}

        @area_address.deleter
        def area_address(self):
            del self.area_addresses

        system_id = managedattribute(
            name='system_id',
            type=IsisSystemID,
            doc='The system ID. Default is a unique value per device name.')

        @system_id.defaulter
        def system_id(self):
            system_id = self.parent.system_id
            if system_id is None:
                unique_int = binascii.crc32(self.device_name.encode())
                system_id = IsisSystemID(
                    'FFFF.{:04X}.{:04X}'.format(
                        (unique_int >> 16) & 0xFFFF,
                        unique_int & 0xFFFF,
                    ))
            return system_id

        @property
        def net_ids(self):
            '''The set of Network Entity Titles (NETs).

            Please assign using `system_id`, `area_addresses` or `net_id`.
            '''
            system_id = self.system_id
            return frozenset([
                IsisNET(area_address=area_address, system_id=system_id)
                for area_address in self.area_addresses])

        @property
        def net_id(self):
            '''The Network Entity Title (NET).

            The NET is formatted as `{area_address}.{system_id}.00`

            There can be only 1 `system_id` but there can be multiple areas (`area_addresses`).

            `net_id` can be assigned to and will set `area_addresses` to a
            single item as well as `system_id` to the desired value.

            `net_id`'s value is a single NET, or None. Use `net_ids` to
            retrieve all the NETs. Assign `area_addresses` and `system_id` to
            support multiple NETs.
            '''
            for net_id in sorted(self.net_ids):
                return net_id
            return None

        @net_id.setter
        def net_id(self, value):
            if value is None:
                self.area_addresses = ()
            else:
                net_id = IsisNET(value)
                self.system_id = net_id.system_id
                self.area_address = net_id.area_address

        @net_id.deleter
        def net_id(self):
            try:
                del self.area_address
            except AttributeError:
                pass
            try:
                del self.system_id
            except AttributeError:
                pass

        class AddressFamilyAttributes(AddressFamilySubAttributes):

            def __init__(self, parent, key):
                super().__init__(parent, key)

        address_family_attr = managedattribute(
            name='address_family_attr',
            read_only=True,
            doc=AddressFamilyAttributes.__doc__)

        @address_family_attr.initter
        def address_family_attr(self):
            return SubAttributesDict(self.AddressFamilyAttributes, parent=self)

        class InterfaceAttributes(genie.conf.base.attributes.InterfaceSubAttributes):

            address_families = managedattribute(
                name='address_families',
                type=typedset(AddressFamily)._from_iterable)

            @address_families.defaulter
            def address_families(self):
                return frozenset(self.parent.address_families)

            class AddressFamilyAttributes(AddressFamilySubAttributes):

                def __init__(self, parent, key):
                    super().__init__(parent, key)

            address_family_attr = managedattribute(
                name='address_family_attr', read_only=True,
                doc=AddressFamilyAttributes.__doc__)

            @address_family_attr.initter
            def address_family_attr(self):
                return SubAttributesDict(self.AddressFamilyAttributes, parent=self)

            def __init__(self, parent, key):
                super().__init__(parent, key)

        interface_attr = managedattribute(
            name='interface_attr',
            read_only=True,
            doc=InterfaceAttributes.__doc__)

        @interface_attr.initter
        def interface_attr(self):
            return SubAttributesDict(self.InterfaceAttributes, parent=self)

        def __init__(self, parent, key):
            super().__init__(parent, key)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __init__(self, pid, *args, **kwargs):
        self.pid = pid
        super().__init__(*args, **kwargs)

    def build_config(self, devices=None, apply=True, attributes=None,
                     **kwargs):
        cfgs = {}
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

