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
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        static_routing = StaticRouting()

        static_routing.device_attr[dev1].vrf_attr['VRF1'].address_family_attr['ipv4'].route_attr[
            '10.2.1.0/24'].interface_attr['GigabitEthernet0/1'].if_nexthop = '192.168.1.2'

        static_routing.device_attr[dev1].vrf_attr['VRF1'].address_family_attr['ipv4'].route_attr[
            '10.2.1.0/24'].interface_attr['GigabitEthernet0/1'].if_preference = 2

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), '\n'.join(
           ['ip route vrf VRF1 10.2.1.0 255.255.255.0 GigabitEthernet0/1 192.168.1.2 2'
        ]))

        static_routing_4 = StaticRouting()

        static_routing_4.device_attr[dev1].vrf_attr['default'].address_family_attr['ipv4'].route_attr[
            '3.3.3.3/32'].interface_attr['GigabitEthernet0/3']

        self.assertIs(static_routing_4.testbed, testbed)

        dev1.add_feature(static_routing_4)

        cfgs = static_routing_4.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), '\n'.join(
            ['ip route 3.3.3.3 255.255.255.255 GigabitEthernet0/3'
             ]))


    def test_static_routing_without_interface_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        static_routing = StaticRouting()

        static_routing.device_attr[dev1].vrf_attr['VRF1'].address_family_attr['ipv4'].route_attr[
            '10.2.1.0/24'].next_hop_attr['192.168.1.2'].preference = 3

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), '\n'.join(
            ['ip route vrf VRF1 10.2.1.0 255.255.255.0 192.168.1.2 3'
             ]))

    def test_static_routing_ipv6_without_interface_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        static_routing_6 = StaticRouting()

        static_routing_6.device_attr[dev1].vrf_attr['VRF1'].address_family_attr['ipv6'].route_attr[
            '2001:3:3:3::3/128'].next_hop_attr['2001:10:1:2::2'].preference = 3

        self.assertIs(static_routing_6.testbed, testbed)

        dev1.add_feature(static_routing_6)

        cfgs_6 = static_routing_6.build_config(apply=False)
        self.assertCountEqual(cfgs_6.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs_6[dev1.name]), '\n'.join(
            ['ipv6 route vrf VRF1 2001:3:3:3::3/128 2001:10:1:2::2 3'
             ]))

    def test_static_routing_ipv6_with_interface_tag_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        static_routing = StaticRouting()

        static_routing.device_attr[dev1].vrf_attr['default'].address_family_attr['ipv6'].route_attr[
            '2001:2:2:2::2/128'].interface_attr['GigabitEthernet0/0'].if_nexthop = '2001:10:1:2::2'

        static_routing.device_attr[dev1].vrf_attr['default'].address_family_attr['ipv6'].route_attr[
            '2001:2:2:2::2/128'].interface_attr['GigabitEthernet0/0'].if_tag = 100

        static_routing.device_attr[dev1].vrf_attr['default'].address_family_attr['ipv6'].route_attr[
            '2001:2:2:2::2/128'].interface_attr['GigabitEthernet0/0'].if_track = 1
        static_routing.device_attr[dev1].vrf_attr['default'].address_family_attr['ipv6'].route_attr[
            '2001:2:2:2::2/128'].interface_attr['GigabitEthernet0/0'].if_preference = 11

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), '\n'.join(
           ['ipv6 route 2001:2:2:2::2/128 GigabitEthernet0/0 2001:10:1:2::2 11 tag 100 track 1'
        ]))

    def test_static_routing_ipv6_with_interface_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        static_routing = StaticRouting()
        interface = 'GigabitEthernet0/1'
        vrf = 'VRF1'
        af = 'ipv6'

        route = '{}'.format('2001:2:2:2::2/128')

        static_routing.device_attr[dev1].vrf_attr[vrf].address_family_attr[af].route_attr[
            route].interface_attr[interface].if_nexthop = '2001:20:1:2::2'

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), '\n'.join(
           ['ipv6 route vrf VRF1 2001:2:2:2::2/128 GigabitEthernet0/1 2001:20:1:2::2'
        ]))

        static_routing_2 = StaticRouting()

        static_routing_2.device_attr[dev1].vrf_attr['default'].address_family_attr['ipv6'].route_attr[
            '2001:2:2:2::2/128'].interface_attr['Null0'].if_preference = 5


        self.assertIs(static_routing_2.testbed, testbed)

        dev1.add_feature(static_routing_2)

        cfgs = static_routing_2.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), '\n'.join(
            ['ipv6 route 2001:2:2:2::2/128 Null0 5'
             ]))

    def test_static_routing_uncfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')


        static_routing_2 = StaticRouting()

        static_routing_2.device_attr[dev1].vrf_attr['default'].address_family_attr['ipv4'].route_attr[
            '10.2.1.0/24'].next_hop_attr['18.0.1.1']

        dev1.add_feature(static_routing_2)

        un_cfgs = static_routing_2.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(
            ['no ip route 10.2.1.0 255.255.255.0 18.0.1.1'
             ]))


if __name__ == '__main__':
    unittest.main()
