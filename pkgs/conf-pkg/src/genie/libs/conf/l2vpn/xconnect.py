
__all__ = (
        'Xconnect',
        'XconnectLink',
        )

from enum import Enum
import functools
import weakref

from pyats.datastructures import WeakList

from genie.utils.cisco_collections import typedset

from genie.decorator import managedattribute
import genie.conf.base
from genie.conf.base import DeviceFeature, Interface, Link, Base
from genie.conf.base.link import EmulatedLink, VirtualLink
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, KeyedSubAttributes, InterfaceSubAttributes, SubAttributesDict, AttributesHelper

from genie.libs.conf.base import IPv6Address
from genie.libs.conf.bgp import RouteDistinguisher, RouteTarget

from .pseudowire import Pseudowire, PseudowireClass, \
    PseudowireNeighbor, PseudowireNeighborSubAttributes, \
    EncapsulationType


class XconnectNamespace(Base):

    def __init__(self, xconnect=None):
        assert xconnect
        self._xconnect = xconnect
        super().__init__()

    _xconnect = None

    @property
    def xconnect(self):
        return self._xconnect

    @property
    def testbed(self):
        return self.xconnect.testbed

    @property
    def device(self):
        return self.xconnect.device


class XconnectLink(VirtualLink):

    xconnect = managedattribute(
        name='xconnect',
        read_only=True,
        gettype=managedattribute.auto_unref)

    def connect_interface(self, interface):
        '''Not supported; Use Xconnect.add_segment'''
        raise TypeError('%s objects do not support connect_interface; Please use Xconnect.add_segment')

    def _connect_interface_from_xconnect(self, interface):
        #had_interfaces = any(self.interfaces)
        super().connect_interface(interface)
        #if not had_interfaces:
        #    self.testbed.add_link(self)

    def disconnect_interface(self, interface):
        '''Not supported; Use Xconnect.remove_segment'''
        raise TypeError('%s objects do not support disconnect_interface; Please use Xconnect.remove_segment')

    def _disconnect_interface_from_xconnect(self, interface):
        super().disconnect_interface(interface)
        #if not any(self.interfaces):
        #    self.testbed.remove_link(self)

    def __init__(self, xconnect):
        assert isinstance(xconnect, Xconnect)
        self._xconnect = weakref.ref(xconnect)
        super().__init__(
                testbed=xconnect.testbed,
                name='{g}:{n}'.format(
                    g=xconnect.group_name,
                    n=xconnect.name))


@functools.total_ordering
class Xconnect(DeviceFeature):

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

    class Type(Enum):
        p2p = 1
        mp2mp = 2

    xconnect_type = managedattribute(
        name='xconnect_type',
        default=Type.p2p,
        type=Type)

    shutdown = managedattribute(
        name='shutdown',
        default=None,
        type=(None,bool))

    link = managedattribute(
        name='link',
        read_only=True,
        doc='The XconnectLink instance that represents the connected interfaces')

    redundancy_predictive = managedattribute(
        name='redundancy_predictive',
        default=None,
        type=(None,bool))

    class DeviceAutodiscoveryBgpAttributesDefaults(XconnectNamespace):

        enabled = managedattribute(
            name='enabled',
            default=False,
            type=managedattribute.test_istype(bool))

        control_word = managedattribute(
            name='control_word',
            default=None,
            type=(None, managedattribute.test_istype(bool)))

        rd = managedattribute(
            name='rd',
            default=None,
            type=(None, RouteDistinguisher,
                  managedattribute.test_in((
                      'auto',
                  ))))

        export_route_policy = managedattribute(
            name='export_route_policy',
            default=None,
            type=(None, managedattribute.test_istype(str)))

        export_route_targets = managedattribute(
            name='export_route_targets',
            finit=typedset(RouteTarget.ImportExport).copy,
            type=typedset(RouteTarget.ImportExport)._from_iterable)

        import_route_targets = managedattribute(
            name='import_route_targets',
            finit=typedset(RouteTarget.ImportExport).copy,
            type=typedset(RouteTarget.ImportExport)._from_iterable)

        table_policy = managedattribute(
            name='table_policy',
            default=None,
            type=(None, managedattribute.test_istype(str)))

        class DeviceSignalingProtocolBgpAttributesDefaults(XconnectNamespace):

            enabled = managedattribute(
                name='enabled',
                default=False,
                type=managedattribute.test_istype(bool))

            ce_range = managedattribute(
                name='ce_range',
                default=None,
                type=(None,
                      managedattribute.test_istype(int),
                      managedattribute.test_istype(str)))

        signaling_protocol_bgp = managedattribute(
            name='signaling_protocol_bgp',
            read_only=True,
            doc=DeviceSignalingProtocolBgpAttributesDefaults.__doc__)

        @signaling_protocol_bgp.initter
        def signaling_protocol_bgp(self):
            return self.DeviceSignalingProtocolBgpAttributesDefaults(xconnect=self.xconnect)

        def __init__(self, xconnect):
            super().__init__(xconnect=xconnect)

    autodiscovery_bgp = managedattribute(
        name='autodiscovery_bgp',
        read_only=True,
        doc=DeviceAutodiscoveryBgpAttributesDefaults.__doc__)

    @autodiscovery_bgp.initter
    def autodiscovery_bgp(self):
        return self.DeviceAutodiscoveryBgpAttributesDefaults(xconnect=self)

    description = managedattribute(
        name='description',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # TODO Cannot use typedset because segments need to be updated
    interfaces = managedattribute(
        name='interfaces',
        finit=WeakList,
        type=managedattribute.test_set_of(
            managedattribute.test_isinstance(Interface)),
        gettype=frozenset,
        doc='A `set` of Interface associated objects')

    def add_interface(self, interface):
        prev_segments = self.segments
        self.interfaces |= {interface}
        self._on_segments_updated(prev_segments)

    def remove_interface(self, interface):
        prev_segments = self.segments
        self.interfaces -= {interface}
        self._on_segments_updated(prev_segments)

    class Interworking(Enum):
        ethernet = 'ethernet'
        ipv4 = 'ipv4'

    interface = managedattribute(
        name='interface',
        default=None,
        type=(None, Interworking))

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

    @property
    def segments(self):
        segments = []
        segments += list(self.interfaces)
        segments += list(self.pseudowires)
        return frozenset(segments)

    def add_segment(self, segment):
        if isinstance(segment, Interface):
            self.add_interface(segment)
        elif isinstance(segment, Pseudowire):
            self.add_pseudowire(segment)
        else:
            raise ValueError(segment)

    def remove_segment(self, segment):
        if isinstance(segment, Interface):
            self.remove_interface(segment)
        elif isinstance(segment, Pseudowire):
            self.remove_pseudowire(segment)
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
            self.link._disconnect_interface_from_xconnect(link_interface)
        for link_interface in new_link_interfaces - prev_link_interfaces:
            self.link._connect_interface_from_xconnect(link_interface)

    def link_interfaces_from_segment(self, segment):
        link_interfaces = set()
        if isinstance(segment, Interface):
            # Links under Genie Interface object is deprecated
            # Placed the below workaround to bypass the Unittest
            from pyats.datastructures import WeakList
            segment_links = set(WeakList()) - set([self])
            # Priority to L2 virtual links...
            if not link_interfaces:
                for link in segment_links:
                    if isinstance(link, (XconnectLink, XconnectLink)):
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
            # For VLAN TGEN connections, the CE interface is the peer of the AC interface's parent
            if not link_interfaces:
                parent_interface = segment.parent_interface
                if parent_interface:
                    # recurse
                    link_interfaces = self.link_interfaces_from_segment(parent_interface)
        elif isinstance(segment, Pseudowire):
            pass
        else:
            raise ValueError(segment)
        return link_interfaces

    def create_pseudowire_neighbor(self, device, **kwargs):
        return self.device_attr[device].create_pseudowire_neighbor(**kwargs)

    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        class NeighborAttributes(PseudowireNeighborSubAttributes):

            # ip -> self.neighbor.ip
            # pw_id -> self.neighbor.pw_id

            ipv6_source = managedattribute(
                name='ipv6_source',
                default=None,
                type=(None, IPv6Address))

            mpls_static_label = managedattribute(
                name='mpls_static_label',
                default=None,
                type=(None, managedattribute.test_istype(int)))

            pw_class = managedattribute(
                name='pw_class',
                default=None,
                type=(None, managedattribute.test_isinstance(PseudowireClass)))

            redundancy_group = managedattribute(
                name='redundancy_group',
                type=(None,str))

            redundancy_priority = managedattribute(
                name='redundancy_priority',
                type=(None,int))

            encapsulation = managedattribute(
                name='encapsulation',
                default=EncapsulationType.mpls,
                type=(None, EncapsulationType))

        neighbor_attr = managedattribute(
            name='neighbor_attr',
            read_only=True,
            doc=NeighborAttributes.__doc__)

        @neighbor_attr.initter
        def neighbor_attr(self):
            return SubAttributesDict(self.NeighborAttributes, parent=self)

        # interfaces -- See DeviceSubAttributes

        class AutodiscoveryBgpAttributes(SubAttributes):

            export_route_targets = managedattribute(
                name='export_route_targets',
                type=typedset(RouteTarget.ImportExport)._from_iterable)

            @export_route_targets.defaulter
            def export_route_targets(self):
                return frozenset(self.parent.export_route_targets)

            import_route_targets = managedattribute(
                name='import_route_targets',
                type=typedset(RouteTarget.ImportExport)._from_iterable)

            @import_route_targets.defaulter
            def import_route_targets(self):
                return frozenset(self.parent.import_route_targets)

            @property
            def device_name(self):
                return self._device_attr.device_name

            @property
            def device(self):
                return self._device_attr.device

            class SignalingProtocolBgpAttributes(SubAttributes):

                ce_ids = managedattribute(
                    name='ce_ids',
                    finit=typedset(int).copy,
                    type=typedset(int)._from_iterable)

                def add_ce_id(self, ce_id):  # TODO DEPRECATE
                    self.ce_ids.add(ce_id)

                def remove_ce_id(self, ce_id):  # TODO DEPRECATE
                    self.ce_ids.remove(ce_id)

                @property
                def device_name(self):
                    return self._device_attr.device_name

                @property
                def device(self):
                    return self._device_attr.device

                class CeAttributes(KeyedSubAttributes):

                    @classmethod
                    def _sanitize_key(cls, key):
                        return int(key)

                    ce_id = managedattribute(
                        name='ce_id',
                        read_only=True)  # read-only key

                    interfaces = managedattribute(
                        name='interfaces',
                        finit=typedset(managedattribute.test_isinstance(Interface)).copy,
                        type=typedset(managedattribute.test_isinstance(Interface))._from_iterable)

                    def add_interface(self, intf):  # TODO DEPRECATE
                        self.interfaces.add(intf)

                    def remove_interface(self, intf):  # TODO DEPRECATE
                        self.interfaces.remove(intf)

                    class InterfaceAttributes(InterfaceSubAttributes):

                        remote_ce_id = None
                        #Always only one per interface
                        #    interface GigabitEthernet0/0/1/0 remote-ce-id 2000
                        #    !!% Invalid argument: AC already used by existing xconnect

                    interface_attr = None  # InterfaceAttributes

                    def __init__(self, parent, key):
                        self._ce_id = key
                        super().__init__(parent=parent)
                        self.interface_attr = SubAttributesDict(self.InterfaceAttributes, parent=self)

                ce_attr = managedattribute(
                    name='ce_attr',
                    read_only=True,
                    doc=CeAttributes.__doc__)
                
                @ce_attr.initter
                def ce_attr(self):
                    return SubAttributesDict(self.CeAttributes, parent=self)

                def __init__(self, device_attr):
                    self._device_attr = device_attr
                    super().__init__(parent=device_attr.parent.autodiscovery_bgp.signaling_protocol_bgp)

            signaling_protocol_bgp = managedattribute(
                name='signaling_protocol_bgp',
                read_only=True,
                doc=SignalingProtocolBgpAttributes.__doc__)

            @signaling_protocol_bgp.initter
            def signaling_protocol_bgp(self):
                return self.SignalingProtocolBgpAttributes(device_attr=self._device_attr)

            def __init__(self, device_attr):
                self._device_attr = device_attr
                super().__init__(parent=device_attr.parent.autodiscovery_bgp)

        autodiscovery_bgp = managedattribute(
            name='autodiscovery_bgp',
            read_only=True,
            doc=AutodiscoveryBgpAttributes.__doc__)

        @autodiscovery_bgp.initter
        def autodiscovery_bgp(self):
            return self.AutodiscoveryBgpAttributes(device_attr=self)

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

        def create_pseudowire_neighbor(self, **kwargs):
            pwnbr = PseudowireNeighbor(container=self.parent,
                                       device=self.device,
                                       **kwargs)
            return pwnbr

        @property
        def segments(self):
            segments = []
            segments += list(self.interfaces)
            segments += list(self.pseudowires)
            return frozenset(segments)

        def __init__(self, parent, key, **kwargs):
            super().__init__(parent=parent, key=key, **kwargs)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)
    
    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __eq__(self, other):
        if not isinstance(other, Xconnect):
            return NotImplemented
        # return (self.group_name, self.name, self.testbed) \
        #     == (other.group_name, other.name, other.testbed)
        return (self.name, self.group_name, self.testbed) \
            == (other.name, other.group_name, other.testbed)

    def __lt__(self, other):
        if not isinstance(other, Xconnect):
            return NotImplemented
        return (self.group_name, self.name, self.testbed) \
            < (other.group_name, other.name, self.testbed)

    def __hash__(self):
        # return hash((self.group_name, self.name))
        return hash(self.name)

    def __init__(self, name, *args, **kwargs):
        self._name = name
        segments = kwargs.pop('segments', ())
        super().__init__(*args, **kwargs)
        self._link = XconnectLink(xconnect=self)
        # TODO support self.segments = segments
        for segment in set(segments):
            self.add_segment(segment)

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

