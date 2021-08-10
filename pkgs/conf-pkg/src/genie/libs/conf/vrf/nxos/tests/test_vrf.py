#!/usr/bin/env python

'''
NXOS unit tests for Genie Vrf conf using CLI.
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
        self.dev1 = Device(name='PE1', testbed=testbed, os='nxos')

    def test_cli_config_vni(self):
        vrf_conf = Vrf('VRF1')
        self.dev1.add_feature(vrf_conf)
        vrf_conf.device_attr[self.dev1].vni = 4092
        vrf_conf.device_attr[self.dev1].vni_mode_l3 = 4091
        cfgs = vrf_conf.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf context VRF1',
                ' vni 4092',
                ' vni 4091 l3',
                ' exit',
            ]))

        # Build unconfig for vni attribute
        cfgs = vrf_conf.build_unconfig(apply=False,
                                       attributes={'device_attr': {
                                           self.dev1: {
                                               'vni': None,
                                               'vni_mode_l3': None,
                                                   }}})
        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf context VRF1',
                ' no vni 4092',
                ' no vni 4091 l3',
                ' exit',
            ]))

    def test_cli_trm_config(self):
        vrf_conf = Vrf('VRF1')
        self.dev1.add_feature(vrf_conf)

        # Apply configuration
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 mvpn']. \
            route_target_attr['200:1'].rt_type = 'import'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 mvpn']. \
            route_target_attr['200:1'].protocol_attr['mvpn'].rt_mvpn = True

        # Build config
        cfgs = vrf_conf.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf context VRF1',
                ' address-family ipv4 mvpn',
                '  route-target import 200:1',
                '  route-target import 200:1 mvpn',
                '  exit',
                ' exit',
            ]))

        # # Build unconfig for selected attributes
        uncfgs = vrf_conf.build_unconfig(apply=False,
                                       attributes={'device_attr': {
                                           self.dev1: {
                                                'address_family_attr': {
                                                    'ipv4 mvpn': {
                                                        'route_target_attr': {
                                                            '200:1': {
                                                                'rt_type': 'both',
                                                                'protocol_attr':{
                                                                    'mvpn':{
                                                                        'rt_mvpn': None,
                                                                        }
                                                                    }
                                                                }
                                                          }
                                                    }}}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(uncfgs[self.dev1.name]),
            '\n'.join([
                'vrf context VRF1',
                ' address-family ipv4 mvpn',
                '  route-target import 200:1',
                '  route-target export 200:1',
                '  no route-target both 200:1 mvpn',
                '  exit',
                ' exit',
            ]))
    def test_cli_trm_mvpn_config(self):
        vrf_conf = Vrf('VRF1')
        self.dev1.add_feature(vrf_conf)

        # Apply configuration
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 mvpn']. \
            route_target_attr['200:1'].rt_type = 'import'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 mvpn']. \
            route_target_attr['200:1'].protocol_attr['mvpn'].rt_mvpn = True

        # Build config
        cfgs = vrf_conf.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf context VRF1',
                ' address-family ipv4 mvpn',
                '  route-target import 200:1',
                '  route-target import 200:1 mvpn',
                '  exit',
                ' exit',
            ]))

        # # Build unconfig for selected attributes
        uncfgs = vrf_conf.build_unconfig(apply=False,
                                       attributes={'device_attr': {
                                           self.dev1: {
                                                'address_family_attr': {
                                                    'ipv4 mvpn': {
                                                        'route_target_attr': {
                                                            '200:1': {
                                                                'rt_type': 'import',
                                                                'protocol_attr':{
                                                                    'mvpn':{
                                                                        'rt_mvpn': None,
                                                                        }
                                                                    }
                                                                }
                                                          }
                                                    }}}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(uncfgs[self.dev1.name]),
            '\n'.join([
                'vrf context VRF1',
                ' address-family ipv4 mvpn',
                '  route-target import 200:1',
                '  no route-target import 200:1 mvpn',
                '  exit',
                ' exit',
            ]))

    def test_cli_vxlan_evpn_config(self):
        vrf_conf = Vrf('VRF1')
        self.dev1.add_feature(vrf_conf)

        # Apply configuration
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 unicast']. \
            route_target_attr['200:1'].rt_type = 'both'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 unicast']. \
            route_target_attr['200:1'].protocol_attr['evpn'].rt_evpn = True

        # Build config
        cfgs = vrf_conf.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf context VRF1',
                ' address-family ipv4 unicast',
                '  route-target import 200:1',
                '  route-target export 200:1',
                '  route-target both 200:1 evpn',
                '  exit',
                ' exit',
            ]))

        # Build unconfig for selected attributes
        uncfgs = vrf_conf.build_unconfig(apply=False,
                                         attributes={'device_attr': {
                                             self.dev1: {
                                                 'address_family_attr': {
                                                     'ipv4 unicast': {
                                                         'route_target_attr': {
                                                             '200:1': {
                                                                 'rt_type': 'both',
                                                                 'protocol_attr': {
                                                                     'evpn': {
                                                                         'rt_evpn': None,
                                                                     }
                                                                 }
                                                             }
                                                         }
                                                     }}}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(uncfgs[self.dev1.name]),
            '\n'.join([
                'vrf context VRF1',
                ' address-family ipv4 unicast',
                '  route-target import 200:1',
                '  route-target export 200:1',
                '  no route-target both 200:1 evpn',
                '  exit',
                ' exit',
            ]))

    def test_cli_config_v4(self):
        # prefix-list conf
        vrf_conf = Vrf('VRF1')
        self.dev1.add_feature(vrf_conf)

        # Apply configuration
        vrf_conf.device_attr[self.dev1].rd = '100:1'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 unicast'].\
            import_from_global_map = 'import_from_global_map'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 unicast'].\
            routing_table_limit_number = 10000
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 unicast'].\
            simple_alert  = True

        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 unicast'].\
            route_target_attr['200:1'].rt_type  = 'both'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv4 unicast'].\
            route_target_attr['100:1'].rt_type  = 'import'

        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            routing_table_limit_number = 10000
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            alert_percent_value  = 70

        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            route_target_attr['200:1'].rt_type  = 'import'
        vrf_conf.device_attr[self.dev1].address_family_attr['ipv6 unicast'].\
            route_target_attr['100:1'].rt_type  = 'export'


        # Build config
        cfgs = vrf_conf.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf context VRF1',
                ' rd 100:1',
                ' address-family ipv4 unicast',
                '  import vrf default map import_from_global_map',
                '  maximum routes 10000 warning-only',
                '  route-target import 100:1',
                '  route-target import 200:1',
                '  route-target export 200:1',
                '  exit',
                ' address-family ipv6 unicast',
                '  maximum routes 10000 70',
                '  route-target export 100:1',
                '  route-target import 200:1',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = vrf_conf.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no vrf context VRF1',
            ]))

        # Build unconfig for selected attributes
        cfgs = vrf_conf.build_unconfig(apply=False,
                                       attributes={'device_attr': {
                                                        self.dev1: {
                                                            'rd': None,
                                                             'address_family_attr': {
                                                                'ipv4 unicast': {
                                                                    'import_from_global_map': None
                                                                }
                                                             }}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'vrf context VRF1',
                ' no rd 100:1',
                ' address-family ipv4 unicast',
                '  no import vrf default map import_from_global_map',
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
                'vrf context VRF1',
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
                'vrf context VRF2',
                ' rd 100:1',
                ' address-family ipv6 unicast',
                '  import vrf default map test_import',
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
                'no vrf context VRF2',
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
                'vrf context VRF2',
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
                'vrf context VRF2',
                ' address-family ipv6 unicast',
                '  no route-target import 200:1',
                '  no route-target export 200:1',
                '  exit',
                ' exit',
            ]))


    def test_learn_config(self):

        testbed = Testbed()
        dev = Device(testbed=testbed, name='PE1', os='nxos')
        dev.custom = {'abstraction': {'order': ['os'], 'context': 'cli'}}

        golden_output = {'return_value': '''
R2# show run vrf vni_10100 | sec '^vrf'
vrf context vni_10100
  vni 10100
  rd auto
  address-family ipv4 unicast
    route-target both auto
    route-target both auto mvpn
    route-target both auto evpn
 '''}
        golden_output2 = {'return_value': '''
R2# show run vrf vni_10100 | sec '^vrf'
vrf context vni_10100
  vni 10100 l3
  rd auto
  address-family ipv4 unicast
    route-target both auto
    route-target both auto mvpn
    route-target both auto evpn
 '''}

        vrf = Vrf('vni_10100')

        # Return outputs above as inputs to parser when called
        dev.execute = Mock(**golden_output)
        dev.execute = Mock(**golden_output2)

        vrf.device_attr[dev]

        learn = Vrf.learn_config(device=dev)
        if learn:
            self.assertEqual(learn[0].device_attr[dev].address_family_attr['ipv4 unicast'].\
                         route_target_attr['auto'].protocol_attr['mvpn'].rt_mvpn, True)

if __name__ == '__main__':
    unittest.main()

