import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    configure_routing_static_route
)


class TestConfigureRoutingStaticRoute(unittest.TestCase):

    def test_configure_routing_static_route(self):
        device = Mock()

        result = configure_routing_static_route(
            device,
            '7.7.7.0',
            '255.255.255.0',
            None,
            None,
            None,
            True,
            6
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
             (['ip route 7.7.7.0 255.255.255.0 dhcp 6'],)
        )