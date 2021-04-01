'''
    Generic Device class for TGEN-based devices.
'''

__all__ = (
    'Device',
)

import contextlib
import logging
logger = logging.getLogger(__name__)

from genie.decorator import managedattribute

import genie.libs.conf.device
from genie.libs.conf.stream.stream import Stream

class Device(genie.libs.conf.device.Device):
    '''Base Device class for TGEN devices'''

    @property
    def tgen_port_interfaces(self):
        from genie.libs.conf.interface.tgen import PhysicalInterface
        def testPhysicalInterface(intf):
            return isinstance(intf, PhysicalInterface)
        return self.find_interfaces(
            # XXXJST This is supposed to be self_, not callable_!!
            callable_=testPhysicalInterface)

    streams = managedattribute(
        name='streams',
        finit=set,
        read_only=True)

    def find_streams(self, *rs, iterable=None, count=None,
                     cls=Stream, obj_state='active', **kwargs):
        '''Find Stream objects from Device object or from a provided iterable'''
        if iterable is None:
            iterable = self.streams

        return self._find_objects(*rs, iterable=iterable, count=count, cls=cls,
                                  obj_state=obj_state, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def restart_traffic(self, **kwargs):
        raise NotImplementedError

    def start_traffic(self, **kwargs):
        raise NotImplementedError

    def stop_traffic(self, **kwargs):
        raise NotImplementedError

    def traffic_control(self, **kwargs):
        raise NotImplementedError

    def is_traffic_running(self, **kwargs):
        raise NotImplementedError

    def get_stream_stats(self, streams=None, **kwargs):
        raise NotImplementedError

    def get_stream_resolved_mac_addresses(self, streams=None):
        raise NotImplementedError

    def start_emulation(self, **kwargs):
        raise NotImplementedError

    def stop_emulation(self, **kwargs):
        raise NotImplementedError

    @contextlib.contextmanager
    def defer_apply_context(self):
        '''A context during which low-level apply calls are deferred.

        Implementation is Vendor-specific and may not be available, in such
        cases, this is a no-op.
        '''
        yield  # no-op

