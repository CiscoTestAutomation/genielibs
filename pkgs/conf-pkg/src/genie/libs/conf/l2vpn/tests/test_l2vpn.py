#!/usr/bin/env python

import unittest
from unittest.mock import Mock
from genie.tests.conf import TestCase

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.l2vpn import L2vpn


class test_l2vpn(TestCase):

    def test_init(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/0/3')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/0/4')

        Genie.testbed = None
        with self.assertRaises(TypeError):
            l2vpn = L2vpn()
        l2vpn = L2vpn(testbed=testbed)
        self.assertIs(l2vpn.testbed, testbed)
        Genie.testbed = testbed
        l2vpn = L2vpn()
        self.assertIs(l2vpn.testbed, testbed)

        self.assertIsNone(getattr(dev1, 'l2vpn', None))

        dev1.add_feature(l2vpn)
        self.assertIs(dev1.l2vpn, l2vpn)

        cfgs = l2vpn.build_config(apply=False)
        self.assertMultiLineDictEqual(cfgs, {
            dev1.name: '\n'.join([
                'l2vpn',
                ' exit',
                ]),
            })

        dev2.add_feature(l2vpn)
        self.assertIs(dev2.l2vpn, l2vpn)

        cfgs = l2vpn.build_config(apply=False)
        self.assertMultiLineDictEqual(cfgs, {
            dev1.name: '\n'.join([
                'l2vpn',
                ' exit',
                ]),
            dev2.name: '\n'.join([
                'l2vpn',
                ' exit',
                ]),
            })

        l2vpn.device_attr[dev1].router_id = '100.0.0.1'
        l2vpn.device_attr[dev2].router_id = '100.0.0.2'
        #l2vpn.recovery_timer = 100
        #l2vpn.device_attr[dev1].recovery_timer = 200
        #l2vpn.peering_timer = 300

        cfgs = l2vpn.build_config(apply=False)
        self.assertMultiLineDictEqual(cfgs, {
            dev1.name: '\n'.join([
                'l2vpn',
                ' router-id 100.0.0.1',
                ' exit',
                ]),
            dev2.name: '\n'.join([
                'l2vpn',
                ' router-id 100.0.0.2',
                ' exit',
                ]),
            })

if __name__ == '__main__':
    unittest.main()

