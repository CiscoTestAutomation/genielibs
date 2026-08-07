import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    configure_routing_ipv6_route
)


class TestConfigureRoutingIpv6Route(unittest.TestCase):

    def test_configure_routing_ipv6_route(self):
        device = Mock()

        result = configure_routing_ipv6_route(
            device,
            '9001::/64',
            'Tunnel1',
            '8001::100'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ipv6 route 9001::/64 Tunnel1 8001::100'],)
        )