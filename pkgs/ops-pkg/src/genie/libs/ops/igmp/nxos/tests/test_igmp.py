# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.igmp.nxos.igmp import Igmp
from genie.libs.ops.igmp.nxos.tests.igmp_output import IgmpOutput

# Parser
from genie.libs.parser.nxos.show_igmp import ShowIpIgmpInterface, \
                                  ShowIpIgmpGroups, \
                                  ShowIpIgmpLocalGroups


class test_igmp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        igmp = Igmp(device=self.device)
        # Get outputs
        igmp.maker.outputs[ShowIpIgmpInterface] = \
            {"{'vrf':'all'}": IgmpOutput.ShowIpIgmpInterface}

        igmp.maker.outputs[ShowIpIgmpGroups] = \
            {"{'vrf':'all'}": IgmpOutput.ShowIpIgmpGroups}

        igmp.maker.outputs[ShowIpIgmpLocalGroups] = \
            {"{'vrf':'all'}": IgmpOutput.ShowIpIgmpLocalGroups}

        # Learn the feature
        igmp.learn()

        # Verify Ops was created successfully
        self.assertEqual(igmp.info, IgmpOutput.Igmp_info)

    def test_empty_output(self):
        self.maxDiff = None
        igmp = Igmp(device=self.device)
        # Get outputs
        igmp.maker.outputs[ShowIpIgmpInterface] = \
            {"{'vrf':'all'}": {}}

        igmp.maker.outputs[ShowIpIgmpGroups] = \
            {"{'vrf':'all'}": {}}

        igmp.maker.outputs[ShowIpIgmpLocalGroups] = \
            {"{'vrf':'all'}": {}}

        # Learn the feature
        igmp.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            igmp.info['vrfs']

    def test_selective_attribute(self):
        self.maxDiff = None
        igmp = Igmp(device=self.device)

        # Get outputs
        igmp.maker.outputs[ShowIpIgmpInterface] = \
            {"{'vrf':'all'}": IgmpOutput.ShowIpIgmpInterface}

        igmp.maker.outputs[ShowIpIgmpGroups] = \
            {"{'vrf':'all'}": IgmpOutput.ShowIpIgmpGroups}

        igmp.maker.outputs[ShowIpIgmpLocalGroups] = \
            {"{'vrf':'all'}": IgmpOutput.ShowIpIgmpLocalGroups}

        # Learn the feature
        igmp.learn()      

        # Check specific attribute values
        # info - default vrf
        self.assertEqual(igmp.info['vrfs']['default']['groups_count'], 2)
        # info - vrf VRF1
        self.assertEqual(igmp.info['vrfs']['VRF1']['interfaces']\
                                  ['Ethernet2/4']['group']\
                                  ['239.6.6.6']['last_reporter'], '10.186.2.1')

    def test_incomplete_output(self):
        self.maxDiff = None
        
        igmp = Igmp(device=self.device)

        # Get outputs
        igmp.maker.outputs[ShowIpIgmpInterface] = \
            {"{'vrf':'all'}": IgmpOutput.ShowIpIgmpInterface}

        igmp.maker.outputs[ShowIpIgmpGroups] = \
            {"{'vrf':'all'}": IgmpOutput.ShowIpIgmpGroups}

        igmp.maker.outputs[ShowIpIgmpLocalGroups] = \
            {"{'vrf':'all'}": {}}

        # Learn the feature
        igmp.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(IgmpOutput.Igmp_info)
        del(expect_dict['vrfs']['default']['interfaces']['Ethernet2/1']['join_group'])
        del(expect_dict['vrfs']['default']['interfaces']['Ethernet2/1']['static_group'])
        del(expect_dict['vrfs']['VRF1']['interfaces']['Ethernet2/4']['join_group'])
        del(expect_dict['vrfs']['VRF1']['interfaces']['Ethernet2/4']['static_group'])

                
        # Verify Ops was created successfully
        self.assertEqual(igmp.info, expect_dict)


if __name__ == '__main__':
    unittest.main()
