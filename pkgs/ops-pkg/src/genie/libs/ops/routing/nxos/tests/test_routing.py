# Python
import unittest

# Ats
from pyats.topology import Device

# Genie package
from genie.ops.base import Base
from genie.ops.base.maker import Maker

from unittest.mock import Mock
# genie.libs
from genie.libs.ops.routing.nxos.routing import Routing
from genie.libs.ops.routing.nxos.tests.routing_output import RouteOutput

from genie.libs.parser.nxos.show_routing import ShowIpRoute , ShowIpv6Route


class test_route_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_custom_output(self):
        f = Routing(device=self.device)
        # Get outputs
        f.maker.outputs[ShowIpRoute] = {"{'vrf':'VRF1'}": RouteOutput.showIpRoute}
        f.maker.outputs[ShowIpv6Route] = {"{'vrf':'VRF1'}": RouteOutput.showIpv6Route}
        self.device.execute = Mock()
        # Learn the feature
        f.learn(vrf='VRF1')
        self.maxDiff = None
        self.assertEqual(f.info, RouteOutput.routeOpsOutput_custom)

    def test_full_route(self):
        f = Routing(device=self.device)
        # Get outputs
        f.maker.outputs[ShowIpRoute] = {"{'vrf':'all'}": RouteOutput.showIpRoute}
        f.maker.outputs[ShowIpv6Route] = {"{'vrf':'all'}": RouteOutput.showIpv6Route}
        self.device.execute = Mock()
        # Learn the feature
        f.learn()
        self.maxDiff = None
        self.assertEqual(f.info, RouteOutput.routeOpsOutput)


    def test_selective_attribute_route(self):
        f = Routing(device=self.device)

        # Get 'show ipv4 static route' output
        f.maker.outputs[ShowIpRoute] = {"{'vrf':'all'}": RouteOutput.showIpRoute}
        f.maker.outputs[ShowIpv6Route] = {"{'vrf':'all'}": RouteOutput.showIpv6Route}
        # Learn the feature
        f.learn()
        # Check match

        self.assertEqual('local', f.info['vrf']['default']['address_family']['ipv4']['routes']\
            ['10.21.33.33/32']['source_protocol'])
        # Check does not match
        self.assertNotEqual(200, f.info['vrf']['default']['address_family']['ipv4']['routes']\
            ['10.21.33.33/32']['route_preference'])


    def test_missing_attributes_route(self):
        f = Routing(device=self.device)
        f.maker.outputs[ShowIpRoute] = {"{'vrf':'all'}": RouteOutput.showIpRoute}
        f.maker.outputs[ShowIpv6Route] = {"{'vrf':'all'}": RouteOutput.showIpv6Route}

        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            interfaces = f.info['vrf']['VRF1']['address_family']['ipv4']['routes']\
                ['10.36.3.3/32']['next_hop']['interface']

    def test_empty_output_route(self):
        self.maxDiff = None
        f = Routing(device=self.device)

        # Get outputs
        f.maker.outputs[ShowIpRoute] = {"{'vrf':'all'}": {}}
        f.maker.outputs[ShowIpv6Route] = {"{'vrf':'all'}": {}}

        # Learn the feature
        f.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.info['vrf']

if __name__ == '__main__':
    unittest.main()
