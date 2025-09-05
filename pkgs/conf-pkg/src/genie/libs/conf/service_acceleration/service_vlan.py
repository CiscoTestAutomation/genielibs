__all__ = (
    'ServiceVlan',
)

# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class ServiceVlan(ConfigurableBase):

    @property
    def testbed(self):
        return self.device.testbed

    @property
    def device(self):
        return self._device()

    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================

    # ServiceAcceleration
    #     +- DeviceAttributes
    #       +- ServiceAttributes

    # service_vlan_name
    service_vlan_name = managedattribute(
        name='vlan_name',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # module_affinity
    module_affinity = managedattribute(
        name="module_affinity", 
        default='dynamic', 
        type=(None, managedattribute.test_in({'dynamic',1, 2, 3, 4}))
    )


    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, ServiceVlan):
            raise NotImplemented

        return (self.service_vlan_name,
                self.module_affinity,
                self.device) == \
            (other.service_vlan_name,
             other.module_affinity,
             other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, ServiceVlan):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(
                s=type(self), o=type(other)))

        return (self.service_vlan_name,
                self.module_affinity,
                self.device) < \
            (other.service_vlan_name,
             other.module_affinity,
             other.device)

    # Overload __hash__
    def __hash__(self):
        return hash((self.service_vlan_name,
                     self.module_affinity,
                     self.device))

    # Overload __repr__
    def __repr__(self):
        return '%s object at 0x%x' % (
            self.__class__.__name__,
            id(self))

    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)
