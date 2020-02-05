#!/usr/bin/env python

'''
IOSXE unit tests for Genie Vrf conf using CLI.
'''

# Python
import re
import unittest
from unittest.mock import Mock

# Genie
from genie.conf import Genie
from genie.tests.conf import TestCase
from genie.conf.base import Testbed, Device
from genie.libs.conf.vrf.vrf import Vrf


class test_vrf(TestCase):

    def setUp(self):
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxr')

    def test_cli_config(self):        
        # prefix-list conf
        vrf_conf = Vrf('VRF1')
        self.dev1.add_feature(vrf_conf)

        # Apply configuration
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 unicast'].\
            route_target_attr['200:1'].rt_type  = 'both'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 unicast'].\
            route_target_attr['100:1'].rt_type  = 'import'

        # Build config
        cfgs = vrf_conf.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf VRF1',
                ' address-family ipv4 unicast',
                '  import route-target 100:1',
                '  import route-target 200:1',
                '  export route-target 200:1',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = vrf_conf.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no vrf VRF1',
            ]))

        # Build unconfig for selected attributes
        cfgs = vrf_conf.build_unconfig(apply=False,
                                       attributes={'device_attr': {
                                                        self.dev1: {
                                                            'address_family_attr': {
                                                                'ipv4 unicast': {
                                                                    'route_target_attr': None
                                                                }
                                                             }}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf VRF1',
                ' address-family ipv4 unicast',
                '  no import route-target 100:1',
                '  no import route-target 200:1',
                '  no export route-target 200:1',
                '  exit',
                ' exit',
            ]))

        # Build unconfig for selected attributes
        cfgs = vrf_conf.build_unconfig(apply=False,
                                       attributes={'device_attr': {
                                                    self.dev1: {
                                                        'address_family_attr': {
                                                            'ipv4 unicast': {
                                                                'route_target_attr': {
                                                                    '200:1': {
                                                                        'rt_type': None}
                                                    }}}}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf VRF1',
                ' address-family ipv4 unicast',
                '  no import route-target 200:1',
                '  no export route-target 200:1',
                '  exit',
                ' exit',
            ]))

    def test_cli_config_v6(self):        
        # prefix-list conf
        vrf_conf = Vrf('VRF2')
        self.dev1.add_feature(vrf_conf)

        # Apply configuration
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            route_target_attr['100:1'].rt_type  = 'export'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            route_target_attr['200:1'].rt_type  = 'export'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            route_target_attr['300:1'].rt_type  = 'import'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            route_target_attr['400:1'].rt_type  = 'both'

        # Build config
        cfgs = vrf_conf.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf VRF2',
                ' address-family ipv6 unicast',
                '  export route-target 100:1',
                '  export route-target 200:1',
                '  import route-target 300:1',
                '  import route-target 400:1',
                '  export route-target 400:1',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = vrf_conf.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no vrf VRF2',
            ]))

        # Build unconfig for selected attributes
        cfgs = vrf_conf.build_unconfig(apply=False,
                                       attributes={
                                           'device_attr': {
                                                self.dev1: {
                                                    'address_family_attr': {
                                                        'ipv6 unicast': {
                                                            'route_target_attr': None
                                                        }
                                            }}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf VRF2',
                ' address-family ipv6 unicast',
                '  no export route-target 100:1',
                '  no export route-target 200:1',
                '  no import route-target 300:1',
                '  no import route-target 400:1',
                '  no export route-target 400:1',
                '  exit',
                ' exit',
            ]))

        # Build unconfig for selected attributes
        cfgs = vrf_conf.build_unconfig(apply=False,
                                       attributes={
                                            'device_attr': {
                                                self.dev1: {
                                                    'address_family_attr': {
                                                        'ipv6 unicast': {
                                                            'route_target_attr': {
                                                                '200:1': {
                                                                    'rt_type': None}
                                            }}}}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf VRF2',
                ' address-family ipv6 unicast',
                '  no export route-target 200:1',
                '  exit',
                ' exit',
            ]))


if __name__ == '__main__':
    unittest.main()

