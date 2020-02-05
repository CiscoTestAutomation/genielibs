# Python
import unittest

# Ats
from pyats.topology import Device

# Genie package
from genie.ops.base import Base
from genie.ops.base.maker import Maker

from unittest.mock import Mock
# genie.libs
from genie.libs.ops.static_routing.iosxe.static_routing import StaticRouting
from genie.libs.ops.static_routing.iosxe.tests.static_routing_output import StaticRouteOutput

from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail

outputs = {}
outputs['show ip static route'] = StaticRouteOutput.showIpv4StaticRoute_default
outputs['show ip static route vrf VRF1'] = StaticRouteOutput.showIpv4StaticRoute_vrf1
outputs['show ipv6 static detail'] = StaticRouteOutput.showIpv6StaticRoute_default
outputs['show ipv6 static vrf VRF1 detail'] = StaticRouteOutput.showIpv6StaticRoute_vrf1

def mapper(key):
    return outputs[key]

class test_static_route_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_full_static_route(self):
        f = StaticRouting(device=self.device)
        f.maker.outputs[ShowVrfDetail] = {'': StaticRouteOutput.ShowVrfDetail}

        # Get 'show ip static route' output
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        f.learn()

        self.maxDiff = None
        self.assertEqual(f.info, StaticRouteOutput.staticRouteOpsOutput)

    def test_selective_attribute_static_route(self):
        f = StaticRouting(device=self.device)
        f.maker.outputs[ShowVrfDetail] = {'': StaticRouteOutput.ShowVrfDetail}

        # Get 'show ip static route' output
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        f.learn()
        # Check match

        self.assertEqual('GigabitEthernet0/2', f.info['vrf']['VRF1']['address_family']['ipv4']['routes']\
            ['10.36.3.3/32']['next_hop']['outgoing_interface']['GigabitEthernet0/2']['outgoing_interface'])
        # Check does not match
        self.assertNotEqual('GigabitEthernet0/0', f.info['vrf']['VRF1']['address_family']['ipv4']['routes']\
            ['10.36.3.3/32']['next_hop']['outgoing_interface']['GigabitEthernet0/2']['outgoing_interface'])


    def test_missing_attributes_static_route(self):
        f = StaticRouting(device=self.device)
        f.maker.outputs[ShowVrfDetail] = {'': StaticRouteOutput.ShowVrfDetail}

        # Get 'show ip static route' output
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            interfaces = f.info['vrf']['VRF1']['address_family']['ipv4']['routes']\
                ['10.36.3.3/32']['next_hop']['interface']

    def test_empty_output_static_route(self):
        self.maxDiff = None
        f = StaticRouting(device=self.device)
        # Get outputs
        f.maker.outputs[ShowVrfDetail] = {'': {}}

        outputs['show ip static route'] = ''
        outputs['show ip static route vrf VRF1'] = ''
        outputs['show ipv6 static detail'] = ''
        outputs['show ipv6 static vrf VRF1 detail'] = ''

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        f.learn()

        # revert back
        outputs['show ip static route'] = StaticRouteOutput.showIpv4StaticRoute_default
        outputs['show ip static route vrf VRF1'] = StaticRouteOutput.showIpv4StaticRoute_vrf1
        outputs['show ipv6 static detail'] = StaticRouteOutput.showIpv6StaticRoute_default
        outputs['show ipv6 static vrf VRF1 detail'] = StaticRouteOutput.showIpv6StaticRoute_vrf1

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.info['vrf']


if __name__ == '__main__':
    unittest.main()
