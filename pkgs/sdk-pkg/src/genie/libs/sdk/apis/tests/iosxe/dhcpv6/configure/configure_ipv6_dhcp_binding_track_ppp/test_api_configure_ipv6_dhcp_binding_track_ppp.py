from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_binding_track_ppp
from unittest.mock import Mock


class TestConfigureIpv6DhcpBindingTrackPpp(TestCase):

    def test_configure_ipv6_dhcp_binding_track_ppp(self):
        self.device = Mock()
        result = configure_ipv6_dhcp_binding_track_ppp(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ipv6 dhcp binding track ppp',)
        )
