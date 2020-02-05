#!/usr/bin/env python

#python
import unittest
# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# Genie XBu_shared
from genie.libs.conf.nd.nd import Nd


class test_nd(TestCase):

    def test_nd_with_interface_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        nd = Nd()
        nd.interface = 'Ethernet0/1'

        nd.device_attr[dev1].interface_attr[nd.interface].if_ra_interval = 201
        nd.device_attr[dev1].interface_attr[nd.interface].if_ra_lifetime = 1802
        nd.device_attr[dev1].interface_attr[nd.interface].if_ra_suppress = True

        self.assertIs(nd.testbed, testbed)
        dev1.add_feature(nd)
        cfgs = nd.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
           ['interface Ethernet0/1',
            ' ipv6 nd ra-interval 201',
            ' ipv6 nd ra-lifetime 1802',
            ' ipv6 nd suppress-ra',
            ' exit',
        ]))
        uncfg = nd.build_unconfig(apply=False, attributes={
                                                    'device_attr':
                                                        { dev1.name:
                                                                {'interface_attr': {
                                                                '*': {
                                                                    'if_ra_interval': None,
                                                                    'if_ra_lifetime': None,
                                                                    'if_ra_suppress': False,
                                                                     }}}}})

        self.assertCountEqual(uncfg.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(uncfg[dev1.name]), '\n'.join(
            ['interface Ethernet0/1',
             ' no ipv6 nd ra-interval 201',
             ' no ipv6 nd ra-lifetime 1802',
             ' no ipv6 nd suppress-ra',
             ' exit',
             ]))

        uncfg_intf = nd.build_unconfig(apply=False)
        self.maxDiff = None
        self.assertEqual(str(uncfg_intf[dev1.name]), '\n'.join(
            ['no interface Ethernet0/1',
             ]))

    def test_nd_neighbor_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        nd = Nd()
        nd.interface = 'Ethernet1/1'
        nd.ip = '2010:2:3::33'

        nd.device_attr[dev1].interface_attr[nd.interface].neighbor_attr[nd.ip].link_layer_address = 'aabb.beef.cccc'
        self.assertIs(nd.testbed, testbed)
        dev1.add_feature(nd)

        cfgs = nd.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), '\n'.join(
            ['interface Ethernet1/1',
             ' ipv6 neighbor 2010:2:3::33 aabb.beef.cccc',
             ' exit'
             ]))
        uncfg = nd.build_unconfig(apply=False, attributes={
                                                        'device_attr':
                                                            {dev1.name:
                                                                {'interface_attr': {
                                                                    '*': { 'neighbor_attr':{
                                                                        '*':None}}}}}})
        self.assertCountEqual(uncfg.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(uncfg[dev1.name]), '\n'.join(
            ['interface Ethernet1/1',
             ' no ipv6 neighbor 2010:2:3::33 aabb.beef.cccc',
             ' exit',
             ]))
if __name__ == '__main__':
    unittest.main()
