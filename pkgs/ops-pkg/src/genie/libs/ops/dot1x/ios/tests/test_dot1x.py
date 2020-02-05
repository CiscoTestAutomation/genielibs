# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.dot1x.ios.dot1x import Dot1X
from genie.libs.ops.dot1x.ios.tests.dot1x_output import Dot1xOutput

# Parser
from genie.libs.parser.ios.show_dot1x import ShowDot1xAllDetail, \
                                             ShowDot1xAllStatistics, \
                                             ShowDot1xAllSummary, \
                                             ShowDot1xAllCount


class test_dot1x(unittest.TestCase):

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
        dot1x = Dot1X(device=self.device)
        # Get outputs
        dot1x.maker.outputs[ShowDot1xAllDetail] = \
            {'': Dot1xOutput.ShowDot1xAllDetail}

        dot1x.maker.outputs[ShowDot1xAllStatistics] = \
            {'': Dot1xOutput.ShowDot1xAllStatistics}
            
        dot1x.maker.outputs[ShowDot1xAllSummary] = \
            {'': Dot1xOutput.ShowDot1xAllSummary}
            
        dot1x.maker.outputs[ShowDot1xAllCount] = \
            {'': Dot1xOutput.ShowDot1xAllCount}

        # Learn the feature
        dot1x.learn()

        # Verify Ops was created successfully
        self.assertEqual(dot1x.info, Dot1xOutput.Dot1x_info)

        # Check Selected Attributes
        self.assertEqual(dot1x.info['version'], 3)
        # info - mdot1x default
        self.assertEqual(dot1x.info['interfaces']['GigabitEthernet1/0/9']\
                                  ['max_start'], 3)

    def test_empty_output(self):
        self.maxDiff = None
        dot1x = Dot1X(device=self.device)

        dot1x.maker.outputs[ShowDot1xAllDetail] = \
            {'': {}}
            
        dot1x.maker.outputs[ShowDot1xAllStatistics] = \
            {'': {}}
            
        dot1x.maker.outputs[ShowDot1xAllSummary] = \
            {'': {}}
            
        dot1x.maker.outputs[ShowDot1xAllCount] = \
            {'': {}}

        # Learn the feature
        dot1x.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            dot1x.info['version']


    def test_incomplete_output(self):
        self.maxDiff = None
        
        dot1x = Dot1X(device=self.device)
        # Get outputs
        dot1x.maker.outputs[ShowDot1xAllDetail] = \
            {'': Dot1xOutput.ShowDot1xAllDetail}
            
        dot1x.maker.outputs[ShowDot1xAllStatistics] = \
            {'': Dot1xOutput.ShowDot1xAllStatistics}
            
        dot1x.maker.outputs[ShowDot1xAllSummary] = \
            {'': Dot1xOutput.ShowDot1xAllSummary}
            
        dot1x.maker.outputs[ShowDot1xAllCount] = \
            {'': {}}

        # Learn the feature
        dot1x.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(Dot1xOutput.Dot1x_info)
        del(expect_dict['sessions'])
                
        # Verify Ops was created successfully
        self.assertEqual(dot1x.info, expect_dict)


if __name__ == '__main__':
    unittest.main()
