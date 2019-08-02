__all__ = (
    'Mroute'
)

# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase
from genie.libs.conf.base import IPv4Address, IPv6Address, IPv4Interface, IPv6Interface


@functools.total_ordering
class Mroute(ConfigurableBase):

    @property
    def testbed(self):
        return self.device.testbed

    @property
    def device(self):
        return self._device()

    # mroute_address
    mroute_address = managedattribute(
        name='mroute_ip_address',
        default=None,
        type=(None, IPv4Address, IPv6Address),
        doc="Configure 'ip mroute' or 'ipv6 mroute' on the device.")

    # mroute_prefix_mask
    mroute_prefix_mask = managedattribute(
        name='mroute_prefix_mask',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure 'ip/ipv6 mroute' prefix mask on the device.")

    # mroute_neighbor_address
    mroute_neighbor_address = managedattribute(
        name='mroute_neighbor_address',
        default=None,
        type=(None, IPv4Address, IPv6Address),
        doc="Configure 'ip/ipv6 mroute' neighbor address on the device.")
    
    # mroute_interface_name
    mroute_interface_name = managedattribute(
        name='mroute_interface_name',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure 'ip/ipv6 mroute' interface name on the device.")
    
    # mroute_admin_distance
    mroute_admin_distance = managedattribute(
        name='mroute_admin_distance',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure 'ip/ipv6 mroute' admin distance on the device.")

    # mroute_vrf
    mroute_vrf = managedattribute(
        name='mroute_vrf',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure 'ip/ipv6 mroute' VRF on the device.")

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, Mroute):
            raise NotImplemented
        
        return (self.mroute_address,
                self.mroute_prefix_mask,
                self.mroute_neighbor_address,
                self.mroute_admin_distance,
                self.mroute_vrf,
                self.mroute_interface_name,
                self.device) == \
               (other.mroute_address,
                other.mroute_prefix_mask,
                other.mroute_neighbor_address,
                other.mroute_admin_distance,
                other.mroute_vrf,
                other.mroute_interface_name,
                other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, Mroute):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(s=type(self), o=type(other)))

        # Comparing same types (both v4 or both v6)
        if type(self.mroute_address) == type(other.mroute_address):
            return self.mroute_address < other.mroute_address
        # Comparing mistmatch types
        else:
            self_addr = str(self.mroute_address)
            other_addr = str(other.mroute_address)
            return self_addr < other_addr
    
    # Overload __hash__
    def __hash__(self):
        return hash((self.mroute_address,
                self.mroute_prefix_mask,
                self.mroute_neighbor_address,
                self.mroute_admin_distance,
                self.mroute_vrf,
                self.mroute_interface_name,
                self.device))

    # Overload __repr__
    def __repr__(self):
        if isinstance(self.mroute_address, IPv6Address):
            return '%s object at 0x%x with ipv6 address %s/%s' % (
                    self.__class__.__name__,
                    id(self),
                    self.mroute_address,
                    self.mroute_prefix_mask)
        else:
            return '%s object at 0x%x with ip address %s/%s' % (
                    self.__class__.__name__,
                    id(self),
                    self.mroute_address,
                    self.mroute_prefix_mask)


    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)