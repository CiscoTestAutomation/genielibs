import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    configure_routing_ipv6_route_vrf
)


class TestConfigureRoutingIpv6RouteVrf(unittest.TestCase):

    def test_configure_routing_ipv6_route_vrf(self):
        device = Mock()

        result = configure_routing_ipv6_route_vrf(
            device,
            '9001::/64',
            'OVERLAY',
            'GigabitEthernet5',
            '8001::100'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ipv6 route vrf OVERLAY 9001::/64 GigabitEthernet5 8001::100'],)
        )