# python
import unittest
from unittest.mock import Mock

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# Genie XBu_shared
from genie.libs.conf.vlan import Vlan
from genie.libs.conf.interface import Layer, L2_type

class test_vlan(TestCase):
    def test_init(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        dev2 = Device(testbed=testbed, name='PE2', os='nxos')
        intf1 = Interface(name='Ethernet0/0/1', device=dev1)
        intf2 = Interface(name='Ethernet0/0/2', device=dev2)
        link = Link(name='1_2_1', testbed=testbed)
        link.connect_interface(interface=intf1)
        link.connect_interface(interface=intf2)
        self.assertSetEqual(
            set(link.find_interfaces()),
            set([intf1, intf2]))
        self.assertSetEqual(
            set(dev1.find_interfaces()),
            set([intf1]))
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
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        dev2 = Device(testbed=testbed, name='PE2', os='nxos')
        intf1 = Interface(name='Ethernet0/0/1', device=dev1, layer=Layer.L3)
        intf2 = Interface(name='Ethernet0/0/2', device=dev2, layer=Layer.L2)
        link = Link(name='1_2_1', testbed=testbed)
        link.connect_interface(interface=intf1)
        link.connect_interface(interface=intf2)
        vlan = Vlan()
        link.add_feature(vlan)
        vlan.vlan_id = 100
        access_map_id = 'ed'
        vlan_configuration_id = '3'

        vlan.device_attr[dev1]
        vlan.device_attr[dev2]
        vlan.device_attr[dev1].interface_attr[intf1]
        vlan.device_attr[dev2].interface_attr[intf2]
        vlan.device_attr[dev2].interface_attr[intf2].switchport_mode = \
            L2_type.TRUNK
        vlan.device_attr[dev2].interface_attr[intf2].sw_trunk_allowed_vlan = \
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
        vlan.egress_load_balance = True
        vlan.device_attr[dev1].access_map_action = 'drop'
        vlan.datalink_flow_monitor = True

        intf1.ipv4 = '201.0.12.1'
        intf1.ipv4.netmask = '255.255.255.0'
        intf1.speed = 1000
        intf1.mtu = 500
        intf1.ipv6 = '2001::12:1'

        cfg1 = vlan.build_config(apply=False)
        cfg2 = intf1.build_config(apply=False)
        self.assertCountEqual(cfg1.keys(), ['PE1', 'PE2'])

        self.assertMultiLineEqual(
            str(cfg1['PE1']),
            '\n'.join([
                'vlan 100',
                ' media enet',
                ' no shutdown',
                ' exit',
                'vlan access-map ed',
                ' action drop',
                ' exit',
                'vlan configuration 3',
                ' egress port-channel load-balance random',
                ' exit',
                'interface Ethernet0/0/1',
                ' mtu 500',
                ' ip address 201.0.12.1 255.255.255.0',
                ' ipv6 address 2001::12:1/128',
                ' speed 1000',
                ' exit',
            ]))

        self.assertMultiLineEqual(
            str(cfg1['PE2']),
            '\n'.join([
                'vlan 100',
                ' media enet',
                ' no shutdown',
                ' exit',
                'vlan access-map ed',
                ' exit',
                'vlan configuration 3',
                ' egress port-channel load-balance random',
                ' exit',
                'interface Ethernet0/0/2',
                ' switchport mode trunk',
                ' switchport trunk allowed vlan 200-201',
                ' exit',
            ]))

        self.assertMultiLineEqual(
            str(cfg2),
            '\n'.join([
                'interface Ethernet0/0/1',
                ' mtu 500',
                ' ip address 201.0.12.1 255.255.255.0',
                ' ipv6 address 2001::12:1/128',
                ' speed 1000',
                ' exit',
            ]))

    def test_basic_uncfg(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        dev2 = Device(testbed=testbed, name='PE2', os='nxos')
        intf1 = Interface(name='Ethernet0/0/1', device=dev1, layer=Layer.L3)
        intf2 = Interface(name='Ethernet0/0/2', device=dev2, layer=Layer.L2)
        link = Link(name='1_2_1', testbed=testbed)
        link.connect_interface(interface=intf1)
        link.connect_interface(interface=intf2)
        vlan = Vlan()
        link.add_feature(vlan)
        vlan.vlan_id = 100
        access_map_id = 'ed'
        vlan_configuration_id = '3'

        vlan.device_attr[dev1]
        vlan.device_attr[dev2]
        vlan.device_attr[dev1].access_map_attr[access_map_id]
        vlan.device_attr[dev2].access_map_attr[access_map_id]
        vlan.device_attr[dev1].interface_attr[intf1]
        vlan.device_attr[dev2].interface_attr[intf2]
        vlan.device_attr[dev2].interface_attr[intf2].switchport_mode = \
            L2_type.TRUNK
        vlan.device_attr[dev2].interface_attr[intf2].sw_trunk_allowed_vlan = \
            '200-201'
        vlan.device_attr[dev1].vlan_configuration_attr[vlan_configuration_id]
        vlan.device_attr[dev2].vlan_configuration_attr[vlan_configuration_id]

        # Defining attributes section
        vlan.shutdown = False
        with self.assertRaises(ValueError):
            vlan.media = 'invalid'
        vlan.media = 'enet'
        self.assertIs(type(vlan.media), Vlan.Media)
        vlan.egress_port_channel_load_balance_random = True
        vlan.device_attr[dev1].access_map_action = 'drop'
        vlan.datalink_flow_monitor = True

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

        uncfg1 = vlan.build_unconfig(apply=False)
        self.assertCountEqual(uncfg1.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(
            str(uncfg1['PE1']),
            '\n'.join([
                'no vlan 100',
                'no vlan access-map ed',
                'no vlan configuration 3',
            ]))

        self.assertMultiLineEqual(
            str(uncfg1['PE2']),
            '\n'.join([
                'no vlan 100',
                'no vlan access-map ed',
                'no vlan configuration 3',
                'interface Ethernet0/0/2',
                ' no switchport mode trunk',
                ' no switchport trunk allowed vlan 200-201',
                ' exit',
            ]))

        partial_uncfg1 = vlan.build_unconfig(apply=False,
                                             attributes={'device_attr': \
                                                             {'*': "media"}})
        self.assertCountEqual(partial_uncfg1.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(
            str(partial_uncfg1['PE1']),
            '\n'.join([
                'vlan 100',
                ' no media enet',
                ' exit',
            ]))

        partial_unconfigure = vlan.build_unconfig(apply=False,
                                                  attributes={'device_attr': \
                                                                  {'*': {'access_map_attr': \
                                                                             {'*': "access_map_action"}}}})
        self.assertCountEqual(partial_unconfigure.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(
            str(partial_unconfigure['PE1']),
            '\n'.join([
                'vlan access-map ed',
                ' no action drop',
                ' exit',
            ]))

        all_vlan_interface_uncfg = vlan.build_unconfig(apply=False,
                                                       attributes={ \
                                                           'device_attr': {'*': { \
                                                               'interface_attr': '*'}}})
        self.assertCountEqual(all_vlan_interface_uncfg.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(
            str(all_vlan_interface_uncfg['PE2']),
            '\n'.join([
                'interface Ethernet0/0/2',
                ' no switchport mode trunk',
                ' no switchport trunk allowed vlan 200-201',
                ' exit',
            ]))

        partial_vlan_interface_uncfg = vlan.build_unconfig(apply=False,
                                                           attributes={ \
                                                               'device_attr': {'*': \
                                                                                   {'interface_attr': \
                                                                                        {
                                                                                            '*': "sw_trunk_allowed_vlan"}}}})
        self.assertCountEqual(partial_vlan_interface_uncfg.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(
            str(partial_vlan_interface_uncfg['PE2']),
            '\n'.join([
                'interface Ethernet0/0/2',
                ' no switchport trunk allowed vlan 200-201',
                ' exit',
            ]))

    def test_cfg_with_args(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        dev2 = Device(testbed=testbed, name='PE2', os='nxos')
        intf1 = Interface(name='Ethernet0/0/1', device=dev1, layer=Layer.L3)
        intf2 = Interface(name='Ethernet0/0/2', device=dev2, layer=Layer.L2)
        link = Link(name='1_2_1', testbed=testbed)
        link.connect_interface(interface=intf1)
        link.connect_interface(interface=intf2)
        vlan = Vlan(vlan_id=100)
        link.add_feature(vlan)

        access_map_id = 'ed'
        vlan_configuration_id = '3'

        vlan.device_attr[dev1]
        vlan.device_attr[dev2]
        vlan.device_attr[dev1].interface_attr[intf1]
        vlan.device_attr[dev2].interface_attr[intf2]
        vlan.device_attr[dev2].interface_attr[intf2].switchport_mode = \
            L2_type.TRUNK
        vlan.device_attr[dev2].interface_attr[intf2].sw_trunk_allowed_vlan = \
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
        vlan.egress_load_balance = True
        vlan.device_attr[dev1].access_map_action = 'drop'
        vlan.datalink_flow_monitor = True

        intf1.ipv4 = '201.0.12.1'
        intf1.ipv4.netmask = '255.255.255.0'
        intf1.speed = 1000
        intf1.mtu = 500
        intf1.ipv6 = '2001::12:1'

        cfg1 = vlan.build_config(apply=False)
        cfg2 = intf1.build_config(apply=False)
        self.assertCountEqual(cfg1.keys(), ['PE1', 'PE2'])

        self.assertMultiLineEqual(
            str(cfg1['PE1']),
            '\n'.join([
                'vlan 100',
                ' media enet',
                ' no shutdown',
                ' exit',
                'vlan access-map ed',
                ' action drop',
                ' exit',
                'vlan configuration 3',
                ' egress port-channel load-balance random',
                ' exit',
                'interface Ethernet0/0/1',
                ' mtu 500',
                ' ip address 201.0.12.1 255.255.255.0',
                ' ipv6 address 2001::12:1/128',
                ' speed 1000',
                ' exit',
            ]))

        self.assertMultiLineEqual(
            str(cfg1['PE2']),
            '\n'.join([
                'vlan 100',
                ' media enet',
                ' no shutdown',
                ' exit',
                'vlan access-map ed',
                ' exit',
                'vlan configuration 3',
                ' egress port-channel load-balance random',
                ' exit',
                'interface Ethernet0/0/2',
                ' switchport mode trunk',
                ' switchport trunk allowed vlan 200-201',
                ' exit',
            ]))

        self.assertMultiLineEqual(
            str(cfg2),
            '\n'.join([
                'interface Ethernet0/0/1',
                ' mtu 500',
                ' ip address 201.0.12.1 255.255.255.0',
                ' ipv6 address 2001::12:1/128',
                ' speed 1000',
                ' exit',
            ]))

        uncfg = vlan.build_unconfig(apply=False, attributes={'device_attr': {
                                                        dev1: {
                                                            'shutdown': None}
                                                            }})
        self.assertMultiLineEqual(
            str(uncfg['PE1']),
            '\n'.join([
                'vlan 100',
                ' shutdown',
                ' exit',
            ]))

    def test_new_vlan_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='N95', os='nxos')

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

    def test_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        with self.assertNoWarnings():
            Genie.testbed = None
            with self.assertRaises(TypeError):
                vlan = Vlan()
            Genie.testbed = testbed

            vlan = Vlan(vlan='102')
            vlan.device_attr[dev1].vlan_attr['102'].name = 'vlan2'
            vlan.device_attr[dev1].vlan_attr['102'].state = 'active'
            vlan.device_attr[dev1].vlan_attr['102'].mode = 'ce'

            self.assertIs(vlan.testbed, testbed)

            dev1.add_feature(vlan)

            cfgs = vlan.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                'vlan 102',
                ' name vlan2',
                ' state active',
                ' mode ce',
                ' exit',
            ]))

    def test_uncfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        with self.assertNoWarnings():
            Genie.testbed = None
            with self.assertRaises(TypeError):
                vlan = Vlan()
            Genie.testbed = testbed

            vlan = Vlan(vlan='102')
            vlan.device_attr[dev1].vlan_attr['102'].name = 'vlan2'
            vlan.device_attr[dev1].vlan_attr['102'].state = 'active'
            vlan.device_attr[dev1].vlan_attr['102'].mode = 'ce'

            self.assertIs(vlan.testbed, testbed)

            dev1.add_feature(vlan)

            cfgs = vlan.build_unconfig(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                'no vlan 102',
            ]))

    def test_cfg_with_igmp(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        with self.assertNoWarnings():
            Genie.testbed = None
            with self.assertRaises(TypeError):
                vlan = Vlan()
            Genie.testbed = testbed

            vlan = Vlan(vlan='102')
            vlan.device_attr[dev1].vlan_attr['102'].name = 'vlan2'
            vlan.device_attr[dev1].vlan_attr['102'].state = 'active'
            vlan.device_attr[dev1].vlan_attr['102'].mode = 'ce'

            vlan.device_attr[dev1].config_vlan_attr['102'].config_vlan_id = '102'
            vlan.device_attr[dev1].config_vlan_attr['102'].ip_igmp_snooping = True

            self.assertIs(vlan.testbed, testbed)

            dev1.add_feature(vlan)

            cfgs = vlan.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                'vlan 102',
                ' name vlan2',
                ' state active',
                ' mode ce',
                ' exit',
                'vlan configuration 102',
                ' ip igmp snooping',
                ' exit'
            ]))

            un_cfgs = vlan.build_unconfig(apply=False)
            self.assertMultiLineEqual(str(un_cfgs[dev1.name]), '\n'.join([
                'no vlan 102',
                'no vlan configuration 102',
            ]))

            un_cfgs = vlan.build_unconfig(apply=False,
                                          attributes={'device_attr': {
                                                        dev1: {
                                                            'vlan_attr': {
                                                                '102': {"mode": None}
                                                            },
                                                            'config_vlan_attr': {
                                                                '102': {"ip_igmp_snooping": None}
                                                            }
                                                        }
                                                    }
                                                })
            self.assertCountEqual(un_cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(un_cfgs[dev1.name]), '\n'.join([
                'vlan 102',
                ' no mode ce',
                ' exit',
                'vlan configuration 102',
                ' no ip igmp snooping',
                ' exit',
            ]))

    def test_cfg_without_igmp(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        with self.assertNoWarnings():
            Genie.testbed = None
            with self.assertRaises(TypeError):
                vlan = Vlan()
            Genie.testbed = testbed

            vlan = Vlan(vlan='102')
            vlan.device_attr[dev1].vlan_attr['102'].name = 'vlan2'
            vlan.device_attr[dev1].vlan_attr['102'].state = 'active'
            vlan.device_attr[dev1].vlan_attr['102'].mode = 'ce'

            vlan.device_attr[dev1].config_vlan_attr['102'].config_vlan_id = '102'

            self.assertIs(vlan.testbed, testbed)

            dev1.add_feature(vlan)

            cfgs = vlan.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                'vlan 102',
                ' name vlan2',
                ' state active',
                ' mode ce',
                ' exit',
                'vlan configuration 102',
                ' exit',
            ]))

    def test_enable_disable(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        # Create Vlan object
        vlan1 = Vlan()
        dev1.add_feature(vlan1)
        vlan1.device_attr[dev1].enabled = True

        # Check config strings built correctly
        cfgs = vlan1.build_config(apply=False)
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'feature interface-vlan',
                'feature vn-segment-vlan-based',
            ]))

        # Unconfigure
        uncfgs = vlan1.build_unconfig(apply=False)
        self.assertMultiLineEqual(
            str(uncfgs[dev1.name]),
            '\n'.join([
                'no feature interface-vlan',
                'no feature vn-segment-vlan-based',
            ]))

        dev1.remove_feature(vlan1)

        # Create Vlan object
        vlan2 = Vlan()
        dev1.add_feature(vlan2)
        vlan2.device_attr[dev1].enabled_interface_vlan = True

        # Check config strings built correctly
        cfgs = vlan2.build_config(apply=False)
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'feature interface-vlan',
            ]))

        # Unconfigure
        uncfgs = vlan2.build_unconfig(apply=False)
        self.assertMultiLineEqual(
            str(uncfgs[dev1.name]),
            '\n'.join([
                'no feature interface-vlan',
            ]))

        # Remove feature
        dev1.remove_feature(vlan2)

        # Create Vlan object
        vlan3 = Vlan()
        dev1.add_feature(vlan3)
        vlan3.device_attr[dev1].enabled_vn_segment_vlan_based = True

        # Build config
        cfgs = vlan3.build_config(apply=False)
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'feature vn-segment-vlan-based',
            ]))

        # Unconfigure
        uncfgs = vlan3.build_unconfig(apply=False)
        self.assertMultiLineEqual(
            str(uncfgs[dev1.name]),
            '\n'.join([
                'no feature vn-segment-vlan-based',
            ]))

if __name__ == '__main__':
    unittest.main()