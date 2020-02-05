'''
Device class for HLTAPI devices with ixia OS.
'''

__all__ = (
    'Device',
    'EmulatedDevice',
)

from enum import Enum
import logging

try:
    from pyats.tcl import tclstr
    import pyats.tcl
except Exception:
    pass

from genie.decorator import managedattribute

from genie.libs.conf.device.hltapi import Device as HltapiDevice
import genie.libs.conf.device
import genie.libs.conf.interface.hltapi
from genie.libs.conf.stream import Stream
from genie.libs.conf.base import IPv4Address, IPv6Address, MAC

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)


class Device(HltapiDevice):
    '''Device class for HLTAPI devices with ixia OS'''

    class Hltapi(HltapiDevice.Hltapi):
        '''Hltapi class customized for Ixia.
        
        The following APIs are also provided by the HLTAPI connection:
            - ixNet
        '''

        def traffic_config(self, **kwargs):
            if 'name' in kwargs:
                assert '.' not in kwargs['name'], \
                    'Ixia stream names are used as stream IDs in Tcl keyed ' \
                    'lists and should not contain "." characters: {}' \
                    .format(kwargs['name'])
            # Supports frame_size or l3_length
            try:
                kwargs['frame_size'] = kwargs.pop('packet_len')
            except KeyError:
                pass
            try:
                kwargs['frame_size'] = kwargs.pop('l2_length')
            except KeyError:
                pass
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
            # Legacy API accepts MAC steps can be in either MAC or integer format and internally converts to integer.
            # ixnetwork_540 API accepts only MAC steps in MAC format.
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
            # Ixia HLTAPI does not support l3_protocol=none, not sending it is equivalent.
            if kwargs.get('l3_protocol', None) == 'none':
                del kwargs['l3_protocol']
            # Ixia HLTAPI does not support l4_protocol=none, not sending it is equivalent.
            if kwargs.get('l4_protocol', None) == 'none':
                del kwargs['l4_protocol']
            # Ixia HLTAPI does not support mac_discovery_gw
            kwargs.pop('mac_discovery_gw', None)
            kwargs.pop('mac_discovery_gw_count', None)
            kwargs.pop('mac_discovery_gw_step', None)
            # Enable tracking
            if kwargs.get('mode', None) == 'create':
                kwargs.setdefault('track_by', 'traffic_item')
            # Extra Ixia options for MPLS
            if 'mpls_labels' in kwargs:
                kwargs.setdefault('mpls_labels_mode', 'fixed')
                kwargs.setdefault('mpls', 'enable')
            # Extra Ixia vlan toggle
            if kwargs.get('mode', None) == 'create' and 'vlan_id' in kwargs:
                kwargs.setdefault('vlan', 'enable')

            # -type is Agilent-specific. Default should be "stream"; Anything else is not supported.
            if kwargs.get('type', None) == 'stream':
                del kwargs['type']
            # -dut_type is Agilent-specific.
            kwargs.pop('dut_type', None)
            # Ixia uses -port_handle2 instead of -dest_port_list (for unidirectional streams)
            if 'dest_port_list' in kwargs:
                kwargs.setdefault('port_handle2', kwargs.pop('dest_port_list'))

            hltkl = self.pyats_connection.traffic_config(**kwargs)

            return hltkl

        def traffic_control(self, **kwargs):

            # TODO
            # if {
            #     ![info exists opts(traffic_generator)] &&
            #     [info exists ::enaTgnUtils::traffic_generator] &&
            #     $::enaTgnUtils::traffic_generator ne ""
            # } {
            #     set opts(traffic_generator) $::enaTgnUtils::traffic_generator
            # }

            # -port_handle is mandatory if -traffic_generator is "ixos", default to all anyway
            if 'port_handle' not in kwargs:
                kwargs['port_handle'] = self.device.all_port_handles

            hltkl = self.pyats_connection.traffic_control(**kwargs)

            return hltkl

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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

        from genie.libs.conf.interface import EthernetInterface

        intf_kwargs = {}
        intf_kwargs['port_handle'] = self.tgen_port_handle

        # -count                                      NUMERIC
        #                                             DEFAULT 1
        # -check_opposite_ip_version                  CHOICES 0 1
        #                                             DEFAULT 1
        # -override_existence_check                   CHOICES 0 1
        # -override_tracking                          CHOICES 0 1

        if emulated_interface and emulated_interface.ipv4:
            intf_kwargs['ipv4_address'] = emulated_interface.ipv4.ip
            # -ipv4_address_step                          IPV4
            intf_kwargs['ipv4_prefix_length'] = emulated_interface.ipv4.network.prefixlen
            # -ipv4_prefix_length                         NUMERIC
            if isinstance(emulated_interface, EthernetInterface):
                # -check_gateway_exists                       CHOICES 0 1
                #                                             DEFAULT 0
                intf_kwargs['gateway_address'] = self.gateway_ipv4
                # -gateway_address_step                       IPV4

        if emulated_interface and emulated_interface.ipv6:
            intf_kwargs['ipv6_address'] = emulated_interface.ipv6.ip
            intf_kwargs['ipv6_prefix_length'] = emulated_interface.ipv6.network.prefixlen
            # -ipv6_address_step                          IPV6
            if isinstance(emulated_interface, EthernetInterface):
                intf_kwargs['ipv6_gateway'] = self.gateway_ipv6
                # -ipv6_gateway_step                          IPV6
            # -target_link_layer_address                  CHOICES 0 1

        intf_kwargs['loopback_count'] = 0
        if emulated_loopback and emulated_loopback.ipv4:
            intf_kwargs['loopback_count'] = 1
            intf_kwargs['loopback_ipv4_address'] = emulated_loopback.ipv4.ip
            # -loopback_ipv4_address_outside_step         IPV4
            # -loopback_ipv4_address_step                 IPV4
            intf_kwargs['loopback_ipv4_prefix_length'] = emulated_loopback.ipv4.network.prefixlen
        if emulated_loopback and emulated_loopback.ipv6:
            intf_kwargs['loopback_count'] = 1
            intf_kwargs['loopback_ipv6_address'] = emulated_loopback.ipv6.ip
            # -loopback_ipv6_address_outside_step         IPV6
            # -loopback_ipv6_address_step                 IPV6
            intf_kwargs['loopback_ipv6_prefix_length'] = emulated_loopback.ipv6.network.prefixlen

        if isinstance(emulated_interface, EthernetInterface):
            intf_kwargs['mac_address'] = emulated_interface.mac_address or self.tgen_interface.mac_address or '00:00:01:00:00:01'
            # -mac_address_step

        if emulated_interface.mtu is not None:
            intf_kwargs['mtu'] = emulated_interface.mtu

        # -atm_encapsulation                          CHOICES VccMuxIPV4Routed
        #                                             CHOICES VccMuxIPV6Routed
        #                                             CHOICES VccMuxBridgedEthernetFCS
        #                                             CHOICES VccMuxBridgedEthernetNoFCS
        #                                             CHOICES LLCRoutedCLIP
        #                                             CHOICES LLCBridgedEthernetFCS
        #                                             CHOICES LLCBridgedEthernetNoFCS
        #                                             CHOICES VccMuxMPLSRouted
        #                                             CHOICES VccMuxPPPoA
        #                                             CHOICES LLCNLPIDRouted
        #                                             CHOICES LLCPPPoA
        # -atm_vci                                    RANGE   0-65535
        # -atm_vci_step                               RANGE   0-65535
        # -atm_vpi                                    RANGE   0-255
        # -atm_vpi_step                               RANGE   0-255

        # -gre_count                                  NUMERIC
        #                                             DEFAULT 1
        # -gre_ipv4_address                           IPV4
        # -gre_ipv4_prefix_length                     NUMERIC
        # -gre_ipv4_address_step                      IPV4
        # -gre_ipv4_address_outside_connected_reset   CHOICES 0 1
        #                                             DEFAULT 1
        # -gre_ipv4_address_outside_connected_step    IPV4
        # -gre_ipv4_address_outside_loopback_step     IPV4
        # -gre_ipv6_address                           IPV6
        # -gre_ipv6_prefix_length                     NUMERIC
        # -gre_ipv6_address_step                      IPV6
        # -gre_ipv6_address_outside_connected_reset   CHOICES 0 1
        #                                             DEFAULT 1
        # -gre_ipv6_address_outside_connected_step    IPV6
        # -gre_ipv6_address_outside_loopback_step     IPV6
        # -gre_dst_ip_address                         IP
        # -gre_dst_ip_address_step                    IP
        # -gre_dst_ip_address_reset                   CHOICES 0 1
        #                                             DEFAULT 1
        # -gre_dst_ip_address_outside_connected_step  IP
        # -gre_dst_ip_address_outside_loopback_step   IP
        # -gre_src_ip_address                         CHOICES connected routed
        #                                             DEFAULT connected
        # -gre_checksum_enable                        CHOICES 0 1
        # -gre_seq_enable                             CHOICES 0 1
        # -gre_key_enable                             CHOICES 0 1
        # -gre_key_in                                 NUMERIC
        # -gre_key_in_step                            NUMERIC
        # -gre_key_out                                NUMERIC
        # -gre_key_out_step                           NUMERIC

        intf_kwargs['vlan_enabled'] = 0
        if emulated_interface.eth_encap_val1 is not None:
            intf_kwargs['vlan_enabled'] = 1
            intf_kwargs['vlan_id'] = emulated_interface.eth_encap_val1  # REGEXP ^[0-9]{1,4}(,[0-9]{1,4})*$
            intf_kwargs['vlan_id_mode'] = 'fixed'  # REGEXP ^(fixed|increment)(,(fixed|increment))*$
            # -vlan_id_step                               REGEXP ^[0-9]{1,4}(,[0-9]{1,4})*$
            # -vlan_tpid                                  REGEXP ^0x[0-9a-fA-F]+(,0x[0-9a-fA-F]+)*$
            # -vlan_user_priority                         REGEXP ^[0-7](,[0-7])*$
            # -vlan_user_priority_step                    REGEXP ^[0-7](,[0-7])*$

        kl = tcl.cast_keyed_list(
            hltapi.ixNetworkProtocolIntfCfg(**intf_kwargs),
            item_cast=tclstr)
        if int(kl.get('status', 0)) == 0:
            raise ValueError(kl.get('log', 'Unknown message'))

        self.tgen_handle = tcl.cast_list(
            kl.connected_interfaces,
            item_cast=tclstr)

        # TODO self.name
        # TODO emulated_interface.ipv6_link_local

        return ''

    def build_unconfig(self, **kwargs):
        if self.tgen_handle is None:
            logger.warn('%r: Nothing to do (no tgen_handle).', self)
            return ''

        tgen_device = self.tgen_device
        hltapi = tgen_device.hltapi
        #tcl = hltapi.tcl

        try:
            hltapi.isNetworkRemove(self.tgen_handle)
            hltapi.ixNetworkCommit()
        finally:
            self.tgen_handle = None

        return ''

    @property
    def _ix_hltapi_interface_handle(self):
        if self.tgen_handle:
            return tuple(
                '{}|dummy|ProtocolIntf'.format(ix_connected_interface)
                for ix_connected_interface in self.tgen_handle)

