# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.mld.iosxr.mld import Mld
from genie.libs.ops.mld.iosxr.tests.mld_output import MldOutput

# Parser
from genie.libs.parser.iosxr.show_mld import ShowMldSummaryInternal, \
                                             ShowMldInterface, \
                                             ShowMldGroupsDetail

# iosxr show_vrf
from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail

outputs = {}
# outputs['show mld summary internal'] = MldOutput.ShowMldSummaryInternal_default
outputs['show mld vrf VRF1 summary internal'] = MldOutput.ShowMldSummaryInternal_VRF
# outputs['show mld interface'] = MldOutput.ShowMldInterface_default
outputs['show mld vrf VRF1 interface'] = MldOutput.ShowMldInterface_VRF
# outputs['show mld groups detail'] = MldOutput.ShowMldGroupsDetail_default
outputs['show mld vrf VRF1 groups detail'] = MldOutput.ShowMldGroupsDetail_VRF


def mapper(key):
    return outputs[key]


class test_mld(unittest.TestCase):

    def setUp(self):
        self.device = Device(name = 'aDevice')
        self.device.os = 'iosxr'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        mld = Mld(device = self.device)

        # Get outputs
        mld.maker.outputs[ShowVrfAllDetail] = \
            {'': MldOutput.ShowVrfAllDetail}

        mld.maker.outputs[ShowMldSummaryInternal] = \
            {"{'vrf':''}": MldOutput.ShowMldSummaryInternal_default}

        mld.maker.outputs[ShowMldInterface] = \
            {"{'vrf':''}": MldOutput.ShowMldInterface_default}

        mld.maker.outputs[ShowMldGroupsDetail] = \
            {"{'vrf':''}": MldOutput.ShowMldGroupsDetail_default}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        mld.learn()

        # Verify Ops was created successfully
        self.assertEqual(mld.info, MldOutput.Mld_info)

    def test_empty_output(self):
        self.maxDiff = None
        mld = Mld(device = self.device)

        # Get outputs
        mld.maker.outputs[ShowVrfAllDetail] = {'': {}}

        mld.maker.outputs[ShowMldSummaryInternal] = {"{'vrf':''}": {}}

        mld.maker.outputs[ShowMldInterface] = {"{'vrf':''}": {}}

        mld.maker.outputs[ShowMldGroupsDetail] = {"{'vrf':''}": {}}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        outputs['show mld vrf VRF1 summary internal'] = ''
        outputs['show mld vrf VRF1 interface'] = ''
        outputs['show mld vrf VRF1 groups detail'] = ''
        self.device.execute.side_effect = mapper

        # Learn the feature
        mld.learn()

        # revert the outputs
        outputs['show mld vrf VRF1 summary internal'] = MldOutput.ShowMldSummaryInternal_VRF
        outputs['show mld vrf VRF1 interface'] = MldOutput.ShowMldInterface_VRF
        outputs['show mld vrf VRF1 groups detail'] = MldOutput.ShowMldGroupsDetail_VRF

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            mld.info['vrfs']

    def test_selective_attribute(self):
        self.maxDiff = None
        mld = Mld(device = self.device)
        
        # Get outputs
        mld.maker.outputs[ShowVrfAllDetail] = \
            {'': MldOutput.ShowVrfAllDetail}

        mld.maker.outputs[ShowMldSummaryInternal] = \
            {"{'vrf':''}": MldOutput.ShowMldSummaryInternal_default}

        mld.maker.outputs[ShowMldInterface] = \
            {"{'vrf':''}": MldOutput.ShowMldInterface_default}

        mld.maker.outputs[ShowMldGroupsDetail] = \
            {"{'vrf':''}": MldOutput.ShowMldGroupsDetail_default}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        mld.learn()      

        # Check specific attribute values
        # info - default vrf
        self.assertEqual(mld.info['vrfs']['default']['interfaces']\
                        ['GigabitEthernet0/0/0/0']['querier'], 'fe80::5054:ff:fed7:c01f')
        # info - vrf VRF1
        self.assertEqual(mld.info['vrfs']['VRF1']['interfaces']\
                        ['GigabitEthernet0/0/0/1']['query_interval'], 366)

    def test_incomplete_output(self):
        self.maxDiff = None
        
        mld = Mld(device = self.device)

        # Get outputs
        mld.maker.outputs[ShowVrfAllDetail] = \
            {'': MldOutput.ShowVrfAllDetail}

        mld.maker.outputs[ShowMldSummaryInternal] = \
            {"{'vrf':''}": MldOutput.ShowMldSummaryInternal_default}

        mld.maker.outputs[ShowMldInterface] = \
            {"{'vrf':''}": MldOutput.ShowMldInterface_default}

        mld.maker.outputs[ShowMldGroupsDetail] = \
            {"{'vrf':''}": MldOutput.ShowMldGroupsDetail_default}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()

        # overwrite output with empty output
        # outputs['show ipv6 mld vrf VRF1 groups detail'] = ''
        outputs['show mld vrf VRF1 groups detail'] = ''
        self.device.execute.side_effect = mapper

        # Learn the feature
        mld.learn()
        
        # revert the outputs
        outputs['show mld vrf VRF1 groups detail'] = MldOutput.ShowMldGroupsDetail_VRF

        # Delete missing specific attribute values
        expect_dict = deepcopy(MldOutput.Mld_info)
        del(expect_dict['vrfs']['VRF1']['interfaces']['GigabitEthernet0/0/0/1']['join_group'])
        del(expect_dict['vrfs']['VRF1']['interfaces']['GigabitEthernet0/0/0/1']['static_group'])
        del(expect_dict['vrfs']['VRF1']['interfaces']['GigabitEthernet0/0/0/1']['group'])

        # Verify Ops was created successfully
        self.assertEqual(mld.info, expect_dict)


if __name__ == '__main__':
    unittest.main()
