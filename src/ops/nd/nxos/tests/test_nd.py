# Python
import unittest

# Ats
from ats.topology import Device

# Genie package
from genie.ops.base import Base
from genie.ops.base.maker import Maker

from unittest.mock import Mock
# genie.libs
from genie.libs.ops.nd.nxos.nd import Nd
from genie.libs.ops.nd.nxos.tests.nd_output import NdOutput

from genie.libs.parser.nxos.show_nd import ShowIpv6NeighborDetail,\
                                            ShowIpv6NdInterface,\
                                            ShowIpv6IcmpNeighborDetail,\
                                            ShowIpv6Routers

class test_nd_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_full_nd(self):
        f = Nd(device=self.device)
        f.maker.outputs[ShowIpv6NeighborDetail] = {"{'vrf':'all'}": NdOutput.showIpv6NeighborDetail}
        f.maker.outputs[ShowIpv6NdInterface] = {"{'vrf':'all'}": NdOutput.showIpv6NdInterface}
        f.maker.outputs[ShowIpv6IcmpNeighborDetail] = {"{'vrf':'all'}": NdOutput.showIpv6IcmpNeighborDetail}
        f.maker.outputs[ShowIpv6Routers] = {"{'vrf':'all'}": NdOutput.showIpv6Routers}
        self.device.execute = Mock()
        # Learn the feature
        f.learn()

        self.maxDiff = None
        self.assertEqual(f.info, NdOutput.ndOpsOutput)


    def test_selective_attribute_nd(self):
        f = Nd(device=self.device)
        f.maker.outputs[ShowIpv6NeighborDetail] = {"{'vrf':'all'}": NdOutput.showIpv6NeighborDetail}
        f.maker.outputs[ShowIpv6NdInterface] = {"{'vrf':'all'}": NdOutput.showIpv6NdInterface}
        f.maker.outputs[ShowIpv6IcmpNeighborDetail] = {"{'vrf':'all'}": NdOutput.showIpv6IcmpNeighborDetail}
        f.maker.outputs[ShowIpv6Routers] = {"{'vrf':'all'}": NdOutput.showIpv6Routers}
        # Learn the feature
        f.learn()
        # Check match

        self.assertEqual('other', f.info['interfaces']['Ethernet1/1']['neighbors']['2010:2:3::2']['origin'])
        # Check does not match
        self.assertNotEqual('static', f.info['interfaces']['Ethernet1/1']['neighbors']['2010:2:3::2']['origin'])


    def test_missing_attributes_nd(self):
        f = Nd(device=self.device)
        f.maker.outputs[ShowIpv6NeighborDetail] = {"{'vrf':'all'}": NdOutput.showIpv6NeighborDetail}
        f.maker.outputs[ShowIpv6NdInterface] = {"{'vrf':'all'}": NdOutput.showIpv6NdInterface}
        f.maker.outputs[ShowIpv6IcmpNeighborDetail] = {"{'vrf':'all'}": NdOutput.showIpv6IcmpNeighborDetail}
        f.maker.outputs[ShowIpv6Routers] = {"{'vrf':'all'}": NdOutput.showIpv6Routers}

        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            interfaces = f.info['interfaces']['Etherenet1/1']['neighbors']['2010:2:3::2']

    def test_empty_output_nd(self):
        self.maxDiff = None
        f = Nd(device=self.device)

        # Get outputs
        f.maker.outputs[ShowIpv6NeighborDetail] = {"{'vrf':'all'}": {}}
        f.maker.outputs[ShowIpv6NdInterface] = {"{'vrf':'all'}": {}}
        f.maker.outputs[ShowIpv6IcmpNeighborDetail] = {"{'vrf':'all'}": {}}
        f.maker.outputs[ShowIpv6Routers] = {"{'vrf':'all'}": {}}

        # Learn the feature
        f.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.info['interfaces']


if __name__ == '__main__':
    unittest.main()
