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

class test_interface(unittest.TestCase):

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

        self.assertCountEqual(link.interfaces, [intf1, intf2])
        self.assertEqual(intf1.device, dev1)
        self.assertEqual(intf2.device, dev2)

    def test_basic_gig_cfg(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe', context='yang')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe', context='yang')
        intf1 = Interface(name='GigabitEthernet0/0/1',device=dev1)
        intf2 = Interface(name='GigabitEthernet0/0/2',device=dev2)
        link = Link(name='1_2_1',testbed=testbed)
        link.connect_interface(interface=intf1)
        link.connect_interface(interface=intf2)
        vrf = Vrf(name='test')
        intf1.vrf = vrf
        intf2.vrf = vrf
        intf1.ipv4 = '1.2.3.4/30'
        intf2.ipv4 = '1.2.3.5/30'
        intf1.shutdown = False
        intf2.shutdown = True

        self.maxDiff = None
        cfg1 = intf1.build_config(apply=False)
        cfg2 = intf2.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg1), '''<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target>
    <running></running>
  </target>
  <config>
    <GigabitEthernet xmlns="http://cisco.com/ns/yang/ned/ios">
      <name>0/0/1</name>
      <ip>
        <address>
          <primary>
            <address>1.2.3.4</address>
            <mask>255.255.255.252</mask>
          </primary>
        </address>
      </ip>
      <shutdown xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"/>
      <vrf>
        <forwarding>test</forwarding>
      </vrf>
    </GigabitEthernet>
  </config>
</edit-config>
''')


        self.assertMultiLineEqual(str(cfg2),'''<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target>
    <running></running>
  </target>
  <config>
    <GigabitEthernet xmlns="http://cisco.com/ns/yang/ned/ios">
      <name>0/0/2</name>
      <ip>
        <address>
          <primary>
            <address>1.2.3.5</address>
            <mask>255.255.255.252</mask>
          </primary>
        </address>
      </ip>
      <shutdown></shutdown>
      <vrf>
        <forwarding>test</forwarding>
      </vrf>
    </GigabitEthernet>
  </config>
</edit-config>
''')


        uncfg1 = intf1.build_unconfig(apply=False)
        uncfg2 = intf2.build_unconfig(apply=False)

        self.assertMultiLineEqual(str(uncfg1), '''<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target>
    <running></running>
  </target>
  <config>
    <GigabitEthernet xmlns="http://cisco.com/ns/yang/ned/ios">
      <name>0/0/1</name>
      <ip>
        <address>
          <primary>
            <address xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"/>
            <mask xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"/>
          </primary>
        </address>
      </ip>
      <shutdown></shutdown>
      <vrf>
        <forwarding xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"/>
      </vrf>
    </GigabitEthernet>
  </config>
</edit-config>
''')

        self.assertMultiLineEqual(str(uncfg2), '''<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target>
    <running></running>
  </target>
  <config>
    <GigabitEthernet xmlns="http://cisco.com/ns/yang/ned/ios">
      <name>0/0/2</name>
      <ip>
        <address>
          <primary>
            <address xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"/>
            <mask xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"/>
          </primary>
        </address>
      </ip>
      <shutdown></shutdown>
      <vrf>
        <forwarding xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"/>
      </vrf>
    </GigabitEthernet>
  </config>
</edit-config>
''')

    def test_basic_loopback_cfg(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe', context='yang')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe', context='yang')
        intf1 = Interface(name='Loopback100',device=dev1)
        intf2 = Interface(name='Loopback200',device=dev2)
        link = Link(name='1_2_1',testbed=testbed)
        link.connect_interface(interface=intf1)
        link.connect_interface(interface=intf2)
        vrf = Vrf(name='test')
        intf1.vrf = vrf
        intf2.vrf = vrf
        intf1.ipv4 = '1.2.3.4/32'
        intf2.ipv4 = '1.2.3.5/32'

        cfg1 = intf1.build_config(apply=False)
        cfg2 = intf2.build_config(apply=False)
        print(cfg1)
        print(cfg2)
        self.assertMultiLineEqual(str(cfg1), '''<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target>
    <running></running>
  </target>
  <config>
    <Loopback xmlns="http://cisco.com/ns/yang/ned/ios">
      <name>100</name>
      <ip>
        <address>
          <primary>
            <address>1.2.3.4</address>
            <mask>255.255.255.255</mask>
          </primary>
        </address>
      </ip>
      <vrf>
        <forwarding>test</forwarding>
      </vrf>
    </Loopback>
  </config>
</edit-config>
''')

        self.assertMultiLineEqual(str(cfg2), '''<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target>
    <running></running>
  </target>
  <config>
    <Loopback xmlns="http://cisco.com/ns/yang/ned/ios">
      <name>200</name>
      <ip>
        <address>
          <primary>
            <address>1.2.3.5</address>
            <mask>255.255.255.255</mask>
          </primary>
        </address>
      </ip>
      <vrf>
        <forwarding>test</forwarding>
      </vrf>
    </Loopback>
  </config>
</edit-config>
''')

if __name__ == '__main__':
    unittest.main()
