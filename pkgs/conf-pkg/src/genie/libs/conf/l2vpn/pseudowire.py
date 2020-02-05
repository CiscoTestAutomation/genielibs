
__all__ = (
    'Pseudowire',
    'PseudowireIPv4Neighbor',
    'PseudowireIPv6Neighbor',
    'PseudowireEviNeighbor',
    'PseudowireClass',
    # Abstract classes:
    'PseudowireNeighbor',
    'PseudowireIPNeighbor',
)

import functools
import weakref
import ipaddress
from enum import Enum

from pyats.datastructures import WeakList

from genie.decorator import managedattribute
from genie.conf.base import Base, Device, Interface, DeviceFeature
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, SubAttributesDict, AttributesInheriter, AttributesHelper

from genie.libs.conf.base import Neighbor, IPNeighbor, IPv4Neighbor, IPv6Neighbor, IPv4Address, IPv6Address, MAC
from genie.libs.conf.evpn.evi import Evi, EviNeighbor


class PseudowireNeighbor(Neighbor):

    container = managedattribute(
        name='container',
        read_only=True,
        gettype=managedattribute.auto_unref,
        doc='The container (BridgeDomain, Xconnect, Vfi, Pseudowire, Evpn) (mandatory)')

    device = managedattribute(
        name='device',
        read_only=True,
        gettype=managedattribute.auto_unref,
        doc='The device (mandatory)')

    pseudowire_interface = managedattribute(
        name='pseudowire_interface',
        default=None,
        type=(None,
              managedattribute.test_isinstance((
                  Interface,  # e.g.: iosxe PseudowireInterface
              ))))

    @property
    def testbed(self):
        device = self.device
        return device and device.testbed

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if cls is PseudowireNeighbor:
            if 'ip' in kwargs:
                factory_cls = PseudowireIPNeighbor
            elif 'evi' in kwargs:
                factory_cls = PseudowireEviNeighbor
            else:
                raise TypeError('\'ip\' or \'evi\' arguments missing')

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self

    def __init__(self, container, device=None, **kwargs):
        assert container
        if device is None:
            device = container.device
        assert isinstance(device, Device)
        self._container = weakref.ref(container)
        self._device = weakref.ref(device)
        super().__init__(**kwargs)

    def _neighbor_comparison_tokens(self):
        container = self.container
        return super()._neighbor_comparison_tokens() + (
            'device', self.device,
            'container', container and __class__.__name__, container,
        )

    def __hash__(self):
        return hash((self.device, self.container))


class PseudowireIPNeighbor(PseudowireNeighbor, IPNeighbor):

    pw_id = managedattribute(
        name='pw_id',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if cls is PseudowireIPNeighbor:
            try:
                ip = kwargs['ip']
            except KeyError:
                raise TypeError('\'ip\' argument missing')
            ip = ipaddress.ip_address(ip)
            if isinstance(ip, ipaddress.IPv4Address):
                factory_cls = PseudowireIPv4Neighbor
            elif isinstance(ip, ipaddress.IPv6Address):
                factory_cls = PseudowireIPv6Neighbor
            else:
                raise ValueError(ip)

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self

    def __repr__(self):
        s = '<{}'.format(
            self.__class__.__name__,
        )
        s += ' {}:{}'.format(
            self.ip,
            self.pw_id,
        )
        s += '>'
        return s

    def __hash__(self):
        return hash((self.device, self.container, repr(self)))


class PseudowireIPv4Neighbor(PseudowireIPNeighbor, IPv4Neighbor):
    pass


class PseudowireIPv6Neighbor(PseudowireIPNeighbor, IPv6Neighbor):
    pass


class PseudowireEviNeighbor(PseudowireNeighbor, EviNeighbor):

    source_ac_id = managedattribute(
        name='source_ac_id',
        type=(None, managedattribute.test_istype(int)))

    @source_ac_id.defaulter
    def source_ac_id(self):
        return self.ac_id

    def _neighbor_comparison_tokens(self):
        return super()._neighbor_comparison_tokens() + (
            'source_ac_id', self.source_ac_id,
        )

    def __repr__(self):
        s = '<{}'.format(
            self.__class__.__name__,
        )
        s += ' EVI {} AC {}'.format(
            self.evi.evi_id,
            self.ac_id,
        )
        if self.source_ac_id != self.ac_id:
            s += ' (source {})'.format(
                self.source_ac_id,
            )
        s += '>'


class PseudowireNeighborSubAttributes(genie.conf.base.attributes.KeyedSubAttributes):

    neighbor = managedattribute(
        name='neighbor',
        read_only=True,  # key
        gettype=managedattribute.auto_unref)

    @property
    def remote_neighbor(self):
        local_neighbor = self.neighbor
        for pw in self.parent.pseudowires:
            if local_neighbor not in pw.neighbors:
                continue
            for remote_neighbor in pw.neighbors:
                if remote_neighbor is local_neighbor:
                    continue
                return remote_neighbor

    @property
    def ip(self):
        return getattr(self.neighbor, 'ip', None)

    @property
    def pw_id(self):
        return getattr(self.neighbor, 'pw_id', None)

    @property
    def evi(self):
        return getattr(self.neighbor, 'evi', None)

    @property
    def ac_id(self):
        return getattr(self.neighbor, 'ac_id', None)

    @property
    def source_ac_id(self):
        return getattr(self.neighbor, 'source_ac_id', None)

    @classmethod
    def _sanitize_key(cls, key):
        return key

    @classmethod
    def _assert_key_allowed(cls, key):
        if not isinstance(key, PseudowireNeighbor):
            raise KeyError('{cls} only accepts PseudowireNeighbor instances, not {key!r}'.
                    format(cls=cls.__name__,
                        key=key))

    def __init__(self, parent, key):
        assert isinstance(key, PseudowireNeighbor)
        self._neighbor = weakref.ref(key)
        super().__init__(parent=parent)


class EncapsulationType(Enum):
    l2tpv3 = 'l2tpv3'
    mpls = 'mpls'


class EncapsulationProtocol(Enum):
    l2tpv3 = 'l2tpv3'
    ldp = 'ldp'


class TransportMode(Enum):
    ethernet = 'ethernet'
    vlan = 'vlan'
    vlan_passthrough = 'vlan passthrough'


@functools.total_ordering
class PseudowireClass(DeviceFeature):

    name = managedattribute(
        name='name',
        read_only=True)  # read-only hash key

    class DefaultEncapsulationAttributes(object):

        type = managedattribute(
            name='type',
            default=None,
            type=(None, EncapsulationType))

        cookie_size = managedattribute(
            name='cookie_size',
            default=None,
            type=(None, managedattribute.test_istype(int)))

        dfbit_set = managedattribute(
            name='dfbit_set',
            default=None,
            type=(None, managedattribute.test_istype(bool)))

        ipv4_source = managedattribute(
            name='ipv4_source',
            default=None,
            type=(None, IPv4Address))

        pmtu_max = managedattribute(
            name='pmtu_max',
            default=None,
            type=(None, managedattribute.test_istype(int)))

        protocol = managedattribute(
            name='protocol',
            default=None,
            type=(None, EncapsulationProtocol))

        protocol_class = managedattribute(
            name='protocol_class',
            default=None,
            type=(None, managedattribute.test_istype(str)))

        sequencing_direction = managedattribute(
            name='sequencing_direction',
            default=None,
            type=(None, managedattribute.test_istype(str)))

        sequencing_resync = managedattribute(
            name='sequencing_resync',
            default=None,
            type=(None, managedattribute.test_istype(int)))

        tos_reflect = managedattribute(
            name='tos_reflect',
            default=None,
            type=(None, managedattribute.test_istype(bool)))

        tos = managedattribute(
            name='tos',
            default=None,
            type=(None, managedattribute.test_istype(int)))

        transport_mode = managedattribute(
            name='transport_mode',
            default=None,
            type=(None, TransportMode))

        ttl = managedattribute(
            name='ttl',
            default=None,
            type=(None, managedattribute.test_istype(int)))

        control_word = managedattribute(
            name='control_word',
            default=None,
            type=(None, managedattribute.test_istype(bool)))

        tag_rewrite_ingress_vlan = managedattribute(
            name='tag_rewrite_ingress_vlan',
            default=None,
            type=(None, managedattribute.test_istype(int)))

        vccv_verification_type = managedattribute(
            name='vccv_verification_type',
            default=None,
            type=(None, managedattribute.test_istype(str)))

        _pw_class = None

        @property
        def testbed(self):
            return self._pw_class.testbed

        def __init__(self, pw_class):
            self._pw_class = pw_class
            super().__init__()

    encapsulation = managedattribute(
        name='encapsulation',
        read_only=True,
        doc=DefaultEncapsulationAttributes.__doc__)

    @encapsulation.initter
    def encapsulation(self):
        return self.DefaultEncapsulationAttributes(pw_class=self)

    mac_withdraw = managedattribute(
        name='mac_withdraw',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        class EncapsulationAttributes(SubAttributes):

            def __init__(self, _device_attr):
                self._device_attr = _device_attr
                super().__init__(
                        # PseudowireClass.encapsulation
                        parent=_device_attr.parent.encapsulation)

            @property
            def device_name(self):
                return self._device_attr.device_name

            @property
            def device(self):
                return self._device_attr.device

        _encapsulation = None  # EncapsulationAttributes

        @property
        def encapsulation(self):
            return self._encapsulation

        def __init__(self, parent, key):
            super().__init__(parent, key)
            self._encapsulation = self.EncapsulationAttributes(_device_attr=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __init__(self, name, *args, **kwargs):
        assert isinstance(name, str)
        self._name = name
        super().__init__(*args, **kwargs)

    def build_config(self, apply=True,
            devices=None,
            attributes=None,
            *args, **kwargs):
        cfgs = {}
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        if devices is None:
            devices = self.devices

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, apply=True,
            devices=None,
            attributes=None,
            *args, **kwargs):
        cfgs = {}
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        if devices is None:
            devices = self.devices

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

    def __eq__(self, other):
        if not isinstance(other, PseudowireClass):
            return NotImplemented
        return (self.name, self.testbed) \
            == (other.name, other.testbed)

    def __lt__(self, other):
        if not isinstance(other, PseudowireClass):
            return NotImplemented
        return (self.name, self.testbed) \
            < (other.name, other.testbed)

    def __hash__(self):
        return hash(self.name)


class Pseudowire(Base):
    '''A Pseudowire.

    Example:

        # Containers (either Xconnect and/or BridgeDomain)
        xc = Xconnect(...)
        bd = BridgeDomain(...)

        # Create a PseudowireIPv4Neighbor:
        pwnbr1 = xc.create_pseudowire_neighbor(device=dev1, ip=lo2.ipv4.ip, pw_id=123)
        # Create a PseudowireIPv6Neighbor:
        pwnbr1 = xc.create_pseudowire_neighbor(device=dev1, ip=lo2.ipv6.ip, pw_id=123)
        # Create a PseudowireEviNeighbor
        pwnbr1 = xc.create_pseudowire_neighbor(device=dev1, evi=evi2, ac_id=123)
        # pwnbr1.container --> xc
        # pwnbr1.device --> dev1

        # Create a PseudowireIPv4Neighbor:
        pwnbr2 = bd.create_pseudowire_neighbor(device=dev2, ip=lo1.ipv4.ip, pw_id=123)
        # Create a PseudowireEviNeighbor
        pwnbr2 = bd.create_pseudowire_neighbor(device=dev2, evi=evi1, ac_id=123)
        # pwnbr2.container --> bd
        # pwnbr2.device --> dev2

        pw = Pseudowire(neighbors=[pwnbr1, pwnbr2])
        # Implicit:
        #  xc.add_segment(pw)
        #  bd.add_segment(pw)

    '''

    EncapsulationType = EncapsulationType

    EncapsulationProtocol = EncapsulationProtocol

    TransportMode = TransportMode

    neighbors = managedattribute(
        name='neighbors',
        read_only=True,
        gettype=frozenset)

    @property
    def neighbor_devices(self):
        return frozenset(neighbor.device for neighbor in self.neighbors)

    @property
    def testbed(self):
        for nbr in self.neighbors:
            return nbr.testbed

    pw_class = managedattribute(
        name='pw_class',
        default=None,
        type=(None, managedattribute.test_isinstance(PseudowireClass)))

    split_horizon = managedattribute(
        name='split_horizon',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    static_mac_address = managedattribute(
        name='static_mac_address',
        default=None,
        type=(None, MAC))

    ipv6_source = managedattribute(
        name='ipv6_source',
        default=None,
        type=(None, IPv6Address))

    dhcp_ipv4_snooping_profile = managedattribute(
        name='dhcp_ipv4_snooping_profile',
        default=None,
        type=(None,
              managedattribute.test_is(False),  # False
              managedattribute.test_istype(str),  # <profile>
              ))

    igmp_snooping_profile = managedattribute(
        name='igmp_snooping_profile',
        default=None,
        type=(None,
              managedattribute.test_is(False),  # False
              managedattribute.test_istype(str),  # <profile>
              ))

    mld_snooping_profile = managedattribute(
        name='mld_snooping_profile',
        default=None,
        type=(None,
              managedattribute.test_is(False),  # False
              managedattribute.test_istype(str),  # <profile>
              ))

    mpls_static_label = managedattribute(
        name='mpls_static_label',
        default=None,
        type=(None, managedattribute.test_is(int)))

    def __init__(self, neighbors, **kwargs):
        neighbors = set(neighbors)
        if len(neighbors) != 2:
            raise ValueError('Exactly 2 neighbors are expected: %r' % (neighbors,))  # XXXJST TODO
        for nbr in neighbors:
            if not isinstance(nbr, PseudowireNeighbor):
                raise ValueError('%r is not a PseudowireNeighbor' % (nbr,))
        self._neighbors = set(neighbors)
        super().__init__()
        for nbr in self.neighbors:
            nbr.container.add_pseudowire(self)
        for k, v in kwargs.items():
            for nbr in self.neighbors:
                setattr(nbr, k, v)

    def __hash__(self):
        return hash(id(self))  # TODO Always unique

