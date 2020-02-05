# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.ntp.nxos.ntp import Ntp
from genie.libs.ops.ntp.nxos.tests.ntp_output import NtpOutput, NtpOutputNoConfig

# Parser
from genie.libs.parser.nxos.show_ntp import ShowNtpPeerStatus, \
                                            ShowNtpPeers


# Set values
outputs = {}
outputs['show ntp peers'] = NtpOutputNoConfig.ShowNtpPeers
outputs['show ntp peer-status'] = NtpOutputNoConfig.ShowNtpPeerStatus


def mapper(key):
    return outputs[key]

class test_ntp(unittest.TestCase):

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
        ntp = Ntp(device=self.device)
        # Get outputs
        ntp.maker.outputs[ShowNtpPeerStatus] = \
            {"": NtpOutput.ShowNtpPeerStatus}

        ntp.maker.outputs[ShowNtpPeers] = \
            {"": NtpOutput.ShowNtpPeers}

        # Learn the feature
        ntp.learn()

        # Verify Ops was created successfully
        self.assertEqual(ntp.info, NtpOutput.Ntp_info)

        # Check specific attribute values
        # info - default vrf
        self.assertEqual(ntp.info['clock_state']['system_status']['clock_state'], 'synchronized')
        # info - vrf VRF1
        self.assertEqual(ntp.info['vrf']['default']['unicast_configuration']['address']\
                                 ['10.16.2.2']['type']['server']['type'], 'server')

    def test_output_with_attribute(self):
        self.maxDiff = None
        ntp = Ntp(device=self.device,
                  attributes=['info[associations][(.*)]',
                              'info[unicast_configuration][(.*)]'])
        # Get outputs
        ntp.maker.outputs[ShowNtpPeerStatus] = \
            {"": NtpOutput.ShowNtpPeerStatus}

        ntp.maker.outputs[ShowNtpPeers] = \
            {"": NtpOutput.ShowNtpPeers}

        # Learn the feature
        ntp.learn()

        # Check no attribute not found
        with self.assertRaises(KeyError):
            ntp.info['clock_state']

        # info - unicast_configuration
        self.assertEqual(ntp.info['vrf'], NtpOutput.Ntp_info['vrf'])

    def test_empty_output(self):
        self.maxDiff = None
        ntp = Ntp(device=self.device)
        # Get outputs
        ntp.maker.outputs[ShowNtpPeerStatus] = \
            {"": {}}

        ntp.maker.outputs[ShowNtpPeers] = \
            {"": {}}

        # Learn the feature
        ntp.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            ntp.info['clock_state']

    def test_incomplete_output(self):
        self.maxDiff = None
        
        ntp = Ntp(device=self.device)

        # Get outputs
        ntp.maker.outputs[ShowNtpPeerStatus] = \
            {"": NtpOutput.ShowNtpPeerStatus}

        ntp.maker.outputs[ShowNtpPeers] = \
            {"": {}}

        # Learn the feature
        ntp.learn()
                
        # Check no attribute not found
        with self.assertRaises(KeyError):
            ntp.info['unicast_configuration']


class test_ntp_without_peer_configuration(unittest.TestCase):
    '''only has 'ntp master 3' configured on device'''

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
        ntp = Ntp(device=self.device)
        
        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        ntp.learn()

        # Verify Ops was created successfully
        # no associtaion attribtues since there is only one synch
        # server which shouldn't go to association
        self.assertEqual(ntp.info, NtpOutputNoConfig.Ntp_info)

        # Check specific attribute values
        # info - default vrf
        self.assertEqual(ntp.info['clock_state']['system_status']['associations_address'], '127.127.1.0')
        # info - vrf default
        self.assertEqual(ntp.info['vrf']['default']['unicast_configuration']['address']\
                                 ['127.127.1.0']['type']['server']['type'], 'server')

if __name__ == '__main__':
    unittest.main()
