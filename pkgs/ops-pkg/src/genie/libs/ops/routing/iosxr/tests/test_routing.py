# Python
import unittest

# Ats
from ats.topology import Device

from unittest.mock import Mock
# genie.libs
from genie.libs.ops.routing.iosxr.routing import Routing
from genie.libs.ops.routing.iosxr.tests.routing_output import RoutingOutput

from genie.libs.parser.iosxr.show_routing import ShowRouteIpv4, ShowRouteIpv6


class test_route_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_full_route(self):
        f = Routing(device=self.device)
        # Get 'show ip static route' output
        f.maker.outputs[ShowRouteIpv4] = {'': RoutingOutput.showRouteIpv4}
        f.maker.outputs[ShowRouteIpv6] = {'': RoutingOutput.showRouteIpv6}
        self.device.execute = Mock()
        # Learn the feature
        f.learn()
        self.maxDiff = None
        self.assertEqual(f.info, RoutingOutput.showRouteOpsOutput)


    def test_selective_attribute_route(self):
        f = Routing(device=self.device)

        # Get 'show ipv4 static route' output
        f.maker.outputs[ShowRouteIpv4] = {'': RoutingOutput.showRouteIpv4}
        f.maker.outputs[ShowRouteIpv6] = {'': RoutingOutput.showRouteIpv6}
        # Learn the feature
        f.learn()
        # Check match

        self.assertEqual('2001:1:1:1::1/128', f.info['vrf']['default']['address_family']['ipv6']['routes']\
            ['2001:1:1:1::1/128']['route'])
        # Check does not match
        self.assertNotEqual(5, f.info['vrf']['default']['address_family']['ipv6']['routes']\
            ['2001:1:1:1::1/128']['next_hop']['next_hop_list'][1]['index'])



    def test_missing_attributes_route(self):
        f = Routing(device=self.device)
        f.maker.outputs[ShowRouteIpv4] = {'': RoutingOutput.showRouteIpv4}
        f.maker.outputs[ShowRouteIpv6] = {'': RoutingOutput.showRouteIpv6}

        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            interfaces = f.info['vrf']['VRF1']['address_family']['ipv4']['routes']\
                ['10.4.1.1/32']['next_hop']['next_hop_vrf']

    def test_empty_output_route(self):
        self.maxDiff = None
        f = Routing(device=self.device)

        # Get outputs
        f.maker.outputs[ShowRouteIpv4] = {'': {}}
        f.maker.outputs[ShowRouteIpv6] = {'': {}}

        # Learn the feature
        f.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.info['vrf']

if __name__ == '__main__':
    unittest.main()
