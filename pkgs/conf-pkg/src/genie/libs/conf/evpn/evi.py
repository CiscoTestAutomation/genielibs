
__all__ = (
    'Evi',
    'EviNeighbor',
)

import functools
import weakref

from genie.utils.cisco_collections import typedset

from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, KeyedSubAttributes, AttributesHelper

from genie.libs.conf.base import Neighbor
from genie.libs.conf.base import RouteDistinguisher, RouteTarget
#from .evpn import Evpn


@functools.total_ordering
class EviNeighbor(Neighbor):
    '''An EVI Neighbor class.'''

    evi = managedattribute(
        name='evi',
        read_only=True,
        doc='Evi: The EVI neighbor (read-only hash key)')

    ac_id = managedattribute(
        name='ac_id',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    def __init__(self, evi, **kwargs):
        '''
        Args:
            evi (Evi): The EVI Neighbor.
        '''
        if not isinstance(evi, Evi):
            raise TypeError(evi)
        self._evi = evi
        super().__init__(**kwargs)

    def _neighbor_comparison_tokens(self):
        return super()._neighbor_comparison_tokens() + (
            'evi', self.evi,
            'ac_id', self.ac_id,
        )

    def __hash__(self):
        return hash((self.evi, self.ac_id))

    def __repr__(self):
        s = '<{}'.format(
            self.__class__.__name__,
        )
        s += ' EVI {} AC {}'.format(
            self.evi.evi_id,
            self.ac_id,
        )
        s += '>'


class EviSubAttributes(KeyedSubAttributes):
    '''SubAttributes class keyed by EVI ID.'''

    evi_id = managedattribute(
        name='evi_id',
        read_only=True,
        doc='''int: EVI ID read-only key''')

    @property
    def evi(self):
        '''Evi: The Evi object associated with the EVI ID.'''
        evi_id = self.evi_id
        for evi in self.parent.evis:
            if evi.evi_id == evi_id:
                return evi
        raise AttributeError('evi: no Evi found matching evi_id=%r' % (evi_id,))

    @classmethod
    def _sanitize_key(cls, key):
        if isinstance(key, Evi):
            return key.evi_id
        if isinstance(key, (str, int)):
            return int(key)
        return key

    def __init__(self, parent, key):
        '''
        Args:
            parent: Parent object to inherit attributes from.
            key (int): EVI ID key.
        '''
        self._evi_id = int(key)
        super().__init__(parent=parent)


@functools.total_ordering
class Evi(ConfigurableBase):

    evi_id = managedattribute(
        name='evi_id',
        read_only=True,
        doc='int: EVI ID (read-only hash key)')

    evi_mode = managedattribute(
        name='evi_mode',
        default='vlan-based',
        type=(None,str))

    device = managedattribute(
        name='device',
        read_only=True,
        gettype=managedattribute.auto_unref)

    @property
    def testbed(self):
        return self.device.testbed

    @property
    def evpn(self):
        return self.device.evpn

    advertise_mac = managedattribute(
        name='advertise_mac',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    control_word_disable = managedattribute(
        name='control_word_disable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    class BgpAttributes(SubAttributes):

        enabled = managedattribute(
            name='enabled',
            default=False,
            type=managedattribute.test_istype(bool))

        rd = managedattribute(
            name='rd',
            default=None,
            type=(None, RouteDistinguisher))

        export_route_targets = managedattribute(
            name='export_route_targets',
            finit=typedset(RouteTarget.ImportExport).copy,
            type=typedset(RouteTarget.ImportExport)._from_iterable)

        export_route_target_none = managedattribute(
            name='export_route_target_none',
            default=None,
            type=(None, managedattribute.test_istype(bool)))

        import_route_targets = managedattribute(
            name='import_route_targets',
            finit=typedset(RouteTarget.ImportExport).copy,
            type=typedset(RouteTarget.ImportExport)._from_iterable)

        import_route_target_none = managedattribute(
            name='import_route_target_none',
            default=None,
            type=(None, managedattribute.test_istype(bool)))

    bgp = managedattribute(
        name='bgp',
        read_only=True,
        doc=BgpAttributes.__doc__)

    @bgp.initter
    def bgp(self):
        return self.BgpAttributes(parent=self)

    class LoadBalancingAttributes(SubAttributes):

        def __init__(self, _evi):
            self._evi = _evi
            super().__init__(
                    # Evpn.device_attr[].load_balancing
                    parent=None)

        @property
        def parent(self):
            return self._evi.evpn.device_attr[self.device].load_balancing

        @property
        def testbed(self):
            return self._evi.testbed

        @property
        def device_name(self):
            return self._evi.device_name

        @property
        def device(self):
            return self._evi.device

    load_balancing = managedattribute(
        name='load_balancing',
        read_only=True,
        doc=LoadBalancingAttributes.__doc__)

    @load_balancing.initter
    def load_balancing(self):
        return self.LoadBalancingAttributes(_evi=self)

    def __eq__(self, other):
        if not isinstance(other, Evi):
            return NotImplemented
        # return (self.device, self.evi_id) == (other.device, other.evi_id)
        return (self.evi_id, self.device) == (other.evi_id, other.device)

    def __lt__(self, other):
        if not isinstance(other, Evi):
            return NotImplemented
        return (self.device, self.evi_id) < (other.device, other.evi_id)

    def __hash__(self):
        return hash(self.evi_id)

    def __init__(self, device, evi_id, *args, **kwargs):
        self._evi_id = evi_id
        assert getattr(device, 'evpn', None)
        self._device = weakref.ref(device)
        self.evpn.add_evi(self)
        super().__init__(*args, **kwargs)

    def remove(self):
        try:
            self.evpn.remove_evi(self)
        except:
            pass
        self._device = None

    def __repr__(self):
        return '<%s object %r on %r at 0x%x>' % (
            self.__class__.__name__,
            self.evi_id,
            self.device.name,
            id(self))

