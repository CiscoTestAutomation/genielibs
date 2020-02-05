# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock

# genie.libs
from genie.libs.ops.isis.iosxr.isis import Isis
from genie.libs.ops.isis.iosxr.tests.isis_output import IsisOutput

# iosxr parsers
from genie.libs.parser.iosxr.show_isis import (ShowIsis,
                                               ShowIsisSpfLog,
                                               ShowIsisLspLog,
                                               ShowIsisHostname,
                                               ShowIsisAdjacency,
                                               ShowIsisInterface,
                                               ShowIsisStatistics,
                                               ShowIsisDatabaseDetail)

outputs = {}
outputs['show isis'] = IsisOutput.showIsis
outputs['show isis spf-log'] = IsisOutput.showIsisSpfLog
outputs['show isis lsp-log'] = IsisOutput.showIsisLspLog
outputs['show isis hostname'] = IsisOutput.showIsisHostname
outputs['show isis adjacency'] = IsisOutput.showIsisAdjacency
outputs['show isis interface'] = IsisOutput.showIsisInterface
outputs['show isis statistics'] = IsisOutput.showIsisStatistics
outputs['show isis database detail'] = IsisOutput.showIsisDatabaseDetail

def mapper(key):
    return outputs[key]

class TestIsisAll(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_full_isis(self):
        isis = Isis(device=self.device)
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        isis.learn()

        self.maxDiff = None
        self.assertEqual(isis.info, IsisOutput.isisOpsOutput)
        self.assertEqual(isis.lsdb, IsisOutput.isisLsdbOpsOutput)

    def test_selective_attribute_isis(self):
        isis = Isis(device=self.device)
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        isis.learn()

        # Check match
        self.assertEqual('R3', isis.info['instance']['test']['vrf']['default']
            ["hostname_db"]["hostname"]["3333.3333.3333"]["hostname"])
        self.assertEqual('R3', isis.lsdb['instance']['test']['vrf']['default']
            ["level_db"][1]["R3.00-00"]["dynamic_hostname"])

        # Check does not match
        self.assertNotEqual('R7', isis.info['instance']['test']['vrf']['default']
            ["hostname_db"]["hostname"]["4444.4444.4444"]["hostname"])
        self.assertNotEqual('R5', isis.lsdb['instance']['test']['vrf']['default']
            ["level_db"][1]["R4.00-00"]["dynamic_hostname"])

    def test_missing_attributes_Isis(self):
        isis = Isis(device=self.device)

        outputs['show isis hostname'] = ''
        outputs['show isis database detail'] = ''
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        isis.learn()

        # revert back
        outputs['show isis hostname'] = IsisOutput.showIsisHostname
        outputs['show isis database detail'] = IsisOutput.showIsisDatabaseDetail

        with self.assertRaises(KeyError):
            metric = isis.info['instance']['test']['vrf']['default']["hostname_db"]
            metric = isis.lsdb['instance']['test']

    def test_empty_output_Isis(self):
        isis = Isis(device=self.device)

        # Return outputs as inputs to parser when called
        outputs['show isis'] = ''
        outputs['show isis spf-log'] = ''
        outputs['show isis lsp-log'] = ''
        outputs['show isis hostname'] = ''
        outputs['show isis adjacency'] = ''
        outputs['show isis interface'] = ''
        outputs['show isis statistics'] = ''
        outputs['show isis database detail'] = ''

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        isis.learn()

        # revert back
        outputs['show isis'] = IsisOutput.showIsis
        outputs['show isis spf-log'] = IsisOutput.showIsisSpfLog
        outputs['show isis lsp-log'] = IsisOutput.showIsisLspLog
        outputs['show isis hostname'] = IsisOutput.showIsisHostname
        outputs['show isis adjacency'] = IsisOutput.showIsisAdjacency
        outputs['show isis interface'] = IsisOutput.showIsisInterface
        outputs['show isis statistics'] = IsisOutput.showIsisStatistics
        outputs['show isis database detail'] = IsisOutput.showIsisDatabaseDetail

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            isis.info['instance']
            isis.lsdb['instance']

if __name__ == '__main__':
    unittest.main()
