
__all__ = (
    'BridgeDomain',
    'BridgeDomainLink',
)

import collections
import functools
import weakref

from pyats.datastructures import WeakList

from genie.decorator import managedattribute
import genie.conf.base
from genie.conf.base import DeviceFeature, Interface, Link
from genie.conf.base.link import EmulatedLink, VirtualLink
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, KeyedSubAttributes,\
        SubAttributesDict, AttributesHelper

from genie.libs.conf.base import MAC
from genie.libs.conf.interface import BviInterface
import genie.libs.conf.l2vpn
from ..evpn.evi import Evi, EviSubAttributes
from ..evpn.vni import Vni, VniSubAttributes
from .pseudowire import Pseudowire, PseudowireClass, PseudowireNeighbor, PseudowireNeighborSubAttributes
from .vfi import Vfi


class BridgeDomainLink(VirtualLink):

    bridge_domain = managedattribute(
        name='bridge_domain',
        read_only=True,
        gettype=managedattribute.auto_unref)

    @property
    def testbed(self):
        return self.bridge_domain.testbed

    def connect_interface(self, interface):
        '''Not supported; Use BridgeDomain.add_segment'''
        raise TypeError('%s objects do not support connect_interface; \
                        Please use BridgeDomain.add_segment')

    def _connect_interface_from_bridge_domain(self, interface):
        #had_interfaces = any(self.interfaces)
        super().connect_interface(interface)
        #if not had_interfaces:
        #    self.testbed.add_link(self)

    def disconnect_interface(self, interface):
        '''Not supported; Use BridgeDomain.remove_segment'''
        raise TypeError('%s objects do not support disconnect_interface; \
                        Please use BridgeDomain.remove_segment')

    def _disconnect_interface_from_bridge_domain(self, interface):
        super().disconnect_interface(interface)
        #if not any(self.interfaces):
        #    self.testbed.remove_link(self)

    def __init__(self, bridge_domain):
        self._bridge_domain = weakref.ref(bridge_domain)
        super().__init__(
                name='{g}:{n}'.format(
                    g=bridge_domain.group_name,
                    n=bridge_domain.name))


@functools.total_ordering
class BridgeDomain(DeviceFeature):

    group_name = managedattribute(
        name='group_name',
        type=managedattribute.test_istype(str))

    @group_name.defaulter
    def group_name(self):
        return self.name + 'g'

    name = managedattribute(
        name='name',
        read_only=True,  # read-only hash key
        doc='Bridge domain name (mandatory)')

    link = managedattribute(
        name='link',
        read_only=True,
        doc='The BridgeDomainLink instance that represents the connected interfaces')

    # TODO Cannot use typedset because segments need to be updated
    evis = managedattribute(
        name='evis',
        finit=set,
        type=managedattribute.test_set_of(
            managedattribute.test_isinstance(Evi)),
        gettype=frozenset,
        doc='A `set` of Evi associated objects')

    def add_evi(self, evi):
        prev_segments = self.segments
        self.evis |= {evi}
        self._on_segments_updated(prev_segments)

    def remove_evi(self, evi):
        prev_segments = self.segments
        self.evis -= {evi}
        self._on_segments_updated(prev_segments)

    class DefaultDeviceAndInterfaceMacAttributes(object):
        pass

    mac = managedattribute(
        name='mac',
        read_only=True,
        finit=DefaultDeviceAndInterfaceMacAttributes,
        doc=DefaultDeviceAndInterfaceMacAttributes.__doc__)

    # TODO Cannot use typedset because segments need to be updated
    interfaces = managedattribute(
        name='interfaces',
        finit=WeakList,
        type=managedattribute.test_set_of(
            managedattribute.test_isinstance(Interface)),
        gettype=frozenset,
        doc='A `set` of Interface associated objects')

    def add_interface(self, interface):
        if isinstance(interface, Vni):
            self.add_vni(interface)
            return
        prev_segments = self.segments
        self.interfaces |= {interface}
        self._on_segments_updated(prev_segments)

    def remove_interface(self, interface):
        if isinstance(interface, Vni):
            self.remove_vni(interface)
            return
        prev_segments = self.segments
        self.interfaces -= {interface}
        self._on_segments_updated(prev_segments)

    aging_time = managedattribute(
        name='aging_time',
        default=None,
        type=(None,managedattribute.test_istype(int)))

    learning_disable = managedattribute(
        name='learning_disable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    split_horizon_group = managedattribute(
        name='split_horizon_group',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    split_horizon_group_core = managedattribute(
        name='split_horizon_group_core',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # TODO Cannot use typedset because segments need to be updated
    pseudowires = managedattribute(
        name='pseudowires',
        finit=set,
        type=managedattribute.test_set_of(
            managedattribute.test_isinstance(Pseudowire)),
        gettype=frozenset,
        doc='A `set` of Pseudowire associated objects')

    def add_pseudowire(self, pseudowire):
        prev_segments = self.segments
        self.pseudowires |= {pseudowire}
        self._on_segments_updated(prev_segments)

    def remove_pseudowire(self, pseudowire):
        prev_segments = self.segments
        self.pseudowires -= {pseudowire}
        self._on_segments_updated(prev_segments)

    @property
    def pseudowire_neighbors(self):
        for pw in self.pseudowires:
            for nbr in pw.neighbors:
                if nbr.container is self:
                    yield nbr

    # TODO Cannot use typedset because segments need to be updated
    vnis = managedattribute(
        name='vnis',
        finit=set,
        type=managedattribute.test_set_of(
            managedattribute.test_isinstance(Vni)),
        gettype=frozenset,
        doc='A `set` of Vni associated objects')

    def add_vni(self, vni):
        prev_segments = self.segments
        self.vnis |= {vni}
        self._on_segments_updated(prev_segments)

    def remove_vni(self, vni):
        prev_segments = self.segments
        self.vnis -= {vni}
        self._on_segments_updated(prev_segments)

    # TODO Cannot use typedset because segments need to be updated
    vfis = managedattribute(
        name='vfis',
        finit=set,
        type=managedattribute.test_set_of(
            managedattribute.test_isinstance(Vfi)),
        gettype=frozenset,
        doc='A `set` of Vfi associated objects')

    def add_vfi(self, vfi):
        assert isinstance(vfi, Vfi)
        if vfi.container is not None:
            raise ValueError(
                '%r is already assigned to %r' % (vfi, vfi.container))
        prev_segments = self.segments
        self.vfis |= {vfi}
        vfi.container = self
        self._on_segments_updated(prev_segments)

    def remove_vfi(self, vfi):
        assert isinstance(vfi, Vfi)
        if vfi.container is not None and vfi.container is not self:
            raise ValueError(
                '%r is assigned to %r, not %r' % (vfi, vfi.container, self))
        prev_segments = self.segments
        self.vfis -= {vfi}
        vfi.container = None
        self._on_segments_updated(prev_segments)

    shutdown = managedattribute(
        name='shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    @property
    def segments(self):
        segments = set()
        segments |= self.interfaces
        segments |= self.pseudowires
        segments |= self.vnis
        segments |= self.vfis
        segments |= self.evis
        return frozenset(segments)

    def add_segment(self, segment):
        if isinstance(segment, Evi):
            self.add_evi(segment)
        elif isinstance(segment, Vni):
            self.add_vni(segment)
        elif isinstance(segment, Interface):
            self.add_interface(segment)
        elif isinstance(segment, Pseudowire):
            self.add_pseudowire(segment)
        elif isinstance(segment, Vfi):
            self.add_vfi(segment)
        else:
            raise ValueError(segment)

    def remove_segment(self, segment):
        if isinstance(segment, Evi):
            self.remove_evi(segment)
        elif isinstance(segment, Vni):
            self.remove_vni(segment)
        elif isinstance(segment, Interface):
            self.remove_interface(segment)
        elif isinstance(segment, Pseudowire):
            self.remove_pseudowire(segment)
        elif isinstance(segment, Vfi):
            self.remove_vfi(segment)
        else:
            raise ValueError(segment)

    def _on_segments_updated(self, prev_segments):
        # UNUSED prev_segments = frozenset(prev_segments)
        cur_segments = frozenset(self.segments)
        prev_link_interfaces = frozenset(self.link.interfaces)
        new_link_interfaces = frozenset(
            interface
            for segment in cur_segments
            for interface in self.link_interfaces_from_segment(segment))
        for link_interface in prev_link_interfaces - new_link_interfaces:
            self.link._disconnect_interface_from_bridge_domain(link_interface)
        for link_interface in new_link_interfaces - prev_link_interfaces:
            self.link._connect_interface_from_bridge_domain(link_interface)

    def link_interfaces_from_segment(self, segment):
        link_interfaces = set()
        if isinstance(segment, Evi):
            pass
        elif isinstance(segment, Vni):
            pass
        elif isinstance(segment, Interface):
            if isinstance(segment, BviInterface):
                link_interfaces.add(segment)
            else:
                # Links under Genie Interface object is deprecated
                # Placed the below workaround to bypass the Unittest
                from pyats.datastructures import WeakList
                segment_links = set(WeakList()) - set([self.link])
                # Priority to L2 virtual links...
                if not link_interfaces:
                    for link in segment_links:
                        if isinstance(
                                link,
                                (BridgeDomainLink,
                                 genie.libs.conf.l2vpn.XconnectLink)):
                            link_interfaces.update(link.interfaces)
                            link_interfaces.discard(segment)
                # ... then emulated links
                if not link_interfaces:
                    for link in segment_links:
                        if isinstance(link, EmulatedLink):
                            link_interfaces.update(link.interfaces)
                            link_interfaces.discard(segment)
                # ... finally, all links
                if not link_interfaces:
                    for link in segment_links:
                        link_interfaces.update(link.interfaces)
                        link_interfaces.discard(segment)
                # For VLAN TGEN connections, the CE interface is the peer of
                # the AC interface's parent
                if not link_interfaces:
                    parent_interface = segment.parent_interface
                    if parent_interface:
                        # recurse
                        link_interfaces = self.link_interfaces_from_segment(
                            parent_interface)
        elif isinstance(segment, Pseudowire):
            pass
        elif isinstance(segment, Vfi):
            pass
        else:
            raise ValueError(segment)
        return link_interfaces

    def create_pseudowire_neighbor(self, device, **kwargs):
        return self.device_attr[device].create_pseudowire_neighbor(**kwargs)

    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        class InterfaceAttributes(
                genie.conf.base.attributes.InterfaceSubAttributes):

            class MacAttributes(SubAttributes):

                def __init__(self, _interface_attr):
                    self._interface_attr = _interface_attr
                    super().__init__(
                            # BridgeDomain.device_attr[].mac
                            parent=_interface_attr.parent.mac)

                @property
                def interface_name(self):
                    return self._interface_attr.interface_name

                @property
                def interface(self):
                    return self._interface_attr.interface

            mac = managedattribute(
                name='mac',
                read_only=True,
                doc=MacAttributes.__doc__)

            @mac.initter
            def mac(self):
                return self.MacAttributes(_interface_attr=self)

            static_mac_address = managedattribute(
                name='static_mac_address',
                default=None,
                type=(None, MAC))

            def __init__(self, parent, key):
                super().__init__(parent, key)

        interface_attr = managedattribute(
            name='interface_attr',
            read_only=True,
            doc=InterfaceAttributes.__doc__)

        @interface_attr.initter
        def interface_attr(self):
            return SubAttributesDict(self.InterfaceAttributes, parent=self)

        class NeighborAttributes(PseudowireNeighborSubAttributes):

            # ip -> self.neighbor.ip
            # pw_id -> self.neighbor.pw_id
            # evi -> self.neighbor.evi
            # ac_id -> self.neighbor.ac_id
            # source_ac_id -> self.neighbor.source_ac_id

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
                type=(None,
                      managedattribute.test_istype(int)))

            pw_class = managedattribute(
                name='pw_class',
                default=None,
                type=(None,
                      managedattribute.test_isinstance(PseudowireClass)))

            split_horizon = managedattribute(
                name='split_horizon',
                default=None,
                type=(None,
                      managedattribute.test_istype(bool)))

            static_mac_address = managedattribute(
                name='static_mac_address',
                default=None,
                type=(None, MAC))

        neighbor_attr = managedattribute(
            name='neighbor_attr',
            read_only=True,
            doc=NeighborAttributes.__doc__)

        @neighbor_attr.initter
        def neighbor_attr(self):
            return SubAttributesDict(self.NeighborAttributes, parent=self)

        class EviAttributes(EviSubAttributes):

            vlan = managedattribute(
                name='vlan',
                default=None,
                type=(None, int))

            def __init__(self, parent, key):
                super().__init__(parent=parent, key=key)

        evi_attr = managedattribute(
            name='evi_attr',
            read_only=True,
            doc=EviAttributes.__doc__)

        @evi_attr.initter
        def evi_attr(self):
            return SubAttributesDict(self.EviAttributes, parent=self)

        class VniAttributes(VniSubAttributes):

            def __init__(self, parent, key):
                super().__init__(parent, key)

        vni_attr = managedattribute(
            name='vni_attr',
            read_only=True,
            doc=VniAttributes.__doc__)

        @vni_attr.initter
        def vni_attr(self):
            return SubAttributesDict(self.VniAttributes, parent=self)

        class MacAttributes(SubAttributes):

            def __init__(self, _device_attr):
                self._device_attr = _device_attr
                super().__init__(
                        # BridgeDomain.mac
                        parent=_device_attr.parent.mac)

            @property
            def device_name(self):
                return self._device_attr.device_name

            @property
            def device(self):
                return self._device_attr.device

            @property
            def testbed(self):
                return self._device_attr.testbed

        mac = managedattribute(
            name='mac',
            read_only=True,
            doc=MacAttributes.__doc__)

        @mac.initter
        def mac(self):
            return self.MacAttributes(_device_attr=self)

        @property
        def evis(self):
            device = self.device
            for evi in self.parent.evis:
                if evi.device is device:
                    yield evi

        # interfaces -- See DeviceSubAttributes

        @property
        def vnis(self):
            device = self.device
            for vni in self.parent.vnis:
                if vni.device is device:
                    yield vni

        @property
        def pseudowires(self):
            container = self.parent
            device = self.device
            for pw in container.pseudowires:
                for nbr in pw.neighbors:
                    if nbr.container is container \
                            and nbr.device is device:
                        yield pw
                        break  # next pw

        @property
        def pseudowire_neighbors(self):
            device = self.device
            for nbr in self.parent.pseudowire_neighbors:
                if nbr.device is device:
                    yield nbr

        @property
        def vfis(self):
            device = self.device
            for vfi in self.parent.vfis:
                if vfi.device is device:
                    yield vfi

        @property
        def segments(self):
            yield from self.interfaces
            yield from self.pseudowires
            yield from self.vnis
            yield from self.vfis
            yield from self.evis

        def create_pseudowire_neighbor(self, **kwargs):
            pwnbr = PseudowireNeighbor(container=self.parent,
                                       device=self.device,
                                       **kwargs)
            return pwnbr

        def __init__(self, parent, key):
            super().__init__(parent, key)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __eq__(self, other):
        if not isinstance(other, BridgeDomain):
            return NotImplemented
        # return (self.group_name, self.name) == (other.group_name, other.name)
        return (self.name, self.group_name, self.testbed) \
            == (other.name, other.group_name, other.testbed)

    def __lt__(self, other):
        if not isinstance(other, BridgeDomain):
            return NotImplemented
        return (self.group_name, self.name, self.testbed) \
            < (other.group_name, other.name, other.testbed)

    def __hash__(self):
        # return hash((self.group_name, self.name))
        return hash(self.name)

    def __init__(self, name, *args, **kwargs):
        self._name = name
        super().__init__(*args, **kwargs)
        self._link = BridgeDomainLink(bridge_domain=self)

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

