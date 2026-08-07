import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    unconfigure_routing_ipv6_route
)


class TestUnconfigureRoutingIpv6Route(unittest.TestCase):

    def test_unconfigure_routing_ipv6_route(self):
        device = Mock()

        result = unconfigure_routing_ipv6_route(
            device,
            '9001::/64',
            'GigabitEthernet5',
            '8001::100'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ipv6 route 9001::/64 GigabitEthernet5 8001::100'],)
        )