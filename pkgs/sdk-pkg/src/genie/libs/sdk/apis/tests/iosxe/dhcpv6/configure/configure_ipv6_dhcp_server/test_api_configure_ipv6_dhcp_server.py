from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_server
from unittest.mock import Mock


class TestConfigureIpv6DhcpServer(TestCase):

    def test_configure_ipv6_dhcp_server(self):
        self.device = Mock()
        result = configure_ipv6_dhcp_server(self.device, 'join', 'all-dhcp-servers')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 dhcp server join all-dhcp-servers'],)
        )
