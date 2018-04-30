
__all__ = (
        'Vfi',
        )

import functools
import weakref

from genie.utils.cisco_collections import typedset

from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase, Device
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, SubAttributesDict, AttributesInheriter

from genie.libs.conf.base import MAC
from genie.libs.conf.bgp import RouteDistinguisher, RouteTarget

from .pseudowire import Pseudowire, PseudowireClass, PseudowireNeighbor, PseudowireNeighborSubAttributes


class ConfigurableVfiNamespace(ConfigurableBase):

    def __init__(self, vfi=None):
        assert vfi
        self._vfi = vfi

    _vfi = None

    @property
    def vfi(self):
        return self._vfi

    @property
    def testbed(self):
        return self.vfi.testbed

    @property
    def device(self):
        return self.vfi.device


@functools.total_ordering
class Vfi(ConfigurableBase):

    container = None  # BridgeDomain

    device = managedattribute(
        name='device',
        read_only=True,
        gettype=managedattribute.auto_unref)

    name = managedattribute(
        name='name',
        read_only=True)  # read-only hash key

    virtual = managedattribute(
        name='virtual',
        default=False,
        type=(None, managedattribute.test_istype(bool)))

    shutdown = managedattribute(
        name='shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    vpn_id = managedattribute(
        name='vpn_id',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    class AutodiscoveryBgpAttributes(ConfigurableVfiNamespace):

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

        class SignalingProtocolBgpAttributes(ConfigurableVfiNamespace):

            enabled = managedattribute(
                name='enabled',
                default=False,
                type=managedattribute.test_istype(bool))

            ve_id = managedattribute(
                name='ve_id',
                default=None,
                type=(None, managedattribute.test_istype(int)))

            ve_range = managedattribute(
                name='ve_range',
                default=None,
                type=(None,
                      managedattribute.test_istype(int),
                      managedattribute.test_istype(str)))

        signaling_protocol_bgp = managedattribute(
            name='signaling_protocol_bgp',
            read_only=True,
            doc=SignalingProtocolBgpAttributes.__doc__)

        @signaling_protocol_bgp.initter
        def signaling_protocol_bgp(self):
            return self.SignalingProtocolBgpAttributes(vfi=self.vfi)

        class SignalingProtocolLdpAttributes(ConfigurableVfiNamespace):

            enabled = managedattribute(
                name='enabled',
                default=False,
                type=managedattribute.test_istype(bool))

            vpls_id = managedattribute(
                name='vpls_id',
                default=None,
                type=(None, RouteTarget))

        signaling_protocol_ldp = managedattribute(
            name='signaling_protocol_ldp',
            read_only=True,
            doc=SignalingProtocolLdpAttributes.__doc__)

        @signaling_protocol_ldp.initter
        def signaling_protocol_ldp(self):
            return self.SignalingProtocolLdpAttributes(vfi=self.vfi)

        def __init__(self, vfi):
            super().__init__(vfi=vfi)

    autodiscovery_bgp = managedattribute(
        name='autodiscovery_bgp',
        read_only=True,
        doc=AutodiscoveryBgpAttributes.__doc__)

    @autodiscovery_bgp.initter
    def autodiscovery_bgp(self):
        return self.AutodiscoveryBgpAttributes(vfi=self)

    class MulticastP2mpAttributes(ConfigurableVfiNamespace):

        class SignalingProtocolBgpAttributes(ConfigurableVfiNamespace):

            enabled = managedattribute(
                name='enabled',
                default=False,
                type=managedattribute.test_istype(bool))

        signaling_protocol_bgp = managedattribute(
            name='signaling_protocol_bgp',
            read_only=True,
            doc=SignalingProtocolBgpAttributes.__doc__)

        @signaling_protocol_bgp.initter
        def signaling_protocol_bgp(self):
            return self.SignalingProtocolBgpAttributes(vfi=self.vfi)

        class TransportRsvpTeAttributes(ConfigurableVfiNamespace):

            enabled = managedattribute(
                name='enabled',
                default=False,
                type=managedattribute.test_istype(bool))

            attribute_set_p2mp_te = managedattribute(
                name='attribute_set_p2mp_te',
                default=None,
                type=(None, managedattribute.test_istype(str)))

        transport_rsvp_te = managedattribute(
            name='transport_rsvp_te',
            read_only=True,
            doc=TransportRsvpTeAttributes.__doc__)

        @transport_rsvp_te.initter
        def transport_rsvp_te(self):
            return self.TransportRsvpTeAttributes(vfi=self.vfi)

        def __init__(self, vfi):
            super().__init__(vfi=vfi)

    multicast_p2mp = managedattribute(
        name='multicast_p2mp',
        read_only=True,
        doc=MulticastP2mpAttributes.__doc__)

    @multicast_p2mp.initter
    def multicast_p2mp(self):
        return self.MulticastP2mpAttributes(vfi=self)

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
                    # implied: nbr.device is self.device
                    yield nbr

    def create_pseudowire_neighbor(self, **kwargs):
        pwnbr = PseudowireNeighbor(container=self,
                                   device=self.device,
                                   **kwargs)
        return pwnbr

    @property
    def segments(self):
        segments = []
        segments += list(self.pseudowires)
        return frozenset(segments)

    def add_segment(self, segment):
        if isinstance(segment, Pseudowire):
            self.add_pseudowire(segment)
        else:
            raise ValueError(segment)

    def remove_segment(self, segment):
        if isinstance(segment, Pseudowire):
            self.remove_pseudowire(segment)
        else:
            raise ValueError(segment)

    def _on_segments_updated(self, prev_segments):
        pass  # TODO

    class NeighborAttributes(PseudowireNeighborSubAttributes):

        # ip -> self.neighbor.ip
        # pw_id -> self.neighbor.pw_id

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

    def __init__(self, name, device, bridge_domain=None, *args, **kwargs):
        assert isinstance(name, str)
        self._name = name
        assert isinstance(device, Device)
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)
        if bridge_domain is not None:
            bridge_domain.add_vfi(self)

    def __eq__(self, other):
        if not isinstance(other, Vfi):
            return NotImplemented
        # return (self.device, self.name,
        #         self.container.__class__.__name__, self.container) \
        #     == (other.device, other.name,
        #         other.container.__class__.__name__, other.container)
        return (self.name, self.device,
                self.container.__class__.__name__, self.container) \
            == (other.name, other.device,
                other.container.__class__.__name__, other.container)

    def __lt__(self, other):
        if not isinstance(other, Vfi):
            return NotImplemented
        return (self.device, self.name,
                self.container.__class__.__name__, self.container) \
            < (other.device, other.name,
                other.container.__class__.__name__, other.container)

    def __hash__(self):
        # return hash((self.device, self.container, self.name))
        # return hash((self.name, self.device, self.container))
        return hash(self.name)

