from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_remember
from unittest.mock import Mock


class TestConfigureIpDhcpRemember(TestCase):

    def test_configure_ip_dhcp_remember(self):
        self.device = Mock()
        result = configure_ip_dhcp_remember(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip dhcp remember',)
        )
