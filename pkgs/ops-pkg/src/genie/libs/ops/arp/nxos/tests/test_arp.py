# Python
import unittest

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.arp.nxos.arp import Arp
from genie.libs.ops.arp.nxos.tests.arp_output import ArpOutput

# Parser
from genie.libs.parser.nxos.show_arp import ShowIpArpDetailVrfAll, \
                                            ShowIpArpSummaryVrfAll, \
                                            ShowIpArpstatisticsVrfAll

from genie.libs.parser.nxos.show_interface import ShowIpInterfaceVrfAll


class test_arp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        arp = Arp(device=self.device)

        # Get outputs
        arp.maker.outputs[ShowIpArpDetailVrfAll] = \
            {"": ArpOutput.ShowIpArpDetailVrfAll}

        arp.maker.outputs[ShowIpArpSummaryVrfAll] = \
            {"": ArpOutput.ShowIpArpSummaryVrfAll}

        arp.maker.outputs[ShowIpArpstatisticsVrfAll] = \
            {"": ArpOutput.ShowIpArpstatisticsVrfAll}

        arp.maker.outputs[ShowIpInterfaceVrfAll] = \
            {"": ArpOutput.ShowIpInterfaceVrfAll}

        # Learn the feature
        arp.learn()

        # Verify Ops was created successfully
        self.assertEqual(arp.info, ArpOutput.Arp_info)

        # Check specific attribute values
        # info - interfaces
        self.assertEqual(arp.info['interfaces']['Ethernet1/4.200']['ipv4']\
            ['neighbors']['10.76.1.101']['ip'], '10.76.1.101')
        # info - statistics
        self.assertEqual(arp.info['statistics']['in_drops'], 28218)

    def test_output_with_attribute(self):
        self.maxDiff = None
        arp = Arp(device=self.device,
                  attributes=['info[statistics][(.*)]'])

        # Get outputs
        arp.maker.outputs[ShowIpArpDetailVrfAll] = \
            {"": ArpOutput.ShowIpArpDetailVrfAll}

        arp.maker.outputs[ShowIpArpSummaryVrfAll] = \
            {"": ArpOutput.ShowIpArpSummaryVrfAll}

        arp.maker.outputs[ShowIpArpstatisticsVrfAll] = \
            {"": ArpOutput.ShowIpArpstatisticsVrfAll}

        arp.maker.outputs[ShowIpInterfaceVrfAll] = \
            {"": ArpOutput.ShowIpInterfaceVrfAll}

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
        arp.maker.outputs[ShowIpArpDetailVrfAll] = \
            {"": {}}

        arp.maker.outputs[ShowIpArpSummaryVrfAll] = \
            {"": {}}

        arp.maker.outputs[ShowIpArpstatisticsVrfAll] = \
            {"": {}}

        arp.maker.outputs[ShowIpInterfaceVrfAll] = \
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
        arp.maker.outputs[ShowIpArpDetailVrfAll] = \
            {"": ArpOutput.ShowIpArpDetailVrfAll}

        arp.maker.outputs[ShowIpArpSummaryVrfAll] = \
            {"": {}}

        arp.maker.outputs[ShowIpArpstatisticsVrfAll] = \
            {"": {}}

        arp.maker.outputs[ShowIpInterfaceVrfAll] = \
            {"": ArpOutput.ShowIpInterfaceVrfAll}

        # Learn the feature
        arp.learn()
                
        # Check no attribute not found
        with self.assertRaises(KeyError):
            arp.info['statistics']

if __name__ == '__main__':
    unittest.main()
