# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.stp.iosxr.stp import Stp
from genie.libs.ops.stp.iosxr.tests.stp_output import StpOutput

# Parser
from genie.libs.parser.iosxr.show_spanning_tree import ShowSpanningTreeMst, \
                                        ShowSpanningTreeMstag, \
                                        ShowSpanningTreePvrst, \
                                        ShowSpanningTreePvrsTag, \
                                        ShowSpanningTreePvsTag

outputs = {}
outputs.update({'show spanning-tree mst test': StpOutput.ShowSpanningTreeMst_output})
outputs.update({'show spanning-tree mstag risc': StpOutput.ShowSpanningTreeMstag_output})
outputs.update({'show spanning-tree pvrst a': StpOutput.ShowSpanningTreePvrst_output})
outputs.update({'show spanning-tree pvrstag foo': StpOutput.ShowSpanningTreePvrsTag_output})
outputs.update({'show spanning-tree pvstag foo': StpOutput.ShowSpanningTreePvsTag_output})


def mapper(key):
    return outputs[key]

class test_stp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device
        

    def test_complete_output(self):
        stp = Stp(device=self.device)
        # Get outputs
        stp.maker.outputs[ShowSpanningTreeMst] = \
            {'': StpOutput.ShowSpanningTreeMst}

        stp.maker.outputs[ShowSpanningTreeMstag] = \
            {'': StpOutput.ShowSpanningTreeMstag}

        stp.maker.outputs[ShowSpanningTreePvrst] = \
            {'': StpOutput.ShowSpanningTreePvrst}

        stp.maker.outputs[ShowSpanningTreePvrsTag] = \
            {'': StpOutput.ShowSpanningTreePvrsTag}

        stp.maker.outputs[ShowSpanningTreePvsTag] = \
            {'': StpOutput.ShowSpanningTreePvsTag}
        
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        stp.learn(mst_domain='test', mstag_domain='risc', pvst_id='a', pvrstag_domain='foo', pvstag_domain='foo')
        self.maxDiff = None
        # Verify Ops was created successfully
        self.assertEqual(stp.info, StpOutput.stpOutput)
        
        # Check Selected Attributes
        self.assertEqual(stp.info['mstp']['test']['mst_instances']['0']['vlan'],
            '1-4094')


    def test_empty_output(self):
        self.maxDiff = None
        stp = Stp(device=self.device)

        stp.maker.outputs[ShowSpanningTreeMst] = \
            {'': {}}

        stp.maker.outputs[ShowSpanningTreeMstag] = \
            {'': {}}

        stp.maker.outputs[ShowSpanningTreePvrst] = \
            {'': {}}

        stp.maker.outputs[ShowSpanningTreePvrsTag] = \
            {'': {}}

        stp.maker.outputs[ShowSpanningTreePvsTag] = \
            {'': {}}


        outputs.update({'show spanning-tree mst test': ''})
        outputs.update({'show spanning-tree mstag risc': ''})
        outputs.update({'show spanning-tree pvrst a': ''})
        outputs.update({'show spanning-tree pvrstag foo': ''})
        outputs.update({'show spanning-tree pvstag foo': ''})
        
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        
        # Learn the feature
        stp.learn(mst_domain='test', mstag_domain='risc', pvst_id='a', pvrstag_domain='foo', pvstag_domain='foo')

        outputs.update({'show spanning-tree mst test': StpOutput.ShowSpanningTreeMst_output})
        outputs.update({'show spanning-tree mstag risc': StpOutput.ShowSpanningTreeMstag_output})
        outputs.update({'show spanning-tree pvrst a': StpOutput.ShowSpanningTreePvrst_output})
        outputs.update({'show spanning-tree pvrstag foo': StpOutput.ShowSpanningTreePvrsTag_output})
        outputs.update({'show spanning-tree pvstag foo': StpOutput.ShowSpanningTreePvsTag_output})
        
        # Check no attribute not found
        with self.assertRaises(AttributeError):
            stp.info['mstp']['test']['mst_instances']['0']['vlan']

    def test_incomplete_output(self):
        self.maxDiff = None
        
        stp = Stp(device=self.device)

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Get outputs
        stp.maker.outputs[ShowSpanningTreeMst] = \
            {'': StpOutput.ShowSpanningTreeMst}

        stp.maker.outputs[ShowSpanningTreeMstag] = \
            {'': StpOutput.ShowSpanningTreeMstag}

        stp.maker.outputs[ShowSpanningTreePvrst] = \
            {'': StpOutput.ShowSpanningTreePvrst}

        stp.maker.outputs[ShowSpanningTreePvrsTag] = \
            {'': StpOutput.ShowSpanningTreePvrsTag}

        stp.maker.outputs[ShowSpanningTreePvsTag] = \
            {'': StpOutput.ShowSpanningTreePvsTag}

        # Learn the feature
        stp.learn(mst_domain='test', mstag_domain='risc', pvst_id='a', pvrstag_domain='foo', pvstag_domain='foo')
        
        # delete keys from input
        del(stp.info['mstp']['test']['mst_instances']['0']['mst_id'])
        
        # Delete missing specific attribute values
        expect_dict = deepcopy(StpOutput.stpOutput)
        del(expect_dict['mstp']['test']['mst_instances']['0']['mst_id'])  

        # Verify Ops was created successfully
        self.assertEqual(stp.info, expect_dict)

if __name__ == '__main__':
    unittest.main()
