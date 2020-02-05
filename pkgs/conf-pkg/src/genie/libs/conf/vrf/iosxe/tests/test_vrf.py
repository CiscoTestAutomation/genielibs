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
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxe')

    def test_cli_config_v4(self):        
        # prefix-list conf
        vrf_conf = Vrf('VRF1')
        self.dev1.add_feature(vrf_conf)

        # Apply configuration
        vrf_conf.device_attr[self.dev1].rd = '100:1'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 unicast'].\
            import_from_global_map = 'import_from_global_map'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 unicast'].\
            export_to_global_map = 'export_to_global_map'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 unicast'].\
            routing_table_limit_number = 10000
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 unicast'].\
            simple_alert  = True

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
                'vrf definition VRF1',
                ' rd 100:1',
                ' address-family ipv4 unicast',
                '  import ipv4 unicast map import_from_global_map',
                '  export ipv4 unicast map export_to_global_map',
                '  maximum routes 10000 warning-only',
                '  route-target import 100:1',
                '  route-target import 200:1',
                '  route-target export 200:1',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = vrf_conf.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no vrf definition VRF1',
            ]))

        # Build unconfig for selected attributes
        cfgs = vrf_conf.build_unconfig(apply=False,
                                       attributes={'device_attr': {
                                                        self.dev1: {
                                                            'rd': None,
                                                             'address_family_attr': {
                                                                'ipv4 unicast': {
                                                                    'export_to_global_map': None
                                                                }
                                                             }}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf definition VRF1',
                ' no rd 100:1',
                ' address-family ipv4 unicast',
                '  no export ipv4 unicast map export_to_global_map',
                '  exit',
                ' exit',
            ]))

        # Build unconfig for selected attributes
        cfgs = vrf_conf.build_unconfig(apply=False,
                                       attributes={'device_attr': {self.dev1: {
                                                           'address_family_attr': {'ipv4 unicast': {
                                                              'route_target_attr': {'200:1': {
                                                                'rt_type': None}
                                                           }}}}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf definition VRF1',
                ' address-family ipv4 unicast',
                '  no route-target import 200:1',
                '  no route-target export 200:1',
                '  exit',
                ' exit',
            ]))

    def test_cli_config_v6(self):        
        # prefix-list conf
        vrf_conf = Vrf('VRF2')
        self.dev1.add_feature(vrf_conf)

        # Apply configuration
        vrf_conf.device_attr[self.dev1].rd = '100:1'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            import_from_global_map = 'test_import'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            export_to_global_map = 'test_export'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            routing_table_limit_number = 10000
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            alert_percent_value  = 50

        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            route_target_attr['100:1'].rt_type  = 'export'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            route_target_attr['200:1'].rt_type  = 'export'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            route_target_attr['300:1'].rt_type  = 'import'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            route_target_attr['400:1'].rt_type  = 'import'


        # Build config
        cfgs = vrf_conf.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf definition VRF2',
                ' rd 100:1',
                ' address-family ipv6 unicast',
                '  import ipv6 unicast map test_import',
                '  export ipv6 unicast map test_export',
                '  maximum routes 10000 50',
                '  route-target export 100:1',
                '  route-target export 200:1',
                '  route-target import 300:1',
                '  route-target import 400:1',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = vrf_conf.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no vrf definition VRF2',
            ]))

        # Build unconfig for selected attributes
        cfgs = vrf_conf.build_unconfig(apply=False,
                                       attributes={'device_attr': {
                                                        self.dev1: {
                                                            'rd': None,
                                                             'address_family_attr': {
                                                                'ipv6 unicast': {
                                                                    'routing_table_limit_number': None,
                                                                    'alert_percent_value': None,
                                                                }
                                                             }}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf definition VRF2',
                ' no rd 100:1',
                ' address-family ipv6 unicast',
                '  no maximum routes 10000 50',
                '  exit',
                ' exit',
            ]))

        # Build unconfig for selected attributes
        cfgs = vrf_conf.build_unconfig(apply=False,
                                       attributes={'device_attr': {self.dev1: {
                                                           'address_family_attr': {'ipv6 unicast': {
                                                              'route_target_attr': {'200:1': {
                                                                'rt_type': None}
                                                           }}}}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf definition VRF2',
                ' address-family ipv6 unicast',
                '  no route-target export 200:1',
                '  exit',
                ' exit',
            ]))


if __name__ == '__main__':
    unittest.main()

