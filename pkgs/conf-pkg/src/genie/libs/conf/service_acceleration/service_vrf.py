__all__ = (
    'ServiceVrf',
)

# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class ServiceVrf(ConfigurableBase):

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

    # service_vrf_name
    service_vrf_name = managedattribute(
        name='vrf_name',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # module_affinity
    module_affinity = managedattribute(
        name="module_affinity", 
        default='dynamic', 
        type=(None, managedattribute.test_in({'dynamic',1, 2, 3, 4}))
    )


    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, ServiceVrf):
            raise NotImplemented

        return (self.service_vrf_name,
                self.module_affinity,
                self.device) == \
            (other.service_vrf_name,
             other.module_affinity,
             other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, ServiceVrf):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(
                s=type(self), o=type(other)))

        return (self.service_vrf_name,
                self.module_affinity,
                self.device) < \
            (other.service_vrf_name,
             other.module_affinity,
             other.device)

    # Overload __hash__
    def __hash__(self):
        return hash((self.service_vrf_name,
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
