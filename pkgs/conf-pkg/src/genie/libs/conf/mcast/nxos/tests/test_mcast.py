#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import UnsupportedAttributeWarning

# Mcast
from genie.libs.conf.mcast.mroute import Mroute
from genie.libs.conf.vrf import Vrf
from genie.libs.conf.mcast import Mcast


class test_mcast_mroute(TestCase):

    def setUp(self):
        
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='nxos')
        
        # Mcast object
        self.mcast = Mcast()

    def test_mcast_config(self):

        # For failures
        self.maxDiff = None

        # Create VRFs
        vrf1 = Vrf('red')
        self.mcast.device_attr[self.dev1].vrf_attr[vrf1]
        
        vrf2 = Vrf('blue')
        self.mcast.device_attr[self.dev1].vrf_attr[vrf2]

        self.mcast.device_attr[self.dev1].vrf_attr[None].address_family_attr['ipv4'].enabled = True
        self.mcast.device_attr[self.dev1].vrf_attr[None].address_family_attr['ipv6'].enabled = True
        self.mcast.device_attr[self.dev1].vrf_attr[None].address_family_attr['ipv4'].multipath = True

        # ipv4 config under VRF1
        # vrf1 ip mroute config
        mroute1a = Mroute(device=self.dev1)
        mroute1a.mroute_address = '192.1.1.1'
        mroute1a.mroute_prefix_mask = 24
        mroute1a.mroute_neighbor_address = '172.30.10.13'
        mroute1a.mroute_admin_distance = 100
        mroute1a.mroute_vrf = 'VRF1'
        # Add mroute to mcast config
        self.mcast.device_attr[self.dev1].vrf_attr[vrf1].address_family_attr['ipv4'].add_mroute(mroute1a)

        # ipv6 config under VRF1
        # vrf1 ipv6 mroute config
        mroute1b = Mroute(device=self.dev1)
        mroute1b.mroute_address = '129::'
        mroute1b.mroute_prefix_mask = 16
        mroute1b.mroute_neighbor_address = '140::'
        mroute1b.mroute_admin_distance = 100
        # Add mroute to mcast config
        self.mcast.device_attr[self.dev1].vrf_attr[vrf1].address_family_attr['ipv6'].add_mroute(mroute1b)

        # ipv4 config under VRF1
        # vrf1 ip mroute config
        mroute1c = Mroute(device=self.dev1)
        mroute1c.mroute_address = '192.2.2.1'
        mroute1c.mroute_prefix_mask = 32
        mroute1c.mroute_neighbor_address = '172.40.50.15'
        mroute1c.mroute_admin_distance = 175
        # Add mroute to mcast config
        self.mcast.device_attr[self.dev1].vrf_attr[vrf1].address_family_attr['ipv4'].add_mroute(mroute1c)
       
        # ipv4 config under VRF2
        # vrf2 ip mroute config
        mroute2a = Mroute(device=self.dev1)
        mroute2a.mroute_address = '192.168.2.1'
        mroute2a.mroute_prefix_mask = 32
        mroute2a.mroute_neighbor_address = '176.40.11.12'
        mroute2a.mroute_admin_distance = 150
        mroute2a.mroute_vrf = 'VRF2'
        # Add mroute to mcast config
        self.mcast.device_attr[self.dev1].vrf_attr[vrf2].address_family_attr['ipv4'].add_mroute(mroute2a)

        # ipv6 config under VRF2
        # vrf2 ipv6 mroute config
        mroute2b = Mroute(device=self.dev1)
        mroute2b.mroute_address = '126::'
        mroute2b.mroute_prefix_mask = 24
        mroute2b.mroute_neighbor_address = '130::'
        # Add mroute to mcast config
        self.mcast.device_attr[self.dev1].vrf_attr[vrf2].address_family_attr['ipv6'].add_mroute(mroute2b)

        # ipv4 config under top level
        # default vrf ip mroute config
        mroute3a = Mroute(device=self.dev1)
        mroute3a.mroute_address = '192.168.3.1'
        mroute3a.mroute_prefix_mask = 24
        mroute3a.mroute_interface_name = 'Ethernet3/1'
        mroute3a.mroute_admin_distance = 85
        mroute3a.mroute_vrf = 'VRF3'
        self.mcast.device_attr[self.dev1].vrf_attr[None].address_family_attr['ipv4'].add_mroute(mroute3a)

        # ipv6 config under top level
        # default vrf ipv6 mroute config
        mroute3b = Mroute(device=self.dev1)
        mroute3b.mroute_address = '126::'
        mroute3b.mroute_prefix_mask = 24
        mroute3b.mroute_interface_name = 'Null0'
        # Add mroute to mcast config
        self.mcast.device_attr[self.dev1].vrf_attr[None].address_family_attr['ipv6'].add_mroute(mroute3b)

        # Build config
        cfgs = self.mcast.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'feature pim',
                'ip multicast multipath',
                'ip mroute 192.168.3.1/24 Ethernet3/1 85 vrf VRF3',
                'feature pim6',
                'ipv6 mroute 126::/24 Null0',
                'vrf context blue',
                ' ip mroute 192.168.2.1/32 176.40.11.12 150 vrf VRF2',
                ' ipv6 mroute 126::/24 130::',
                ' exit',
                'vrf context red',
                ' ip mroute 192.1.1.1/24 172.30.10.13 100 vrf VRF1',
                ' ip mroute 192.2.2.1/32 172.40.50.15 175',
                ' ipv6 mroute 129::/16 140:: 100',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.mcast.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no feature pim',
                'no ip multicast multipath',
                'no ip mroute 192.168.3.1/24 Ethernet3/1 85 vrf VRF3',
                'no feature pim6',
                'no ipv6 mroute 126::/24 Null0',
                'vrf context blue',
                ' no ip mroute 192.168.2.1/32 176.40.11.12 150 vrf VRF2',
                ' no ipv6 mroute 126::/24 130::',
                ' exit',
                'vrf context red',
                ' no ip mroute 192.1.1.1/24 172.30.10.13 100 vrf VRF1',
                ' no ip mroute 192.2.2.1/32 172.40.50.15 175',
                ' no ipv6 mroute 129::/16 140:: 100',
                ' exit',
            ]))

    def test_mroute_operators(self):
        
        # For failures
        self.maxDiff = None

        # Make object1 for comparisons
        mroute1 = Mroute(device=self.dev1)
        mroute1.mroute_address = '172.25.1.1'
        mroute1.mroute_prefix_mask = 24
        mroute1.mroute_interface_name = 'Ethernet1/1'
        mroute1.mroute_admin_distance = 95
        mroute1.mroute_vrf = 'VRF1'
        
        # Make object2 for comparisons
        mroute2 = Mroute(device=self.dev1)
        mroute2.mroute_address = '172.25.1.1'
        mroute2.mroute_prefix_mask = 24
        mroute2.mroute_interface_name = 'Ethernet1/1'
        mroute2.mroute_admin_distance = 95
        mroute2.mroute_vrf = 'VRF1'

        # Make object3 for comparisons
        mroute3 = Mroute(device=self.dev1)
        mroute3.mroute_address = '192.168.1.1'
        mroute3.mroute_prefix_mask = 24
        mroute3.mroute_interface_name = 'Ethernet3/1'
        mroute3.mroute_admin_distance = 100
        mroute3.mroute_vrf = 'VRF2'

        # Make object4 for comparisons
        mroute4 = Mroute(device=self.dev1)
        mroute4.mroute_address = '126::'
        mroute4.mroute_prefix_mask = 32
        mroute4.mroute_neighbor_address = '130::'
        mroute4.mroute_admin_distance = 150
        mroute4.mroute_vrf = 'VRF3'

        # Test __eq__
        self.assertTrue(mroute1 == mroute2)
        self.assertFalse(mroute1 == mroute3)
        self.assertEqual(mroute1, mroute2)
        self.assertNotEqual(mroute1, mroute3)

        # Test __lt__
        self.assertTrue(mroute1 < mroute3)
        self.assertFalse(mroute3 < mroute1)
        self.assertLess(mroute1, mroute3)

        self.assertTrue(mroute2 < mroute3)
        self.assertFalse(mroute3 < mroute2)
        self.assertLess(mroute2, mroute3)

        # Compare IPv4Address to IPv6Address
        self.assertFalse(mroute3 < mroute4)
        self.assertTrue(mroute4 < mroute3)
        self.assertLess(mroute4, mroute3)

        # Test __gt
        self.assertTrue(mroute3 > mroute1)
        self.assertFalse(mroute1 > mroute3)
        self.assertGreater(mroute3, mroute1)

        self.assertTrue(mroute3 > mroute2)
        self.assertFalse(mroute2 > mroute3)
        self.assertGreater(mroute3, mroute2)

        # Compare IPv4Address to IPv6Address
        self.assertFalse(mroute4 > mroute3)
        self.assertTrue(mroute3 > mroute4)
        self.assertGreater(mroute3, mroute4)

        # Test __repr__
        self.assertIn('ip address 172.25.1.1/24', str(mroute1.__repr__))
        self.assertIn('ip address 192.168.1.1/24', str(mroute3.__repr__))
        self.assertIn('ipv6 address 126::/32', str(mroute4.__repr__))


if __name__ == '__main__':
    unittest.main()
