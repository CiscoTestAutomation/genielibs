from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_pool_host
from unittest.mock import Mock


class TestUnconfigureIpDhcpPoolHost(TestCase):
    
    def test_unconfigure_ip_dhcp_pool_host(self):
        self.device = Mock()
        unconfigure_ip_dhcp_pool_host(self.device, 'test-pool', '100.10.10.10 255.255.255.0', None, None, 'pi-dhcp-client')
        self.assertEqual(
        self.device.configure.mock_calls[0].args,
        (['ip dhcp pool test-pool','no host 100.10.10.10 255.255.255.0','no client-name pi-dhcp-client'],)
    )