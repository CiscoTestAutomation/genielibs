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
from genie.libs.conf.interface.ixia.interface import \
    IxiaParsedInterfaceName
from genie.libs.conf.interface.ixia import \
    Interface as ixiaInterface, \
    PhysicalInterface as ixiaPhysicalInterface, \
    EmulatedInterface as ixiaEmulatedInterface, \
    VirtualInterface as ixiaVirtualInterface, \
    SubInterface as ixiaSubInterface


class test_interface(TestCase):

    def test_init(self):

        self.assertTrue(issubclass(ixiaInterface, Interface))
        self.assertTrue(issubclass(ixiaInterface, hltapiInterface))
        self.assertTrue(issubclass(ixiaInterface, tgenInterface))

        self.assertTrue(issubclass(ixiaPhysicalInterface, ixiaInterface))
        self.assertTrue(issubclass(ixiaPhysicalInterface, hltapiPhysicalInterface))
        self.assertTrue(issubclass(ixiaPhysicalInterface, tgenPhysicalInterface))
        self.assertFalse(issubclass(ixiaPhysicalInterface, EmulatedInterface))
        self.assertFalse(issubclass(ixiaPhysicalInterface, VirtualInterface))

        self.assertTrue(issubclass(ixiaEmulatedInterface, ixiaInterface))
        self.assertTrue(issubclass(ixiaEmulatedInterface, hltapiEmulatedInterface))
        self.assertTrue(issubclass(ixiaEmulatedInterface, tgenEmulatedInterface))
        self.assertFalse(issubclass(ixiaEmulatedInterface, ixiaPhysicalInterface))
        self.assertFalse(issubclass(ixiaEmulatedInterface, hltapiPhysicalInterface))
        self.assertFalse(issubclass(ixiaEmulatedInterface, tgenPhysicalInterface))
        self.assertFalse(issubclass(ixiaEmulatedInterface, VirtualInterface))

        self.assertTrue(issubclass(ixiaVirtualInterface, ixiaInterface))
        self.assertTrue(issubclass(ixiaVirtualInterface, hltapiVirtualInterface))
        self.assertTrue(issubclass(ixiaVirtualInterface, tgenVirtualInterface))
        self.assertFalse(issubclass(ixiaVirtualInterface, ixiaPhysicalInterface))
        self.assertFalse(issubclass(ixiaVirtualInterface, hltapiPhysicalInterface))
        self.assertFalse(issubclass(ixiaVirtualInterface, tgenPhysicalInterface))
        self.assertFalse(issubclass(ixiaVirtualInterface, EmulatedInterface))

        self.assertTrue(issubclass(ixiaSubInterface, ixiaInterface))
        self.assertTrue(issubclass(ixiaSubInterface, ixiaVirtualInterface))
        self.assertTrue(issubclass(ixiaSubInterface, hltapiSubInterface))
        self.assertTrue(issubclass(ixiaSubInterface, tgenSubInterface))
        self.assertFalse(issubclass(ixiaSubInterface, ixiaPhysicalInterface))
        self.assertFalse(issubclass(ixiaSubInterface, hltapiPhysicalInterface))
        self.assertFalse(issubclass(ixiaSubInterface, tgenPhysicalInterface))
        self.assertFalse(issubclass(ixiaSubInterface, EmulatedInterface))

        Genie.testbed = Testbed()
        dev1 = Device(name='TGEN', os='ixia')
        intf1 = Interface(device=dev1, name='11/22')
        intf2 = Interface(device=dev1, name='11/33')

        self.assertIsInstance(intf1, ixiaPhysicalInterface)
        self.assertNotIsInstance(intf1, EmulatedInterface)
        self.assertNotIsInstance(intf1, VirtualInterface)
        self.assertNotIsInstance(intf1, SubInterface)

    def test_IxiaParsedInterfaceName(self):

        d_parsed = IxiaParsedInterfaceName(' 11/22 ')
        self.assertEqual(d_parsed.slot, '11')
        self.assertEqual(d_parsed.port, '22')
        self.assertEqual(d_parsed.subintf_sep, None)
        self.assertEqual(d_parsed.subintf, None)
        self.assertEqual(d_parsed.reconstruct(), '11/22')

        d_parsed = IxiaParsedInterfaceName(' 11/22.33 ')
        self.assertEqual(d_parsed.slot, '11')
        self.assertEqual(d_parsed.port, '22')
        self.assertEqual(d_parsed.subintf_sep, '.')
        self.assertEqual(d_parsed.subintf, '33')
        self.assertEqual(d_parsed.reconstruct(), '11/22.33')

        Genie.testbed = Testbed()
        dev1 = Device(name='TGEN', os='ixia')
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
        dev1 = Device(name='TGEN', os='ixia')
        intf1 = Interface(device=dev1, name='11/22')
        intf2 = Interface(device=dev1, name='11/33')

        sub1 = intf1.generate_sub_interface()
        self.assertEqual(sub1.name, '{}.0'.format(intf1.name))

        self.assertIsInstance(sub1, ixiaSubInterface)
        self.assertNotIsInstance(sub1, ixiaPhysicalInterface)
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

