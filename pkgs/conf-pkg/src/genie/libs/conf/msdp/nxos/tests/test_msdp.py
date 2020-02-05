#!/usr/bin/env python

# python
import unittest
from unittest.mock import Mock

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device

# Genie XBu_shared
from genie.libs.conf.msdp.msdp import Msdp

outputs = {}

def mapper(key):
    return outputs[key]


class test_msdp(TestCase):
    def setUp(self):
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='nxos')

    def test_msdp_feature_cfg(self):

        msdp = Msdp()
        self.maxDiff = None

        self.dev1.add_feature(msdp)
        msdp.device_attr[self.dev1].enabled = True

        cfgs = msdp.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [self.dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.join(
           ['feature msdp',
        ]))

        uncfg = msdp.build_unconfig(apply=False)
        self.assertCountEqual(uncfg.keys(), [self.dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(uncfg[self.dev1.name]), '\n'.join(
            ['no feature msdp',
             ]))

    def test_msdp_vrf_default_cfg(self):

        msdp = Msdp()
        self.dev1.add_feature(msdp)
        vrf_name = 'default'
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].originating_rp = 'loopback2'
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].global_connect_retry_interval = 33

        cfgs = msdp.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [self.dev1.name])

        cfgs = msdp.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [self.dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs[self.dev1.name]), '\n'.join(
            ['ip msdp originator-id loopback2',
             'ip msdp reconnect-interval 33'
             ]))
        uncfg = msdp.build_unconfig(apply=False, attributes={
                                                        'device_attr':
                                                            {self.dev1.name:
                                                                {'vrf_attr': {
                                                                    vrf_name: {
                                                                        'originating_rp':None,
                                                                        'global_connect_retry_interval':None}}}}})
        self.assertCountEqual(uncfg.keys(), [self.dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(uncfg[self.dev1.name]), '\n'.join(
            ['no ip msdp originator-id loopback2',
             'no ip msdp reconnect-interval 33',
             ]))

    def test_msdp_vrf_cfg(self):
        msdp = Msdp()
        self.dev1.add_feature(msdp)
        vrf_name = 'VRF1'
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].originating_rp = 'loopback2'
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].global_connect_retry_interval = 33

        cfgs = msdp.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [self.dev1.name])

        cfgs = msdp.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [self.dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs[self.dev1.name]), '\n'.join(
            ['vrf context VRF1',
             ' ip msdp originator-id loopback2',
             ' ip msdp reconnect-interval 33',
             ' exit'
             ]))
        uncfg = msdp.build_unconfig(apply=False, attributes={
                                                        'device_attr':
                                                            {self.dev1.name:
                                                                {'vrf_attr': {
                                                                    vrf_name: {
                                                                        'originating_rp':None,
                                                                        'global_connect_retry_interval':None}}}}})
        self.assertCountEqual(uncfg.keys(), [self.dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(uncfg[self.dev1.name]), '\n'.join(
            ['vrf context VRF1',
             ' no ip msdp originator-id loopback2',
             ' no ip msdp reconnect-interval 33',
             ' exit',
             ]))

    def test_msdp_peer_cfg(self):
        msdp = Msdp()
        self.dev1.add_feature(msdp)
        vrf_name = 'default'
        address = '1.1.1.1'
        msdp.device_attr[self.dev1].enabled = True
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].peer_attr[address].peer_as = '100'
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].peer_attr[address].connected_source = 'loopback2'
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].peer_attr[address].enable = False
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].peer_attr[address].description = 'R1'
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].peer_attr[address].mesh_group = '1'
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].peer_attr[address].sa_filter_in = 'filtera'
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].peer_attr[address].sa_filter_out = 'filtera'
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].peer_attr[address].sa_limit = 111
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].peer_attr[address].keepalive_interval = 13
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].peer_attr[address].holdtime_interval = 50

        cfgs = msdp.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [self.dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs[self.dev1.name]), '\n'.join(
            ['feature msdp',
             'ip msdp peer 1.1.1.1 connect-source loopback2 remote-as 100',
             'ip msdp shutdown 1.1.1.1',
             'ip msdp description 1.1.1.1 R1',
             'ip msdp mesh-group 1.1.1.1 1',
             'ip msdp sa-policy 1.1.1.1 filtera in',
             'ip msdp sa-policy 1.1.1.1 filtera out',
             'ip msdp sa-limit 1.1.1.1 111',
             'ip msdp keepalive 1.1.1.1 13 50',
             ]))
        uncfg = msdp.build_unconfig(apply=False, attributes={
                                                        'device_attr':
                                                            {self.dev1.name:
                                                                {'vrf_attr': {
                                                                    'default': {
                                                                        'peer_attr': {
                                                                             '1.1.1.1': {
                                                                                 'address': None,
                                                                                 'enable':None,
                                                                                 'description':None,
                                                                                 'mesh_group':None,
                                                                                 'sa_filter_in':None,
                                                                                 'sa_filter_out':None,
                                                                                 'sa_limit':None,
                                                                                 'keepalive_interval':None,
                                                                                 'holdtime_interval':None}}}}}}})
        self.assertCountEqual(uncfg.keys(), [self.dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(uncfg[self.dev1.name]), '\n'.join(
            ['no ip msdp peer 1.1.1.1',
             'no ip msdp shutdown 1.1.1.1',
             'no ip msdp description 1.1.1.1 R1',
             'no ip msdp mesh-group 1.1.1.1 1',
             'no ip msdp sa-policy 1.1.1.1 filtera in',
             'no ip msdp sa-policy 1.1.1.1 filtera out',
             'no ip msdp sa-limit 1.1.1.1 111',
             'no ip msdp keepalive 1.1.1.1 13 50',
             ]))
        # unconfig msdp when all keys are configured
        uncfg_feature = msdp.build_unconfig(apply=False)
        self.assertCountEqual(uncfg_feature.keys(), [self.dev1.name])

        self.maxDiff = None
        self.assertMultiLineEqual(str(uncfg_feature[self.dev1.name]), '\n'.join(
            ['no feature msdp',
              ]))

    def test_msdp_enable_uncfg(self):
        msdp = Msdp()
        self.dev1.add_feature(msdp)
        vrf_name = 'default'
        address = '1.1.1.1'
        msdp.device_attr[self.dev1].vrf_attr[vrf_name].peer_attr[address].enable = True

        cfgs = msdp.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [self.dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs[self.dev1.name]), '\n'.join(
            ['no ip msdp shutdown 1.1.1.1',
             ]))
        uncfg = msdp.build_unconfig(apply=False, attributes={
                                                        'device_attr':
                                                            {self.dev1.name:
                                                                {'vrf_attr': {
                                                                    vrf_name: {
                                                                        'peer_attr': {
                                                                             address: {
                                                                                 'enable':None}}}}}}})
        self.assertCountEqual(uncfg.keys(), [self.dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(uncfg[self.dev1.name]), '\n'.join(
            ['ip msdp shutdown 1.1.1.1',
            ]))

    def test_learn_config(self):

        testbed = Testbed()
        dev = Device(testbed=testbed, name='PE2', os='nxos')
        dev.custom = {'abstraction':{'order':['os'], 'context':'cli'}}
        dev.mapping={}
        dev.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        dev.connectionmgr.connections['cli'] = dev

        golden_output = {'return_value': '''
            N95_2_R2# show run msdp
!Command: show running-config msdp
!Time: Mon Aug 27 20:17:11 2018

version 7.0(3)I7(3)
feature msdp

ip msdp description 6.6.6.6 test description
ip msdp keepalive 6.6.6.6 50 60
ip msdp reconnect-interval 15

vrf context VRF1
  ip msdp description 6.6.6.6 test description on VRF1
        '''}

        golden_output_vrf = '''
            N95_2_R2# show run pim | inc vrf
vrf context VRF1
        '''
        golden_output_reconnect = '''
            N95_2_R2# show run msdp | sec '^i' | inc reconnect-interval
ip msdp reconnect-interval 15
        '''
        golden_output_reconnect_vrf = '''
            N95_2_R2# show run msdp | sec VRF1 | inc reconnect-interval

        '''
        golden_output_description = '''
            N95_2_R2# show run msdp | sec '^i | inc description
ip msdp description 6.6.6.6 test description
        '''
        golden_output_description_vrf = '''
            N95_2_R2# show run msdp | sec VRF1 | inc description
  ip msdp description 6.6.6.6 test description on VRF1
        '''
        golden_output_keepalive = '''
            N95_2_R2# show run msdp | sec '^i' | inc keepalive
ip msdp keepalive 6.6.6.6 50 60
        '''
        golden_output_keepalive_vrf = '''
            N95_2_R2# show run msdp | sec VRF1 | inc keepalive
        '''
        golden_output_originator_id = '''
            N95_2_R2# show run msdp | sec '^i' | inc originator-id
ip msdp originator-id loopback0
        '''
        golden_output_originator_id_vrf = '''
            N95_2_R2# show run msdp | sec VRF1 | inc originator-id
  ip msdp originator-id loopback11
        '''
        golden_output_connect_source = '''
            N95_2_R2# show run msdp | sec '^i' | inc originator-id
ip msdp peer 6.6.6.6 connect-source loopback0
        '''
        golden_output_connect_source_vrf = '''
            N95_2_R2# show run msdp | sec VRF1 | inc originator-id
  ip msdp peer 6.6.6.6 connect-source loopback11 remote-as 234
        '''

        msdp = Msdp()
        outputs['show running-config msdp | inc vrf'] = golden_output_vrf
        outputs["show running-config msdp | sec '^i' | inc reconnect-interval"] = golden_output_reconnect
        outputs["show running-config msdp | sec VRF1 | inc reconnect-interval"] = golden_output_reconnect_vrf
        outputs["show running-config msdp | sec '^i' | inc description"] = golden_output_description
        outputs["show running-config msdp | sec VRF1 | inc description"] = golden_output_description_vrf
        outputs["show running-config msdp | sec '^i' | inc keepalive"] = golden_output_keepalive
        outputs["show running-config msdp | sec VRF1 | inc keepalive"] = golden_output_keepalive_vrf
        outputs["show running-config msdp | sec '^i' | inc originator-id"] = golden_output_originator_id
        outputs["show running-config msdp | sec VRF1 | inc originator-id"] = golden_output_originator_id_vrf
        outputs["show running-config msdp | sec '^i' | inc connect-source"] = golden_output_connect_source
        outputs["show running-config msdp | sec VRF1 | inc connect-source"] = golden_output_connect_source_vrf
        # Return outputs above as inputs to parser when called
        dev.execute = Mock()
        dev.execute.side_effect = mapper

        learn = Msdp.learn_config(device=dev,
                                  attributes=['msdp[vrf_attr][default][peer_attr][(.*)][description]'])

        self.assertEqual(learn[0].device_attr[dev].vrf_attr['default']\
                .peer_attr['6.6.6.6'].description, 'test description')
        self.assertEqual(learn[0].device_attr[dev].vrf_attr['default']\
                .peer_attr['6.6.6.6'].keepalive_interval, None)

        learn = Msdp.learn_config(device=dev)

        self.assertEqual(learn[0].device_attr[dev].vrf_attr['default']\
                .peer_attr['6.6.6.6'].keepalive_interval, 50)
        self.assertEqual(learn[0].device_attr[dev].vrf_attr['default']\
                .peer_attr['6.6.6.6'].holdtime_interval, 60)

        self.assertEqual(learn[0].device_attr[dev].vrf_attr['VRF1']\
                .peer_attr['6.6.6.6'].description, 'test description on VRF1')
        self.assertEqual(learn[0].device_attr[dev].vrf_attr['default']\
                .peer_attr['6.6.6.6'].description, 'test description')

        self.assertEqual(learn[0].device_attr[dev].vrf_attr['default']\
                .originating_rp, 'loopback0')
        self.assertEqual(learn[0].device_attr[dev].vrf_attr['VRF1']\
                .originating_rp, 'loopback11')

        self.assertEqual(learn[0].device_attr[dev].vrf_attr['default']\
                .peer_attr['6.6.6.6'].connected_source, 'loopback0')
        self.assertEqual(learn[0].device_attr[dev].vrf_attr['VRF1']\
                .peer_attr['6.6.6.6'].connected_source, 'loopback11')
        self.assertEqual(learn[0].device_attr[dev].vrf_attr['VRF1']\
                .peer_attr['6.6.6.6'].peer_as, '234')

        self.assertEqual(learn[0].device_attr[dev].vrf_attr['default']\
                .global_connect_retry_interval, 15)


if __name__ == '__main__':
    unittest.main()
