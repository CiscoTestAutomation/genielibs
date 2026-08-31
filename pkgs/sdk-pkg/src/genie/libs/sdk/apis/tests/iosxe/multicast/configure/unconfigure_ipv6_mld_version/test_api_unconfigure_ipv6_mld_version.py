from unittest import TestCase
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ipv6_mld_version
from unittest.mock import Mock


class TestUnconfigureIpv6MldVersion(TestCase):

    def test_unconfigure_ipv6_mld_version(self):
        self.device = Mock()
        result = unconfigure_ipv6_mld_version(self.device, 'TwentyFiveGigE1/0/3', 2)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TwentyFiveGigE1/0/3', 'no ipv6 mld version 2'],)
        )
