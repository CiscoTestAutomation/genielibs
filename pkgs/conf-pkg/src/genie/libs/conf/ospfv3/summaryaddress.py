__all__ = (
    'SummarAddress'
)

# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class SummaryAddress(ConfigurableBase):

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
    #       +- AddressFamilyAttributes

    # summary_address_prefix
    summary_address_prefix = managedattribute(
        name='summary_address_prefix',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # summary_address_not_advertise
    summary_address_not_advertise = managedattribute(
        name='summary_address_not_advertise',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # summary_address_tag
    summary_address_tag = managedattribute(
        name='summary_address_tag',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, SummaryAddress):
            raise NotImplemented

        return (self.summary_address_prefix,
                self.summary_address_not_advertise,
                self.summary_address_tag,
                self.device) == \
            (other.summary_address_prefix,
             other.summary_address_not_advertise,
             other.summary_address_tag,
             other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, SummaryAddress):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(
                s=type(self), o=type(other)))

        return (self.summary_address_prefix,
                self.summary_address_not_advertise,
                self.summary_address_tag,
                self.device) < \
            (other.summary_address_prefix,
             other.summary_address_not_advertise,
             other.summary_address_tag,
             other.device)

    # Overload __hash__
    def __hash__(self):
        return hash((self.summary_address_prefix,
                     self.summary_address_not_advertise,
                     self.summary_address_tag,
                     self.device))

    # Overload __repr__
    def __repr__(self):
        return '%s object at 0x%x' % (
            self.__class__.__name__,
            id(self))

    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)
