__all__ = (
    'AreaNetwork'
)

# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class AreaNetwork(ConfigurableBase):

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
    #     +- AreaAttributes

    # area_network
    area_network = managedattribute(
        name='area_network',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # area_network_wildcard
    area_network_wildcard = managedattribute(
        name='area_network_wildcard',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, AreaNetwork):
            raise NotImplemented
        
        return (self.area_network,
                self.area_network_wildcard,
                self.device) == \
               (other.area_network,
                other.area_network_wildcard,
                other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, AreaNetwork):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(s=type(self), o=type(other)))

        return (self.area_network,
                self.area_network_wildcard,
                self.device) < \
               (other.area_network,
                other.area_network_wildcard,
                other.device)

    # Overload __hash__
    def __hash__(self):
        return hash((self.area_network,
                     self.area_network_wildcard,
                     self.device))

    # Overload __repr__
    def __repr__(self):
        return '%s object at 0x%x' % (
                self.__class__.__name__,
                id(self))

    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)