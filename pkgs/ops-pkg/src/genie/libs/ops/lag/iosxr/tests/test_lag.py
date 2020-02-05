# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.lag.iosxr.lag import Lag
from genie.libs.ops.lag.iosxr.tests.lag_output import LagOutput

# Parser
from genie.libs.parser.iosxr.show_lag import ShowLacpSystemId, \
                                             ShowBundle, \
                                             ShowLacp

class test_lag(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_full_lag(self):
        self.maxDiff = None
        lag = Lag(device=self.device)
        # Get outputs
        lag.maker.outputs[ShowLacpSystemId] = {'': LagOutput.ShowLacpSystemId}
        lag.maker.outputs[ShowBundle] = {'': LagOutput.ShowBundle}
        lag.maker.outputs[ShowLacp] = {'': LagOutput.ShowLacp}

        # Learn the feature
        lag.learn()

        # Verify Ops was created successfully
        self.assertEqual(lag.info, LagOutput.LagOpsOutput)

    def test_selective_attribute_lag(self):
        lag = Lag(device=self.device)
        # Get outputs
        lag.maker.outputs[ShowLacpSystemId] = {'': LagOutput.ShowLacpSystemId}
        lag.maker.outputs[ShowBundle] = {'': LagOutput.ShowBundle}
        lag.maker.outputs[ShowLacp] = {'': LagOutput.ShowLacp}

        # Learn the feature
        lag.learn()

        # Check match
        self.assertEqual('out_sync', lag.info['interfaces']['Bundle-Ether2']['members']
                         ['GigabitEthernet0/0/0/2']['synchronization'])

        # Check does not match
        self.assertNotEqual(2, lag.info['interfaces']['Bundle-Ether1']['lacp_max_bundle'])

    def test_missing_attributes_lag(self):
        lag = Lag(device=self.device)
        # Get outputs
        lag.maker.outputs[ShowLacpSystemId] = {'': {}}
        lag.maker.outputs[ShowBundle] = {'': LagOutput.ShowBundle}
        lag.maker.outputs[ShowLacp] = {'': LagOutput.ShowLacp}

        # Learn the feature
        lag.learn()

        with self.assertRaises(KeyError):
            system_priority = lag.info['system_priority']

    def test_only_system_id(self):
        lag = Lag(device=self.device)
        # Get outputs
        lag.maker.outputs[ShowLacpSystemId] = {'': LagOutput.ShowLacpSystemId}
        lag.maker.outputs[ShowBundle] = {'': {}}
        lag.maker.outputs[ShowLacp] = {'': {}}

        # Learn the feature
        lag.learn()

        self.assertIn("system_priority", lag.info)

    def test_empty_output_lag(self):
        self.maxDiff = None
        lag = Lag(device=self.device)

        lag.maker.outputs[ShowLacpSystemId] = {'': {}}
        lag.maker.outputs[ShowBundle] = {'': {}}
        lag.maker.outputs[ShowLacp] = {'': {}}

        # Learn the feature
        lag.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            lag.info['system_priority']


if __name__ == '__main__':
    unittest.main()
