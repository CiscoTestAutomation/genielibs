from unittest import TestCase
from genie.libs.sdk.apis.iosxe.multicast.configure import configure_ipv6_mld_version
from unittest.mock import Mock


class TestConfigureIpv6MldVersion(TestCase):

    def test_configure_ipv6_mld_version(self):
        self.device = Mock()
        result = configure_ipv6_mld_version(self.device, 'TwentyFiveGigE1/0/3', 2)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TwentyFiveGigE1/0/3', 'ipv6 mld version 2'],)
        )
