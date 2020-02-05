# Python
import unittest
from unittest.mock import Mock

# pyats
from pyats.topology import Device

# genie.libs
from genie.libs.ops.nd.nxos.nd import Nd
from genie.libs.ops.nd.nxos.tests.nd_output import NdOutput

from genie.libs.parser.nxos.show_nd import (ShowIpv6NeighborDetail,
                                            ShowIpv6NdInterface,
                                            ShowIpv6IcmpNeighborDetail,
                                            ShowIpv6Routers)

class test_nd_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = self.device
        
    def test_full_nd(self):
        nd = Nd(device=self.device)
        nd.maker.outputs[ShowIpv6NeighborDetail] = {"{'vrf':'all'}": NdOutput.showIpv6NeighborDetail}
        nd.maker.outputs[ShowIpv6NdInterface] = {"{'interface':'','vrf':'all'}": NdOutput.showIpv6NdInterface}
        nd.maker.outputs[ShowIpv6IcmpNeighborDetail] = {"{'interface':'','vrf':'all'}": NdOutput.showIpv6IcmpNeighborDetail}
        nd.maker.outputs[ShowIpv6Routers] = {"{'vrf':'all'}": NdOutput.showIpv6Routers}
        # Learn the feature
        nd.learn()

        self.maxDiff = None
        self.assertEqual(nd.info, NdOutput.ndOpsOutput)

    def test_custom_nd(self):
        nd = Nd(device=self.device)
        nd.maker.outputs[ShowIpv6NeighborDetail] = {"{'vrf':'VRF1'}": NdOutput.showIpv6NeighborDetail_custom}
        nd.maker.outputs[ShowIpv6NdInterface] = {"{'interface':'Ethernet1/2.420','vrf':'VRF1'}": NdOutput.showIpv6NdInterface_custom}
        nd.maker.outputs[ShowIpv6IcmpNeighborDetail] = {"{'interface':'Ethernet1/2.420','vrf':'VRF1'}": NdOutput.showIpv6IcmpNeighborDetail_custom}
        nd.maker.outputs[ShowIpv6Routers] = {"{'vrf':'VRF1'}": NdOutput.showIpv6Routers_custom}

        # Learn the feature
        nd.learn(vrf='VRF1', interface='Ethernet1/2.420')

        self.maxDiff = None
        self.assertEqual(nd.info, NdOutput.ndOpsOutput_custom)

    def test_selective_attribute_nd(self):
        nd = Nd(device=self.device)
        nd.maker.outputs[ShowIpv6NeighborDetail] = {"{'vrf':'all'}": NdOutput.showIpv6NeighborDetail}
        nd.maker.outputs[ShowIpv6NdInterface] = {"{'interface':'','vrf':'all'}": NdOutput.showIpv6NdInterface}
        nd.maker.outputs[ShowIpv6IcmpNeighborDetail] = {"{'interface':'','vrf':'all'}": NdOutput.showIpv6IcmpNeighborDetail}
        nd.maker.outputs[ShowIpv6Routers] = {"{'vrf':'all'}": NdOutput.showIpv6Routers}
        # Learn the feature
        nd.learn()
        # Check match

        self.assertEqual('other', nd.info['interfaces']['Ethernet1/1']['neighbors']['2001:db8:c56d:4::2']['origin'])
        # Check does not match
        self.assertNotEqual('static', nd.info['interfaces']['Ethernet1/1']['neighbors']['2001:db8:c56d:4::2']['origin'])


    def test_missing_attributes_nd(self):
        nd = Nd(device=self.device)
        nd.maker.outputs[ShowIpv6NeighborDetail] = {"{'vrf':'all'}": NdOutput.showIpv6NeighborDetail}
        nd.maker.outputs[ShowIpv6NdInterface] = {"{'interface':'','vrf':'all'}": NdOutput.showIpv6NdInterface}
        nd.maker.outputs[ShowIpv6IcmpNeighborDetail] = {"{'interface':'','vrf':'all'}": NdOutput.showIpv6IcmpNeighborDetail}
        nd.maker.outputs[ShowIpv6Routers] = {"{'vrf':'all'}": NdOutput.showIpv6Routers}

        # Learn the feature
        nd.learn()

        with self.assertRaises(KeyError):
            interfaces = nd.info['interfaces']['Etherenet1/1']['neighbors']['2001:db8:c56d:4::2']

    def test_empty_output_nd(self):
        self.maxDiff = None
        nd = Nd(device=self.device)

        # Get outputs
        nd.maker.outputs[ShowIpv6NeighborDetail] = {"{'vrf':'all'}": {}}
        nd.maker.outputs[ShowIpv6NdInterface] = {"{'interface':'','vrf':'all'}": {}}
        nd.maker.outputs[ShowIpv6IcmpNeighborDetail] = {"{'interface':'','vrf':'all'}": {}}
        nd.maker.outputs[ShowIpv6Routers] = {"{'vrf':'all'}": {}}

        # Learn the feature
        nd.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            nd.info['interfaces']


if __name__ == '__main__':
    unittest.main()
