# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.fdb.nxos.fdb import Fdb
from genie.libs.ops.fdb.nxos.tests.fdb_output import FdbOutput

outputs = {}
outputs['show mac address-table'] = FdbOutput.show_mac_address_table
outputs['show mac address-table address 5e00.c000.0007 interface ethernet1/3 vlan 8000'] = FdbOutput.show_mac_address_table_custom
outputs['show mac address-table aging-time'] = FdbOutput.show_mac_address_table_aging_time
outputs['show system internal l2fwder mac'] = FdbOutput.show_system_internal_l2fwder_mac

def mapper(key):
    return outputs[key]

class TestFdb(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        fdb = Fdb(device=self.device)

        # Learn the feature
        fdb.learn()

        # Verify Ops was created successfully
        self.assertEqual(fdb.info, FdbOutput.fdb_info)


    def test_custom_output(self):
        self.maxDiff = None
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        fdb = Fdb(device=self.device)

        # Learn the feature
        fdb.learn(address='5e00.c000.0007', interface='ethernet1/3', vlan='8000')

        self.assertEqual(fdb.info['mac_table']['vlans']['8000']['vlan'], '8000')

    def test_empty_output(self):
        self.maxDiff = None
        self.device.execute = Mock()
        self.device.execute.return_value = ''
        fdb = Fdb(device=self.device)

        fdb.learn()

        with self.assertRaises(AttributeError):
            fdb.info['mac_table']