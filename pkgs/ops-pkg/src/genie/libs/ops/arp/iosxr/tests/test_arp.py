# Python
import unittest

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.arp.iosxr.arp import Arp
from genie.libs.ops.arp.iosxr.tests.arp_output import ArpOutput

# Parser
from genie.libs.parser.iosxr.show_arp import ShowArpDetail, \
                                             ShowArpTrafficDetail

from genie.libs.parser.iosxr.show_interface import ShowIpv4VrfAllInterface


class test_arp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        arp = Arp(device=self.device)

        # Get outputs
        arp.maker.outputs[ShowArpDetail] = \
            {"": ArpOutput.ShowArpDetail}

        arp.maker.outputs[ShowArpTrafficDetail] = \
            {"": ArpOutput.ShowArpTrafficDetail}

        arp.maker.outputs[ShowIpv4VrfAllInterface] = \
            {"": ArpOutput.ShowIpv4VrfAllInterface}

        # Learn the feature
        arp.learn()

        # Verify Ops was created successfully
        self.assertEqual(arp.info, ArpOutput.Arp_info)

        # Check specific attribute values
        # info - interfaces
        self.assertEqual(arp.info['interfaces']['GigabitEthernet0/0/0/0']\
            ['ipv4']['neighbors']['10.1.2.1']['ip'], '10.1.2.1')
        # info - statistics
        self.assertEqual(
            arp.info['statistics']['in_replies_pkts'], 8)

    def test_output_with_attribute(self):
        self.maxDiff = None
        arp = Arp(device=self.device,
                  attributes=['info[statistics][(.*)]'])

        # Get outputs
        arp.maker.outputs[ShowArpDetail] = \
            {"": ArpOutput.ShowArpDetail}

        arp.maker.outputs[ShowArpTrafficDetail] = \
            {"": ArpOutput.ShowArpTrafficDetail}

        arp.maker.outputs[ShowIpv4VrfAllInterface] = \
            {"": ArpOutput.ShowIpv4VrfAllInterface}

        # Learn the feature
        arp.learn()

        # Check no attribute not found
        with self.assertRaises(KeyError):
            arp.info['interfaces']

        # info - statistics
        self.assertEqual(arp.info['statistics'],
            ArpOutput.Arp_info['statistics'])

    def test_empty_output(self):
        self.maxDiff = None
        arp = Arp(device=self.device)

        # Get outputs
        arp.maker.outputs[ShowArpDetail] = \
            {"": {}}

        arp.maker.outputs[ShowArpTrafficDetail] = \
            {"": {}}

        arp.maker.outputs[ShowIpv4VrfAllInterface] = \
            {"": {}}

        # Learn the feature
        arp.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            arp.info['statistics']

    def test_incomplete_output(self):
        self.maxDiff = None
        
        arp = Arp(device=self.device)

        # Get outputs
        arp.maker.outputs[ShowArpDetail] = \
            {"": ArpOutput.ShowArpDetail}

        arp.maker.outputs[ShowArpTrafficDetail] = \
            {"": {}}

        arp.maker.outputs[ShowIpv4VrfAllInterface] = \
            {"": ArpOutput.ShowIpv4VrfAllInterface}

        # Learn the feature
        arp.learn()
                
        # Check no attribute not found
        with self.assertRaises(KeyError):
            arp.info['statistics']

if __name__ == '__main__':
    unittest.main()