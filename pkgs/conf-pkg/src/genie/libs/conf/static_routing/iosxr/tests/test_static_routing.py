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
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')

        static_routing = StaticRouting()
        static_routing.interface = 'GigabitEthernet0/1'
        static_routing.vrf = 'VRF1'
        static_routing.af = 'ipv4'
        static_routing.route = '10.2.1.0/24'

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_nexthop = '192.168.1.2'

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_preference = 2

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
           ['router static',
            ' vrf VRF1',
            '  address-family ipv4 unicast',
            '   10.2.1.0/24 GigabitEthernet0/1 192.168.1.2 2',
            '   exit',
            '  exit',
            ' exit',

        ]))

        static_routing_ipv6 = StaticRouting()
        static_routing_ipv6.interface = 'GigabitEthernet0/0/0/0'
        static_routing_ipv6.af = 'ipv6'
        static_routing_ipv6.route = '2001:1:1:1::1/128'
        static_routing_ipv6.vrf = 'default'
        static_routing_ipv6.device_attr[dev1].vrf_attr[static_routing_ipv6.vrf].address_family_attr[static_routing_ipv6.af].route_attr[
            static_routing_ipv6.route].interface_attr[static_routing_ipv6.interface].if_nexthop = '2001:20:1:2::1'

        self.assertIs(static_routing_ipv6.testbed, testbed)

        dev1.add_feature(static_routing_ipv6)

        cfgs = static_routing_ipv6.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['router static',
             ' address-family ipv6 unicast',
             '  2001:1:1:1::1/128 GigabitEthernet0/0/0/0 2001:20:1:2::1',
             '  exit',
             ' exit',

             ]))

    def test_static_routing_vrf_default_with_interface_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')

        static_routing = StaticRouting()
        static_routing.interface = 'GigabitEthernet0/0/0/0'
        static_routing.vrf = 'default'
        static_routing.af = 'ipv4'
        static_routing.route = '1.1.1.1/32'

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface]

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
           ['router static',
            ' address-family ipv4 unicast',
            '  1.1.1.1/32 GigabitEthernet0/0/0/0',
            '  exit',
            ' exit',
        ]))

        static_routing = StaticRouting()
        static_routing.interface = 'GigabitEthernet0/0/0/0'
        static_routing.af = 'ipv4'
        static_routing.route = '10.2.1.0/24'
        static_routing.vrf = 'default'
        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_nexthop = '192.168.1.2'

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_preference = 2

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['router static',
             ' address-family ipv4 unicast',
             '  10.2.1.0/24 GigabitEthernet0/0/0/0 192.168.1.2 2',
             '  exit',
             ' exit',
             ]))

    def test_static_routing_without_interface_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')

        static_routing = StaticRouting()
        static_routing.interface = 'GigabitEthernet0/1'
        static_routing.vrf = 'VRF1'
        static_routing.af = 'ipv4'


        static_routing.route = '{}'.format('10.2.1.0/24')

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].next_hop_attr['192.168.1.2'].preference = 3

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['router static',
             ' vrf VRF1',
             '  address-family ipv4 unicast',
             '   10.2.1.0/24 192.168.1.2 3',
             '   exit',
             '  exit',
             ' exit',
             ]))

    def test_static_routing_ipv6_without_interface_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')

        static_routing = StaticRouting()
        static_routing.vrf = 'default'
        static_routing.af = 'ipv6'

        static_routing.route = '{}'.format('2001:3:3:3::3/128')

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].next_hop_attr['2001:20:2:3::3'].preference = 3

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['router static',
             ' address-family ipv6 unicast',
             '  2001:3:3:3::3/128 2001:20:2:3::3 3',
             '  exit',
             ' exit',
             ]))

    def test_static_routing_ipv4_ipv6_with_vrf_interface_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')

        static_routing = StaticRouting()
        static_routing.interface = 'Null0'
        static_routing.vrf = 'VRF1'
        static_routing.af = 'ipv4'
        static_routing.route = '1.1.1.1/32'

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].interface_attr[static_routing.interface].if_preference = 99

        self.assertIs(static_routing.testbed, testbed)

        dev1.add_feature(static_routing)

        cfgs = static_routing.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
           ['router static',
            ' vrf VRF1',
            '  address-family ipv4 unicast',
            '   1.1.1.1/32 Null0 99',
            '   exit',
            '  exit',
            ' exit',
        ]))

        static_routing_6 = StaticRouting()
        static_routing_6.interface = 'Null0'
        static_routing_6.vrf = 'VRF1'
        static_routing_6.af = 'ipv6'
        static_routing_6.route = '2001:1:1:1::1/128'

        static_routing_6.device_attr[dev1].vrf_attr[static_routing_6.vrf].address_family_attr[static_routing_6.af].route_attr[
            static_routing_6.route].interface_attr[static_routing_6.interface].if_preference = 99

        self.assertIs(static_routing_6.testbed, testbed)

        dev1.add_feature(static_routing_6)

        cfgs = static_routing_6.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['router static',
             ' vrf VRF1',
             '  address-family ipv6 unicast',
             '   2001:1:1:1::1/128 Null0 99',
             '   exit',
             '  exit',
             ' exit',

             ]))


    def test_static_routing_uncfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')

        static_routing = StaticRouting()
        static_routing.vrf = 'VRF1'
        static_routing.af = 'ipv4'
        static_routing.route = '{}'.format('10.2.1.0/24')

        static_routing.device_attr[dev1].vrf_attr[static_routing.vrf].address_family_attr[static_routing.af].route_attr[
            static_routing.route].next_hop_attr[None]

        dev1.add_feature(static_routing)

        un_cfgs = static_routing.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(un_cfgs[dev1.name]), '\n'.join(
            ['router static',
             ' vrf VRF1',
             '  address-family ipv4 unicast',
             '   no 10.2.1.0/24',
             '   exit',
             '  exit',
             ' exit',
             ]))

if __name__ == '__main__':
    unittest.main()
