#!/usr/bin/env python
#python
import unittest
from unittest.mock import Mock
import itertools

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# Genie XBu_shared 
from genie.libs.conf.vlan import Vlan


class test_vlan(TestCase):

    def test_vlan_interface_configuration(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        intf1 = Interface(name='GigabitEthernet0/0/1',device=dev1)
        intf2 = Interface(name='GigabitEthernet0/0/2',device=dev2)
        intf3 = Interface(name='GigabitEthernet0/0/3',device=dev1)
        link = Link(name='1_2_1',testbed=testbed)
        link.connect_interface(interface=intf1)
        link.connect_interface(interface=intf2)
        vlan = Vlan()
        link.add_feature(vlan)

        vlan.device_attr[dev1]
        vlan.device_attr[dev2]
        vlan.device_attr[dev1].interface_attr[intf1]
        vlan.device_attr[dev1].interface_attr[intf1].eth_encap_type1 = 'dot1q'
        vlan.device_attr[dev1].interface_attr[intf1].eth_encap_val1 = 2
        vlan.device_attr[dev1].interface_attr[intf1].eth_encap_type2 = 'second-dot1q'
        vlan.device_attr[dev1].interface_attr[intf1].eth_encap_val2 = 5

        cfg1 = vlan.build_config(apply=False)
        self.assertCountEqual(cfg1.keys(), ['PE1', 'PE2'])

        self.assertMultiLineEqual(
            str(cfg1['PE1']),
            '\n'.join([
                'interface GigabitEthernet0/0/1',
                ' encapsulation dot1q 2 second-dot1q 5',
                ' exit',
            ]))

    def test_basic_uncfg(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        intf1 = Interface(name='GigabitEthernet0/0/1',device=dev1)
        intf2 = Interface(name='GigabitEthernet0/0/2',device=dev2)
        intf3 = Interface(name='GigabitEthernet0/0/3',device=dev1)
        link = Link(name='1_2_1',testbed=testbed)
        link.connect_interface(interface=intf1)
        link.connect_interface(interface=intf2)
        vlan = Vlan()
        link.add_feature(vlan)

        # Defining attributes section
        vlan.device_attr[dev1]
        vlan.device_attr[dev2]
        vlan.device_attr[dev1].interface_attr[intf1]
        vlan.device_attr[dev1].interface_attr[intf1].eth_encap_type1 = 'dot1q'
        vlan.device_attr[dev1].interface_attr[intf1].eth_encap_val1 = 2
        vlan.device_attr[dev1].interface_attr[intf1].eth_encap_type2 = 'second-dot1q'
        vlan.device_attr[dev1].interface_attr[intf1].eth_encap_val2 = 5

        # Unconfig testing
        # Set a mock
        dev1.cli = Mock()
        dev1.configure = Mock()
        dev2.cli = Mock()
        dev2.configure = Mock()
        dev1.add_feature(vlan)
        dev2.add_feature(vlan)
        # Mock config

        output = vlan.build_config(apply=True)

        uncfg = vlan.build_unconfig(apply=False)
        self.assertMultiLineEqual(
            str(uncfg['PE1']),
            '\n'.join([
                'interface GigabitEthernet0/0/1',
                ' no encapsulation dot1q 2 second-dot1q 5',
                ' exit',
            ]))

        all_vlan_interface_uncfg = vlan.build_unconfig(apply=False, 
                                                       attributes={'device_attr':\
                                                       {'*':{'interface_attr':'*'}}})
        self.assertCountEqual(all_vlan_interface_uncfg.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(
            str(all_vlan_interface_uncfg['PE1']),
            '\n'.join([
                'interface GigabitEthernet0/0/1',
                ' no encapsulation dot1q 2 second-dot1q 5',
                ' exit',
            ]))

        partial_vlan_interface_uncfg = vlan.build_unconfig(apply=False, 
                                                           attributes={'device_attr':\
                                                           {'*':{'interface_attr':\
                                                           {'*':"eth_encap_type1"}}}})
        self.assertCountEqual(partial_vlan_interface_uncfg.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(
            str(partial_vlan_interface_uncfg['PE1']),
            '\n'.join([
                'interface GigabitEthernet0/0/1',
                ' no encapsulation dot1q 2 second-dot1q 5',
                ' exit',
            ]))

if __name__ == '__main__':
    unittest.main()
