# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock

# genie-libs
from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail
from genie.libs.ops.msdp.iosxr.msdp import Msdp
from genie.libs.ops.msdp.iosxr.tests.msdp_output import MsdpOutput

outputs = {}
outputs['show msdp peer'] = MsdpOutput.showMsdpPeer
outputs['show msdp vrf VRF1 peer'] = MsdpOutput.showMsdpVRFPeer
outputs['show msdp vrf VRF1 peer 10.4.1.1'] = MsdpOutput.showMsdpVRFPeerArg
outputs['show msdp context'] = MsdpOutput.showMsdpContext
outputs['show msdp vrf VRF1 context'] = MsdpOutput.showMsdpVRFContext
outputs['show msdp summary'] = MsdpOutput.showMsdpSummary
outputs['show msdp vrf VRF1 summary'] = MsdpOutput.showMsdpVRFSummary
outputs['show msdp sa-cache'] = MsdpOutput.showMsdpSaCache
outputs['show msdp vrf VRF1 sa-cache'] = MsdpOutput.showMsdpVRFSaCache
outputs['show msdp statistics peer'] = MsdpOutput.showMsdpStatisticsPeer
outputs['show msdp vrf VRF1 statistics peer 10.4.1.1'] = MsdpOutput.showMsdpVRFStatisticsPeerArg
outputs['show msdp vrf VRF1 statistics peer'] = MsdpOutput.showMsdpVRFStatisticsPeer

def mapper(key):
    return outputs[key]


class TestMsdp(unittest.TestCase):
    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        # Give the device as as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    # support vrf = 'VRF1'
    def test_output_vrf1(self):
        self.maxDiff = None
        msdp = Msdp(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        msdp.learn(vrf='VRF1')

        # Verify Ops was created successfully
        self.assertEqual(msdp.info, MsdpOutput.showMsdpVrfOpsOutput)

    # support vrf = 'default'
    def test_output_vrf_default(self):
        self.maxDiff = None
        msdp = Msdp(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        msdp.learn(vrf='default')

        # Verify Ops was created successfully
        self.assertEqual(msdp.info, MsdpOutput.showMsdpVrfDefaultOutput)

    # support vrf both default and valued
    def test_complete_output_3(self):
        self.maxDiff = None
        msdp = Msdp(device=self.device)

        # Get outputs
        msdp.maker.outputs[ShowVrfAllDetail] = \
            {'': MsdpOutput.showVrfAllDetail}
        msdp.maker.outputs['show msdp peer'] = {"{'vrf':''}": MsdpOutput.showMsdpPeer}
        msdp.maker.outputs['show msdp statistics peer'] = {"{'vrf':''}": MsdpOutput.showMsdpStatisticsPeer}
        msdp.maker.outputs['show msdp sa-cache'] = {"{'vrf':''}": MsdpOutput.showMsdpSaCache}
        msdp.maker.outputs['show msdp summary'] = {"{'vrf':''}": MsdpOutput.showMsdpSummary}
        msdp.maker.outputs['show msdp context'] = {"{'vrf':''}": MsdpOutput.showMsdpContext}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        msdp.learn()

        # Verify Ops was created successfully
        self.assertEqual(msdp.info, MsdpOutput.showMsdpVrfLoopsOutput)

    # support vrf = 'VRF1' peer = '10.4.1.1'
    def test_output_vrf1_peer(self):
        self.maxDiff = None
        msdp = Msdp(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        msdp.learn(vrf='VRF1', peer='10.4.1.1')

        # Verify Ops was created successfully
        self.assertEqual(msdp.info, MsdpOutput.showMsdpVrf1PeerArgOutput)


    def test_selective_attribute(self):
        self.maxDiff = None
        msdp = Msdp(device=self.device)

        msdp.maker.outputs[ShowVrfAllDetail] = \
            {'': {}}

        # Set outputs
        msdp.maker.outputs['show msdp peer'] = {'': MsdpOutput.showMsdpPeer}
        msdp.maker.outputs['show msdp sa-cache'] = {'': MsdpOutput.showMsdpSaCache}
        msdp.maker.outputs['show msdp context'] = {'': MsdpOutput.showMsdpContext}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        msdp.learn()

        self.assertEqual(65109, msdp.info['vrf']['default'] \
            ['peer']['192.168.229.3']['peer_as'])

    def test_empty_output(self):
        self.maxDiff = None
        msdp = Msdp(device=self.device)

        msdp.maker.outputs[ShowVrfAllDetail] = \
            {'': {}}

        self.device.execute = Mock()

        # Set outputs
        outputs['show msdp peer'] = ''
        outputs['show msdp vrf VRF1 peer'] = ''
        outputs['show msdp context'] = ''
        outputs['show msdp vrf VRF1 context'] = ''
        outputs['show msdp summary'] = ''
        outputs['show msdp vrf VRF1 summary'] = ''
        outputs['show msdp sa-cache'] = ''
        outputs['show msdp vrf VRF1 sa-cache'] = ''
        outputs['show msdp statistics peer'] = ''
        outputs['show msdp vrf VRF1 statistics peer'] = ''

        self.device.execute.side_effect = mapper
        # Learn the feature
        msdp.learn()

        outputs['show msdp peer'] = MsdpOutput.showMsdpPeer
        outputs['show msdp vrf VRF1 peer'] = MsdpOutput.showMsdpVRFPeer
        outputs['show msdp context'] = MsdpOutput.showMsdpContext
        outputs['show msdp vrf VRF1 context'] = MsdpOutput.showMsdpVRFContext
        outputs['show msdp summary'] = MsdpOutput.showMsdpSummary
        outputs['show msdp vrf VRF1 summary'] = MsdpOutput.showMsdpVRFSummary
        outputs['show msdp sa-cache'] = MsdpOutput.showMsdpSaCache
        outputs['show msdp vrf VRF1 sa-cache'] = MsdpOutput.showMsdpVRFSaCache
        outputs['show msdp statistics peer'] = MsdpOutput.showMsdpStatisticsPeer
        outputs['show msdp vrf VRF1 statistics peer'] = MsdpOutput.showMsdpVRFStatisticsPeer

        with self.assertRaises(AttributeError):
            msdp.info['vrf']

    def test_missing_attributes(self):
        self.maxDiff = None
        msdp = Msdp(device=self.device)

        msdp.maker.outputs[ShowVrfAllDetail] = \
            {'': {}}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        msdp.learn()

        with self.assertRaises(KeyError):
            description = msdp.info['description']


if __name__ == '__main__':
    unittest.main()

