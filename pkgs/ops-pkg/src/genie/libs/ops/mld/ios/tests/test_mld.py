# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.mld.ios.mld import Mld
from genie.libs.ops.mld.ios.tests.mld_output import MldOutput

# Parser
from genie.libs.parser.ios.show_mld import ShowIpv6MldInterface, \
                                           ShowIpv6MldGroupsDetail, \
                                           ShowIpv6MldSsmMap

# iosxe show_vrf
from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail

outputs = {}
outputs['show ipv6 mld vrf VRF1 interface'] = MldOutput.ShowIpv6MldInterface_VRF1
outputs['show ipv6 mld vrf VRF1 groups detail'] = MldOutput.ShowIpv6MldGroupsDetail_VRF1
outputs['show ipv6 mld ssm-map FF15:1::1'] = MldOutput.ShowIpv6MldSsmMap_default_1
outputs['show ipv6 mld ssm-map FF25:2::1'] = MldOutput.ShowIpv6MldSsmMap_default_2
outputs['show ipv6 mld ssm-map FF35:1::1'] = MldOutput.ShowIpv6MldSsmMap_default_3
outputs['show ipv6 mld ssm-map FF45:1::1'] = MldOutput.ShowIpv6MldSsmMap_default_4
outputs['show ipv6 mld vrf VRF1 ssm-map FF15:1::1'] = MldOutput.ShowIpv6MldSsmMap_VRF1_1
outputs['show ipv6 mld vrf VRF1 ssm-map FF25:2::1'] = MldOutput.ShowIpv6MldSsmMap_VRF1_2
outputs['show ipv6 mld vrf VRF1 ssm-map FF35:1::1'] = MldOutput.ShowIpv6MldSsmMap_VRF1_3
outputs['show ipv6 mld vrf VRF1 ssm-map FF45:1::1'] = MldOutput.ShowIpv6MldSsmMap_VRF1_4


def mapper(key):
    return outputs[key]


class test_mld(unittest.TestCase):

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
        mld = Mld(device=self.device)
        # Get outputs
        mld.maker.outputs[ShowVrfDetail] = \
            {'': MldOutput.ShowVrfDetail}

        mld.maker.outputs[ShowIpv6MldInterface] = \
            {"{'vrf':''}": MldOutput.ShowIpv6MldInterface_default}

        mld.maker.outputs[ShowIpv6MldGroupsDetail] = \
            {"{'vrf':''}": MldOutput.ShowIpv6MldGroupsDetail_default}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        mld.learn()

        # Verify Ops was created successfully
        self.assertEqual(mld.info, MldOutput.Mld_info)

    def test_empty_output(self):
        self.maxDiff = None
        mld = Mld(device=self.device)
        # Get outputs
        mld.maker.outputs[ShowVrfDetail] = \
            {'': {}}

        mld.maker.outputs[ShowIpv6MldInterface] = \
            {"{'vrf':''}": {}}

        mld.maker.outputs[ShowIpv6MldGroupsDetail] = \
            {"{'vrf':''}": {}}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        outputs['show ipv6 mld vrf VRF1 interface'] = ''
        outputs['show ipv6 mld vrf VRF1 groups detail'] = ''
        outputs['show ipv6 mld ssm-map FF35:1::1'] = ''
        outputs['show ipv6 mld vrf VRF1 ssm-map FF35:1::1'] = ''
        self.device.execute.side_effect = mapper


        # Learn the feature
        mld.learn()

        # revert the outputs
        outputs['show ipv6 mld vrf VRF1 interface'] = MldOutput.ShowIpv6MldInterface_VRF1
        outputs['show ipv6 mld vrf VRF1 groups detail'] = MldOutput.ShowIpv6MldGroupsDetail_VRF1
        outputs['show ipv6 mld ssm-map FF35:1::1'] = MldOutput.ShowIpv6MldSsmMap_default_3
        outputs['show ipv6 mld vrf VRF1 ssm-map FF35:1::1'] = MldOutput.ShowIpv6MldSsmMap_VRF1_3

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            mld.info['vrfs']

    def test_selective_attribute(self):
        self.maxDiff = None
        mld = Mld(device=self.device)
        # Get outputs
        mld.maker.outputs[ShowVrfDetail] = \
            {'': MldOutput.ShowVrfDetail}

        mld.maker.outputs[ShowIpv6MldInterface] = \
            {"{'vrf':''}": MldOutput.ShowIpv6MldInterface_default}

        mld.maker.outputs[ShowIpv6MldGroupsDetail] = \
            {"{'vrf':''}": MldOutput.ShowIpv6MldGroupsDetail_default}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        mld.learn()      

        # Check specific attribute values
        # info - default vrf
        self.assertEqual(mld.info['vrfs']['default']['max_groups'], 64000)
        # info - vrf VRF1
        self.assertEqual(mld.info['vrfs']['VRF1']['interfaces']\
                                  ['GigabitEthernet2']['querier'], 'FE80::5054:FF:FEDD:BB49')

    def test_incomplete_output(self):
        self.maxDiff = None
        
        mld = Mld(device=self.device)

        # Get outputs
        mld.maker.outputs[ShowVrfDetail] = \
            {'': MldOutput.ShowVrfDetail}

        mld.maker.outputs[ShowIpv6MldInterface] = \
            {"{'vrf':''}": MldOutput.ShowIpv6MldInterface_default}

        mld.maker.outputs[ShowIpv6MldGroupsDetail] = \
            {"{'vrf':''}": MldOutput.ShowIpv6MldGroupsDetail_default}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()

        # overwrite output with empty output
        outputs['show ipv6 mld vrf VRF1 groups detail'] = ''
        self.device.execute.side_effect = mapper

        # Learn the feature
        mld.learn()
        
        # revert the outputs
        outputs['show ipv6 mld vrf VRF1 groups detail'] = MldOutput.ShowIpv6MldGroupsDetail_VRF1

        # Delete missing specific attribute values
        expect_dict = deepcopy(MldOutput.Mld_info)
        del(expect_dict['vrfs']['VRF1']['interfaces']['GigabitEthernet2']['join_group'])
        del(expect_dict['vrfs']['VRF1']['interfaces']['GigabitEthernet2']['static_group'])
        del(expect_dict['vrfs']['VRF1']['interfaces']['GigabitEthernet2']['group'])
        del(expect_dict['vrfs']['VRF1']['ssm_map'])

                
        # Verify Ops was created successfully
        self.assertEqual(mld.info, expect_dict)


if __name__ == '__main__':
    unittest.main()