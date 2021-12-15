__all__ = (
    'AreaRange'
)

# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class AreaRange(ConfigurableBase):

    @property
    def testbed(self):
        return self.device.testbed

    @property
    def device(self):
        return self._device()

    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================

    # +- DeviceAttributes
    #   +- VrfAttributes
    #       +- AddressFamilyAttributes

    # range_area_id
    range_area_id = managedattribute(
        name='range_area_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # area_range_prefix
    area_range_prefix = managedattribute(
        name='area_range_prefix',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # area_range_not_advertise
    area_range_not_advertise = managedattribute(
        name='area_range_not_advertise',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area_range_cost
    area_range_cost = managedattribute(
        name='area_range_cost',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, AreaRange):
            raise NotImplemented

        return (self.area_range_prefix,
                self.area_range_not_advertise,
                self.area_range_cost,
                self.range_area_id,
                self.device) == \
            (other.area_range_prefix,
             other.area_range_not_advertise,
             other.area_range_cost,
             other.range_area_id,
             other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, AreaRange):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(
                s=type(self), o=type(other)))

        return (self.area_range_prefix,
                self.area_range_not_advertise,
                self.area_range_cost,
                self.range_area_id,
                self.device) < \
            (other.area_range_prefix,
             other.area_range_not_advertise,
             other.area_range_cost,
             other.range_area_id,
             other.device)

    # Overload __hash__
    def __hash__(self):
        return hash((self.area_range_prefix,
                     self.area_range_not_advertise,
                     self.area_range_cost,
                     self.range_area_id,
                     self.device))

    # Overload __repr__
    def __repr__(self):
        return '%s object at 0x%x' % (
            self.__class__.__name__,
            id(self))

    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)
