__all__ = (
    'StubRouter'
)

# Python
import weakref
import functools
from enum import Enum

# Genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase


@functools.total_ordering
class StubRouter(ConfigurableBase):

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

    # stub_router_always
    stub_router_always = managedattribute(
        name='stub_router_always',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # stub_router_on_startup
    stub_router_on_startup = managedattribute(
        name='stub_router_on_startup',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # stub_router_on_switchover
    stub_router_on_switchover = managedattribute(
        name='stub_router_on_switchover',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # stub_router_include_stub
    stub_router_include_stub = managedattribute(
        name='stub_router_include_stub',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # stub_router_summary_lsa
    stub_router_summary_lsa = managedattribute(
        name='stub_router_summary_lsa',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # stub_router_external_lsa
    stub_router_external_lsa = managedattribute(
        name='stub_router_external_lsa',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==========================================================================

    # Overload __eq__
    def __eq__(self, other):
        if not isinstance(other, StubRouter):
            raise NotImplemented
        
        return (self.stub_router_always,
                self.stub_router_on_startup,
                self.stub_router_on_switchover,
                self.stub_router_include_stub,
                self.stub_router_summary_lsa,
                self.stub_router_external_lsa,
                self.device) == \
               (other.stub_router_always,
                other.stub_router_on_startup,
                other.stub_router_on_switchover,
                other.stub_router_include_stub,
                other.stub_router_summary_lsa,
                other.stub_router_external_lsa,
                other.device)

    # Overload __lt__
    def __lt__(self, other):
        if not isinstance(other, StubRouter):
            raise NotImplemented("Cannot compare '{s}' to a '{o}'".format(s=type(self), o=type(other)))

        str1 = '{} {} {} {} {} {}'.format(self.stub_router_always,\
                                        self.stub_router_on_startup,\
                                        self.stub_router_on_switchover,\
                                        self.stub_router_include_stub,\
                                        self.stub_router_summary_lsa,\
                                        self.stub_router_external_lsa)
        str2 = '{} {} {} {} {} {}'.format(other.stub_router_always,\
                                        other.stub_router_on_startup,\
                                        other.stub_router_on_switchover,\
                                        other.stub_router_include_stub,\
                                        other.stub_router_summary_lsa,\
                                        other.stub_router_external_lsa)
        return str1 < str2
    
    # Overload __hash__
    def __hash__(self):
        return hash((self.stub_router_always,
                     self.stub_router_on_startup,
                     self.stub_router_on_switchover,
                     self.stub_router_include_stub,
                     self.stub_router_summary_lsa,
                     self.stub_router_external_lsa,
                     self.device))

    # Overload __repr__
    def __repr__(self):
        return '%s object at 0x%x' % (
                self.__class__.__name__,
                id(self))

    def __init__(self, device, *args, **kwargs):
        self._device = weakref.ref(device)
        super().__init__(*args, **kwargs)