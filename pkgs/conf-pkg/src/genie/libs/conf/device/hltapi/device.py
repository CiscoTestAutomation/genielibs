'''
    Generic Device class for HLTAPI-based devices.
'''

__all__ = (
    'Device',
)

from enum import Enum
import contextlib
import functools
import itertools
import logging
import time
try:
    from hltapi.exceptions import HltapiError
except Exception:
    class HltapiError(Exception):
        pass

from genie.decorator import managedattribute
from genie.conf.base.attributes import AttributesHelper

import genie.libs.conf.device.tgen
from genie.libs.conf.stream.stream import Stream, StreamStats

logger = logging.getLogger(__name__)


class Device(genie.libs.conf.device.tgen.Device):
    '''Base Device class for HLTAPI-based TGEN devices'''

    class Hltapi(object):
        '''HLTAPI abstraction object.

        HLTAPI Device subclasses are encouraged to subclass Hltapi as well to customize HLTAPI calls to allow Vendor-specific requirements.
        '''

        device = managedattribute(
            name='device',
            type=managedattribute.auto_ref,  # TODO Device is not finished declaring yet
            gettype=managedattribute.auto_unref,
            doc='''The HLTAPI-based Genie Device object''')

        @property
        def pyats_connection(self):
            '''The pyATS connection used for HLTAPI access'''
            connectionmgr = self.device.connectionmgr
            try:
                return connectionmgr.connections['hltapi']
            except KeyError:
                # TODO This might not be a HltApiConnection!?
                return connectionmgr.connections[connectionmgr.default_alias]

        @property
        def tcl(self):
            '''The Tcl interpreter instance.'''
            return self.pyats_connection._tcl

        @property
        def tcl_namespace(self):
            '''The Tcl namespace where HLTAPI vendor code is loaded.'''
            return self.pyats_connection._ns

        def __getattr__(self, name):
            '''Redirect to undefined attributes to the pyATS connection.'''

            if not name.startswith('_') and name != 'device':
                return getattr(self.pyats_connection, name)

            f = getattr(super(), '__getattr__', None)
            if f is not None:
                return f(name)
            else:
                raise AttributeError(name)

        def __init__(self, device):
            self.device = device
            super().__init__()

    hltapi = managedattribute(
        name='hltapi',
        read_only=True,
        doc=Hltapi.__doc__)

    @hltapi.initter
    def hltapi(self):
        '''Create an instance of Hltapi.

        This can be a subclass of Hltapi if the Device subclass redefines it.
        '''
        return self.Hltapi(device=self)

    @property
    def all_port_handles(self):
        pass  # TODO hltspl_get_all_port_handles

    @property
    def tgen_port_handle_to_interface_map(self):
        return {
            interface.tgen_port_handle: interface \
            for interface in self.tgen_port_interfaces}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_stream_stats(self, streams=None):
        if streams is None:
            streams = self.find_streams()

        stats = StreamStats()

        hltapi = self.hltapi
        tcl = hltapi.tcl

        #from genie.libs.conf.device.agilent import Device as AgilentDevice
        from genie.libs.conf.device.ixia import Device as IxiaDevice
        #from genie.libs.conf.device.pagent import Device as PagentDevice
        #from genie.libs.conf.device.spirent import Device as SpirentDevice

        map_stream_id_to_stream_obj = {}
        for stream in streams:
            stream_ids = stream.tgen_handle
            if stream_ids:
                for stream_id in stream_ids:
                    assert stream_id not in map_stream_id_to_stream_obj
                    map_stream_id_to_stream_obj[stream_id] = stream
            else:
                logger.warn('%r: Nothing to do (no tgen_handle).', stream)

        if map_stream_id_to_stream_obj:
            tgen_port_handle_to_interface_map = \
                self.tgen_port_handle_to_interface_map
            hltkwargs = {}
            hltkwargs['port_handle'] = \
                list(tgen_port_handle_to_interface_map.keys())
            hltkwargs['mode'] = 'streams'
            hltkwargs['streams'] = list(map_stream_id_to_stream_obj.keys())

            stream_key_rename_map = {
                'tx.pkt_rate': 'tx.total_pkt_rate',
                'rx.pkt_rate': 'rx.total_pkt_rate',
                'rx.loss_pkts': 'rx._dropped_pkts',
            }
            if isinstance(self, IxiaDevice):
                stream_key_rename_map.update({
                    'rx.loss_pkts': 'rx._delta_pkts',
                })

            hltkl = hltapi.traffic_stats(**hltkwargs)
            if hltkl.get('waiting_for_stats', False):
                # if { $try <= 6 } {
                #         continue ;# retry
                # } else {
                #     enaLogVerify -warning "Statistics not ready... giving up"
                # }
                raise NotImplementedError

            for port_handle, rx_interface \
                    in tgen_port_handle_to_interface_map.items():
                for stream_id, hltkl_stream \
                        in hltkl.get('{}.stream'.format(port_handle), {})\
                        .items():
                    stream_id = str(stream_id)  # already string?
                    try:
                        stream = map_stream_id_to_stream_obj[stream_id]
                    except KeyError:
                        continue
                    if stream not in stats.by_stream:
                        stats.by_stream[stream] = StreamStats.ByStreamStats()
                    stream_stats = stats.by_stream[stream]
                    for kfrom, kto in stream_key_rename_map.items():
                        try:
                            v = hltkl_stream.pop(kfrom)
                        except KeyError:
                            continue
                        hltkl_stream.setdefault(kto, v)
                    if rx_interface not in stream_stats.by_interface:
                        stream_stats.by_interface[rx_interface] = StreamStats.ByInterfaceStreamStats()
                    intf_stream_stats = stream_stats.by_interface[rx_interface]
                    for k1, v1 in hltkl_stream.items():
                        if k1 in (
                                'tx',
                                'rx',
                        ):
                            txrx_intf_stream_stats = getattr(intf_stream_stats, k1)
                            txrx_stream_stats = getattr(stream_stats, k1)
                            for k2, v2 in v1.items():
                                setattr(txrx_intf_stream_stats, k2, v2)
                                if k2 in (
                                        'total_pkts', 'total_pkt_rate',
                                        'dropped_pkts', '_dropped_pkts',
                                        'duplicate_pkts', '_duplicate_pkts',
                                ):
                                    setattr(txrx_stream_stats, k2, \
                                        (getattr(txrx_stream_stats, k2, 0) or 0) \
                                        + v2)
                                elif k2 in (
                                        'encap',
                                ):
                                    if getattr(txrx_stream_stats, k2, None) is None:
                                            setattr(txrx_stream_stats, k2, set())
                                    getattr(txrx_stream_stats, k2).add(
                                        v2)
                                else:
                                    pass  # TODO
                        elif k1 in (
                                'ipv4_present', 'ipv6_present',
                                'tcp_present', 'udp_present',
                        ):
                            setattr(intf_stream_stats, k1, v1)
                            if not getattr(stream_stats, k1, False):
                                setattr(stream_stats, k1, v1)
                        else:
                            setattr(intf_stream_stats, k1, v1)

            # XXXJST HACK for TGENs that can't return elapsed_time, such as
            # Pagent
            for stream, stream_stats in stats.by_stream.items():
                if stream_stats.elapsed_time is None:
                    try:
                        stream_stats.elapsed_time = \
                            float(stream_stats.tx.total_pkts)  \
                            / float(stream_stats.tx.total_pkt_rate)
                    except Exception as e:
                        logger.debug('Stream %s: No relevant TX information to'
                                     ' derive elapsed_time from', stream)
                    else:
                        logger.debug('Stream %s: Derived elapsed_time from'
                                     ' tx.total_pkts/tx.total_pkt_rate', stream)

        return stats

    def restart_traffic(self, *, ports=None, learn=True, start=True, clear_on_start=True, wait_rx=True, rx_timeout=10, tx_timeout=10):

        if ports is None:
            ports = set(stream.source_tgen_interface for stream in self.find_streams())

        port_handles = set(port.tgen_port_handle for port in ports)

        klStreamsStats1 = None
        klStreamsStats2 = None

        if port_handles:

            def do_poll_traffic_running():
                nonlocal wait_rx

                timeout = rx_timeout if wait_rx else tx_timeout
                is_traffic_running = False
                td = 0
                t0 = time.perf_counter()
                last_iteration = False
                for iteration in itertools.count(start=1):
                    if last_iteration:
                        is_traffic_running = False
                        logger.info('Timeout waiting for traffic (%r>%r)',
                                    td, timeout)
                        break
                    if iteration > 1:
                        t1 = time.perf_counter()
                        td = int(t1 - t0)
                        time.sleep(1)
                    if td > timeout:
                        last_iteration = True

                    if klStreamsStats1 is not None:
                        klStreamsStats2 = self.get_stream_stats()
                        klStreamsStats = klStreamsStats2 - klStreamsStats1
                    else:
                        klStreamsStats = self.get_stream_stats()

                    is_traffic_running = True
                    for stream in klStreamsStats.by_stream.keys():
                        if wait_rx:
                            # TODO get rx stats specific to MulticastGroup receivers
                            kl_rx = klStreamsStats.by_stream[stream].rx
                            rx_total_pkts = kl_rx.total_pkts
                            if rx_total_pkts is None:
                                rx_total_pkts = 0
                            if not (rx_total_pkts > 0):
                                is_traffic_running = False
                                logger.info('%r RX packets is %r; Not running!', stream, rx_total_pkts)
                            else:
                                logger.info('%r RX packets is %r; Ok.', stream, rx_total_pkts)
                        else:
                            tx_total_pkts = klStreamsStats.by_stream[stream].tx.total_pkts
                            if tx_total_pkts is None:
                                tx_total_pkts = 0
                            if not (tx_total_pkts > 0):
                                is_traffic_running = False
                                logger.info('%r TX packets is %r; Not running!', stream, tx_total_pkts)
                            else:
                                logger.info('%r TX packets is %r; Ok.', stream, tx_total_pkts)

                    if is_traffic_running:
                        break

                if not is_traffic_running:
                    wait_rx = False

                return is_traffic_running

            if learn:
                # Start?, Wait RX/TX (Learn MAC) {{{

                if self.is_traffic_running():
                    klStreamsStats1 = self.get_stream_stats()
                else:
                    os = self.os
                    if os in ('ixia', 'spirent'):
                        # Ixia and Spirent do not automatically clear stats; Avoid this step to save time.
                        self.traffic_control(mode='start',
                                             ports=ports,
                                             wait=False,
                                             clear_on_start=False)
                    else:  # ('agilent', 'pagent', ...)
                        # Always clears on start
                        self.traffic_control(mode='start',
                                             ports=ports,
                                             wait=False)

                do_poll_traffic_running()
                klStreamsStats1 = None

                # }}}

            # Stop, Clear+Start, Wait RX/TX {{{

            self.traffic_control(mode='stop',
                                 ports=ports)
            if start:
                self.traffic_control(mode='start',
                                     ports=ports,
                                     wait=False,
                                     clear_on_start=clear_on_start)
                do_poll_traffic_running()

            # }}}

        else:
            logger.debug('Nothing to do.')

    def start_traffic(self, **kwargs):
        return self.traffic_control(mode='start', **kwargs)

    def stop_traffic(self, **kwargs):
        return self.traffic_control(mode='stop', **kwargs)

    def is_traffic_running(self, **kwargs):
        hltapi = self.hltapi
        tcl = hltapi.tcl
        hltkl = self.traffic_control('poll', **kwargs)
        return not tcl.cast_boolean(hltkl.stopped)

    def traffic_control(self, mode, *, ports=None, wait=True, duration=None, clear_on_start=True, stop_counting=True, **kwargs):
        hltkl = None  # Returned value

        from genie.libs.conf.device.agilent import Device as AgilentDevice
        from genie.libs.conf.device.ixia import Device as IxiaDevice
        from genie.libs.conf.device.pagent import Device as PagentDevice
        from genie.libs.conf.device.spirent import Device as SpirentDevice

        hltapi = self.hltapi
        tcl = hltapi.tcl

        if ports is None:
            ports = []
            # for mcast_gorup in self.testbed.object_instances(cls=MulticastGroup):
            #     foreach sender [enaMcastGetMcastGroupParam $vMcastGroup -senders] {
            #         lassign $sender vTgenIntf stream_id
            #         if { [enaObjIsObject $vTgenIntf stream] } { continue } ;# done below
            #         lappend ports $vTgenIntf
            #     }
            ports += [stream.source_tgen_interface
                      for stream in self.streams]

        port_handles = list(set(
            port if type(port) is str else port.tgen_port_handle
            for port in ports))

        if port_handles:
            # Let hltapi object deal with no -port_handle vs "all"
            if len(port_handles) == 1 and port_handles[0] == 'all':
                port_handles = []

            if mode == 'start':
                hltkwargs = {}
                if clear_on_start:
                    # Clear stats, if needed.
                    if isinstance(self, (IxiaDevice, SpirentDevice)):
                        self.traffic_control(mode='clear_stats', ports=['all'])
                    else:
                        pass  # No need to clear stats

                # Start traffic
                if isinstance(self, IxiaDevice):
                    hltkwargs['action'] = 'sync_run'
                    if not clear_on_start:
                        # Makes a difference in pre-ixnetwork
                        hltkwargs['action'] = 'run'
                elif isinstance(self, PagentDevice):
                    # NOTE Pagent: For streams with non-continuous transmit_mode, action should be "manual_trigger"
                    hltkwargs['action'] = 'run'
                    if not clear_on_start:
                        # Hack Pagent code to avoid "tgn clear count"
                        pass # TODO
                        # logger.debug('Disabling Pagent::traffic_control\'s "tgn clear count"')
                        # enaDestructor [xscale_save_proc ::Pagent::traffic_control]
                        # ::xscale::patch_proc_body ::Pagent::traffic_control \
                        #     {(?n).*"tgn clear count".*} \
                        #     ""
                else:
                    hltkwargs['action'] = 'run'

                if port_handles:
                    hltkwargs['port_handle'] = port_handles

                if duration is not None:
                    # NOTE: Spirent: Make sure your Spirent has patch for
                    # SR #279953571 or at least version 3.70 or else
                    # duration will be blocking
                    hltkwargs['duration'] = duration

                hltkl = hltapi.traffic_control(**hltkwargs)

                # Wait
                if wait is True:
                    if isinstance(self, SpirentDevice):
                        # action is asynchronous; poll or wait.
                        wait = 5
                    else:
                        # TBD
                        wait = 5
                if wait:
                    logger.info('Waiting %s seconds for traffic start', wait)
                    time.sleep(wait)

            elif mode == 'stop':
                # Stop traffic

                if isinstance(self, PagentDevice):
                    if not stop_counting:
                        # Hack Pagent code to avoid "pkts stop"
                        pass # TODO
                        # logger.debug('Disabling Pagent::traffic_control\'s "pkts stop"')
                        # enaDestructor [xscale_save_proc ::Pagent::traffic_control]
                        # ::xscale::patch_proc_body ::Pagent::traffic_control \
                        #     {(?n).*"pkts stop".*} \
                        #     ""

                hltkwargs = {}

                hltkwargs['action'] = 'stop'

                if port_handles:
                    hltkwargs['port_handle'] = port_handles

                if isinstance(self, SpirentDevice):
                    if int(tcl.eval('::package vcompare [::package require SpirentHltApi] 3.70')) >= 0:
                        # Tell STC HLTAPI 3.70+ to not save the EOT results database
                        hltkwargs['db_file'] = False

                # Wait
                if wait is True:
                    # Default trickle wait time for stop.
                    # It is assumed that the TGEN doesn't return until traffic
                    # is stopped. The extra wait time is mostly for packets to
                    # complete their path and stats to update.
                    wait = 2
                if wait:
                    if isinstance(self, AgilentDevice):
                        # NOTE: Agilent already has it's own trickle_time
                        if int(tcl.call('::AgtInvoke', 'AgtTestController', 'IsTrickleTimeEnabled')):
                            wait = False
                    elif isinstance(self, IxiaDevice):
                        # Without max_wait_timer, Ixia goes into asynchronous mode
                        hltkwargs['max_wait_timer'] = 10
                    else:
                        pass  # No default trickle time

                for tryno in range(1, 3):
                    try:
                        hltkl = hltapi.traffic_control(**hltkwargs)
                    except HltapiError:
                        if tryno == 1 and isinstance(self, AgilentDevice):
                            # NOTE Agilent: Could fail to stop on first try!
                            continue
                        raise
                    break

                if wait:
                    logger.info('Waiting %s seconds for traffic stop', wait)
                    time.sleep(wait)

            elif mode == 'clear_stats' or True:  # default!
                # TODO wrap -mode/action "poll"
                # No further special processing; straight HLTAPI/HLTSPL

                hltkwargs = {}

                hltkwargs['action'] = mode

                if port_handles:
                    hltkwargs['port_handle'] = port_handles

                hltkl = hltapi.traffic_control(**hltkwargs)

        else:
            logger.debug('Nothing to do.')

        return hltkl

    def start_emulation(self, **kwargs):
        pass  # TODO no emulation supported yet! raise NotImplementedError

    def stop_emulation(self, **kwargs):
        pass  # TODO no emulation supported yet! raise NotImplementedError

    def build_config(self, apply=True, attributes=None, **kwargs):
        attributes = AttributesHelper(self, attributes)

        # Don't call super().build_config

        # Nothing to do.

        return ''  # No CLI lines

    def build_unconfig(self, clean=False, apply=True, attributes=None, **kwargs):
        attributes = AttributesHelper(self, attributes)

        # Don't call super().build_unconfig

        if clean:
            pass  # TODO

        # Nothing to do.

        return ''  # No CLI lines

