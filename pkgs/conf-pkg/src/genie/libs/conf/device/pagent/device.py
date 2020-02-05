'''
Device class for HLTAPI devices with pagent OS.
'''

__all__ = (
    'Device',
)

from enum import Enum
import collections.abc
import logging
logger = logging.getLogger(__name__)

try:
    from pyats.tcl import tclstr, TclCommand
except Exception:
    pass

from genie.decorator import managedattribute

from genie.libs.conf.device.hltapi import Device as HltapiDevice
import genie.libs.conf.interface.hltapi
import genie.libs.conf.device.ios
from genie.libs.conf.stream import Stream
from genie.libs.conf.base import IPv4Address, IPv6Address, MAC


class Device(HltapiDevice, genie.libs.conf.device.ios.Device):
    '''Device class for HLTAPI devices with pagent OS'''

    class Hltapi(HltapiDevice.Hltapi):
        '''Hltapi class customized for Pagent.'''

        def interface_config(self, **kwargs):

            # Pagent does not support -arp_send_req
            kwargs.pop('arp_send_req', None)
            # Pagent does not support -intf_mode
            kwargs.pop('intf_mode', None)
            # Pagent does not support -op_mode; Unset if "normal"
            if kwargs.get('op_mode', None) == 'normal':
                kwargs.pop('op_mode')
            # Pagent does not support -vlan; Unset if false
            if self.tcl.cast_boolean(kwargs.get('vlan', True)) is False:
                kwargs.pop('vlan')

            hltkl = self.pyats_connection.interface_config(**kwargs)

            return hltkl

        def traffic_config(self, **kwargs):

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

            # IPv4/IPv6 steps have to be in IP format
            try:
                kwargs['ip_src_step'] = str(IPv4Address(kwargs['ip_src_step']))
            except KeyError:
                pass
            try:
                kwargs['ip_dst_step'] = str(IPv4Address(kwargs['ip_dst_step']))
            except KeyError:
                pass
            try:
                kwargs['ipv6_src_step'] = str(IPv6Address(kwargs['ipv6_src_step']))
            except KeyError:
                pass
            try:
                kwargs['ipv6_dst_step'] = str(IPv6Address(kwargs['ipv6_dst_step']))
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
            # Pagent HLTAPI does not support l3_protocol=none, not sending it is equivalent.
            if kwargs.get('l3_protocol', None) == 'none':
                del kwargs['l3_protocol']
            # Pagent HLTAPI does not support l4_protocol=none, not sending it is equivalent.
            if kwargs.get('l4_protocol', None) == 'none':
                del kwargs['l4_protocol']
            # Pagent does not support -mac_discovery_gw
            kwargs.pop('mac_discovery_gw', None)
            # Pagent does not support -name
            kwargs.pop('name', None)
            # Pagent only supports -mpls_labels in this format: <label>,<cos>,<bottom>,<ttl>
            if 'mpls_labels' in kwargs:
                mpls_labels = self.tcl.cast_list(kwargs['mpls_labels'], item_cast=tclstr)
                for i, mpls_label in enumerate(mpls_labels):
                    try:
                        mpls_label = int(mpls_label)
                    except ValueError:
                        continue
                    else:
                        mpls_label = '{mpls_label},{cos},{bottom},{ttl}'.format(
                            mpls_label=mpls_label,
                            cos=0,
                            bottom=int(i == len(mpls_labels) - 1),
                            ttl=0)
                    mpls_labels[i] = mpls_label
            # Pagent does not support -gateway and -ipv6_gateway
            kwargs.pop('gateway', None)
            kwargs.pop('ipv6_gateway', None)
            # Pagent does not support -mpls_labels_mode, support is equivalent to "fixed"
            if kwargs.get('mpls_labels_mode', None) == 'fixed':
                del kwargs['mpls_labels_mode']

            # -type is Agilent-specific. Default should be "stream"; Anything else is not supported.
            if kwargs.get('type', None) == 'stream':
                del kwargs['type']
            # -dut_type is Agilent-specific.
            kwargs.pop('dut_type', None)
            # Pagent does not support -dest_port_list
            kwargs.pop('dest_port_list', None)

            hltkl = self.pyats_connection.traffic_config(**kwargs)

            if kwargs.get('mode', None) == 'remove' \
                    and 'port_handle' in kwargs \
                    and 'stream_id' in kwargs:
                pagent_stream_ids_var = self.tcl.vars.byref('::Pagent::_Tgn_Info', array_index=kwargs['port_handle'])
                if pagent_stream_ids_var.exists():
                    # Workaround a bug in Pagent where -mode remove does not
                    # "forget" the stream IDs associated with a port
                    pagent_stream_ids = self.tcl.cast_list(pagent_stream_ids_var.get_obj(), item_cast=tclstr)
                    kwarg_stream_ids = set(self.tcl.cast_list(kwargs['stream_id'], item_cast=tclstr))
                    pagent_stream_ids = [stream_id
                                         for stream_id in pagent_stream_ids
                                         if stream_id not in kwarg_stream_ids]
                    if pagent_stream_ids:
                        pagent_stream_ids_var.set(pagent_stream_ids)
                    else:
                        # If left empty, commands such as traffic_control -action
                        # poll may return failure.
                        pagent_stream_ids_var.unset()

            return hltkl

        def traffic_stats(self, **kwargs):

            if 'streams' in kwargs:
                streams_ids = self.tcl.cast_list(kwargs['streams'], item_cast=tclstr)
                Pagent_GET_STREAMS_STATS_proc = TclCommand(
                    '::Pagent::GET_STREAMS_STATS',
                    tcl=self.tcl)
                if len(streams_ids) > 1 \
                        and Pagent_GET_STREAMS_STATS_proc.exists() \
                        and 'lsearch $stream_id $streams' in Pagent_GET_STREAMS_STATS_proc.proc_body():
                    # Due to a bug in ::Pagent::GET_STREAMS_STATS where stream
                    # IDs are incorrectly matched (wrong order of [lsearch]
                    # parameters), revert to getting all the streams on all or
                    # only the specified ports
                    del kwargs['streams']

            hltkl = self.pyats_connection.traffic_stats(**kwargs)

            return hltkl

        def traffic_control(self, **kwargs):

            hltkl = self.pyats_connection.traffic_control(**kwargs)

            if kwargs.get('action', None) == 'poll' \
                    and 'stopped' not in hltkl:
                # -------------------------- Keyed List: hltkl -------------------------
                # status                              = 0
                # log                                 = {No traffic streams defined in Ethernet0/3 of SEB2-PT}
                # SEB2-PT_Ethernet0/1
                #     stopped                         = 0
                # SEB2-PT_Ethernet0/3
                #     stopped                         = 0
                # ----------------------------------------------------------------------
                stopped = True
                for k, v in hltkl.items():
                    if not isinstance(v, collections.abc.Mapping):
                        continue
                    if 'stopped' not in v:
                        continue
                    stopped = self.tcl.cast_boolean(v['stopped'])
                    if not stopped:
                        break
                stopped = 1 if stopped else 0
                logger.debug('Pagent: setting hltkl stopped = %r', stopped)
                hltkl['stopped'] = stopped

            return hltkl

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

