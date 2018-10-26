#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import SubAttributes, SubAttributesDict, AttributesHelper, KeyedSubAttributes

from genie.libs.conf.base import Routing, IPv4Neighbor, IPv4Address, IPv6Address
from genie.libs.conf.address_family import AddressFamily, AddressFamilySubAttributes
from genie.libs.conf.base.neighbor import IPv4NeighborSubAttributes
from genie.libs.conf.ospf import Ospf
from genie.libs.conf.vrf import Vrf

try:
    from ydk.models.ned import ned
    from ydk.services import CodecService
    from ydk.providers import CodecServiceProvider
    from ydk.types import DELETE, Empty
    from ydk.services import CRUDService
except:
    pass


class NetconfConnectionInfo(object):
    def __init__(self):
        self.ip = str('1.1.1.1')
        self.port = 830
        self.username = 'admin'
        self.password = 'lab'

class test_vrf(unittest.TestCase):

    def test_init(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe', context='yang')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe', context='yang')
        intf1 = Interface(name='GigabitEthernet0/0/1',device=dev1)
        intf2 = Interface(name='GigabitEthernet0/0/2',device=dev2)
        link = Link(name='1_2_1',testbed=testbed)
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
        vrf = Vrf(name='test')

        self.assertSetEqual(set(vrf.devices), set([]))
        self.assertSetEqual(set(vrf.interfaces), set([]))
        intf1.vrf = vrf
        intf2.vrf = vrf
        dev1.add_feature(vrf)
        dev2.add_feature(vrf)

        self.assertCountEqual(vrf.devices, [dev1, dev2])
        self.assertSetEqual(set(vrf.interfaces), set([intf1, intf2]))

        with self.assertRaises(AttributeError):
            vrf.address_families = set([AddressFamily.ipv8_unicast])

    def test_basic_cfg(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe', context='yang')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe', context='yang')
        vrf = Vrf(name='test')
        vrf1 = Vrf(name='test1')
        vrf2 = Vrf(name='test2')

        for dev in testbed.devices:
            dev.connections=Mock()
            dev.connections={'netconf':NetconfConnectionInfo()}
            dev.add_feature(vrf2)

        dev1.add_feature(vrf)
        dev2.add_feature(vrf1)
        vrf.address_families = set([AddressFamily.ipv4_unicast])
        vrf1.address_families = set([AddressFamily.ipv6_unicast])
        vrf2.address_families = set([AddressFamily.ipv4_unicast,
                                        AddressFamily.ipv6_unicast])

        cfg1 = vrf.build_config(apply=False)
        cfg2 = vrf1.build_config(apply=False)
        cfg3 = vrf2.build_config(apply=False, devices=['PE1'])
        cfg4 = vrf2.build_config(apply=False)
        self.assertCountEqual(cfg1.keys(), ['PE1'])
        self.assertCountEqual(cfg2.keys(), ['PE2'])
        self.assertCountEqual(cfg3.keys(), ['PE1'])
        self.assertCountEqual(cfg4.keys(), ['PE1','PE2'])
        self.assertMultiLineEqual(cfg1['PE1'], '\n'.join(['<vrf xmlns="http://cisco.com/ns/yang/ned/ios">\n'
'  <definition>\n'
'    <name>test</name>\n'
'    <address-family>\n'
'      <ipv4/>\n'
'    </address-family>\n'
'  </definition>\n'
'</vrf>\n']))
        self.assertMultiLineEqual(cfg2['PE2'], '\n'.join(['<vrf xmlns="http://cisco.com/ns/yang/ned/ios">\n'
'  <definition>\n'
'    <name>test1</name>\n'
'    <address-family>\n'
'      <ipv6/>\n'
'    </address-family>\n'
'  </definition>\n'
'</vrf>\n']))

        self.assertMultiLineEqual(cfg3['PE1'], '\n'.join(['<vrf xmlns="http://cisco.com/ns/yang/ned/ios">\n'
'  <definition>\n'
'    <name>test2</name>\n'
'    <address-family>\n'
'      <ipv4/>\n'
'      <ipv6/>\n'
'    </address-family>\n'
'  </definition>\n'
'</vrf>\n']))

        self.assertMultiLineEqual(cfg4['PE1'], '\n'.join(['<vrf xmlns="http://cisco.com/ns/yang/ned/ios">\n'
'  <definition>\n'
'    <name>test2</name>\n'
'    <address-family>\n'
'      <ipv4/>\n'
'      <ipv6/>\n'
'    </address-family>\n'
'  </definition>\n'
'</vrf>\n']))
        self.assertMultiLineEqual(cfg4['PE2'], '\n'.join(['<vrf xmlns="http://cisco.com/ns/yang/ned/ios">\n'
'  <definition>\n'
'    <name>test2</name>\n'
'    <address-family>\n'
'      <ipv4/>\n'
'      <ipv6/>\n'
'    </address-family>\n'
'  </definition>\n'
'</vrf>\n']))
        # uncfg1 = ospf.build_unconfig(apply=False)
        # self.assertCountEqual(uncfg1.keys(), ['PE1', 'PE2'])
        # self.assertMultiLineEqual(uncfg1['PE1'], '\n'.join([
        # 'no router ospf 100\n'
        # 'interface GigabitEthernet0/0/1\n'
        # ' no ip ospf 100 area 0\n'
        # ' exit'        ]))
        #
        # self.assertMultiLineEqual(uncfg1['PE2'], '\n'.join([
        # 'no router ospf 100\n'
        # 'interface GigabitEthernet0/0/2\n'
        # ' no ip ospf 100 area 0\n'
        # ' exit']))
#
#     def test_cfg_vrfs_areas_interfaces(self):
#         testbed = Genie.testbed = Testbed()
#         dev1 = Device(testbed=testbed, name='PE1', os='iosxe', context='yang')
#         dev2 = Device(testbed=testbed, name='PE2', os='iosxe', context='yang')
#         intf1 = Interface(name='GigabitEthernet0/0/1',device=dev1)
#         intf2 = Interface(name='GigabitEthernet0/0/2',device=dev2)
#         intf1_1 = Interface(name='GigabitEthernet0/1/1',device=dev1)
#         intf2_1 = Interface(name='GigabitEthernet0/1/2',device=dev2)
#         link = Link(name='1_2_1',testbed=testbed)
#         link.connect_interface(interface=intf1)
#         link.connect_interface(interface=intf2)
#         link1 = Link(name='2_2_2',testbed=testbed)
#         link1.connect_interface(interface=intf1_1)
#         link1.connect_interface(interface=intf2_1)
#         ospf = Ospf()
#         vrf = Vrf(name='test')
#         ospf.add_force_vrf(vrf)
#         link.add_feature(ospf)
#         link1.add_feature(ospf)
#         intf1.vrf = vrf
#         intf2.vrf = vrf
#         intf1_1.vrf = vrf
#         intf2_1.vrf = vrf
#         ospf.ospf_name = '100'
#         area_id = 0
#         area_id_1 = 1
#         ospf.device_attr[dev1].vrf_attr[vrf].area_attr[area_id]
#         ospf.device_attr[dev2].vrf_attr[vrf].area_attr[area_id]
#         ospf.device_attr[dev1].vrf_attr[vrf].instance_router_id = IPv4Address('2.1.1.1')
#         ospf.device_attr[dev2].vrf_attr[vrf].instance_router_id = IPv4Address('2.1.2.1')
#
#         ospf.device_attr[dev1].vrf_attr[vrf].area_attr[area_id].interface_attr[intf1].area_interface_cost = 10
#         ospf.device_attr[dev2].vrf_attr[vrf].area_attr[area_id].interface_attr[intf2].area_interface_cost = 10
#         ospf.device_attr[dev1].vrf_attr[vrf].area_attr[area_id_1].interface_attr[intf1_1].area_interface_cost = 20
#         ospf.device_attr[dev2].vrf_attr[vrf].area_attr[area_id_1].interface_attr[intf2_1].area_interface_cost = 20
#
#         ospf.nsr = True
#         ospf.auto_cost_ref_bw = 12345
#         cfg1 = ospf.build_config(apply=False)
#         self.assertCountEqual(cfg1.keys(), ['PE1', 'PE2'])
#         self.assertMultiLineEqual(cfg1['PE1'], '\n'.join(['<ospf xmlns="http://cisco.com/ns/yang/ned/ios">\n'
# '  <id>100</id>\n'
# '  <auto-cost>\n'
# '    <reference-bandwidth>12345</reference-bandwidth>\n'
# '  </auto-cost>\n'
# '  <nsr></nsr>\n'
# '  <router-id>2.1.1.1</router-id>\n'
# '  <vrf>test</vrf>\n'
# '</ospf>\n'
# '<GigabitEthernet xmlns="http://cisco.com/ns/yang/ned/ios">\n'
# '  <name>0/0/1</name>\n'
# '  <ip>\n'
# '    <ospf>\n'
# '      <cost>10</cost>\n'
# '      <process-id>\n'
# '        <id>100</id>\n'
# '        <area>0</area>\n'
# '      </process-id>\n'
# '    </ospf>\n'
# '  </ip>\n'
# '</GigabitEthernet>\n'
# '<GigabitEthernet xmlns="http://cisco.com/ns/yang/ned/ios">\n'
# '  <name>0/1/1</name>\n'
# '  <ip>\n'
# '    <ospf>\n'
# '      <cost>20</cost>\n'
# '      <process-id>\n'
# '        <id>100</id>\n'
# '        <area>1</area>\n'
# '      </process-id>\n'
# '    </ospf>\n'
# '  </ip>\n'
# '</GigabitEthernet>\n']))
#         self.assertMultiLineEqual(cfg1['PE2'], '\n'.join(['<ospf xmlns="http://cisco.com/ns/yang/ned/ios">\n'
# '  <id>100</id>\n'
# '  <auto-cost>\n'
# '    <reference-bandwidth>12345</reference-bandwidth>\n'
# '  </auto-cost>\n'
# '  <nsr></nsr>\n'
# '  <router-id>2.1.2.1</router-id>\n'
# '  <vrf>test</vrf>\n'
# '</ospf>\n'
# '<GigabitEthernet xmlns="http://cisco.com/ns/yang/ned/ios">\n'
# '  <name>0/0/2</name>\n'
# '  <ip>\n'
# '    <ospf>\n'
# '      <cost>10</cost>\n'
# '      <process-id>\n'
# '        <id>100</id>\n'
# '        <area>0</area>\n'
# '      </process-id>\n'
# '    </ospf>\n'
# '  </ip>\n'
# '</GigabitEthernet>\n'
# '<GigabitEthernet xmlns="http://cisco.com/ns/yang/ned/ios">\n'
# '  <name>0/1/2</name>\n'
# '  <ip>\n'
# '    <ospf>\n'
# '      <cost>20</cost>\n'
# '      <process-id>\n'
# '        <id>100</id>\n'
# '        <area>1</area>\n'
# '      </process-id>\n'
# '    </ospf>\n'
# '  </ip>\n'
# '</GigabitEthernet>\n']))
#
#         self.maxDiff = None
#
#         # Set a mock
#         dev1.configure = Mock()
#         dev2.configure = Mock()
#         dev1.add_feature(ospf)
#         dev2.add_feature(ospf)
#         # Mock config
#
#         output = ospf.build_config(apply=True)

        # uncfg1 = ospf.build_unconfig(apply=False, attributes={'device_attr':{'*':{'vrf_attr':{'*':{'area_attr':area_id}}}}})
        #
        # self.assertCountEqual(uncfg1.keys(), ['PE1', 'PE2'])
        # self.assertMultiLineEqual(uncfg1['PE1'], '\n'.join(['router ospf 100 vrf test\n'
        # ' no passive-interface GigabitEthernet0/0/1\n'
        # ' exit\n'
        # 'interface GigabitEthernet0/0/1\n'
        # ' no ip ospf 100 area 0\n'
        # ' no ip ospf cost 10\n'
        # ' exit']))
        #
        # self.assertMultiLineEqual(uncfg1['PE2'], '\n'.join(['interface GigabitEthernet0/0/2\n'
        # ' no ip ospf 100 area 0\n'
        # ' no ip ospf cost 10\n'
        # ' exit']))
        #
        # uncfg5 = ospf.build_unconfig(apply=False, attributes={'device_attr':{'*':{'vrf_attr':{'*':{'area_attr':{'*':{'interface_attr':'*'}}}}}}})
        #
        # self.assertCountEqual(uncfg5.keys(), ['PE1', 'PE2'])
        # self.assertMultiLineEqual(uncfg5['PE1'], '\n'.join(['router ospf 100 vrf test\n'
        # ' no passive-interface GigabitEthernet0/0/1\n'
        # ' exit\n'
        # 'interface GigabitEthernet0/0/1\n'
        # ' no ip ospf 100 area 0\n'
        # ' no ip ospf cost 10\n'
        # ' exit\n'
        # 'interface GigabitEthernet0/1/1\n'
        # ' no ip ospf 100 area 1\n'
        # ' no ip ospf cost 20\n'
        # ' exit']))
        #
        # self.assertMultiLineEqual(uncfg5['PE2'], '\n'.join(['interface GigabitEthernet0/0/2\n'
        # ' no ip ospf 100 area 0\n'
        # ' no ip ospf cost 10\n'
        # ' exit\n'
        # 'interface GigabitEthernet0/1/2\n'
        # ' no ip ospf 100 area 1\n'
        # ' no ip ospf cost 20\n'
        # ' exit']))
        #
        # uncfg2 = ospf.build_unconfig(apply=False, attributes={'device_attr':{'*':{'vrf_attr':{'*':{'area_attr':'*'}}}}})
        #
        # self.assertCountEqual(uncfg2.keys(), ['PE1', 'PE2'])
        # self.assertMultiLineEqual(uncfg2['PE1'], '\n'.join(['router ospf 100 vrf test\n'
        # ' no passive-interface GigabitEthernet0/0/1\n'
        # ' exit\n'
        # 'interface GigabitEthernet0/0/1\n'
        # ' no ip ospf 100 area 0\n'
        # ' no ip ospf cost 10\n'
        # ' exit\n'
        # 'interface GigabitEthernet0/1/1\n'
        # ' no ip ospf 100 area 1\n'
        # ' no ip ospf cost 20\n'
        # ' exit']))
        #
        # self.assertMultiLineEqual(uncfg2['PE2'], '\n'.join(['interface GigabitEthernet0/0/2\n'
        # ' no ip ospf 100 area 0\n'
        # ' no ip ospf cost 10\n'
        # ' exit\n'
        # 'interface GigabitEthernet0/1/2\n'
        # ' no ip ospf 100 area 1\n'
        # ' no ip ospf cost 20\n'
        # ' exit']))
        #
        #
        # uncfg3 = ospf.build_unconfig(apply=False, attributes={'device_attr':{'*':{'vrf_attr':'*'}}})
        #
        # self.assertCountEqual(uncfg3.keys(), ['PE1', 'PE2'])
        # self.assertMultiLineEqual(uncfg3['PE1'], '\n'.join(['no router ospf 100 vrf test\n'
        # 'interface GigabitEthernet0/0/1\n'
        # ' no ip ospf 100 area 0\n'
        # ' no ip ospf cost 10\n'
        # ' exit\n'
        # 'interface GigabitEthernet0/1/1\n'
        # ' no ip ospf 100 area 1\n'
        # ' no ip ospf cost 20\n'
        # ' exit']))
        #
        # self.assertMultiLineEqual(uncfg3['PE2'], '\n'.join(['no router ospf 100 vrf test\n'
        # 'interface GigabitEthernet0/0/2\n'
        # ' no ip ospf 100 area 0\n'
        # ' no ip ospf cost 10\n'
        # ' exit\n'
        # 'interface GigabitEthernet0/1/2\n'
        # ' no ip ospf 100 area 1\n'
        # ' no ip ospf cost 20\n'
        # ' exit']))
        #
        # uncfg4 = ospf.build_unconfig(apply=False)
        #
        # self.assertCountEqual(uncfg4.keys(), ['PE1', 'PE2'])
        # self.assertMultiLineEqual(uncfg4['PE1'], '\n'.join(['no router ospf 100 vrf test\n'
        # 'interface GigabitEthernet0/0/1\n'
        # ' no ip ospf 100 area 0\n'
        # ' no ip ospf cost 10\n'
        # ' exit\n'
        # 'interface GigabitEthernet0/1/1\n'
        # ' no ip ospf 100 area 1\n'
        # ' no ip ospf cost 20\n'
        # ' exit']))
        #
        # self.assertMultiLineEqual(uncfg4['PE2'], '\n'.join(['no router ospf 100 vrf test\n'
        # 'interface GigabitEthernet0/0/2\n'
        # ' no ip ospf 100 area 0\n'
        # ' no ip ospf cost 10\n'
        # ' exit\n'
        # 'interface GigabitEthernet0/1/2\n'
        # ' no ip ospf 100 area 1\n'
        # ' no ip ospf cost 20\n'
        # ' exit']))

if __name__ == '__main__':
    unittest.main()
