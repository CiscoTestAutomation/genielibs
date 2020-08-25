# Python
import unittest

# Ats
from pyats.topology import Device

from unittest.mock import Mock
# genie.libs
from genie.libs.ops.routing.iosxr.routing import Routing
from genie.libs.ops.routing.iosxr.tests.routing_output import RoutingOutput

from genie.libs.parser.iosxr.show_routing import ShowRouteIpv4, ShowRouteIpv6


outputs = {
    'show route ipv4': RoutingOutput.showRouteIpv4,
    'show route vrf all ipv4': RoutingOutput.showRouteVrfAllIpv4,
    'show route ipv6': RoutingOutput.showRouteIpv6,
    'show route vrf all ipv6': RoutingOutput.showRouteVrfAllIpv6,
    'show route ipv4 10.23.90.0': RoutingOutput.showRouteIpv4_route,
    'show route vrf all ipv4 10.23.90.0': RoutingOutput.showRouteVrfAllIpv4_route,
}

def mapper(key):
    return outputs[key]

class test_route_all(unittest.TestCase):
    
    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping = {'cli': 'cli'}
        self.device.connectionmgr.connections['cli'] = self.device

    def test_custom_output(self):
        f = Routing(device=self.device)
        # Get 'show ip static route' output
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        f.learn(address_family='ipv4', route='10.23.90.0', interface='GigabitEthernet0/0/0/1.90')
        self.maxDiff = None
        self.assertEqual(f.info, RoutingOutput.showRouteOpsOutput_custom)

    def test_full_route(self):
        f = Routing(device=self.device)
        # Get 'show ip static route' output
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        f.learn()
        self.maxDiff = None
        self.assertEqual(f.info, RoutingOutput.showRouteOpsOutput)


    def test_selective_attribute_route(self):
        f = Routing(device=self.device)

        # Get 'show ipv4 static route' output
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        f.learn()
        # Check match
        self.maxDiff = None
        self.assertEqual('2001:10:23:120::2/128', f.info['vrf']['default']['address_family']['ipv6']['routes']\
            ['2001:10:23:120::2/128']['route'])

    def test_empty_output_route(self):
        self.maxDiff = None
        f = Routing(device=self.device)

        outputs['show route ipv4'] = ''
        outputs['show route vrf all ipv4'] = ''
        outputs['show route ipv6'] = ''
        outputs['show route vrf all ipv6'] = ''
        outputs['show route ipv4 10.23.90.0'] = ''
        outputs['show route vrf all ipv4 10.23.90.0'] = ''
        # Get outputs
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        f.learn()
        self.maxDiff = None
        outputs['show route ipv4'] = RoutingOutput.showRouteIpv4
        outputs['show route vrf all ipv4'] = RoutingOutput.showRouteVrfAllIpv4
        outputs['show route ipv6'] = RoutingOutput.showRouteIpv6
        outputs['show route vrf all ipv6'] = RoutingOutput.showRouteVrfAllIpv6
        outputs['show route ipv4 10.23.90.0'] = RoutingOutput.showRouteIpv4_route
        outputs['show route vrf all ipv4 10.23.90.0'] = RoutingOutput.showRouteVrfAllIpv4_route
        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.info['vrf']

if __name__ == '__main__':
    unittest.main()
