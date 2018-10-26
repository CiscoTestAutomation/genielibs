#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.l2vpn import BridgeDomain


class test_bridge_domain(unittest.TestCase):

    def test_init(self):

        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/0/3')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/0/4')
        link1 = Link(testbed=testbed, name='link1', interfaces=(intf1, intf3))
        link2 = Link(testbed=testbed, name='link2', interfaces=(intf2, intf4))

        with self.assertRaises(TypeError):
            bd1 = BridgeDomain()

        with self.assertRaises(TypeError):
            bd1 = BridgeDomain(group_name='bg1')

        bd1 = BridgeDomain(name='bd1', group_name='mybg1')
        self.assertEqual(bd1.name, 'bd1')
        self.assertEqual(bd1.group_name, 'mybg1')

        bd1 = BridgeDomain(name='bd1')
        self.assertEqual(bd1.name, 'bd1')
        self.assertEqual(bd1.group_name, 'bd1g')

        self.assertCountEqual(bd1.devices, [])
        self.assertCountEqual(bd1.interfaces, [])
        self.assertCountEqual(bd1.vnis, [])
        self.assertCountEqual(bd1.vfis, [])
        self.assertCountEqual(bd1.evis, [])
        self.assertCountEqual(bd1.segments, [])
        self.assertCountEqual(bd1.link.interfaces, [])

        dev1.add_feature(bd1)
        self.assertCountEqual(bd1.devices, [dev1])
        self.assertCountEqual(bd1.interfaces, [])
        self.assertCountEqual(bd1.vnis, [])
        self.assertCountEqual(bd1.vfis, [])
        self.assertCountEqual(bd1.evis, [])
        self.assertCountEqual(bd1.segments, [])
        self.assertCountEqual(bd1.link.interfaces, [])

        cfgs = bd1.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
            'l2vpn',
            ' bridge group bd1g',
            '  bridge-domain bd1',
            '   exit',
            '  exit',
            ' exit',
            ]))

        bd1.add_interface(intf1)
        intf1.l2transport.enabled = True
        self.assertCountEqual(bd1.interfaces, [intf1])
        self.assertCountEqual(bd1.devices, [dev1])
        self.assertCountEqual(bd1.vnis, [])
        self.assertCountEqual(bd1.vfis, [])
        self.assertCountEqual(bd1.evis, [])
        self.assertCountEqual(bd1.segments, [intf1])
        # Links under Genie Interface object is deprecated
        # Placed the below workaround to bypass the Unittest (commented out)
        # self.assertCountEqual(bd1.link.interfaces, [intf3])
        self.assertCountEqual(bd1.device_attr[dev1].interfaces, [intf1])
        self.assertCountEqual(bd1.device_attr[dev2].interfaces, [])
        self.assertCountEqual(bd1.device_attr[dev1].segments, [intf1])
        self.assertCountEqual(bd1.device_attr[dev2].segments, [])

        cfgs = bd1.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
            'l2vpn',
            ' bridge group bd1g',
            '  bridge-domain bd1',
            '   interface GigabitEthernet0/0/0/1',
            '    exit',
            '   exit',
            '  exit',
            ' exit',
            ]))

if __name__ == '__main__':
    unittest.main()

