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
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxr')
        
        # Mcast object
        self.mcast = Mcast()

    def test_mcast_config(self):

        # For failures
        self.maxDiff = None

        # Create VRFs
        vrf1 = Vrf('red')
        self.mcast.device_attr[self.dev1].vrf_attr[vrf1]

        self.mcast.device_attr[self.dev1].vrf_attr[None].address_family_attr['ipv4'].enable = True
        self.mcast.device_attr[self.dev1].vrf_attr[None].address_family_attr['ipv6'].enable = True
        self.mcast.device_attr[self.dev1].vrf_attr['default'].address_family_attr['ipv4'].multipath = True
        self.mcast.device_attr[self.dev1].vrf_attr['default'].address_family_attr['ipv6'].multipath = True

        self.mcast.device_attr[self.dev1].vrf_attr[vrf1].address_family_attr['ipv4'].enable = True
        self.mcast.device_attr[self.dev1].vrf_attr[vrf1].address_family_attr['ipv6'].enable = True
        intf1_obj = Interface(device=self.dev1, name='GigabitEthernet0/0/0/0')
        self.mcast.device_attr[self.dev1].vrf_attr[vrf1].address_family_attr['ipv6'].\
            interface_attr[intf1_obj.name].if_enable = True
        
        # ipv4 config under VRF1
        # vrf1 ip mroute config
        mroute1a = Mroute(device=self.dev1)
        mroute1a.mroute_address = '192.1.1.1'
        mroute1a.mroute_prefix_mask = 32
        mroute1a.mroute_interface_name = 'GigabitEthernet0/0/0/2'
        mroute1a.mroute_neighbor_address = '172.30.10.13'

        mroute1c = Mroute(device=self.dev1)
        mroute1c.mroute_address = '192.1.1.10'
        mroute1c.mroute_prefix_mask = 32
        mroute1c.mroute_interface_name = 'GigabitEthernet0/0/0/1'
        mroute1c.mroute_neighbor_address = '172.30.10.14'
        # Add mroute to mcast config
        self.mcast.device_attr[self.dev1].vrf_attr[vrf1].address_family_attr['ipv4'].add_mroute(mroute1a)
        self.mcast.device_attr[self.dev1].vrf_attr[vrf1].address_family_attr['ipv4'].add_mroute(mroute1c)

        # ipv6 config under VRF1
        # vrf1 ipv6 mroute config
        mroute1b = Mroute(device=self.dev1)
        mroute1b.mroute_address = '129::'
        mroute1b.mroute_prefix_mask = 128
        mroute1b.mroute_interface_name = 'GigabitEthernet0/0/0/2'
        mroute1b.mroute_neighbor_address = '140::'
        # Add mroute to mcast config
        self.mcast.device_attr[self.dev1].vrf_attr[vrf1].address_family_attr['ipv6'].add_mroute(mroute1b)

        # ipv4 config under top level
        # default vrf ip mroute config
        mroute2a = Mroute(device=self.dev1)
        mroute2a.mroute_address = '192.168.3.1'
        mroute2a.mroute_prefix_mask = 32
        mroute2a.mroute_interface_name = 'GigabitEthernet0/0/0/5'
        mroute2a.mroute_neighbor_address = '172.30.10.20'
        self.mcast.device_attr[self.dev1].vrf_attr['default'].address_family_attr['ipv4'].add_mroute(mroute2a)

        # ipv6 config under top level
        # default vrf ipv6 mroute config
        mroute2b = Mroute(device=self.dev1)
        mroute2b.mroute_address = '126::'
        mroute2b.mroute_prefix_mask = 128
        mroute2b.mroute_interface_name = 'GigabitEthernet0/0/0/5'
        mroute2b.mroute_neighbor_address = '150::'
        # Add mroute to mcast config
        self.mcast.device_attr[self.dev1].vrf_attr['default'].address_family_attr['ipv6'].add_mroute(mroute2b)

        # Build config
        cfgs = self.mcast.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'multicast-routing',
                ' address-family ipv4',
                '  interface all enable',
                '  multipath',
                '  static-rpf 192.168.3.1 32 GigabitEthernet0/0/0/5 172.30.10.20',
                '  exit',
                ' address-family ipv6',
                '  interface all enable',
                '  multipath',
                '  static-rpf 126:: 128 GigabitEthernet0/0/0/5 150::',
                '  exit',
                ' vrf red',
                '  address-family ipv4',
                '   interface all enable',
                '   static-rpf 192.1.1.1 32 GigabitEthernet0/0/0/2 172.30.10.13',
                '   static-rpf 192.1.1.10 32 GigabitEthernet0/0/0/1 172.30.10.14',
                '   exit',
                '  address-family ipv6',
                '   interface all enable',
                '   static-rpf 129:: 128 GigabitEthernet0/0/0/2 140::',
                '   interface GigabitEthernet0/0/0/0',
                '    enable',
                '    exit',
                '   exit',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.mcast.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                # Top level - IPv4
                'no multicast-routing',
            ]))
        
        cfgs = self.mcast.build_unconfig(apply=False,
                                  attributes={'device_attr': {
                                                self.dev1: {
                                                    'vrf_attr': {
                                                        'default': {
                                                            'address_family_attr': {
                                                                'ipv4': {
                                                                    'enable': None
                                                                }
                                                            }
                                                        },
                                                        'red': {
                                                            'address_family_attr': {
                                                                'ipv4': {
                                                                    'mroutes': None
                                                                }
                                                            }                                                            
                                                        }
                                                    }
        }}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'multicast-routing',
                ' address-family ipv4',
                '  no interface all enable',
                '  exit',
                ' vrf red',
                '  address-family ipv4',
                '   no static-rpf 192.1.1.1 32 GigabitEthernet0/0/0/2 172.30.10.13',
                '   no static-rpf 192.1.1.10 32 GigabitEthernet0/0/0/1 172.30.10.14',
                '   exit',
                '  exit',
                ' exit',
            ]))


if __name__ == '__main__':
    unittest.main()
