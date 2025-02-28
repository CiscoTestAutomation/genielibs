from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_ipv6_dhcp_server_join_all_dhcp_server
from unittest.mock import Mock


class TestUnconfigureIpv6DhcpServerJoinAllDhcpServer(TestCase):

    def test_unconfigure_ipv6_dhcp_server_join_all_dhcp_server(self):
        self.device = Mock()
        result = unconfigure_ipv6_dhcp_server_join_all_dhcp_server(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ipv6 dhcp server join all-dhcp-server',)
        )
