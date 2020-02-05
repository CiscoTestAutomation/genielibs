# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.lag.ios.lag import Lag
from genie.libs.ops.lag.ios.tests.lag_output import LagOutput

# Parser
from genie.libs.parser.ios.show_lag import ShowLacpSysId, \
                                           ShowLacpCounters, \
                                           ShowEtherchannelSummary,\
                                           ShowLacpInternal,\
                                           ShowLacpNeighbor,\
                                           ShowPagpCounters, \
                                           ShowPagpNeighbor,\
                                           ShowPagpInternal


class test_lag(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'ios'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        lag = Lag(device=self.device)
        # Get outputs
        lag.maker.outputs[ShowLacpSysId] = \
            {'': LagOutput.ShowLacpSysId}

        lag.maker.outputs[ShowLacpCounters] = \
            {'': LagOutput.ShowLacpCounters}

        lag.maker.outputs[ShowEtherchannelSummary] = \
            {'': LagOutput.ShowEtherchannelSummary}

        lag.maker.outputs[ShowLacpNeighbor] = \
            {'': LagOutput.ShowLacpNeighbor}

        lag.maker.outputs[ShowPagpCounters] = \
            {'': LagOutput.ShowPagpCounters}

        lag.maker.outputs[ShowPagpNeighbor] = \
            {'': LagOutput.ShowPagpNeighbor}

        lag.maker.outputs[ShowPagpInternal] = \
            {'': LagOutput.ShowPagpInternal}


        # Learn the feature
        lag.learn()

        # Verify Ops was created successfully
        self.assertEqual(lag.info, LagOutput.Lag_info)

        # Check Selected Attributes
        self.assertEqual(lag.info['system_priority'], 32768)
        # info - mlag default
        self.assertEqual(lag.info['interfaces']['Port-channel1']\
                                  ['bundle_id'], 1)

    def test_empty_output(self):
        self.maxDiff = None
        lag = Lag(device=self.device)

        lag.maker.outputs[ShowLacpSysId] = \
            {'': {}}

        lag.maker.outputs[ShowLacpCounters] = \
            {'': {}}

        lag.maker.outputs[ShowEtherchannelSummary] = \
            {'': {}}

        lag.maker.outputs[ShowLacpNeighbor] = \
            {'': {}}

        lag.maker.outputs[ShowPagpCounters] = \
            {'': {}}

        lag.maker.outputs[ShowPagpNeighbor] = \
            {'': {}}
            
        lag.maker.outputs[ShowPagpInternal] = \
            {'': {}}

        # Learn the feature
        lag.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            lag.info['system_priority']


    def test_incomplete_output(self):
        self.maxDiff = None
        
        lag = Lag(device=self.device)
        # Get outputs
        lag.maker.outputs[ShowLacpSysId] = \
            {'': LagOutput.ShowLacpSysId}

        lag.maker.outputs[ShowLacpCounters] = \
            {'': LagOutput.ShowLacpCounters}

        lag.maker.outputs[ShowEtherchannelSummary] = \
            {'': LagOutput.ShowEtherchannelSummary}

        lag.maker.outputs[ShowLacpNeighbor] = \
            {'': LagOutput.ShowLacpNeighbor}

        lag.maker.outputs[ShowPagpCounters] = \
            {'': LagOutput.ShowPagpCounters}

        lag.maker.outputs[ShowPagpNeighbor] = \
            {'': LagOutput.ShowPagpNeighbor}
            
        lag.maker.outputs[ShowPagpInternal] = \
            {'': {}}

        # Learn the feature
        lag.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(LagOutput.Lag_info)
        del(expect_dict['interfaces']['Port-channel2']['members']['GigabitEthernet1/1'])
        del(expect_dict['interfaces']['Port-channel2']['members']['GigabitEthernet1/0'])
        del(expect_dict['interfaces']['Port-channel2']['members']['GigabitEthernet0/3'])
        del(expect_dict['interfaces']['Port-channel1']['members']['GigabitEthernet0/2'])
        del(expect_dict['interfaces']['Port-channel1']['members']['GigabitEthernet0/1'])

        # Verify Ops was created successfully
        self.assertEqual(lag.info, expect_dict)


if __name__ == '__main__':
    unittest.main()