# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.igmp.ios.igmp import Igmp
from genie.libs.ops.igmp.ios.tests.igmp_output import IgmpOutput

# Parser
from genie.libs.parser.ios.show_igmp import ShowIpIgmpInterface, \
                                            ShowIpIgmpGroupsDetail, \
                                            ShowIpIgmpSsmMapping

# iosxe show_vrf
from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail

outputs = {}
outputs['show ip igmp interface'] = IgmpOutput.ShowIpIgmpInterface_default
outputs['show ip igmp vrf VRF1 interface'] = IgmpOutput.ShowIpIgmpInterface_VRF1
outputs['show ip igmp groups detail'] = IgmpOutput.ShowIpIgmpGroupsDetail_default
outputs['show ip igmp vrf VRF1 groups detail'] = IgmpOutput.ShowIpIgmpGroupsDetail_VRF1
outputs['show ip igmp ssm-mapping 239.1.1.1'] = IgmpOutput.ShowIpIgmpSsmMapping_default_1
outputs['show ip igmp ssm-mapping 239.2.2.2'] = IgmpOutput.ShowIpIgmpSsmMapping_default_2
outputs['show ip igmp ssm-mapping 239.3.3.3'] = IgmpOutput.ShowIpIgmpSsmMapping_default_3
outputs['show ip igmp ssm-mapping 239.4.4.4'] = IgmpOutput.ShowIpIgmpSsmMapping_default_4
outputs['show ip igmp ssm-mapping 239.5.5.5'] = IgmpOutput.ShowIpIgmpSsmMapping_default_5
outputs['show ip igmp ssm-mapping 239.6.6.6'] = IgmpOutput.ShowIpIgmpSsmMapping_default_6
outputs['show ip igmp ssm-mapping 239.7.7.7'] = IgmpOutput.ShowIpIgmpSsmMapping_default_7
outputs['show ip igmp ssm-mapping 239.8.8.8'] = IgmpOutput.ShowIpIgmpSsmMapping_default_8
outputs['show ip igmp ssm-mapping 239.9.9.9'] = IgmpOutput.ShowIpIgmpSsmMapping_default_9
outputs['show ip igmp ssm-mapping 224.0.1.40'] = IgmpOutput.ShowIpIgmpSsmMapping_default_10
outputs['show ip igmp vrf VRF1 ssm-mapping 239.1.1.1'] = IgmpOutput.ShowIpIgmpSsmMapping_VRF1_1
outputs['show ip igmp vrf VRF1 ssm-mapping 239.2.2.2'] = IgmpOutput.ShowIpIgmpSsmMapping_VRF1_2
outputs['show ip igmp vrf VRF1 ssm-mapping 239.3.3.3'] = IgmpOutput.ShowIpIgmpSsmMapping_VRF1_3
outputs['show ip igmp vrf VRF1 ssm-mapping 239.4.4.4'] = IgmpOutput.ShowIpIgmpSsmMapping_VRF1_4
outputs['show ip igmp vrf VRF1 ssm-mapping 239.5.5.5'] = IgmpOutput.ShowIpIgmpSsmMapping_VRF1_5
outputs['show ip igmp vrf VRF1 ssm-mapping 239.6.6.6'] = IgmpOutput.ShowIpIgmpSsmMapping_VRF1_6
outputs['show ip igmp vrf VRF1 ssm-mapping 239.7.7.7'] = IgmpOutput.ShowIpIgmpSsmMapping_VRF1_7
outputs['show ip igmp vrf VRF1 ssm-mapping 239.8.8.8'] = IgmpOutput.ShowIpIgmpSsmMapping_VRF1_8
outputs['show ip igmp vrf VRF1 ssm-mapping 224.0.1.40'] = IgmpOutput.ShowIpIgmpSsmMapping_VRF1_10


def mapper(key):
    return outputs[key]


class test_igmp(unittest.TestCase):

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
        igmp = Igmp(device=self.device)
        # Get outputs
        igmp.maker.outputs[ShowVrfDetail] = \
            {'': IgmpOutput.ShowVrfDetail}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        igmp.learn()

        # Verify Ops was created successfully
        self.assertEqual(igmp.info, IgmpOutput.Igmp_info)

    def test_empty_output(self):
        self.maxDiff = None
        igmp = Igmp(device=self.device)
        # Get outputs
        igmp.maker.outputs[ShowVrfDetail] = \
            {'': {}}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        outputs['show ip igmp interface'] = ''
        outputs['show ip igmp vrf VRF1 interface'] = ''
        outputs['show ip igmp groups detail'] = ''
        outputs['show ip igmp vrf VRF1 groups detail'] = ''
        outputs['show ip igmp ssm-mapping 239.1.1.1'] = ''
        outputs['show ip igmp vrf VRF1 ssm-mapping 239.1.1.1'] = ''
        self.device.execute.side_effect = mapper


        # Learn the feature
        igmp.learn()

        # revert the outputs
        outputs['show ip igmp interface'] = IgmpOutput.ShowIpIgmpInterface_default
        outputs['show ip igmp vrf VRF1 interface'] = IgmpOutput.ShowIpIgmpInterface_VRF1
        outputs['show ip igmp groups detail'] = IgmpOutput.ShowIpIgmpGroupsDetail_default
        outputs['show ip igmp vrf VRF1 groups detail'] = IgmpOutput.ShowIpIgmpGroupsDetail_VRF1
        outputs['show ip igmp ssm-mapping 239.1.1.1'] = IgmpOutput.ShowIpIgmpSsmMapping_default_1
        outputs['show ip igmp vrf VRF1 ssm-mapping 239.1.1.1'] = IgmpOutput.ShowIpIgmpSsmMapping_VRF1_1

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            igmp.info['vrfs']

    def test_selective_attribute(self):
        self.maxDiff = None
        igmp = Igmp(device=self.device)
        # Get outputs
        igmp.maker.outputs[ShowVrfDetail] = \
            {'': IgmpOutput.ShowVrfDetail}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        igmp.learn()      

        # Check specific attribute values
        # info - default vrf
        self.assertEqual(igmp.info['vrfs']['default']['max_groups'], 20)
        # info - vrf VRF1
        self.assertEqual(igmp.info['vrfs']['VRF1']['interfaces']\
                                  ['GigabitEthernet2']['querier'], '10.186.2.1')

    def test_incomplete_output(self):
        self.maxDiff = None
        
        igmp = Igmp(device=self.device)

        # Get outputs
        igmp.maker.outputs[ShowVrfDetail] = \
            {'': IgmpOutput.ShowVrfDetail}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()

        # overwrite output with empty output
        outputs['show ip igmp vrf VRF1 groups detail'] = '''\
            show ip igmp vrf VRF1 groups detail
        '''
        self.device.execute.side_effect = mapper

        # Learn the feature
        igmp.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(IgmpOutput.Igmp_info)
        del(expect_dict['vrfs']['VRF1']['interfaces']['GigabitEthernet2']['join_group'])
        del(expect_dict['vrfs']['VRF1']['interfaces']['GigabitEthernet2']['static_group'])
        del(expect_dict['vrfs']['VRF1']['interfaces']['GigabitEthernet2']['group'])
        del(expect_dict['vrfs']['VRF1']['ssm_map'])

                
        # Verify Ops was created successfully
        self.assertEqual(igmp.info, expect_dict)


if __name__ == '__main__':
    unittest.main()