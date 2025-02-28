from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_interface_ipv6_dhcp_client_information
from unittest.mock import Mock


class TestConfigureInterfaceIpv6DhcpClientInformation(TestCase):

    def test_configure_interface_ipv6_dhcp_client_information(self):
        self.device = Mock()
        result = configure_interface_ipv6_dhcp_client_information(self.device, 'GigabitEthernet1/0/8', '60')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/8', 'ipv6 dhcp client information refresh minimum 60'],)
        )
