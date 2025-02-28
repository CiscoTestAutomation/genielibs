from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_test_server
from unittest.mock import Mock


class TestConfigureIpv6DhcpTestServer(TestCase):

    def test_configure_ipv6_dhcp_test_server(self):
        self.device = Mock()
        result = configure_ipv6_dhcp_test_server(self.device, '12223242')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 dhcp test server add vsio 12223242'],)
        )
