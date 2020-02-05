#!/usr/bin/env python

import unittest
import re
from unittest.mock import Mock

from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.vrf import Vrf
from genie.libs.conf.bgp import RouteTarget
from genie.libs.conf.address_family import AddressFamily


class test_vrf(TestCase):

    def setUp(self):
        tb = Genie.testbed = Testbed()
        self.dev1 = Device(testbed=tb, name='PE1', os='iosxr')
        self.dev2 = Device(testbed=tb, name='PE2', os='iosxr')
        self.i1 = Interface(name='GigabitEthernet0/0/0/1', device=self.dev1)
        self.i2 = Interface(name='GigabitEthernet0/0/0/2', device=self.dev2)
        self.i3 = Interface(name='GigabitEthernet0/0/0/3', device=self.dev1)
        self.i4 = Interface(name='GigabitEthernet0/0/0/4', device=self.dev2)
        self.i5 = Interface(name='GigabitEthernet0/0/0/5', device=self.dev1)
        self.i6 = Interface(name='GigabitEthernet0/0/0/6', device=self.dev2)
        self.i7 = Interface(name='GigabitEthernet0/0/0/7', device=self.dev1)
        self.i8 = Interface(name='GigabitEthernet0/0/0/8', device=self.dev2)
        self.link = Link(name='1_2_1', testbed=tb)
        self.link.connect_interface(interface=self.i1)
        self.link.connect_interface(interface=self.i2)
        self.link2 = Link(name='1_2_2', testbed=tb)
        self.link2.connect_interface(interface=self.i3)
        self.link2.connect_interface(interface=self.i4)
        self.link3 = Link(name='1_2_3', testbed=tb)
        self.link3.connect_interface(interface=self.i5)
        self.link3.connect_interface(interface=self.i6)
        self.link4 = Link(name='1_2_4', testbed=tb)
        self.link4.connect_interface(interface=self.i7)
        self.link4.connect_interface(interface=self.i8)
        self.assertSetEqual(
            set(self.link.find_interfaces()),
            set([self.i1, self.i2]))
        self.assertSetEqual(
            set(self.dev1.find_interfaces()),
            set([self.i1, self.i3, self.i5, self.i7]))
        self.assertSetEqual(
            set(self.dev2.find_interfaces()),
            set([self.i2, self.i4, self.i6, self.i8]))

    def test_init(self):

        with self.subTest('name'):
            with self.assertRaises(TypeError):
                vrf = Vrf()
            with self.assertRaises(AssertionError):
                vrf = Vrf(name=123)
            vrf = Vrf(name='red')
            vrf2 = Vrf(name='blue')

        with self.subTest('fallback_vrf'):
            # fallback_vrf's type is defined post Vrf class; Make sure it works.
            self.assertIs(vrf.fallback_vrf, None)
            with self.assertRaises(ValueError):
                vrf.fallback_vrf = 123
            self.assertIs(vrf.fallback_vrf, None)
            with self.assertRaises(ValueError):
                vrf.fallback_vrf = 'blue'
            self.assertIs(vrf.fallback_vrf, None)
            vrf.fallback_vrf = None
            self.assertIs(vrf.fallback_vrf, None)
            vrf.fallback_vrf = vrf2
            self.assertIs(vrf.fallback_vrf, vrf2)

    def test_1_top_level(self):

        vrf = Vrf(name='vrf1')
        self.dev1.add_feature(vrf)
        self.dev2.add_feature(vrf)

        vrf.device_attr['PE1'].scale_mode = 'big'
        vrf.description = 'my description'
        cfgs = vrf.build_config(apply=False)
        
        self.assertMultiLineDictEqual(cfgs, {
            self.dev1.name: '\n'.join([
                'vrf vrf1',
                ' description my description',
                ' mode big',
                ' exit',
            ]),
            self.dev2.name: '\n'.join([
                'vrf vrf1',
                ' description my description',
                ' exit',
            ]),
        })

        cfgs = vrf.build_config(apply=False, attributes='device_attr__*__description')

        self.assertMultiLineDictEqual(cfgs, {
            self.dev1.name: '\n'.join([
                'vrf vrf1',
                ' description my description',
                ' exit',
            ]),
            self.dev2.name: '\n'.join([
                'vrf vrf1',
                ' description my description',
                ' exit',
            ]),
        })

        cfgs = vrf.build_config(apply=False, attributes={
            'device_attr': {
                '*': {
                    'description': None,
                },
            },
        })
        self.assertMultiLineDictEqual(cfgs, {
            self.dev1.name: '\n'.join([
                'vrf vrf1',
                ' description my description',
                ' exit',
            ]),
            self.dev2.name: '\n'.join([
                'vrf vrf1',
                ' description my description',
                ' exit',
            ]),
        })

        cfgs = vrf.build_config(apply=False, devices=[self.dev2], attributes={
            'device_attr': {
                '*': {
                    'description': None,
                },
            },
        })
        self.assertMultiLineDictEqual(cfgs, {
            self.dev2.name: '\n'.join([
                'vrf vrf1',
                ' description my description',
                ' exit',
            ]),
        })

        cfgs = vrf.build_config(apply=False, devices=[self.dev2], attributes={
            'device_attr': {
                self.dev1: {
                    'description': None,
                },
            },
        })
        self.assertMultiLineDictEqual(cfgs, {})

        cfgs = vrf.build_config(apply=False, devices=[self.dev2], attributes={
            'device_attr': {
                self.dev2: {
                    'description': None,
                },
            },
        })
        self.assertMultiLineDictEqual(cfgs, {
            self.dev2.name: '\n'.join([
                'vrf vrf1',
                ' description my description',
                ' exit',
            ]),
        })

        cfgs = vrf.build_config(apply=False, devices=[self.dev2], attributes={
            'device_attr': {
                self.dev2.name: {
                    'description': None,
                },
            },
        })
        self.assertMultiLineDictEqual(cfgs, {
            self.dev2.name: '\n'.join([
                'vrf vrf1',
                ' description my description',
                ' exit',
            ]),
        })

    def test_4_per_af(self):

        vrf = Vrf(name='vrf1')
        self.dev1.add_feature(vrf)

        vrf.address_families |= {AddressFamily.ipv6_unicast}
        vrf.device_attr['PE1'].address_family_attr['ipv4 unicast'].export_route_targets = [
                RouteTarget.ImportExport('100:200', stitching=True),
                ]

        cfgs = vrf.build_config(apply=False)

        self.assertMultiLineDictEqual(cfgs, {
            self.dev1.name: '\n'.join([
                'vrf vrf1',
                ' address-family ipv4 unicast',
                '  export route-target 100:200 stitching',
                '  exit',
                ' exit',
            ]),
        })

if __name__ == '__main__':
    unittest.main()

