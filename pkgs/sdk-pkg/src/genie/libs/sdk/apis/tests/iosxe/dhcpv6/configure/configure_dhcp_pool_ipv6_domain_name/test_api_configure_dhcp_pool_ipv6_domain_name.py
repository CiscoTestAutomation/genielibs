from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_dhcp_pool_ipv6_domain_name
from unittest.mock import Mock

class TestConfigureDhcpPoolIpv6DomainName(TestCase):

    def test_configure_dhcp_pool_ipv6_domain_name(self):
        self.device = Mock()
        configure_dhcp_pool_ipv6_domain_name(self.device, 'DHCPPOOL', 'cisco.com', '2001:100:0:1::1')
        self.assertEqual(self.device.configure.mock_calls[0].args, (['ipv6 dhcp pool DHCPPOOL','domain-name cisco.com','dns-server 2001:100:0:1::1'],))
