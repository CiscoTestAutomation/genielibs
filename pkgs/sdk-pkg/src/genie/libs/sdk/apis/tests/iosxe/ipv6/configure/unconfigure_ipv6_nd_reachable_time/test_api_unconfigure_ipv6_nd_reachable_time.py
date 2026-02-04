from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipv6.configure import unconfigure_ipv6_nd_reachable_time
from unittest.mock import Mock


class TestUnconfigureIpv6NdReachableTime(TestCase):

    def test_unconfigure_ipv6_nd_reachable_time(self):
        self.device = Mock()
        result = unconfigure_ipv6_nd_reachable_time(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ipv6 nd reachable-time',)
        )
