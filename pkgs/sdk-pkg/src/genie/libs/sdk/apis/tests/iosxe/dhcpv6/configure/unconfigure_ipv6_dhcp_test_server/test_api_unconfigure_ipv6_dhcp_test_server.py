from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_ipv6_dhcp_test_server
from unittest.mock import Mock


class TestUnconfigureIpv6DhcpTestServer(TestCase):

    def test_unconfigure_ipv6_dhcp_test_server(self):
        self.device = Mock()
        result = unconfigure_ipv6_dhcp_test_server(self.device, '12223242')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ipv6 dhcp test server add vsio 12223242'],)
        )
