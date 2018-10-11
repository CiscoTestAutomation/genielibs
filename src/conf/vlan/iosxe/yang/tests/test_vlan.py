#!/usr/bin/env python

#python
import unittest
from unittest.mock import Mock

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import SubAttributes, \
                                       SubAttributesDict, \
                                       AttributesHelper, \
                                       KeyedSubAttributes

from genie.libs.conf.vlan import Vlan

try:
    # from ydk.models.ned import ned
    from ydk.models.xe_recent_edison import Cisco_IOS_XE_native as ned
    from ydk.services import CodecService
    from ydk.providers import CodecServiceProvider
    from ydk.types import DELETE, Empty
    from ydk.services import CRUDService

    # patch a netconf provider
    from ydk.providers import NetconfServiceProvider as _NetconfServiceProvider
    from ydk.providers._provider_plugin import _ClientSPPlugin
except:
    pass

class NetconfConnectionInfo(object):
    def __init__(self):
        self.ip = '1.1.1.1'
        self.port = 830
        self.username = 'admin'
        self.password = 'lab'

class test_vlan(unittest.TestCase):

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
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe', context='yang')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe', context='yang')
        intf1 = Interface(name='GigabitEthernet0/0/1',device=dev1)
        intf2 = Interface(name='GigabitEthernet0/0/2',device=dev2)
        intf3 = Interface(name='Vlan100',device=dev1)
        link = Link(name='1_2_1',testbed=testbed)
        link.connect_interface(interface=intf1)
        link.connect_interface(interface=intf2)
        vlan = Vlan()

        for dev in testbed.devices:
            dev.connections=Mock()
            dev.connections={'netconf':NetconfConnectionInfo()}

        link.add_feature(vlan)
        vlan.vlan_id = 100

        cfg1 = vlan.build_config(apply=False)
        self.assertCountEqual(cfg1.keys(), ['PE1', 'PE2'])
        compare = ""
        for i in cfg1['PE1']: 
            compare+=str(i)

        self.assertMultiLineEqual(compare, '\n'.join(
            ['<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
'  <target>\n'
'    <running></running>\n'
'  </target>\n'
'  <config>\n'
'    <vlan xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
'      <vlan-list xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-vlan">\n'
'        <id>100</id>\n'
'      </vlan-list>\n'
'    </vlan>\n'
'  </config>\n'
'</edit-config>\n']))

        compare = ""
        for i in cfg1['PE2']: 
            compare+=str(i)

        self.assertMultiLineEqual(compare, '\n'.join(
            ['<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
'  <target>\n'
'    <running></running>\n'
'  </target>\n'
'  <config>\n'
'    <vlan xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
'      <vlan-list xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-vlan">\n'
'        <id>100</id>\n'
'      </vlan-list>\n'
'    </vlan>\n'
'  </config>\n'
'</edit-config>\n']))

    def test_basic_uncfg(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe', context='yang')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe', context='yang')
        intf1 = Interface(name='GigabitEthernet0/0/1',device=dev1)
        intf2 = Interface(name='GigabitEthernet0/0/2',device=dev2)
        intf3 = Interface(name='Vlan100',device=dev1)
        vlan = Vlan()

        for dev in testbed.devices:
            dev.connections=Mock()
            dev.connections={'netconf':NetconfConnectionInfo()}

        vlan.device_attr[dev1].vlan_id = 100
        vlan.device_attr[dev2].vlan_id = 300

        # Unconfig testing
        # Set a mock
        dev1.configure = Mock()
        dev2.configure = Mock()
        dev1.add_feature(vlan)
        dev2.add_feature(vlan)
        # Mock config

        uncfg1 = vlan.build_unconfig(apply=False)
        self.assertCountEqual(uncfg1.keys(), ['PE1', 'PE2'])

        compare = ""
        for i in uncfg1['PE1']: 
            compare+=str(i)

        # A case has been already raised by JB so the unconfig for yang works as expected.
        # Currently, retruned xml for yang unconfig is exactly the same for the unconfig one.
        self.assertMultiLineEqual(compare, '\n'.join(
            ['<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
'  <target>\n'
'    <running></running>\n'
'  </target>\n'
'  <config>\n'
'    <vlan xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
'      <vlan-list xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-vlan">\n'
'        <id>100</id>\n'
'      </vlan-list>\n'
'    </vlan>\n'
'  </config>\n'
'</edit-config>\n']))

        compare = ""
        for i in uncfg1['PE2']: 
            compare+=str(i)

        self.assertMultiLineEqual(compare, '\n'.join(
            ['<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
'  <target>\n'
'    <running></running>\n'
'  </target>\n'
'  <config>\n'
'    <vlan xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">\n'
'      <vlan-list xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-vlan">\n'
'        <id>300</id>\n'
'      </vlan-list>\n'
'    </vlan>\n'
'  </config>\n'
'</edit-config>\n']))

if __name__ == '__main__':
    unittest.main()