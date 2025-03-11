from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_ipv6_dhcp_binding_track_ppp
from unittest.mock import Mock


class TestUnconfigureIpv6DhcpBindingTrackPpp(TestCase):

    def test_unconfigure_ipv6_dhcp_binding_track_ppp(self):
        self.device = Mock()
        result = unconfigure_ipv6_dhcp_binding_track_ppp(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ipv6 dhcp binding track ppp',)
        )
