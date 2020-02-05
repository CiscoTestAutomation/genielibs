# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock

# genie-libs
from genie.libs.ops.msdp.nxos.msdp import Msdp
from genie.libs.ops.msdp.nxos.tests.msdp_output import MsdpOutput

from genie.libs.parser.nxos.show_msdp import ShowIpMsdpPeerVrf, \
                                             ShowIpMsdpSaCacheDetailVrf


outputs = {}
outputs['show ip msdp policy statistics sa-policy 10.4.1.1 in'] = MsdpOutput.ShowIpMsdpPolicyStatisticsSaPolicyIn
outputs['show ip msdp policy statistics sa-policy 10.94.44.44 in vrf VRF1'] = MsdpOutput.ShowIpMsdpPolicyStatisticsSaPolicyInVRF1
outputs['show ip msdp policy statistics sa-policy 10.4.1.1 out'] = MsdpOutput.ShowIpMsdpPolicyStatisticsSaPolicyOut
outputs['show ip msdp policy statistics sa-policy 10.94.44.44 out vrf VRF1'] = MsdpOutput.ShowIpMsdpPolicyStatisticsSaPolicyOutVRF1
outputs['show ip msdp summary'] = MsdpOutput.ShowIpMsdpSummary
outputs['show ip msdp summary vrf VRF1'] = MsdpOutput.ShowIpMsdpSummaryVRF1
outputs['show ip msdp sa-cache detail vrf all'] = MsdpOutput.showIpMsdpSaCacheDetailVrf
outputs['show ip msdp peer vrf all'] = MsdpOutput.showIpMsdpPeerVrf


def mapper(key):
    return outputs[key]

class test_msdp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_msdp_full(self):
        f= Msdp(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        f.learn()
        self.maxDiff = None
        self.assertEqual(f.info, MsdpOutput.showOpsOutput)

    def test_msdp_selective_attribute(self):
        f = Msdp(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        f.learn()

        self.assertEqual('R4', f.info['vrf']['VRF1']['peer']['10.94.44.44']['description'])
        # Check does not match
        self.assertNotEqual(1, f.info['vrf']['VRF1']['peer']['10.94.44.44']['description'])


    def test_msdp_missing_attributes(self):
        f = Msdp(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            description = f.info['description']

    def test_msdp_empty_output(self):
        f = Msdp(device=self.device)


        self.device.execute = Mock()
        
        outputs['show ip msdp policy statistics sa-policy 10.4.1.1 in'] = ''
        outputs['show ip msdp policy statistics sa-policy 10.94.44.44 in vrf VRF1'] = ''
        outputs['show ip msdp policy statistics sa-policy 10.4.1.1 out'] = ''
        outputs['show ip msdp policy statistics sa-policy 10.94.44.44 out vrf VRF1'] = ''
        outputs['show ip msdp summary'] = ''
        outputs['show ip msdp summary vrf VRF1'] = ''
        outputs['show ip msdp sa-cache detail vrf all'] = ''
        outputs['show ip msdp peer vrf all'] = ''
        self.device.execute.side_effect = mapper

        self.maxDiff = None
        # Learn the feature
        f.learn()

        # revert the global outputs back        
        outputs['show ip msdp policy statistics sa-policy 10.4.1.1 in'] = \
            MsdpOutput.ShowIpMsdpPolicyStatisticsSaPolicyIn
        outputs['show ip msdp policy statistics sa-policy 10.94.44.44 in'] = \
            MsdpOutput.ShowIpMsdpPolicyStatisticsSaPolicyInVRF1
        outputs['show ip msdp policy statistics sa-policy 10.4.1.1 out'] = \
            MsdpOutput.ShowIpMsdpPolicyStatisticsSaPolicyOut
        outputs['show ip msdp policy statistics sa-policy 10.94.44.44 out vrf VRF1'] = \
            MsdpOutput.ShowIpMsdpPolicyStatisticsSaPolicyOutVRF1
        outputs['show ip msdp summary'] = MsdpOutput.ShowIpMsdpSummary
        outputs['show ip msdp summary vrf VRF1'] = MsdpOutput.ShowIpMsdpSummaryVRF1
        outputs['show ip msdp sa-cache detail vrf all'] = MsdpOutput.showIpMsdpSaCacheDetailVrf
        outputs['show ip msdp peer vrf all'] = MsdpOutput.showIpMsdpPeerVrf

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.info['vrf']

if __name__ == '__main__':
    unittest.main()

