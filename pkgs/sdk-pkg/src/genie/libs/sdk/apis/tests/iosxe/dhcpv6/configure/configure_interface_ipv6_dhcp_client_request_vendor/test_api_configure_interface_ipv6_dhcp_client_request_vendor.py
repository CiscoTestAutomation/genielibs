from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_interface_ipv6_dhcp_client_request_vendor
from unittest.mock import Mock


class TestConfigureInterfaceIpv6DhcpClientRequestVendor(TestCase):

    def test_configure_interface_ipv6_dhcp_client_request_vendor(self):
        self.device = Mock()
        result = configure_interface_ipv6_dhcp_client_request_vendor(self.device, 'GigabitEthernet1/0/8')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/8', 'ipv6 dhcp client request vendor'],)
        )
