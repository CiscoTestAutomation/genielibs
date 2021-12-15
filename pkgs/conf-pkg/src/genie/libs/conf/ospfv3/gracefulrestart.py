__all__ = (
    'GracefulRestart'
)

# Python
import weakref
import functools

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class GracefulRestart(ConfigurableBase):

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

    # gr_enable
    gr_enable = managedattribute(
        name='gr_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # gr_helper_enable
    gr_helper_enable = managedattribute(
        name='gr_helper_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # gr_restart_interval
    gr_restart_interval = managedattribute(
        name='gr_restart_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # gr_planned_only
    gr_planned_only = managedattribute(
        name='gr_planned_only',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, GracefulRestart):
            raise NotImplemented

        return (self.gr_enable,
                self.gr_helper_enable,
                self.gr_restart_interval,
                self.gr_planned_only,
                self.device) == \
            (other.gr_enable,
             other.gr_helper_enable,
             other.gr_restart_interval,
             other.gr_planned_only,
             other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, GracefulRestart):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(
                s=type(self), o=type(other)))

        str1 = '{} {} {} {}'.format(self.gr_enable,
                                    self.gr_helper_enable,
                                    self.gr_restart_interval,
                                    self.gr_planned_only)
        str2 = '{} {} {} {}'.format(other.gr_enable,
                                    other.gr_helper_enable,
                                    other.gr_restart_interval,
                                    other.gr_planned_only)
        return str1 < str2

    # Overload __hash__
    def __hash__(self):
        return hash((self.gr_enable,
                    self.gr_helper_enable,
                    self.gr_restart_interval,
                    self.gr_planned_only,
                    self.device))

    # Overload __repr__
    def __repr__(self):
        return '%s object at 0x%x' % (
            self.__class__.__name__,
            id(self))

    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)
