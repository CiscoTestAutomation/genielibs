#!/usr/bin/env python

#python
import unittest
from unittest.mock import Mock

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# Genie XBu_shared
from genie.libs.conf.static_routing.static_routing import StaticRouting


class test_static_routing(TestCase):


    def test_static_routing_with_interface_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        static_routing = StaticRouting()
        static_routing.interface = 'Ethernet0/1'
        static_routing.vrf = 'VRF1'
        static_routing.af = 'ipv4'
        static_routing.route = '10.2.1.0/24'

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_nexthop = '192.168.1.2'

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_preference = 2

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_nh_vrf = 'VRF1'

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
           ['vrf context VRF1',
            ' ip route 10.2.1.0/24 Ethernet0/1 192.168.1.2 vrf VRF1 2',
            ' exit',
        ]))
        static_routing = StaticRouting()
        static_routing.interface = 'Ethernet0/1'
        static_routing.vrf = 'default'
        static_routing.af = 'ipv4'
        static_routing.route = '10.2.1.0/24'

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_nexthop = '192.168.1.2'

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_preference = 2

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_nh_vrf = 'VRF1'

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['ip route 10.2.1.0/24 Ethernet0/1 192.168.1.2 vrf VRF1 2',
             ]))

    def test_static_routing_without_interface_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        static_routing = StaticRouting()
        static_routing.af = 'ipv4'

        static_routing.route = '10.2.1.0/24'

        static_routing.device_attr[dev1].vrf_attr[None].address_family_attr[static_routing.af].route_attr[
            static_routing.route].next_hop_attr['192.168.1.2'].preference = 3

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), '\n'.join(
            ['ip route 10.2.1.0/24 192.168.1.2 3',
             ]))

    def test_static_routing_with_interface_next_vrf_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        static_routing = StaticRouting()
        static_routing.interface = 'Ethernet1/2'
        static_routing.vrf = 'default'
        static_routing.af = 'ipv4'
        static_routing.route = '1.1.1.1/32'

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_nexthop = '10.1.3.1'

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_preference = 4

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_tag = 10

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_track = 1

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_nh_vrf = 'VRF1'

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['ip route 1.1.1.1/32 Ethernet1/2 10.1.3.1 vrf VRF1 track 1 tag 10 4',
             ]))

    def test_static_routing_ipv6_without_interface_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        static_routing = StaticRouting()
        static_routing.af = 'ipv6'

        static_routing.route = '2001:2:2:2::2/128'

        static_routing.device_attr[dev1].vrf_attr['default'].address_family_attr[static_routing.af].route_attr[
            static_routing.route].next_hop_attr['2001:10:2:3::2'].preference = 3

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), '\n'.join(
            ['ipv6 route 2001:2:2:2::2/128 2001:10:2:3::2 3',
             ]))

    def test_static_routing_ipv6_with_interface_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        static_routing = StaticRouting()
        static_routing.interface = 'Ethernet1/4'
        static_routing.vrf = 'default'
        static_routing.af = 'ipv6'
        static_routing.route = '2001:2:2:2::2/128'

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_nexthop = '2001:10:2:3::2'

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_tag = 10

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_track = 1

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_nh_vrf = 'VRF1'

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['ipv6 route 2001:2:2:2::2/128 Ethernet1/4 2001:10:2:3::2 vrf VRF1 track 1 tag 10',
             ]))

    def test_static_routing_ipv6_with_interface_vrf_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        static_routing = StaticRouting()
        static_routing.interface = 'Null0'
        static_routing.vrf = 'VRF1'
        static_routing.af = 'ipv6'
        static_routing.route = '2001:1:1:1::1/128'

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface]


        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['vrf context VRF1',
             ' ipv6 route 2001:1:1:1::1/128 Null0',
             ' exit',
             ]))

    def test_static_routing_uncfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        static_routing = StaticRouting()
        static_routing.af = 'ipv4'
        static_routing.interface = 'Ethernet0/1'
        static_routing.route = '10.2.1.0/24'

        static_routing.device_attr[dev1].vrf_attr['VRF1'].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_nexthop ='192.168.2.2'

        dev1.add_feature(static_routing)

        un_cfgs = static_routing.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(
            ['vrf context VRF1',
             ' no ip route 10.2.1.0/24 Ethernet0/1 192.168.2.2',
             ' exit',
             ]))

    def test_static_routing_default_uncfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        static_routing = StaticRouting()
        static_routing.af = 'ipv4'
        static_routing.interface = 'Ethernet0/1'
        static_routing.route = '10.2.1.0/24'

        static_routing.device_attr[dev1].vrf_attr['default'].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_nexthop = '192.168.2.2'

        dev1.add_feature(static_routing)

        un_cfgs = static_routing.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(
            ['no ip route 10.2.1.0/24 Ethernet0/1 192.168.2.2',
             ]))

if __name__ == '__main__':
    unittest.main()
