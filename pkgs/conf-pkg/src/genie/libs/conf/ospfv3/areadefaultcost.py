__all__ = (
    'AreaDefaultCost'
)

# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class AreaDefaultCost(ConfigurableBase):

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

    # af_area_id
    af_area_id = managedattribute(
        name='af_area_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # area_def_cost
    area_def_cost = managedattribute(
        name='area_def_cost',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, AreaDefaultCost):
            raise NotImplemented

        return (self.af_area_id,
                self.area_def_cost,
                self.device) == \
            (other.af_area_id,
             other.area_def_cost,
             other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, AreaDefaultCost):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(
                s=type(self), o=type(other)))

        return (self.af_area_id,
                self.area_def_cost,
                self.device) < \
            (other.af_area_id,
             other.area_def_cost,
             other.device)

    # Overload __hash__
    def __hash__(self):
        return hash((self.af_area_id,
                     self.area_def_cost,
                     self.device))

    # Overload __repr__
    def __repr__(self):
        return '%s object at 0x%x' % (
            self.__class__.__name__,
            id(self))

    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)
