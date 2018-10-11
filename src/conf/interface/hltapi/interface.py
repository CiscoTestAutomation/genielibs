'''
    Generic Interface classes for HLTAPI-based TGEN devices.
'''

__all__ = (
    'Interface',
    'PhysicalInterface',
    'EthernetInterface',
    'PosInterface',
    'AtmInterface',
    'EmulatedInterface',
    'VirtualInterface',
    'SubInterface',
)

import abc
from enum import Enum

from genie.decorator import managedattribute
from genie.conf.base.attributes import AttributesHelper

import genie.libs.conf.interface
import genie.libs.conf.interface.tgen


class Interface(genie.libs.conf.interface.tgen.Interface):
    '''Base Interface class for HLTAPI-based TGEN devices'''

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PhysicalInterface(Interface,
                        genie.libs.conf.interface.tgen.PhysicalInterface):
    '''Class for physical HLTAPI-based TGEN interfaces/ports'''

    class InterfaceMode(Enum):
        ethernet = 'ethernet'
        atm = 'atm'
        pos_hdlc = 'pos_hdlc'
        fr = 'fr'
        pos_ppp = 'pos_ppp'

    intf_mode = managedattribute(
        name='intf_mode',
        default=InterfaceMode.ethernet,
        type=InterfaceMode)

    tgen_port_handle = managedattribute(
        name='tgen_port_handle',
        doc='''The port handle, as understood by HLTAPI/low-level vendor APIs.

            If the HLTAPI connection sets this value on the interface
            object, this value will be returned.

            Otherwise, the Interface's name is used.
        ''')

    tgen_handle = managedattribute(
        name='tgen_handle',
        default=None,
        doc='''The logical interface configuration handle, as understood by
            HLTAPI/low-level vendor APIs.''')

    @tgen_port_handle.defaulter
    def tgen_port_handle(self):
        try:
            return self.tgen_port_handle
        except AttributeError:
            pass

        return self.name

    class PhysicalMode(Enum):
        fiber = gbic = 'fiber'
        copper = rj45 = 'copper'
        sfp = 'sfp'

    phy_mode = managedattribute(
        name='phy_mode',
        default=None,
        type=(None, PhysicalMode))

    class OperationalMode(Enum):
        normal = 'normal'
        loopback = 'loopback'

    op_mode = managedattribute(
        name='op_mode',
        default=OperationalMode.normal,
        type=OperationalMode)

    @property
    def layer2_peer_interfaces(self):
        '''Get the list of layer2 peer interfaces, the one(s) physically
        connected and from which layer2 protocol is chosen.'''
        # TODO find appropriate peer...
        # - from link of type [iflink ifmesh ctrlink]
        # - if multiple peers (broadcast), return all
        # **NOTE** 
        # Links under Genie Interface object is deprecated
        # Placed the below workaround to bypass the Unittest (commented out)
        # for link in self.links:
        # if self.link.obj_state != 'active':
        #     continue
        for interface in self.link.interfaces:
            if interface.obj_state != 'active':
                continue
            if interface.device is not self.device:
                yield interface

    gateway_interface = managedattribute(
        name='gateway_interface',
        type=(None, managedattribute.test_isinstance(
            genie.libs.conf.interface.Interface)))

    @gateway_interface.defaulter
    def gateway_interface(self):
        # TODO find appropriate peer...
        # - in priority from link of type [xc bd otnxc],
        #   then [iflink ifmesh ctrlink], then other types.
        # - if multiple peers (broadcast), take the first.
        # **NOTE** 
        # Links under Genie Interface object is deprecated
        # Placed the below workaround to bypass the Unittest (commented out)
        # for link in self.links:
        # if self.link.obj_state != 'active':
        #     continue
        for interface in self.link.interfaces:
            if interface.obj_state != 'active':
                continue
            if interface.device is not self.device:
                return interface

    @property
    def gateway_ipv4(self):
        gw_ip = None
        gw_intf = self.gateway_interface
        if gw_intf is not None and gw_intf.ipv4:
            return gw_intf.ipv4.ip
        if self.ipv4:
            # Find a linked interface on the same IP network
            for gw_intf in (intf for intf in self.link.interfaces):
                if gw_intf is not self \
                        and gw_intf.ipv4 \
                        and gw_intf.ipv4.network == self.ipv4.network:
                    return gw_intf.ipv4
            # Pick a dummy IP on the same network
            for gw_ip in self.ipv4.network:
                if gw_ip != self.ipv4.ip:
                    return gw_ip
        return None

    @property
    def gateway_ipv6(self):
        gw_ip = None
        gw_intf = self.gateway_interface
        if gw_intf is not None and gw_intf.ipv6:
            return gw_intf.ipv6.ip
        if self.ipv6:
            # Find a linked interface on the same IP network
            for gw_intf in (intf for intf in self.link.interfaces):
                if gw_intf is not self \
                        and gw_intf.ipv6 \
                        and gw_intf.ipv6.network == self.ipv6.network:
                    return gw_intf.ipv6
            # Pick a dummy IP on the same network
            for gw_ip in self.ipv6.network:
                if gw_ip != self.ipv6.ip:
                    return gw_ip
        return None

    def _build_interface_config_hltkwargs(self, attributes=None,
                                          unconfig=False):
        attributes = AttributesHelper(self, attributes)

        hltkwargs = None

        if unconfig:

            if self.tgen_port_configured:
                hltkwargs = {}
                hltkwargs['port_handle'] = self.tgen_port_handle
                hltkwargs['mode'] = 'destroy'

        else:

            hltkwargs = {}
            hltkwargs['mode'] = mode = 'modify' \
                if self.tgen_port_configured else 'config'
            hltkwargs['port_handle'] = self.tgen_port_handle
            # hltkwargs['aps'] = TODO
            # hltkwargs['aps_arch'] = TODO
            # hltkwargs['aps_channel'] = TODO
            # hltkwargs['aps_request_1_1'] = TODO
            # hltkwargs['aps_request_1_n'] = TODO
            # hltkwargs['aps_switch_mode'] = TODO
            hltkwargs.update(attributes.format_dict({
                'phy_mode': '{phy_mode.value}'}))
            hltkwargs.update(attributes.format_dict({
                'intf_mode': '{intf_mode.value}'}))
            if self.intf_mode is self.InterfaceMode.ethernet:
                hltkwargs.update(attributes.format_dict({
                    'autonegotiation': '{auto_negotiation:d}'}))
                # speed and duplex may also be used with auto_negotiation to
                # limit possibilities.
                hltkwargs.update(attributes.format_dict({
                    'speed': '{speed}'}))
                hltkwargs.update(attributes.format_dict({
                    'duplex': '{duplex}'}))
            elif self.intf_mode is self.InterfaceMode.atm:
                # hltkwargs['speed'] = TODO
                # hltkwargs['atm_enable_coset'] = TODO
                # hltkwargs['atm_enable_pattern_matching'] = TODO
                # hltkwargs['atm_encapsulation'] = TODO
                # hltkwargs['atm_filler_cell'] = TODO
                # hltkwargs['atm_interface_type'] = TODO
                # hltkwargs['atm_packet_decode_mode'] = TODO
                # hltkwargs['atm_reassembly_timeout'] = TODO
                pass
            elif self.intf_mode in (
                self.InterfaceMode.pos_hdlc,
                self.InterfaceMode.fr,
                self.InterfaceMode.pos_ppp,
            ):
                # hltkwargs['speed'] = TODO
                hltkwargs.update(attributes.format_dict({
                    'tx_scrambling': '{tx_scrambling:d}'}))
                hltkwargs.update(attributes.format_dict({
                    'rx_scrambling': '{rx_scrambling:d}'}))
            else:
                raise ValueError(
                    'Unsupported intf_mode %r' % (self.intf_mode,))

            hltkwargs.update(attributes.format_dict({
                'op_mode': '{op_mode.value}'}))
            if self.op_mode is self.OperationalMode.loopback:
                pass
            elif self.op_mode is self.OperationalMode.normal:
                if self.intf_mode is self.InterfaceMode.ethernet:
                    hltkwargs.update(attributes.format_dict({
                        'src_mac_addr': '{mac_address}'}))
                    if self.mac_address is not None:
                        pass  # hltkwargs['src_mac_addr_step'] = TODO
                    if self.ipv4 is not None:
                        # hltkwargs['arp_cache_retrieve'] = TODO
                        # hltkwargs['arp_req_retries'] = TODO
                        # hltkwargs['arp_req_timer'] = TODO
                        hltkwargs.update(attributes.format_dict({
                            'arp_send_req': '1'}))
                    if self.eth_encap_val1 is not None:
                        hltkwargs['vlan'] = 1
                        hltkwargs['vlan_id'] = self.eth_encap_val1
                        # TODO
                        # if { [set count [enaTbGetInterfaceParam $vIntf -count]] > 1 } {
                            # hltkwargs['vlan_id_mode'] = "increment"
                            # hltkwargs['vlan_id_step'] = [expr {
                            #         [enaTbGetInterfaceParam $vIntf -instance 1 -eth-encap-val1] -
                            #         $vlan
                            # }]
                            # hltkwargs['vlan_id_count'] = $count
                        # } else {
                        hltkwargs['vlan_id_mode'] = "fixed"
                        # }
                        # hltkwargs['vlan_user_priority'] = TODO
                        if self.eth_encap_val2 is not None:
                            hltkwargs['vlan_id_inner'] = self.eth_encap_val2
                            # if { [set count [enaTbGetInterfaceParam $vIntf -count]] > 1 } {
                                # hltkwargs['vlan_id_inner_mode'] = "increment"
                                # hltkwargs['vlan_id_inner_step'] = [expr {
                                #         [enaTbGetInterfaceParam $vIntf -instance 1 -eth-encap-val2] -
                                #         $vlan
                                # }]
                                # hltkwargs['vlan_id_inner_count'] = $count
                            # } else {
                            hltkwargs['vlan_id_inner_mode'] = "fixed"
                            # }
                    else:
                        hltkwargs['vlan'] = 0
                elif self.intf_mode is self.InterfaceMode.atm:
                    pass
                elif self.intf_mode in (
                    self.InterfaceMode.pos_hdlc,
                    self.InterfaceMode.fr,
                    self.InterfaceMode.pos_ppp,
                ):
                    pass
                else:
                    raise ValueError(
                        'Unsupported intf_mode %r' % (self.intf_mode,))

                if self.ipv4:
                    hltkwargs['intf_ip_addr'] = self.ipv4.ip
                    hltkwargs['netmask'] = self.ipv4.netmask
                    gw_ip = self.gateway_ipv4
                    if gw_ip:
                        hltkwargs['gateway'] = gw_ip
                else:
                    hltkwargs['intf_ip_addr'] = '0.0.0.0'
                    hltkwargs['netmask'] = '255.255.255.0'
                    hltkwargs['gateway'] = '0.0.0.0'

                if self.ipv6:
                    hltkwargs['ipv6_intf_addr'] = self.ipv6.ip
                    hltkwargs['ipv6_prefix_length'] = \
                        self.ipv6.network.prefixlen
                    gw_ip = self.gateway_ipv6
                    if gw_ip:
                        hltkwargs['ipv6_gateway'] = gw_ip
                else:
                    # hltkwargs['ipv6_intf_addr'] = '::'
                    # hltkwargs['ipv6_prefix_length'] = 112
                    # hltkwargs['ipv6_gateway'] = '::'
                    pass

            # hltkwargs['auto_line_rdi'] = TODO
            # hltkwargs['auto_line_rei'] = TODO
            # hltkwargs['auto_path_rdi'] = TODO
            # hltkwargs['auto_path_rei'] = TODO
            # hltkwargs['clocksource'] = TODO
            # hltkwargs['collision_exponent'] = TODO
            # hltkwargs['control_plane_mtu'] = TODO
            # hltkwargs['crlf_path_trace'] = TODO
            # hltkwargs['data_integrity'] = TODO
            # hltkwargs['dst_mac_addr'] = TODO
            # hltkwargs['enforce_mtu_on_rx'] = TODO
            # hltkwargs['ether_pause_mode'] = TODO
            # hltkwargs['framing'] = TODO
            # hltkwargs['gre_checksum_enable'] = TODO
            # hltkwargs['gre_dst_ip_addr'] = TODO
            # hltkwargs['gre_ip_addr'] = TODO
            # hltkwargs['gre_ip_prefix_length'] = TODO
            # hltkwargs['gre_ipv6_addr'] = TODO
            # hltkwargs['gre_ipv6_prefix_length'] = TODO
            # hltkwargs['gre_key_enable'] = TODO
            # hltkwargs['gre_key_in'] = TODO
            # hltkwargs['gre_key_out'] = TODO
            # hltkwargs['gre_seq_enable'] = TODO
            # hltkwargs['ignore_pause_frames'] = TODO
            # hltkwargs['internal_ppm_adjust'] = TODO
            # hltkwargs['interpacket_gap'] = TODO
            # hltkwargs['lais_lrdi_threshold'] = TODO
            # hltkwargs['line_ais'] = TODO
            # hltkwargs['line_bip24'] = TODO
            # hltkwargs['line_bip384'] = TODO
            # hltkwargs['line_bip96'] = TODO
            # hltkwargs['line_rdi'] = TODO
            # hltkwargs['line_rei'] = TODO
            # hltkwargs['line_type'] = TODO
            # hltkwargs['long_lof_wait'] = TODO
            # hltkwargs['output_enable'] = TODO
            # hltkwargs['path_ais'] = TODO
            # hltkwargs['path_bip8'] = TODO
            # hltkwargs['path_rdi'] = TODO
            # hltkwargs['path_rei'] = TODO
            # hltkwargs['path_type'] = TODO
            # hltkwargs['pause_length'] = TODO
            # hltkwargs['port_setup_mode'] = TODO
            # hltkwargs['prdi_threshold'] = TODO
            # hltkwargs['rpr_hec_seed'] = TODO
            # hltkwargs['rx_c2'] = TODO
            # hltkwargs['rx_enhanced_prdi'] = TODO
            # hltkwargs['rx_equalization'] = TODO
            # hltkwargs['rx_fcs'] = TODO
            # hltkwargs['rx_hec'] = TODO
            # hltkwargs['section_bip8'] = TODO
            # hltkwargs['section_unequip'] = TODO
            # hltkwargs['signal_fail_ber'] = TODO
            # hltkwargs['src_mac_addr'] = TODO
            # hltkwargs['ss_bits_pointer_interp'] = TODO
            # hltkwargs['static_atm_header_encapsulation'] = TODO
            # hltkwargs['static_atm_range_count'] = TODO
            # hltkwargs['static_dlci_count_mode'] = TODO
            # hltkwargs['static_dlci_repeat_count'] = TODO
            # hltkwargs['static_dlci_repeat_count_step'] = TODO
            # hltkwargs['static_dlci_value'] = TODO
            # hltkwargs['static_dlci_value_step'] = TODO
            # hltkwargs['static_enable'] = TODO
            # hltkwargs['static_fr_range_count'] = TODO
            # hltkwargs['static_indirect'] = TODO
            # hltkwargs['static_intf_handle'] = TODO
            # hltkwargs['static_ip_dst_addr'] = TODO
            # hltkwargs['static_ip_dst_count'] = TODO
            # hltkwargs['static_ip_dst_count_step'] = TODO
            # hltkwargs['static_ip_dst_increment'] = TODO
            # hltkwargs['static_ip_dst_increment_step'] = TODO
            # hltkwargs['static_ip_dst_prefix_len'] = TODO
            # hltkwargs['static_ip_dst_prefix_len_step'] = TODO
            # hltkwargs['static_ip_dst_range_step'] = TODO
            # hltkwargs['static_ip_range_count'] = TODO
            # hltkwargs['static_l3_protocol'] = TODO
            # hltkwargs['static_lan_range_count'] = TODO
            # hltkwargs['static_mac_dst'] = TODO
            # hltkwargs['static_mac_dst_count'] = TODO
            # hltkwargs['static_mac_dst_count_step'] = TODO
            # hltkwargs['static_mac_dst_mode'] = TODO
            # hltkwargs['static_mac_dst_step'] = TODO
            # hltkwargs['static_pvc_count'] = TODO
            # hltkwargs['static_pvc_count_step'] = TODO
            # hltkwargs['static_range_per_spoke'] = TODO
            # hltkwargs['static_site_id'] = TODO
            # hltkwargs['static_site_id_enable'] = TODO
            # hltkwargs['static_site_id_step'] = TODO
            # hltkwargs['static_vci'] = TODO
            # hltkwargs['static_vci_increment'] = TODO
            # hltkwargs['static_vci_increment_step'] = TODO
            # hltkwargs['static_vci_step'] = TODO
            # hltkwargs['static_vlan_enable'] = TODO
            # hltkwargs['static_vlan_id'] = TODO
            # hltkwargs['static_vlan_id_mode'] = TODO
            # hltkwargs['static_vlan_id_step'] = TODO
            # hltkwargs['static_vpi'] = TODO
            # hltkwargs['static_vpi_increment'] = TODO
            # hltkwargs['static_vpi_increment_step'] = TODO
            # hltkwargs['static_vpi_step'] = TODO
            # hltkwargs['transmit_clock_source'] = TODO
            # hltkwargs['transmit_mode'] = TODO
            # hltkwargs['tx_c2'] = TODO
            # hltkwargs['tx_enhanced_prdi'] = TODO
            # hltkwargs['tx_fcs'] = TODO
            # hltkwargs['tx_k2'] = TODO
            # hltkwargs['tx_preemphasis_main_tap'] = TODO
            # hltkwargs['tx_preemphasis_post_tap'] = TODO
            # hltkwargs['tx_s1'] = TODO

        return hltkwargs

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EthernetInterface(PhysicalInterface,
                        genie.libs.conf.interface.EthernetInterface):
    '''Class for physical ethernet HLTAPI-based TGEN interfaces/ports'''

    intf_mode = PhysicalInterface.intf_mode.copy(
        default=PhysicalInterface.InterfaceMode.ethernet)

    # Because not all vendors agree on the default, make it False as defined in
    # the Cisco HLTAPI spec.
    auto_negotiation = genie.libs.conf.interface.EthernetInterface.auto_negotiation.copy(
        default=False)

    # Restrict duplex to only HLTAPI-allowed strings
    duplex = genie.libs.conf.interface.EthernetInterface.duplex.copy(
        type=(None, managedattribute.test_in((
            'full',
            'half',
        ))))

    # Restrict speed to only HLTAPI-allowed strings
    speed = genie.libs.conf.interface.EthernetInterface.speed.copy(
        type=(None, managedattribute.test_in((
            'ether10',
            'ether100',
            'ether1000',
            'ether10000',
            'ether40Gig',
            'ether100Gig',
            'ether10000lan',  # Ixia
            'ether40000lan',  # Ixia
            'ether100000lan',  # Ixia
        ))))

    @abc.abstractmethod  # XXXJST TODO
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AtmInterface(PhysicalInterface,
                   genie.libs.conf.interface.AtmInterface):
    '''Class for physical ATM HLTAPI-based TGEN interfaces/ports'''

    intf_mode = PhysicalInterface.intf_mode.copy(
        default=PhysicalInterface.InterfaceMode.atm)

    @abc.abstractmethod  # XXXJST TODO
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PosInterface(PhysicalInterface,
                   genie.libs.conf.interface.PosInterface):
    '''Class for physical POS HLTAPI-based TGEN interfaces/ports'''

    intf_mode = PhysicalInterface.intf_mode.copy(
        default=PhysicalInterface.InterfaceMode.pos_hdlc)

    tx_scrambling = managedattribute(
        name='tx_scrambling',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    rx_scrambling = managedattribute(
        name='rx_scrambling',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    @abc.abstractmethod  # XXXJST TODO
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EmulatedInterface(Interface,
                        genie.libs.conf.interface.tgen.EmulatedInterface):
    '''Class for emulated HLTAPI-based TGEN interfaces'''

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VirtualInterface(Interface,
                       genie.libs.conf.interface.tgen.VirtualInterface):
    '''Class for virtual HLTAPI-based TGEN interfaces'''

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SubInterface(VirtualInterface,
                   genie.libs.conf.interface.tgen.SubInterface):
    '''Class for HLTAPI-based TGEN sub-interfaces'''

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


