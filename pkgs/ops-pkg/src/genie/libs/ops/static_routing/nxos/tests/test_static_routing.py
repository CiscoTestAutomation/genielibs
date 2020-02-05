# Python
import unittest

# Ats
from pyats.topology import Device

# Genie package
from genie.ops.base import Base
from genie.ops.base.maker import Maker

from unittest.mock import Mock
# genie.libs
from genie.libs.ops.static_routing.nxos.static_routing import StaticRouting
from genie.libs.ops.static_routing.nxos.tests.static_routing_output import StaticRouteOutput

from genie.libs.parser.nxos.show_static_routing import ShowIpStaticRoute , ShowIpv6StaticRoute


class test_static_route_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_full_static_route(self):
        f = StaticRouting(device=self.device)
        # Get 'show ip static route' output
        f.maker.outputs[ShowIpStaticRoute] = {'': StaticRouteOutput.showIpv4StaticRoute}
        f.maker.outputs[ShowIpv6StaticRoute] = {'': StaticRouteOutput.showIpv6StaticRoute}
        self.device.execute = Mock()
        # Learn the feature
        f.learn()

        self.maxDiff = None
        self.assertEqual(f.info, StaticRouteOutput.staticRouteOpsOutput)


    def test_selective_attribute_static_route(self):
        f = StaticRouting(device=self.device)

        # Get 'show ipv4 static route' output
        f.maker.outputs[ShowIpStaticRoute] = {'': StaticRouteOutput.showIpv4StaticRoute}
        f.maker.outputs[ShowIpv6StaticRoute] = {'': StaticRouteOutput.showIpv6StaticRoute}
        # Learn the feature
        f.learn()
        # Check match

        self.assertEqual('Null0', f.info['vrf']['VRF1']['address_family']['ipv6']['routes']\
            ['2001:1:1:1::1/128']['next_hop']['outgoing_interface']['Null0']['outgoing_interface'])
        # Check does not match
        self.assertNotEqual(5, f.info['vrf']['VRF1']['address_family']['ipv6']['routes']\
            ['2001:1:1:1::1/128']['next_hop']['next_hop_list'][1]['index'])


    def test_missing_attributes_static_route(self):
        f = StaticRouting(device=self.device)
        f.maker.outputs[ShowIpStaticRoute] = {'': StaticRouteOutput.showIpv4StaticRoute}
        f.maker.outputs[ShowIpv6StaticRoute] = {'': StaticRouteOutput.showIpv6StaticRoute}

        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            interfaces = f.info['vrf']['VRF1']['address_family']['ipv4']['routes']\
                ['10.4.1.1/32']['next_hop']['next_hop_vrf']

    def test_empty_output_static_route(self):
        self.maxDiff = None
        f = StaticRouting(device=self.device)

        # Get outputs
        f.maker.outputs[ShowIpStaticRoute] = {'': {}}
        f.maker.outputs[ShowIpv6StaticRoute] = {'': {}}

        # Learn the feature
        f.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.info['vrf']


if __name__ == '__main__':
    unittest.main()
