
# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class Ssm(ConfigurableBase):

    @property
    def testbed(self):
        return self.device.testbed

    @property
    def device(self):
        return self._device()

    # ssm_source_addr
    ssm_source_addr = managedattribute(
        name='ssm_source_addr',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure ssm_source_addr under vrf.")

    # ssm_group_policy
    ssm_group_policy = managedattribute(
        name='ssm_group_policy',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure ssm_group_policy under vrf.")

    # ssm_group_range
    ssm_group_range = managedattribute(
        name='ssm_group_range',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure ssm_group_range under vrf.")

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, Ssm):
            raise NotImplemented
        
        return (self.ssm_source_addr,
                self.ssm_group_range,
                self.ssm_group_policy,
                self.device) == \
               (other.ssm_source_addr,
                other.ssm_group_range,
                other.ssm_group_policy,
                other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, Ssm):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(s=type(self), o=type(other)))

        # Comparing same types
        if type(self.ssm_source_addr) == type(other.ssm_source_addr):
            if type(self.ssm_group_range) != type(None):
                if self.ssm_source_addr == other.ssm_source_addr:
                    return self.ssm_group_range < other.ssm_group_range
            elif type(self.ssm_group_policy) != type(None):
                if self.ssm_source_addr == other.ssm_source_addr:
                    return self.ssm_group_policy < other.ssm_group_policy
            return self.ssm_source_addr < other.ssm_source_addr
        # Comparing mistmatch types
        else:
            self_addr = str(self.ssm_source_addr)
            other_addr = str(other.ssm_source_addr)
            return self_addr < other_addr
    
    # Overload __hash__
    def __hash__(self):
        return hash((self.ssm_source_addr,
                self.ssm_group_range,
                self.ssm_group_policy,
                self.device))

    # Overload __repr__
    def __repr__(self):
        if isinstance(self.ssm_source_addr, str):
            return '%s object at 0x%x with string %s/%s/%s' % (
                    self.__class__.__name__,
                    id(self),
                    self.ssm_source_addr,
                    self.ssm_group_range,
                    self.ssm_group_policy)
        else:
            return '%s object at 0x%x with the name %s/%s/%s which is not string' % (
                    self.__class__.__name__,
                    id(self),
                    self.ssm_source_addr,
                    self.ssm_group_range,
                    self.ssm_group_policy)


    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)