import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    disable_ipv6_multicast_routing
)


class TestDisableIpv6MulticastRouting(unittest.TestCase):

    def test_disable_ipv6_multicast_routing(self):
        device = Mock()

        result = disable_ipv6_multicast_routing(
            device=device
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ipv6 multicast-routing',)
        )