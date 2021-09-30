#!/usr/bin/env python

#python
import unittest
from unittest.mock import Mock

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# Genie XBu_shared
from genie.libs.conf.vxlan.vxlan import Vxlan


class test_vxlan(TestCase):

    def test_vxlan_enable_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        vxlan = Vxlan()
        vxlan.device_attr[dev1].enabled = True

        self.assertIs(vxlan.testbed, testbed)
        dev1.add_feature(vxlan)

        cfgs = vxlan.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['feature nv overlay',
             'feature vn-segment-vlan-based',
             'nv overlay evpn',
             ]))

        un_cfgs = vxlan.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(
            ['no feature nv overlay',
             'no feature vn-segment-vlan-based',
             'no nv overlay evpn',
             ]))

    def test_trm_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='R2', os='nxos')

        vxlan = Vxlan()
        vxlan.device_attr[dev1].enabled_ngmvpn = True
        vxlan.device_attr[dev1].advertise_evpn_multicast = True

        self.assertIs(vxlan.testbed, testbed)
        dev1.add_feature(vxlan)

        cfgs = vxlan.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['feature ngmvpn',
             'advertise evpn multicast',
             ]))

        un_cfgs = vxlan.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(
            ['no feature ngmvpn',
             'no advertise evpn multicast',
             ]))

    def test_vxlan_basic_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        vxlan = Vxlan()
        vxlan.device_attr[dev1].enabled_nv_overlay = True
        vxlan.device_attr[dev1].enabled_vn_segment_vlan_based = True
        vxlan.device_attr[dev1].enabled_nv_overlay_evpn = True
        vxlan.device_attr[dev1].fabric_fwd_anycast_gw_mac = '0002.0002.0002'

        self.assertIs(vxlan.testbed, testbed)
        dev1.add_feature(vxlan)
        cfgs = vxlan.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['feature nv overlay',
             'feature vn-segment-vlan-based',
             'nv overlay evpn',
             'fabric forwarding anycast-gateway-mac 0002.0002.0002',
             ]))

        un_cfgs = vxlan.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(
            ['no feature nv overlay',
             'no feature vn-segment-vlan-based',
             'no nv overlay evpn',
             ]))

    def test_vxlan_fabric_forwarding_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        vxlan = Vxlan()
        vxlan.device_attr[dev1].fabric_fwd_anycast_gw_mac = '0002.0002.0002'

        self.assertIs(vxlan.testbed, testbed)
        dev1.add_feature(vxlan)
        cfgs = vxlan.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['fabric forwarding anycast-gateway-mac 0002.0002.0002',
             ]))

        un_cfgs = vxlan.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(
            ['no fabric forwarding anycast-gateway-mac 0002.0002.0002',
             ]))

    def test_vxlan_evpn_msite(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        vxlan = Vxlan()
        vxlan.device_attr[dev1].evpn_msite_attr[11111].evpn_msite_bgw_delay_restore_time = 30
        self.assertIs(vxlan.testbed, testbed)
        dev1.add_feature(vxlan)

        cfgs = vxlan.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['evpn multisite border-gateway 11111',
             ' delay-restore time 30',
             ' exit',
             ]))

        uncfgs = vxlan.build_unconfig(apply=False)
        self.assertCountEqual(uncfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(uncfgs[dev1.name]), '\n'.join(
            ['no evpn multisite border-gateway 11111'
             ]))
        # uncfg with attributes
        uncfgs_1 = vxlan.build_unconfig(apply=False,
                                   attributes={'device_attr': {
                                       dev1 : {
                                           'evpn_msite_attr': {
                                               '*': {
                                               'evpn_msite_bgw_delay_restore_time': None
                                               }}}}})
        self.assertMultiLineEqual(str(uncfgs_1[dev1.name]), '\n'.join([
            'evpn multisite border-gateway 11111',
            ' no delay-restore time 30',
            ' exit',
        ]))

    def test_vxlan_evpn_msite_advertise_pip(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        vxlan = Vxlan()
        vxlan.device_attr[dev1].evpn_msite_attr[11111].evpn_msite_dci_advertise_pip = True
        self.assertIs(vxlan.testbed, testbed)
        dev1.add_feature(vxlan)

        cfgs = vxlan.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        print(str(cfgs[dev1.name]))
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['evpn multisite border-gateway 11111',
             ' dci-advertise-pip',
             ' exit'
             ]))

        uncfgs = vxlan.build_unconfig(apply=False)
        self.assertCountEqual(uncfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(uncfgs[dev1.name]), '\n'.join(
            ['no evpn multisite border-gateway 11111'
             ]))
        # uncfg with attributes
        uncfgs_1 = vxlan.build_unconfig(apply=False,
                                        attributes={'device_attr': {
                                            dev1: {
                                                'evpn_msite_attr': {
                                                    '*': {
                                                        'evpn_msite_dci_advertise_pip': True
                                                    }}}}})
        self.assertMultiLineEqual(str(uncfgs_1[dev1.name]), '\n'.join([
            'evpn multisite border-gateway 11111',
            ' no dci-advertise-pip',
            ' exit',
        ]))

    def test_vxlan_evpn_msite_split_horizon(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        vxlan = Vxlan()
        vxlan.device_attr[dev1].evpn_msite_attr[11111].evpn_msite_split_horizon_per_site = True
        self.assertIs(vxlan.testbed, testbed)
        dev1.add_feature(vxlan)

        cfgs = vxlan.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['evpn multisite border-gateway 11111',
             ' split-horizon per-site',
             ' exit'
             ]))

        uncfgs = vxlan.build_unconfig(apply=False)
        self.assertCountEqual(uncfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(uncfgs[dev1.name]), '\n'.join(
            ['no evpn multisite border-gateway 11111'
             ]))
        # uncfg with attributes
        uncfgs_1 = vxlan.build_unconfig(apply=False,
                                        attributes={'device_attr': {
                                            dev1: {
                                                'evpn_msite_attr': {
                                                    '*': {
                                                        'evpn_msite_split_horizon_per_site': True
                                                    }}}}})
        self.assertMultiLineEqual(str(uncfgs_1[dev1.name]), '\n'.join([
            'evpn multisite border-gateway 11111',
            ' no split-horizon per-site',
            ' exit',
        ]))

    def test_vxlan_evpn(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        vxlan = Vxlan()
        vxlan.device_attr[dev1].evpn_attr[None].vni_attr[11].evpn_vni_rd = 'auto'
        self.assertIs(vxlan.testbed, testbed)
        dev1.add_feature(vxlan)

        cfgs = vxlan.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['evpn',
             ' vni 11 l2',
             '  rd auto',
             '  exit',
             ' exit',
             ]))

        un_cfgs = vxlan.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(
            ['no evpn',
             ]))

        un_cfgs_partial = vxlan.build_unconfig(apply=False,attributes={'device_attr':{
                                                                           dev1.name :{
                                                                                'evpn_attr':{
                                                                                     '*':{
                                                                                     'vni_attr':{
                                                                                         '*':{
                                                                                             'evpn_vni_rd':None
                                                                                         }}
                                                                                         }}}}})
        self.assertCountEqual(un_cfgs_partial.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs_partial[dev1.name]), '\n'.join(
            ['evpn',
              ' vni 11 l2',
              '  no rd auto',
              '  exit',
              ' exit',
             ]))
        un_cfgs_partial_2 = vxlan.build_unconfig(apply=False, attributes={'device_attr': {
                                                                                    dev1.name: {
                                                                                        'evpn_attr': {
                                                                                            '*': {
                                                                                               'vni_attr':{
                                                                                                   '*':None
                                                                                               }
                                                                                            }
                                                                                            }}}})
        self.assertCountEqual(un_cfgs_partial_2.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs_partial_2[dev1.name]), '\n'.join(
            ['evpn',
             ' no vni 11 l2',
             ' exit',
             ]))

    def test_vxlan_evpn_vni_route_type(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        vxlan = Vxlan()
        vxlan.device_attr[dev1].evpn_attr[None].vni_attr[11].route_target_attr['auto'].evpn_vni_rt_type = 'both'
        self.assertIs(vxlan.testbed, testbed)
        dev1.add_feature(vxlan)

        cfgs = vxlan.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['evpn',
             ' vni 11 l2',
             '  route-target both auto',
             '  exit',
             ' exit',
             ]))

        un_cfgs_partial = vxlan.build_unconfig(apply=False, attributes={'device_attr': {
                                                                                dev1.name: {
                                                                                    'evpn_attr': {
                                                                                        '*': {
                                                                                            'vni_attr': {
                                                                                                '*': {
                                                                                                    'route_target_attr':{
                                                                                                        "*":None
                                                                                                    }}}}}}}})
        self.assertCountEqual(un_cfgs_partial.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs_partial[dev1.name]), '\n'.join(
             ['evpn',
              ' vni 11 l2',
              '  no route-target both auto',
              '  exit',
              ' exit',
              ]))


if __name__ == '__main__':
    unittest.main()
