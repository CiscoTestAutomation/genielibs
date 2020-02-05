# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.fdb.ios.fdb import Fdb
from genie.libs.ops.fdb.ios.tests.fdb_output import FdbOutput

# Parser
from genie.libs.parser.ios.show_fdb import ShowMacAddressTable, \
                                           ShowMacAddressTableAgingTime, \
                                           ShowMacAddressTableLearning


class test_fdb(unittest.TestCase):

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
        fdb = Fdb(device=self.device)
        # Get outputs
        fdb.maker.outputs[ShowMacAddressTable] = \
            {'': FdbOutput.ShowMacAddressTable}

        fdb.maker.outputs[ShowMacAddressTableAgingTime] = \
            {'': FdbOutput.ShowMacAddressTableAgingTime}

        fdb.maker.outputs[ShowMacAddressTableLearning] = \
            {'': FdbOutput.ShowMacAddressTableLearning}

        # Learn the feature
        fdb.learn()

        # Verify Ops was created successfully
        self.assertEqual(fdb.info, FdbOutput.Fdb_info)

        # Check Selected Attributes
        self.assertEqual(fdb.info['mac_table']['vlans']['100']['vlan'], 100)
        self.assertEqual(fdb.info['mac_aging_time'], 0)

    def test_empty_output(self):
        self.maxDiff = None
        fdb = Fdb(device=self.device)

        fdb.maker.outputs[ShowMacAddressTable] = \
            {'': {}}

        fdb.maker.outputs[ShowMacAddressTableAgingTime] = \
            {'': {}}

        fdb.maker.outputs[ShowMacAddressTableLearning] = \
            {'': {}}

        # Learn the feature
        fdb.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            fdb.info['fdbs']['fdb_name']['name']

    def test_incomplete_output(self):
        self.maxDiff = None
        
        fdb = Fdb(device=self.device)
        # Get outputs
        fdb.maker.outputs[ShowMacAddressTable] = \
            {'': FdbOutput.ShowMacAddressTable}

        fdb.maker.outputs[ShowMacAddressTableAgingTime] = \
            {'': {}}

        fdb.maker.outputs[ShowMacAddressTableLearning] = \
            {'': FdbOutput.ShowMacAddressTableLearning}

        # Learn the feature
        fdb.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(FdbOutput.Fdb_info)
        del(expect_dict['mac_aging_time'])
        del(expect_dict['mac_table']['vlans']['10']['mac_aging_time'])
                
        # Verify Ops was created successfully
        self.assertEqual(fdb.info, expect_dict)


if __name__ == '__main__':
    unittest.main()