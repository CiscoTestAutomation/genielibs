# Python
import unittest
from unittest.mock import Mock

# Pyats
from pyats.topology import Device

# genie.libs
from genie.libs.ops.nd.iosxe.nd import Nd
from genie.libs.ops.nd.iosxe.tests.nd_output import NdOutput
from genie.libs.parser.iosxe.show_ipv6 import ShowIpv6Neighbors
from genie.libs.parser.iosxe.show_interface import ShowIpv6Interface


class test_nd(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_full_nd(self):
        self.maxDiff = None
        nd = Nd(device=self.device)
        nd.maker.outputs[ShowIpv6Neighbors] = {"{'interface':'','vrf':''}": NdOutput.ShowIpv6Neighbors}
        nd.maker.outputs[ShowIpv6Interface] = {"{'interface':''}": NdOutput.ShowIpv6Interface}

        # Learn the feature
        nd.learn()
        
        self.assertEqual(nd.info, NdOutput.ndOpsOutput)

    def test_custom_nd(self):
        self.maxDiff = None
        nd = Nd(device=self.device)
        nd.maker.outputs[ShowIpv6Neighbors] = {"{'interface':'GigabitEthernet2.90','vrf':''}": NdOutput.ShowIpv6Neighbors}
        nd.maker.outputs[ShowIpv6Interface] = {"{'interface':'GigabitEthernet2.90'}": NdOutput.ShowIpv6Interface}

        # Learn the feature
        nd.learn(interface='GigabitEthernet2.90', vrf='')

        self.assertEqual(nd.info, NdOutput.ndOpsOutput)

    def test_selective_attribute_nd(self):
        nd = Nd(device=self.device)
        nd.maker.outputs[ShowIpv6Neighbors] = {"{'interface':'','vrf':''}": NdOutput.ShowIpv6Neighbors}
        nd.maker.outputs[ShowIpv6Interface] = {"{'interface':''}": NdOutput.ShowIpv6Interface}

        # Learn the feature
        nd.learn()

        # Check match
        self.assertEqual(200, nd.info['interface']['GigabitEthernet2.90']['router_advertisement']['interval'])
        # Check does not match
        self.assertNotEqual(True, nd.info['interface']['GigabitEthernet2.90']['router_advertisement']['suppress'])

    def test_missing_attributes_nd(self):
        nd = Nd(device=self.device)
        nd.maker.outputs[ShowIpv6Neighbors] = {"{'interface':'','vrf':''}": NdOutput.ShowIpv6Neighbors}
        nd.maker.outputs[ShowIpv6Interface] = {"{'interface':''}": {}}

        # Learn the feature
        nd.learn()

        with self.assertRaises(KeyError):
            nd.info['interface']['GigabitEthernet2.90']['router_advertisement']

    def test_empty_output_nd(self):
        self.maxDiff = None
        nd = Nd(device=self.device)

        # Get outputs
        nd.maker.outputs[ShowIpv6Neighbors] = {"{'interface':'','vrf':''}": {}}
        nd.maker.outputs[ShowIpv6Interface] = {"{'interface':''}": {}}

        # Learn the feature
        nd.learn()

        # Check attribute not found
        with self.assertRaises(AttributeError):
            nd.info['interface']


if __name__ == '__main__':
    unittest.main()
