import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    unconfigure_routing_static_routev6
)


class TestUnconfigureRoutingStaticRoutev6(unittest.TestCase):

    def test_unconfigure_routing_static_routev6(self):
        device = Mock()

        result = unconfigure_routing_static_routev6(
            device,
            '24:1::2',
            '64',
            'CLIENT-VRF1v6',
            'tunnel20',
            '25:1::2'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
             (['ipv6 route vrf CLIENT-VRF1v6 24:1::2/64 25:1::2'],)
        )