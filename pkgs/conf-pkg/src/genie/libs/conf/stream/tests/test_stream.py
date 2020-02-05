#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from genie.utils.cisco_collections import typedset

from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import UnsupportedAttributeWarning

from genie.libs.conf.stream import Stream
from genie.libs.conf.base import MAC, IPv4Address, IPv6Address


class test_stream(TestCase):

    def assertTypedEqual(self, first, second, msg=None):
        self.assertEqual(
            (type(first), first),
            (type(second), second),
            msg=msg)

    def test_init(self):

        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='iosxr')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2')
        dev2 = Device(name='PE2', os='iosxr')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/0/3')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/0/4')
        tgen = Device(testbed=Genie.testbed, name='TGEN', os='spirent')
        intf5 = Interface(device=tgen, name='1/1', intf_mode='ethernet')
        intf6 = Interface(device=tgen, name='1/2', intf_mode='ethernet')
        Link(name='PE1-TGEN-1', interfaces=(intf1, intf5))
        Link(name='PE1-PE2-1', interfaces=(intf2, intf3))
        Link(name='PE2-TGEN-1', interfaces=(intf4, intf6))

        with self.assertRaises(AttributeError):
            stream1 = Stream()

        stream1 = Stream(source=intf5,
                         destination=intf6)
        self.assertIs(stream1.source_tgen_interface, intf5)
        self.assertIs(stream1.device, tgen)
        self.assertIs(stream1.testbed, Genie.testbed)
        self.assertTypedEqual(stream1.tgen_handle, None)
        self.assertTypedEqual(stream1.source, intf5)
        self.assertTypedEqual(stream1.source_instance, None)
        self.assertTypedEqual(stream1.source_count, 1)
        self.assertTypedEqual(stream1.destination, intf6)
        self.assertTypedEqual(stream1.destination_instance, None)
        self.assertTypedEqual(stream1.destination_count, 1)
        self.assertTypedEqual(stream1.destination_tgen_interfaces, frozenset([stream1.destination]))
        self.assertTypedEqual(stream1.layer2_protocol, Stream.Layer2Protocol.ethernet_ii)
        self.assertTypedEqual(stream1.source_mac_address, None)
        self.assertTypedEqual(stream1.source_mac_address_count, 0)
        self.assertTypedEqual(stream1.source_mac_address_step, None)
        self.assertTypedEqual(stream1.destination_mac_address, MAC('ffff.ffff.ffff'))
        self.assertTypedEqual(stream1.destination_mac_address_count, 1)
        self.assertTypedEqual(stream1.destination_mac_address_step, 1)
        self.assertTypedEqual(stream1.eth_encap_val1, None)
        self.assertTypedEqual(stream1.eth_encap_count1, 0)
        self.assertTypedEqual(stream1.eth_encap_step1, None)
        self.assertTypedEqual(stream1.eth_encap_range1, range(0))
        self.assertTypedEqual(stream1.eth_encap_val2, None)
        self.assertTypedEqual(stream1.eth_encap_count2, 0)
        self.assertTypedEqual(stream1.eth_encap_step2, None)
        self.assertTypedEqual(stream1.eth_encap_range2, range(0))
        self.assertTypedEqual(stream1.mpls_labels, ())
        self.assertTypedEqual(stream1.ip_version, None)
        self.assertIs(stream1.layer3_protocol, None)
        self.assertTypedEqual(stream1.source_ip, None)
        self.assertTypedEqual(stream1.source_ip_count, 0)
        self.assertTypedEqual(stream1.source_ip_step, None)
        self.assertTypedEqual(stream1.destination_ip, None)
        self.assertTypedEqual(stream1.destination_ip_count, 0)
        self.assertTypedEqual(stream1.destination_ip_step, None)
        self.assertIs(stream1.layer4_protocol, None)
        self.assertTypedEqual(stream1.bandwidth, 10)
        self.assertIs(stream1.bandwidth_units, Stream.BandwidthUnits.kbps)
        self.assertTypedEqual(stream1.frame_length, 512)
        self.assertTypedEqual(stream1.frame_length_mode, Stream.FrameLengthMode.l2)
        self.assertTypedEqual(stream1.name, None)
        self.assertTypedEqual(stream1.obj_state, 'active')
        self.assertTypedEqual(stream1.sub_stream_increments, typedset(Stream.SubStreamIncrement, ()))

        intf1.mac_address = 'baad.baad.beef'
        intf5.mac_address = 'aaaa.bbbb.cccc'
        intf5.eth_encap_val1 = 1001
        stream1.eth_encap_range2 = range(2000, 3000, 2)
        intf5.ipv4 = '1.2.3.1/24'
        intf6.ipv4 = '1.2.3.2/24'
        self.assertIs(stream1.source_tgen_interface, intf5)
        self.assertIs(stream1.device, tgen)
        self.assertIs(stream1.testbed, Genie.testbed)
        self.assertTypedEqual(stream1.tgen_handle, None)
        self.assertTypedEqual(stream1.source, intf5)
        self.assertTypedEqual(stream1.source_instance, None)
        self.assertTypedEqual(stream1.source_count, 1)
        self.assertTypedEqual(stream1.destination, intf6)
        self.assertTypedEqual(stream1.destination_instance, None)
        self.assertTypedEqual(stream1.destination_count, 1)
        self.assertTypedEqual(stream1.destination_tgen_interfaces, frozenset([stream1.destination]))
        self.assertTypedEqual(stream1.layer2_protocol, Stream.Layer2Protocol.ethernet_ii)
        self.assertTypedEqual(stream1.source_mac_address, MAC('aaaa.bbbb.cccc'))
        self.assertTypedEqual(stream1.source_mac_address_count, 1)
        self.assertTypedEqual(stream1.source_mac_address_step, 1)
        self.assertTypedEqual(stream1.destination_mac_address, MAC('ffff.ffff.ffff'))
        self.assertTypedEqual(stream1.destination_mac_address_count, 1)
        self.assertTypedEqual(stream1.destination_mac_address_step, 1)
        self.assertTypedEqual(stream1.eth_encap_val1, 1001)
        self.assertTypedEqual(stream1.eth_encap_count1, 1)
        self.assertTypedEqual(stream1.eth_encap_step1, 1)
        self.assertTypedEqual(stream1.eth_encap_range1, range(1001, 1002))
        self.assertTypedEqual(stream1.eth_encap_val2, 2000)
        self.assertTypedEqual(stream1.eth_encap_count2, 500)
        self.assertTypedEqual(stream1.eth_encap_step2, 2)
        self.assertTypedEqual(stream1.eth_encap_range2, range(2000, 3000, 2))
        self.assertTypedEqual(stream1.mpls_labels, ())
        self.assertTypedEqual(stream1.ip_version, 4)
        self.assertIs(stream1.layer3_protocol, Stream.Layer3Protocol.ipv4)
        self.assertTypedEqual(stream1.source_ip, IPv4Address('1.2.3.1'))
        self.assertTypedEqual(stream1.source_ip_count, 1)
        self.assertTypedEqual(stream1.source_ip_step, 1)
        self.assertTypedEqual(stream1.destination_ip, IPv4Address('1.2.3.2'))
        self.assertTypedEqual(stream1.destination_ip_count, 1)
        self.assertTypedEqual(stream1.destination_ip_step, 1)
        self.assertIs(stream1.layer4_protocol, None)
        self.assertTypedEqual(stream1.bandwidth, 10)
        self.assertIs(stream1.bandwidth_units, Stream.BandwidthUnits.kbps)
        self.assertTypedEqual(stream1.frame_length, 512)
        self.assertTypedEqual(stream1.frame_length_mode, Stream.FrameLengthMode.l2)
        self.assertTypedEqual(stream1.name, None)
        self.assertTypedEqual(stream1.obj_state, 'active')
        self.assertTypedEqual(stream1.sub_stream_increments, typedset(Stream.SubStreamIncrement, ()))

if __name__ == '__main__':
    unittest.main()

