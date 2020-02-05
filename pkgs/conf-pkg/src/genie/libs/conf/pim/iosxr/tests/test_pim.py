#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import UnsupportedAttributeWarning

# PIM
from genie.libs.conf.vrf import Vrf
from genie.libs.conf.pim import Pim


class test_pim(TestCase):

    def setUp(self):
        
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxr')

    def test_pim_full_config(self):

        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1
        
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        # VRF configuration
        vrf1 = Vrf('default')
        pim.device_attr[self.dev1].vrf_attr[vrf1]
        vrf2 = Vrf('red')
        pim.device_attr[self.dev1].vrf_attr[vrf2]

        for vrf in [vrf1, vrf2]:
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                rp_address = '2.2.2.2'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr['Loopback0']
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr['HundredGigE0/0/0/1']
        
        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'router pim',
                ' address-family ipv4',
                '  interface HundredGigE0/0/0/1',
                '   exit',
                '  interface Loopback0',
                '   exit',
                '  rp-address 2.2.2.2',
                '  exit',
                ' vrf red',
                '  address-family ipv4',
                '   interface HundredGigE0/0/0/1',
                '    exit',
                '   interface Loopback0',
                '    exit',
                '   rp-address 2.2.2.2',
                '   exit',
                '  exit',
                ' exit',
            ]))

        cfgs = pim.build_unconfig(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'no router pim',
            ]))

        
        cfgs = pim.build_unconfig(apply=False,
                                  attributes={'device_attr': {
                                                self.dev1: {
                                                    'vrf_attr': {
                                                        'default': {
                                                            'address_family_attr': {
                                                                'ipv4': {
                                                                    'rp_address': None
                                                                }
                                                            }
                                                        },
                                                        'red': {
                                                            'address_family_attr': {
                                                                'ipv4': {
                                                                    'interface_attr': {
                                                                        'Loopback0': None
                                                                    }
                                                                }
                                                            }                                                            
                                                        }
                                                    }
        }}})

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'router pim',
                ' address-family ipv4',
                '  no rp-address 2.2.2.2',
                '  exit',
                ' vrf red',
                '  address-family ipv4',
                '   no interface Loopback0',
                '   exit',
                '  exit',
                ' exit',
            ]))


if __name__ == '__main__':
    unittest.main()
