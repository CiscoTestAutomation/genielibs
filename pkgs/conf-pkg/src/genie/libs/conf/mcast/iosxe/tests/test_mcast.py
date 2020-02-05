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
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxe')
        
        # Mcast object
        self.mcast = Mcast()

    def test_mcast_config(self):

        # For failures
        self.maxDiff = None

        # Apply configuration
        # self.mcast.device_attr[self.dev1].enable = True
        # self.mcast.device_attr[self.dev1].multipath = True

        # VRF configuration
        vrf1 = Vrf('red')
        mcast1 = self.mcast.device_attr[self.dev1].vrf_attr[vrf1].address_family_attr['ipv4']
        mcast1.enable = True
        mcast1.multipath = True
        mroute3a = Mroute(device=self.dev1)
        mroute3a.mroute_address = '192.168.3.1'
        mroute3a.mroute_prefix_mask = 24
        mroute3a.mroute_interface_name = 'Ethernet3/1'
        mroute3a.mroute_admin_distance = 85
        mcast1.add_mroute(mroute3a)

        mcast2 = self.mcast.device_attr[self.dev1].vrf_attr[vrf1].address_family_attr['ipv6']
        mcast2.enable = True
        mcast2.multipath = True
        mroute1b = Mroute(device=self.dev1)
        mroute1b.mroute_address = '129::'
        mroute1b.mroute_prefix_mask = 16
        mroute1b.mroute_neighbor_address = '140::'
        mroute1b.mroute_admin_distance = 100
        # Add mroute to mcast config
        mcast2.add_mroute(mroute1b)


        vrf2 = Vrf('default')
        mcast3 = self.mcast.device_attr[self.dev1].vrf_attr[vrf2].address_family_attr['ipv6']
        mcast3.enable = True
        mcast3.multipath = True
        mroute3b = Mroute(device=self.dev1)
        mroute3b.mroute_address = '126::'
        mroute3b.mroute_prefix_mask = 24
        mroute3b.mroute_interface_name = 'Null0'
        # Add mroute to mcast config
        mcast3.add_mroute(mroute3b)

        mcast4 = self.mcast.device_attr[self.dev1].vrf_attr[vrf2].address_family_attr['ipv4']
        mcast4.enable = True
        mcast4.multipath = True
        mroute2a = Mroute(device=self.dev1)
        mroute2a.mroute_address = '192.168.2.1'
        mroute2a.mroute_prefix_mask = 32
        mroute2a.mroute_neighbor_address = '176.40.11.12'
        mroute2a.mroute_admin_distance = 150
        # Add mroute to mcast config
        mcast4.add_mroute(mroute2a)

        # Build config
        cfgs = self.mcast.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'ip multicast-routing distributed',
                'ip multicast multipath',
                'ip mroute 192.168.2.1 255.255.255.255 176.40.11.12 150',
                'ipv6 multicast-routing',
                'ipv6 multicast multipath',
                'ipv6 route 126::/24 Null0',
                'ip multicast-routing vrf red distributed',
                'ip multicast multipath',
                'ip mroute vrf red 192.168.3.1 255.255.255.0 Ethernet3/1 85',
                'ipv6 multicast-routing vrf red',
                'ipv6 multicast multipath',
                'ipv6 route vrf red 129::/16 140:: 100',
            ]))

        # Build unconfig
        cfgs = self.mcast.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no ip multicast-routing distributed',
                'no ip multicast multipath',
                'no ip mroute 192.168.2.1 255.255.255.255 176.40.11.12 150',
                'no ipv6 multicast-routing',
                'no ipv6 multicast multipath',
                'no ipv6 route 126::/24 Null0',
                'no ip multicast-routing vrf red distributed',
                'no ip multicast multipath',
                'no ip mroute vrf red 192.168.3.1 255.255.255.0 Ethernet3/1 85',
                'no ipv6 multicast-routing vrf red',
                'no ipv6 multicast multipath',
                'no ipv6 route vrf red 129::/16 140:: 100',
            ]))


if __name__ == '__main__':
    unittest.main()
