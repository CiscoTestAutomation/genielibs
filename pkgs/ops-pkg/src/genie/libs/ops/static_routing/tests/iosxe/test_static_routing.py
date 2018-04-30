# Python
import unittest

# Ats
from ats.topology import Device

# Genie package
from genie.ops.base import Base
from genie.ops.base.maker import Maker

from unittest.mock import Mock
# genie.libs
from genie.libs.ops.static_routing.iosxe.static_routing import StaticRoute
from genie.libs.ops.static_routing.iosxe.tests.static_routing_output import StaticRouteOutput

from genie.libs.parser.iosxe.show_static_routing import ShowIpStaticRoute , ShowIpv6StaticDetail


class test_static_route_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_full_static_route(self):
        f = StaticRoute(device=self.device)
        # Get 'show ip static route' output
        f.maker.outputs[ShowIpStaticRoute] = {'': StaticRouteOutput.showIpv4StaticRoute}
        f.maker.outputs[ShowIpv6StaticDetail] = {'': StaticRouteOutput.showIpv6StaticRoute}
        self.device.execute = Mock()
        # Learn the feature
        f.learn()

        self.maxDiff = None
        self.assertEqual(f.info, StaticRouteOutput.staticRouteOpsOutput)


    def test_selective_attribute_static_route(self):
        f = StaticRoute(device=self.device)

        # Get 'show ipv4 static route' output
        f.maker.outputs[ShowIpStaticRoute] = {'': StaticRouteOutput.showIpv4StaticRoute}
        f.maker.outputs[ShowIpv6StaticDetail] = {'': StaticRouteOutput.showIpv6StaticRoute}
        # Learn the feature
        f.learn()
        # Check match

        self.assertEqual('GigabitEthernet0/2', f.info['vrf']['VRF1']['address_family']['ipv4']['routes']\
            ['3.3.3.3/32']['next_hop']['outgoing_interface']['GigabitEthernet0/2']['outgoing_interface'])
        # Check does not match
        self.assertNotEqual('GigabitEthernet0/0', f.info['vrf']['VRF1']['address_family']['ipv4']['routes']\
            ['3.3.3.3/32']['next_hop']['outgoing_interface']['GigabitEthernet0/2']['outgoing_interface'])


    def test_missing_attributes_static_route(self):
        f = StaticRoute(device=self.device)
        f.maker.outputs[ShowIpStaticRoute] = {'': StaticRouteOutput.showIpv4StaticRoute}
        f.maker.outputs[ShowIpv6StaticDetail] = {'': StaticRouteOutput.showIpv6StaticRoute}

        # Learn the feature
        f.learn()

        with self.assertRaises(KeyError):
            interfaces = f.info['vrf']['VRF1']['address_family']['ipv4']['routes']\
                ['3.3.3.3/32']['next_hop']['interface']

    def test_empty_output_static_route(self):
        self.maxDiff = None
        f = StaticRoute(device=self.device)

        # Get outputs
        f.maker.outputs[ShowIpStaticRoute] = {'': {}}
        f.maker.outputs[ShowIpv6StaticDetail] = {'': {}}

        # Learn the feature
        f.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.info['vrf']


if __name__ == '__main__':
    unittest.main()
