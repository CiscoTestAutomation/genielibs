import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    enable_ipv6_multicast_routing
)


class TestEnableIpv6MulticastRouting(unittest.TestCase):

    def test_enable_ipv6_multicast_routing(self):
        device = Mock()

        result = enable_ipv6_multicast_routing(
            device=device
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ipv6 multicast-routing',)
        )