__all__ = (
    'InterfaceStaticNeighbor'
)

# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class InterfaceStaticNeighbor(ConfigurableBase):

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
    #       +- InterfaceAttributes

    # if_static_neighbor
    if_static_neighbor = managedattribute(
        name='if_static_neighbor',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # if_static_cost
    if_static_cost = managedattribute(
        name='if_static_cost',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # if_static_poll_interval
    if_static_poll_interval = managedattribute(
        name='if_static_poll_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # if_static_priority
    if_static_priority = managedattribute(
        name='if_static_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, InterfaceStaticNeighbor):
            raise NotImplemented
        
        return (self.if_static_neighbor,
                self.if_static_cost,
                self.if_static_poll_interval,
                self.if_static_priority,
                self.device) == \
               (other.if_static_neighbor,
                other.if_static_cost,
                other.if_static_poll_interval,
                other.if_static_priority,
                other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, InterfaceStaticNeighbor):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(s=type(self), o=type(other)))

        str1 = '{} {} {} {}'.format(self.if_static_neighbor,\
                                    self.if_static_cost,\
                                    self.if_static_poll_interval,\
                                    self.if_static_priority)
        str2 = '{} {} {} {}'.format(other.if_static_neighbor,\
                                    other.if_static_cost,\
                                    other.if_static_poll_interval,\
                                    other.if_static_priority)
        return str1 < str2
    
    # Overload __hash__
    def __hash__(self):
        return hash((self.if_static_neighbor,
                    self.if_static_cost,
                    self.if_static_poll_interval,
                    self.if_static_priority,
                    self.device))

    # Overload __repr__
    def __repr__(self):
        return '%s object at 0x%x with static neighbor %s' % (
                self.__class__.__name__,
                id(self),
                self.if_static_neighbor)


    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)