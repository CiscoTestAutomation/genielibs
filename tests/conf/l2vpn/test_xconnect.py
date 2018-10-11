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
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/0/3')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/0/4')
        link1 = Link(testbed=testbed, name='link1', interfaces=(intf1, intf3))
        link2 = Link(testbed=testbed, name='link2', interfaces=(intf2, intf4))

        with self.assertRaises(TypeError):
            xc1 = Xconnect()

        with self.assertRaises(TypeError):
            xc1 = Xconnect(group_name='bg1')

        xc1 = Xconnect(name='xc1', group_name='bg1')
        self.assertIs(xc1.xconnect_type, Xconnect.Type.p2p)
        self.assertEqual(xc1.name, 'xc1')
        self.assertEqual(xc1.group_name, 'bg1')

        xc1 = Xconnect(name='xc1')
        self.assertEqual(xc1.name, 'xc1')
        self.assertEqual(xc1.group_name, 'xc1g')

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
            'l2vpn',
            ' xconnect group xc1g',
            '  p2p xc1',
            '   exit',
            '  exit',
            ' exit',
            ]))

        #xc1.add_interface(intf1)
        intf1.l2transport.enabled = True
        #self.assertCountEqual(xc1.interfaces, [intf1])
        #self.assertCountEqual(xc1.devices, [dev1])
        #self.assertCountEqual(xc1.segments, [intf1])
        #self.assertCountEqual(xc1.link.interfaces, [intf3])
        #self.assertCountEqual(xc1.device_attr[dev1].interfaces, [intf1])
        #self.assertCountEqual(xc1.device_attr[dev2].interfaces, [])
        #self.assertCountEqual(xc1.device_attr[dev1].segments, [intf1])
        self.assertCountEqual(xc1.device_attr[dev2].segments, [])

        cfgs = xc1.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        if False:
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                'l2vpn',
                ' xconnect group xc1g',
                '  p2p xc1',
                '   interface GigabitEthernet0/0/0/1',
                '   exit',
                '  exit',
                ' exit',
                ]))

        dev2.add_feature(xc1)    
        xc1.xconnect_type = Xconnect.Type.mp2mp
        xc1.autodiscovery_bgp.enabled = True
        xc1.autodiscovery_bgp.signaling_protocol_bgp.enabled = True     
        xc1.autodiscovery_bgp.export_route_targets = [RouteTarget.ImportExport('1.1.1.1:1')]
        xc1.autodiscovery_bgp.import_route_targets = [RouteTarget.ImportExport('1.1.1.1:1')]
        xc1.autodiscovery_bgp.rd = '1000:1'
        xc1.device_attr[dev1].vpn_id = 100
        xc1.device_attr[dev2].vpn_id = 101        

        ce_id1 = 1001
        xc1.device_attr[dev1].autodiscovery_bgp.signaling_protocol_bgp.add_ce_id(ce_id1)
        xc1.device_attr[dev1].autodiscovery_bgp.signaling_protocol_bgp.ce_attr[ce_id1].add_interface(intf1)
        ce_id2 = 1000
        xc1.device_attr[dev2].autodiscovery_bgp.signaling_protocol_bgp.add_ce_id(ce_id1)
        xc1.device_attr[dev2].autodiscovery_bgp.signaling_protocol_bgp.ce_attr[ce_id2].add_interface(intf2)


        xc1.device_attr[dev1].autodiscovery_bgp.signaling_protocol_bgp.ce_attr[ce_id1].interface_attr[intf1].remote_ce_id = ce_id2
        xc1.device_attr[dev2].autodiscovery_bgp.signaling_protocol_bgp.ce_attr[ce_id2].interface_attr[intf2].remote_ce_id = ce_id1
        cfgs = xc1.build_config(apply=False)
        # TODO print(cfgs)

if __name__ == '__main__':
    unittest.main()

