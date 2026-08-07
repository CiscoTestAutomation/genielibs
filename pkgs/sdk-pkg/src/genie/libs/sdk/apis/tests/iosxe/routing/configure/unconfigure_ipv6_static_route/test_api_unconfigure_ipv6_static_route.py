import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    unconfigure_ipv6_static_route
)


class TestUnconfigureIpv6StaticRoute(unittest.TestCase):

    def test_unconfigure_ipv6_static_route(self):
        device = Mock()

        result = unconfigure_ipv6_static_route(
            device,
            '2001:16:1::0',
            '64',
            'Tunnel1',
            None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ipv6 route 2001:16:1::0/64 Tunnel1'],)
        )