#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.isis import Isis
from genie.libs.conf.address_family import AddressFamily, AddressFamilySubAttributes



class test_isis(unittest.TestCase):

    def setUp(self):
        pass

        testbed = Genie.testbed = Testbed()
        self.dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        self.dev2 = Device(testbed=testbed, name='PE2', os='iosxe')
        self.intf1 = Interface(name='GigabitEthernet0/0/1',device=self.dev1)
        self.intf2 = Interface(name='GigabitEthernet0/0/2',device=self.dev2)

        self.link = Link(name='1_2_1',testbed=testbed)
        self.link.connect_interface(interface=self.intf1)
        self.link.connect_interface(interface=self.intf2)
        self.assertSetEqual(
            set(self.link.find_interfaces()),
            set([self.intf1, self.intf2]))
        self.assertSetEqual(
            set(self.dev1.find_interfaces()),
            set([self.intf1]))
        self.assertSetEqual(
            set(self.dev2.find_interfaces()),
            set([self.intf2]))

        isis = Isis("core")
        self.assertSetEqual(set(isis.devices), set([]))
        self.assertSetEqual(set(isis.links), set([]))

        self.link.add_feature(isis)
        for intf_iter in self.link.interfaces:
            intf_iter.add_feature(isis)
        self.assertCountEqual(isis.devices, [self.dev1, self.dev2])
        self.assertSetEqual(set(isis.links), set([self.link]))
        self.assertSetEqual(set(isis.interfaces), set([self.intf1, self.intf2]))

            
    def test_IsisGlobal(self):
        isis = Isis("core")
        self.link.add_feature(isis)

        # Global ISIS config
        isis.nsr = True

        # override default for both devices
        isis.is_type = Isis.IsType.level_1
        isis.device_attr['PE1'].is_type = Isis.IsType.level_1_2
        isis.device_attr['PE2'].is_type = Isis.IsType.level_2

        # use no default
        isis.device_attr['PE1'].nsf = Isis.Nsf.ietf
        isis.device_attr['PE2'].nsf = Isis.Nsf.cisco

        # override default for one device
        val = 1
        isis.device_attr['PE1'].net_id = "00.0000.0000.000{}.00".format(val)
        val += 1
        isis.device_attr['PE2'].net_id = "00.0000.0000.000{}.00".format(val)

        cfg1 = isis.build_config(apply=False)

        self.assertCountEqual(cfg1.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(str(cfg1['PE1']), '\n'.join([
            'router isis core',
            ' is-type level-1-2',
            ' nsf ietf',
            ' nsr',
            ' net 00.0000.0000.0001.00',
            ' exit',
            'interface GigabitEthernet0/0/1',
            ' ip router isis core',
            ' exit',
        ]))
        self.assertMultiLineEqual(str(cfg1['PE2']), '\n'.join([
            'router isis core',
            ' is-type level-2-only',
            ' nsf cisco',
            ' nsr',
            ' net 00.0000.0000.0002.00',
            ' exit',
            'interface GigabitEthernet0/0/2',
            ' ip router isis core',
            ' exit',
            ]))


        uncfg1 = isis.build_unconfig(apply=False)

        self.assertCountEqual(uncfg1.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(str(uncfg1['PE1']), '\n'.join([
            'no router isis core',
            'interface GigabitEthernet0/0/1',
            ' no ip router isis core',
            ' exit',
        ]))
        self.assertMultiLineEqual(str(uncfg1['PE2']), '\n'.join([
            'no router isis core',
            'interface GigabitEthernet0/0/2',
            ' no ip router isis core',
            ' exit',
            ]))

        partial_cfg1 = isis.build_config(apply=False,attributes='device_attr__PE1__nsf')
        self.assertCountEqual(partial_cfg1.keys(), ['PE1'])
        self.assertMultiLineEqual(str(partial_cfg1['PE1']), '\n'.join([
            'router isis core',
            ' nsf ietf',
            ' exit',
        ]))


    def test_IsisPerAddrFamily(self):

        isis = Isis("core")
        self.link.add_feature(isis)

        val = 1
        isis.device_attr['PE1'].net_id = "00.0000.0000.000{}.00".format(val)
        val += 1
        isis.device_attr['PE2'].net_id = "00.0000.0000.000{}.00".format(val)

        # per address family ISIS
        isis.device_attr['PE1'].address_family_attr['ipv4 unicast'].metric_style = "wide"
        isis.device_attr['PE1'].address_family_attr['ipv4 unicast'].mpls_te_level = Isis.IsType.level_1
        isis.device_attr['PE1'].address_family_attr['ipv4 unicast'].mpls_te_rtrid = self.intf1

        isis.device_attr['PE2'].address_family_attr['ipv4 unicast'].metric_style = "narrow"
        isis.device_attr['PE2'].address_family_attr['ipv4 unicast'].mpls_te_level = Isis.IsType.level_2
        isis.device_attr['PE2'].address_family_attr['ipv4 unicast'].mpls_te_rtrid = self.intf2

        cfg1 = isis.build_config(apply=False)

        self.assertMultiLineEqual(str(cfg1['PE1']), '\n'.join([
            'router isis core',
            ' net 00.0000.0000.0001.00',
            ' metric-style wide',
            ' mpls traffic-eng level-1',
            ' mpls traffic-eng router-id GigabitEthernet0/0/1',
            ' exit',
            'interface GigabitEthernet0/0/1',
            ' ip router isis core',
            ' exit',
            ]))
        self.assertMultiLineEqual(str(cfg1['PE2']), '\n'.join([
            'router isis core',
            ' net 00.0000.0000.0002.00',
            ' metric-style narrow',
            ' mpls traffic-eng level-2',
            ' mpls traffic-eng router-id GigabitEthernet0/0/2',
            ' exit',
            'interface GigabitEthernet0/0/2',
            ' ip router isis core',
            ' exit',
            ]))

        isis.address_families = set([AddressFamily.ipv4_unicast, AddressFamily.ipv6_unicast])
        isis.device_attr['PE1'].address_family_attr['ipv6 unicast'].metric_style = "wide"
        isis.device_attr['PE2'].address_family_attr['ipv6 unicast'].metric_style = "narrow"

        cfg2 = isis.build_config(apply=False)

        self.assertMultiLineEqual(str(cfg2['PE1']), '\n'.join([
            'router isis core',
            ' net 00.0000.0000.0001.00',
            ' metric-style wide',
            ' mpls traffic-eng level-1',
            ' mpls traffic-eng router-id GigabitEthernet0/0/1',
            ' address-family ipv6 unicast',
            '  metric-style wide',
            '  exit',
            ' exit',
            'interface GigabitEthernet0/0/1',
            ' ip router isis core',
            ' ipv6 router isis core',
            ' exit',
            ]))

        self.assertMultiLineEqual(str(cfg2['PE2']), '\n'.join([
            'router isis core',
            ' net 00.0000.0000.0002.00',
            ' metric-style narrow',
            ' mpls traffic-eng level-2',
            ' mpls traffic-eng router-id GigabitEthernet0/0/2',
            ' address-family ipv6 unicast',
            '  metric-style narrow',
            '  exit',
            ' exit',
            'interface GigabitEthernet0/0/2',
            ' ip router isis core',
            ' ipv6 router isis core',
            ' exit',
            ]))

        uncfg2 = isis.build_unconfig(apply=False)
        self.assertMultiLineEqual(str(uncfg2['PE1']), '\n'.join([
            'no router isis core',
            'interface GigabitEthernet0/0/1',
            ' no ip router isis core',
            ' no ipv6 router isis core',
            ' exit',
            ]))

        self.assertMultiLineEqual(str(uncfg2['PE2']), '\n'.join([
            'no router isis core',
            'interface GigabitEthernet0/0/2',
            ' no ip router isis core',
            ' no ipv6 router isis core',
            ' exit',
            ]))

        partial_uncfg2 = isis.build_unconfig(apply=False,attributes='device_attr__*__address_family_attr__*')

        self.assertMultiLineEqual(str(partial_uncfg2['PE1']), '\n'.join([
            'router isis core',
            ' no metric-style wide',
            ' no mpls traffic-eng level-1',
            ' no mpls traffic-eng router-id GigabitEthernet0/0/1',
            ' no address-family ipv4 unicast',
            ' no address-family ipv6 unicast',
            ' exit',
            ]))

        self.assertMultiLineEqual(str(partial_uncfg2['PE2']), '\n'.join([
            'router isis core',
            ' no metric-style narrow',
            ' no mpls traffic-eng level-2',
            ' no mpls traffic-eng router-id GigabitEthernet0/0/2',
            ' no address-family ipv4 unicast',
            ' no address-family ipv6 unicast',
            ' exit',
            ]))

        partial_cfg21 = isis.build_config(apply=False,attributes='device_attr__PE1__address_family_attr__ipv4 unicast__metric_style')
        self.assertMultiLineEqual(str(partial_cfg21['PE1']), '\n'.join([
            'router isis core',
            ' metric-style wide',
            ' exit',
            ]))


        partial_uncfg21 = isis.build_unconfig(apply=False,attributes='device_attr__PE1__address_family_attr__ipv4 unicast__metric_style')
        self.assertMultiLineEqual(str(partial_uncfg21['PE1']), '\n'.join([
            'router isis core',
            ' no metric-style wide',
            ' exit',
            ]))

        partial_cfg22 = isis.build_config(apply=False,attributes='device_attr__PE1__address_family_attr__ipv6 unicast__metric_style')
        self.assertMultiLineEqual(str(partial_cfg22['PE1']), '\n'.join([
            'router isis core',
            ' address-family ipv6 unicast',
            '  metric-style wide',
            '  exit',
            ' exit',
            ]))

        partial_uncfg22 = isis.build_unconfig(apply=False,attributes='device_attr__PE1__address_family_attr__ipv6 unicast__metric_style')
        self.assertMultiLineEqual(str(partial_uncfg22['PE1']), '\n'.join([
            'router isis core',
            ' address-family ipv6 unicast',
            '  no metric-style wide',
            '  exit',
            ' exit',
            ]))

    def test_IsisPerInterface(self):

        isis = Isis("core")
        self.link.add_feature(isis)
        for intf_iter in self.link.interfaces:
            intf_iter.add_feature(isis)

        val = 1
        isis.device_attr['PE1'].net_id = "00.0000.0000.000{}.00".format(val)
        val += 1
        isis.device_attr['PE2'].net_id = "00.0000.0000.000{}.00".format(val)

        # per interface ISIS
        isis.device_attr['PE1'].interface_attr[self.intf1].passive = True
        isis.device_attr['PE1'].interface_attr[self.intf1].metric = 20
        isis.device_attr['PE2'].interface_attr[self.intf2].point_to_point = True

        cfg1 = isis.build_config(apply=False)

        self.assertMultiLineEqual(str(cfg1['PE1']), '\n'.join([
            'router isis core',
            ' net 00.0000.0000.0001.00',
            ' passive-interface GigabitEthernet0/0/1',
            ' exit',
            'interface GigabitEthernet0/0/1',
            ' ip router isis core',
            ' isis metric 20',
            ' exit',
            ]))
        self.assertMultiLineEqual(str(cfg1['PE2']), '\n'.join([
            'router isis core',
            ' net 00.0000.0000.0002.00',
            ' exit',
            'interface GigabitEthernet0/0/2',
            ' ip router isis core',
            ' isis network point-to-point',
            ' exit',
            ]))

        isis.address_families = set([AddressFamily.ipv4_unicast, AddressFamily.ipv6_unicast])

        cfg2 = isis.build_config(apply=False)

        self.assertMultiLineEqual(str(cfg2['PE1']), '\n'.join([
            'router isis core',
            ' net 00.0000.0000.0001.00',
            ' passive-interface GigabitEthernet0/0/1',
            ' exit',
            'interface GigabitEthernet0/0/1',
            ' ip router isis core',
            ' ipv6 router isis core',
            ' isis metric 20',
            ' exit',
            ]))
        self.assertMultiLineEqual(str(cfg2['PE2']), '\n'.join([
            'router isis core',
            ' net 00.0000.0000.0002.00',
            ' exit',
            'interface GigabitEthernet0/0/2',
            ' ip router isis core',
            ' ipv6 router isis core',
            ' isis network point-to-point',
            ' exit',
            ]))

        partial_cfg21 = isis.build_config(apply=False,attributes='device_attr__*__interface_attr__*__metric')
        self.assertMultiLineEqual(str(partial_cfg21['PE1']), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' isis metric 20',
            ' exit',
            ]))

        partial_cfg22 = isis.build_config(apply=False,attributes='device_attr__*__interface_attr__*__address_family_attr__ipv6 unicast')
        self.assertMultiLineEqual(str(partial_cfg22['PE1']), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' ipv6 router isis core',
            ' exit',
            ]))

if __name__ == '__main__':
    unittest.main()

