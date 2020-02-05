# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.lldp.nxos.lldp import Lldp
from genie.libs.ops.lldp.nxos.tests.lldp_output import LldpOutput

# nxos show_lldp
from genie.libs.parser.nxos.show_lldp import ShowLldpAll, ShowLldpTimers, \
    ShowLldpTlvSelect, ShowLldpNeighborsDetail, ShowLldpTraffic


class test_lldp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        lldp = Lldp(device=self.device)
        # Get outputs
        lldp.maker.outputs[ShowLldpAll] = \
            {'': LldpOutput.ShowLldpAll}

        lldp.maker.outputs[ShowLldpTlvSelect] = \
            {'': LldpOutput.ShowLldpTlvSelect}

        lldp.maker.outputs[ShowLldpNeighborsDetail] = \
            {'': LldpOutput.ShowLldpNeighborsDetail}

        lldp.maker.outputs[ShowLldpTimers] = \
            {'': LldpOutput.ShowLldpTimers}

        lldp.maker.outputs[ShowLldpTraffic] = \
            {'': LldpOutput.ShowLldpTraffic}

        # Learn the feature
        lldp.learn()
        # Verify Ops was created successfully
        self.assertDictEqual(lldp.info, LldpOutput.Lldp_info)

        # Check Selected Attributes
        self.assertEqual(lldp.info['hello_timer'], 30)
        # info - mlldp default
        self.assertEqual(lldp.info['interfaces']['Ethernet1/2'] \
                             ['enabled'], True)

    def test_empty_output(self):
        self.maxDiff = None
        lldp = Lldp(device=self.device)
        # Get outputs
        lldp.maker.outputs[ShowLldpAll] = \
            {'': {}}

        lldp.maker.outputs[ShowLldpTlvSelect] = \
            {'': {}}

        lldp.maker.outputs[ShowLldpNeighborsDetail] = \
            {'': {}}

        lldp.maker.outputs[ShowLldpTimers] = \
            {'': {}}

        lldp.maker.outputs[ShowLldpTraffic] = \
            {'': LldpOutput.ShowLldpTraffic}

        # Learn the feature
        lldp.learn()
        with self.assertRaises(KeyError):
            lldp.info['hello_timer']

    def test_incomplete_output(self):
        self.maxDiff = None
        lldp = Lldp(device=self.device)
        # Get outputs
        lldp.maker.outputs[ShowLldpAll] = \
            {'': {}}

        lldp.maker.outputs[ShowLldpTlvSelect] = \
            {'': LldpOutput.ShowLldpTlvSelect}

        lldp.maker.outputs[ShowLldpNeighborsDetail] = \
            {'': LldpOutput.ShowLldpNeighborsDetail}

        lldp.maker.outputs[ShowLldpTimers] = \
            {'': LldpOutput.ShowLldpTimers}

        lldp.maker.outputs[ShowLldpTraffic] = \
            {'': LldpOutput.ShowLldpTraffic}

        # Learn the feature
        lldp.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(LldpOutput.Lldp_info)
        del (expect_dict['interfaces']['Ethernet1/1']['enabled'])
        del (expect_dict['interfaces']['Ethernet1/2']['enabled'])

        # Verify Ops was created successfully
        self.assertEqual(lldp.info, expect_dict)

if __name__ == '__main__':
    unittest.main()