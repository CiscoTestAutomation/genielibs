# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock

# genie.libs
from genie.libs.ops.isis.ios.isis import Isis
from genie.libs.ops.isis.ios.tests.isis_output import IsisOutput

from genie.libs.parser.iosxe.show_isis import (ShowIsisLspLog,
                                               ShowIsisHostname,
                                               ShowRunSectionIsis,
                                               ShowIsisDatabaseDetail)

from genie.libs.parser.iosxe.show_clns import (ShowClnsTraffic,
                                               ShowClnsProtocol,
                                               ShowClnsInterface,
                                               ShowClnsNeighborsDetail,
                                               ShowClnsIsNeighborsDetail)

outputs = {}
outputs['show isis hostname'] = IsisOutput.showIsisHostname
outputs['show isis lsp-log'] = IsisOutput.showIsisLspLog
outputs['show isis database detail'] = IsisOutput.showIsisDatabaseDetail
outputs['show clns interface'] = IsisOutput.showClnsInterface
outputs['show clns protocol'] = IsisOutput.showClnsProtocol
outputs['show clns neighbors detail'] = IsisOutput.showClnsNeighborsDetail
outputs['show clns is-neighbors detail'] = IsisOutput.showClnsIsNeighborsDetail
outputs['show clns traffic'] = IsisOutput.showClnsTraffic

def mapper(key):
    return outputs[key]

class TestIsisAll(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'ios'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_full_isis(self):
        f = Isis(device=self.device)

        f.maker.outputs[ShowRunSectionIsis] = {'': IsisOutput.showRunSectionIsis}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        f.learn()
        self.maxDiff = None
        self.assertEqual(f.info, IsisOutput.isisOpsOutput)
        self.assertEqual(f.lsdb, IsisOutput.isisLsdbOpsOutput)

    def test_selective_attribute_isis(self):
        f = Isis(device=self.device)
        f.maker.outputs[ShowRunSectionIsis] = {'': IsisOutput.showRunSectionIsis}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        f.learn()

        # Check match
        self.assertEqual('R1_xe', f.info['instance']['test1']['vrf']['VRF1'] \
                ["hostname_db"]["hostname"]["1111.1111.1111"]["hostname"])
        self.assertEqual('0x00000161', f.lsdb['instance']['test1']['vrf']['VRF1'] \
            ["level_db"][2]["R1_xe.00-00"]["sequence"])

        # Check does not match
        self.assertNotEqual('R1_xe', f.info['instance']['test']['vrf']['default'] \
                ["hostname_db"]["hostname"]["2222.2222.2222"]["hostname"])
        self.assertNotEqual('0x00000885', f.lsdb['instance']['test']['vrf']['default'] \
            ["level_db"][1]["R1_xe.00-00"]["sequence"])

    def test_missing_attributes_Isis(self):
        f = Isis(device=self.device)
        f.maker.outputs[ShowRunSectionIsis] = {'': IsisOutput.showRunSectionIsis}

        # Get 'show ip static route' output
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            metric = f.info['instance']['VRF1']['vrf']['VRF1'] \
                ["hostname_db"]["hostname"]["2222.2222.2222"]['metric']
            metric = f.lsdb['instance']['VRF1']['vrf']['VRF1'] \
                        ["level_db"]["L2"]["R7.00-00"]['metric']

    def test_empty_output_Isis(self):
        self.maxDiff = None
        f = Isis(device=self.device)
        # Get outputs

        f.maker.outputs[ShowRunSectionIsis] = {'': {}}

        outputs['show isis hostname'] = {'': {}}
        outputs['show isis lsp-log'] = {'': {}}
        outputs['show isis database detail'] = {'': {}}
        outputs['show clns interface'] = {'': {}}
        outputs['show clns protocol'] = {'': {}}
        outputs['show clns neighbors detail'] = {'': {}}
        outputs['show clns is-neighbors detail'] = {'': {}}
        outputs['show clns traffic'] = {'': {}}
        # Return outputs above as inputs to parser when called

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        f.learn()

        # revert back
        outputs['show isis hostname'] = IsisOutput.showIsisHostname
        outputs['show isis lsp-log'] = IsisOutput.showIsisLspLog
        outputs['show isis database detail'] = IsisOutput.showIsisDatabaseDetail
        outputs['show clns interface'] = IsisOutput.showClnsInterface
        outputs['show clns protocol'] = IsisOutput.showClnsProtocol
        outputs['show clns neighbors detail'] = IsisOutput.showClnsNeighborsDetail
        outputs['show clns is-neighbors detail'] = IsisOutput.showClnsIsNeighborsDetail
        outputs['show clns traffic'] = IsisOutput.showClnsTraffic

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.info['instance']
            f.lsdb['instance']

if __name__ == '__main__':
    unittest.main()
