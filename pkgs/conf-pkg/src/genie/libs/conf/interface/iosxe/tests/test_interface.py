#!/usr/bin/env python

# python
import unittest
from unittest.mock import Mock

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# xBU-shared genie pacakge
from genie.libs.conf.interface import TunnelTeInterface
from genie.libs.conf.base import MAC, IPv4Interface, IPv6Interface, IPv4Address, IPv6Address
from genie.libs.conf.interface import Layer, L2_type, IPv4Addr, IPv6Addr
from genie.libs.conf.vrf import Vrf


class test_interface(TestCase):

    maxDiff = None

    def test_TunnelTeInterface(self):
        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxe')
        lo0 = Interface(device=dev1, name='Loopback0')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/1')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/2')
        intf1.ipv4 = '1.2.3.4/32'
        tun3 = Interface(device=dev1, name='Tunnel101', tunnel_mode='mpls traffic-eng')
        # tun3 = TunnelTeInterface(device=dev1, name='Tunnel101')
        self.assertTrue(isinstance(tun3, TunnelTeInterface))
        self.assertEqual(tun3.interface_number, 101)
        tun3.destination = intf1.ipv4.ip
        tun3.autoroute_announce = True
        tun3.ipv4_unnumbered_interface = dev1.interfaces['Loopback0']
        tun3.add_path_option(1)
        tun3.path_option_attr[1].dynamic = True
        tun3.add_path_option(2)
        tun3.path_option_attr[2].explicit_name = "exp_PE2_P1_PE1"
        cfg = tun3.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'interface Tunnel101',
            ' tunnel mode mpls traffic-eng',
            ' ip unnumbered Loopback0',
            ' tunnel destination 1.2.3.4',
            ' tunnel mpls traffic-eng autoroute announce',
            ' tunnel mpls traffic-eng path-option 1 dynamic',
            ' tunnel mpls traffic-eng path-option 2 explicit name exp_PE2_P1_PE1',
            ' exit',
        ]))

        uncfg = tun3.build_unconfig(apply=False)
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'no interface Tunnel101',
        ]))

        partial_uncfg = tun3.build_unconfig(apply=False,attributes='autoroute_announce')
        self.assertMultiLineEqual(str(partial_uncfg), '\n'.join([
            'interface Tunnel101',
            ' no tunnel mpls traffic-eng autoroute announce',
            ' exit',
        ]))

        partial_cfg1 = tun3.build_config(apply=False,attributes='path_option_attr__2')
        self.assertMultiLineEqual(str(partial_cfg1), '\n'.join([
            'interface Tunnel101',
            ' tunnel mpls traffic-eng path-option 2 explicit name exp_PE2_P1_PE1',
            ' exit',
        ]))

    # def test_LoopbackInterface(self):
    #     Genie.testbed = Testbed()
    #     dev1 = Device(name='PE1', os='iosxe')
    #     intf1 = Interface(device=dev1, name='Loopback0')
    #     intf1.ipv4 = '1.2.3.4/32'
    #     intf1.ipv6 = '2001:0:0::1/128'
    #     cfg = intf1.build_config(apply=False)
    #     self.assertMultiLineEqual(str(cfg), '\n'.join([
    #         'interface Loopback0',
    #         ' ip address 1.2.3.4 255.255.255.255',
    #         ' ipv6 address 2001::1/128',
    #         ' exit',
    #     ]))
    #     uncfg = intf1.build_unconfig(apply=False)
    #     self.assertMultiLineEqual(str(uncfg), '\n'.join([
    #         'no interface Loopback0',
    #     ]))

    def test_EthernetInterface(self):
        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/1')
        intf1.ipv4 = '1.2.3.4/32'
        intf1.auto_negotiation = True
        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' ip address 1.2.3.4 255.255.255.255',
            ' negotiation auto',
            ' exit',
        ]))
        uncfg = intf1.build_unconfig(apply=False)
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'default interface GigabitEthernet0/0/1',
            'interface GigabitEthernet0/0/1',
            'shutdown',
        ]))
        partial_uncfg1 = intf1.build_unconfig(apply=False,attributes="auto_negotiation")
        self.assertMultiLineEqual(str(partial_uncfg1), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' default negotiation auto',
            ' exit',
        ]))

        partial_uncfg2 = intf1.build_unconfig(apply=False, attributes="ipv4")
        self.assertMultiLineEqual(str(partial_uncfg2), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' no ip address 1.2.3.4 255.255.255.255',
            ' exit',
        ]))

        # FiftyGig interface
        intf2 = Interface(device=dev1, name='FiftyGigE6/0/1')
        intf2.ipv4 = '10.20.30.40/24'
        intf2.shutdown = False
        cfg = intf2.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'interface FiftyGigE6/0/1',
            ' ip address 10.20.30.40 255.255.255.0',
            ' no shutdown',
            ' exit'
        ]))
        uncfg = intf2.build_unconfig(apply=False)
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'default interface FiftyGigE6/0/1',
            'interface FiftyGigE6/0/1',
            'shutdown'
        ]))


    def test_EthernetSubInterface(self):
        """Test subinterface support without usage of service_instance"""
        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxe')

        sub_intf = Interface(device=dev1, name='GigabitEthernet0/0/1.20')

        sub_intf.ipv4 = '10.10.0.1/24'
        sub_intf.eth_encap_type1 = 'dot1q'
        sub_intf.eth_encap_val1 = 20

        cfg = sub_intf.build_config(apply=False)

        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'interface GigabitEthernet0/0/1.20',
            ' encapsulation dot1q 20',
            ' ip address 10.10.0.1 255.255.255.0',
            ' exit',
        ]))

        uncfg = sub_intf.build_unconfig(apply=False)
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'no interface GigabitEthernet0/0/1.20',
        ]))


    def test_EFPInterface(self):
        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/1')
        efp = Interface(device=dev1, name='GigabitEthernet0/0/1.20',service_instance=20)
        efp.eth_encap_val1 = 20
        efp.rewrite_ingress = 'pop 1 symmetric'
        cfg = efp.build_config(apply=False)

        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' service instance 20 ethernet',
            '  encapsulation dot1q 20',
            '  rewrite ingress tag pop 1 symmetric',
            '  exit',
            ' exit',
        ]))

        uncfg = efp.build_unconfig(apply=False)
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' no service instance 20 ethernet',
            ' exit',
        ]))

    def test_VlanInterface(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        intf1 = Interface(name='Vlan100',device=dev1)

        # Defining attributes section
        intf1.mtu = 500
        intf1.ipv4 = '201.0.12.1'
        intf1.ipv4.netmask = '255.255.255.0'
        intf1.ipv6 = '2001::12:1'

        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(
            str(cfg),
            '\n'.join([
                'interface Vlan100',
                ' ip address 201.0.12.1 255.255.255.0',
                ' ipv6 address 2001::12:1/128',
                ' mtu 500',
                ' exit',
            ]))

        uncfg = intf1.build_unconfig(apply=False)
        self.assertMultiLineEqual(
            str(uncfg),
            '\n'.join([
                'no interface Vlan100',
            ]))

        partial_uncfg = intf1.build_unconfig(apply=False,attributes="mtu")
        self.assertMultiLineEqual(str(partial_uncfg), '\n'.join([
            'interface Vlan100',
            ' no mtu 500',
            ' exit',
        ]))

    def test_InterfaceSwitchport(self):
        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/1')

        # Do not set switchport - default
        # Check config
        cfg1 = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg1), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' exit',
        ]))

        # Set switchport to True
        intf1.switchport = True
        # Check config
        cfg2 = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg2), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' switchport',
            ' exit',
        ]))
        # Check unconfig
        uncfg2 = intf1.build_unconfig(apply=False, attributes="switchport")
        self.assertMultiLineEqual(str(uncfg2), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' no switchport',
            ' exit',
        ]))

        # Set switchport to False
        intf1.switchport = False
        # Check config
        cfg3 = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg3), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' no switchport',
            ' exit',
        ]))
        # Check unconfig
        uncfg3 = intf1.build_unconfig(apply=False, attributes="switchport")
        self.assertMultiLineEqual(str(uncfg3), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' switchport',
            ' exit',
        ]))

        # test full switchport related configuration
        intf1.switchport_enable = True
        intf1.switchport_mode = "access"
        intf1.access_vlan = "100"
        intf1.trunk_vlans = "all"
        intf1.trunk_add_vlans = "100"
        intf1.trunk_remove_vlans = "100-200"
        intf1.native_vlan = "1"

        cfg1 = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg1), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' switchport',
            ' switchport mode access',
            ' switchport trunk allowed vlan all',
            ' switchport trunk native vlan 1',
            ' switchport access vlan 100',
            ' switchport trunk allowed vlan add 100',
            ' switchport trunk allowed vlan remove 100-200',
            ' exit',
        ]))

    def test_all_ethernet(self):
        testbed = Testbed()
        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/1')
        vrf = Vrf(name='test', testbed=testbed)
        dev1.add_feature(vrf)

        # Defining attributes section
        intf1.description = 'test desc'
        intf1.enabled = True
        intf1.link_up_down_trap_enable = True
        intf1.mtu = 500
        intf1.vrf = vrf
        intf1.vrf_downstream = 'vrf_downstream_test'
        intf1.mac_address = 'aaaa.bbbb.cccc'
        intf1.bandwidth = 768
        intf1.link_status = True
        intf1.load_interval = 30
        intf1.encapsulation = 'dot1q'
        intf1.first_dot1q = '20'
        intf1.second_dot1q = '30'

        ipv4a = IPv4Addr(device=dev1)
        ipv4a.ipv4 = IPv4Address('192.168.1.1')
        ipv4a.prefix_length = '24'
        intf1.add_ipv4addr(ipv4a)
        ipv4b = IPv4Addr(device=dev1)
        ipv4b.ipv4 = IPv4Address('192.168.1.2')
        ipv4b.prefix_length = '24'
        ipv4b.ipv4_secondary = True
        intf1.add_ipv4addr(ipv4b)

        ipv6a = IPv6Addr(device=dev1)
        ipv6a.ipv6 = IPv6Address('2001:db1:1::1')
        ipv6a.ipv6_prefix_length = '64'
        intf1.add_ipv6addr(ipv6a)
        ipv6b = IPv6Addr(device=dev1)
        ipv6b.ipv6 = IPv6Address('2001:db1:2::2')
        ipv6b.ipv6_prefix_length = '64'
        intf1.add_ipv6addr(ipv6b)
        ipv6b.ipv6_anycast = True

        intf1.dhcp = True
        intf1.dhcp_client_id = '10'
        intf1.dhcp_hostname = 'dhcp-host'
        intf1.unnumbered_intf_ref = 'GigabitEthernet0/0/2.20'
        intf1.ipv6_unnumbered_intf_ref = 'GigabitEthernet0/0/3.100'
        intf1.ipv6_enabled = True
        intf1.ipv6_autoconf = True
        intf1.ipv6_autoconf_default = True
        intf1.medium = "broadcast"
        intf1.delay = 100
        intf1.port_speed = '1000'
        intf1.auto_negotiate = True
        intf1.duplex_mode = "full"
        intf1.flow_control_receive = True
        intf1.flow_control_send = False


        # Check config
        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' encapsulation dot1q 20 second-dot1q 30',
            ' vrf forwarding test downstream vrf_downstream_test',
            ' description test desc',
            ' bandwidth 768',
            ' mtu 500',
            ' no shutdown',
            ' snmp trap link-status',
            ' logging event link-status',
            ' load-interval 30',
            ' ipv6 enable',
            ' ipv6 address autoconfig default',
            ' ip unnumbered GigabitEthernet0/0/2.20',
            ' ipv6 unnumbered GigabitEthernet0/0/3.100',
            ' speed 1000',
            ' negotiation auto',
            ' duplex full',
            ' flowcontrol receive on',
            ' flowcontrol send off',
            ' ip address dhcp client-id 10 hostname dhcp-host',
            ' medium broadcast',
            ' delay 100',
            ' ip address 192.168.1.1 255.255.255.0',
            ' ip address 192.168.1.2 255.255.255.0 secondary',
            ' ipv6 address 2001:db1:1::1/64',
            ' ipv6 address 2001:db1:2::2/64 anycast',
            ' mac-address aaaa.bbbb.cccc',
            ' exit',
        ]))

        # Check unconfig without attribtues
        uncfg = intf1.build_unconfig(apply=False)
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'default interface GigabitEthernet0/0/1',
            'interface GigabitEthernet0/0/1',
            'shutdown',
        ]))

        # Check ipv4 unconfig
        uncfg = intf1.build_unconfig(apply=False, attributes="ipv4addr")
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' no ip address 192.168.1.1 255.255.255.0',
            ' no ip address 192.168.1.2 255.255.255.0 secondary',
            ' exit',
        ]))

        # Check encapsulation unconfig
        uncfg = intf1.build_unconfig(apply=False, attributes={"encapsulation": None,
                                                              "first_dot1q": None})
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' no encapsulation dot1q',
            ' exit',
        ]))

    def test_enabled_switchport_enabled(self):
        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/1')

        # Defining attributes section
        intf1.switchport_enable = True
        intf1.enabled = True

        # Check config
        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' no shutdown',
            ' switchport',
            ' exit',
        ]))

        # Check unconfig
        uncfg = intf1.build_unconfig(apply=False, attributes={"switchport_enable": True,
                                                              "enabled": True})
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' shutdown',
            ' no switchport',
            ' exit',
        ]))

        # Defining attributes section
        intf1.switchport_enable = False
        intf1.enabled = False

        # Check config
        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' shutdown',
            ' no switchport',
            ' exit',
        ]))

        # Check unconfig
        uncfg = intf1.build_unconfig(apply=False, attributes={"switchport_enable": True,
                                                              "enabled": True})
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' no shutdown',
            ' switchport',
            ' exit',
        ]))

    def test_virtual(self):
        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='Vlan100')
        intf2 = Interface(device=dev1, name='Loopback10')


        # Defining attributes section
        intf1.enabled = True
        intf2.enabled = False

        # Check config
        cfg1 = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg1), '\n'.join([
            'interface Vlan100',
            ' no shutdown',
            ' exit',
        ]))
        # Check unconfig
        uncfg1 = intf1.build_unconfig(apply=False)
        self.assertMultiLineEqual(str(uncfg1), '\n'.join([
            'no interface Vlan100',
        ]))

        # Check config
        cfg2 = intf2.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg2), '\n'.join([
            'interface Loopback10',
            ' shutdown',
            ' exit',
        ]))

        # Check unconfig
        uncfg2 = intf2.build_unconfig(apply=False)
        self.assertMultiLineEqual(str(uncfg2), '\n'.join([
            'no interface Loopback10',
        ]))

        # Check unconfig with attributes
        uncfg2 = intf2.build_unconfig(apply=False, attributes="enabled")
        self.assertMultiLineEqual(str(uncfg2), '\n'.join([
            'interface Loopback10',
            ' no shutdown',
            ' exit',
        ]))

    def test_lag_interafce(self):
        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='GigabitEthernet1/0/1')
        intf2 = Interface(device=dev1, name='GigabitEthernet1/0/2')
        intf3 = Interface(device=dev1, name='Port-channel10')

        # lacp
        intf1.lag_bundle_id = 10
        intf1.lag_activity = 'active'
        intf1.lag_lacp_port_priority = 30
        # pagp
        intf2.lag_bundle_id = 20
        intf2.lag_activity = 'auto'
        intf2.lag_non_silent = True
        intf2.lag_pagp_port_priority = 50

        # virtual lagInterface        
        intf3.lag_lacp_system_priority = 100
        intf3.lag_lacp_max_bundle = 20
        intf3.lag_lacp_min_bundle = 15

        # error assigned attributes, shouldn't in the configuration
        intf2.lag_lacp_max_bundle = 123
        
        # Check config
        cfg1 = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg1), '\n'.join([
            'interface GigabitEthernet1/0/1',
            ' channel-group 10 mode active',
            ' lacp port-priority 30',
            ' exit',
        ]))

        cfg2 = intf2.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg2), '\n'.join([
	        'interface GigabitEthernet1/0/2',
			' channel-group 20 mode auto non-silent',
			' pagp port-priority 50',
			' exit',
        ]))

        cfg3 = intf3.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg3), '\n'.join([
            'lacp system-priority 100',
            'interface Port-channel10',
            ' lacp max-bundle 20',
            ' lacp min-bundle 15',
            ' exit',
        ]))

        # Check unconfig
        uncfg1 = intf1.build_unconfig(apply=False)
        self.assertMultiLineEqual(str(uncfg1), '\n'.join([
            'default interface GigabitEthernet1/0/1',
			'interface GigabitEthernet1/0/1',
			'shutdown',
        ]))

        uncfg2 = intf2.build_unconfig(apply=False)
        self.assertMultiLineEqual(str(uncfg2), '\n'.join([
            'default interface GigabitEthernet1/0/2',
			'interface GigabitEthernet1/0/2',
			'shutdown',
        ]))

        # Check unconfig with attributes
        uncfg1 = intf1.build_unconfig(apply=False, attributes={'lag_activity': None, 
        	                                                   'lag_bundle_id': None})
        self.assertMultiLineEqual(str(uncfg1), '\n'.join([
	        'interface GigabitEthernet1/0/1',
			' no channel-group 10 mode active',
			' exit',
        ]))

        uncfg2 = intf2.build_unconfig(apply=False, attributes="lag_pagp_port_priority")
        self.assertMultiLineEqual(str(uncfg2), '\n'.join([
	        'interface GigabitEthernet1/0/2',
			' no pagp port-priority 50',
			' exit',
        ]))

    def test_NveInterface_L2vni_mcast(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        intf1 = Interface(name='nve1',device=dev1)

        # Defining attributes section
        intf1.nve_bgp_host_reachability = True
        intf1.nve_src_intf_loopback = 'Loopback0'

        intf1.nve_vni= '20000'
        intf1.nve_vni_mcast_group = '239.1.1.2'
        intf1.nve_vni_local_routing = True

        # Build config
        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(
            str(cfg),
            '\n'.join([
                'interface nve1',
                ' host-reachability protocol bgp',
                ' source-interface Loopback0',
                ' member vni 20000',
                '  mcast-group 239.1.1.2 local-routing',
                '  exit',
                ' exit'
            ]))

        # Build unconfig
        partial_uncfg_1 = intf1.build_unconfig(apply=False, attributes={
                                               'nve_bgp_host_reachability': True,
                                               'nve_vni': '20000'})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(partial_uncfg_1),
            '\n'.join([
                'interface nve1',
                ' no host-reachability protocol bgp',
                ' no member vni 20000',
                ' exit'
            ]))

        # Build unconfig
        partial_uncfg_2 = intf1.build_unconfig(apply=False, attributes={
                                               'nve_src_intf_loopback': 'Loopback0'})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(partial_uncfg_2),
            '\n'.join([
                'interface nve1',
                ' no source-interface Loopback0',
                ' exit'
            ]))

    def test_NveInterface_L2vni_ir(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        intf1 = Interface(name='nve1',device=dev1)

        # Defining attributes section
        intf1.nve_bgp_host_reachability = True
        intf1.nve_src_intf_loopback = 'Loopback0'

        intf1.nve_vni= '20000'
        intf1.nve_vni_ingress_replication = True

        # Build config
        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(
            str(cfg),
            '\n'.join([
                'interface nve1',
                ' host-reachability protocol bgp',
                ' source-interface Loopback0',
                ' member vni 20000',
                '  ingress-replication',
                '  exit',
                ' exit'
            ]))

        # Build unconfig
        uncfg= intf1.build_unconfig(apply=False, attributes={'nve_vni': '20000'})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfg),
            '\n'.join([
                'interface nve1',
                ' no member vni 20000',
                ' exit'
            ]))

    def test_NveInterface_L3vni(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        intf1 = Interface(name='nve1',device=dev1)

        # Defining attributes section
        intf1.nve_bgp_host_reachability = True
        intf1.nve_src_intf_loopback = 'Loopback0'

        intf1.nve_vni= '30000'
        intf1.nve_vni_vrf = 'red'

        # Build config
        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(
            str(cfg),
            '\n'.join([
                'interface nve1',
                ' host-reachability protocol bgp',
                ' source-interface Loopback0',
                ' member vni 30000 vrf red',
                ' exit'
            ]))

        # Build unconfig
        uncfg= intf1.build_unconfig(apply=False, attributes={'nve_vni': '20000'})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfg),
            '\n'.join([
                'interface nve1',
                ' no member vni 30000',
                ' exit'
            ]))

if __name__ == '__main__':
    unittest.main()

