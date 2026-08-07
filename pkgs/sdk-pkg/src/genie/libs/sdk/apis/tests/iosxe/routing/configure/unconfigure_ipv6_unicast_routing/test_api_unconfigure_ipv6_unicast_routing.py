import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    unconfigure_ipv6_unicast_routing
)


class TestUnconfigureIpv6UnicastRouting(unittest.TestCase):

    def test_unconfigure_ipv6_unicast_routing(self):
        device = Mock()

        result = unconfigure_ipv6_unicast_routing(
            device
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ipv6 unicast-routing',)
        )