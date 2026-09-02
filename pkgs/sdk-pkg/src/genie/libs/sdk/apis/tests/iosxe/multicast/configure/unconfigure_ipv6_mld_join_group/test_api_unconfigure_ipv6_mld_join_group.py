from unittest import TestCase
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ipv6_mld_join_group
from unittest.mock import Mock


class TestUnconfigureIpv6MldJoinGroup(TestCase):

    def test_unconfigure_ipv6_mld_join_group(self):
        self.device = Mock()
        result = unconfigure_ipv6_mld_join_group(self.device, 'ff0e::1:1:1', 'TwentyFiveGigE1/0/3', '2001:db8:20:20::100')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TwentyFiveGigE1/0/3', 'no ipv6 mld join-group ff0e::1:1:1 include 2001:db8:20:20::100'],)
        )
