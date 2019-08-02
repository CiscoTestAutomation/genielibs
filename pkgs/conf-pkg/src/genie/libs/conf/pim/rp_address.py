
# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class RPAddressGroup(ConfigurableBase):

    @property
    def testbed(self):
        return self.device.testbed

    @property
    def device(self):
        return self._device()

    # # ==== PIM Static-RP =======
    static_rp_address = managedattribute(
        name='static_rp_address',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="IP address of router which is RP for group range")

    static_rp_group_list = managedattribute(
        name='static_rp_group_list',
        default=None,
        type=(None, managedattribute.test_istype(str),
                    managedattribute.test_istype(int)),
        doc="Group range for static RP")

    static_rp_prefix_list = managedattribute(
        name='static_rp_prefix_list',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Prefix List policy for static RP")

    static_rp_route_map = managedattribute(
        name='static_rp_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Route Map policy for static RP")

    static_rp_policy = managedattribute(
        name='static_rp_policy',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Group range policy for static RP")

    static_rp_bidir = managedattribute(
        name='static_rp_bidir',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="Group range advertised in PIM bidirectional mode")

    # this is used when ipv6
    static_rp_override = managedattribute(
        name='static_rp_override',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="Overrides the dynamically learnt RPs")

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, RPAddressGroup) or \
           not isinstance(self, RPAddressGroup):
            raise NotImplemented
        
        return (self.static_rp_address,
                self.static_rp_group_list,
                self.static_rp_prefix_list,
                self.static_rp_route_map,
                self.static_rp_policy,
                self.static_rp_bidir,
                self.static_rp_override,
                self.device) == \
               (other.static_rp_address,
                other.static_rp_group_list,
                other.static_rp_prefix_list,
                other.static_rp_route_map,
                other.static_rp_policy,
                other.static_rp_bidir,
                other.static_rp_override,
                other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, RPAddressGroup) or \
           not isinstance(self, RPAddressGroup):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(s=type(self), o=type(other)))

        # Comparing same types
        if type(self.static_rp_address) == type(other.static_rp_address):
            return self.static_rp_address < other.static_rp_address
        else:
            self_addr = str(self.static_rp_address)
            other_addr = str(other.static_rp_address)
            return self_addr < other_addr

    
    # Overload __hash__
    def __hash__(self):
        return hash((self.static_rp_address,
                    self.static_rp_group_list,
                    self.static_rp_prefix_list,
                    self.static_rp_route_map,
                    self.static_rp_policy,
                    self.static_rp_bidir,
                    self.static_rp_override,
                     self.device))

    # Overload __repr__
    def __repr__(self):
        if isinstance(self.join_group, str):
            return '%s object at 0x%x with string name %s/%s/%s/%s/%s/%s/%s' % (
                    self.__class__.__name__,
                    id(self),
                    self.static_rp_address,
                    self.static_rp_group_list,
                    self.static_rp_prefix_list,
                    self.static_rp_route_map,
                    self.static_rp_policy,
                    self.static_rp_bidir,
                    self.static_rp_override,)
        else:
            return '%s object at 0x%x with none string name %s/%s/%s/%s/%s/%s/%s' % (
                    self.__class__.__name__,
                    id(self),
                    self.static_rp_address,
                    self.static_rp_group_list,
                    self.static_rp_prefix_list,
                    self.static_rp_route_map,
                    self.static_rp_policy,
                    self.static_rp_bidir,
                    self.static_rp_override,)


    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)