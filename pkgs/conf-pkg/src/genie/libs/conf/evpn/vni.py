
__all__ = (
        'Vni',
        )

import functools
import weakref

from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase
from genie.conf.base.attributes import KeyedSubAttributes

from genie.libs.conf.vrf import Vrf
from genie.libs.conf.base import IPv4Address
from genie.libs.conf.interface import NveInterface


class VniSubAttributes(KeyedSubAttributes):

    vni_id = managedattribute(
        name='vni_id',
        read_only=True)  # Key

    @property
    def vni(self):
        for vni in self.parent.vnis:
            if vni.vni_id == VniSubAttributes.vni_id:
                return vni
        raise AttributeError('vni: no Vni found matching vni_id=%r' % (VniSubAttributes.vni_id,))

    @classmethod
    def _sanitize_key(cls, key):
        if isinstance(key, Vni):
            return key.vni_id
        if isinstance(key, (str, int)):
            return int(key)
        return key

    def __init__(self, parent, key):
        self._vni_id = int(key)
        super().__init__(parent=parent)


@functools.total_ordering
class Vni(ConfigurableBase):

    vni_id = managedattribute(
        name='vni_id',
        read_only=True,  # read-only hash key
        doc='VNI ID (mandatory)')

    device = managedattribute(
        name='device',
        read_only=True,
        gettype=managedattribute.auto_unref)

    @property
    def testbed(self):
        return self.device.testbed

    nve = managedattribute(
        name='nve',
        default=None,
        gettype=managedattribute.auto_unref)

    @nve.deleter
    def nve(self):
        old_nve = self.nve
        del self._nve  # may raise AttributeError
        if old_nve is not None:
            if self in old_nve.vnis:
                old_nve.remove_vni(self)

    @nve.setter
    def nve(self, nve):
        if nve is not None and not isinstance(nve, NveInterface):
            raise ValueError(nve)
        old_nve = self.nve
        if old_nve is not None:
            if self in old_nve.vnis:
                old_nve.remove_vni(self)
        self._nve = None
        if nve is not None:
            if nve.vnis_map.get(self.vni_id, None) is not self:
                assert nve.device is self.device
                nve.add_vni(self)
            self._nve = weakref.ref(nve)

    host_reachability_protocol = managedattribute(
        name='host_reachability_protocol',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    load_balance = managedattribute(
        name='load_balance',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    mcast_group = managedattribute(
        name='mcast_group',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    vrf = managedattribute(
        name='vrf',
        default=None,
        type=(None, managedattribute.test_isinstance(Vrf)))

    def __init__(self, vni_id, device=None, nve=None, *args, **kwargs):
        if not device:
            if not nve:
                raise TypeError('provide either device or nve arguments')
            device = nve.device
        self._vni_id = int(vni_id)
        self._device = weakref.ref(device)
        super().__init__(*args, nve=nve, **kwargs)

    def _on_added_from_nve_interface(self, nve):
        self.nve = nve

    def _on_removed_from_nve_interface(self, nve):
        self.nve = None

    def __eq__(self, other):
        if not isinstance(other, Vni):
            return NotImplemented
        # return (self.device, self.vni_id) == (other.device, other.vni_id)
        return (self.vni_id, self.device) == (other.vni_id, other.device)

    def __lt__(self, other):
        if not isinstance(other, Vni):
            return NotImplemented
        return (self.device, self.vni_id) < (other.device, other.vni_id)

    def __hash__(self):
        return hash(self.vni_id)

