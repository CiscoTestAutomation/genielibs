from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipv6.configure import configure_ipv6_nd_reachable_time
from unittest.mock import Mock


class TestConfigureIpv6NdReachableTime(TestCase):

    def test_configure_ipv6_nd_reachable_time(self):
        self.device = Mock()
        result = configure_ipv6_nd_reachable_time(self.device, 360000)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ipv6 nd reachable-time 360000',)
        )
