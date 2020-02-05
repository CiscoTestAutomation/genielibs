#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import UnsupportedAttributeWarning

from genie.libs.conf.evpn import Evpn, Evi
from genie.libs.conf.bgp import RouteDistinguisher


class test_evpn(TestCase):

    def test_init(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/0/3')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/0/4')

        with self.assertNoWarnings():

            Genie.testbed = None
            with self.assertRaises(TypeError):
                evpn = Evpn()
            evpn = Evpn(testbed=testbed)
            self.assertIs(evpn.testbed, testbed)
            Genie.testbed = testbed
            evpn = Evpn()
            self.assertIs(evpn.testbed, Genie.testbed)
            self.assertIs(evpn.testbed, testbed)

            self.assertIsNone(getattr(dev1, 'evpn', None))
            self.assertIsNone(getattr(intf1, 'evpn', None))

            intf1.add_feature(evpn)
            self.assertIs(intf1.evpn, evpn)
            # TODO self.assertIs(dev1.evpn, evpn)
            self.assertIsNone(getattr(dev1, 'evpn', None))

            dev1.add_feature(evpn)
            self.assertIs(dev1.evpn, evpn)

    def test_config(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/0/3')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/0/4')

        with self.assertNoWarnings():

            evpn = Evpn()
            intf1.add_feature(evpn)
            dev1.add_feature(evpn)

            cfgs = evpn.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'evpn',
                    ' interface GigabitEthernet0/0/0/1',
                    '  exit',
                    ' exit',
                    ]))

            dev2.add_feature(evpn)
            self.assertIs(dev2.evpn, evpn)

            cfgs = evpn.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name, dev2.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'evpn',
                    ' interface GigabitEthernet0/0/0/1',
                    '  exit',
                    ' exit',
                    ]))
            self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join([
                    'evpn',
                    ' exit',
                    ]))

            evpn.recovery_timer = 100
            with self.assertRaisesRegex(ValueError, r'^blah: Not None\. Not of type int\.$'):
                evpn.device_attr[dev1].recovery_timer = 'blah'
            evpn.device_attr[dev1].recovery_timer = 200
            evpn.peering_timer = 300
            evpn.device_attr[dev2].peering_timer = 400

            self.assertEqual(evpn.recovery_timer, 100)
            self.assertEqual(evpn.peering_timer, 300)
            self.assertEqual(evpn.device_attr[dev1].recovery_timer, 200)
            self.assertEqual(evpn.device_attr[dev2].recovery_timer, 100)
            self.assertEqual(evpn.device_attr[dev1].peering_timer, 300)
            self.assertEqual(evpn.device_attr[dev2].peering_timer, 400)
            self.assertIs(evpn.device_attr[dev1].
                    isinherited('recovery_timer'), False)
            self.assertIs(evpn.device_attr[dev2].
                    isinherited('recovery_timer'), True)

            cfgs = evpn.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name, dev2.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'evpn',
                    ' interface GigabitEthernet0/0/0/1',
                    '  exit',
                    ' timers',
                    '  recovery 200',
                    '  peering 300',
                    '  exit',
                    ' exit',
                    ]))
            self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join([
                    'evpn',
                    ' timers',
                    '  recovery 100',
                    '  peering 400',
                    '  exit',
                    ' exit',
                    ]))

            evpn.device_attr[intf1.device].interface_attr[intf1].peering_timer = 200
            evpn.mac_flush = 'mvrp'
            with self.assertWarns(UnsupportedAttributeWarning,
                    msg='evpn interface peering_timer'):
                cfgs = evpn.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name, dev2.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'evpn',
                    ' interface GigabitEthernet0/0/0/1',
                    '  mac-flush mvrp',
                    '  exit',
                    ' timers',
                    '  recovery 200',
                    '  peering 300',
                    '  exit',
                    ' exit',
                    ]))
            self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join([
                    'evpn',
                    ' timers',
                    '  recovery 100',
                    '  peering 400',
                    '  exit',
                    ' exit',
                    ]))

            with self.assertWarns(UnsupportedAttributeWarning,
                    msg='evpn interface peering_timer'):
                cfgs = evpn.build_config(apply=False,
                        attributes='device_attr__*__interface_attr')
            self.assertCountEqual(cfgs.keys(), [dev1.name, dev2.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'evpn',
                    ' interface GigabitEthernet0/0/0/1',
                    '  mac-flush mvrp',
                    '  exit',
                    ' exit',
                    ]))
            self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join([
                    'evpn',
                    ' exit',
                    ]))

            cfgs = evpn.build_unconfig(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name, dev2.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'no evpn',
                    ]))
            self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join([
                    'no evpn',
                    ]))

            cfgs = evpn.build_unconfig(apply=False, devices=[dev1])
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'no evpn',
                    ]))

            cfgs = evpn.build_unconfig(apply=False,
                    attributes='device_attr__{}'.format(dev1.name))
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'no evpn',
                    ]))

            cfgs = evpn.build_unconfig(apply=False,
                    attributes='device_attr__*__interface_attr')
            self.assertCountEqual(sorted(cfgs.keys()), sorted([dev1.name,
                                                               dev2.name]))
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'evpn',
                    ' no interface GigabitEthernet0/0/0/1',
                    ' exit',
                    ]))

            cfgs = evpn.build_unconfig(apply=False,
                    attributes='device_attr__*__peering_timer')
            self.assertCountEqual(cfgs.keys(), [dev1.name, dev2.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'evpn',
                    ' timers',
                    '  no peering 300',
                    '  exit',
                    ' exit',
                    ]))
            self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join([
                    'evpn',
                    ' timers',
                    '  no peering 400',
                    '  exit',
                    ' exit',
                    ]))

            # TODO
            # cfgs = evpn.build_unconfig(apply=False,
            #         attributes=[
            #             'device_attr__{}__peering_timer'.format(dev1.name),
            #             'device_attr__{}__recovery_timer'.format(dev2.name),
            #             ])
            cfgs = evpn.build_unconfig(apply=False,
                    attributes={
                        'device_attr': {
                            dev1.name: 'peering_timer',
                            dev2.name: 'recovery_timer',
                            },
                        })
            self.assertCountEqual(cfgs.keys(), [dev1.name, dev2.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'evpn',
                    ' timers',
                    '  no peering 300',
                    '  exit',
                    ' exit',
                    ]))
            self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join([
                    'evpn',
                    ' timers',
                    '  no recovery 100',
                    '  exit',
                    ' exit',
                    ]))

            evpn.bgp.rd = RouteDistinguisher('1000:5000')
            self.assertIs(type(evpn.bgp.rd), RouteDistinguisher)
            self.assertEqual(evpn.bgp.rd, RouteDistinguisher('1000:5000'))
            evpn.bgp.rd = '1000:5000'
            self.assertIs(type(evpn.bgp.rd), RouteDistinguisher)
            self.assertEqual(evpn.bgp.rd, RouteDistinguisher('1000:5000'))

            o = evpn.device_attr[intf1.device].interface_attr[intf1]
            o.rd = RouteDistinguisher('1000:5001')
            self.assertIs(type(o.rd), RouteDistinguisher)
            self.assertEqual(o.rd, RouteDistinguisher('1000:5001'))
            o.rd = '1000:5001'
            #self.assertIs(type(o.rd), RouteDistinguisher)
            self.assertEqual(o.rd, RouteDistinguisher('1000:5001'))

if __name__ == '__main__':
    unittest.main()

