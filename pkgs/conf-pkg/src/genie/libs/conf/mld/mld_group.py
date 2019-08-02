
# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class MldGroup(ConfigurableBase):

    @property
    def testbed(self):
        return self.device.testbed

    @property
    def device(self):
        return self._device()

    # join_group
    join_group = managedattribute(
        name='join_group',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure join_group under interface.")

    # join_group_source_addr
    join_group_source_addr = managedattribute(
        name='join_group_source_addr',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure join_group_source_addr under interface.")

    # static_group
    static_group = managedattribute(
        name='static_group',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure static_group under interface.")

    # static_group_source_addr
    static_group_source_addr = managedattribute(
        name='static_group_source_addr',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure static_group_source_addr under interface.")

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, MldGroup):
            raise NotImplemented
        
        return (self.join_group,
                self.join_group_source_addr,
                self.static_group,
                self.static_group_source_addr,
                self.device) == \
               (other.join_group,
                other.join_group_source_addr,
                other.static_group,
                other.static_group_source_addr,
                other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, MldGroup):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(s=type(self), o=type(other)))

        group_current = self.join_group if self.join_group else self.static_group
        group_previous = other.join_group if other.join_group else other.static_group

        source_current = self.join_group_source_addr if \
            self.join_group_source_addr else self.static_group_source_addr
        source_previous = other.join_group_source_addr if \
            other.join_group_source_addr else other.static_group_source_addr

        # Comparing same types
        if type(group_current) == type(group_previous):
            if group_current == group_previous:
                return source_current < source_previous
            return group_current < group_previous
        else:
            self_addr = str(group_current)
            other_addr = str(group_previous)
            return self_addr < other_addr

    
    # Overload __hash__
    def __hash__(self):
        return hash((self.join_group,
                     self.join_group_source_addr,
                     self.static_group,
                     self.static_group_source_addr,
                     self.device))

    # Overload __repr__
    def __repr__(self):
        if isinstance(self.join_group, str):
            return '%s object at 0x%x with string name %s/%s/%s/%s' % (
                    self.__class__.__name__,
                    id(self),
                    self.join_group,
                    self.join_group_source_addr,
                    self.static_group,
                    self.static_group_source_addr)
        else:
            return '%s object at 0x%x with the name %s/%s/%s/%s which is not string' % (
                    self.__class__.__name__,
                    id(self),
                    self.join_group,
                    self.join_group_source_addr,
                    self.static_group,
                    self.static_group_source_addr)


    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)