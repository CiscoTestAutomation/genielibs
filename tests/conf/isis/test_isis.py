#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.isis import Isis


class test_isis(unittest.TestCase):

    def setUp(self):

        testbed = Genie.testbed = Testbed()
        self.dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        self.dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        self.intf1 = Interface(name='GigabitEthernet0/0/0/1',device=self.dev1)
        self.intf2 = Interface(name='GigabitEthernet0/0/0/2',device=self.dev2)

        self.link = Link(name='1_2_1',testbed=testbed)
        self.link.connect_interface(interface=self.intf1)
        self.link.connect_interface(interface=self.intf2)

    def test_init(self):

        isis = Isis("core")
        self.assertCountEqual(isis.devices, [])
        self.assertCountEqual(isis.interfaces, [])
        self.assertCountEqual(isis.links, [])

        self.link.add_feature(isis)
        for intf_iter in self.link.interfaces:
            intf_iter.add_feature(isis)
        self.assertCountEqual(isis._devices_with_feature(), [self.dev1, self.dev2])
        self.assertCountEqual(isis._interfaces_with_feature(), [self.intf1, self.intf2])
        self.assertCountEqual(isis._links_with_feature(), [self.link])
        self.assertCountEqual(isis.devices, [self.dev1, self.dev2])
        self.assertCountEqual(isis.interfaces, [self.intf1, self.intf2])
        self.assertCountEqual(isis.links, [self.link])

    def test_IsisGlobal(self):

        isis = Isis("core")
        self.link.add_feature(isis)

        self.assertCountEqual(isis.devices, [self.dev1, self.dev2])
        self.assertCountEqual(isis.interfaces, [self.intf1, self.intf2])
        self.assertCountEqual(isis.links, [self.link])

        # Global ISIS config
        isis.nsr = True
        isis.nsf_lifetime = 5

        # override default for both devices
        isis.is_type = Isis.IsType.level_1
        isis.device_attr['PE1'].is_type = Isis.IsType.level_1_2
        isis.device_attr['PE2'].is_type = Isis.IsType.level_2

        # use no default
        isis.device_attr['PE1'].nsf = Isis.Nsf.ietf
        isis.device_attr['PE2'].nsf = Isis.Nsf.cisco

        # override default for one device
        isis.lsp_mtu = 1400
        isis.device_attr['PE1'].lsp_mtu = 1500
        val = 1
        isis.device_attr['PE1'].net_id = "00.0000.0000.000{}.00".format(val)
        val += 1
        isis.device_attr['PE2'].net_id = "00.0000.0000.000{}.00".format(val)

        cfg1 = isis.build_config(apply=False)
        #print("\nPE1 config\n" + str(cfg1['PE1']))
        #print("\nPE2 config\n" + str(cfg1['PE2']))

        self.assertCountEqual(cfg1.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(str(cfg1['PE1']), '\n'.join([
            'router isis core',
            ' is-type level-1-2',
            ' lsp-mtu 1500',
            ' net 00.0000.0000.0001.00',
            ' nsf ietf',
            ' nsf lifetime 5',
            ' nsr',
            ' address-family ipv4 unicast',
            '  exit',
            ' interface GigabitEthernet0/0/0/1',
            '  address-family ipv4 unicast',
            '   exit',
            '  exit',
            ' exit',
        ]))
        self.assertMultiLineEqual(str(cfg1['PE2']), '\n'.join([
            'router isis core',
            ' is-type level-2-only',
            ' lsp-mtu 1400',
            ' net 00.0000.0000.0002.00',
            ' nsf cisco',
            ' nsf lifetime 5',
            ' nsr',
            ' address-family ipv4 unicast',
            '  exit',
            ' interface GigabitEthernet0/0/0/2',
            '  address-family ipv4 unicast',
            '   exit',
            '  exit',
            ' exit',
            ]))

    def test_IsisPerAddrFamily(self):

        isis = Isis("core")
        self.link.add_feature(isis)

        # per address family ISIS
        isis.device_attr['PE1'].address_family_attr['ipv4 unicast'].metric_style = "wide"
        isis.device_attr['PE1'].address_family_attr['ipv4 unicast'].mpls_te_level = Isis.IsType.level_1
        isis.device_attr['PE1'].address_family_attr['ipv4 unicast'].mpls_te_rtrid = self.intf1
        isis.device_attr['PE1'].address_family_attr['ipv4 unicast'].redistribute_connected = True  

        isis.device_attr['PE2'].address_family_attr['ipv4 unicast'].metric_style = "narrow"
        isis.device_attr['PE2'].address_family_attr['ipv4 unicast'].mpls_te_level = Isis.IsType.level_2
        isis.device_attr['PE2'].address_family_attr['ipv4 unicast'].mpls_te_rtrid = self.intf2

        cfg1 = isis.build_config(apply=False)
        #print("\nPE1 config\n" + str(cfg1['PE1']))
        #print("\nPE2 config\n" + str(cfg1['PE2']))
        self.assertMultiLineEqual(str(cfg1['PE1']), '\n'.join([
            'router isis core',
            ' net 47.6B8D.854F.FFFF.4F2D.4CD8.00',
            ' address-family ipv4 unicast',
            '  metric-style wide',
            '  mpls traffic-eng level-1',
            '  mpls traffic-eng router-id GigabitEthernet0/0/0/1',
            '  redistribute connected',
            '  exit',
            ' interface GigabitEthernet0/0/0/1',
            '  address-family ipv4 unicast',
            '   exit',
            '  exit',
            ' exit',
            ]))
        self.assertMultiLineEqual(str(cfg1['PE2']), '\n'.join([
            'router isis core',
            ' net 47.6B8D.854F.FFFF.D624.1D62.00',
            ' address-family ipv4 unicast',
            '  metric-style narrow',
            '  mpls traffic-eng level-2-only',
            '  mpls traffic-eng router-id GigabitEthernet0/0/0/2',
            '  exit',
            ' interface GigabitEthernet0/0/0/2',
            '  address-family ipv4 unicast',
            '   exit',
            '  exit',
            ' exit',
            ]))

    def test_IsisPerInterface(self):

        isis = Isis("core")
        self.link.add_feature(isis)
        for intf_iter in self.link.interfaces:
            intf_iter.add_feature(isis)

        # per interface ISIS
        isis.device_attr['PE1'].interface_attr[self.intf1].passive = True
        isis.device_attr['PE1'].interface_attr[self.intf1].shutdown = True

        isis.device_attr['PE2'].interface_attr[self.intf2].point_to_point = True

        cfg1 = isis.build_config(apply=False)
        #print("\nPE1 config\n" + str(cfg1['PE1']))
        #print("\nPE2 config\n" + str(cfg1['PE2']))
        self.assertMultiLineEqual(str(cfg1['PE1']), '\n'.join([
            'router isis core',
            ' net 47.6B8D.854F.FFFF.4F2D.4CD8.00',
            ' address-family ipv4 unicast',
            '  exit',
            ' interface GigabitEthernet0/0/0/1',
            '  passive',
            '  shutdown',
            '  address-family ipv4 unicast',
            '   exit',
            '  exit',
            ' exit',
            ]))
        self.assertMultiLineEqual(str(cfg1['PE2']), '\n'.join([
            'router isis core',
            ' net 47.6B8D.854F.FFFF.D624.1D62.00',
            ' address-family ipv4 unicast',
            '  exit',
            ' interface GigabitEthernet0/0/0/2',
            '  point-to-point',
            '  address-family ipv4 unicast',
            '   exit',
            '  exit',
            ' exit',
            ]))

    def test_IsisPerInterfacePerAddressFamily(self):

        # No attributes defined yet
        if 0:
            # per interface per address family ISIS
            isis.device_attr['PE1'].interface_attr[self.intf1].address_family_attr['ipv4 unicast'].attr = "value"

            isis.device_attr['PE1'].interface_attr[self.intf1].address_family_attr['ipv4 unicast'].attr = "value"

            cfg1 = isis.build_config(apply=False)
            self.assertMultiLineEqual(str(cfg1['PE1']), '\n'.join([
                'router isis 100',
                ]))
            self.assertMultiLineEqual(str(cfg1['PE2']), '\n'.join([
                'router isis 100',
                ]))
                
    def test_NET(self):

        isis = Isis("core")

        self.assertEqual(isis.system_id, None)
        self.assertEqual(isis.device_attr[self.dev1].system_id, 'FFFF.4F2D.4CD8')  # "PE1"
        self.assertEqual(isis.device_attr[self.dev2].system_id, 'FFFF.D624.1D62')  # "PE2"
        isis.system_id = '0000.0000.0001'
        self.assertEqual(isis.device_attr[self.dev1].system_id, '0000.0000.0001')
        self.assertEqual(isis.device_attr[self.dev2].system_id, '0000.0000.0001')
        del isis.system_id
        self.assertEqual(isis.system_id, None)
        self.assertEqual(isis.device_attr[self.dev1].system_id, 'FFFF.4F2D.4CD8')  # "PE1"
        self.assertEqual(isis.device_attr[self.dev2].system_id, 'FFFF.D624.1D62')  # "PE2"

        self.assertEqual(isis.area_address, '47.6B8D.854F')  # "core"
        self.assertEqual(isis.device_attr[self.dev1].area_address, '47.6B8D.854F')  # "core"
        self.assertEqual(isis.device_attr[self.dev2].area_address, '47.6B8D.854F')  # "core"
        isis.area_address = '47.0000.0000'
        self.assertEqual(isis.area_address, '47.0000.0000')
        self.assertEqual(isis.device_attr[self.dev1].area_address, '47.0000.0000')
        self.assertEqual(isis.device_attr[self.dev2].area_address, '47.0000.0000')
        isis.area_address = None
        self.assertEqual(isis.area_address, None)
        self.assertEqual(isis.device_attr[self.dev1].area_address, '47.4F2D.4CD8')  # "PE1"
        self.assertEqual(isis.device_attr[self.dev2].area_address, '47.D624.1D62')  # "PE2"
        del isis.area_address
        self.assertEqual(isis.area_address, '47.6B8D.854F')  # "core"
        self.assertEqual(isis.device_attr[self.dev1].area_address, '47.6B8D.854F')  # "core"
        self.assertEqual(isis.device_attr[self.dev2].area_address, '47.6B8D.854F')  # "core"

        self.assertEqual(isis.device_attr[self.dev1].net_id, '47.6B8D.854F.FFFF.4F2D.4CD8.00')  # "core"."PE1".00
        self.assertEqual(isis.device_attr[self.dev2].net_id, '47.6B8D.854F.FFFF.D624.1D62.00')  # "core"."PE2".00

if __name__ == '__main__':
    unittest.main()

