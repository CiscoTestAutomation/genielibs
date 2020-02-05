# Python
import unittest

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.arp.ios.arp import Arp
from genie.libs.ops.arp.ios.tests.arp_output import ArpOutput

# Parser
from genie.libs.parser.ios.show_arp import ShowIpArp, \
                                           ShowIpArpSummary, \
                                           ShowIpTraffic

from genie.libs.parser.ios.show_interface import ShowIpInterface
from genie.libs.parser.ios.show_vrf import ShowVrf

class test_arp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'ios'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        arp = Arp(device=self.device)

        # Get outputs
        arp.maker.outputs[ShowIpArp] = \
            {"": ArpOutput.ShowIpArp,
             "{'vrf':'VRF1'}": ArpOutput.ShowIpArpVrf}
        arp.maker.outputs[ShowVrf] = \
            {"": ArpOutput.ShowVrf}

        arp.maker.outputs[ShowIpArpSummary] = \
            {"": ArpOutput.ShowIpArpSummary}

        arp.maker.outputs[ShowIpTraffic] = \
            {"": ArpOutput.ShowIpTraffic}

        arp.maker.outputs[ShowIpInterface] = \
            {"": ArpOutput.ShowIpInterface}

        # Learn the feature
        arp.learn()

        # Verify Ops was created successfully
        self.assertEqual(arp.info, ArpOutput.Arp_info)

        # Check specific attribute values
        # info - interfaces
        self.assertEqual(arp.info['interfaces']['Port-channel10']['ipv4']\
            ['neighbors']['10.9.1.1']['ip'], '10.9.1.1')
        # info - statistics
        self.assertEqual(arp.info['statistics']['in_drops'], 0)

    def test_output_with_attribute(self):
        self.maxDiff = None
        arp = Arp(device=self.device,
                  attributes=['info[statistics][(.*)]'])

        # Get outputs
        arp.maker.outputs[ShowIpArp] = \
            {"": ArpOutput.ShowIpArp,
             "{'vrf':'VRF1'}": ArpOutput.ShowIpArpVrf}
        arp.maker.outputs[ShowVrf] = \
            {"": ArpOutput.ShowVrf}
        arp.maker.outputs[ShowIpArpSummary] = \
            {"": ArpOutput.ShowIpArpSummary}

        arp.maker.outputs[ShowIpTraffic] = \
            {"": ArpOutput.ShowIpTraffic}

        arp.maker.outputs[ShowIpInterface] = \
            {"": ArpOutput.ShowIpInterface}

        # Learn the feature
        arp.learn()

        # Check no attribute not found
        with self.assertRaises(KeyError):
            arp.info['interfaces']

        # info - statistics
        self.assertEqual(arp.info['statistics'], ArpOutput.Arp_info['statistics'])

    def test_empty_output(self):
        self.maxDiff = None
        arp = Arp(device=self.device)

        # Get outputs
        arp.maker.outputs[ShowIpArp] = \
            {"": {},
             "{'vrf':'VRF1'}": {}}
        arp.maker.outputs[ShowVrf] = \
            {"": {}}

        arp.maker.outputs[ShowIpArpSummary] = \
            {"": {}}

        arp.maker.outputs[ShowIpTraffic] = \
            {"": {}}

        arp.maker.outputs[ShowIpInterface] = \
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
        arp.maker.outputs[ShowIpArp] = \
            {"": ArpOutput.ShowIpArp,
             "{'vrf':'VRF1'}": ArpOutput.ShowIpArpVrf}
        arp.maker.outputs[ShowVrf] = \
            {"": ArpOutput.ShowVrf}

        arp.maker.outputs[ShowIpArpSummary] = \
            {"": {}}

        arp.maker.outputs[ShowIpTraffic] = \
            {"": {}}

        arp.maker.outputs[ShowIpInterface] = \
            {"": ArpOutput.ShowIpInterface}

        # Learn the feature
        arp.learn()
                
        # Check no attribute not found
        with self.assertRaises(KeyError):
            arp.info['statistics']

if __name__ == '__main__':
    unittest.main()