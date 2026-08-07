import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    unconfigure_routing_ip_route_vrf
)


class TestUnconfigureRoutingIpRouteVrf(unittest.TestCase):

    def test_unconfigure_routing_ip_route_vrf(self):
        device = Mock()

        result = unconfigure_routing_ip_route_vrf(
            device,
            '1.0.0.1',
            '255.0.0.0',
            'UNDERLAY',
            'GigabitEthernet10',
            '11.11.11.2'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ip route vrf UNDERLAY 1.0.0.1 255.0.0.0 GigabitEthernet10 11.11.11.2'],)
        )