#!/usr/bin/env python

import unittest
import unittest.mock
from unittest.mock import Mock, MagicMock

from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.l2vpn import BridgeDomain, Xconnect, Vfi, Pseudowire
from genie.libs.conf.l2vpn import PseudowireNeighbor, PseudowireIPNeighbor, PseudowireIPv4Neighbor


class test_pseudowire(TestCase):

    def test_init(self):

        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        lo1 = Interface(device=dev1, name='Loopback0', ipv4='101.0.0.1/32')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1', ipv4='10.1.0.1/24')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2', ipv4='10.2.0.1/24')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        lo2 = Interface(device=dev2, name='Loopback0', ipv4='102.0.0.1/32')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/0/3', ipv4='10.1.0.2/24')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/0/4', ipv4='10.2.0.2/24')
        link1 = Link(testbed=testbed, name='link1', interfaces=(intf1, intf3))
        link2 = Link(testbed=testbed, name='link2', interfaces=(intf2, intf4))
        dev3 = Device(testbed=testbed, name='PE3', os='iosxr')

        container = Mock()
        container.add_pseudowire = MagicMock()
        nbr1 = PseudowireNeighbor(container=container, device=dev1, ip='1.2.3.4')
        nbr2 = PseudowireNeighbor(container=container, device=dev2, ip='1.2.3.4')
        nbr3 = PseudowireNeighbor(container=container, device=dev3, ip='1.2.3.4')

        with self.assertRaises(TypeError):
            pw1 = Pseudowire()
        with self.assertRaises(TypeError):
            pw1 = Pseudowire(pw_id=1)
        with self.assertRaises(ValueError):
            pw1 = Pseudowire(neighbors=())
        with self.assertRaises(ValueError):
            pw1 = Pseudowire(neighbors=(nbr1,))
        with self.assertRaises(ValueError):
            pw1 = Pseudowire(neighbors=(nbr1, nbr1))
        with self.assertRaises(ValueError):
            pw1 = Pseudowire(neighbors=(nbr1, nbr2, nbr3))
        with self.assertRaises(ValueError):
            pw1 = Pseudowire(neighbors=(nbr1, intf2))

        pw1 = Pseudowire(neighbors=(nbr1, nbr2))
        self.assertCountEqual(pw1.neighbors, [nbr1, nbr2])
        self.assertEqual(nbr1.pw_id, None)
        self.assertEqual(nbr2.pw_id, None)
        container.add_pseudowire.assert_has_calls([
            unittest.mock.call(pw1),
            unittest.mock.call(pw1),
        ])
        container.add_pseudowire.reset_mock()

        pw1 = Pseudowire(neighbors=(nbr1, nbr2), pw_id=1)
        self.assertCountEqual(pw1.neighbors, [nbr1, nbr2])
        self.assertEqual(nbr1.pw_id, 1)
        self.assertEqual(nbr2.pw_id, 1)
        container.add_pseudowire.assert_has_calls([
            unittest.mock.call(pw1),
            unittest.mock.call(pw1),
        ])
        container.add_pseudowire.reset_mock()

    def test_init_vpls(self):

        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        lo1 = Interface(device=dev1, name='Loopback0', ipv4='101.0.0.1/32')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1', ipv4='10.1.0.1/24')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2', ipv4='10.2.0.1/24')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        lo2 = Interface(device=dev2, name='Loopback0', ipv4='102.0.0.1/32')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/0/3', ipv4='10.1.0.2/24')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/0/4', ipv4='10.2.0.2/24')
        link1 = Link(testbed=testbed, name='link1', interfaces=(intf1, intf3))
        link2 = Link(testbed=testbed, name='link2', interfaces=(intf2, intf4))
        dev3 = Device(testbed=testbed, name='PE3', os='iosxr')

        bd1 = BridgeDomain(name='bd1')
        dev1.add_feature(bd1)
        dev2.add_feature(bd1)

        self.assertCountEqual(bd1.pseudowires, [])
        nbr1 = bd1.create_pseudowire_neighbor(device=dev1, ip=lo2.ipv4.ip)
        nbr2 = bd1.device_attr[dev2].create_pseudowire_neighbor(ip=lo1.ipv4.ip)
        pw1 = Pseudowire(neighbors=(nbr1, nbr2), pw_id=1)
        self.assertCountEqual(bd1.pseudowires, [pw1])
        self.assertCountEqual(bd1.pseudowire_neighbors, [nbr1, nbr2])
        self.assertCountEqual(bd1.device_attr[dev1].pseudowires, [pw1])
        self.assertCountEqual(bd1.device_attr[dev1].pseudowire_neighbors, [nbr1])
        self.assertCountEqual(bd1.device_attr[dev2].pseudowires, [pw1])
        self.assertCountEqual(bd1.device_attr[dev2].pseudowire_neighbors, [nbr2])
        self.assertCountEqual(bd1.device_attr[dev3].pseudowires, [])
        self.assertCountEqual(bd1.device_attr[dev3].pseudowire_neighbors, [])
        self.assertCountEqual(bd1.segments, [pw1])
        self.assertCountEqual(bd1.device_attr[dev1].segments, [pw1])
        self.assertCountEqual(bd1.device_attr[dev2].segments, [pw1])
        self.assertCountEqual(bd1.device_attr[dev3].segments, [])

        cfgs = bd1.build_config(apply=False)
        self.assertMultiLineDictEqual(
            cfgs,
            {
                dev1.name: '\n'.join([
                    'l2vpn',
                    ' bridge group bd1g',
                    '  bridge-domain bd1',
                    '   neighbor 102.0.0.1 pw-id 1',
                    '    exit',
                    '   exit',
                    '  exit',
                    ' exit',
                ]),
                dev2.name: '\n'.join([
                    'l2vpn',
                    ' bridge group bd1g',
                    '  bridge-domain bd1',
                    '   neighbor 101.0.0.1 pw-id 1',
                    '    exit',
                    '   exit',
                    '  exit',
                    ' exit',
                ]),
            })

    def test_init_vpls_vfi(self):

        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        lo1 = Interface(device=dev1, name='Loopback0', ipv4='101.0.0.1/32')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1', ipv4='10.1.0.1/24')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2', ipv4='10.2.0.1/24')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        lo2 = Interface(device=dev2, name='Loopback0', ipv4='102.0.0.1/32')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/0/3', ipv4='10.1.0.2/24')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/0/4', ipv4='10.2.0.2/24')
        link1 = Link(testbed=testbed, name='link1', interfaces=(intf1, intf3))
        link2 = Link(testbed=testbed, name='link2', interfaces=(intf2, intf4))
        dev3 = Device(testbed=testbed, name='PE3', os='iosxr')

        bd1 = BridgeDomain(name='bd1')
        dev1.add_feature(bd1)
        dev2.add_feature(bd1)

        vfi1 = Vfi(name='vfi1', device=dev1)
        bd1.add_vfi(vfi1)

        self.assertCountEqual(bd1.segments, [vfi1])
        self.assertCountEqual(bd1.device_attr[dev1].segments, [vfi1])
        self.assertCountEqual(bd1.device_attr[dev2].segments, [])
        self.assertCountEqual(bd1.device_attr[dev3].segments, [])

        self.assertCountEqual(bd1.pseudowires, [])
        nbr1 = vfi1.create_pseudowire_neighbor(ip=lo2.ipv4.ip)
        nbr2 = bd1.device_attr[dev2].create_pseudowire_neighbor(ip=lo1.ipv4.ip)
        pw1 = Pseudowire(neighbors=(nbr1, nbr2), pw_id=1)

        self.assertCountEqual(vfi1.pseudowires, [pw1])
        self.assertCountEqual(vfi1.pseudowire_neighbors, [nbr1])
        self.assertCountEqual(vfi1.segments, [pw1])

        self.assertCountEqual(bd1.pseudowires, [pw1])
        self.assertCountEqual(bd1.pseudowire_neighbors, [nbr2])
        self.assertCountEqual(bd1.device_attr[dev1].pseudowires, [])
        self.assertCountEqual(bd1.device_attr[dev1].pseudowire_neighbors, [])
        self.assertCountEqual(bd1.device_attr[dev2].pseudowires, [pw1])
        self.assertCountEqual(bd1.device_attr[dev2].pseudowire_neighbors, [nbr2])
        self.assertCountEqual(bd1.device_attr[dev3].pseudowires, [])
        self.assertCountEqual(bd1.device_attr[dev3].pseudowire_neighbors, [])
        self.assertCountEqual(bd1.segments, [vfi1, pw1])
        self.assertCountEqual(bd1.device_attr[dev1].segments, [vfi1])
        self.assertCountEqual(bd1.device_attr[dev2].segments, [pw1])
        self.assertCountEqual(bd1.device_attr[dev3].segments, [])

        cfgs = bd1.build_config(apply=False)
        self.assertMultiLineDictEqual(
            cfgs,
            {
                dev1.name: '\n'.join([
                    'l2vpn',
                    ' bridge group bd1g',
                    '  bridge-domain bd1',
                    '   vfi vfi1',
                    '    neighbor 102.0.0.1 pw-id 1',
                    '     exit',
                    '    exit',
                    '   exit',
                    '  exit',
                    ' exit',
                ]),
                dev2.name: '\n'.join([
                    'l2vpn',
                    ' bridge group bd1g',
                    '  bridge-domain bd1',
                    '   neighbor 101.0.0.1 pw-id 1',
                    '    exit',
                    '   exit',
                    '  exit',
                    ' exit',
                ]),
            })

    def test_init_vpws(self):

        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        lo1 = Interface(device=dev1, name='Loopback0', ipv4='101.0.0.1/32')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1', ipv4='10.1.0.1/24')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2', ipv4='10.2.0.1/24')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        lo2 = Interface(device=dev2, name='Loopback0', ipv4='102.0.0.1/32')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/0/3', ipv4='10.1.0.2/24')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/0/4', ipv4='10.2.0.2/24')
        link1 = Link(testbed=testbed, name='link1', interfaces=(intf1, intf3))
        link2 = Link(testbed=testbed, name='link2', interfaces=(intf2, intf4))
        dev3 = Device(testbed=testbed, name='PE3', os='iosxr')

        xc1 = Xconnect(name='xc1')
        dev1.add_feature(xc1)
        dev2.add_feature(xc1)

        self.assertCountEqual(xc1.pseudowires, [])
        nbr1 = xc1.create_pseudowire_neighbor(device=dev1, ip=lo2.ipv4.ip)
        nbr2 = xc1.device_attr[dev2].create_pseudowire_neighbor(ip=lo1.ipv4.ip)
        pw1 = Pseudowire(neighbors=(nbr1, nbr2), pw_id=1)
        self.assertCountEqual(xc1.pseudowires, [pw1])
        self.assertCountEqual(xc1.device_attr[dev1].pseudowires, [pw1])
        self.assertCountEqual(xc1.device_attr[dev2].pseudowires, [pw1])
        self.assertCountEqual(xc1.device_attr[dev3].pseudowires, [])
        self.assertCountEqual(xc1.segments, [pw1])
        self.assertCountEqual(xc1.device_attr[dev1].segments, [pw1])
        self.assertCountEqual(xc1.device_attr[dev2].segments, [pw1])
        self.assertCountEqual(xc1.device_attr[dev3].segments, [])

        cfgs = xc1.build_config(apply=False)
        self.assertMultiLineDictEqual(
            cfgs,
            {
                dev1.name: '\n'.join([
                    'l2vpn',
                    ' xconnect group xc1g',
                    '  p2p xc1',
                    '   neighbor ipv4 102.0.0.1 pw-id 1',
                    '    exit',
                    '   exit',
                    '  exit',
                    ' exit',
                ]),
                dev2.name: '\n'.join([
                    'l2vpn',
                    ' xconnect group xc1g',
                    '  p2p xc1',
                    '   neighbor ipv4 101.0.0.1 pw-id 1',
                    '    exit',
                    '   exit',
                    '  exit',
                    ' exit',
                ]),
            })

if __name__ == '__main__':
    unittest.main()

