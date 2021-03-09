__all__ = (
    'IPv4Addr'
)

# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase
from genie.libs.conf.base import IPv4Address


@functools.total_ordering
class IPv4Addr(ConfigurableBase):

    @property
    def testbed(self):
        return self.device.testbed

    @property
    def device(self):
        return self._device()

    # ipv4
    ipv4 = managedattribute(
        name='ipv4',
        default=None,
        type=(None, IPv4Address, managedattribute.test_istype(str)),
        doc='IP address')

    # ipv4_secondary
    ipv4_secondary = managedattribute(
        name='ipv4_secondary',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Make this IP address a secondary address')

    # prefix_length
    prefix_length = managedattribute(
        name='prefix_length',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='IP subnet mask')

    # route_tag
    route_tag = managedattribute(
        name='route_tag',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='URIB route tag value for local/direct routes')

    # secondary_vrf
    secondary_vrf = managedattribute(
        name='secondary_vrf',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Assign the secondary address to a VRF table')

    # ip redirect
    redirect = managedattribute(
        name='redirect',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Assign the redirect attribute'
    )

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, IPv4Addr):
            return False
        return (self.ipv4,
                self.ipv4_secondary,
                self.prefix_length,
                self.route_tag,
                self.secondary_vrf,
                self.device) == \
               (other.ipv4,
                other.ipv4_secondary,
                other.prefix_length,
                other.route_tag,
                other.secondary_vrf,
                other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, IPv4Addr):
            return NotImplemented("Cannot compare '{s}' to a '{o}'".format(s=type(self), o=type(other)))

        if self.ipv4 and other.ipv4:
            # compare v4 addresses if both v4
            return self.ipv4 < other.ipv4

    # Overload __hash__
    def __hash__(self):
        return hash((self.ipv4,
            self.ipv4_secondary,
            self.prefix_length,
            self.route_tag,
            self.secondary_vrf,
            self.device))

    # Overload __repr__
    def __repr__(self):
        if self.ipv4:
            return '%s object at 0x%x with ip address %s/%s' % (
                self.__class__.__name__,
                id(self),
                self.ipv4,
                self.prefix_length)

    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)
