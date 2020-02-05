# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.mld.nxos.mld import Mld
from genie.libs.ops.mld.nxos.tests.mld_output import MldOutput

# Parser
from genie.libs.parser.nxos.show_mld import ShowIpv6MldInterface, \
                                 ShowIpv6MldGroups, \
                                 ShowIpv6MldLocalGroups


class test_mld(unittest.TestCase):

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
        mld = Mld(device=self.device)
        # Get outputs
        mld.maker.outputs[ShowIpv6MldInterface] = \
            {"{'vrf':'all'}": MldOutput.ShowIpv6MldInterface}

        mld.maker.outputs[ShowIpv6MldGroups] = \
            {"{'vrf':'all'}": MldOutput.ShowIpv6MldGroups}

        mld.maker.outputs[ShowIpv6MldLocalGroups] = \
            {"{'vrf':'all'}": MldOutput.ShowIpv6MldLocalGroups}

        # Learn the feature
        mld.learn()

        # Verify Ops was created successfully
        self.assertEqual(mld.info, MldOutput.Mld_info)

    def test_empty_output(self):
        self.maxDiff = None
        mld = Mld(device=self.device)
        # Get outputs
        mld.maker.outputs[ShowIpv6MldInterface] = \
            {"{'vrf':'all'}": {}}

        mld.maker.outputs[ShowIpv6MldGroups] = \
            {"{'vrf':'all'}": {}}

        mld.maker.outputs[ShowIpv6MldLocalGroups] = \
            {"{'vrf':'all'}": {}}

        # Learn the feature
        mld.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            mld.info['vrfs']

    def test_selective_attribute(self):
        self.maxDiff = None
        mld = Mld(device=self.device)

        # Get outputs
        mld.maker.outputs[ShowIpv6MldInterface] = \
            {"{'vrf':'all'}": MldOutput.ShowIpv6MldInterface}

        mld.maker.outputs[ShowIpv6MldGroups] = \
            {"{'vrf':'all'}": MldOutput.ShowIpv6MldGroups}

        mld.maker.outputs[ShowIpv6MldLocalGroups] = \
            {"{'vrf':'all'}": MldOutput.ShowIpv6MldLocalGroups}

        # Learn the feature
        mld.learn()      

        # Check specific attribute values
        # info - default vrf
        self.assertEqual(mld.info['vrfs']['default']['interfaces']\
        		['Ethernet2/1']['group_policy'], 'test')
        # info - vrf VRF1
        self.assertEqual(mld.info['vrfs']['VRF1']['interfaces']\
                                  ['Ethernet2/2']['group']\
                                  ['fffe::2']['last_reporter'], '2001:db8:8404:751c::1')

    def test_incomplete_output(self):
        self.maxDiff = None
        
        mld = Mld(device=self.device)

        # Get outputs
        mld.maker.outputs[ShowIpv6MldInterface] = \
            {"{'vrf':'all'}": MldOutput.ShowIpv6MldInterface}

        mld.maker.outputs[ShowIpv6MldGroups] = \
            {"{'vrf':'all'}": MldOutput.ShowIpv6MldGroups}

        mld.maker.outputs[ShowIpv6MldLocalGroups] = \
            {"{'vrf':'all'}": {}}

        # Learn the feature
        mld.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(MldOutput.Mld_info)
        del(expect_dict['vrfs']['default']['interfaces']['Ethernet2/1']['join_group'])
        del(expect_dict['vrfs']['default']['interfaces']['Ethernet2/1']['static_group'])
        del(expect_dict['vrfs']['VRF1']['interfaces']['Ethernet2/2']['join_group'])
        del(expect_dict['vrfs']['VRF1']['interfaces']['Ethernet2/2']['static_group'])

                
        # Verify Ops was created successfully
        self.assertEqual(mld.info, expect_dict)


if __name__ == '__main__':
    unittest.main()
