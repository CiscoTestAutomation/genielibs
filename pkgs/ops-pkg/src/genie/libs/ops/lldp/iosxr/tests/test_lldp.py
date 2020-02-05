# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.lldp.iosxr.lldp import Lldp
from genie.libs.ops.lldp.iosxr.tests.lldp_output import LldpOutput

# Parser
from genie.libs.parser.iosxr.show_lldp import ShowLldp, \
                                   ShowLldpEntry, \
                                   ShowLldpNeighborsDetail,\
                                   ShowLldpTraffic, \
                                   ShowLldpInterface

class test_lldp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        lldp = Lldp(device=self.device)
        # Get outputs
        lldp.maker.outputs[ShowLldp] = \
            {'': LldpOutput.ShowLldp}

        lldp.maker.outputs[ShowLldpEntry] = \
            {'': LldpOutput.ShowLldpEntry}

        lldp.maker.outputs[ShowLldpNeighborsDetail] = \
            {'': LldpOutput.ShowLldpNeighborsDetail}

        lldp.maker.outputs[ShowLldpTraffic] = \
            {'': LldpOutput.ShowLldpTraffic}

        lldp.maker.outputs[ShowLldpInterface] = \
            {'': LldpOutput.ShowLldpInterface}

        # Learn the feature
        lldp.learn()
        
        # Verify Ops was created successfully
        self.assertEqual(lldp.info, LldpOutput.lldpOutput)

        # Check specific attribute values
        # info - interfaces
        self.assertEqual(lldp.info['interfaces']['GigabitEthernet0/0/0/1']\
            ['port_id']['Ethernet1/2']['neighbors']['R3_n9kv']['chassis_id'],\
             '5e00.8002.0009')

        self.assertEqual(lldp.info['interfaces']['GigabitEthernet0/0/0/1']\
            ['enabled'], True)

    def test_empty_output(self):
        self.maxDiff = None
        lldp = Lldp(device=self.device)
        # Get outputs
        lldp.maker.outputs[ShowLldp] = \
            {'': {}}

        lldp.maker.outputs[ShowLldpEntry] = \
            {'': {}}

        lldp.maker.outputs[ShowLldpNeighborsDetail] = \
            {'': {}}

        lldp.maker.outputs[ShowLldpTraffic] = \
            {'': {}}

        lldp.maker.outputs[ShowLldpInterface] = \
            {'': LldpOutput.ShowLldpInterface}
        # Learn the feature
        lldp.learn()

        # Check no attribute not found
        with self.assertRaises(KeyError):
            lldp.info['enabled']

    def test_incomplete_output(self):
        self.maxDiff = None
        
        lldp = Lldp(device=self.device)
        # Get outputs
        lldp.maker.outputs[ShowLldp] = \
            {'': LldpOutput.ShowLldp}

        lldp.maker.outputs[ShowLldpEntry] = \
            {'': LldpOutput.ShowLldpEntry}

        lldp.maker.outputs[ShowLldpNeighborsDetail] = \
            {'': LldpOutput.ShowLldpNeighborsDetail}

        lldp.maker.outputs[ShowLldpTraffic] = \
            {'': LldpOutput.ShowLldpTraffic}

        lldp.maker.outputs[ShowLldpInterface] = \
            {'': LldpOutput.ShowLldpInterface}

        # delete keys from input
        del(LldpOutput.ShowLldp['hello_timer'])
        # Learn the feature
        lldp.learn()
        
        # Delete missing specific attribute values
        expect_dict = deepcopy(LldpOutput.lldpOutput)
        del(expect_dict['hello_timer'])     
        # Verify Ops was created successfully
        self.assertEqual(lldp.info, expect_dict)

if __name__ == '__main__':
    unittest.main()