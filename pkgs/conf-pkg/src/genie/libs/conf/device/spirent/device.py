'''
    Device class for HLTAPI devices with spirent OS.
'''

__all__ = (
    'Device',
    'EmulatedDevice',
)

from enum import Enum
import collections
import contextlib
import functools
import logging
import re
import statistics
import time
import types

try:
    from pyats.tcl import tclstr
    import pyats.tcl
    str_type = tclstr
except Exception:
    str_type = str

from genie.decorator import managedattribute
from genie.conf.base.attributes import AttributesHelper
import genie.conf.base.attributes

from genie.libs.conf.device.hltapi import Device as HltapiDevice
import genie.libs.conf.device
import genie.libs.conf.interface.hltapi
from genie.libs.conf.stream import Stream, StreamStats
from genie.libs.conf.base import IPv4Address, IPv6Address, MAC

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)


def try_cast_number(value):
    if type(value) in (tuple, int, float, bool):
        # Already a type recognized by Tk
        return value
    try:
        return pyats.tcl.cast_int(value)
    except (TypeError, ValueError):
        pass
    try:
        return pyats.tcl.cast_double(value)
    except (TypeError, ValueError):
        pass
    return tclstr(value)


class Device(HltapiDevice):
    '''Device class for HLTAPI devices with spirent OS'''

    class Hltapi(HltapiDevice.Hltapi):
        '''Hltapi class customized for Spirent.

        The following APIs are also provided by the HLTAPI connection:
            - stc_get(obj[, '-member'])
            - stc_config(obj, [member=value, ...])
            - stc_create(type[, member=value, ...])
            - stc_delete(obj)
            - stc_perform(action[, arg=value])
            - stc_apply()
        '''

        def traffic_config(self, **kwargs):

            # Setup persistent datasets at the first sign of traffic
            persist_data = self.device.persist_data
            if persist_data.use_stc_streamblock_stats:
                persist_data.stc_TxStreamBlockResults_resultdataset
                persist_data.stc_RxStreamBlockResults_resultdataset
            else:
                persist_data.stc_TxStreamResults_resultdataset
                persist_data.stc_RxStreamSummaryResults_resultdataset

            need_stc_apply = False
            try:

                # Supports l3_length
                try:
                    kwargs['l2_length'] = kwargs.pop('frame_size')
                except KeyError:
                    pass
                try:
                    kwargs['l2_length'] = kwargs.pop('packet_len')
                except KeyError:
                    pass
                if 'l2_length' in kwargs or 'l2_length_min' in kwargs:
                    l2_encap = kwargs.get('l2_encap', '')
                    if l2_encap in (
                            'ethernet_ii',
                            'ethernet_ii_vlan',
                            'ethernet_ii_unicast_mpls',
                            'ethernet_ii_multicast_mpls',
                            'ethernet_ii_vlan_unicast_mpls',
                            'ethernet_ii_vlan_multicast_mpls',
                            'ethernet_ii_pppoe',
                            'ethernet_ii_vlan_pppoe',
                            'ethernet_ii_qinq_pppoe',
                    ):
                        # L2 = ETH(14) [VLAN(n*4)] [MPLS(n*4)] [PPPoE(6) PPP(2)] L3 FCS(4)
                        l2_hdr_len = 18  # ETH(14) ... FCS(4)
                        if 'vlan' in l2_encap or 'qinq' in l2_encap:
                            if 'vlan_id2' in kwargs or 'vlan_id_outer' in kwargs:
                                l2_hdr_len += 8  # VLAN(2*4)
                            else:
                                l2_hdr_len += 4  # VLAN(4)
                        if 'mpls' in l2_encap:
                            l2_hdr_len += len(self.tcl.cast_list(kwargs['mpls_labels'])) * 4  # MPLS(n*4)
                        if 'pppoe' in l2_encap:
                            l2_hdr_len += 8  # PPPoE(6) PPP(2)
                    elif l2_encap in (
                        'ethernet_mac_in_mac',
                        'atm_snap',
                        'atm_snap_802.3snap',
                        'atm_snap_802.3snap_nofcs',
                        'atm_snap_ethernet_ii',
                        'atm_snap_ppp',
                        'atm_snap_pppoe',
                        'atm_llcsnap',
                        'atm_vc_mux',
                        'atm_vc_mux_802.3snap',
                        'atm_vc_mux_802.3snap_nofcs',
                        'atm_vc_mux_ethernet_ii',
                        'atm_vc_mux_ppp',
                        'atm_vc_mux_pppoe',
                        'atm_mpls',
                        'hdlc_unicast',
                        'hdlc_broadcast',
                        'hdlc_unicast_mpls',
                        'hdlc_multicast_mpls',
                        'ppp_link',
                        'cisco_framerelay',
                        'ietf_framerelay',
                        'eth',
                        'raw_l2',
                    ):
                        # TODO
                        l2_hdr_len = 18
                    else:
                        # TODO
                        l2_hdr_len = 18
                    try:
                        kwargs['l3_length'] = int(kwargs['l2_length']) - l2_hdr_len
                    except KeyError:
                        pass
                    try:
                        kwargs['l3_length_min'] = int(kwargs['l2_length_min']) - l2_hdr_len
                    except KeyError:
                        pass
                    try:
                        kwargs['l3_length_max'] = int(kwargs['l2_length_max']) - l2_hdr_len
                    except KeyError:
                        pass
                    try:
                        kwargs['l3_length_step'] = int(kwargs['l2_length_step'])
                    except KeyError:
                        pass
                    kwargs.pop('l2_length', None)
                    kwargs.pop('l2_length_min', None)
                    kwargs.pop('l2_length_max', None)
                    kwargs.pop('l2_length_step', None)

                # IPv4 steps have to be in IP format, IPv6 in integer format
                try:
                    kwargs['mac_discovery_gw_step'] = str(IPv4Address(kwargs['mac_discovery_gw_step']))
                except KeyError:
                    pass
                try:
                    kwargs['ip_src_step'] = str(IPv4Address(kwargs['ip_src_step']))
                except KeyError:
                    pass
                try:
                    kwargs['ip_dst_step'] = str(IPv4Address(kwargs['ip_dst_step']))
                except KeyError:
                    pass
                try:
                    kwargs['ipv6_src_step'] = int(IPv6Address(kwargs['ipv6_src_step']))
                except KeyError:
                    pass
                try:
                    kwargs['ipv6_dst_step'] = int(IPv6Address(kwargs['ipv6_dst_step']))
                except KeyError:
                    pass
                # MAC steps have to be in MAC format
                try:
                    kwargs['mac_src_step'] = str(MAC(kwargs['mac_src_step']))
                except KeyError:
                    pass
                try:
                    kwargs['mac_dst_step'] = str(MAC(kwargs['mac_dst_step']))
                except KeyError:
                    pass
                try:
                    kwargs['mac_src2_step'] = str(MAC(kwargs['mac_src2_step']))
                except KeyError:
                    pass
                try:
                    kwargs['mac_dst2_step'] = str(MAC(kwargs['mac_dst2_step']))
                except KeyError:
                    pass
                try:
                    kwargs['arp_src_hw_step'] = str(MAC(kwargs['arp_src_hw_step']))
                except KeyError:
                    pass
                try:
                    kwargs['arp_dst_hw_step'] = str(MAC(kwargs['arp_dst_hw_step']))
                except KeyError:
                    pass
                # Spirent HLTAPI does not support l3_protocol=none. Set to ipv4 and remote the ipv4 header later.
                remote_ipv4_header = False
                if kwargs.get('l3_protocol', None) == 'none':
                    kwargs['l3_protocol'] = 'ipv4'
                    remote_ipv4_header = True
                # Spirent HLTAPI does not support l4_protocol=none, not sending it is equivalent.
                if kwargs.get('l4_protocol', None) == 'none':
                    del kwargs['l4_protocol']
                # Spirent doesn't deactivate the "Resolve Destination MAC Address" option even when using static MAC
                disable_mac_resolver = False
                if kwargs.get('mode', None) in ('create', 'modify') \
                        and 'mac_dst' in kwargs \
                        and 'mac_discovery_gw' not in kwargs \
                        and kwargs.get('mac_dst_mode', None) != 'discovery':
                    disable_mac_resolver = True
                # mac_dst_mode discovery was introduced in STC HLTAPI 4.60 (4.62?)
                if kwargs.get('mac_dst_mode', None) == 'discovery':
                    if int(self.tcl.eval('package vcompare [package present SpirentHltApi] 4.60')) < 0:
                        # Not specifying mac_dst_mode should work if mac_dst is not specified and mac_discovery_gw is set
                        del kwargs['mac_dst_mode']
                # Extra Spirent options for MPLS
                fix_mpls_labels = False
                if 'mpls_labels' in kwargs:
                    mpls_labels_mode = kwargs.setdefault('mpls_labels_mode', 'fixed')
                    if mpls_labels_mode == 'fixed':
                        mpls_labels = self.tcl.cast_list(kwargs['mpls_labels'], item_cast=int)
                        if len(mpls_labels) > 1:
                            # Spirent HLTAPI only supports 1 MPLS label; Fix headers after create.
                            kwargs['mpls_labels'] = (mpls_labels[0],)
                            fix_mpls_labels = True

                # -type is Agilent-specific. Default should be "stream"; Anything else is not supported.
                if kwargs.get('type', None) == 'stream':
                    del kwargs['type']
                # -dut_type is Agilent-specific.
                kwargs.pop('dut_type', None)

                hltkl = self.pyats_connection.traffic_config(**kwargs)

                if 'stream_id' in hltkl:
                    streamblocks = self.tcl.cast_list(hltkl['stream_id'], item_cast=tclstr)

                    if remote_ipv4_header:
                        logger.debug('Spirent: delete IPv4 header')
                        for streamblock in streamblocks:
                            ipv4_handles = self.stc_get(streamblock, '-children-ipv4:ipv4',
                                                        cast_=functools.partial(self.tcl.cast_list, item_cast=tclstr))
                            for ipv4_handle in ipv4_handles:
                                self.stc_delete(ipv4_handle)
                                need_stc_apply = True

                    if fix_mpls_labels:
                        for streamblock in streamblocks:
                            headers = self.stc_get(streamblock, '-children',
                                                              cast_=functools.partial(self.tcl.cast_list, item_cast=tclstr))
                            # Find and remove existing mpls header
                            idx_mpls_header, mpls_header = next((idx, header) for (idx, header) in enumerate(headers) if header.startswith('mpls:'))
                            logger.debug('Spirent: delete MPLS header %r', mpls_header)
                            self.stc_delete(mpls_header)
                            need_stc_apply = True
                            # Other headers will have to be moved later
                            move_headers = headers[idx_mpls_header+1:]
                            # Create new mpls headers (at end of packet)
                            for i_mpls_label, mpls_label in enumerate(mpls_labels):
                                sBit = int(i_mpls_label == len(mpls_labels) - 1)
                                logger.debug('Spirent: append MPLS header with label %r (sBit=%r)', mpls_label, sBit)
                                self.stc_create(
                                    'mpls:Mpls', '-under', streamblock,
                                    '-sBit', sBit,
                                    '-label', mpls_label)
                                need_stc_apply = True
                            # Move other headers at the end of the packet (after mpls)
                            for header in move_headers:
                                self.stc_config(header, '-parent', '')
                                self.stc_config(header, '-parent', streamblock)
                                need_stc_apply = True

                    if disable_mac_resolver:
                        logger.debug('Spirent: disabling destination MAC resolver')
                        for streamblock in streamblocks:
                            self.stc_config(streamblock, '-EnableResolveDestMacAddress', 'false')
                            need_stc_apply = True

            finally:
                if need_stc_apply:
                    self.stc_apply()
                    need_stc_apply = False

            return hltkl

        def traffic_control(self, **kwargs):

            # Setup persistent datasets at the first sign of traffic
            persist_data = self.device.persist_data
            if persist_data.use_stc_streamblock_stats:
                persist_data.stc_TxStreamBlockResults_resultdataset
                persist_data.stc_RxStreamBlockResults_resultdataset
            else:
                persist_data.stc_TxStreamResults_resultdataset
                persist_data.stc_RxStreamSummaryResults_resultdataset

            # -port_handle is mandatory, use the Spirent-specific "all" value
            kwargs.setdefault('port_handle', ['all'])

            if kwargs.get('action', None) == 'stop':
                if int(self.tcl.eval('package vcompare [package present SpirentHltApi] 3.70')) >= 0:
                    # Tell STC HLTAPI 3.70+ to not save the EOT results database
                    # This takes a long time and fails most of the time.
                    kwargs.setdefault('db_file', 0)

            hltkl = self.pyats_connection.traffic_control(**kwargs)

            if kwargs.get('action', None) == 'poll' and 'stopped' not in hltkl:
                stopped = True
                for k, v in hltkl.items():
                    if re.match(r'^port.*-generator.*$', k):
                        if v != 'STOPPED':
                            stopped = False
                            break
                stopped = 1 if stopped else 0
                logger.debug('Spirent: setting hltkl stopped = %r', stopped)
                hltkl.stopped = stopped

            return hltkl

        @property
        def _sth_project(self):
            return tclstr(self.tcl.call('set', '{}::GBLHNDMAP(project)'.format(self.tcl_namespace)))

    class PersistData(object):

        pyats_connection = managedattribute(
            name='pyats_connection',
            type=managedattribute.auto_ref,
            gettype=managedattribute.auto_unref)

        @property
        def tcl(self):
            '''The Tcl interpreter instance.'''
            return self.pyats_connection._tcl

        @property
        def tcl_namespace(self):
            '''The Tcl namespace where HLTAPI vendor code is loaded.'''
            return self.pyats_connection._ns

        @property
        def _sth_project(self):
            return tclstr(self.tcl.call('set', '{}::GBLHNDMAP(project)'.format(self.tcl_namespace)))

        def __init__(self, pyats_connection):
            self.pyats_connection = pyats_connection
            super().__init__()

        use_stc_streamblock_stats = managedattribute(
            name='use_stc_streamblock_stats',
            default=False,
            type=managedattribute.test_istype(bool),
            doc='''If True, use STC's TxStreamBlockResults/RxStreamBlockResults
            instead of TxStreamResults/RxStreamSummaryResults.''')

        stc_TxStreamBlockResults_resultdataset = managedattribute(
            name='stc_TxStreamBlockResults_resultdataset',
            type=str_type)

        stc_RxStreamBlockResults_resultdataset = managedattribute(
            name='stc_RxStreamBlockResults_resultdataset',
            type=str_type)

        stc_TxStreamResults_resultdataset = managedattribute(
            name='stc_TxStreamResults_resultdataset',
            type=str_type)

        @stc_TxStreamResults_resultdataset.initter
        def stc_TxStreamResults_resultdataset(self):
            pyats_connection = self.pyats_connection
            tcl = self.tcl
            project = self._sth_project
            resultdatasets = pyats_connection.stc_get(
                project, '-children-ResultDataSet',
                cast_=functools.partial(tcl.cast_list, item_cast=tclstr))
            for resultdataset in resultdatasets:
                # Find existing resultdataset in session
                resultdataset_name = pyats_connection.stc_get(
                    resultdataset, '-Name',
                    cast_=tclstr)
                if resultdataset_name == 'Genie TxStreamResults':
                    break
            else:
                # Subscribe to TxStreamResults
                resultdataset = pyats_connection.stc_subscribe(
                    '-Parent', project,
                    '-ConfigType', 'StreamBlock',
                    '-ResultType', 'TxStreamResults',
                    cast_=tclstr)
                pyats_connection.stc_config(resultdataset,
                                            '-Name', 'Genie TxStreamResults',
                                            '-DisablePaging', 'false',
                                            '-RecordsPerPage', 256,
                                            )
            return resultdataset

        stc_RxStreamSummaryResults_resultdataset = managedattribute(
            name='stc_RxStreamSummaryResults_resultdataset',
            type=str_type)

        @stc_RxStreamSummaryResults_resultdataset.initter
        def stc_RxStreamSummaryResults_resultdataset(self):
            pyats_connection = self.pyats_connection
            tcl = self.tcl
            project = self._sth_project
            resultdatasets = pyats_connection.stc_get(
                project, '-children-ResultDataSet',
                cast_=functools.partial(tcl.cast_list, item_cast=tclstr))
            for resultdataset in resultdatasets:
                # Find existing resultdataset in session
                resultdataset_name = pyats_connection.stc_get(
                    resultdataset, '-Name',
                    cast_=tclstr)
                if resultdataset_name == 'Genie RxStreamSummaryResults':
                    break
            else:
                # Subscribe to RxStreamSummaryResults
                resultdataset = pyats_connection.stc_subscribe(
                    '-Parent', project,
                    '-ConfigType', 'StreamBlock',
                    '-ResultType', 'RxStreamSummaryResults',
                    cast_=tclstr)
                pyats_connection.stc_config(resultdataset,
                                            '-Name', 'Genie RxStreamSummaryResults',
                                            '-DisablePaging', 'false',
                                            '-RecordsPerPage', 256,
                                            )
            return resultdataset

    @property
    def persist_data(self):
        pyats_connection = self.hltapi.pyats_connection
        persist_data = getattr(pyats_connection, '_genie_persist_data', None)
        if not persist_data:
            persist_data = Device.PersistData(pyats_connection)
            setattr(pyats_connection, '_genie_persist_data', persist_data)
        return persist_data

    def get_stream_stats(self, streams=None, *, refresh=True):
        if streams is None:
            streams = self.find_streams()

        stats = StreamStats()

        hltapi = self.hltapi
        tcl = hltapi.tcl

        need_stc_apply = False

        map_streamblock_to_stream_obj = {}
        for stream in streams:
            streamblocks = stream.tgen_handle
            if streamblocks:
                for streamblock in streamblocks:
                    assert streamblock not in map_streamblock_to_stream_obj
                    map_streamblock_to_stream_obj[streamblock] = stream
            else:
                logger.warn('%r: Nothing to do (no tgen_handle).', stream)

        streamblocks = list(map_streamblock_to_stream_obj.keys())
        if streamblocks:

            # set tx_resultdataset/rx_resultdataset
            if self.persist_data.use_stc_streamblock_stats:
                tx_resultdataset = self.persist_data.stc_TxStreamBlockResults_resultdataset
                rx_resultdataset = self.persist_data.stc_RxStreamBlockResults_resultdataset
                if refresh:
                    # NOTE:
                    #   TxStreamBlockResults and RxStreamBlockResults are for end of test results.
                    #   You must use RefreshResultViewCommand before you can access the results.
                    hltapi.stc_perform('RefreshResultViewCommand',
                                       '-ResultDataSet', tx_resultdataset,
                                       '-ExecuteSynchronous', 'TRUE')
                    hltapi.stc_perform('RefreshResultViewCommand',
                                       '-ResultDataSet', rx_resultdataset,
                                       '-ExecuteSynchronous', 'TRUE')
                    refresh = False
            else:
                tx_resultdataset = self.persist_data.stc_TxStreamResults_resultdataset
                rx_resultdataset = self.persist_data.stc_RxStreamSummaryResults_resultdataset

            tx_resultdataset_dict = hltapi.stc_get(tx_resultdataset,
                                                   cast_=functools.partial(tcl.cast_array, item_cast=tcl.cast_any))
            logger.debug('tx_resultdataset_dict=%r', tx_resultdataset_dict)
            rx_resultdataset_dict = hltapi.stc_get(rx_resultdataset,
                                                   cast_=functools.partial(tcl.cast_array, item_cast=tcl.cast_any))
            logger.debug('rx_resultdataset_dict=%r', rx_resultdataset_dict)
            n_tx_pages_todo = tx_resultdataset_dict['-TotalPageCount']
            n_rx_pages_todo = rx_resultdataset_dict['-TotalPageCount']
            arr_tx_streamresults_dicts_per_streamblock = collections.defaultdict(list)
            arr_rx_streamresults_dicts_per_streamblock = collections.defaultdict(list)
            arr_rxstreamportresult_dict = {}
            for page_iter in range(1, max(n_tx_pages_todo, n_rx_pages_todo) + 1):
                # Change pages
                bPageChanged = False
                try:
                    if True:
                        # Always read pages in the same order (1..n) so that
                        # results are more consistent.
                        if page_iter <= n_tx_pages_todo \
                                and page_iter != tx_resultdataset_dict['-PageNumber']:
                            hltapi.stc_config(tx_resultdataset, '-PageNumber', page_iter)
                            need_stc_apply = True
                            tx_resultdataset_dict['-PageNumber'] = page_iter
                            bPageChanged = True
                        if page_iter <= n_rx_pages_todo \
                                and page_iter != rx_resultdataset_dict['-PageNumber']:
                            hltapi.stc_config(rx_resultdataset, '-PageNumber', page_iter)
                            need_stc_apply = True
                            rx_resultdataset_dict['-PageNumber'] = page_iter
                            bPageChanged = True
                    else:
                        # Only change page if necessary. This saves 1 sleep of 2
                        # seconds per cycle but never reads in the same order
                        # (1,2,3; 2,3,1; 3,1,2; ...)
                        if page_iter > 1:
                            if page_iter <= n_tx_pages_todo:
                                PageNumber = tx_resultdataset_dict['-PageNumber'] \
                                    % tx_resultdataset_dict['-TotalPageCount'] + 1
                                hltapi.stc_config(tx_resultdataset, '-PageNumber', PageNumber)
                                need_stc_apply = True
                                tx_resultdataset_dict['-PageNumber'] = PageNumber
                                bPageChanged = True
                            if page_iter <= n_rx_pages_todo:
                                PageNumber = rx_resultdataset_dict['-PageNumber'] \
                                    % rx_resultdataset_dict['-TotalPageCount'] + 1
                                hltapi.stc_config(rx_resultdataset, '-PageNumber', PageNumber)
                                need_stc_apply = True
                                rx_resultdataset_dict['-PageNumber'] = PageNumber
                                bPageChanged = True
                finally:
                    if need_stc_apply:
                        hltapi.stc_apply()
                        need_stc_apply = False
                if bPageChanged or refresh:
                    if True:
                        # Until proven otherwise, RefreshResultViewCommand should be sufficient even on page change.
                        if page_iter <= n_tx_pages_todo:
                            hltapi.stc_perform('RefreshResultViewCommand',
                                               '-ResultDataSet', tx_resultdataset,
                                               '-ExecuteSynchronous', 'TRUE')
                        if page_iter <= n_rx_pages_todo:
                            hltapi.stc_perform('RefreshResultViewCommand',
                                               '-ResultDataSet', rx_resultdataset,
                                               '-ExecuteSynchronous', 'TRUE')
                    elif bPageChanged:
                        logger.info('Waiting 2 seconds for STC result update after page change')
                        time.sleep(2)

                # Collect results
                if page_iter <= n_tx_pages_todo:
                    logger.debug('%s: Fetching TX stream results page %d of %d...', self, tx_resultdataset_dict['-PageNumber'], tx_resultdataset_dict['-TotalPageCount'])
                    for txstreamresults in hltapi.stc_get(tx_resultdataset, '-ResultHandleList',
                                                          cast_=functools.partial(tcl.cast_list, item_cast=tclstr)):
                        txstreamstats = hltapi.stc_get(txstreamresults,
                                                       cast_=functools.partial(tcl.cast_array, item_cast=try_cast_number))
                        logger.debug('txstreamstats (%s): %r', txstreamresults, txstreamstats)
                        streamblock = txstreamstats['-parent']
                        if streamblock not in streamblocks:
                            continue
                        arr_tx_streamresults_dicts_per_streamblock[streamblock].append(txstreamstats)
                if page_iter <= n_rx_pages_todo:
                    logger.debug('%s: Fetching RX stream results page %d of %d...', self, rx_resultdataset_dict['-PageNumber'], rx_resultdataset_dict['-TotalPageCount'])
                    for rxstreamresults in hltapi.stc_get(rx_resultdataset, '-ResultHandleList',
                                                          cast_=functools.partial(tcl.cast_list, item_cast=tclstr)):
                        rxstreamstats = hltapi.stc_get(rxstreamresults,
                                                       cast_=functools.partial(tcl.cast_array, item_cast=try_cast_number))
                        logger.debug('rxstreamstats (%s): %r', rxstreamresults, rxstreamstats)
                        streamblock = rxstreamstats['-parent']
                        if streamblock not in streamblocks:
                            continue
                        if self.persist_data.use_stc_streamblock_stats:
                            rxstreamportresults = rxstreamstats.get('-summaryresultchild-Targets', ())  # [-1]?
                        else:
                            rxstreamportresults = rxstreamstats.get('-resultchild-Targets', ())  # [-1]?
                        rxstreamportresults = tcl.cast_list(rxstreamportresults, item_cast=tclstr)
                        for rxstreamportresult in rxstreamportresults:
                            rxstreamportstats = hltapi.stc_get(rxstreamportresult,
                                                               cast_=functools.partial(tcl.cast_array, item_cast=try_cast_number))
                            logger.debug('rxstreamportstats (%s): %r', rxstreamportresult, rxstreamportstats)
                            arr_rxstreamportresult_dict[rxstreamportresult] = rxstreamportstats
                        arr_rx_streamresults_dicts_per_streamblock[streamblock].append(rxstreamstats)

            for streamblock in streamblocks:
                stream = map_streamblock_to_stream_obj[streamblock]
                stream_stats = stats.by_stream[stream] = StreamStats.ByStreamStats()
                stcstatstx = collections.defaultdict(list)
                stcstatsrx = collections.defaultdict(list)
                stc_StreamId_to_TxStreamIndex = {}
                rx_interfaces = set()

                # Fetch statistics
                StreamIndexes = set()
                for txstreamstats in arr_tx_streamresults_dicts_per_streamblock[streamblock]:
                    for k, v in txstreamstats.items():
                        stcstatstx[k].append(v)
                    StreamIndex = int(tcl.cast_list(stcstatstx['-StreamIndex'])[-1])
                    StreamIndexes.add(StreamIndex)
                    StreamId = int(tcl.cast_list(stcstatstx['-StreamId'])[-1])
                    stc_StreamId_to_TxStreamIndex[StreamId] = StreamIndex
                    for k, v in txstreamstats.items():
                        stcstatstx[(StreamIndex, k)].append(v)
                for rxstreamstats in arr_rx_streamresults_dicts_per_streamblock[streamblock]:
                    for k, v in rxstreamstats.items():
                        stcstatsrx[k].append(v)
                    StreamId = int(tcl.cast_list(stcstatsrx['-Comp32'])[-1])
                    if StreamId:
                        StreamIndex = stc_StreamId_to_TxStreamIndex[StreamId]
                    else:
                        StreamIndex = int(tcl.cast_list(stcstatsrx['-StreamIndex'])[-1])
                    StreamIndexes.add(StreamIndex)
                    for k, v in rxstreamstats.items():
                        stcstatsrx[(StreamIndex, v)].append(v)
                    if self.persist_data.use_stc_streamblock_stats:
                        rxstreamportresults = rxstreamstats.get('-summaryresultchild-Targets', ())  # [-1]?
                    else:
                        rxstreamportresults = rxstreamstats.get('-resultchild-Targets', ())  # [-1]?
                    rxstreamportresults = tcl.cast_list(rxstreamportresults, item_cast=tclstr)
                    for rxstreamportresult in rxstreamportresults:
                        rxstreamstats = arr_rxstreamportresult_dict[rxstreamportresult]
                        analyzer = rxstreamstats['-parent']
                        port = hltapi.stc_get(analyzer, '-parent',
                                              cast_=tclstr)
                        for rx_interface in self.tgen_port_interfaces:
                            if rx_interface.tgen_port_handle != port:
                                continue
                            rx_interfaces.add(rx_interface)
                            for k, v in rxstreamstats.items():
                                stcstatsrx[(rx_interface, k)].append(v)
                            # #lappend StreamIndexes [set StreamIndex [if { [set StreamId [lindex $stcstatsrx($rx_interface,-Comp32) end]] } { set stc_StreamId_to_TxStreamIndex($StreamId) } else { lindex $stcstatsrx($rx_interface,-StreamIndex) end }]]
                            for k, v in rxstreamstats.items():
                                stcstatsrx[(rx_interface, StreamIndex, k)].append(v)
                            break

                # Don't collect sub-stream information if there are none (only 1)
                if len(StreamIndexes) == 1:
                    StreamIndexes = set()
                StreamIndexes = sorted(StreamIndexes)
                StreamIndexes.append(None)
                # enaLogVerify -debug [enaTbArrayPrint stcstatstx] ; enaLogVerify -debug [enaTbArrayPrint stcstatsrx]
                for StreamIndex in StreamIndexes:

                    # TX

                    sub_stream_stats = stream_stats.tx
                    if StreamIndex is None:
                        asub = lambda x: x
                    else:
                        sub_stream_stats = sub_stream_stats.by_sub_stream[StreamIndex] = StreamStats.BySubStreamTxStats()
                        asub = lambda x: (StreamIndex, x)

                    # Example stcstatstx
                    #   stcstatstx(-Active)               = true
                    #   stcstatstx(-BitCount)             = 1869824
                    #   stcstatstx(-BitRate)              = 8600
                    #   stcstatstx(-BlockId)              = 0
                    #   stcstatstx(-CellCount)            = 0
                    #   stcstatstx(-CellRate)             = 0
                    #   stcstatstx(-CounterTimestamp)     = 0
                    #   stcstatstx(-ExpectedRxFrameCount) = 1826
                    #   stcstatstx(-FrameCount)           = 1826
                    #   stcstatstx(-FrameRate)            = 8
                    #   stcstatstx(-L1BitCount)           = 2161984
                    #   stcstatstx(-L1BitRate)            = 9946
                    #   stcstatstx(-Name)                 =
                    #   stcstatstx(-OctetCount)           = 233728
                    #   stcstatstx(-OctetRate)            = 1075
                    #   stcstatstx(-parent)               = streamblock2
                    #   stcstatstx(-resultchild-Sources)  = streamblock2 resultdataset26
                    #   stcstatstx(-StreamId)             = 327681
                    #   stcstatstx(-StreamIndex)          = 1
                    if not self.persist_data.use_stc_streamblock_stats:
                        # XXXJST These are always 0 when using stream block stats
                        sub_stream_stats.total_pkt_bits = sum(stcstatstx[asub('-L1BitCount')])
                        sub_stream_stats.total_pkt_bit_rate = sum(stcstatstx[asub('-L1BitRate')])
                        sub_stream_stats.total_pkt_rate = sum(stcstatstx[asub('-FrameRate')])
                    sub_stream_stats.total_pkt_bytes = sum(stcstatstx[asub('-OctetCount')])
                    sub_stream_stats.total_pkt_byte_rate = sum(stcstatstx[asub('-OctetRate')])
                    sub_stream_stats.total_pkts = sum(stcstatstx[asub('-FrameCount')])

                    # RX

                    sub_stream_stats = stream_stats.rx
                    if StreamIndex is None:
                        asub = lambda x: x
                    else:
                        sub_stream_stats = sub_stream_stats.by_sub_stream[StreamIndex] = StreamStats.BySubStreamTxStats()
                        asub = lambda x: (StreamIndex, x)

                    # Example stcstatsrx
                    #   stcstatsrx(-Active)                       = true
                    #   stcstatsrx(-AvgInterarrivalTime)          = 0
                    #   stcstatsrx(-AvgJitter)                    = 0
                    #   stcstatsrx(-AvgLatency)                   = 86.231
                    #   stcstatsrx(-BitCount)                     = 11740160
                    #   stcstatsrx(-BitRate)                      = 8536
                    #   stcstatsrx(-CellCount)                    = 0
                    #   stcstatsrx(-CellRate)                     = 0
                    #   stcstatsrx(-Comp16_1)                     = 0
                    #   stcstatsrx(-Comp16_2)                     = 0
                    #   stcstatsrx(-Comp16_3)                     = 0
                    #   stcstatsrx(-Comp16_4)                     = 0
                    #   stcstatsrx(-Comp32)                       = 327680
                    #   stcstatsrx(-CounterTimestamp)             = 0
                    #   stcstatsrx(-DroppedFrameCount)            = 74
                    #   stcstatsrx(-DroppedFramePercent)          = 0.641
                    #   stcstatsrx(-DroppedFramePercentRate)      = 0
                    #   stcstatsrx(-DroppedFrameRate)             = 0
                    #   stcstatsrx(-DuplicateFrameCount)          = 0
                    #   stcstatsrx(-DuplicateFrameRate)           = 0
                    #   stcstatsrx(-ExpectedSeqNum)               = 0
                    #   stcstatsrx(-FcsErrorFrameCount)           = 0
                    #   stcstatsrx(-FcsErrorFrameRate)            = 0
                    #   stcstatsrx(-FirstArrivalTime)             = 0
                    #   stcstatsrx(-FrameCount)                   = 11465
                    #   stcstatsrx(-FrameRate)                    = 8
                    #   stcstatsrx(-HistBin1Count)                = 0
                    #   stcstatsrx(-HistBin1Name)                 = x < 2
                    #   stcstatsrx(-HistBin1Rate)                 = 0
                    #   stcstatsrx(-HistBin2Count)                = 0
                    #   stcstatsrx(-HistBin2Name)                 = 2 <= x < 6
                    #   stcstatsrx(-HistBin2Rate)                 = 0
                    #   stcstatsrx(-HistBin3Count)                = 0
                    #   stcstatsrx(-HistBin3Name)                 = 6 <= x < 14
                    #   stcstatsrx(-HistBin3Rate)                 = 0
                    #   stcstatsrx(-HistBin4Count)                = 0
                    #   stcstatsrx(-HistBin4Name)                 = 14 <= x < 30
                    #   stcstatsrx(-HistBin4Rate)                 = 0
                    #   stcstatsrx(-HistBin5Count)                = 0
                    #   stcstatsrx(-HistBin5Name)                 = 30 <= x < 62
                    #   stcstatsrx(-HistBin5Rate)                 = 0
                    #   stcstatsrx(-HistBin6Count)                = 0
                    #   stcstatsrx(-HistBin6Name)                 = 62 <= x < 126
                    #   stcstatsrx(-HistBin6Rate)                 = 0
                    #   stcstatsrx(-HistBin7Count)                = 0
                    #   stcstatsrx(-HistBin7Name)                 = 126 <= x < 254
                    #   stcstatsrx(-HistBin7Rate)                 = 0
                    #   stcstatsrx(-HistBin8Count)                = 0
                    #   stcstatsrx(-HistBin8Name)                 = 254 <= x < 510
                    #   stcstatsrx(-HistBin8Rate)                 = 0
                    #   stcstatsrx(-HistBin9Count)                = 0
                    #   stcstatsrx(-HistBin9Name)                 = 510 <= x < 1022
                    #   stcstatsrx(-HistBin9Rate)                 = 0
                    #   stcstatsrx(-HistBin10Count)               = 0
                    #   stcstatsrx(-HistBin10Name)                = 1022 <= x < 2046
                    #   stcstatsrx(-HistBin10Rate)                = 0
                    #   stcstatsrx(-HistBin11Count)               = 0
                    #   stcstatsrx(-HistBin11Name)                = 2046 <= x < 4094
                    #   stcstatsrx(-HistBin11Rate)                = 0
                    #   stcstatsrx(-HistBin12Count)               = 0
                    #   stcstatsrx(-HistBin12Name)                = 4094 <= x < 8190
                    #   stcstatsrx(-HistBin12Rate)                = 0
                    #   stcstatsrx(-HistBin13Count)               = 0
                    #   stcstatsrx(-HistBin13Name)                = 8190 <= x < 16382
                    #   stcstatsrx(-HistBin13Rate)                = 0
                    #   stcstatsrx(-HistBin14Count)               = 0
                    #   stcstatsrx(-HistBin14Name)                = 16382 <= x < 32766
                    #   stcstatsrx(-HistBin14Rate)                = 0
                    #   stcstatsrx(-HistBin15Count)               = 0
                    #   stcstatsrx(-HistBin15Name)                = 32766 <= x < 65534
                    #   stcstatsrx(-HistBin15Rate)                = 0
                    #   stcstatsrx(-HistBin16Count)               = 0
                    #   stcstatsrx(-HistBin16Name)                = x >= 65534
                    #   stcstatsrx(-HistBin16Rate)                = 0
                    #   stcstatsrx(-InOrderFrameCount)            = 11465
                    #   stcstatsrx(-InOrderFrameRate)             = 8
                    #   stcstatsrx(-InSeqFrameCount)              = 0
                    #   stcstatsrx(-InSeqFrameRate)               = 0
                    #   stcstatsrx(-Ipv4ChecksumErrorCount)       = 0
                    #   stcstatsrx(-Ipv4ChecksumErrorRate)        = 0
                    #   stcstatsrx(-L1BitCount)                   = 13574560
                    #   stcstatsrx(-L1BitRate)                    = 9867
                    #   stcstatsrx(-LastArrivalTime)              = 0
                    #   stcstatsrx(-LastSeqNum)                   = 0
                    #   stcstatsrx(-LateFrameCount)               = 0
                    #   stcstatsrx(-LateFrameRate)                = 0
                    #   stcstatsrx(-MaxFrameLength)               = 0
                    #   stcstatsrx(-MaxInterarrivalTime)          = 0
                    #   stcstatsrx(-MaxJitter)                    = 0
                    #   stcstatsrx(-MaxLatency)                   = 119.08
                    #   stcstatsrx(-MinFrameLength)               = 0
                    #   stcstatsrx(-MinInterarrivalTime)          = 0
                    #   stcstatsrx(-MinJitter)                    = 0
                    #   stcstatsrx(-MinLatency)                   = 53.89
                    #   stcstatsrx(-Name)                         =
                    #   stcstatsrx(-OctetCount)                   = 1467520
                    #   stcstatsrx(-OctetRate)                    = 1067
                    #   stcstatsrx(-OutSeqFrameCount)             = 0
                    #   stcstatsrx(-OutSeqFrameRate)              = 0
                    #   stcstatsrx(-parent)                       = streamblock1
                    #   stcstatsrx(-PortStrayFrames)              = NA
                    #   stcstatsrx(-PrbsBitErrorCount)            = 0
                    #   stcstatsrx(-PrbsBitErrorRate)             = 0
                    #   stcstatsrx(-PrbsBitErrorRatio)            = 0
                    #   stcstatsrx(-PrbsErrorFrameCount)          = 0
                    #   stcstatsrx(-PrbsErrorFrameRate)           = 0
                    #   stcstatsrx(-PrbsFillOctetCount)           = 0
                    #   stcstatsrx(-PrbsFillOctetRate)            = 0
                    #   stcstatsrx(-ReorderedFrameCount)          = 0
                    #   stcstatsrx(-ReorderedFrameRate)           = 0
                    #   stcstatsrx(-resultchild-Sources)          = streamblock1 resultdataset25
                    #   stcstatsrx(-resultchild-Targets)          = rxstreamresults4
                    #   stcstatsrx(-Rfc4689AbsoluteAvgJitter)     = 0
                    #   stcstatsrx(-SeqRunLength)                 = 0
                    #   stcstatsrx(-ShortTermAvgInterarrivalTime) = 0
                    #   stcstatsrx(-ShortTermAvgJitter)           = 0
                    #   stcstatsrx(-ShortTermAvgLatency)          = 95.016
                    #   stcstatsrx(-SigFrameCount)                = 11465
                    #   stcstatsrx(-SigFrameRate)                 = 8
                    #   stcstatsrx(-StreamIndex)                  = 0
                    #   stcstatsrx(-summaryresultchild-Targets)   = rxstreamresults4
                    #   stcstatsrx(-TcpUdpChecksumErrorCount)     = 0
                    #   stcstatsrx(-TcpUdpChecksumErrorRate)      = 0
                    #   stcstatsrx(-TotalInterarrivalTime)        = 0
                    #   stcstatsrx(-TotalJitter)                  = 0
                    #   stcstatsrx(-TotalJitterRate)              = 0
                    if asub('-OctetCount') in stcstatsrx:
                        sub_stream_stats.total_pkt_bytes = sum(stcstatsrx[asub('-OctetCount')])
                        sub_stream_stats.total_pkts = sum(stcstatsrx[asub('-FrameCount')])
                        sub_stream_stats.min_delay = min(stcstatsrx[asub('-MinLatency')])
                        sub_stream_stats.max_delay = max(stcstatsrx[asub('-MaxLatency')])
                        # AvgLatency could be "N/A"
                        try:
                            sub_stream_stats.avg_delay = statistics.mean(stcstatsrx[asub('-AvgLatency')])
                        except TypeError:
                            pass
                        sub_stream_stats.out_of_sequence_pkts = sum(stcstatsrx[asub('-OutSeqFrameCount')])
                        sub_stream_stats.out_of_sequence_pkt_rate = sum(stcstatsrx[asub('-OutSeqFrameRate')])
                        # XXXJST These are extensions from the Advanced Sequence Checker and may not be always reliable; For example, x_adv_seq_dropped_pkts is only calculated between 2 received frames; It does not count initial or final drops!
                        sub_stream_stats.x_adv_seq_in_order_pkts = sum(stcstatsrx[asub('-InOrderFrameCount')])
                        sub_stream_stats.x_adv_seq_in_order_pkt_rate = sum(stcstatsrx[asub('-InOrderFrameRate')])
                        sub_stream_stats.x_adv_seq_reordered_pkts = sum(stcstatsrx[asub('-ReorderedFrameCount')])
                        sub_stream_stats.x_adv_seq_reordered_pkt_rate = sum(stcstatsrx[asub('-ReorderedFrameRate')])
                        sub_stream_stats.x_adv_seq_late_pkts = sum(stcstatsrx[asub('-LateFrameCount')])
                        sub_stream_stats.x_adv_seq_late_pkt_rate = sum(stcstatsrx[asub('-LateFrameRate')])
                        sub_stream_stats.x_adv_seq_duplicate_pkts = sum(stcstatsrx[asub('-DuplicateFrameCount')])
                        sub_stream_stats.x_adv_seq_duplicate_pkt_rate = sum(stcstatsrx[asub('-DuplicateFrameRate')])
                        sub_stream_stats.x_adv_seq_dropped_pkts = sum(stcstatsrx[asub('-DroppedFrameCount')])
                        sub_stream_stats.x_adv_seq_dropped_pkt_rate = sum(stcstatsrx[asub('-DroppedFrameRate')])
                        PortStrayFrames = stcstatsrx.get(asub('-PortStrayFrames'), ['NA'])[0]
                        if PortStrayFrames == 'YES':
                            sub_stream_stats.x_has_port_stray_pkts = True
                        elif PortStrayFrames == 'NO':
                            sub_stream_stats.x_has_port_stray_pkts = False
                        if not self.persist_data.use_stc_streamblock_stats:
                            # XXXJST These are always 0 when using stream block stats
                            sub_stream_stats.total_pkt_bits = sum(stcstatsrx[asub('-L1BitCount')])
                            sub_stream_stats.total_pkt_bit_rate = sum(stcstatsrx[asub('-L1BitRate')])
                            sub_stream_stats.total_pkt_byte_rate = sum(stcstatsrx[asub('-OctetRate')])
                            sub_stream_stats.total_pkt_rate = sum(stcstatsrx[asub('-FrameRate')])
                        for rx_interface in rx_interfaces:
                            if rx_interface not in stream_stats.by_interface:
                                stream_stats.by_interface[rx_interface] = StreamStats.ByInterfaceStreamStats()
                            intf_sub_stream_stats = stream_stats.by_interface[rx_interface].rx
                            if StreamIndex is None:
                                asubi = lambda intf, x: (intf, x)
                            else:
                                intf_sub_stream_stats = intf_sub_stream_stats.by_sub_stream[StreamIndex] = StreamStats.BySubStreamTxStats()
                                asubi = lambda intf, x: (intf, StreamIndex, x)
                            if asubi(rx_interface, '-OctetCount') in stcstatsrx:
                                intf_sub_stream_stats.total_pkt_bytes = sum(stcstatsrx[asubi(rx_interface, '-OctetCount')])
                                intf_sub_stream_stats.total_pkts = sum(stcstatsrx[asubi(rx_interface, '-FrameCount')])
                                intf_sub_stream_stats.min_delay = min(stcstatsrx[asubi(rx_interface, '-MinLatency')])
                                intf_sub_stream_stats.max_delay = min(stcstatsrx[asubi(rx_interface, '-MaxLatency')])
                                # AvgLatency could be "N/A"
                                try:
                                    intf_sub_stream_stats.avg_delay = statistics.mean(stcstatsrx[asubi(rx_interface, '-AvgLatency')])
                                except TypeError:
                                    pass
                                # XXXJST These are extensions from the Advanced Sequence Checker and may not be always reliable; For example, x_adv_seq_dropped_pkts is only calculated between 2 received frames; It does not count initial or final drops!
                                intf_sub_stream_stats.x_adv_seq_in_order_pkts = sum(stcstatsrx[asubi(rx_interface, '-InOrderFrameCount')])
                                intf_sub_stream_stats.x_adv_seq_reordered_pkts = sum(stcstatsrx[asubi(rx_interface, '-ReorderedFrameCount')])
                                intf_sub_stream_stats.x_adv_seq_late_pkts = sum(stcstatsrx[asubi(rx_interface, '-LateFrameCount')])
                                intf_sub_stream_stats.x_adv_seq_duplicate_pkts = sum(stcstatsrx[asubi(rx_interface, '-DuplicateFrameCount')])
                                intf_sub_stream_stats.x_adv_seq_dropped_pkts = sum(stcstatsrx[asubi(rx_interface, '-DroppedFrameCount')])
                                PortStrayFrames = stcstatsrx.get(asubi(rx_interface, '-PortStrayFrames'), ['NA'])[0]
                                if PortStrayFrames == 'YES':
                                    intf_sub_stream_stats.x_has_port_stray_pkts = True
                                elif PortStrayFrames == 'NO':
                                    intf_sub_stream_stats.x_has_port_stray_pkts = False
                                if not self.persist_data.use_stc_streamblock_stats:
                                    intf_sub_stream_stats.total_pkt_bits = sum(stcstatsrx[asubi(rx_interface, '-L1BitCount')])
                                    intf_sub_stream_stats.total_pkt_bit_rate = sum(stcstatsrx[asubi(rx_interface, '-L1BitRate')])
                                    intf_sub_stream_stats.total_pkt_byte_rate = sum(stcstatsrx[asubi(rx_interface, '-OctetRate')])
                                    intf_sub_stream_stats.total_pkt_rate = sum(stcstatsrx[asubi(rx_interface, '-FrameRate')])

                try:
                    if self.persist_data.use_stc_streamblock_stats:
                        stream_stats.elapsed_time = stream_stats.tx.total_pkt_bytes / stream_stats.tx.total_pkt_byte_rate
                    else:
                        stream_stats.elapsed_time = stream_stats.tx.total_pkt_bits / stream_stats.tx.total_pkt_bit_rate
                except ZeroDivisionError:
                    stream_stats.elapsed_time = 0
                tx_interface = stream.source_tgen_interface
                if tx_interface not in stream_stats.by_interface:
                    stream_stats.by_interface[tx_interface] = StreamStats.ByInterfaceStreamStats()
                stream_stats.by_interface[tx_interface]._tx = stream_stats.tx

        return stats

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    arp_nd_auto_arp = managedattribute(
        name='arp_nd_auto_arp',
        default=True,
        type=(None, managedattribute.test_istype(bool)),
        doc='''Whether to resolve IPv4 or IPv6 addresses before transmitting.

        For emulated hosts and routers, once ARP has been resolved, it will not be resolved again.
        For stream blocks, ARP will be resolved each time before transmitting, even if it has already
        been resolved.
        ''')

    arp_nd_cyclic = managedattribute(
        name='arp_nd_cyclic',
        default=True,
        type=(None, managedattribute.test_istype(bool)),
        doc='''Enable Cyclic ARP/ND: Enable cyclic ARP/ND if you want to seed the DUT's ARP cache with the source IP and MAC addresses.

        When Cyclic ARP/ND is enabled, and a variable field definition (VFD) is specified on the source IP address, the number of APR/ND requests sent by Spirent TestCenter matches the VFD count on the source IP address.

        If this option is disabled, only one ARP/ND request is sent.
        ''')

    arp_nd_duplicate_gw_detection = managedattribute(
        name='arp_nd_duplicate_gw_detection',
        default=True,
        type=(None, managedattribute.test_istype(bool)),
        doc='''Enable ARP/ND Suppression for Duplicate Gateways: Available when cyclic ARP is enabled.

        Select this option to suppress ARP requests if all destinations are reachable through the same gateway.

        Enabling this option generates one ARP request, if:
            - cyclic ARP is enabled
            - a VFD is specified on the source IP address
            - a VFD is specified on the destination IP address
            - a valid gateway is specified

        Disable this option to default to the cyclic ARP case: the number of ARP requests sent matches the VFD count on the source IP address.''')

    collect_stray_frames = managedattribute(
        name='collect_stray_frames',
        default=True,
        type=(None, managedattribute.test_istype(bool)))

    def build_config(self, apply=True, attributes=None, **kwargs):
        attributes = AttributesHelper(self, attributes)

        hltapi = self.hltapi
        tcl = hltapi.tcl

        need_stc_apply = False
        try:

            arp_nd_config_kwargs = {}

            v = attributes.value('arp_nd_auto_arp')
            if v is not None:
                arp_nd_config_kwargs['auto_arp_enable'] = 'true' if v else 'false'

            v = attributes.value('arp_nd_cyclic')
            if v is not None:
                arp_nd_config_kwargs['cyclic_arp_enable'] = 'true' if v else 'false'

            v = attributes.value('arp_nd_duplicate_gw_detection')
            if v is not None:
                arp_nd_config_kwargs['duplicate_gw_detection'] = 'true' if v else 'false'

            if arp_nd_config_kwargs:
                hltapi.arp_nd_config(**arp_nd_config_kwargs)

            resultoptions_kwargs = {}

            v = attributes.value('collect_stray_frames')
            if v is not None:
                resultoptions_kwargs['CollectStrayFrame'] = 'true' if v else 'false'

            if resultoptions_kwargs:
                resultoptions, = hltapi.stc_get(
                    hltapi._sth_project,
                    '-children-ResultOptions',
                    cast_=functools.partial(tcl.cast_list, item_cast=tclstr))
                hltapi.stc_config(resultoptions, **resultoptions_kwargs)
                need_stc_apply = True

        finally:
            if need_stc_apply:
                hltapi.stc_apply()
                need_stc_apply = False

        return super().build_config(apply=apply, attributes=attributes)

    def build_unconfig(self, clean=False, apply=True, attributes=None, **kwargs):


        # Don't call super().build_unconfig
        if clean:
            pass  # TODO


        # Nothing to do.
        return super().build_unconfig(clean=clean, apply=apply, attributes=attributes, **kwargs)

    @contextlib.contextmanager
    def defer_apply_context(self):
        '''A context during which low-level apply calls are deferred.'''
        hltapi = self.hltapi
        tcl = hltapi.tcl
        if int(tcl.eval('''expr {
            [info exists ::sth::sthCore::optimization] &&
            !$::sth::sthCore::optimization
                        }''')):
            hltapi.test_control(action='enable')
            yield
            hltapi.test_control(action='disable')
            hltapi.test_control(action='sync')
        else:
            yield  # no-op

    def get_stream_resolved_mac_addresses(self, streams=None, update_cache=True):

        if streams is None:
            streams = self.find_streams()

        hltapi = self.hltapi
        tcl = hltapi.tcl

        mac_addresses_by_stream = collections.defaultdict(list)

        map_tgen_interface_to_stream_objs = collections.defaultdict(set)
        for stream in streams:
            map_tgen_interface_to_stream_objs[stream.source_tgen_interface].add(stream)

        if update_cache and map_tgen_interface_to_stream_objs:
            hltapi.stc_perform('ArpNdUpdateArpCacheCommand',
                               HandleList=tuple(tgen_interface.port_handle
                                                for tgen_interface in map_tgen_interface_to_stream_objs.keys()))

        for tgen_interface, port_streams in map_tgen_interface_to_stream_objs.items():
            map_name_to_stream = {stream.name: stream
                                  for stream in port_streams}

            arp_cache = tgen_interface.get_arp_cache(update_cache=False)
            for arp_entry in arp_cache:
                stream_name = re.sub(r' :\d+$', '', arp_entry.object_name)
                try:
                    stream = map_name_to_stream[stream_name]
                except KeyError:
                    continue
                mac_addresses_by_stream[stream].append(arp_entry)

        raise types.SimpleNamespace(by_stream=mac_addresses_by_stream)


class EmulatedDevice(genie.libs.conf.device.EmulatedDevice):

    def __init__(self, name, *, tgen_interface, **kwargs):
        super().__init__(name=name, tgen_interface=tgen_interface, **kwargs)

    def build_config(self, *, apply=True, **kwargs):

        if self.tgen_handle is not None:
            # TODO support modifying values
            logger.warn('%r: Nothing to do (already configured).', self)
            return ''

        assert self.tgen_port_handle

        tgen_device = self.tgen_device
        hltapi = tgen_device.hltapi
        tcl = hltapi.tcl

        emulated_interface = self.emulated_interface
        emulated_loopback = self.emulated_loopback

        self.tgen_handle = hltapi.stc_create(
            'EmulatedDevice',
            '-under', hltapi._sth_project,
            #'-DeviceCount', 1,
            '-EnablePingResponse', 'TRUE',
            #'-ReadOnly', 'FALSE',
            #'-Active', 'TRUE',
            #'-LocalActive', 'TRUE',
            '-Name', self.name)

        if emulated_loopback and emulated_loopback.ipv4:
            hltapi.stc_config(
                self.tgen_handle,
                '-RouterId', emulated_loopback.ipv4.ip,
                #'-RouterIdStep', '0.0.0.1',
            )

        if emulated_loopback and emulated_loopback.ipv6:
            hltapi.stc_config(
                self.tgen_handle,
                '-Ipv6RouterId', emulated_loopback.ipv6.ip,
                #'-Ipv6RouterIdStep', '::1',
            )

        hltapi.stc_config(self.tgen_port_handle,
                          '-AffiliationPort-sources',
                          hltapi.stc_get(self.tgen_port_handle,
                                         '-AffiliationPort-sources',
                                         cast_=tcl.cast_list) \
                          + (self.tgen_handle,))

        encap_stack = []
        if emulated_interface and emulated_interface.ipv4:
            Ipv4If = hltapi.stc_create(
                'Ipv4If',
                '-under', self.tgen_handle,
                '-Address', emulated_interface.ipv4.ip,
                #'-AddrStep', '0.0.0.1',
                #'-AddrStepMask', '255.255.255.255',
                #'-SkipReserved', 'TRUE',
                #'-AddrList', '',
                #'-AddrRepeatCount', '0',
                #'-AddrResolver', 'default',
                '-PrefixLength', emulated_interface.ipv4.network.prefixlen,
                '-UsePortDefaultIpv4Gateway', 'FALSE',
                '-Gateway', self.gateway_ipv4,
                #'-GatewayStep', '0.0.0.0',
                #'-GatewayRepeatCount', '0',
                #'-GatewayRecycleCount', '0',
                #'-UseIpAddrRangeSettingsForGateway', 'FALSE',
                #'-GatewayList', '',
                '-ResolveGatewayMac', 'TRUE',
                #'-GatewayMac', '00:00:01:00:00:01',
                #'-GatewayMacResolver', 'default',
                #'-Ttl', '255',
                #'-TosType', 'TOS',
                #'-Tos', '192',
                #'-NeedsAuthentication', 'FALSE',
                #'-IfCountPerLowerIf', '1',
                #'-IfRecycleCount', '0',
                #'-IsDecorated', 'FALSE',
                #'-IsLoopbackIf', 'FALSE',
                #'-IsRange', 'TRUE',
                #'-IsDirectlyConnected', 'TRUE',
                #'-Active', 'TRUE',
                #'-LocalActive', 'TRUE',
                #'-Name', 'IPv4 19',
            )
            encap_stack.append(Ipv4If)

        # TODO emulated_interface.ipv6
        # TODO emulated_interface.ipv6_link_local

        if emulated_interface and emulated_interface.eth_encap_val1:
            VlanIf = hltapi.stc_create(
                'VlanIf',
                '-under', self.tgen_handle,
                '-VlanId', emulated_interface.eth_encap_val1,
                #'-IdStep', '0',
                #'-IdList', '',
                #'-IdRepeatCount', '0',
                #'-IdResolver', 'default',
                #'-Priority', '7',
                #'-Cfi', '0',
                #'-Tpid', '33024',
                #'-IfCountPerLowerIf', '1',
                #'-IfRecycleCount', '0',
                #'-IsDecorated', 'FALSE',
                #'-IsLoopbackIf', 'FALSE',
                #'-IsRange', 'TRUE',
                #'-IsDirectlyConnected', 'TRUE',
                #'-Active', 'TRUE',
                #'-LocalActive', 'TRUE',
                #'-Name', 'VLAN 1',
            )
            encap_stack.append(VlanIf)

        from genie.libs.conf.interface import EthernetInterface
        if isinstance(emulated_interface, EthernetInterface):
            EthIIIf = hltapi.stc_create(
                'EthIIIf',
                '-under', self.tgen_handle,
                '-SourceMac', emulated_interface.mac_address or self.tgen_interface.mac_address or '00:00:01:00:00:01',  # TODO see stc::get ... -NextMac
                #'-SrcMacStep', '00:00:00:00:00:01',
                #'-SrcMacList', '',
                #'-SrcMacStepMask', '00:00:ff:ff:ff:ff',
                #'-SrcMacRepeatCount', '0',
                #'-Authenticator', 'default',
                '-UseDefaultPhyMac', 'FALSE',
                #'-IfCountPerLowerIf', '1',
                #'-IfRecycleCount', '0',
                #'-IsDecorated', 'FALSE',
                #'-IsLoopbackIf', 'FALSE',
                #'-IsRange', 'TRUE',
                #'-IsDirectlyConnected', 'TRUE',
                #'-Active', 'TRUE',
                #'-LocalActive', 'TRUE',
                #'-Name', 'EthernetII 19',
            )
            encap_stack.append(EthIIIf)
        else:
            raise NotImplementedError(emulated_interface.__class__.__qualname__)

        hltapi.stc_config(self.tgen_handle,
                          '-TopLevelIf-targets', [encap_stack[0]],
                          '-PrimaryIf-targets', [encap_stack[0]],
                          )
        for prev_encap, this_encap in zip(encap_stack[:-1], encap_stack[1:]):
            hltapi.stc_config(prev_encap, '-StackedOnEndpoint-targets', [this_encap])

        return ''

    def build_unconfig(self, **kwargs):
        if self.tgen_handle is None:
            logger.warn('%r: Nothing to do (no tgen_handle).', self)
            return ''

        tgen_device = self.tgen_device
        hltapi = tgen_device.hltapi
        #tcl = hltapi.tcl

        try:
            hltapi.stc_delete(self.tgen_handle)
        finally:
            self.tgen_handle = None

        return ''

    @property
    def _stc_ipv4if(self):

        tgen_device = self.tgen_device
        hltapi = tgen_device.hltapi
        tcl = hltapi.tcl

        ipv4ifList = hltapi.stc_get(self.tgen_handle, '-children-ipv4if',
                                    cast_=functools.partial(tcl.cast_list, item_cast=tclstr))
        ipv4ifList = tcl.call('::sth::deleteGreIP', ipv4ifList, self.tgen_handle)
        ipv4if, = ipv4ifList

        return ipv4if

