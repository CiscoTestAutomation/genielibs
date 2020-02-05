#!/usr/bin/env python

import unittest
from unittest.mock import Mock
import itertools

from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.libs.conf.interface import \
    ParsedInterfaceName, \
    Interface, \
    PhysicalInterface, \
    EmulatedInterface, \
    VirtualInterface, \
    SubInterface
from genie.libs.conf.interface.tgen import \
    Interface as tgenInterface, \
    PhysicalInterface as tgenPhysicalInterface, \
    EmulatedInterface as tgenEmulatedInterface, \
    VirtualInterface as tgenVirtualInterface, \
    SubInterface as tgenSubInterface
from genie.libs.conf.interface.hltapi import \
    Interface as hltapiInterface, \
    PhysicalInterface as hltapiPhysicalInterface, \
    EmulatedInterface as hltapiEmulatedInterface, \
    VirtualInterface as hltapiVirtualInterface, \
    SubInterface as hltapiSubInterface
from genie.libs.conf.interface.spirent.interface import \
    SpirentParsedInterfaceName
from genie.libs.conf.interface.spirent import \
    Interface as spirentInterface, \
    PhysicalInterface as spirentPhysicalInterface, \
    EmulatedInterface as spirentEmulatedInterface, \
    VirtualInterface as spirentVirtualInterface, \
    SubInterface as spirentSubInterface


class test_interface(TestCase):

    def test_init(self):

        self.assertTrue(issubclass(spirentInterface, Interface))
        self.assertTrue(issubclass(spirentInterface, hltapiInterface))
        self.assertTrue(issubclass(spirentInterface, tgenInterface))

        self.assertTrue(issubclass(spirentPhysicalInterface, spirentInterface))
        self.assertTrue(issubclass(spirentPhysicalInterface, hltapiPhysicalInterface))
        self.assertTrue(issubclass(spirentPhysicalInterface, tgenPhysicalInterface))
        self.assertFalse(issubclass(spirentPhysicalInterface, EmulatedInterface))
        self.assertFalse(issubclass(spirentPhysicalInterface, VirtualInterface))

        self.assertTrue(issubclass(spirentEmulatedInterface, spirentInterface))
        self.assertTrue(issubclass(spirentEmulatedInterface, hltapiEmulatedInterface))
        self.assertTrue(issubclass(spirentEmulatedInterface, tgenEmulatedInterface))
        self.assertFalse(issubclass(spirentEmulatedInterface, spirentPhysicalInterface))
        self.assertFalse(issubclass(spirentEmulatedInterface, hltapiPhysicalInterface))
        self.assertFalse(issubclass(spirentEmulatedInterface, tgenPhysicalInterface))
        self.assertFalse(issubclass(spirentEmulatedInterface, VirtualInterface))

        self.assertTrue(issubclass(spirentVirtualInterface, spirentInterface))
        self.assertTrue(issubclass(spirentVirtualInterface, hltapiVirtualInterface))
        self.assertTrue(issubclass(spirentVirtualInterface, tgenVirtualInterface))
        self.assertFalse(issubclass(spirentVirtualInterface, spirentPhysicalInterface))
        self.assertFalse(issubclass(spirentVirtualInterface, hltapiPhysicalInterface))
        self.assertFalse(issubclass(spirentVirtualInterface, tgenPhysicalInterface))
        self.assertFalse(issubclass(spirentVirtualInterface, EmulatedInterface))

        self.assertTrue(issubclass(spirentSubInterface, spirentInterface))
        self.assertTrue(issubclass(spirentSubInterface, spirentVirtualInterface))
        self.assertTrue(issubclass(spirentSubInterface, hltapiSubInterface))
        self.assertTrue(issubclass(spirentSubInterface, tgenSubInterface))
        self.assertFalse(issubclass(spirentSubInterface, spirentPhysicalInterface))
        self.assertFalse(issubclass(spirentSubInterface, hltapiPhysicalInterface))
        self.assertFalse(issubclass(spirentSubInterface, tgenPhysicalInterface))
        self.assertFalse(issubclass(spirentSubInterface, EmulatedInterface))

        Genie.testbed = Testbed()
        dev1 = Device(name='TGEN', os='spirent')
        intf1 = Interface(device=dev1, name='11/22')
        intf2 = Interface(device=dev1, name='11/33')

        self.assertIsInstance(intf1, spirentPhysicalInterface)
        self.assertNotIsInstance(intf1, EmulatedInterface)
        self.assertNotIsInstance(intf1, VirtualInterface)
        self.assertNotIsInstance(intf1, SubInterface)

    def test_SpirentParsedInterfaceName(self):

        d_parsed = SpirentParsedInterfaceName(' 11/22 ')
        self.assertEqual(d_parsed.slot, '11')
        self.assertEqual(d_parsed.port, '22')
        self.assertEqual(d_parsed.subintf_sep, None)
        self.assertEqual(d_parsed.subintf, None)
        self.assertEqual(d_parsed.reconstruct(), '11/22')

        d_parsed = SpirentParsedInterfaceName(' 11/22.33 ')
        self.assertEqual(d_parsed.slot, '11')
        self.assertEqual(d_parsed.port, '22')
        self.assertEqual(d_parsed.subintf_sep, '.')
        self.assertEqual(d_parsed.subintf, '33')
        self.assertEqual(d_parsed.reconstruct(), '11/22.33')

        Genie.testbed = Testbed()
        dev1 = Device(name='TGEN', os='spirent')
        intf1 = Interface(device=dev1, name='11/22')

        d_parsed = intf1.parse_interface_name()
        self.assertEqual(d_parsed.number, '11/22')
        self.assertEqual(d_parsed.slot, '11')
        self.assertEqual(d_parsed.port, '22')
        self.assertEqual(d_parsed.subintf_sep, None)
        self.assertEqual(d_parsed.subintf, None)
        self.assertEqual(d_parsed.reconstruct(), intf1.name)

    def test_SubInterface(self):

        Genie.testbed = Testbed()
        dev1 = Device(name='TGEN', os='spirent')
        intf1 = Interface(device=dev1, name='11/22')
        intf2 = Interface(device=dev1, name='11/33')

        sub1 = intf1.generate_sub_interface()
        self.assertEqual(sub1.name, '{}.0'.format(intf1.name))

        self.assertIsInstance(sub1, spirentSubInterface)
        self.assertNotIsInstance(sub1, spirentPhysicalInterface)
        self.assertNotIsInstance(sub1, EmulatedInterface)

        d_parsed = sub1.parse_interface_name()
        self.assertEqual(d_parsed.number, '11/22')
        self.assertEqual(d_parsed.slot, '11')
        self.assertEqual(d_parsed.port, '22')
        self.assertEqual(d_parsed.subintf_sep, '.')
        self.assertEqual(d_parsed.subintf, '0')
        self.assertEqual(d_parsed.reconstruct(), sub1.name)

        self.assertIs(sub1.parent_interface, intf1)
        self.assertEqual(sub1.build_config(), '')
        self.assertEqual(sub1.build_unconfig(), '')

if __name__ == '__main__':
    unittest.main()

