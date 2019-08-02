__all__ = (
    'GracefulRestart'
)

# Python
import weakref
import functools
from enum import Enum

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
    #                           GLOBAL ENUM TYPES
    # ==========================================================================
    
    class GR_TYPE(Enum):
        ietf = 'ietf'
        cisco = 'cisco'

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

    # gr_type
    gr_type = managedattribute(
        name='gr_type',
        default=GR_TYPE.ietf,
        type=(None, GR_TYPE))

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

    # gr_helper_strict_lsa_checking
    gr_helper_strict_lsa_checking = managedattribute(
        name='gr_helper_strict_lsa_checking',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, GracefulRestart):
            raise NotImplemented
        
        return (self.gr_enable,
                self.gr_type,
                self.gr_helper_enable,
                self.gr_restart_interval,
                self.gr_helper_strict_lsa_checking,
                self.device) == \
               (other.gr_enable,
                other.gr_type,
                other.gr_helper_enable,
                other.gr_restart_interval,
                other.gr_helper_strict_lsa_checking,
                other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, GracefulRestart):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(s=type(self), o=type(other)))

        str1 = '{} {} {} {} {}'.format(self.gr_enable,\
                                       self.gr_type.value,\
                                       self.gr_helper_enable,\
                                       self.gr_restart_interval,\
                                       self.gr_helper_strict_lsa_checking)
        str2 = '{} {} {} {} {}'.format(other.gr_enable,\
                                       other.gr_type.value,\
                                       other.gr_helper_enable,\
                                       other.gr_restart_interval,\
                                       other.gr_helper_strict_lsa_checking)
        return str1 < str2
    
    # Overload __hash__
    def __hash__(self):
        return hash((self.gr_enable,
                    self.gr_type,
                    self.gr_helper_enable,
                    self.gr_restart_interval,
                    self.gr_helper_strict_lsa_checking,
                    self.device))

    # Overload __repr__
    def __repr__(self):
        if isinstance(self.gr_type, GracefulRestart.GR_TYPE):
            return '%s object at 0x%x with graceful restart type %s' % (
                    self.__class__.__name__,
                    id(self),
                    self.gr_type)


    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)