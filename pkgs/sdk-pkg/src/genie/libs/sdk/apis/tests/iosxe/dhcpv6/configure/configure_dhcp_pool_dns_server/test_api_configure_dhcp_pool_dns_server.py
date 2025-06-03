from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_dhcp_pool_dns_server
from unittest.mock import Mock

class TestConfigureDhcpPoolDnsServer(TestCase):

    def test_configure_dhcp_pool_dns_server(self):
        self.device = Mock()
        configure_dhcp_pool_dns_server(self.device, 'ipv6', 'test', '2001::26')
        self.assertEqual(self.device.configure.mock_calls[0].args,  (['ipv6 dhcp pool test', 'dns-server 2001::26'],))
