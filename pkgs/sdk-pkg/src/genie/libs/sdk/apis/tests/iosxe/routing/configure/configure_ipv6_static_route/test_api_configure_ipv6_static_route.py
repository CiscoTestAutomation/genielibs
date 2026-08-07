import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    configure_ipv6_static_route
)


class TestConfigureIpv6StaticRoute(unittest.TestCase):

    def test_configure_ipv6_static_route(self):
        device = Mock()

        result = configure_ipv6_static_route(
            device,
            '2001:16:1::0',
            64,
            'tunnel1',
            None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
             (['ipv6 route 2001:16:1::0/64 tunnel1'],)
        )