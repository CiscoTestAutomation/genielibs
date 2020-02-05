# Python
import unittest

# ATS
from pyats.topology import Device
from unittest.mock import Mock
# Genie
from genie.libs.ops.arp.iosxe.arp import Arp
from genie.libs.ops.arp.iosxe.tests.arp_output import ArpOutput

# Parser
from genie.libs.parser.iosxe.show_arp import ShowArp, \
                                             ShowIpArpSummary, \
                                             ShowIpTraffic, ShowIpArp

from genie.libs.parser.iosxe.show_interface import ShowIpInterface
from genie.libs.parser.iosxe.show_vrf import ShowVrf

outputs = {}
outputs['show ip arp'] = ArpOutput.ShowIpArp_all
outputs['show ip arp vrf VRF1'] = ArpOutput.ShowIpArp_vrf1
def mapper(key):
    return outputs[key]


class test_arp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        arp = Arp(device=self.device)

        # Get outputs
        arp.maker.outputs[ShowArp] = \
            {"": ArpOutput.ShowArp}
        arp.maker.outputs[ShowVrf] = \
            {"": ArpOutput.ShowVrf}
        arp.maker.outputs[ShowIpArp] = \
            {"{'vrf':'VRF1'}": ArpOutput.ShowIpArp}
        arp.maker.outputs[ShowIpArpSummary] = \
            {"": ArpOutput.ShowIpArpSummary}

        arp.maker.outputs[ShowIpTraffic] = \
            {"": ArpOutput.ShowIpTraffic}

        arp.maker.outputs[ShowIpInterface] = \
            {"": ArpOutput.ShowIpInterface}
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        arp.learn()

        # Verify Ops was created successfully
        self.assertDictEqual(arp.info, ArpOutput.Arp_info)

        # Check specific attribute values
        # info - interfaces
        self.assertEqual(arp.info['interfaces']['Vlan100']['ipv4']\
            ['neighbors']['192.168.234.1']['ip'], '192.168.234.1')
        # info - statistics
        self.assertEqual(arp.info['statistics']['entries_total'], 8)

    def test_output_with_attribute(self):
        self.maxDiff = None
        arp = Arp(device=self.device,
                  attributes=['info[statistics][(.*)]'])

        # Get outputs
        arp.maker.outputs[ShowArp] = \
            {"": ArpOutput.ShowArp}
        arp.maker.outputs[ShowVrf] = \
            {"": ArpOutput.ShowVrf}
        arp.maker.outputs[ShowIpArp] = \
            {"{'vrf':'VRF1'}": ArpOutput.ShowIpArp}
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
        arp.maker.outputs[ShowArp] = \
            {"": {}}
        arp.maker.outputs[ShowVrf] = \
            {"": {}}
        arp.maker.outputs[ShowIpArp] = \
            {"{'vrf':'VRF1'}": {}}
        arp.maker.outputs[ShowIpArpSummary] = \
            {"": {}}

        arp.maker.outputs[ShowIpTraffic] = \
            {"": {}}

        arp.maker.outputs[ShowIpInterface] = \
            {"": {}}
        outputs['show ip arp']=''
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        arp.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            arp.info['statistics']
        outputs['show ip arp'] = ArpOutput.ShowIpArp_all

    def test_incomplete_output(self):
        self.maxDiff = None
        
        arp = Arp(device=self.device)

        # Get outputs
        arp.maker.outputs[ShowArp] = \
            {"": ArpOutput.ShowArp}
        arp.maker.outputs[ShowVrf] = \
            {"": ArpOutput.ShowVrf}
        arp.maker.outputs[ShowIpArp] = \
            {"{'vrf':'VRF1'}": ArpOutput.ShowIpArp}
        arp.maker.outputs[ShowIpArpSummary] = \
            {"": {}}

        arp.maker.outputs[ShowIpTraffic] = \
            {"": {}}

        arp.maker.outputs[ShowIpInterface] = \
            {"": ArpOutput.ShowIpInterface}
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        arp.learn()
                
        # Check no attribute not found
        with self.assertRaises(KeyError):
            arp.info['statistics']

if __name__ == '__main__':
    unittest.main()