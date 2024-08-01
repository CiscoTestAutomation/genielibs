__all__ = (
    'ipv6verify'
)

# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class Ipv6Verify(ConfigurableBase):

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
    #   +- InterfaceAttributes

    # ipv6_verify_strict
    ipv6_verify_strict = managedattribute(
        name='ipv6_verify_strict',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ipv6_strict_allow_vnihosts
    ipv6_strict_allow_vnihosts = managedattribute(
        name='ipv6_strict_allow_vnihosts',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ipv6_verify_loose
    ipv6_verify_loose = managedattribute(
        name='ipv6_verify_loose',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ipv6_loose_allow_default
    ipv6_loose_allow_default = managedattribute(
        name='ipv6_loose_allow_default',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, Ipv6Verify):
            raise NotImplemented

        return (self.ipv6_verify_strict,
                self.ipv6_verify_loose,
                self.ipv6_strict_allow_vnihosts,
                self.ipv6_loose_allow_default,
                self.device) == \
            (other.ipv6_verify_strict,
                other.ipv6_verify_loose,
                other.ipv6_strict_allow_vnihosts,
                other.ipv6_loose_allow_default,
                other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, Ipv6Verify):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(
                s=type(self), o=type(other)))

        return (self.ipv6_verify_strict,
                self.ipv6_verify_loose,
                self.ipv6_strict_allow_vnihosts,
                self.ipv6_loose_allow_default,
                self.device) < \
            (other.ipv6_verify_strict,
                other.ipv6_verify_loose,
                other.ipv6_strict_allow_vnihosts,
                other.ipv6_loose_allow_default,
                other.device)

    # Overload __hash__
    def __hash__(self):
        return hash((self.ipv6_verify_strict,
                self.ipv6_verify_loose,
                self.ipv6_strict_allow_vnihosts,
                self.ipv6_loose_allow_default,
                self.device))

    # Overload __repr__
    def __repr__(self):
        return '%s object at 0x%x' % (
            self.__class__.__name__,
            id(self))

    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)