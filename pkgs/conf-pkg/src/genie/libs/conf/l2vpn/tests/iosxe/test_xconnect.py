#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.l2vpn import Xconnect
from genie.libs.conf.bgp import RouteTarget

class test_xconnect(unittest.TestCase):

    def test_init(self):

        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/1')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/2')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/3')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/4')
        link1 = Link(testbed=testbed, name='link1', interfaces=(intf1, intf3))
        link2 = Link(testbed=testbed, name='link2', interfaces=(intf2, intf4))

        with self.assertRaises(TypeError):
            xc1 = Xconnect()

        xc1 = Xconnect(name='xc1')
        self.assertIs(xc1.xconnect_type, Xconnect.Type.p2p)
        self.assertEqual(xc1.name, 'xc1')

        self.assertCountEqual(xc1.devices, [])
        self.assertCountEqual(xc1.interfaces, [])
        self.assertCountEqual(xc1.segments, [])
        self.assertCountEqual(xc1.link.interfaces, [])

        dev1.add_feature(xc1)
        self.assertCountEqual(xc1.devices, [dev1])
        self.assertCountEqual(xc1.interfaces, [])
        self.assertCountEqual(xc1.segments, [])
        self.assertCountEqual(xc1.link.interfaces, [])

        cfgs = xc1.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
            'l2vpn xconnect context xc1',
            ' exit',
            ]))

        efp = Interface(device=dev1, name='GigabitEthernet0/0/1.20',service_instance=20)
        efp.encapsulation = 'dot1q'
        efp.rewrite_ingress = 'pop 1 symmetric'

        xc1.add_segment(efp)
        self.assertCountEqual(xc1.interfaces, [efp])
        self.assertCountEqual(xc1.devices, [dev1])
        self.assertCountEqual(xc1.segments, [efp])
        self.assertCountEqual(xc1.device_attr[dev1].interfaces, [efp])
        self.assertCountEqual(xc1.device_attr[dev2].interfaces, [])
        self.assertCountEqual(xc1.device_attr[dev1].segments, [efp])
        self.assertCountEqual(xc1.device_attr[dev2].segments, [])

        cfgs = xc1.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
            'l2vpn xconnect context xc1',
            ' member GigabitEthernet0/0/1 service-instance 20',
            ' exit',
            ]))

if __name__ == '__main__':
    unittest.main()

