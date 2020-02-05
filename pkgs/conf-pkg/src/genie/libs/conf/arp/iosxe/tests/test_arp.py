#!/usr/bin/env python

# import python
import unittest

# import genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Interface

# import genie.libs
from genie.libs.conf.arp import Arp

class test_arp(TestCase):
    def test_arp_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        arp = Arp()
        arp.device_attr[dev1].max_entries = 100

        self.assertIs(arp.testbed, testbed)
        dev1.add_feature(arp)

        cfgs = arp.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['arp entries interface-limit 100',
             ]))

        un_cfgs = arp.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(
            ['no arp entries interface-limit 100']))


    def test_arp_sub_interface_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        arp = Arp()
        intf= 'GigabitEthernet2'
        arp.device_attr[dev1].interface_attr[intf].if_proxy_enable = True
        arp.device_attr[dev1].interface_attr[intf].if_local_proxy_enable = True
        arp.device_attr[dev1].interface_attr[intf].if_expire_time = 10

        self.assertIs(arp.testbed, testbed)
        dev1.add_feature(arp)

        cfg_all = arp.build_config(apply=False)
        self.assertCountEqual(cfg_all.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfg_all[dev1.name]), '\n'.join(
            ['interface GigabitEthernet2',
             ' ip proxy-arp',
             ' ip local-proxy-arp',
             ' arp timeout 10',
             ' exit'
             ]))

        un_cfg_all = arp.build_unconfig(apply=False)
        self.assertCountEqual(un_cfg_all.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfg_all[dev1.name]), '\n'.join(
            ['interface GigabitEthernet2',
             ' no ip proxy-arp',
             ' no ip local-proxy-arp',
             ' no arp timeout 10',
             ' exit'
             ]))

    def test_static_arp_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        arp = Arp()
        intf = 'GigabitEthernet2'
        arp.device_attr[dev1].interface_attr[intf].static_arp_attr['10.10.10.10'].if_static_mac_address ='aaaa.bbbb.cccc'
        arp.device_attr[dev1].interface_attr[intf].static_arp_attr['10.10.10.10'].if_static_encap_type ='arpa'

        self.assertIs(arp.testbed, testbed)
        dev1.add_feature(arp)

        cfg_all = arp.build_config(apply=False)
        self.assertCountEqual(cfg_all.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfg_all[dev1.name]), '\n'.join(
            ['arp 10.10.10.10 aaaa.bbbb.cccc arpa']))

        un_cfg_all = arp.build_unconfig(apply=False)
        self.assertCountEqual(un_cfg_all.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfg_all[dev1.name]), '\n'.join(
            ['no arp 10.10.10.10 aaaa.bbbb.cccc arpa']))


    def test_static_arp_with_vrf_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        intf = 'GigabitEthernet2'

        arp2 = Arp()
        arp2.device_attr[dev1].interface_attr[intf].static_arp_attr[
            '10.10.10.10'].if_static_mac_address = 'aaaa.bbbb.cccc'
        arp2.device_attr[dev1].interface_attr[intf].static_arp_attr['10.10.10.10'].if_static_encap_type = 'arpa'
        arp2.device_attr[dev1].interface_attr[intf].static_arp_attr['10.10.10.10'].if_static_vrf = 'VRF1'
        arp2.device_attr[dev1].interface_attr[intf].static_arp_attr['10.10.10.10'].if_static_alias = True
        self.assertIs(arp2.testbed, testbed)
        dev1.add_feature(arp2)

        cfg = arp2.build_config(apply=False)
        self.assertCountEqual(cfg.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfg[dev1.name]), '\n'.join(
            ['arp vrf VRF1 10.10.10.10 aaaa.bbbb.cccc arpa alias']))

        un_cfg = arp2.build_unconfig(apply=False)
        self.assertCountEqual(un_cfg.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfg[dev1.name]), '\n'.join(
            ['no arp vrf VRF1 10.10.10.10 aaaa.bbbb.cccc arpa alias']))

if __name__ == '__main__':
    unittest.main()

