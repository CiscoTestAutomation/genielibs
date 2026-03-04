from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ipv6_multicast_routing

class TestUnconfigureIpv6MulticastRouting(TestCase):

    def test_unconfigure_ipv6_multicast_routing(self):
        device = Mock()
        result = unconfigure_ipv6_multicast_routing(device, None)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ipv6 multicast-routing',)
        )

    def test_unconfigure_ipv6_multicast_routing_1(self):
        device = Mock()
        result = unconfigure_ipv6_multicast_routing(device, 'green')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ipv6 multicast-routing vrf green',)
        )