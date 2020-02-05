# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.stp.iosxe.stp import Stp
from genie.libs.ops.stp.iosxe.tests.spanning_tree_output import StpMstOutput, \
                                                                StpRpstOutput

# Parser
from genie.libs.parser.iosxe.show_spanning_tree import ShowSpanningTreeDetail, \
                                    ShowSpanningTreeMstDetail, \
                                    ShowSpanningTreeSummary, \
                                    ShowErrdisableRecovery, \
                                    ShowSpanningTree, \
                                    ShowSpanningTreeMstConfiguration



class test_stp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_mst_output(self):
        self.maxDiff = None
        stp = Stp(device=self.device)
        # Get outputs
        stp.maker.outputs[ShowSpanningTreeDetail] = \
            {'': StpMstOutput.ShowSpanningTreeDetail}

        stp.maker.outputs[ShowSpanningTreeMstDetail] = \
            {'': StpMstOutput.ShowSpanningTreeMstDetail}

        stp.maker.outputs[ShowSpanningTreeSummary] = \
            {'': StpMstOutput.ShowSpanningTreeSummary}

        stp.maker.outputs[ShowErrdisableRecovery] = \
            {'': StpMstOutput.ShowErrdisableRecovery}
            
        stp.maker.outputs[ShowSpanningTree] = \
            {'': StpMstOutput.ShowSpanningTree}
            
        stp.maker.outputs[ShowSpanningTreeMstConfiguration] = \
            {'': StpMstOutput.ShowSpanningTreeMstConfiguration}

        # Learn the feature
        stp.learn()

        # Verify Ops was created successfully
        self.assertEqual(stp.info, StpMstOutput.Stp_info)

        # Check Selected Attributes
        # info - global bpdu_filter
        self.assertEqual(stp.info['global']['bpdu_filter'], False)
        # info - mstp default
        self.assertEqual(stp.info['mstp']['default']['mst_instances']\
                                  [0]['root_port'], 5)

    def test_empty_output(self):
        self.maxDiff = None
        stp = Stp(device=self.device)

        stp.maker.outputs[ShowSpanningTreeDetail] = \
            {'': {}}

        stp.maker.outputs[ShowSpanningTreeMstDetail] = \
            {'': {}}

        stp.maker.outputs[ShowSpanningTreeSummary] = \
            {'': {}}

        stp.maker.outputs[ShowErrdisableRecovery] = \
            {'': {}}
            
        stp.maker.outputs[ShowSpanningTree] = \
            {'': {}}
            
        stp.maker.outputs[ShowSpanningTreeMstConfiguration] = \
            {'': {}}

        # Learn the feature
        stp.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            stp.info['mstp']


    def test_incomplete_output(self):
        self.maxDiff = None
        
        stp = Stp(device=self.device)
        # Get outputs
        stp.maker.outputs[ShowSpanningTreeDetail] = \
            {'': StpMstOutput.ShowSpanningTreeDetail}

        stp.maker.outputs[ShowSpanningTreeMstDetail] = \
            {'': StpMstOutput.ShowSpanningTreeMstDetail}

        stp.maker.outputs[ShowSpanningTreeSummary] = \
            {'': StpMstOutput.ShowSpanningTreeSummary}

        stp.maker.outputs[ShowErrdisableRecovery] = \
            {'': {}}
            
        stp.maker.outputs[ShowSpanningTree] = \
            {'': StpMstOutput.ShowSpanningTree}
            
        stp.maker.outputs[ShowSpanningTreeMstConfiguration] = \
            {'': StpMstOutput.ShowSpanningTreeMstConfiguration}

        # Learn the feature
        stp.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(StpMstOutput.Stp_info)
        del(expect_dict['global']['bpduguard_timeout_recovery'])
                
        # Verify Ops was created successfully
        self.assertEqual(stp.info, expect_dict)

    def test_complete_rpst_output(self):
        self.maxDiff = None
        stp = Stp(device=self.device)
        # Get outputs
        stp.maker.outputs[ShowSpanningTreeDetail] = \
            {'': StpRpstOutput.ShowSpanningTreeDetail}

        stp.maker.outputs[ShowSpanningTreeSummary] = \
            {'': StpRpstOutput.ShowSpanningTreeSummary}

        stp.maker.outputs[ShowErrdisableRecovery] = \
            {'': StpRpstOutput.ShowErrdisableRecovery}
            
        stp.maker.outputs[ShowSpanningTree] = \
            {'': StpRpstOutput.ShowSpanningTree}
            
        stp.maker.outputs[ShowSpanningTreeMstConfiguration] = \
            {'': {}}

        stp.maker.outputs[ShowSpanningTreeMstDetail] = \
            {'': {}}

        # Learn the feature
        stp.learn()

        # Verify Ops was created successfully
        self.assertEqual(stp.info, StpRpstOutput.Stp_info)


if __name__ == '__main__':
    unittest.main()
