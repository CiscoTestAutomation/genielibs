#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.l2vpn import IccpGroup


class test_iccp_group(unittest.TestCase):

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
            grp1 = IccpGroup()

        grp1 = IccpGroup(group_id=1)
        self.assertEqual(grp1.group_id, 1)

        self.assertCountEqual(grp1.devices, [])
        self.assertCountEqual(grp1.interfaces, [])

        dev1.add_feature(grp1)
        self.assertCountEqual(grp1.devices, [dev1])
        self.assertCountEqual(grp1.interfaces, [])

        cfgs = grp1.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
            'redundancy',
            ' iccp group 1',
            '  exit',
            ' exit',
            ]))

        grp1.add_interface(intf1)
        self.assertCountEqual(grp1.interfaces, [intf1])
        self.assertCountEqual(grp1.devices, [dev1])
        self.assertCountEqual(grp1.device_attr[dev1].interfaces, [intf1])
        self.assertCountEqual(grp1.device_attr[dev2].interfaces, [])

        cfgs = grp1.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
            'redundancy',
            ' iccp group 1',
            '  interface GigabitEthernet0/0/0/1',
            '   exit',
            '  exit',
            ' exit',
            ]))

        dev2.add_feature(grp1)
        grp1.add_interface(intf2)
        grp1.add_interface(intf3)
        grp1.mac_flush = 'stp-tcn'
        grp1.device_attr[dev1].recovery_delay = 100
        grp1.device_attr[intf1.device].interface_attr[intf1].primary_vlan = 1
        grp1.device_attr[intf1.device].interface_attr[intf1].mac_flush = None

        self.assertCountEqual(grp1.interfaces, [intf1, intf2, intf3])
        self.assertCountEqual(grp1.devices, [dev1, dev2])
        self.assertCountEqual(grp1.device_attr[dev1].interfaces, [intf1, intf2])
        self.assertCountEqual(grp1.device_attr[dev2].interfaces, [intf3])

        cfgs = grp1.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name, dev2.name])
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
            'redundancy',
            ' iccp group 1',
            '  interface GigabitEthernet0/0/0/1',
            '   primary vlan 1',
            '   recovery delay 100',
            '   exit',
            '  interface GigabitEthernet0/0/0/2',
            '   mac-flush stp-tcn',
            '   recovery delay 100',
            '   exit',
            '  exit',
            ' exit',
            ]))
        self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join([
            'redundancy',
            ' iccp group 1',
            '  interface GigabitEthernet0/0/0/3',
            '   mac-flush stp-tcn',
            '   exit',
            '  exit',
            ' exit',
            ]))

if __name__ == '__main__':
    unittest.main()

