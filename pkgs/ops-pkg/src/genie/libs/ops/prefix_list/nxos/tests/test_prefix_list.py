# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.prefix_list.nxos.prefix_list import PrefixList
from genie.libs.ops.prefix_list.nxos.tests.prefix_output import PrefixListOutput

# iosxe show_prefix_list
from genie.libs.parser.nxos.show_prefix_list import ShowIpPrefixList, \
                                         ShowIpv6PrefixList


class test_prefix_list(unittest.TestCase):

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
        prefix = PrefixList(device=self.device)
        # Get outputs
        prefix.maker.outputs[ShowIpPrefixList] = \
            {'':PrefixListOutput.ShowIpPrefixList}

        prefix.maker.outputs[ShowIpv6PrefixList] = \
            {'':PrefixListOutput.ShowIpv6PrefixList}

        # Learn the feature
        prefix.learn()

        # Verify Ops was created successfully
        self.assertEqual(prefix.info, PrefixListOutput.PrefixList_info)

    def test_empty_output(self):
        self.maxDiff = None
        prefix = PrefixList(device=self.device)
        # Get outputs
        prefix.maker.outputs[ShowIpPrefixList] = {'':''}

        prefix.maker.outputs[ShowIpv6PrefixList] = {'':''}

        # Learn the feature
        prefix.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            out = prefix.info['prefix_set_name']

    def test_selective_attribute(self):
        self.maxDiff = None
        prefix = PrefixList(device=self.device)
        # Get outputs
        prefix.maker.outputs[ShowIpPrefixList] = \
            {'':PrefixListOutput.ShowIpPrefixList}

        prefix.maker.outputs[ShowIpv6PrefixList] = \
            {'':PrefixListOutput.ShowIpv6PrefixList}

        # Learn the feature
        prefix.learn()      

        # Check specific attribute values
        # info - protocol
        self.assertEqual(prefix.info['prefix_set_name']['test']['protocol'], 'ipv4')
        # info - ipv6 prefix
        self.assertEqual(prefix.info['prefix_set_name']['test6']['prefixes']\
                                  ['2001:db8:3::/64 64..128 permit']['prefix'], '2001:db8:3::/64')

    def test_incomplete_output(self):
        self.maxDiff = None
        prefix = PrefixList(device=self.device)
        # Get outputs
        prefix.maker.outputs[ShowIpPrefixList] = \
            {'':PrefixListOutput.ShowIpPrefixList}

        prefix.maker.outputs[ShowIpv6PrefixList] = {'':''}

        # Learn the feature
        prefix.learn()      

        # Delete missing specific attribute values
        expect_dict = deepcopy(PrefixListOutput.PrefixList_info)
        del(expect_dict['prefix_set_name']['test6'])
                
        # Verify Ops was created successfully
        self.assertEqual(prefix.info, expect_dict)


if __name__ == '__main__':
    unittest.main()
