#!/usr/bin/env python

#python
import unittest
from unittest.mock import Mock

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# Genie XBu_shared
from genie.libs.conf.vlan import Vlan
from genie.libs.conf.base import Routing, \
                                       IPv4Neighbor, \
                                       IPv4Address, \
                                       IPv6Address


class test_vlan(TestCase):

    def test_init(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe')
        intf1 = Interface(name='GigabitEthernet0/0/1',device=dev1)
        intf2 = Interface(name='GigabitEthernet0/0/2',device=dev2)
        intf3 = Interface(name='Vlan100',device=dev1)
        link = Link(name='1_2_1',testbed=testbed)
        link.connect_interface(interface=intf1)
        link.connect_interface(interface=intf2)
        self.assertSetEqual(
            set(link.find_interfaces()),
            set([intf1, intf2]))
        self.assertSetEqual(
            set(dev1.find_interfaces()),
            set([intf1, intf3]))
        self.assertSetEqual(
            set(dev2.find_interfaces()),
            set([intf2]))

        vlan = Vlan()

        self.assertSetEqual(set(vlan.devices), set([]))
        self.assertSetEqual(set(vlan.links), set([]))

        link.add_feature(vlan)
        self.assertCountEqual(vlan.devices, [dev1, dev2])
        self.assertSetEqual(set(vlan.links), set([link]))
        self.assertSetEqual(set(vlan.interfaces), set([intf1, intf2]))

        with self.assertRaises(AttributeError):
            vlan.access_map_id

        with self.assertRaises(AttributeError):
            vlan.vlan_configuration_id

    def test_basic_cfg(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe')
        intf1 = Interface(name='GigabitEthernet0/0/1',device=dev1)
        intf2 = Interface(name='GigabitEthernet0/0/2',device=dev2)
        intf3 = Interface(name='Vlan100',device=dev1)
        link = Link(name='1_2_1',testbed=testbed)
        link.connect_interface(interface=intf1)
        link.connect_interface(interface=intf2)
        vlan = Vlan()
        link.add_feature(vlan)
        vlan.vlan_id = 100
        access_map_id = 'ed'
        vlan_configuration_id = '3'

        vlan.device_attr[dev1]
        vlan.device_attr[dev2]
        vlan.device_attr[dev1].interface_attr[intf1].switchport_mode = \
            'trunk'
        vlan.device_attr[dev1].interface_attr[intf1].sw_trunk_allowed_vlan = \
            '200-201'
        vlan.device_attr[dev1].access_map_attr[access_map_id]
        vlan.device_attr[dev2].access_map_attr[access_map_id]
        vlan.device_attr[dev1].vlan_configuration_attr[vlan_configuration_id]
        vlan.device_attr[dev2].vlan_configuration_attr[vlan_configuration_id]

        # Defining attributes section
        vlan.shutdown = False
        with self.assertRaises(ValueError):
            vlan.media = 'invalid'
        vlan.media = 'enet'
        self.assertIs(type(vlan.media), Vlan.Media)
        vlan.accounting_type = 'input'
        vlan.device_attr[dev1].access_map_action = 'drop'
        vlan.datalink_flow_monitor = True
        vlan.private_vlan_type = 'association'
        vlan.private_vlan_association_action = 'add'
        vlan.private_vlan_association_ids = '201,205'

        cfg1 = vlan.build_config(apply=False)

        self.assertCountEqual(cfg1.keys(), ['PE1', 'PE2'])

        self.assertMultiLineEqual(
            str(cfg1['PE1']),
            '\n'.join([
                'vlan 100',
                ' media enet',
                ' no shutdown',
                ' private-vlan association add 201,205',
                ' exit',
                'vlan accounting input',
                'vlan access-map ed',
                ' action drop',
                ' exit',
                'vlan configuration 3',
                ' datalink flow monitor',
                ' exit',
                'interface GigabitEthernet0/0/1',
                ' switchport mode trunk',
                ' switchport trunk allowed vlan 200-201',
                ' exit',
            ]))

        self.assertMultiLineEqual(
            str(cfg1['PE2']),
            '\n'.join([
                'vlan 100',
                ' media enet',
                ' no shutdown',
                ' private-vlan association add 201,205',
                ' exit',
                'vlan accounting input',
                'vlan access-map ed',
                ' exit',
                'vlan configuration 3',
                ' datalink flow monitor',
                ' exit',
            ]))

    def test_basic_uncfg(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe')
        intf1 = Interface(name='GigabitEthernet0/0/1',device=dev1)
        intf1.switchport = True
        intf2 = Interface(name='GigabitEthernet0/0/2',device=dev2)
        intf3 = Interface(name='Vlan100',device=dev1)
        vlan = Vlan()
        vlan.device_attr[dev1].vlan_id = 100
        vlan.device_attr[dev2].vlan_id = 300
        access_map_id = 'ed'
        vlan_configuration_id = '3'
        vlan.device_attr[dev1]
        vlan.device_attr[dev2]
        vlan.device_attr[dev1].interface_attr[intf1].switchport_mode = \
            'trunk'
        vlan.device_attr[dev1].interface_attr[intf1].sw_trunk_allowed_vlan = \
            '200-201'

        vlan.device_attr[dev1].access_map_attr[access_map_id]
        vlan.device_attr[dev2].access_map_attr[access_map_id]
        vlan.device_attr[dev1].vlan_configuration_attr[vlan_configuration_id]
        vlan.device_attr[dev2].vlan_configuration_attr[vlan_configuration_id]

        # Defining attributes section
        with self.assertRaises(ValueError):
            vlan.media = 'invalid'
        vlan.media = 'enet'
        self.assertIs(type(vlan.media), Vlan.Media)
        vlan.accounting_type = 'input'
        vlan.device_attr[dev1].access_map_action = 'drop'

        # Unconfig testing
        # Set a mock
        dev1.configure = Mock()
        dev2.configure = Mock()
        dev1.add_feature(vlan)
        dev2.add_feature(vlan)
        # Mock config

        uncfg1 = vlan.build_unconfig(apply=False)
        self.assertCountEqual(uncfg1.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(
            str(uncfg1['PE1']),
            '\n'.join([
                'no vlan 100',
                'no vlan accounting input',
                'no vlan access-map ed',
                'no vlan configuration 3',
                'interface GigabitEthernet0/0/1',
                ' no switchport mode trunk',
                ' no switchport trunk allowed vlan 200-201',
                ' exit',
            ]))

        self.assertMultiLineEqual(
            str(uncfg1['PE2']),
            '\n'.join([
                'no vlan 300',
                'no vlan accounting input',
                'no vlan access-map ed',
                'no vlan configuration 3',
            ]))

        uncfg_intf = intf1.build_unconfig(apply=False, attributes="switchport")
        self.assertMultiLineEqual(
            str(uncfg_intf),
            '\n'.join([
                'interface GigabitEthernet0/0/1',
                ' no switchport',
                ' exit',
            ]))

        partial_uncfg1 = vlan.build_unconfig(apply=False,
                                             attributes={'device_attr':\
                                                        {'*':"media"}})
        self.assertCountEqual(partial_uncfg1.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(
            str(partial_uncfg1['PE1']),
            '\n'.join([
                'vlan 100',
                ' no media enet',
                ' exit',
            ]))

        partial_unconfigure = vlan.build_unconfig(apply=False,
                                                  attributes={'device_attr':\
                                                             {'*':{'access_map_attr':\
                                                             {'*':"access_map_action"}}}})
        self.assertCountEqual(partial_unconfigure.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(
            str(partial_unconfigure['PE1']),
            '\n'.join([
                'vlan access-map ed',
                ' no action drop',
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
                ' no switchport mode trunk',
                ' no switchport trunk allowed vlan 200-201',
                ' exit',
            ]))

        partial_vlan_interface_uncfg = vlan.build_unconfig(apply=False,
                                                           attributes={'device_attr':\
                                                           {'*':{'interface_attr':\
                                                           {'*':"sw_trunk_allowed_vlan"}}}})
        self.assertCountEqual(partial_vlan_interface_uncfg.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(
            str(partial_vlan_interface_uncfg['PE1']),
            '\n'.join([
                'interface GigabitEthernet0/0/1',
                ' no switchport trunk allowed vlan 200-201',
                ' exit',
            ]))

    def test_new_vlan_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        with self.assertNoWarnings():
            Genie.testbed = None
            with self.assertRaises(TypeError):
                vlan = Vlan()
            Genie.testbed = testbed

            vlan = Vlan(vlan='100')
            vlan.device_attr[dev1].vlan_attr['100'].name = 'new_vlan'
            vlan.device_attr[dev1].vlan_attr['100'].state = 'active'

            self.assertIs(vlan.testbed, testbed)

            dev1.add_feature(vlan)

            cfgs = vlan.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                'vlan 100',
                ' name new_vlan',
                ' state active',
                ' exit',
            ]))

    def test_new_vlan_uncfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        with self.assertNoWarnings():
            vlan = Vlan(vlan='100')
            vlan.device_attr[dev1].vlan_attr['100']

            self.assertIs(vlan.testbed, testbed)

            dev1.add_feature(vlan)

            uncfgs = vlan.build_unconfig(apply=False)
            self.assertCountEqual(uncfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(uncfgs[dev1.name]), '\n'.join([
                'no vlan 100',
            ]))

    def test_uncfg_new_vlan_name(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        with self.assertNoWarnings():
            vlan = Vlan(vlan='100')
            vlan.device_attr[dev1].vlan_attr['100'].name = "new_vlan"

            self.assertIs(vlan.testbed, testbed)

            dev1.add_feature(vlan)

            uncfgs = vlan.build_unconfig(apply=False, attributes={'device_attr': \
                                                                      {'*':
                                                                            {'vlan_attr': \
                                                                            {'*': "name"}}}})
            self.assertCountEqual(uncfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(uncfgs[dev1.name]), '\n'.join([
                'vlan 100',
                ' no name new_vlan',
                ' exit',
            ]))

    def test_new_vlan_unshut(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        with self.assertNoWarnings():
            vlan = Vlan(vlan='100')
            vlan.device_attr[dev1].vlan_attr['100']
            vlan.device_attr[dev1].vlan_attr['100'].shutdown = False
            self.assertIs(vlan.testbed, testbed)

            dev1.add_feature(vlan)

            partial_uncfg = vlan.build_config(apply=False)
            self.assertCountEqual(partial_uncfg.keys(), [dev1.name])
            self.assertMultiLineEqual(str(partial_uncfg[dev1.name]), '\n'.join([
                'vlan 100',
                ' no shutdown',
                ' exit',
            ]))

if __name__ == '__main__':
    unittest.main()
