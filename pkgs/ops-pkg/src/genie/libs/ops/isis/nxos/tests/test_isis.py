# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock

# genie.libs
from genie.libs.ops.isis.nxos.isis import Isis
from genie.libs.ops.isis.nxos.tests.isis_output import IsisOutput

from genie.libs.parser.nxos.show_isis import (ShowIsis,
                                              ShowIsisHostname,
                                              ShowIsisAdjacency,
                                              ShowIsisInterface,
                                              ShowIsisDatabaseDetail,
                                              ShowIsisHostnameDetail)
outputs = {}
outputs['show isis vrf all'] = IsisOutput.showIsisVrfAll
outputs['show isis interface vrf all'] = IsisOutput.showIsisInterfaceVrfAll
outputs['show isis adjacency vrf all'] = IsisOutput.showIsisAdjacencyVrfAll
outputs['show isis hostname detail vrf all'] = IsisOutput.showIsisHostnameDetailVrfAll
outputs['show isis database detail vrf all'] = IsisOutput.showIsisDatabaseDetail

def mapper(key):
    return outputs[key]

class TestIsisAll(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_full_isis(self):
        isis = Isis(device=self.device)
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        isis.learn(vrf='all')
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
        self.assertEqual('R2', isis.info['instance']['test']['vrf']['default']
            ["hostname_db"]["hostname"]["2222.2222.2222.00-00"]["hostname"])
        self.assertEqual('R3', isis.lsdb['instance']['test']['vrf']['default']
            ["level_db"][1]["R3.00-00"]["dynamic_hostname"])

        # Check does not match
        self.assertNotEqual('R4', isis.info['instance']['test']['vrf']['default']
            ["hostname_db"]["hostname"]["7777.7777.7777.00-00"]["hostname"])
        self.assertNotEqual('0xAC24', isis.lsdb['instance']['test']['vrf']['default']
            ["level_db"][1]["R3.01-00"]["checksum"])

    def test_missing_attributes_Isis(self):
        isis = Isis(device=self.device)

        outputs['show isis hostname detail vrf all'] = ''
        outputs['show isis database detail vrf all'] = ''
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        isis.learn()

        # revert back
        outputs['show isis hostname detail vrf all'] = IsisOutput.showIsisHostnameDetailVrfAll
        outputs['show isis database detail vrf all'] = IsisOutput.showIsisDatabaseDetail

        with self.assertRaises(KeyError):
            isis.info['instance']['test']['vrf']['default']["hostname_db"]
            isis.lsdb['instance']['test']

    def test_empty_output_Isis(self):
        isis = Isis(device=self.device)

        # Return outputs as inputs to parser when called
        outputs['show isis vrf all'] = ''
        outputs['show isis interface vrf all'] = ''
        outputs['show isis adjacency vrf all'] = ''
        outputs['show isis hostname detail vrf all'] = ''
        outputs['show isis database detail vrf all'] = ''

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        isis.learn()

        # revert back
        outputs['show isis vrf all'] = IsisOutput.showIsisVrfAll
        outputs['show isis interface vrf all'] = IsisOutput.showIsisInterfaceVrfAll
        outputs['show isis adjacency vrf all'] = IsisOutput.showIsisAdjacencyVrfAll
        outputs['show isis hostname detail vrf all'] = IsisOutput.showIsisHostnameDetailVrfAll
        outputs['show isis database detail vrf all'] = IsisOutput.showIsisDatabaseDetail

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            isis.info['instance']
            isis.lsdb['instance']

if __name__ == '__main__':
    unittest.main()
