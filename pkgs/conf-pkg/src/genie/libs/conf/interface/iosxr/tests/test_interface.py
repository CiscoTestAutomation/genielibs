#!/usr/bin/env python

# Python
import unittest
import itertools

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# Genie XBu_shared
from genie.libs.conf.interface import NamedTunnelTeInterface, \
    LoopbackInterface, SubInterface, IPv4Addr, IPv6Addr
from genie.libs.conf.base import IPv4Address, IPv6Address
from genie.libs.conf.vlan import Vlan
from genie.libs.conf.vrf import Vrf

# vni
from genie.libs.conf.evpn.vni import Vni


class test_interface(TestCase):

    def test_vni_lines_confg(self):
        # For failures
        self.maxDiff = None

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='PE1', testbed=testbed, os='iosxr')
        intf1 = Interface(name='nve100', device=dev1, \
            aliases=['PE1_1'])

        # Apply configuration
        intf1.source_interface = Interface(name='Loopback0', device=dev1)
        vni = Vni(100, device=dev1)
        vni.mcast_group = '225.1.1.1 0.0.0.0'
        intf1.add_vni(vni)

        # Build config
        cfgs = intf1.build_config(apply=False)

        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface nve100',
                ' member vni 100',
                '  mcast-group 225.1.1.1 0.0.0.0',
                '  exit',
                ' source-interface Loopback0',
                ' exit'
                ]))        

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False, attributes={'vnis':None})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface nve100',
                ' no member vni 100',
                ' exit'
                ]))  

    def test_TunnelTeInterface(self):

        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxr')
        lo0 = Interface(device=dev1, name='Loopback0')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2')

        intf1.ipv4 = '1.2.3.4/32'
        tun3 = Interface(device=dev1, name='tunnel-te101')
        self.assertEqual(tun3.interface_number, 101)
        tun3.destination = intf1.ipv4.ip
        tun3.autoroute_announce = True
        tun3.ipv4_unnumbered_interface = dev1.interfaces['Loopback0']
        tun3.auto_bw_adj_threshold_pct = 1
        tun3.add_path_option(1)
        tun3.path_option_attr[1].dynamic = True
        tun3.add_path_option(2)
        tun3.path_option_attr[2].explicit_name = "exp_PE2_P1_PE1"
        cfg = tun3.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'interface tunnel-te101',
            ' destination 1.2.3.4',
            ' autoroute announce',
            ' auto-bw adjustment-threshold 1',
            ' ipv4 unnumbered Loopback0',
            ' path-option 1 dynamic',
            ' path-option 2 explicit name exp_PE2_P1_PE1',
            ' exit',
        ]))

    def test_NamedTunnelTeInterface(self):

        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxr')
        lo0 = Interface(device=dev1, name='Loopback0')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2')

        tun = NamedTunnelTeInterface(device=dev1, name='DR01CBF23-1234AMS1')
        tun.add_path_option("BD01TUL17-DR01CBF24-DYN")
        tun.path_option_attr["BD01TUL17-DR01CBF24-DYN"].preference = 10
        tun.path_option_attr["BD01TUL17-DR01CBF24-DYN"].computation = "dynamic"
        tun.autoroute_announce_metric = 1015
        tun.destination = "64.233.174.43"
        tun.affinity_exclude = ['red', 'EDGE', 'ACCESS', 'PEERING']
        cfg = tun.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'mpls traffic-eng',
            ' named-tunnels',
            '  tunnel-te DR01CBF23-1234AMS1',
            '   destination 64.233.174.43',
            '   autoroute announce metric 1015',
            '   affinity exclude red EDGE ACCESS PEERING',
            '   path-option BD01TUL17-DR01CBF24-DYN',
            '    computation dynamic',
            '    preference 10',
            '    exit',
            '   exit',
            '  exit',
            ' exit',
        ]))

        tun2 = NamedTunnelTeInterface(device=dev1,
                                      name='BD01TUL17-DR01CBF24-HIPRI-1')
        tun2.add_path_option("BD01TUL17-DR01CBF24-DYN")
        tun2.path_option_attr["BD01TUL17-DR01CBF24-DYN"].computation = "dynamic"
        tun2.path_option_attr["BD01TUL17-DR01CBF24-DYN"].preference = 10
        tun2.add_path_option(2)
        tun2.path_option_attr[2].preference = 20
        tun2.auto_bw = True
        tun2.auto_bw_bwlimit_min = 200
        tun2.auto_bw_bwlimit_max = 1000
        tun2.auto_bw_adj_threshold_pct = 10
        tun2.auto_bw_adj_threshold_min = 10
        tun2.auto_bw_application_freq = 1800
        tun2.priority_setup = 5
        tun2.priority_hold = 5
        tun2.destination = "64.233.174.44"
        tun2.frr_protect_bandwidth = True
        tun2.frr_protect = "node bandwidth"
        tun2.affinity_exclude = ['red', 'EDGE', 'ACCESS', 'orange', 'PEERING']
        cfg = tun2.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'mpls traffic-eng',
            ' named-tunnels',
            '  tunnel-te BD01TUL17-DR01CBF24-HIPRI-1',
            '   destination 64.233.174.44',
            '   affinity exclude red EDGE ACCESS orange PEERING',
            '   auto-bw',
            '   auto-bw adjustment-threshold 10 min 10',
            '   auto-bw application 1800',
            '   auto-bw bw-limit min 200 max 200',
            '   priority 5 5',
            '   fast-reroute protect node bandwidth',
            '   path-option 2',
            '    preference 20',
            '    exit',
            '   path-option BD01TUL17-DR01CBF24-DYN',
            '    computation dynamic',
            '    preference 10',
            '    exit',
            '   exit',
            '  exit',
            ' exit',
        ]))

    def test_BundleEtherInterface(self):

        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxr')
        lo0 = Interface(device=dev1, name='Loopback0')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2')

        bundle = Interface(device=dev1, name='Bundle-Ether1')
        self.assertEqual(bundle.interface_number, 1)
        bundle.ipv4 = '14.14.14.14/24'
        bundle.ipv6 = '14:14:14::4/64'
        bundle.lag_bfd_v4_destination = '5.0.0.97'
        bundle.lag_bfd_v4_fast_detect = True
        bundle.lag_bfd_v4_min_interval = 100
        bundle.lag_bfd_v6_destination = '6.0.0.98'
        bundle.lag_bfd_v6_fast_detect = True
        bundle.lag_bfd_v6_min_interval = 200

        intf1.bundle = bundle
        intf1.bundle_mode = 'active'

        intf2.bundle = bundle

        cfg = bundle.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'interface Bundle-Ether1',
            ' ipv4 address 14.14.14.14/24',
            ' ipv6 address 14:14:14::4/64',
            ' bfd address-family ipv4 destination 5.0.0.97',
            ' bfd address-family ipv4 fast-detect',
            ' bfd address-family ipv4 minimum-interval 100',
            ' bfd address-family ipv6 destination 6.0.0.98',
            ' bfd address-family ipv6 fast-detect',
            ' bfd address-family ipv6 minimum-interval 200',
            ' exit',
        ]))

        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'interface GigabitEthernet0/0/0/1',
            ' bundle id 1 mode active',
            ' exit',
        ]))

        cfg = intf2.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'interface GigabitEthernet0/0/0/2',
            ' bundle id 1',
            ' exit',
        ]))

    def test_generate_unused_interface_name(self):

        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxr')

        s = LoopbackInterface._generate_unused_interface_name(device=dev1)
        # print(s)
        self.assertRegex(s, '[lL]oopback0')
        s = LoopbackInterface._generate_unused_interface_name(device=dev1)
        self.assertRegex(s, '[lL]oopback0')
        lo0 = Interface(device=dev1, name=s)
        s = LoopbackInterface._generate_unused_interface_name(device=dev1)
        self.assertRegex(s, '[lL]oopback1')
        s = LoopbackInterface._generate_unused_interface_name(device=dev1)
        self.assertRegex(s, '[lL]oopback1')
        lo1 = Interface(device=dev1, name=s)
        lo2 = LoopbackInterface.generate_interface(device=dev1)
        self.assertRegex(lo2.name, '[lL]oopback2')
        lo3 = LoopbackInterface.generate_interface(device=dev1, range=itertools.count(1000))
        self.assertRegex(lo3.name, '[lL]oopback1000')
        lo4 = LoopbackInterface.generate_interface(device=dev1, range=itertools.count(1000))
        self.assertRegex(lo4.name, '[lL]oopback1001')
        r = itertools.count(1000)
        lo5 = LoopbackInterface.generate_interface(device=dev1, range=r)
        self.assertRegex(lo5.name, '[lL]oopback1002')
        s = LoopbackInterface._generate_unused_interface_name(device=dev1, range=r)
        self.assertRegex(s, '[lL]oopback1003')
        s = LoopbackInterface._generate_unused_interface_name(device=dev1, range=r)
        self.assertRegex(s, '[lL]oopback1004')

        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/0')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/1')
        s = SubInterface._generate_unused_sub_interface_name(parent_interface=intf1)
        self.assertEqual(s, intf1.name + '.0')
        s = SubInterface._generate_unused_sub_interface_name(parent_interface=intf1)
        self.assertEqual(s, intf1.name + '.0')
        sub0 = Interface(device=dev1, name=s)
        s = SubInterface._generate_unused_sub_interface_name(parent_interface=intf1)
        self.assertEqual(s, intf1.name + '.1')
        s = SubInterface._generate_unused_sub_interface_name(parent_interface=intf1)
        self.assertEqual(s, intf1.name + '.1')
        sub1 = intf1.generate_sub_interface()
        self.assertEqual(sub1.name, intf1.name + '.1')
        sub2 = intf1.generate_sub_interface()
        self.assertEqual(sub2.name, intf1.name + '.2')
        sub3 = intf2.generate_sub_interface()
        self.assertEqual(sub3.name, intf2.name + '.0')
        sub4 = intf2.generate_sub_interface(range=[100, 200])
        self.assertEqual(sub4.name, intf2.name + '.100')
        sub5 = intf2.generate_sub_interface(range=[100, 200])
        self.assertEqual(sub5.name, intf2.name + '.200')
        with self.assertRaisesRegex(TypeError, r'^No more .* subinterface numbers available'):
            intf2.generate_sub_interface(range=[100, 200])

    def test_clean_short_interface_name(self):

        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxr')

        for clean, short in (
                # Generic
                ('GigabitEthernet0/0/0/0', 'gi0/0/0/0'),
                ('tunnel-te1', 'tt1'),
                # Special cases
                ('Loopback0', 'Lo0'),
                ('tunnel-tp1', 'tp1'),
                ('GCC0', 'g0'),
                ('OTU2', 'O2'),
                ('OTU1E', 'O1E'),
                ('OTU3E2', 'O3E2'),
                ('ODU3', 'd3'),
                ('ODU2F', 'd2F'),
                ('ODU3E2', 'd3E2'),
        ):
            self.assertEqual(dev1.clean_interface_name(clean), clean)
            self.assertEqual(dev1.clean_interface_name(clean.replace('/', '_')), clean)
            self.assertEqual(dev1.clean_interface_name(short), clean)
            self.assertEqual(dev1.clean_interface_name(short.lower()), clean)
            self.assertEqual(dev1.clean_interface_name(short.upper()), clean)

    def test_vlan_interface_confoguration(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        intf1 = Interface(name='GigabitEthernet0/0/1',device=dev1)
        intf2 = Interface(name='GigabitEthernet0/0/2',device=dev2)
        intf3 = Interface(name='GigabitEthernet0/0/3',device=dev1)
        link = Link(name='1_2_1',testbed=testbed)
        link.connect_interface(interface=intf1)
        link.connect_interface(interface=intf2)
        vlan = Vlan()
        link.add_feature(vlan)

        vlan.device_attr[dev1]
        vlan.device_attr[dev2]

        # Defining attributes section
        intf1.transceiver_permit_pid_all = True
        intf1.duplex = 'full'
        intf1.mac_address = 'aaaa.bbbb.cccc'
        intf1.eth_encap_type1 = 'dot1q'
        intf1.eth_encap_val1 = 2
        intf1.eth_encap_val2 = 5
        intf1.eth_dot1q_type = 'tunneling ethertype'
        intf1.eth_dot1q_value = '0x9100'
        intf1.ipv4 = '201.0.12.1'

        intf2.eth_dot1q_type = 'native vlan'
        intf2.eth_dot1q_value = '15'

        cfg1 = intf1.build_config(apply=False)
        self.assertMultiLineEqual(
            str(cfg1),
            '\n'.join([
                'interface GigabitEthernet0/0/1',
                ' dot1q tunneling ethertype 0x9100',
                ' encapsulation dot1q 2 second-dot1q 5',
                ' ipv4 address 201.0.12.1/32',
                ' transceiver permit pid all',
                ' duplex full',
                ' mac-address aaaa.bbbb.cccc',
                ' exit',
            ]))

        cfg2 = intf2.build_config(apply=False)
        self.assertMultiLineEqual(
            str(cfg2),
            '\n'.join([
                'interface GigabitEthernet0/0/2',
                ' dot1q native vlan 15',
                ' exit',
            ]))

        uncfg = intf1.build_unconfig(apply=False, attributes={'mac_address': True,
                                                              'duplex': True,
                                                              'ipv4': True,
                                                              'eth_dot1q_value': True,
                                                              'eth_encap_type1': True,})
        self.assertMultiLineEqual(
            str(uncfg),
            '\n'.join([
                'interface GigabitEthernet0/0/1',
                ' no encapsulation dot1q 2 second-dot1q 5',
                ' no ipv4 address 201.0.12.1/32',
                ' no duplex full',
                ' no mac-address',
                ' exit',
            ]))

class test_xr_interface(TestCase):

    def test_single_line_config(self):

        # For failures
        self.maxDiff = None

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='PE1', testbed=testbed, os='iosxr')
        intf1 = Interface(name='GigabitEthernet0/0/0/0', device=dev1, aliases=['PE1_1'])
        subif1 = Interface(name='GigabitEthernet0/0/0/1.10', device=dev1, aliases=['PE1_1'])
        vrf = Vrf(name='test', testbed=testbed)
        dev1.add_feature(vrf)

        # Apply configuration
        intf1.description = 'test'
        intf1.enabled = True
        intf1.mtu = 1492
        intf1.vrf = vrf
        intf1.mac_address = 'aabb.ccdd.eeff'
        intf1.bandwidth = 8192
        intf1.load_interval = 33
        intf1.unnumbered_intf_ref = 'GigabitEthernet0/0/0/1.10'
        intf1.ipv6_autoconf = True
        intf1.medium = 'p2p'

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface GigabitEthernet0/0/0/0',
                ' bandwidth 8192',
                ' description test',
                ' vrf test',
                ' ipv4 point-to-point',
                ' ipv4 unnumbered GigabitEthernet0/0/0/1.10',
                ' ipv6 address autoconfig',
                ' load-interval 33',
                ' mtu 1492',
                ' no shutdown',
                ' mac-address aabb.ccdd.eeff',
                ' exit'
                ]))

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'no interface GigabitEthernet0/0/0/0',
                ]))

    def test_ipv4_multiple_lines_confg(self):
        # For failures
        self.maxDiff = None

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='PE1', testbed=testbed, os='iosxr')
        intf1 = Interface(name='GigabitEthernet0/0/0/0', device=dev1, \
            aliases=['PE1_1'])
        vrf = Vrf(name='test', testbed=testbed)
        dev1.add_feature(vrf)

        # Apply configuration
        intf1.description = 'multiple lines config'

        ipv4a = IPv4Addr(device=dev1)
        ipv4a.ipv4 = IPv4Address('192.168.1.1')
        ipv4a.prefix_length = '24'
        intf1.add_ipv4addr(ipv4a)
        ipv4b = IPv4Addr(device=dev1)
        ipv4b.ipv4 = IPv4Address('192.168.1.2')
        ipv4b.prefix_length = '24'
        ipv4b.ipv4_secondary = True
        intf1.add_ipv4addr(ipv4b)
        intf1.enabled = True

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface GigabitEthernet0/0/0/0',
                ' ipv4 address 192.168.1.1/24',
                ' ipv4 address 192.168.1.2/24 secondary',
                ' description multiple lines config',
                ' no shutdown',
                ' exit'
                ]))

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False, attributes={'ipv4addr':None,
                                                               'enabled': True,
                                                               'description': True})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface GigabitEthernet0/0/0/0',
                ' no ipv4 address 192.168.1.1/24',
                ' no ipv4 address 192.168.1.2/24 secondary',
                ' no description',
                ' shutdown',
                ' exit'
                ]))        

    def test_ipv6_multiple_lines_confg(self):
        # For failures
        self.maxDiff = None

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        dev1 = Device(name='PE1', testbed=testbed, os='iosxr')
        intf1 = Interface(name='GigabitEthernet0/0/0/0', device=dev1, \
            aliases=['PE1_1'])
        vrf = Vrf(name='test', testbed=testbed)
        dev1.add_feature(vrf)

        # Apply configuration
        intf1.description = 'multiple lines config'
        intf1.enabled = False

        ipv6a = IPv6Addr(device=dev1)
        ipv6a.ipv6 = IPv6Address('2001:db1:1::1')
        ipv6a.ipv6_prefix_length = '64'
        intf1.add_ipv6addr(ipv6a)
        ipv6b = IPv6Addr(device=dev1)
        ipv6b.ipv6 = IPv6Address('2001:db1:2::2')
        ipv6b.ipv6_prefix_length = '64'
        intf1.add_ipv6addr(ipv6b)

        # Build config
        cfgs = intf1.build_config(apply=False)
        # Check config build correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface GigabitEthernet0/0/0/0',
                ' ipv6 address 2001:db1:1::1/64',
                ' ipv6 address 2001:db1:2::2/64',
                ' description multiple lines config',
                ' shutdown',
                ' exit'
                ]))        

        # Build unconfig
        uncfgs = intf1.build_unconfig(apply=False, attributes={'ipv6addr':None})
        # Check config build correctly
        self.assertMultiLineEqual(
            str(uncfgs),
            '\n'.join([
                'interface GigabitEthernet0/0/0/0',
                ' no ipv6 address 2001:db1:1::1/64',
                ' no ipv6 address 2001:db1:2::2/64',
                ' exit'
                ]))        

if __name__ == '__main__':
    unittest.main()

