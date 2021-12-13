__all__ = (
    'AreaRouteMap'
)

# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class AreaRouteMap(ConfigurableBase):

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

    # routemap_area_id
    routemap_area_id = managedattribute(
        name='routemap_area_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # ar_route_map_in
    ar_route_map_in = managedattribute(
        name='ar_route_map_in',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # ar_route_map_out
    ar_route_map_out = managedattribute(
        name='ar_route_map_out',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, AreaRouteMap):
            raise NotImplemented

        return (self.routemap_area_id,
                self.ar_route_map_in,
                self.ar_route_map_out,
                self.device) == \
            (other.routemap_area_id,
             other.ar_route_map_in,
             other.ar_route_map_out,
             other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, AreaRouteMap):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(
                s=type(self), o=type(other)))

        return (self.routemap_area_id,
                self.ar_route_map_in,
                self.ar_route_map_out,
                self.device) < \
            (other.routemap_area_id,
             other.ar_route_map_in,
             other.ar_route_map_out,
             other.device)

    # Overload __hash__
    def __hash__(self):
        return hash((self.routemap_area_id,
                     self.ar_route_map_in,
                     self.ar_route_map_out,
                     self.device))

    # Overload __repr__
    def __repr__(self):
        return '%s object at 0x%x' % (
            self.__class__.__name__,
            id(self))

    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)
