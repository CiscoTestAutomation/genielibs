# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.igmp.iosxr.igmp import Igmp
from genie.libs.ops.igmp.iosxr.tests.igmp_output import IgmpOutput

# Parser
from genie.libs.parser.iosxr.show_igmp import ShowIgmpInterface, \
                                             ShowIgmpSummary, \
                                             ShowIgmpGroupsDetail

# iosxr show_vrf
from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail

class test_igmp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
                # Create a mock connection to get output for parsing
        self.device_connection = Mock(device=self.device)
        self.device.connectionmgr.connections['cli'] = self.device_connection
        # Set outputs
        self.device_connection.execute.side_effect = mapper

    def test_full_igmp(self):
        self.maxDiff = None
        igmp = Igmp(device=self.device)
        # Get outputs
        igmp.maker.outputs[ShowVrfAllDetail] = {'': IgmpOutput.ShowVrfAllDetail}
        igmp.maker.outputs[ShowIgmpInterface] = {"{'vrf':''}": IgmpOutput.ShowIgmpInterface}
        igmp.maker.outputs[ShowIgmpInterface]["{'vrf':'VRF1'}"] = IgmpOutput.ShowIgmpInterface_VRF1
        igmp.maker.outputs[ShowIgmpSummary] = {"{'vrf':''}": IgmpOutput.ShowIgmpSummary}
        igmp.maker.outputs[ShowIgmpSummary]["{'vrf':'VRF1'}"] = IgmpOutput.ShowIgmpSummary_VRF1
        igmp.maker.outputs[ShowIgmpGroupsDetail] = {"{'vrf':''}": IgmpOutput.ShowIgmpGroupsDetail}
        igmp.maker.outputs[ShowIgmpGroupsDetail]["{'vrf':'VRF1'}"] = IgmpOutput.ShowIgmpGroupsDetail_VRF1

        # Learn the feature
        igmp.learn()

        # Verify Ops was created successfully
        self.assertEqual(igmp.info, IgmpOutput.IgmpOpsOutput)

    def test_selective_attribute_igmp(self):
        self.maxDiff = None
        igmp = Igmp(device=self.device)
        # Get outputs
        igmp.maker.outputs[ShowVrfAllDetail] = {'': IgmpOutput.ShowVrfAllDetail}
        igmp.maker.outputs[ShowIgmpInterface] = {"{'vrf':''}": IgmpOutput.ShowIgmpInterface}
        igmp.maker.outputs[ShowIgmpInterface]["{'vrf':'VRF1'}"] = IgmpOutput.ShowIgmpInterface_VRF1
        igmp.maker.outputs[ShowIgmpSummary] = {"{'vrf':''}": IgmpOutput.ShowIgmpSummary}
        igmp.maker.outputs[ShowIgmpSummary]["{'vrf':'VRF1'}"] = IgmpOutput.ShowIgmpSummary_VRF1
        igmp.maker.outputs[ShowIgmpGroupsDetail] = {"{'vrf':''}": IgmpOutput.ShowIgmpGroupsDetail}
        igmp.maker.outputs[ShowIgmpGroupsDetail]["{'vrf':'VRF1'}"] = IgmpOutput.ShowIgmpGroupsDetail_VRF1

        # Learn the feature
        igmp.learn()

        # Check match
        self.assertEqual('2.2.2.2', igmp.info['vrfs']['default']['interfaces']['Loopback0']['group']
                         ['224.0.0.2']['last_reporter'])

        # Check does not match
        self.assertNotEqual('disabled', igmp.info['vrfs']['default']['interfaces']['Loopback0']['enable'])

    def test_missing_attributes_igmp(self):
        igmp = Igmp(device=self.device)
        # Get outputs
        igmp.maker.outputs[ShowVrfAllDetail] = {'': IgmpOutput.ShowVrfAllDetail}
        igmp.maker.outputs[ShowIgmpInterface] = {"{'vrf':''}": IgmpOutput.ShowIgmpInterface}
        igmp.maker.outputs[ShowIgmpInterface]["{'vrf':'VRF1'}"] = IgmpOutput.ShowIgmpInterface_VRF1
        igmp.maker.outputs[ShowIgmpSummary] = {"{'vrf':''}": {}}
        igmp.maker.outputs[ShowIgmpSummary]["{'vrf':'VRF1'}"] = {}
        igmp.maker.outputs[ShowIgmpGroupsDetail] = {"{'vrf':''}": IgmpOutput.ShowIgmpGroupsDetail}
        igmp.maker.outputs[ShowIgmpGroupsDetail]["{'vrf':'VRF1'}"] = IgmpOutput.ShowIgmpGroupsDetail_VRF1

        # Learn the feature
        igmp.learn()

        with self.assertRaises(KeyError):
            status = igmp.info['robustness_value']

    def test_empty_output_igmp(self):
        self.maxDiff = None
        igmp = Igmp(device=self.device)

        # Get outputs
        igmp.maker.outputs[ShowVrfAllDetail] = {'': {}}
        igmp.maker.outputs[ShowIgmpInterface] = {"{'vrf':''}": {}}
        igmp.maker.outputs[ShowIgmpInterface]["{'vrf':'VRF1'}"] = {}
        igmp.maker.outputs[ShowIgmpSummary] = {"{'vrf':''}": {}}
        igmp.maker.outputs[ShowIgmpSummary]["{'vrf':'VRF1'}"] = {}
        igmp.maker.outputs[ShowIgmpGroupsDetail] = {"{'vrf':''}": {}}
        igmp.maker.outputs[ShowIgmpGroupsDetail]["{'vrf':'VRF1'}"] = {}

        # Learn the feature
        igmp.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            igmp.info['robustness_value']

    def test_igmp_groups_detail(self):
        self.maxDiff = None
        igmp = Igmp(device=self.device)
        # Get outputs
        igmp.maker.outputs[ShowVrfAllDetail] = {'': IgmpOutput.ShowVrfAllDetail}
        igmp.maker.outputs[ShowIgmpInterface] = {"{'vrf':''}": IgmpOutput.ShowIgmpInterface}
        igmp.maker.outputs[ShowIgmpInterface]["{'vrf':'VRF1'}"] = IgmpOutput.ShowIgmpInterface_VRF1
        igmp.maker.outputs[ShowIgmpSummary] = {"{'vrf':''}": IgmpOutput.ShowIgmpSummary}
        igmp.maker.outputs[ShowIgmpSummary]["{'vrf':'VRF1'}"] = IgmpOutput.ShowIgmpSummary_VRF1
        igmp.maker.outputs[ShowIgmpGroupsDetail] = {"{'vrf':''}": IgmpOutput.ShowIgmpGroupsDetail}
        igmp.maker.outputs[ShowIgmpGroupsDetail]["{'vrf':'VRF1'}"] = IgmpOutput.ShowIgmpGroupsDetail_VRF1_source_list

        # Learn the feature
        igmp.learn()

        # Verify Ops was created successfully
        self.assertEqual(igmp.info, IgmpOutput.IgmpOpsOutputSourceList)

    def test_learn_vrf_with_no_igmp_data(self):
        # Regression test for issue #186: a vrf that exists on the device
        # (per 'show vrf all detail') but has no igmp-enabled interfaces at
        # all used to crash learn() with KeyError. Per the issue's expected
        # behaviour, such a vrf should still show up in the output as an
        # empty entry, not be dropped from it.
        self.maxDiff = None
        igmp = Igmp(device=self.device)

        igmp.maker.outputs[ShowVrfAllDetail] = {'': IgmpOutput.ShowVrfAllDetail_EmptyVRF}
        igmp.maker.outputs[ShowIgmpInterface] = {"{'vrf':''}": IgmpOutput.ShowIgmpInterface}
        igmp.maker.outputs[ShowIgmpInterface]["{'vrf':'zEmptyVRF'}"] = {}
        igmp.maker.outputs[ShowIgmpSummary] = {"{'vrf':''}": IgmpOutput.ShowIgmpSummary}
        igmp.maker.outputs[ShowIgmpSummary]["{'vrf':'zEmptyVRF'}"] = {}
        igmp.maker.outputs[ShowIgmpGroupsDetail] = {"{'vrf':''}": IgmpOutput.ShowIgmpGroupsDetail}
        igmp.maker.outputs[ShowIgmpGroupsDetail]["{'vrf':'zEmptyVRF'}"] = {}

        # Learn the feature - this used to raise KeyError: 'zEmptyVRF'
        igmp.learn()

        # The vrf with real igmp data is still learned normally
        self.assertIn('default', igmp.info['vrfs'])
        self.assertIn('Loopback0', igmp.info['vrfs']['default']['interfaces'])

        # The vrf with no igmp-enabled interfaces still shows up, empty,
        # instead of being dropped from the output entirely
        self.assertIn('zEmptyVRF', igmp.info['vrfs'])
        self.assertEqual(igmp.info['vrfs']['zEmptyVRF'], {'interfaces': {}})

if __name__ == '__main__':
    unittest.main()
