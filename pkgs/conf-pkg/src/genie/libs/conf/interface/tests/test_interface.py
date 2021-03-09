#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from pyats.topology import Device as AtsDevice
from pyats.topology import Interface as AtsInterface
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.interface import\
    PhysicalInterface as geniePhysicalInterface,\
    VirtualInterface as genieVirtualInterface,\
    PseudoInterface as geniePseudoInterface,\
    LoopbackInterface as genieLoopbackInterface
from genie.libs.conf.interface import\
    ParsedInterfaceName, \
    Interface as xbuInterface,\
    PhysicalInterface, PhysicalInterface as xbuPhysicalInterface,\
    SubInterface, SubInterface as xbuSubInterface,\
    VirtualInterface, VirtualInterface as xbuVirtualInterface,\
    PseudoInterface, PseudoInterface as xbuPseudoInterface,\
    EthernetInterface, EthernetInterface as xbuEthernetInterface,\
    TunnelInterface, TunnelInterface as xbuTunnelInterface,\
    TunnelTeInterface, TunnelTeInterface as xbuTunnelTeInterface,\
    NamedTunnelTeInterface, NamedTunnelTeInterface as xbuNamedTunnelTeInterface
from genie.libs.conf.interface.iosxr import\
    Interface as iosxrInterface,\
    PhysicalInterface as iosxrPhysicalInterface,\
    SubInterface as iosxrSubInterface,\
    VirtualInterface as iosxrVirtualInterface,\
    PseudoInterface as iosxrPseudoInterface,\
    EthernetInterface as iosxrEthernetInterface
from genie.libs.conf.base import MAC, IPv4Interface, IPv6Interface


class test_interface(TestCase):

    def test_ParsedInterfaceName(self):

        # TODO net_module module rack slot instance port subport cpu rsip
        d_parsed = ParsedInterfaceName(' Loopback 0 ')
        self.assertEqual(d_parsed.type, 'Loopback')
        self.assertEqual(d_parsed.number, '0')
        self.assertEqual(d_parsed.subintf_sep, None)
        self.assertEqual(d_parsed.subintf, None)
        self.assertEqual(d_parsed.reconstruct(), 'Loopback0')
        d_parsed = ParsedInterfaceName('Ethernet0/0')
        self.assertEqual(d_parsed.type, 'Ethernet')
        self.assertEqual(d_parsed.number, '0/0')
        self.assertEqual(d_parsed.subintf_sep, None)
        self.assertEqual(d_parsed.subintf, None)
        self.assertEqual(d_parsed.reconstruct(), 'Ethernet0/0')
        d_parsed = ParsedInterfaceName('GigabitEthernet0/0/0/0')
        self.assertEqual(d_parsed.type, 'GigabitEthernet')
        self.assertEqual(d_parsed.number, '0/0/0/0')
        self.assertEqual(d_parsed.subintf_sep, None)
        self.assertEqual(d_parsed.subintf, None)
        self.assertEqual(d_parsed.reconstruct(), 'GigabitEthernet0/0/0/0')
        d_parsed = ParsedInterfaceName('MgmtEth0/RP0/CPU0/0')
        self.assertEqual(d_parsed.type, 'MgmtEth')
        self.assertEqual(d_parsed.number, '0/RP0/CPU0/0')
        self.assertEqual(d_parsed.subintf_sep, None)
        self.assertEqual(d_parsed.subintf, None)
        self.assertEqual(d_parsed.reconstruct(), 'MgmtEth0/RP0/CPU0/0')
        d_parsed = ParsedInterfaceName(' GigabitEthernet 0/0/0/0.0 ')
        self.assertEqual(d_parsed.type, 'GigabitEthernet')
        self.assertEqual(d_parsed.number, '0/0/0/0')
        self.assertEqual(d_parsed.subintf_sep, '.')
        self.assertEqual(d_parsed.subintf, '0')
        self.assertEqual(d_parsed.reconstruct(), 'GigabitEthernet0/0/0/0.0')
        d_parsed = ParsedInterfaceName('GigabitEthernet0/0/0/0:0')
        self.assertEqual(d_parsed.type, 'GigabitEthernet')
        self.assertEqual(d_parsed.number, '0/0/0/0')
        self.assertEqual(d_parsed.subintf_sep, ':')
        self.assertEqual(d_parsed.subintf, '0')
        self.assertEqual(d_parsed.reconstruct(), 'GigabitEthernet0/0/0/0:0')
        d_parsed = ParsedInterfaceName('tunnel-te1')
        self.assertEqual(d_parsed.type, 'tunnel-te')
        self.assertEqual(d_parsed.number, '1')
        self.assertEqual(d_parsed.subintf_sep, None)
        self.assertEqual(d_parsed.subintf, None)
        self.assertEqual(d_parsed.reconstruct(), 'tunnel-te1')
        d_parsed = ParsedInterfaceName('GCC0')
        self.assertEqual(d_parsed.type, 'GCC0')
        self.assertEqual(d_parsed.number, None)
        self.assertEqual(d_parsed.subintf_sep, None)
        self.assertEqual(d_parsed.subintf, None)
        self.assertEqual(d_parsed.reconstruct(), 'GCC0')
        d_parsed = ParsedInterfaceName('g0')
        self.assertEqual(d_parsed.type, 'g0')
        self.assertEqual(d_parsed.number, None)
        self.assertEqual(d_parsed.subintf_sep, None)
        self.assertEqual(d_parsed.subintf, None)
        self.assertEqual(d_parsed.reconstruct(), 'g0')
        d_parsed = ParsedInterfaceName('GCC1')
        self.assertEqual(d_parsed.type, 'GCC1')
        self.assertEqual(d_parsed.number, None)
        self.assertEqual(d_parsed.subintf_sep, None)
        self.assertEqual(d_parsed.subintf, None)
        self.assertEqual(d_parsed.reconstruct(), 'GCC1')
        d_parsed = ParsedInterfaceName('OTU3E20/0/0/0')
        self.assertEqual(d_parsed.type, 'OTU3E2')
        self.assertEqual(d_parsed.number, '0/0/0/0')
        self.assertEqual(d_parsed.subintf_sep, None)
        self.assertEqual(d_parsed.subintf, None)
        self.assertEqual(d_parsed.reconstruct(), 'OTU3E20/0/0/0')

    def test_init(self):

        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxr')

        with self.assertRaises(TypeError):
            intf1 = Interface()
        with self.assertRaises(TypeError):
            intf1 = Interface(device=dev1)
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1')
        intf1.device = None  # forget it!

        #ats_dev1 = AtsDevice(name='PE1')
        ats_dev1 = None
        ats_intf1 = AtsInterface(device=ats_dev1,
                                 name='GigabitEthernet0/0/0/1',
                                 os='iosxr',
                                 type='ethernet')
        intf1 = Interface(device=dev1,
                          name='GigabitEthernet0/0/0/1')

        self.assertTrue(isinstance(intf1, Interface))
        self.assertTrue(isinstance(intf1, xbuInterface))
        self.assertTrue(isinstance(intf1, iosxrInterface))
        self.assertTrue(isinstance(intf1, geniePhysicalInterface))
        self.assertTrue(isinstance(intf1, xbuPhysicalInterface))
        self.assertTrue(isinstance(intf1, iosxrPhysicalInterface))
        #self.assertTrue(isinstance(intf1, EthernetInterface))
        self.assertTrue(isinstance(intf1, xbuEthernetInterface))
        self.assertTrue(isinstance(intf1, iosxrEthernetInterface))

        intf2 = Interface(device=intf1.device,
                          name=intf1.name + '.1')

        self.assertTrue(isinstance(intf2, Interface))
        self.assertTrue(isinstance(intf2, xbuInterface))
        self.assertTrue(isinstance(intf2, iosxrInterface))
        self.assertTrue(isinstance(intf2, genieVirtualInterface))
        self.assertTrue(isinstance(intf2, xbuVirtualInterface))
        self.assertTrue(isinstance(intf2, iosxrVirtualInterface))
        #self.assertTrue(isinstance(intf2, genieSubInterface))
        self.assertTrue(isinstance(intf2, xbuSubInterface))
        self.assertTrue(isinstance(intf2, iosxrSubInterface))

        self.assertEqual(intf1.ipv4, None)
        self.assertEqual(intf1.ipv6, None)
        self.assertEqual(intf1.mac_address, None)
        self.assertEqual(intf1.burnin_mac_address, None)
        self.assertEqual(intf1.effective_mac_address, None)

        intf1.ipv4 = '1.2.3.4/24'
        self.assertEqual(intf1.ipv4, IPv4Interface('1.2.3.4/24'))
        self.assertTrue(isinstance(intf1.ipv4, IPv4Interface))

        intf1.ipv4 = None
        self.assertIs(intf1.ipv4, None)

        with self.assertRaises(ValueError):
            intf1.ipv4 = 'abc'
        if False:
            # TODO -- Setting without a prefix uses 32 bits!
            with self.assertRaises(ValueError):
                intf1.ipv4 = '1.2.3.4'
        else:
            intf1.ipv4 = '1.2.3.4'
            self.assertEqual(intf1.ipv4, IPv4Interface('1.2.3.4/32'))

        intf1.ipv6 = '1234::1/80'
        self.assertEqual(intf1.ipv6, IPv6Interface('1234::1/80'))
        self.assertTrue(isinstance(intf1.ipv6, IPv6Interface))

        intf1.burnin_mac_address = 'a.b.c'
        self.assertTrue(isinstance(intf1.burnin_mac_address, MAC))
        self.assertEqual(intf1.mac_address, None)
        self.assertEqual(intf1.burnin_mac_address, MAC('a.b.c'))
        self.assertEqual(intf1.effective_mac_address, intf1.burnin_mac_address)
        del intf1.burnin_mac_address

        intf1.mac_address = 'a.b.c2'
        self.assertTrue(isinstance(intf1.mac_address, MAC))
        self.assertEqual(intf1.mac_address, MAC('a.b.c2'))
        self.assertEqual(intf1.burnin_mac_address, None)
        self.assertEqual(intf1.effective_mac_address, intf1.mac_address)
        del intf1.mac_address

        intf1.mac_address = 'a.b.c3'
        intf1.burnin_mac_address = 'a.b.c4'
        self.assertEqual(intf1.mac_address, MAC('a.b.c3'))
        self.assertEqual(intf1.burnin_mac_address, MAC('a.b.c4'))
        self.assertEqual(intf1.effective_mac_address, intf1.mac_address)
        del intf1.mac_address
        del intf1.burnin_mac_address

        dev1 = Device(name='PE1', os=None)
        # Should not raise exception
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1')


if __name__ == '__main__':
    unittest.main()

