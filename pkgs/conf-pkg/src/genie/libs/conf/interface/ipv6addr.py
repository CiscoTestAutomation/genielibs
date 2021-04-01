__all__ = (
    'IPv6Addr'
)

# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase
from genie.libs.conf.base import IPv6Address


@functools.total_ordering
class IPv6Addr(ConfigurableBase):

    @property
    def testbed(self):
        return self.device.testbed

    @property
    def device(self):
        return self._device()

    # ipv6
    ipv6 = managedattribute(
        name='ipv6',
        default=None,
        type=(None, IPv6Address),
        doc='IPv6 address')

    # ipv6_prefix_length
    ipv6_prefix_length = managedattribute(
        name='ipv6_prefix_length',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='IPv6 subnet mask')

    # ipv6_anycast
    ipv6_anycast = managedattribute(
        name='ipv6_anycast',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Configure as an anycast')

    # ipv6_eui_64
    ipv6_eui_64 = managedattribute(
        name='ipv6_eui_64',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Use eui-64 interface identifier')

    # ipv6_route_tag
    ipv6_route_tag = managedattribute(
        name='ipv6_route_tag',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Route-tag to be associated with this address')

    # ipv6 redirect
    redirect = managedattribute(
        name='redirect',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Assign the v6 redirect attribute'
    )


    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, IPv6Addr):
            return False
        return (self.ipv6,
                self.ipv6_prefix_length,
                self.ipv6_anycast,
                self.ipv6_eui_64,
                self.ipv6_route_tag,
                self.device) == \
               (other.ipv6,
                other.ipv6_prefix_length,
                other.ipv6_anycast,
                other.ipv6_eui_64,
                other.ipv6_route_tag,
                other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, IPv6Addr):
            return NotImplemented("Cannot compare '{s}' to a '{o}'"\
                .format(s=type(self), o=type(other)))

        if self.ipv6 and other.ipv6:
            # compare v6 addresses if both v6
            return self.ipv6 < other.ipv6

    # Overload __hash__
    def __hash__(self):
        return hash((self.ipv6,
            self.ipv6_prefix_length,
            self.ipv6_anycast,
            self.ipv6_eui_64,
            self.ipv6_route_tag,
            self.device))

    # Overload __repr__
    def __repr__(self):
        if self.ipv6:
            return '%s object at 0x%x with ip address %s/%s' % (
                self.__class__.__name__,
                id(self),
                self.ipv6,
                self.ipv6_prefix_length)

    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)
