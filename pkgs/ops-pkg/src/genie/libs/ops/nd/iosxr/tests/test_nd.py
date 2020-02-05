# Python
import unittest
from unittest.mock import Mock

# Pyats
from pyats.topology import Device

# genie.libs
from genie.libs.ops.nd.iosxr.nd import Nd
from genie.libs.ops.nd.iosxr.tests.nd_output import NdOutput
from genie.libs.parser.iosxr.show_interface import ShowIpv6VrfAllInterface
from genie.libs.parser.iosxr.show_ipv6 import ShowIpv6NeighborsDetail, ShowIpv6Neighbors

outputs = {}

# Set values
outputs['show running-config interface'] = NdOutput.ShowRunInterface
outputs['show running-config interface GigabitEthernet0/0/0/0.390'] = NdOutput.ShowRunInterface_custom


def mapper(key):
    return outputs[key]

class test_nd(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = self.device
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

    def test_full_nd(self):
        self.maxDiff = None
        nd = Nd(device=self.device)
        nd.maker.outputs[ShowIpv6VrfAllInterface] = {"{'interface':'','vrf':'all'}": NdOutput.ShowIpv6VrfAllInterface}
        nd.maker.outputs[ShowIpv6Neighbors] = {"{'interface':'','vrf':'all'}": NdOutput.ShowIpv6Neighbors}
        nd.maker.outputs[ShowIpv6NeighborsDetail] = {"": NdOutput.ShowIpv6NeighborsDetail}

        # Learn the feature
        nd.learn()
        self.assertEqual(nd.info, NdOutput.ndOpsOutput)

    def test_custom_nd(self):
        self.maxDiff = None
        nd = Nd(device=self.device)
        nd.maker.outputs[ShowIpv6VrfAllInterface] = {"{'interface':'GigabitEthernet0/0/0/0.390','vrf':'VRF1'}": NdOutput.ShowIpv6VrfAllInterface}
        nd.maker.outputs[ShowIpv6Neighbors] = {"{'interface':'GigabitEthernet0/0/0/0.390','vrf':'VRF1'}": NdOutput.ShowIpv6Neighbors}
        nd.maker.outputs[ShowIpv6NeighborsDetail] = {"": NdOutput.ShowIpv6NeighborsDetail}

        # Learn the feature
        nd.learn(interface='GigabitEthernet0/0/0/0.390', vrf='VRF1')
        self.assertEqual(nd.info, NdOutput.ndOpsOutput_custom)

    def test_selective_attribute_nd(self):
        nd = Nd(device=self.device)
        nd.maker.outputs[ShowIpv6VrfAllInterface] = {"{'interface':'','vrf':'all'}": NdOutput.ShowIpv6VrfAllInterface}
        nd.maker.outputs[ShowIpv6Neighbors] = {"{'interface':'','vrf':'all'}": NdOutput.ShowIpv6Neighbors}
        nd.maker.outputs[ShowIpv6NeighborsDetail] = {"": NdOutput.ShowIpv6NeighborsDetail}

        # Learn the feature
        nd.learn()

        # Check match
        self.assertEqual('1800', nd.info['interfaces']['GigabitEthernet0/0/0/1.390']['router_advertisement']['lifetime'])
        # Check does not match
        self.assertNotEqual('other', nd.info['interfaces']['GigabitEthernet0/0/0/1.390']['neighbors']['fe80::5c00:40ff:fe02:7']['origin'])

    def test_missing_attributes_nd(self):
        nd = Nd(device=self.device)
        nd.maker.outputs[ShowIpv6VrfAllInterface] = {"{'interface':'','vrf':'all'}": {}}
        nd.maker.outputs[ShowIpv6Neighbors] = {"{'interface':'','vrf':'all'}": NdOutput.ShowIpv6Neighbors}
        nd.maker.outputs[ShowIpv6NeighborsDetail] = {"": NdOutput.ShowIpv6NeighborsDetail}

        # Learn the feature
        nd.learn()

        with self.assertRaises(KeyError):
            nd.info['interfaces']['GigabitEthernet0/0/0/1.420']['router_advertisement']

    def test_empty_output_nd(self):
        self.maxDiff = None
        nd = Nd(device=self.device)

        # Get outputs
        nd.maker.outputs[ShowIpv6VrfAllInterface] = {"{'interface':'','vrf':'all'}": {}}
        nd.maker.outputs[ShowIpv6Neighbors] = {"{'interface':'','vrf':'all'}": {}}
        nd.maker.outputs[ShowIpv6NeighborsDetail] = {"": {}}

        # Learn the feature
        nd.learn()

        # Check attribute not found
        with self.assertRaises(AttributeError):
            nd.info['interfaces']


if __name__ == '__main__':
    unittest.main()
