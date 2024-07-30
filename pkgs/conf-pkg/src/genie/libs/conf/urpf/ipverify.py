__all__ = (
    'ipverify'
)

# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class IpVerify(ConfigurableBase):

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

    # ip_verify_strict
    ip_verify_strict = managedattribute(
        name='ip_verify_strict',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ip_verify_loose
    ip_verify_loose = managedattribute(
        name='ip_verify_loose',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ip_loose_allow_default
    ip_loose_allow_default = managedattribute(
        name='ip_loose_allow_default',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, IpVerify):
            raise NotImplemented

        return (self.ip_verify_strict,
                self.ip_verify_loose,
                self.ip_loose_allow_default,
                self.device) == \
            (other.ip_verify_strict,
             other.ip_verify_loose,
             other.ip_loose_allow_default,
             other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, IpVerify):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(
                s=type(self), o=type(other)))

        return (self.ip_verify_strict,
                self.ip_verify_loose,
                self.ip_loose_allow_default,
                self.device) < \
            (other.ip_verify_strict,
            other.ip_verify_loose,
            other.ip_loose_allow_default,
            other.device)

    # Overload __hash__
    def __hash__(self):
        return hash((self.ip_verify_strict,
                self.ip_verify_loose,
                self.ip_loose_allow_default,
                self.device))

    # Overload __repr__
    def __repr__(self):
        return '%s object at 0x%x' % (
            self.__class__.__name__,
            id(self))

    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)