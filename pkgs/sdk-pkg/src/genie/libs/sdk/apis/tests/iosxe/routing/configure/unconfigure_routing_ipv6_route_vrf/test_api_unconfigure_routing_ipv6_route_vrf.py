import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    unconfigure_routing_ipv6_route_vrf
)


class TestUnconfigureRoutingIpv6RouteVrf(unittest.TestCase):

    def test_unconfigure_routing_ipv6_route_vrf(self):
        device = Mock()

        result = unconfigure_routing_ipv6_route_vrf(
            device,
            '9001::/64',
            'OVERLAY',
            'GigabitEthernet5',
            '8001::100'
        )

        expected_config = [
            'no ipv6 route vrf OVERLAY 9001::/64 '
            'GigabitEthernet5 8001::100'
        ]

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (expected_config,)
        )
