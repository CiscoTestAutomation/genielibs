'''
    Generic Device class for Cisco-based devices.
'''

__all__ = (
    'Device',
)

import re
import logging
logger = logging.getLogger(__name__)

from genie.decorator import managedattribute
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

import genie.libs.conf.device
from genie.libs.conf.base.ipaddress import ip_address, IPv4Network
from .cli import config_cli_to_tree

debug_clean_config = False


class Device(genie.libs.conf.device.Device):
    '''Base Device class for Cisco devices'''

    def __init__(self, *args, **kwargs):
        logging.warning("This class is deprecated, use the one at "
                    "'genie.libs/conf/device/'")
        super().__init__(*args, **kwargs)

    def build_unconfig(self, clean=False, apply=True, attributes=None,
                       **kwargs):

        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=True)

        if clean:
            postclean = None  # TODO support postclean
            # Is postclean using commit replace?
            if not re.search(r'^\s*commit\s+replace\s*$',
                             postclean or '',
                             re.MULTILINE):

                remove_static_routes = postclean or True
                # Do it the hard way...
                cmds_first = CliConfigBuilder()
                cmds = CliConfigBuilder()
                cmds_last = CliConfigBuilder()
                # TODO ignore_errors = {'invalid-input'}

                l_lab_nets = set()
                l_netboot_intfs = set()
                l_netboot_switchport_access_vlans = set()

                if False:
                    pass  # TODO
                    # if {
                    #     [info exists ::tb_gateway_addr($::env(TESTBED))] &&
                    #     [regexp {^(\d+)\.} $::tb_gateway_addr($::env(TESTBED)) - net]
                    # } { lappend l_lab_nets $net }
                    # enaGetTftpServerInfo arr_tftp_info -router $router
                    # if {
                    #     [info exists arr_tftp_info(tftp_addr)] &&
                    #     [regexp {^(\d+)\.} $arr_tftp_info(tftp_addr) - net]
                    # } { lappend l_lab_nets $net }
                else:
                    # XXXJST the ones I've seen:
                    l_lab_nets.add(IPv4Network('1.0.0.0/8'))
                    l_lab_nets.add(IPv4Network('2.0.0.0/8'))
                    l_lab_nets.add(IPv4Network('5.0.0.0/8'))
                    l_lab_nets.add(IPv4Network('10.0.0.0/8'))
                    l_lab_nets.add(IPv4Network('12.0.0.0/8'))
                    l_lab_nets.add(IPv4Network('172.0.0.0/8'))
                    # TFTP:
                    l_lab_nets.add(IPv4Network('223.255.254.0/24'))

                from genie.libs.conf.interface import ManagementInterface
                netboot_link_name = 'netboot'
                for interface in self.interfaces.values():
                    is_netboot_interface = isinstance(interface, ManagementInterface) \
                        or (getattr(interface, 'link', None)
                            and interface.link.name == netboot_link_name)
                    if is_netboot_interface:
                        l_netboot_intfs.add(interface)
                        sw_acc_vlan = getattr(interface, 'sw_acc_vlan', None)
                        if sw_acc_vlan is not None:
                            l_netboot_switchport_access_vlans.add(sw_acc_vlan)
                        if interface.ipv4:
                            l_lab_nets.add(interface.ipv4.network)
                        if interface.ipv6:
                            l_lab_nets.add(interface.ipv6.network)

                show_run_out = self.execute('show run')
                show_run_tree = config_cli_to_tree(
                    show_run_out, sort=True)

                from genie.libs.conf.device.nxos import Device as NxosDevice
                if isinstance(self, NxosDevice):
                    for line1, subcli1 in show_run_tree or ():
                        m = re.match(r'^feature (?P<feature>.+)', line1)
                        if m:
                            feature = m.group('feature')
                            if feature not in (
                                    'telnet',
                                    'ssh',
                                    'rise',
                                    'lldp',
                            ):
                                # n5000 5.2(1)N1(1b): lldp feature cannot be removed?!?
                                cmds.append_line('no ' + line1)
                            continue
                        m = re.match(r'^ip route .*tunnel-te', line1)
                        if m:
                            # XXXJST CSC... tunnel routes must be removed before feature mpls traffic-eng
                            cmds_first.append_line('no ' + line1)
                            continue

                    configurations.append_block(cmds_first)
                    cmds_first.clear()
                    configurations.append_block(cmds)
                    cmds.clear()
                    configurations.append_block(cmds_last)
                    cmds_last.clear()
                    if apply and configurations:
                        # TODO enaTbClearFeatureCache $router
                        show_run_out = self.execute('show run')
                        show_run_tree = config_cli_to_tree(
                            show_run_out, sort=True)

                l_system_channel_groups = set()

                for line1, subcli1 in show_run_tree or ():
                    m = re.match(r'^!|^$|^end', line1)
                    if m:
                        continue

                    m = re.match(r'^(ip(?:v4|v6)? access-list (?:extended|resequence|role-based|standard) \S+)', line1)
                    if m:
                        cmd = 'no ' + m.group(1)
                        if cmd not in cmds_last:
                            cmds_last.append_line(cmd)
                        continue

                    m = re.match(r'^vpdn enable', line1) \
                        or re.match(r'^mpls label range', line1) \
                        or re.match(r'^ip(?:v4|v6)? access-list', line1) \
                        or re.match(r'^system bridge-domain', line1)
                    if m:
                        cmd = 'no ' + line1
                        if cmd not in cmds_last:
                            cmds_last.append_line(cmd)
                        continue

                    m = re.match(r'^multilink bundle-name authenticated$', line1) \
                        or re.match(r'^interface cmp-mgmt', line1)
                    if m:
                        # Ok... should not be test-affecting
                        continue

                    m = re.match(r'^(mpls ldp router-id) ', line1) \
                        or re.match(r'^(ip(?:v4|v6)? prefix-list \S+)', line1)
                    if m:
                        cmd = 'no ' + m.group(1)
                        if cmd not in cmds:
                            cmds.append_line(cmd)
                        continue

                    m = re.match(r'^(?:ip route|route ip(?:v4)?)(?: vrf \S+)? (?P<ip>\d+\.\d+\.\d+\.\d+)', line1)
                    if m:
                        ip = ip_address(m.group('ip'))
                        if remove_static_routes and not any(ip in lab_net
                                                 for lab_net in l_lab_nets):
                            cmd = 'no ' + line1
                            if cmd not in cmds_first:
                                cmds_first.append_line(cmd)
                            continue

                    m = re.match(r'^vrf context management$', line1) \
                        or re.match(r'^vrf definition (?:Mgmt-intf|mgmtVrf|Mgmt-vrf)$', line1)
                    if m:
                        with cmds.submode_context(line1, cancel_empty=True), \
                                cmds_first.submode_context(line1, cancel_empty=True):
                            for line2, subcli2 in subcli1 or ():
                                line2 = line2.strip()
                                m = re.match(r'^!|^$', line2)
                                if m:
                                    continue

                                m = re.match(r'^(?:ip route|route ip(?:v4)?) (?P<ip>\d+\.\d+\.\d+\.\d+)', line2)
                                if m:
                                    ip = ip_address(m.group('ip'))
                                    if remove_static_routes and not any(ip in lab_net
                                                             for lab_net in l_lab_nets):
                                        cmd = 'no ' + line2
                                        cmds_first.append_line(cmd)
                                    continue

                                # TODO
                                # cmd = 'no ' + line2
                                # cmds.append_line(cmd)

                    m = re.match(r'^mpls ldp configuration$', line1) \
                        or re.match(r'^mpls traffic-eng configuration$', line1)
                    if m:
                        with cmds.submode_context(line1, cancel_empty=True):
                            for line2, subcli2 in subcli1 or ():
                                line2 = line2.strip()
                                m = re.match(r'^!|^$', line2)
                                if m:
                                    continue

                                m = re.match(r'^no ', line2)
                                if m:
                                    # Ok... should not be test-affecting
                                    continue

                                cmd = 'no ' + line2
                                cmds.append_line(cmd)

                    m = re.match(r'^cdp$', line1) \
                        or re.match(r'^bfd$', line1) \
                        or re.match(r'^ip(?:v4|v6)? route ', line1) \
                        or re.match(r'^route ip(?:v4|v6)? ', line1) \
                        or re.match(r'^arp', line1) \
                        or re.match(r'^vrf', line1) \
                        or re.match(r'^ip rsvp', line1) \
                        or re.match(r'^rsvp', line1) \
                        or re.match(r'^router msdp', line1) \
                        or re.match(r'^router ospf', line1) \
                        or re.match(r'^router isis', line1) \
                        or re.match(r'^router bgp', line1) \
                        or re.match(r'^router rip', line1) \
                        or re.match(r'^router eigrp', line1) \
                        or re.match(r'^router pim', line1) \
                        or re.match(r'^router igmp', line1) \
                        or re.match(r'^router mld', line1) \
                        or re.match(r'^segment-routing', line1) \
                        or re.match(r'^multicast-routing', line1) \
                        or re.match(r'^ipv6 router ospf', line1) \
                        or re.match(r'^mpls traffic-eng', line1) \
                        or re.match(r'^mpls optical-uni', line1) \
                        or re.match(r'^mpls optical-nni', line1) \
                        or re.match(r'^mpls ldp', line1) \
                        or re.match(r'^mpls label', line1) \
                        or re.match(r'^mpls static', line1) \
                        or re.match(r'^mpls oam', line1) \
                        or re.match(r'^mpls tp', line1) \
                        or re.match(r'^ethernet cfm', line1) \
                        or re.match(r'^interface [lL]oopback', line1) \
                        or re.match(r'^interface [tT]unnel', line1) \
                        or re.match(r'^interface [vV]lan(?!1$)', line1) \
                        or re.match(r'^interface nve', line1) \
                        or re.match(r'^interface Bundle', line1) \
                        or re.match(r'^interface PW-Ether', line1) \
                        or re.match(r'^interface PW-IW', line1) \
                        or re.match(r'^interface BVI', line1) \
                        or re.match(r'^interface multiservice', line1) \
                        or re.match(r'^interface Virtual-TokenRing', line1) \
                        or re.match(r'^interface .*[:.]\d', line1) \
                        or re.match(r'^interface .* l2transport', line1) \
                        or re.match(r'^interface preconfigure', line1) \
                        or re.match(r'^controller preconfigure', line1) \
                        or re.match(r'^explicit-path', line1) \
                        or re.match(r'^ip explicit-path', line1) \
                        or re.match(r'^ip forward-protocol', line1) \
                        or re.match(r'^ipv6 route ', line1) \
                        or re.match(r'^route ipv6 ', line1) \
                        or re.match(r'^l2 ', line1) \
                        or re.match(r'^l2vpn', line1) \
                        or re.match(r'^lldp', line1) \
                        or re.match(r'^evpn', line1) \
                        or re.match(r'^bridge-domain', line1) \
                        or re.match(r'^redundancy$', line1) \
                        or re.match(r'^lmp', line1) \
                        or re.match(r'^xconnect', line1) \
                        or re.match(r'^pw-class', line1) \
                        or re.match(r'^pseudowire-class', line1) \
                        or re.match(r'^port-profile', line1) \
                        or re.match(r'^tag-switching', line1) \
                        or re.match(r'^vpdn', line1) \
                        or re.match(r'^key chain', line1) \
                        or re.match(r'^route-map ', line1) \
                        or re.match(r'^community-set ', line1) \
                        or re.match(r'^route-policy ', line1) \
                        or re.match(r'^multilink ', line1) \
                        or re.match(r'^spanning-tree ', line1) \
                        or re.match(r'^generic-interface-list ', line1)
                    if m:
                        cmd = 'no ' + line1
                        if cmd not in cmds:
                            cmds.append_line(cmd)
                        continue

                    m = re.match(r'^vlan (?P<vlan_spec>[\d,-]+)$', line1)
                    if m:
                        for vlan_range in m.group('vlan_spec').split(','):
                            if '-' in vlan_range:
                                vlan_min, vlan_max = vlan_range.split('-')
                                vlan_range = range(int(vlan_min),
                                                   int(vlan_max) + 1)
                            else:
                                vlan_range = (int(vlan_min),)
                            for vlan_id in vlan_range:
                                if vlan_id == 1:
                                    continue
                                cmds.append_line('no vlan {}'.format(vlan_id))
                        continue

                    m = re.match(r'^interface [pP]ort-channel(?P<channel_group>\d+)', line1)
                    if m:
                        # Special handling Port-channel interfaces used in VSS and FEX connections
                        channel_group = int(m.group('channel_group'))
                        is_system = False
                        for line2, subcli2 in subcli1 or ():
                            line2 = line2.strip()
                            m = re.match(r'^switchport mode fex-fabric', line2) \
                                or re.match(r'^switch virtual link', line2)
                            if m:
                                is_system = True
                                break
                        if is_system:
                            l_system_channel_groups.add(channel_group)
                            continue
                        cmd = 'no ' + line1
                        if cmd not in cmds:
                            cmds.append_line(cmd)
                        continue

                    m = re.match(r'^router static$', line1)
                    if m:
                        with cmds.submode_context(line1, cancel_empty=True):
                            for line2, subcli2 in subcli1 or ():
                                line2 = line2.strip()
                                m = re.match(r'^!|^$', line2)
                                if m:
                                    continue

                                m = re.match(r'^address-family ipv4 unicast$', line2)
                                if m:
                                    with cmds.submode_context(line2, cancel_empty=True):
                                        for line3, subcli3 in subcli2 or ():
                                            line3 = line3.strip()
                                            m = re.match(r'^!|^$', line3)
                                            if m:
                                                continue

                                            m = re.match(r'^(?P<ip>\d+\.\d+\.\d+\.\d+|(?:::[A-Fa-f0-9]|[A-Fa-f0-9]+:)[A-Fa-f0-9:]*)', line3)
                                            if m:
                                                ip = ip_address(m.group('ip'))
                                                if remove_static_routes and not any(ip in lab_net
                                                                         for lab_net in l_lab_nets):
                                                    cmd = 'no ' + line3
                                                    cmds.append_line(cmd)
                                                continue

                                            # For debugging only...
                                            if debug_clean_config:
                                                logger.warn('clean-config: Unrecognized CLI: {} | {} | {}'.format(line1, line2, line3))
                                    continue

                                m = re.match(r'^address-family ', line2)
                                if m:
                                    cmd = 'no ' + line2
                                    cmds.append_line(cmd)
                                    continue

                                # For debugging only...
                                if debug_clean_config:
                                    logger.warn('clean-config: Unrecognized CLI: {} | {}'.format(line1, line2))
                        continue

                    m = re.match(r'^interface (?!GCC\d)(?P<name>\S+)', line1) \
                        or re.match(r'^controller (?!OTU\d|ODU\d)(?P<name>\S+)', line1)
                    if m:
                        interface_name = m.group('name')
                        with cmds.submode_context(line1, cancel_empty=True):
                            is_mgmt = any(interface.name == interface_name
                                          for interface in l_netboot_intfs) \
                                or interface_name.startswith('MgmtEth') \
                                or interface_name.startswith('mgmt')
                            if not is_mgmt:
                                m = re.match(r'^vlan(?P<vlan_id>\d+)$', interface_name)
                                if m:
                                    vlan_id = int(m.group('vlan_id'))
                                    is_mgmt = vlan_id in l_netboot_switchport_access_vlans
                            need_shutdown = (not is_mgmt) \
                                and isinstance(self, NxosDevice)
                            is_system = False
                            for line2, subcli2 in subcli1 or ():
                                line2 = line2.strip()
                                m = re.match(r'^channel-group (?P<channel_group>\d+)', line2)
                                if m:
                                    channel_group = int(m.group('channel_group'))
                                    if channel_group in l_system_channel_groups:
                                        is_system = True
                                        break
                            if not is_system:
                                for line2, subcli2 in subcli1 or ():
                                    line2 = line2.strip()
                                    m = re.match(r'^!|^$', line2)
                                    if m:
                                        continue

                                    m = re.match(r'^description ', line2) \
                                        or re.match(r'^bundle', line2) \
                                        or re.match(r'^cdp', line2) \
                                        or re.match(r'^ip(v4)? addr', line2) \
                                        or re.match(r'^media-type ', line2) \
                                        or re.match(r'^mac-address ', line2) \
                                        or re.match(r'^switchport$', line2) \
                                        or re.match(r'^vrf member', line2) \
                                        or re.match(r'^ip vrf forwarding', line2) \
                                        or re.match(r'^vrf forwarding', line2)
                                    if m:
                                        if not is_mgmt:
                                            cmd = 'no ' + line2
                                            cmds.append_line(cmd)
                                        continue

                                    m = re.match(r'^no shutdown$', line2)
                                    if m:
                                        if not is_mgmt:
                                            need_shutdown = True
                                        continue

                                    m = re.match(r'^ipv6 ', line2) \
                                        or re.match(r'^mtu ', line2) \
                                        or re.match(r'^vrf', line2) \
                                        or re.match(r'^ip router', line2) \
                                        or re.match(r'^ip ospf', line2) \
                                        or re.match(r'^xconnect', line2) \
                                        or re.match(r'^service instance', line2) \
                                        or re.match(r'^l2transport', line2) \
                                        or re.match(r'^ip rsvp', line2) \
                                        or re.match(r'^mpls ip', line2) \
                                        or re.match(r'^mpls label', line2) \
                                        or re.match(r'^mpls traffic-eng', line2) \
                                        or re.match(r'^bundle id ', line2) \
                                        or re.match(r'^bundle-id ', line2) \
                                        or re.match(r'^channel-group ', line2) \
                                        or re.match(r'^lacp period', line2)
                                    if m:
                                        cmd = 'no ' + line2
                                        cmds.append_line(cmd)
                                        continue

                                    m = re.match(r'^(?P<kws>speed) ', line2)
                                    if m:
                                        cmd = 'no ' + m.group('kws')
                                        if is_mgmt:
                                            continue
                                        if re.match(r'^(?:' + r'|'.join([
                                                r'n3\d\d\d',
                                                r'n5\d\d\d',
                                        ]) + r')$', self.platform):
                                            # Don't touch...
                                            # neptune3:
                                            # NAME: "Chassis",  DESCR: "Nexus 3172 Chassis"
                                            # PID: N3K-C3172PQ-10GE    ,  VID: V02 ,  SN: FOC1844R1AW
                                            # NAME: "Slot 1",  DESCR: "48x10GE + 6x40G Supervisor"
                                            # PID: N3K-C3172PQ-10GE    ,  VID: V02 ,  SN: FOC18454MAA
                                            #   ERROR: Ethernet1/1: Configuration does not match the transceiver speed
                                            continue
                                        cmds.append_line(cmd)
                                        continue

                                    m = re.match(r'^(?P<kws>duplex) ', line2)
                                    if m:
                                        cmd = 'no ' + m.group('kws')
                                        if is_mgmt:
                                            continue
                                        cmds.append_line(cmd)
                                        continue

                                    m = re.match(r'^(?P<kws>port-mode) ', line2) \
                                        or re.match(r'^(?P<kws>loopback) ', line2)
                                    if m:
                                        cmd = 'no ' + m.group('kws')
                                        cmds.append_line(cmd)
                                        continue

                                    m = re.match(r'^shutdown$', line2)
                                    if m:
                                        need_shutdown = False
                                        continue

                                    m = re.match(r'^negotiation auto$', line2) \
                                        or re.match(r'^transceiver permit ', line2) \
                                        or re.match(r'^no ', line2)
                                    if m:
                                        # Ok... should not be test-affecting
                                        continue

                                    # For debugging only...
                                    if debug_clean_config:
                                        logger.warn('clean-config: Unrecognized CLI: {} | {}'.format(line1, line2))

                                if need_shutdown:
                                    cmds.append_line('shutdown')
                        continue

                    m = re.match(r'^Building configuration', line1) \
                        or re.match(r'^Current configuration', line1) \
                        or re.match(r'^D?RP/\d+/(RP|RSP)?\d+/(CPU)?\d+:', line1) \
                        or re.match(r'^boot-end-marker$', line1) \
                        or re.match(r'^boot-start-marker$', line1) \
                        or re.match(r'^control-plane$', line1) \
                        or re.match(r'^redundancy$', line1) \
                        or re.match(r'^boot system ', line1) \
                        or re.match(r'^card \d', line1) \
                        or re.match(r'^clock timezone ', line1) \
                        or re.match(r'^clock summer-time ', line1) \
                        or re.match(r'^enable password ', line1) \
                        or re.match(r'^exception crashinfo ', line1) \
                        or re.match(r'^exception choice ', line1) \
                        or re.match(r'^exception core-file ', line1) \
                        or re.match(r'^exception protocol ', line1) \
                        or re.match(r'^exception dump ', line1) \
                        or re.match(r'^facility-alarm ', line1) \
                        or re.match(r'^install feature-set ', line1) \
                        or re.match(r'^feature-set ', line1) \
                        or re.match(r'^feature ', line1) \
                        or re.match(r'^hostname ', line1) \
                        or re.match(r'^switchname ', line1) \
                        or re.match(r'^ip classless$', line1) \
                        or re.match(r'^domain name ', line1) \
                        or re.match(r'^ip domain name ', line1) \
                        or re.match(r'^ip gratuitous-arps$', line1) \
                        or re.match(r'^ip host ', line1) \
                        or re.match(r'^ip subnet-zero$', line1) \
                        or re.match(r'^ip tftp source-interface ', line1) \
                        or re.match(r'^licence grace-period$', line1) \
                        or re.match(r'^line ', line1) \
                        or re.match(r'^ntp ', line1) \
                        or re.match(r'^service internal', line1) \
                        or re.match(r'^service timestamps ', line1) \
                        or re.match(r'^username ', line1) \
                        or re.match(r'^version ', line1) \
                        or re.match(r'^qos match statistics per-', line1) \
                        or re.match(r'^ipv4 virtual address ', line1) \
                        or re.match(r'^logging ', line1) \
                        or re.match(r'^telnet vrf default ipv4 server max-servers ', line1) \
                        or re.match(r'^vty-pool default ', line1) \
                        or re.match(r'^no ', line1)
                    if m:
                        # Ok... should not be test-affecting
                        continue

                    # For debugging only...
                    if debug_clean_config:
                        logger.warn('clean-config: Unrecognized CLI: {}'.format(line1))

                if re.match(r'^(?:' + r'|'.join([
                        r'c?65\d\d',
                        r'c?3750',
                ]) + r')$', self.platform):
                    cmd = 'show vlan'
                    # TODO
                    # if { [OK] == [enaVerify "router_show '$cmd' result" {set kl [router_show -cmd $cmd -device $router -os_type ios] ; OK} [OK] -format ena_return_code -eval true -log false] } {
                    #     foreach vlan [keylkeys kl vlans] {
                    #         set cmd "no vlan $vlan"
                    #         if {
                    #             ![regexp default [keylget kl vlans.$vlan.name]] &&
                    #             [lsearch -exact $l_netboot_switchport_access_vlans $vlan] == -1 &&
                    #             [lsearch -exact $cmds_first $cmd] == -1 &&
                    #             [lsearch -exact $cmds $cmd] == -1 &&
                    #             [lsearch -exact $cmds_last $cmd] == -1
                    #         } {
                    #             lappend cmds $cmd
                    #         }
                    #     }
                    # }

                configurations.append_block(cmds_first)
                cmds_first.clear()
                configurations.append_block(cmds)
                cmds.clear()
                configurations.append_block(cmds_last)
                cmds_last.clear()

                if isinstance(self, NxosDevice):
                    if apply and configurations:
                        self.configure(str(configurations),
                                       # fail_invalid=True, -- best effort?
                                       )
                        configurations.clear()
                        # TODO enaTbClearFeatureCache $router
                        # Clear system-generated checkpoints to get rid of
                        # any disabled feature configs that could reappear.
                        cmd = 'clear checkpoint database system'
                        self.execute(cmd)

            if postclean:
                # ^MAGG(config)# copp profile strict^M^M
                # ^MThis operation can cause disruption of control traffic. Proceed (y/n)?  [no] ^M^M
                # TODO ignore {invalid-input commit-no-changes no-such-config}
                configurations.append_block(postclean)
                # TODO enaTbClearFeatureCache $router

        configurations.append_block(
            super().build_unconfig(clean=clean, apply=False,
                                   attributes=attributes, **kwargs))

        if apply:
            if configurations:
                self.configure(str(configurations),
                               # fail_invalid=True, -- best effort?
                               )
        else:
            # Return configuration
            return CliConfig(device=self, unconfig=True,
                             cli_config=configurations, fail_invalid=True)

