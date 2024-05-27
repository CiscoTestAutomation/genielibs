# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.msdp.ios.msdp import Msdp
from genie.libs.ops.msdp.ios.tests.msdp_output import MsdpOutput

# ios show msdp
from genie.libs.parser.iosxe.show_msdp import (ShowIpMsdpPeer,
                                             ShowIpMsdpSaCache)

outputs = {}
outputs['show ip msdp peer'] = MsdpOutput.ShowIpMsdpPeer_golden
outputs['show ip msdp sa-cache'] = MsdpOutput.ShowIpMsdpSaCache_golden

def mapper(key, **kwargs):
    return outputs[key]

class test_msdp(unittest.TestCase):
    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'ios'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Create a mock connection to get output for parsing
        self.device_connection = Mock(device=self.device)
        self.device.connectionmgr.connections['cli'] = self.device_connection
        # Set outputs
        self.device_connection.execute.side_effect = mapper

    def test_complete_output(self):
        self.maxDiff = None
        msdp = Msdp(device=self.device)

        # Set outputs
        msdp.maker.outputs[ShowIpMsdpPeer] = {'': MsdpOutput.ShowIpMsdpPeer}
        msdp.maker.outputs[ShowIpMsdpSaCache] = {'': MsdpOutput.ShowIpMsdpSaCache}

        # Return outputs above as inputs to parser when called


        # Learn the feature
        msdp.learn()

        # Verify Ops was created successfully
        self.assertEqual(msdp.info, MsdpOutput.MsdpInfo)

    def test_selective_attribute(self):
        self.maxDiff = None
        msdp = Msdp(device=self.device)

        # Set outputs
        msdp.maker.outputs[ShowIpMsdpPeer] = {'': MsdpOutput.ShowIpMsdpPeer}
        msdp.maker.outputs[ShowIpMsdpSaCache] = {'': MsdpOutput.ShowIpMsdpSaCache}

        # Return outputs above as inputs to parser when called


        # Learn the feature
        msdp.learn()

        self.assertEqual('Loopback0', msdp.info['vrf']['default']\
                        ['peer']['10.16.2.2']['connect_source'])

    def test_empty_output(self):
        self.maxDiff = None
        msdp = Msdp(device=self.device)

        # Set outputs
        msdp.maker.outputs[ShowIpMsdpPeer] = {'': ''}
        msdp.maker.outputs[ShowIpMsdpSaCache] = {'': ''}

        # Return outputs above as inputs to parser when called


        # Learn the feature
        msdp.learn()

        with self.assertRaises(AttributeError):
            msdp.info['vrf']

    def test_missing_attributes(self):
        self.maxDiff = None
        msdp = Msdp(device=self.device)

        # Set outputs
        msdp.maker.outputs[ShowIpMsdpPeer] = {'':  MsdpOutput.ShowIpMsdpPeer}
        msdp.maker.outputs[ShowIpMsdpSaCache] = {'': {}}

        # Return outputs above as inputs to parser when called


        # Learn the feature
        msdp.learn()

        with self.assertRaises(KeyError):
            msdp.info['vrf']['default']['sa_cache']


if __name__ == '__main__':
    unittest.main()
